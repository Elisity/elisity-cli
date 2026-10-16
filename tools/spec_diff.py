#!/usr/bin/env python3
"""
Diff two Elisity CCC OpenAPI specs and report what the CLI regeneration will do.

This turns a version bump from a blind regeneration into a reviewable change.
For every operation it answers: is it new, gone, or altered — and what CLI
command does it become?

    python3 tools/spec_diff.py OLD_SPEC NEW_SPEC
    python3 tools/spec_diff.py OLD_SPEC NEW_SPEC --json > diff.json
    python3 tools/spec_diff.py OLD_SPEC NEW_SPEC --strict   # exit 1 on unmapped new tags

Categories reported:
    added        operations present only in NEW
    removed      operations present only in OLD
    changed      same (method, path) but different parameters / request body /
                 responses / tags / operationId / resulting command name
    unchanged    identical
    new tags     tags in NEW that no OLD operation carried. Tags with no
                 TAG_TO_GROUP entry fall back to a path-prefix guess and need a
                 human decision, so they are surfaced separately and loudly.

Operation identity is (METHOD, path). A path rename therefore shows up as a
removal plus an addition, which is the honest reading — the CLI command name
and endpoint both change.
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

# Import the generator's own logic so the diff can never disagree with what
# regeneration actually produces (group mapping, command naming, dedup).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generate_commands import (  # noqa: E402
    HANDCODED_GROUPS,
    TAG_TO_GROUP,
    apply_overlays,
    build_groups,
    dedupe_command_names,
    iter_operations,
    load_spec,
    resolve_group,
)

# Depth cap for $ref expansion. Deep enough for the real CCC schemas, shallow
# enough that a pathological spec can't blow the stack.
MAX_SCHEMA_DEPTH = 8


# --------------------------------------------------------------------------
# Schema normalization
# --------------------------------------------------------------------------


def _resolve_ref(spec: dict, ref: str):
    """Resolve a local '#/a/b/c' JSON pointer. Returns None if unresolvable."""
    if not isinstance(ref, str) or not ref.startswith("#/"):
        return None
    node = spec
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def expand_schema(schema, spec: dict, seen=frozenset(), depth: int = 0):
    """Inline $refs so a change *inside* a referenced schema is visible.

    Comparing raw $ref strings would miss the common real-world case where the
    ref name is stable but the schema behind it gained or lost a field. Cycles
    are replaced with a {"$circular": ref} marker; hitting MAX_SCHEMA_DEPTH
    leaves the ref in place rather than recursing forever.
    """
    if not isinstance(schema, (dict, list)):
        return schema
    if isinstance(schema, list):
        return [expand_schema(item, spec, seen, depth + 1) for item in schema]

    ref = schema.get("$ref")
    if ref:
        if ref in seen:
            return {"$circular": ref}
        if depth >= MAX_SCHEMA_DEPTH:
            return {"$truncated": ref}
        target = _resolve_ref(spec, ref)
        if target is None:
            return {"$unresolved": ref}
        merged = {k: v for k, v in schema.items() if k != "$ref"}
        expanded = expand_schema(target, spec, seen | {ref}, depth + 1)
        if isinstance(expanded, dict):
            out = dict(expanded)
            out.update(merged)
            return out
        return expanded

    return {k: expand_schema(v, spec, seen, depth + 1) for k, v in schema.items()}


def schema_fingerprint(schema) -> str:
    """Stable hash of a schema, insensitive to key ordering."""
    if schema is None:
        return ""
    canonical = json.dumps(schema, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def _schema_required(schema) -> list:
    """Top-level required-field names of a (resolved) object schema."""
    if not isinstance(schema, dict):
        return []
    req = schema.get("required")
    return sorted(req) if isinstance(req, list) else []


def _param_type(param: dict) -> str:
    schema = param.get("schema") or {}
    if not isinstance(schema, dict):
        return "unknown"
    t = schema.get("type")
    if t == "array":
        items = schema.get("items") or {}
        item_t = items.get("type") if isinstance(items, dict) else None
        return f"array[{item_t or 'object'}]"
    if t:
        return t
    if schema.get("$ref"):
        return "object"
    return "unknown"


# --------------------------------------------------------------------------
# Operation descriptors
# --------------------------------------------------------------------------


def describe_operation(spec: dict, path: str, method: str, op: dict,
                       tags: list, op_id: str, command: str) -> dict:
    """Build the comparable descriptor for a single operation."""
    group, matched_by = resolve_group(tags, path)

    params = {}
    for p in op.get("parameters") or []:
        if not isinstance(p, dict):
            continue
        key = f"{p.get('in', '?')}:{p.get('name', '?')}"
        params[key] = {
            "name": p.get("name", ""),
            "in": p.get("in", ""),
            "required": bool(p.get("required", False)),
            "type": _param_type(p),
        }

    request_body = None
    rb = op.get("requestBody")
    if isinstance(rb, dict):
        content = rb.get("content") or {}
        media = {}
        for ct, body in sorted(content.items()):
            resolved = expand_schema((body or {}).get("schema"), spec)
            media[ct] = {
                "fingerprint": schema_fingerprint(resolved),
                "required": _schema_required(resolved),
            }
        request_body = {"required": bool(rb.get("required", False)), "content": media}

    responses = {}
    for code, resp in sorted((op.get("responses") or {}).items()):
        if not isinstance(resp, dict):
            continue
        content = resp.get("content") or {}
        media = {}
        for ct, body in sorted(content.items()):
            resolved = expand_schema((body or {}).get("schema"), spec)
            media[ct] = {"fingerprint": schema_fingerprint(resolved)}
        responses[str(code)] = {"content": media}

    return {
        "method": method.upper(),
        "path": path,
        "tags": list(tags),
        "operationId": op_id,
        "group": group,
        "groupMatchedBy": matched_by,
        "command": command,
        "summary": (op.get("summary") or "").split("\n")[0][:160],
        "parameters": params,
        "requestBody": request_body,
        "responses": responses,
    }


def index_spec(spec: dict) -> dict:
    """Map (METHOD, path) -> descriptor for every operation in a spec.

    Command names come from the generator's own grouping + dedup, so they match
    what regeneration emits.
    """
    groups, _unmapped = build_groups(spec)

    command_by_key = {}
    for group_name, commands in groups.items():
        for method, path, _op, cmd_name in dedupe_command_names(commands):
            command_by_key[(method.upper(), path)] = cmd_name

    index = {}
    for path, method, op, tags, op_id in iter_operations(spec):
        key = (method.upper(), path)
        index[key] = describe_operation(
            spec, path, method, op, tags, op_id, command_by_key.get(key, "")
        )
    return index


def spec_tags(index: dict) -> set:
    tags = set()
    for desc in index.values():
        tags.update(desc["tags"])
    return tags


# --------------------------------------------------------------------------
# Comparison
# --------------------------------------------------------------------------


def diff_parameters(old: dict, new: dict) -> dict:
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = []
    for key in sorted(set(old) & set(new)):
        if old[key] != new[key]:
            changed.append({"parameter": key, "from": old[key], "to": new[key]})
    out = {}
    if added:
        out["added"] = [new[k] for k in added]
    if removed:
        out["removed"] = [old[k] for k in removed]
    if changed:
        out["changed"] = changed
    return out


def diff_request_body(old, new) -> dict:
    if old == new:
        return {}
    if old is None and new is not None:
        return {"status": "added", "to": new}
    if old is not None and new is None:
        return {"status": "removed", "from": old}

    out = {"status": "changed"}
    if old["required"] != new["required"]:
        out["requiredFlag"] = {"from": old["required"], "to": new["required"]}

    old_ct, new_ct = old["content"], new["content"]
    if set(old_ct) != set(new_ct):
        out["contentTypes"] = {
            "added": sorted(set(new_ct) - set(old_ct)),
            "removed": sorted(set(old_ct) - set(new_ct)),
        }

    schema_changes = []
    for ct in sorted(set(old_ct) & set(new_ct)):
        if old_ct[ct] == new_ct[ct]:
            continue
        entry = {"contentType": ct}
        if old_ct[ct]["fingerprint"] != new_ct[ct]["fingerprint"]:
            entry["schemaFingerprint"] = {
                "from": old_ct[ct]["fingerprint"],
                "to": new_ct[ct]["fingerprint"],
            }
        old_req, new_req = old_ct[ct]["required"], new_ct[ct]["required"]
        if old_req != new_req:
            entry["requiredFields"] = {
                "added": sorted(set(new_req) - set(old_req)),
                "removed": sorted(set(old_req) - set(new_req)),
            }
        schema_changes.append(entry)
    if schema_changes:
        out["schema"] = schema_changes
    return out


def diff_responses(old: dict, new: dict) -> dict:
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = []
    for code in sorted(set(old) & set(new)):
        if old[code] == new[code]:
            continue
        entry = {"status": code}
        old_ct, new_ct = old[code]["content"], new[code]["content"]
        if set(old_ct) != set(new_ct):
            entry["contentTypes"] = {
                "added": sorted(set(new_ct) - set(old_ct)),
                "removed": sorted(set(old_ct) - set(new_ct)),
            }
        shapes = [
            {
                "contentType": ct,
                "from": old_ct[ct]["fingerprint"],
                "to": new_ct[ct]["fingerprint"],
            }
            for ct in sorted(set(old_ct) & set(new_ct))
            if old_ct[ct]["fingerprint"] != new_ct[ct]["fingerprint"]
        ]
        if shapes:
            entry["schema"] = shapes
        changed.append(entry)

    out = {}
    if added:
        out["added"] = added
    if removed:
        out["removed"] = removed
    if changed:
        out["changed"] = changed
    return out


def diff_operation(old: dict, new: dict) -> dict:
    """Return the set of changes between two descriptors ({} if equivalent)."""
    changes = {}

    for field in ("tags", "operationId", "group", "command", "groupMatchedBy"):
        if old[field] != new[field]:
            changes[field] = {"from": old[field], "to": new[field]}

    params = diff_parameters(old["parameters"], new["parameters"])
    if params:
        changes["parameters"] = params

    body = diff_request_body(old["requestBody"], new["requestBody"])
    if body:
        changes["requestBody"] = body

    responses = diff_responses(old["responses"], new["responses"])
    if responses:
        changes["responses"] = responses

    return changes


def diff_specs(old_spec: dict, new_spec: dict) -> dict:
    """Full structured diff between two OpenAPI specs."""
    old_index = index_spec(old_spec)
    new_index = index_spec(new_spec)

    old_keys, new_keys = set(old_index), set(new_index)

    added = [new_index[k] for k in sorted(new_keys - old_keys)]
    removed = [old_index[k] for k in sorted(old_keys - new_keys)]

    changed, unchanged = [], 0
    for key in sorted(old_keys & new_keys):
        delta = diff_operation(old_index[key], new_index[key])
        if delta:
            changed.append({
                "method": new_index[key]["method"],
                "path": new_index[key]["path"],
                "command": new_index[key]["command"],
                "group": new_index[key]["group"],
                # The FULL post-change parameter set, not just the delta.
                # gen_changelog needs it to work out which CLI flag the
                # generator actually emits for a parameter: a flag is renamed
                # only when it collides with one the command already owns, so
                # the answer depends on the operation's other parameters.
                "parametersAfter": new_index[key]["parameters"],
                "changes": delta,
            })
        else:
            unchanged += 1

    old_tags, new_tags = spec_tags(old_index), spec_tags(new_index)
    new_tag_names = sorted(new_tags - old_tags)

    # A new tag with no TAG_TO_GROUP entry lands in a group by path-prefix
    # guess. That is exactly the decision a human has to sign off on.
    unmapped_new_tags = []
    for tag in new_tag_names:
        if tag in TAG_TO_GROUP:
            continue
        ops = [d for d in added if tag in d["tags"]]
        if not ops:
            ops = [new_index[k] for k in new_keys if tag in new_index[k]["tags"]]
        fallback_groups = sorted({o["group"] for o in ops})
        unmapped_new_tags.append({
            "tag": tag,
            "operationCount": len(ops),
            "fallbackGroups": fallback_groups,
            "samplePaths": [o["path"] for o in ops[:5]],
        })

    old_groups = {d["group"] for d in old_index.values()}
    new_groups_seen = {d["group"] for d in new_index.values()}

    return {
        "summary": {
            "oldOperationCount": len(old_index),
            "newOperationCount": len(new_index),
            "oldPathCount": len(old_spec.get("paths") or {}),
            "newPathCount": len(new_spec.get("paths") or {}),
            "added": len(added),
            "removed": len(removed),
            "changed": len(changed),
            "unchanged": unchanged,
            "newTags": len(new_tag_names),
            "unmappedNewTags": len(unmapped_new_tags),
            "newGroups": sorted(new_groups_seen - old_groups),
            "handcodedGroups": sorted(HANDCODED_GROUPS),
        },
        "added": added,
        "removed": removed,
        "changed": changed,
        "newTags": new_tag_names,
        "unmappedNewTags": unmapped_new_tags,
    }


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------


def _fmt_change_detail(changes: dict) -> list:
    """Flatten one operation's change dict into readable bullet lines."""
    out = []
    for field in ("operationId", "command", "group", "groupMatchedBy"):
        if field in changes:
            out.append(f"      {field}: {changes[field]['from']!r} -> {changes[field]['to']!r}")
    if "tags" in changes:
        out.append(f"      tags: {changes['tags']['from']} -> {changes['tags']['to']}")

    params = changes.get("parameters", {})
    for p in params.get("added", []):
        req = " (required)" if p["required"] else ""
        out.append(f"      + param {p['in']} {p['name']}: {p['type']}{req}")
    for p in params.get("removed", []):
        out.append(f"      - param {p['in']} {p['name']}: {p['type']}")
    for c in params.get("changed", []):
        f, t = c["from"], c["to"]
        bits = []
        if f["type"] != t["type"]:
            bits.append(f"type {f['type']} -> {t['type']}")
        if f["required"] != t["required"]:
            bits.append(f"required {f['required']} -> {t['required']}")
        out.append(f"      ~ param {c['parameter']}: {', '.join(bits) or 'modified'}")

    body = changes.get("requestBody", {})
    if body:
        status = body.get("status")
        if status == "added":
            out.append("      + request body")
        elif status == "removed":
            out.append("      - request body")
        else:
            if "requiredFlag" in body:
                rf = body["requiredFlag"]
                out.append(f"      ~ request body required: {rf['from']} -> {rf['to']}")
            for ct in body.get("contentTypes", {}).get("added", []):
                out.append(f"      + request content-type {ct}")
            for ct in body.get("contentTypes", {}).get("removed", []):
                out.append(f"      - request content-type {ct}")
            for entry in body.get("schema", []):
                rq = entry.get("requiredFields")
                if rq:
                    if rq["added"]:
                        out.append(f"      + required field(s) {', '.join(rq['added'])} ({entry['contentType']})")
                    if rq["removed"]:
                        out.append(f"      - required field(s) {', '.join(rq['removed'])} ({entry['contentType']})")
                if "schemaFingerprint" in entry and not rq:
                    out.append(f"      ~ request schema changed ({entry['contentType']})")

    responses = changes.get("responses", {})
    for code in responses.get("added", []):
        out.append(f"      + response {code}")
    for code in responses.get("removed", []):
        out.append(f"      - response {code}")
    for entry in responses.get("changed", []):
        for ct in entry.get("contentTypes", {}).get("added", []):
            out.append(f"      + response {entry['status']} content-type {ct}")
        for ct in entry.get("contentTypes", {}).get("removed", []):
            out.append(f"      - response {entry['status']} content-type {ct}")
        for shape in entry.get("schema", []):
            out.append(f"      ~ response {entry['status']} schema changed ({shape['contentType']})")
    return out


def render_text(result: dict, old_label: str, new_label: str) -> str:
    s = result["summary"]
    lines = [
        "=" * 78,
        "OpenAPI spec diff",
        "=" * 78,
        f"  old: {old_label}",
        f"  new: {new_label}",
        "",
        f"  operations: {s['oldOperationCount']} -> {s['newOperationCount']}"
        f"   (paths: {s['oldPathCount']} -> {s['newPathCount']})",
        "",
        f"  SUMMARY  added={s['added']}  removed={s['removed']}  changed={s['changed']}"
        f"  unchanged={s['unchanged']}  new-tags={s['newTags']}"
        f"  unmapped-new-tags={s['unmappedNewTags']}",
        "",
    ]

    if result["unmappedNewTags"]:
        lines += [
            "!" * 78,
            "!! NEW TAGS WITH NO TAG_TO_GROUP MAPPING — HUMAN DECISION REQUIRED",
            "!!",
            "!! These fell back to a path-prefix guess. Add an explicit entry to",
            "!! TAG_TO_GROUP in generate_commands.py before regenerating.",
            "!" * 78,
        ]
        for t in result["unmappedNewTags"]:
            lines.append(f"  TAG {t['tag']!r}  ({t['operationCount']} operation(s))")
            lines.append(f"      fallback group(s): {', '.join(t['fallbackGroups']) or '(none)'}")
            for p in t["samplePaths"]:
                lines.append(f"      e.g. {p}")
        lines.append("")
    elif result["newTags"]:
        lines.append(f"  New tags (all already mapped): {', '.join(result['newTags'])}")
        lines.append("")

    if s["newGroups"]:
        lines.append(f"  NEW CLI GROUPS: {', '.join(s['newGroups'])}")
        lines.append("")

    lines.append(f"ADDED OPERATIONS ({len(result['added'])})")
    lines.append("-" * 78)
    if not result["added"]:
        lines.append("  (none)")
    for d in result["added"]:
        lines.append(f"  + {d['method']:6} {d['path']}")
        lines.append(f"      tag={', '.join(d['tags'])}  operationId={d['operationId']}")
        lines.append(f"      -> elisity {d['group']} {d['command']}")
    lines.append("")

    lines.append(f"REMOVED OPERATIONS ({len(result['removed'])})")
    lines.append("-" * 78)
    if not result["removed"]:
        lines.append("  (none)")
    for d in result["removed"]:
        lines.append(f"  - {d['method']:6} {d['path']}")
        lines.append(f"      was: elisity {d['group']} {d['command']}")
    lines.append("")

    lines.append(f"CHANGED OPERATIONS ({len(result['changed'])})")
    lines.append("-" * 78)
    if not result["changed"]:
        lines.append("  (none)")
    for c in result["changed"]:
        lines.append(f"  ~ {c['method']:6} {c['path']}")
        lines.append(f"      elisity {c['group']} {c['command']}")
        lines.extend(_fmt_change_detail(c["changes"]))
    lines.append("")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Diff two CCC OpenAPI specs and report the CLI impact."
    )
    parser.add_argument("old_spec", help="Path to the baseline OpenAPI JSON spec")
    parser.add_argument("new_spec", help="Path to the new OpenAPI JSON spec")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    parser.add_argument(
        "--overlay",
        action="append",
        default=[],
        metavar="PATH",
        help="Spec overlay to apply to the NEW spec (repeatable), exactly as "
             "generate_commands.py --overlay does",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if new tags have no TAG_TO_GROUP mapping",
    )
    args = parser.parse_args(argv)

    old_spec = load_spec(args.old_spec)
    new_spec, overlay_notes = apply_overlays(load_spec(args.new_spec), args.overlay)
    for note in overlay_notes:
        print(f"Spec overlay: {note}", file=sys.stderr)
    result = diff_specs(old_spec, new_spec)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(render_text(result, args.old_spec, args.new_spec))

    if args.strict and result["unmappedNewTags"]:
        print(
            f"STRICT: {len(result['unmappedNewTags'])} new tag(s) need a "
            "TAG_TO_GROUP mapping.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
