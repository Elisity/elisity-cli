#!/usr/bin/env python3
"""Render a command-level changelog from a spec_diff.py --json report.

Mike's requirement for the 26.7 bump was that the README say *what commands
were added or changed*, not just carry refreshed totals. A hand-maintained list
of 192 additions drifts the moment anyone regenerates, so this renders it from
the diff instead: `spec_diff.py --json` is the input, markdown is the output,
and the next CCC bump is the same one command.

    python3 tools/spec_diff.py old.json new.json --json > diff.json
    python3 tools/gen_changelog.py --diff diff.json --version 26.7 \
        --source insights-demo.idp01.elisity.io > changelog.md

Changes are split by whether they can break a caller, which is the distinction
a reader actually needs:

* **Signature** changes alter the command's flags — a script can stop working.
* **Request body** changes alter the JSON passed to `--body`/`--body-file`.
  The generator emits the body as one opaque JSON option rather than per-field
  flags, so these never change the command's signature, but they do change what
  a caller must send.
* **Response-only** changes cannot break an invocation at all, so they are
  counted rather than enumerated.

Reconciliation
--------------
`spec_diff.py` keys operations by `(METHOD, path)`, so a surviving operation
whose PATH was renamed shows up as one removal plus one addition — while the
command name, derived from the operationId, never changed. Rendered naively that
produces a "Removed (breaking)" section listing commands that still exist, an
"Added" section listing the same commands, and — worst of the three — it hides a
genuine break: `/devices/attributes/trustAttributes/values` became
`/devices/attributes/{attributeName}/values`, which made a positional argument
MANDATORY. A reader looking for migration guidance finds the command under
"Removed" and gets none.

So the diff is reconciled by `(group, command)` before anything is rendered: an
entry appearing on both sides is a path/operation move, is dropped from both
lists, and is emitted under "Changed command signatures" with its real delta.

A third shape needs its own section. `/api/policy/v1/state` really was deleted
from the spec — but `/api/state-sync/v1/state` survived and, with the name it
was competing with now free, took over `policy get-state`. So the command name
still resolves and quietly calls a **different endpoint**. "Any script invoking
one will now fail with `No such command`" is not merely wrong there; it is
backwards. Nothing fails, and that is the problem.

Flags, not spec names
---------------------
A parameter's CLI flag is not always `--<spec name>`: the generator renames it
when it would collide with a flag the command already owns, and a path parameter
is a positional argument with no flag at all. This module resolves the emitted
name through the generator's own `resolve_parameter_names()`. Rendering the raw
spec name advertised `--format` on `devices export-devices`, where `--format` is
the CLI's own output-format override — `--format csv` was silently absorbed and
never sent, at exit 0. The flag that works is `--format-param`.
"""

import argparse
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generate_commands import resolve_parameter_names  # noqa: E402
from tools.spec_diff import diff_parameters  # noqa: E402


def _load(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def _describe(op: dict) -> str:
    """One-line description of an operation, sourced only from the spec.

    Falls back to `METHOD /path` when the spec carries no summary — inventing a
    description would put words in the API's mouth.
    """
    summary = (op.get("summary") or "").strip()
    if summary:
        # Keep it to one line; some CCC summaries embed newlines.
        return " ".join(summary.split())
    return f"`{op['method']} {op['path']}`"


def _classify_change(entry: dict) -> str:
    """Bucket a changed operation: signature | body | response-only.

    Gaining or losing a request body is a SIGNATURE change, not a body change:
    it adds or removes the `--body` / `--body-file` options, so a script that
    passed `--body` to an operation that no longer takes one now fails on an
    unknown option. Only a body that changed SHAPE leaves the flags alone.

    Zero instances between 26.3 and 26.7, so nothing is re-filed today — but the
    next bump runs the same tool.
    """
    changes = entry.get("changes", {})
    if "parameters" in changes or "command" in changes or "group" in changes:
        return "signature"
    if "path" in changes:
        return "signature"
    body = changes.get("requestBody")
    if body:
        if body.get("status") in ("added", "removed"):
            return "signature"
        return "body"
    return "response-only"


def _emitted_names(entry: dict) -> dict:
    """{spec parameter name: how the CLI actually spells it}.

    Resolved through the generator's own `resolve_parameter_names()`, in the
    context of the whole operation, because a flag is renamed only when it
    collides with one the command already owns. A path parameter has no flag —
    it is a positional argument, rendered in the upper case Click shows in the
    usage line.
    """
    parameters = entry.get("parametersAfter") or {}
    method = entry.get("method", "GET")
    path = entry.get("path", "")

    path_params, query_params, header_params = [], [], []
    for spec in parameters.values():
        if spec.get("in") == "path":
            path_params.append((spec["name"], spec.get("type") or "str", ""))
        elif spec.get("in") == "query":
            query_params.append((
                spec["name"], spec.get("type") or "str",
                bool(spec.get("required")), "", None,
            ))
        elif spec.get("in") == "header" and spec.get("required"):
            header_params.append((spec["name"], spec.get("type") or "str", True, "", None))

    names = {}
    if path_params or query_params or header_params:
        resolved_path, resolved_query = resolve_parameter_names(
            method, path_params, query_params, path, header_params
        )
        for spec in resolved_path:
            names[spec["spec_name"]] = spec["dest"].upper()
        for spec in resolved_query:
            names[spec["spec_name"]] = spec["flag"]
    return names


def _render_param(name: str, spec: dict, emitted: dict) -> str:
    """How a caller must actually spell this parameter on the command line."""
    shown = emitted.get(name)
    if shown:
        note = "" if shown.lstrip("-") == name else f" (sends `{name}`)"
        return f"`{shown}`{note}"
    if (spec or {}).get("in") == "path":
        return f"positional `{name.upper()}`"
    return f"`--{name}`"


def _signature_detail(entry: dict) -> str:
    """Human phrasing of what changed about a command's signature."""
    changes = entry.get("changes", {})
    emitted = _emitted_names(entry)
    bits = []

    renamed = changes.get("command")
    if renamed:
        bits.append(f"renamed from `{renamed['from']}`")

    moved = changes.get("group")
    if moved:
        bits.append(f"moved from `{moved['from']}` to `{moved['to']}`")

    path_move = changes.get("path")
    if path_move:
        bits.append(f"path moved from `{path_move['from']}` to `{path_move['to']}`")

    body = changes.get("requestBody") or {}
    if body.get("status") == "added":
        bits.append("now takes a request body (`--body` / `--body-file`)")
    elif body.get("status") == "removed":
        bits.append("no longer takes a request body (`--body` / `--body-file` are gone)")

    params = changes.get("parameters") or {}
    for p in params.get("added", []):
        req = "required" if p.get("required") else "optional"
        bits.append(
            f"new {req} {_render_param(p['name'], p, emitted)} "
            f"({_type_label(p.get('type'))})"
        )
    for p in params.get("removed", []):
        bits.append(f"dropped {_render_param(p['name'], p, emitted)}")
    for p in params.get("changed", []):
        # spec_diff emits {"parameter": "query:size", "from": {...}, "to": {...}}
        old, new = p.get("from") or {}, p.get("to") or {}
        name = new.get("name") or old.get("name") or p.get("parameter", "?")
        shown = _render_param(name, new or old, emitted)
        if old.get("type") != new.get("type"):
            bits.append(
                f"{shown} {_type_label(old.get('type'))} -> "
                f"{_type_label(new.get('type'))}"
            )
        if old.get("required") != new.get("required"):
            became = "required" if new.get("required") else "optional"
            bits.append(f"{shown} became {became}")

    return "; ".join(bits) or "parameters changed"


def reconcile(added: list, removed: list, changed: list) -> tuple:
    """Fold removed-and-added-under-the-same-name pairs into signature changes.

    spec_diff keys by (METHOD, path); the CLI keys by (group, command). An
    operation whose path was renamed is one removal plus one addition to the
    former and a plain signature change to the latter. Reconciling here rather
    than in spec_diff keeps the diff a faithful record of the SPEC and makes
    this module responsible for the CLI's view of it.
    Returns (added, removed, changed, takenOver).
    """
    removed_by_command = {(op["group"], op["command"]): op for op in removed}
    added_by_command = {(op["group"], op["command"]): op for op in added}
    changed_by_command = {(op["group"], op["command"]): op for op in changed}
    moved_keys = set(removed_by_command) & set(added_by_command)
    # A removed operation whose command NAME is now carried by a surviving
    # operation. The name still resolves; it calls something else.
    taken_over = [
        {"before": removed_by_command[key], "after": changed_by_command[key]}
        for key in sorted(set(removed_by_command) & set(changed_by_command))
    ]
    if not moved_keys and not taken_over:
        return added, removed, changed, []

    taken_keys = {(t["before"]["group"], t["before"]["command"]) for t in taken_over}
    still_added = [op for op in added if (op["group"], op["command"]) not in moved_keys]
    still_removed = [
        op for op in removed
        if (op["group"], op["command"]) not in moved_keys | taken_keys
    ]

    moved = []
    for key in sorted(moved_keys):
        before, after = removed_by_command[key], added_by_command[key]
        entry_changes = {}
        if before["path"] != after["path"]:
            entry_changes["path"] = {"from": before["path"], "to": after["path"]}
        if before["method"] != after["method"]:
            entry_changes["method"] = {"from": before["method"], "to": after["method"]}
        params = diff_parameters(before["parameters"], after["parameters"])
        if params:
            entry_changes["parameters"] = params
        body = _body_status(before.get("requestBody"), after.get("requestBody"))
        if body:
            entry_changes["requestBody"] = body
        moved.append({
            "method": after["method"],
            "path": after["path"],
            "command": after["command"],
            "group": after["group"],
            "parametersAfter": after["parameters"],
            "changes": entry_changes or {"path": {"from": before["path"],
                                                  "to": after["path"]}},
        })

    return still_added, still_removed, changed + moved, taken_over


def _body_status(before, after):
    if before == after:
        return {}
    if before is None and after is not None:
        return {"status": "added"}
    if before is not None and after is None:
        return {"status": "removed"}
    return {"status": "changed"}


def _type_label(t) -> str:
    """Render a spec_diff parameter type for humans.

    spec_diff reports `unknown` when the parameter's schema carries no `type`
    key at all. That is not a mystery type — the generator can only treat it as
    a string — so say so, because "unknown -> integer" reads like a tooling gap
    when it is really the spec gaining a type it was always missing.
    """
    if t in (None, "", "unknown"):
        return "untyped (sent as string)"
    return str(t)


def render(diff: dict, version: str, source: str, baseline: str) -> str:
    summary = diff.get("summary", {})
    added, removed, changed, taken_over = reconcile(
        diff.get("added", []), diff.get("removed", []), diff.get("changed", [])
    )

    out = []
    w = out.append

    w(f"## What changed in CCC {version}")
    w("")
    w(
        f"The command set is generated from the CCC {version} OpenAPI spec, pulled from "
        f"`{source}`. The previous set came from the {baseline} spec."
    )
    w("")
    w(
        f"| | {baseline} | {version} |\n"
        f"|---|---:|---:|\n"
        f"| Spec paths | {summary.get('oldPathCount', '?')} | {summary.get('newPathCount', '?')} |\n"
        f"| Spec operations | {summary.get('oldOperationCount', '?')} | {summary.get('newOperationCount', '?')} |"
    )
    w("")
    w(
        f"**{len(added)} commands added, {len(removed)} removed, "
        f"{len(changed)} operations changed"
        + (f", {len(taken_over)} command name(s) repointed at a different endpoint.**"
           if taken_over else ".**")
    )
    w("")

    # ---- Removed: breaking, so it leads. -------------------------------
    w("### Removed commands (breaking)")
    w("")
    if not removed:
        w("None.")
    else:
        w(
            ("This command is gone" if len(removed) == 1
             else f"These {len(removed)} commands are gone")
            + " because the operation was removed "
            "from the CCC spec. Any script invoking one will now fail with "
            "`No such command`. Commands whose underlying *path* moved are not "
            "listed here — they still exist, and are under "
            "[Changed command signatures](#changed-command-signatures)."
        )
        w("")
        by_tag = collections.defaultdict(list)
        for op in removed:
            by_tag[(op.get("tags") or ["untagged"])[0]].append(op)
        for tag in sorted(by_tag):
            ops = sorted(by_tag[tag], key=lambda o: o["command"])
            w(f"**{tag}** ({len(ops)})")
            w("")
            for op in ops:
                w(f"- `elisity {op['group']} {op['command']}` — {_describe(op)}")
            w("")
    w("")

    # ---- Name takeovers: the quiet one, so it gets its own section. -----
    if taken_over:
        w("### Command names now pointing at a different endpoint (breaking, silent)")
        w("")
        w(
            f"{len(taken_over)} command name(s) survived the bump while the operation "
            "behind them did not. The old operation was deleted from the spec and a "
            "different surviving operation inherited the name, so **an existing script "
            "does not fail — it calls a different endpoint.** These are worth checking "
            "before anything else in this changelog."
        )
        w("")
        for entry in taken_over:
            before, after = entry["before"], entry["after"]
            w(
                f"- `elisity {before['group']} {before['command']}` — was "
                f"`{before['method']} {before['path']}` (deleted from the spec), now "
                f"`{after['method']} {after['path']}`"
            )
            detail = _signature_detail(after)
            if detail and detail != "parameters changed":
                w(f"  - the surviving operation also changed: {detail}")
        w("")
    w("")

    # ---- Renames / signature changes: also breaking. --------------------
    sig = [c for c in changed if _classify_change(c) == "signature"]
    body = [c for c in changed if _classify_change(c) == "body"]
    resp = [c for c in changed if _classify_change(c) == "response-only"]

    w("### Changed command signatures")
    w("")
    if not sig:
        w("None.")
    else:
        w(
            f"{len(sig)} commands changed shape — a renamed command or a changed flag "
            "can break an existing script."
        )
        w("")
        by_group = collections.defaultdict(list)
        for c in sig:
            by_group[c["group"]].append(c)
        for group in sorted(by_group):
            w(f"**`{group}`**")
            w("")
            for c in sorted(by_group[group], key=lambda x: x["command"]):
                w(f"- `elisity {group} {c['command']}` — {_signature_detail(c)}")
            w("")
    w("")

    w("### Changed request bodies")
    w("")
    if not body:
        w("None.")
    else:
        w(
            f"{len(body)} commands take a different request body. The command's flags are "
            "unchanged — the body is passed as opaque JSON via `--body` / `--body-file` — "
            "but the JSON you send must match the new schema."
        )
        w("")
        by_group = collections.defaultdict(list)
        for c in body:
            by_group[c["group"]].append(c)
        for group in sorted(by_group):
            cmds = ", ".join(f"`{c['command']}`" for c in sorted(by_group[group], key=lambda x: x["command"]))
            w(f"- **`{group}`** — {cmds}")
        w("")
    w("")

    if resp:
        w(
            f"A further {len(resp)} operations changed only in their response schema or "
            "status codes. Invocation is unaffected, so they are not listed."
        )
        w("")

    # ---- Added. ---------------------------------------------------------
    w("### Added commands")
    w("")
    if not added:
        w("None.")
    else:
        w(f"{len(added)} new commands, grouped by CLI group.")
        w("")
        by_group = collections.defaultdict(list)
        for op in added:
            by_group[op["group"]].append(op)
        for group in sorted(by_group):
            ops = sorted(by_group[group], key=lambda o: o["command"])
            w(f"#### `{group}` (+{len(ops)})")
            w("")
            for op in ops:
                w(f"- `{op['command']}` — {_describe(op)}")
            w("")

    return "\n".join(out).rstrip() + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--diff", required=True, help="spec_diff.py --json output")
    ap.add_argument("--version", required=True, help="New CCC version, e.g. 26.7")
    ap.add_argument("--source", required=True, help="Tenant the spec was pulled from")
    ap.add_argument("--baseline", default="previous", help="Previous CCC version label")
    args = ap.parse_args(argv)

    sys.stdout.write(render(_load(args.diff), args.version, args.source, args.baseline))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
