#!/usr/bin/env python3
"""Regenerate docs/command-reference.md from the generated command modules.

This document used to be hand-maintained, which is why the CCC 26.7 bump caught
it listing 45 commands that no longer exist and none of the 192 new ones — a
stale command reference is worse than a missing one, because a reader has no
way to tell which entries are lies.

Everything here is derived from the command modules themselves: the command
name from the `@group.command("...")` decorator, the description from the
function docstring, and the HTTP verb from the `client.<verb>(` call in the
body. The hand-written sections (auth/config built-ins, global options) are
preserved as constants because they describe CLI-native behaviour that has no
spec to derive from.

    python3 tools/gen_command_reference.py            # rewrite the doc
    python3 tools/gen_command_reference.py --check    # exit 1 if out of date

`--check` is what keeps this honest: it fails when the committed doc differs
from what the current source would produce, so the drift shows up in CI rather
than in front of a customer.
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIR = REPO_ROOT / "src" / "elisity_cli" / "commands"
DOC_PATH = REPO_ROOT / "docs" / "command-reference.md"

# Groups that are not generated from the OpenAPI spec.
HANDCODED_GROUPS = ("glossary", "reporting")
# `reporting` is hand-coded GraphQL and deliberately not enumerated here; the
# user guide carries its catalog. `glossary` is CLI-native and excluded from
# this document's totals entirely.
CLI_NATIVE_AUTH_CONFIG = 7

COMMAND_SPLIT_RE = re.compile(r'\n@group\.command\(\s*"([^"]+)"')
DOCSTRING_RE = re.compile(r'def cmd_\w+\([^)]*\):\s*\n\s*"""(.*?)"""', re.DOTALL)
# `get_ndjson` is a GET that streams newline-delimited JSON. It must be listed
# in the same section as any other GET — matching only `client.get(` silently
# dropped all 14 NDJSON commands out of the Quick Find tables.
# `update_device` is the ENG-31142 device update (generate_commands.py
# KEEP_DEVICE_ATTACHMENT_OPERATIONS): it sends PATCH, falling back to PUT on
# CCC 26.9 and earlier. Unmatched, `update-device` would drop out of the tables.
VERB_RE = re.compile(r"client\.(get_ndjson|get|post|put|patch|delete)\(|= (update_device)\(client")
VERB_ALIASES = {"get_ndjson": "get", "update_device": "patch"}

VERB_SECTIONS = [
    ("List / Get operations", ("get",)),
    ("Create operations", ("post",)),
    ("Update operations", ("put",)),
    ("Delete operations", ("delete",)),
    ("Patch operations", ("patch",)),
]

BUILTIN_SECTION = """## Built-in Commands

### auth

Authentication and token management.

| Command | Description |
|---------|-------------|
| `auth test` | Test CCC authentication and connectivity |
| `auth token` | Get bearer token for use in scripts or curl |
| `auth whoami` | Decode and display JWT token claims |

### config

Profile and configuration management.

| Command | Description |
|---------|-------------|
| `config set-profile NAME` | Create or update a named connection profile |
| `config use-profile NAME` | Switch the active profile |
| `config list-profiles` | List all saved profiles |
| `config show` | Show active configuration (secrets redacted) |

---
"""

GLOBAL_OPTIONS_SECTION = """## Global Options

All API commands support these hidden flags:

| Flag | Description |
|------|-------------|
| `--format`, `-f` | Output format override: `json`, `table`, `yaml`, `csv` |
| `--query`, `-q` | JMESPath query to filter/reshape output |

Mutating commands (`POST`, `PUT`, `PATCH`) accept:

| Flag | Description |
|------|-------------|
| `--body JSON` | Request body as inline JSON string |
| `--body-file PATH` | Read request body from a JSON file |

Destructive commands require `--confirm` to execute. That is every `DELETE`, plus
any verb whose API path names a destructive action — bulk deletes over POST,
`decommission` over PUT, and the Insights `reset-to-default` / `recreate`
commands. Dry-run paths (`.../bulk/delete/validate`) are deliberately not gated.
"""


def _escape(text: str) -> str:
    """Make a description safe inside a markdown table cell."""
    return " ".join(text.split()).replace("|", "\\|")


def parse_group(path: Path) -> list:
    """Return [(command, description, verb)] for a generated module."""
    src = path.read_text()
    out = []
    # Split on the decorator so each chunk is exactly one command's source.
    parts = COMMAND_SPLIT_RE.split(src)
    # parts = [preamble, name1, body1, name2, body2, ...]
    for i in range(1, len(parts), 2):
        name, body = parts[i], parts[i + 1]
        doc = DOCSTRING_RE.search(body)
        desc = _escape(doc.group(1)) if doc else ""
        verb = VERB_RE.search(body)
        raw = verb.group(verb.lastindex) if verb else ""
        out.append((name, desc, VERB_ALIASES.get(raw, raw)))
    return out


def collect() -> dict:
    """{group: [(command, description, verb)]} for every generated group."""
    groups = {}
    for path in sorted(COMMANDS_DIR.glob("*.py")):
        group = path.stem
        if group.startswith("_") or group in HANDCODED_GROUPS:
            continue
        groups[group] = parse_group(path)
    return groups


def _table(rows) -> list:
    out = ["| Group | Command | Description |", "|-------|---------|-------------|"]
    out += [f"| {g} | `{c}` | {d} |" for g, c, d in rows]
    return out


def render(groups: dict) -> str:
    generated = sum(len(v) for v in groups.values())
    reporting = len(parse_group(COMMANDS_DIR / "reporting.py")) if (COMMANDS_DIR / "reporting.py").exists() else 0
    glossary = len(parse_group(COMMANDS_DIR / "glossary.py")) if (COMMANDS_DIR / "glossary.py").exists() else 0
    documented_total = generated + reporting + CLI_NATIVE_AUTH_CONFIG
    full_total = documented_total + glossary
    # Generated groups + reporting + auth + config.
    n_groups = len(groups) + 1 + 2

    L = []
    w = L.append
    w("# Elisity CLI -- Command Reference")
    w("")
    w(f"> The {generated} REST commands below are auto-generated from the Elisity CCC OpenAPI")
    w(f"> specification. The `reporting` group ({reporting} commands) is hand-coded against the")
    w("> CCC GraphQL endpoint at `/api/reporting/v1/data` and is NOT listed in this")
    w("> reference — see [user-guide.md](user-guide.md) section 9 for the full")
    w("> reporting catalog.")
    w(">")
    w(f"> **{documented_total} commands** total: {generated} auto-generated REST + {reporting} hand-coded GraphQL")
    w(f"> reporting + {CLI_NATIVE_AUTH_CONFIG} CLI-native (auth + config). {n_groups} groups total. (Excludes the {glossary}")
    w(f"> CLI-native `glossary` commands; see README for the full {full_total}-command count.)")
    w(">")
    w("> This file is generated — run `python3 tools/gen_command_reference.py` after")
    w("> regenerating commands. Do not edit it by hand.")
    w("")
    w("## Quick Find by Operation Type")
    w("")

    all_cmds = [(g, c, d, v) for g, cmds in sorted(groups.items()) for c, d, v in cmds]
    for title, verbs in VERB_SECTIONS:
        rows = sorted(
            ((g, c, d) for g, c, d, v in all_cmds if v in verbs),
            key=lambda r: (r[0], r[1]),
        )
        w(f"### {title} ({len(rows)} commands)")
        w("")
        L.extend(_table(rows))
        w("")

    w(BUILTIN_SECTION)
    w("## API Command Groups")
    w("")
    for group in sorted(groups):
        cmds = sorted(groups[group], key=lambda r: r[0])
        w(f"### {group} ({len(cmds)} commands)")
        w("")
        w("| Command | Description |")
        w("|---------|-------------|")
        for c, d, _ in cmds:
            w(f"| `{c}` | {d} |")
        w("")

    w("---")
    w("")
    w(GLOBAL_OPTIONS_SECTION)
    return "\n".join(L).rstrip() + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="Exit 1 if the committed doc is out of date, without rewriting it")
    args = ap.parse_args(argv)

    content = render(collect())

    if args.check:
        current = DOC_PATH.read_text() if DOC_PATH.exists() else ""
        if current != content:
            print(
                f"FAIL: {DOC_PATH.relative_to(REPO_ROOT)} is out of date with the command "
                "source.\nRegenerate it with: python3 tools/gen_command_reference.py",
                file=sys.stderr,
            )
            return 1
        print(f"OK: {DOC_PATH.relative_to(REPO_ROOT)} matches the command source.")
        return 0

    DOC_PATH.write_text(content)
    print(f"Wrote {DOC_PATH.relative_to(REPO_ROOT)} ({len(content.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
