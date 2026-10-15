#!/usr/bin/env python3
"""Write the naming skeleton of a CCC OpenAPI spec for the CI test suite.

The full specs are 1-2 MB each and are not committed, so CI cannot run the
tests that regenerate from them. Command names and groups depend on far less:
each operation's path, method, tags and operationId, in spec order (dedupe
suffixes whichever collides second). The skeleton keeps exactly that, so the
naming guards in tests/test_command_invariants.py run in CI against the real
operation set.

    python3 tools/spec_skeleton.py api-docs-26.9.json \\
        --source release-demos.idp02.elisity.io > tests/data/ccc-26.9-operations.json
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generate_commands import HTTP_METHODS  # noqa: E402

# Only these keys of an operation affect the command name or group.
NAMING_KEYS = ("tags", "operationId")


def skeleton(spec: dict) -> dict:
    """paths -> method -> {tags, operationId}, keeping spec order."""
    paths = {}
    for path, ops in (spec.get("paths") or {}).items():
        if not isinstance(ops, dict):
            continue
        kept = {
            method: {k: op[k] for k in NAMING_KEYS if k in op}
            for method, op in ops.items()
            if method in HTTP_METHODS and isinstance(op, dict)
        }
        if kept:
            paths[path] = kept
    return {"paths": paths}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("spec", help="Full OpenAPI JSON spec")
    ap.add_argument("--source", required=True, help="Tenant the spec was pulled from")
    args = ap.parse_args(argv)

    raw = Path(args.spec).read_bytes()
    out = {
        "x-skeleton-of": {
            "source": args.source,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "regenerate": "python3 tools/spec_skeleton.py <spec> --source <tenant>",
        },
        **skeleton(json.loads(raw)),
    }
    json.dump(out, sys.stdout, indent=1)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
