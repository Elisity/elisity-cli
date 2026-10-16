#!/usr/bin/env python3
"""
Authoritative command-count audit for the Elisity CLI.

Walks the source tree, counts what is actually there, and cross-checks every
numeric claim in README.md against it. Exits non-zero on any disagreement, so
documentation drift fails the build instead of accumulating silently.

    python3 tools/audit_counts.py            # human-readable, exit 1 on drift
    python3 tools/audit_counts.py --json     # machine-readable
    python3 tools/audit_counts.py --no-readme-check

The source tree is the source of truth. When this script and README.md
disagree, README.md is the thing that is wrong.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from generate_commands import (  # noqa: E402
    DESTRUCTIVE_NAME_WORDS,
    HANDCODED_GROUPS,
    is_destructive_operation,
)

COMMANDS_DIR = REPO_ROOT / "src" / "elisity_cli" / "commands"
MAIN_PY = REPO_ROOT / "src" / "elisity_cli" / "main.py"
README = REPO_ROOT / "README.md"
COMMAND_REFERENCE = REPO_ROOT / "docs" / "command-reference.md"

# The confirmation guard the generator emits for every destructive operation.
CONFIRM_MARKER = "Use --confirm"

# Commands whose NAME reads destructive while their path does not classify as
# destructive. Each is a deliberate human ruling, not an emergent property of
# the matcher — an entry here is a statement that the operation destroys
# nothing. Anything name-flagged and absent from this list is an invariant
# failure, so a future `bulk-nuke-sites` on an unrecognised path cannot slip
# through the gap between the name and the path.
NON_DESTRUCTIVE_DESPITE_NAME = {
    "topology validate-virtual-edge-bulk-delete":
        "POST .../virtual-edges/bulk/delete/validate — dry run. Reports what a "
        "bulk delete WOULD do and changes nothing.",
    "topology validate-virtual-edge-node-bulk-delete":
        "POST .../virtual-edge-nodes/bulk/delete/validate — dry run, as above.",
}

# Hand-coded groups are classified by hand because they have no generated
# endpoint line to re-derive from. Stated rather than assumed:
#   reporting — 17 commands, all POSTs to the GraphQL endpoint that read
#               metrics, plus `query`, a raw-body escape hatch. Nothing deletes.
#               `query` is deliberately ungated: it forwards an operator-supplied
#               GraphQL document, so the CLI cannot classify what it does.
#   glossary  — 3 commands, local JSON lookups, no API call at all.
HANDCODED_DESTRUCTIVE_COMMANDS = {}


def split_command_blocks(source: str, decorator: str = "@group.command(") -> list:
    """Split a module into one text block per command, keyed by command name."""
    blocks = []
    for chunk in source.split(decorator)[1:]:
        name_match = re.match(r'\s*["\']([^"\']+)["\']', chunk)
        blocks.append((name_match.group(1) if name_match else "<unnamed>", chunk))
    return blocks


VERB_RE = re.compile(r"client\.(get|get_ndjson|post|put|patch|delete)\(")
ENDPOINT_RE = re.compile(r'endpoint = f?"([^"]+)"')


def describe_command(block: str) -> tuple:
    """(verb, path) as the SHIPPED command will actually call the API.

    Re-derived from the generated source rather than from the spec, so the audit
    measures the artifact users run. `get_ndjson` is a GET with streaming
    decode.
    """
    verb = VERB_RE.search(block)
    endpoint = ENDPOINT_RE.search(block)
    verb = {"get_ndjson": "get"}.get(verb.group(1), verb.group(1)) if verb else ""
    return verb.upper(), (endpoint.group(1) if endpoint else "")


def name_looks_destructive(cmd_name: str) -> bool:
    return bool(set(re.split(r"[^a-z]+", cmd_name)) & DESTRUCTIVE_NAME_WORDS)


def audit_group_modules() -> dict:
    """Count commands and confirm-gate coverage per command-group module.

    The denominator is every DESTRUCTIVE command, not every DELETE command.
    Keying it on the verb is what let this script certify "coverage 100.0%"
    while ten destructive POST/PUT commands — four of them added by the 26.7
    bump, including a bulk force-delete of VENs — shipped with no gate at all.
    A coverage metric measured over a narrower set than the thing it claims to
    cover is worse than no metric: it actively reports safety.
    """
    groups = {}
    for path in sorted(COMMANDS_DIR.glob("*.py")):
        if path.name == "__init__.py":
            continue
        source = path.read_text()
        blocks = split_command_blocks(source)
        handcoded = path.stem in HANDCODED_GROUPS
        destructive, gated, ungated, over_gated, unruled = 0, 0, [], [], []

        for cmd_name, block in blocks:
            qualified = f"{path.stem} {cmd_name}"
            is_gated = CONFIRM_MARKER in block
            if handcoded:
                # No generated endpoint line to re-derive from; classified by
                # the explicit table above so the coverage claim stays honest.
                is_destructive = qualified in HANDCODED_DESTRUCTIVE_COMMANDS
            else:
                verb, endpoint = describe_command(block)
                is_destructive = bool(verb) and is_destructive_operation(verb, endpoint)
                if (
                    not is_destructive
                    and name_looks_destructive(cmd_name)
                    and qualified not in NON_DESTRUCTIVE_DESPITE_NAME
                ):
                    unruled.append(f"{qualified} ({verb} {endpoint})")

            if is_destructive:
                destructive += 1
                if is_gated:
                    gated += 1
                else:
                    ungated.append(qualified)
            elif is_gated:
                over_gated.append(qualified)

        groups[path.stem] = {
            "commands": len(blocks),
            "kind": "hand-coded" if handcoded else "generated",
            "destructiveCommands": destructive,
            "gatedDestructive": gated,
            "ungatedDestructive": ungated,
            "gatedButNotClassifiedDestructive": over_gated,
            "nameDestructivePathNot": unruled,
        }
    return groups


def audit_native_groups() -> dict:
    """Count the CLI-native groups defined inline in main.py (auth, config)."""
    source = MAIN_PY.read_text()
    return {
        "auth": len(split_command_blocks(source, "@auth_group.command(")),
        "config": len(split_command_blocks(source, "@config_group.command(")),
    }


def audit_registration(group_modules: dict) -> dict:
    """Confirm every module on disk is registered in COMMAND_GROUPS, and vice versa."""
    init_source = (COMMANDS_DIR / "__init__.py").read_text()
    registered = set(re.findall(r'^\s*"([a-z_]+)",\s*$', init_source, re.MULTILINE))
    on_disk = set(group_modules)
    return {
        "registered": sorted(registered),
        "onDiskNotRegistered": sorted(on_disk - registered),
        "registeredNotOnDisk": sorted(registered - on_disk),
    }


def collect_counts() -> dict:
    group_modules = audit_group_modules()
    native = audit_native_groups()

    generated = sum(g["commands"] for g in group_modules.values() if g["kind"] == "generated")
    handcoded = sum(g["commands"] for g in group_modules.values() if g["kind"] == "hand-coded")
    group_total = generated + handcoded
    native_total = sum(native.values())

    destructive_commands = sum(g["destructiveCommands"] for g in group_modules.values())
    gated = sum(g["gatedDestructive"] for g in group_modules.values())
    ungated = [n for g in group_modules.values() for n in g["ungatedDestructive"]]
    over_gated = [
        n for g in group_modules.values() for n in g["gatedButNotClassifiedDestructive"]
    ]
    unruled = [n for g in group_modules.values() for n in g["nameDestructivePathNot"]]

    per_group = {name: g["commands"] for name, g in group_modules.items()}
    per_group.update(native)

    return {
        "perGroup": per_group,
        "groupModules": group_modules,
        "nativeGroups": native,
        "registration": audit_registration(group_modules),
        "totals": {
            "generated": generated,
            "handcodedGroups": handcoded,
            "groupCommands": group_total,
            "cliNativeAuthConfig": native_total,
            "total": group_total + native_total,
            "groupCount": len(per_group),
        },
        "confirmGate": {
            "destructiveCommands": destructive_commands,
            "gatedDestructive": gated,
            "ungatedDestructive": sorted(ungated),
            "gatedButNotClassifiedDestructive": sorted(over_gated),
            "nameDestructivePathNot": sorted(unruled),
            "ruledNonDestructiveDespiteName": sorted(NON_DESTRUCTIVE_DESPITE_NAME),
            "coveragePercent": (
                round(100.0 * gated / destructive_commands, 2)
                if destructive_commands else 100.0
            ),
        },
    }


# --------------------------------------------------------------------------
# README cross-check
# --------------------------------------------------------------------------


def _normalize(text: str) -> str:
    """Collapse whitespace and markdown blockquote wrapping.

    Lets a single regex match a claim that the source file wraps across lines
    (`> **463 commands** total: 436 auto-generated REST + 20 hand-coded\n> GraphQL`).
    """
    return re.sub(r"\s+", " ", re.sub(r"\n\s*>", " ", text))


def _readme_claims(counts: dict) -> list:
    """(label, regex, expected) for every numeric claim README.md makes.

    Each regex must have exactly one capture group holding the number.
    """
    t = counts["totals"]
    g = counts["perGroup"]
    claims = [
        ("intro: REST endpoints from spec",
         r"all (\d+) REST endpoints from the OpenAPI spec", t["generated"]),
        ("intro: hand-coded GraphQL commands",
         r"(\d+) hand-coded GraphQL commands", g.get("reporting", 0)),
        ("intro: CLI-native glossary group",
         r"a (\d+)-command CLI-native `glossary` group", g.get("glossary", 0)),
        ("features: total commands",
         r"\*\*(\d+) commands\*\* total", t["total"]),
        ("features: auto-generated",
         r"\((\d+) auto-generated from the CCC OpenAPI spec", t["generated"]),
        ("features: hand-coded GraphQL reporting",
         r"\+ (\d+) hand-coded GraphQL reporting commands", g.get("reporting", 0)),
        ("features: CLI-native auth/config",
         r"\+ (\d+) CLI-native auth/config", t["cliNativeAuthConfig"]),
        ("features: CLI-native glossary",
         r"\+ (\d+) CLI-native glossary commands", g.get("glossary", 0)),
        ("docs link: command reference total",
         r"All (\d+) commands with descriptions", t["total"]),
    ]
    for group_name in sorted(g):
        claims.append((
            f"group table: {group_name}",
            rf"\|\s*`{re.escape(group_name)}`\s*\|\s*(\d+)\s*\|",
            g[group_name],
        ))
    return claims


def _command_reference_claims(counts: dict) -> list:
    """Numeric claims made by docs/command-reference.md.

    This file carried the same `reporting` drift the README did, so it is
    checked mechanically too. Its totals deliberately EXCLUDE the CLI-native
    `glossary` group — it documents remote-API commands plus auth/config.
    """
    t = counts["totals"]
    g = counts["perGroup"]
    documented_total = t["generated"] + g.get("reporting", 0) + t["cliNativeAuthConfig"]
    return [
        ("cmd-ref: REST commands listed",
         r"The (\d+) REST commands below", t["generated"]),
        ("cmd-ref: reporting group size",
         r"The `reporting` group \((\d+) commands\)", g.get("reporting", 0)),
        ("cmd-ref: documented total",
         r"\*\*(\d+) commands\*\* total", documented_total),
        ("cmd-ref: auto-generated REST",
         r"(\d+) auto-generated REST", t["generated"]),
        ("cmd-ref: hand-coded GraphQL reporting",
         r"\+ (\d+) hand-coded GraphQL reporting", g.get("reporting", 0)),
        ("cmd-ref: CLI-native auth+config",
         r"\+ (\d+) CLI-native \(auth \+ config\)", t["cliNativeAuthConfig"]),
        ("cmd-ref: excluded glossary commands",
         r"Excludes the (\d+) CLI-native `glossary` commands", g.get("glossary", 0)),
        ("cmd-ref: full command count",
         r"the full (\d+)-command count", t["total"]),
    ]


def check_doc(path: Path, claims: list) -> list:
    """Compare a doc's numeric claims against the source. Returns a result list."""
    label = path.name
    if not path.exists():
        return [{"claim": f"{label}: file present", "status": "MISSING",
                 "expected": None, "found": None,
                 "detail": f"{path} does not exist"}]

    text = _normalize(path.read_text())
    results = []
    for claim, pattern, expected in claims:
        found = re.findall(pattern, text)
        if not found:
            results.append({
                "claim": claim, "status": "MISSING", "expected": expected,
                "found": None,
                "detail": f"no text in {label} matches /{pattern}/",
            })
            continue
        values = sorted({int(v) for v in found})
        if values == [expected]:
            results.append({"claim": claim, "status": "OK", "expected": expected,
                            "found": expected, "detail": ""})
        else:
            results.append({
                "claim": claim, "status": "MISMATCH", "expected": expected,
                "found": values,
                "detail": f"{label} says {values}, source says {expected}",
            })
    return results


def _root_help_claims(counts: dict) -> list:
    """The command count baked into `elisity --help`.

    This one is the most visible number in the project — every user sees it on
    every root help invocation — and it was the last to be checked. It sat at
    466 through the CCC 26.7 bump because the audit only looked at markdown.
    """
    return [
        ("root help: total commands",
         r"— (\d+) commands across", counts["totals"]["total"]),
    ]


def check_docs(counts: dict) -> list:
    """Cross-check every documented count against the source tree."""
    return (
        check_doc(README, _readme_claims(counts))
        + check_doc(COMMAND_REFERENCE, _command_reference_claims(counts))
        + check_doc(MAIN_PY, _root_help_claims(counts))
    )


# --------------------------------------------------------------------------
# Invariants that do not depend on README
# --------------------------------------------------------------------------


def check_invariants(counts: dict) -> list:
    """Structural invariants of the CLI itself."""
    problems = []

    gate = counts["confirmGate"]
    if gate["ungatedDestructive"]:
        problems.append(
            "confirm gate: "
            f"{len(gate['ungatedDestructive'])} destructive command(s) missing "
            "--confirm: " + ", ".join(gate["ungatedDestructive"])
        )
    if gate["nameDestructivePathNot"]:
        problems.append(
            "confirm gate: "
            f"{len(gate['nameDestructivePathNot'])} command(s) read destructive by "
            "name but their path does not classify — rule on each in "
            "NON_DESTRUCTIVE_DESPITE_NAME (or teach the path matcher): "
            + ", ".join(gate["nameDestructivePathNot"])
        )

    reg = counts["registration"]
    if reg["onDiskNotRegistered"]:
        problems.append(
            "registration: module(s) on disk but not in COMMAND_GROUPS: "
            + ", ".join(reg["onDiskNotRegistered"])
        )
    if reg["registeredNotOnDisk"]:
        problems.append(
            "registration: COMMAND_GROUPS names a missing module: "
            + ", ".join(reg["registeredNotOnDisk"])
        )

    for name in HANDCODED_GROUPS:
        if counts["perGroup"].get(name, 0) == 0:
            problems.append(
                f"hand-coded group '{name}' has 0 commands — regeneration "
                "may have overwritten it"
            )

    return problems


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------


def render(counts: dict, readme_results: list, problems: list) -> str:
    t, gate = counts["totals"], counts["confirmGate"]
    lines = [
        "Elisity CLI — command count audit",
        "=" * 60,
        f"Source of truth: {COMMANDS_DIR.relative_to(REPO_ROOT)} + "
        f"{MAIN_PY.relative_to(REPO_ROOT)}",
        "",
        "Per group:",
    ]
    kinds = {name: g["kind"] for name, g in counts["groupModules"].items()}
    for name in sorted(counts["perGroup"]):
        kind = kinds.get(name, "cli-native")
        lines.append(f"  {name:<12} {counts['perGroup'][name]:>4}  {kind}")

    lines += [
        "",
        "Totals:",
        f"  generated (OpenAPI)      {t['generated']:>4}",
        f"  hand-coded groups        {t['handcodedGroups']:>4}",
        f"  CLI-native auth/config   {t['cliNativeAuthConfig']:>4}",
        f"  TOTAL                    {t['total']:>4}  across {t['groupCount']} groups",
        "",
        "Confirm gate (denominator: every DESTRUCTIVE command, all verbs):",
        f"  destructive commands     {gate['destructiveCommands']:>4}",
        f"  gated with --confirm     {gate['gatedDestructive']:>4}",
        f"  coverage                 {gate['coveragePercent']:>6}%",
        f"  ruled non-destructive    {len(gate['ruledNonDestructiveDespiteName']):>4}"
        "  (destructive-sounding name, path says otherwise)",
    ]
    if gate["ungatedDestructive"]:
        lines.append("  UNGATED: " + ", ".join(gate["ungatedDestructive"]))
    if gate["nameDestructivePathNot"]:
        lines.append("  UNRULED NAME/PATH MISMATCH: "
                     + ", ".join(gate["nameDestructivePathNot"]))
    if gate["gatedButNotClassifiedDestructive"]:
        lines.append("  GATED BUT NOT CLASSIFIED DESTRUCTIVE: "
                     + ", ".join(gate["gatedButNotClassifiedDestructive"]))

    if readme_results is not None:
        lines += ["", "Documentation cross-check:"]
        for r in readme_results:
            mark = "OK  " if r["status"] == "OK" else "FAIL"
            detail = f"  <- {r['detail']}" if r["detail"] else ""
            lines.append(f"  [{mark}] {r['claim']:<40} {r['expected']}{detail}")

    lines.append("")
    if problems:
        lines.append("INVARIANT FAILURES:")
        lines.extend(f"  - {p}" for p in problems)
        lines.append("")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Audit Elisity CLI command counts.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    parser.add_argument("--no-readme-check", action="store_true",
                        help="Report counts without cross-checking the docs")
    args = parser.parse_args(argv)

    counts = collect_counts()
    problems = check_invariants(counts)
    readme_results = None if args.no_readme_check else check_docs(counts)
    readme_failures = [r for r in (readme_results or []) if r["status"] != "OK"]

    if args.json:
        print(json.dumps(
            {"counts": counts, "readme": readme_results, "invariantFailures": problems},
            indent=2, sort_keys=True,
        ))
    else:
        print(render(counts, readme_results, problems))

    if problems:
        print(f"FAIL: {len(problems)} invariant failure(s).", file=sys.stderr)
    if readme_failures:
        print(
            f"FAIL: {len(readme_failures)} README.md claim(s) disagree with the "
            "source tree. Update README.md to match the source.",
            file=sys.stderr,
        )
    if problems or readme_failures:
        return 1

    if not args.json:
        # Keep --json output pure JSON on stdout so it can be piped.
        print(
            "PASS: source counts and documentation agree; confirm gate at "
            f"{counts['confirmGate']['coveragePercent']}% over "
            f"{counts['confirmGate']['destructiveCommands']} destructive commands."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
