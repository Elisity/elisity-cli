"""
Mechanical invariants of the generated command surface.

These are the properties that must survive every regeneration from a new CCC
OpenAPI spec. They are enforced here rather than by review because a spec bump
adds commands in bulk and a reviewer scanning a 400-command diff will not
reliably notice a single DELETE that lost its --confirm guard.

Covered:
  1. Delete gate  — 100% of commands issuing client.delete() require --confirm,
                    both in the committed tree and in freshly generated code.
  2. Hand-coded   — the `reporting` (GraphQL) and `glossary` (CLI-native) groups
     survival       are never overwritten or unregistered by regeneration.
  3. Doc counts   — tools/audit_counts.py agrees with the source tree.
  4. Loadability  — every registered group imports and exposes its commands.
"""

import json
import os
import re
import subprocess
import sys
import warnings
from pathlib import Path

import pytest
from click.testing import CliRunner

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from generate_commands import (  # noqa: E402
    HANDCODED_GROUPS,
    build_groups,
    assert_every_tag_mapped,
    is_destructive_operation,
    resolve_group,
    resolve_parameter_names,
    unmapped_tags,
    generate_module,
    merge_path_templates,
    render_init_module,
)
from tools.audit_counts import (  # noqa: E402
    audit_group_modules,
    describe_command,
    check_docs,
    check_invariants,
    collect_counts,
)

from elisity_cli.commands import COMMAND_GROUPS  # noqa: E402
from elisity_cli.main import cli  # noqa: E402

COMMANDS_DIR = REPO_ROOT / "src" / "elisity_cli" / "commands"

# The OpenAPI specs are not committed (1-2 MB each, and the repo generates FROM
# them rather than shipping them). Where a checkout has them staged, a few tests
# assert against the real thing; where it does not, they skip and the synthetic
# equivalents still run. $ELISITY_API_SPEC is the same variable the generator
# reads.
SPEC_267 = Path(
    os.environ.get("ELISITY_API_SPEC", REPO_ROOT.parent / "input" / "api-docs-26.7.json")
)
SPEC_263 = REPO_ROOT.parent / "input" / "api-docs-baseline-26.3.json"
# The spec the committed command set is generated from (CCC 26.9, pulled from
# release-demos.idp02.elisity.io on 2026-10-15).
SPEC_269 = REPO_ROOT.parent / "input" / "api-docs-26.9.0-release-demos.json"


@pytest.fixture(scope="module")
def counts():
    return collect_counts()


# --------------------------------------------------------------------------
# 1. Confirm gate — the security invariant
# --------------------------------------------------------------------------


class TestConfirmGate:
    """The gate keys on DESTRUCTIVENESS, not on the DELETE verb.

    It used to key on the verb, and the audit measured its coverage with the
    same verb-shaped denominator — so `tools/audit_counts.py` certified
    "coverage 100.0%" while ten destructive POST/PUT commands ran ungated, four
    of them added by the 26.7 bump. `topology bulk-force-delete-ve-ns` (POST,
    many VENs) was ungated while `topology force-delete-ven` (DELETE, one VEN)
    was gated, and both docs told agents every delete required --confirm.

    Widening the gate without widening the denominator would have reproduced
    exactly that bug one layer out, so these tests pin BOTH: the gate covers
    every destructive command, and the denominator is derived from the same
    single predicate the generator emits from.
    """

    def test_every_destructive_command_requires_confirm(self, counts):
        gate = counts["confirmGate"]
        assert gate["ungatedDestructive"] == [], (
            f"{len(gate['ungatedDestructive'])} destructive command(s) can run "
            f"without --confirm: {', '.join(gate['ungatedDestructive'])}. "
            "Fix generate_commands.py, not the generated module."
        )
        assert gate["coveragePercent"] == 100.0

    def test_denominator_is_wider_than_the_delete_verb(self, counts):
        """The number that matters: destructive commands, not DELETEs.

        52 DELETEs was the old denominator. If this ever equals the DELETE count
        again, the gate has silently narrowed back to the verb.
        """
        gate = counts["confirmGate"]
        deletes = sum(
            1
            for module in COMMANDS_DIR.glob("*.py")
            if module.name != "__init__.py"
            for block in module.read_text().split("@group.command(")[1:]
            if "client.delete(" in block
        )
        assert deletes == 52, deletes
        assert gate["destructiveCommands"] == 68, gate["destructiveCommands"]
        assert gate["destructiveCommands"] > deletes

    def test_the_non_delete_destructive_commands_are_named(self, counts):
        """Pin the 16 the verb-shaped gate missed, so a silent loss fails here.

        15 by path segment, plus `ad set-groups-default-enabled` from
        DESTRUCTIVE_OPERATIONS (CCC 26.9).
        """
        gated_non_delete = set()
        for module in sorted(COMMANDS_DIR.glob("*.py")):
            if module.name == "__init__.py":
                continue
            for block in module.read_text().split("@group.command(")[1:]:
                name = block.split('"')[1]
                if "Use --confirm" in block and "client.delete(" not in block:
                    gated_non_delete.add(f"{module.stem} {name}")
        assert gated_non_delete == {
            "ad set-groups-default-enabled",
            "devices detach",
            "devices detach-by-mac",
            "insights recreate-policy-suggestions",
            "insights recreate-suggestions",
            "insights reset-policy-suggestions-to-default",
            "insights reset-suggestions-to-default",
            "insights reset-suggestions-to-default-post",
            "policy bulk-delete",
            "topology bulk-delete-distribution-zone",
            "topology bulk-delete-site",
            "topology bulk-delete-site-v2",
            "topology bulk-delete-ve-ns",
            "topology bulk-delete-virtual-edges",
            "topology bulk-force-delete-ve-ns",
            "topology decommission-virtual-edge-node",
        }

    def test_destructive_commands_actually_exist(self, counts):
        """Guards against the audit trivially passing on an empty set."""
        assert counts["confirmGate"]["destructiveCommands"] > 0

    def test_dry_run_siblings_are_not_gated(self, counts):
        """`.../bulk/delete/validate` reports what a delete would do.

        Gating it would be friction with no safety value, and would teach users
        that --confirm on these paths means nothing.
        """
        assert not is_destructive_operation(
            "POST", "/api/topology/v1/virtual-edges/bulk/delete/validate"
        )
        assert is_destructive_operation(
            "POST", "/api/topology/v1/virtual-edges/bulk/delete"
        )
        assert counts["confirmGate"]["gatedButNotClassifiedDestructive"] == []

    def test_whole_segment_matching_not_substring(self):
        """`/devices/purge-settings` configures the purge policy; it purges nothing."""
        assert not is_destructive_operation(
            "PUT", "/api/identity-graph/v2/devices/purge-settings"
        )
        assert is_destructive_operation(
            "DELETE", "/api/identity-graph/v1/devices/bulk/purge"
        )

    def test_every_destructive_sounding_name_has_been_ruled_on(self, counts):
        """The denominator's own watchdog.

        A command whose NAME reads destructive while its PATH does not classify
        is the gap the path matcher cannot see by itself. Each one must be an
        explicit human ruling, not an emergent property — so an unruled
        `bulk-nuke-sites` on an unrecognised path fails the build.
        """
        assert counts["confirmGate"]["nameDestructivePathNot"] == []
        assert set(counts["confirmGate"]["ruledNonDestructiveDespiteName"]) == {
            "topology validate-virtual-edge-bulk-delete",
            "topology validate-virtual-edge-node-bulk-delete",
        }

    def test_the_safe_prefix_rule_never_clears_a_destructive_command(self):
        """docs/AGENTS.md tells agents a `get-`/`list-`/`read-`/`search-`/
        `count-`/`export-` prefix means safe-to-run-without-approval.

        The direction that matters is that nothing destructive is cleared by it.
        The converse — a read-only POST that the rule flags anyway — costs an
        approval round nobody needed, which is the error worth making, and the
        exception table in AGENTS.md is an explicit allowlist for it.
        """
        safe_prefixes = ("get-", "list-", "read-", "search-", "count-", "export-")
        cleared_but_destructive, safe_prefixed, state_changing = [], 0, 0
        for module in sorted(COMMANDS_DIR.glob("*.py")):
            if module.name == "__init__.py" or module.stem in HANDCODED_GROUPS:
                continue
            for block in module.read_text().split("@group.command(")[1:]:
                name = block.split('"')[1]
                verb, endpoint = describe_command(block)
                if verb in ("", "GET"):
                    continue
                state_changing += 1
                if not name.startswith(safe_prefixes):
                    continue
                safe_prefixed += 1
                if is_destructive_operation(verb, endpoint):
                    cleared_but_destructive.append(
                        f"{module.stem} {name} ({verb} {endpoint})"
                    )
        # CCC 26.9: 375 -> 416 and 39 -> 61. The 22 new safe-prefixed POSTs are
        # the search-/export-/list-azure-/get-*-metrics-summary/AD group reads.
        # 416 -> 408 once the eight platform-internal POSTs in OMITTED_OPERATIONS
        # stopped being generated; none of them carried a safe prefix.
        assert state_changing == 408, state_changing
        assert safe_prefixed == 61, safe_prefixed
        assert cleared_but_destructive == [], (
            "AGENTS.md's safe-prefix rule clears a DESTRUCTIVE command: "
            + ", ".join(cleared_but_destructive)
        )

    def test_generated_delete_command_is_gated(self):
        """Regeneration itself must emit the guard, not just today's tree."""
        spec = {
            "paths": {
                "/api/topology/v2/sites/{id}": {
                    "delete": {
                        "tags": ["site-controller"],
                        "operationId": "deleteSiteV2",
                        "parameters": [
                            {"name": "id", "in": "path", "required": True,
                             "schema": {"type": "string"}}
                        ],
                        "responses": {"204": {}},
                    }
                }
            }
        }
        groups, _ = build_groups(spec)
        module = generate_module("topology", groups["topology"])

        assert "--confirm/--no-confirm" in module
        assert "Use --confirm to execute this destructive operation." in module
        assert "client.delete(" in module

    @pytest.mark.parametrize("path", [
        "/api/topology/v1/virtual-edge-nodes/bulk/force-delete",
        "/api/topology/v1/sites/bulk/delete",
        "/api/identity-graph/v1/labels/bulk-delete",
        "/api/identity-graph/v1/devices/{id}/detach",
        "/api/policy/v1/insights/policy-groups/reset-to-default",
        "/api/policy/v1/insights/policy-groups/recreate",
    ])
    def test_generated_destructive_post_is_gated(self, path):
        """A POST that destroys must be gated exactly like the DELETE would be."""
        spec = {"paths": {path: {"post": {
            "tags": ["site-controller"], "operationId": "doTheThing",
            "parameters": [
                {"name": p.strip("{}"), "in": "path", "required": True,
                 "schema": {"type": "string"}}
                for p in path.split("/") if p.startswith("{")
            ],
            "responses": {"200": {}},
        }}}}
        groups, _ = build_groups(spec)
        module = generate_module("topology", groups["topology"])

        assert '@click.option("--confirm/--no-confirm"' in module, path
        assert "Use --confirm to execute this destructive operation." in module, path
        assert "client.post(" in module

    def test_dry_run_post_is_not_gated(self):
        spec = {"paths": {"/api/topology/v1/virtual-edges/bulk/delete/validate": {
            "post": {"tags": ["site-controller"], "operationId": "validateBulkDelete",
                     "responses": {"200": {}}}}}}
        groups, _ = build_groups(spec)
        module = generate_module("topology", groups["topology"])
        assert "--confirm" not in module

    def test_freshly_generated_module_passes_the_gate_scan(self, tmp_path):
        """The audit's own scan must find zero ungated destructives in new output."""
        spec = {
            "paths": {
                f"/api/topology/v2/thing{i}/{{id}}": {
                    "delete": {
                        "tags": ["site-controller"],
                        "operationId": f"deleteThing{i}",
                        "parameters": [
                            {"name": "id", "in": "path", "required": True,
                             "schema": {"type": "string"}}
                        ],
                        "responses": {"204": {}},
                    }
                }
                for i in range(5)
            }
        }
        groups, _ = build_groups(spec)
        module_text = generate_module("topology", groups["topology"])

        ungated = [
            block.split('"')[1]
            for block in module_text.split("@group.command(")[1:]
            if "client.delete(" in block and "Use --confirm" not in block
        ]
        assert ungated == []

    def test_delete_command_refuses_without_confirm(self):
        """Behavioural check — the guard actually blocks, it isn't just text."""
        runner = CliRunner()
        result = runner.invoke(cli, ["topology", "delete-site-v2", "some-id"])

        assert result.exit_code == 1
        assert "Use --confirm" in result.output

    @pytest.mark.parametrize("argv", [
        ["topology", "bulk-force-delete-ve-ns", "--body", '{"ids":["v1","v2"]}'],
        ["topology", "bulk-delete-site", "--body", '{"ids":["s1"]}'],
        ["topology", "decommission-virtual-edge-node", "ven-1"],
        ["policy", "bulk-delete", "--body", '{"ids":["l1"]}'],
        ["devices", "detach-by-mac", "--body", '{"mac":"00:11:22:33:44:55"}'],
        ["insights", "recreate-suggestions"],
    ])
    def test_destructive_non_delete_refuses_with_no_http_call(self, argv):
        """The newly gated commands refuse, and refuse BEFORE touching the API.

        Leia's reproduction of the original defect was
        `elisity topology bulk-delete-site --body '{"ids":[...]}'` -> exit 0 with
        the POST actually sent. This is that reproduction, inverted.
        """
        calls = []

        class RecordingClient:
            def __getattr__(self, verb):
                def call(*args, **kwargs):
                    calls.append((verb, args, kwargs))
                    return {}
                return call

        import elisity_cli.context as ctxmod
        original = ctxmod.CliContext.ensure_client
        ctxmod.CliContext.ensure_client = lambda self: RecordingClient()
        try:
            result = CliRunner().invoke(cli, argv)
        finally:
            ctxmod.CliContext.ensure_client = original

        assert result.exit_code == 1, result.output
        assert "Use --confirm" in result.output
        assert calls == [], f"HTTP call made despite the gate: {calls}"

    def test_confirm_flag_is_advertised_on_a_gated_post(self):
        result = CliRunner().invoke(
            cli, ["topology", "bulk-force-delete-ve-ns", "--help"]
        )
        assert result.exit_code == 0
        assert "--confirm" in result.output

    def test_delete_help_advertises_confirm(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["topology", "delete-site-v2", "--help"])

        assert result.exit_code == 0
        assert "--confirm" in result.output


# --------------------------------------------------------------------------
# 1b. Parameter-name collisions
# --------------------------------------------------------------------------


def _generate_one(method: str, path: str, params: list, tag: str = "site-controller"):
    """Generate a single-command module for a synthetic operation."""
    spec = {"paths": {path: {method: {
        "tags": [tag], "operationId": "doThing",
        "parameters": params, "responses": {"200": {}},
    }}}}
    groups, _ = build_groups(spec)
    group_name = next(iter(groups))
    return generate_module(group_name, groups[group_name])


class TestUnmappedTagGuard:
    """A new CCC tag is a human decision, not something to route by accident.

    resolve_group() takes the first tag that hits TAG_TO_GROUP, so an unmapped
    tag riding along with a mapped one gets routed by whichever mapped tag comes
    first — which may have nothing to do with what the new tag means. The guard
    used to `continue` on any operation carrying a mapped tag, which made
    exactly that case invisible. 21 operations in the 26.7 spec already carry
    two tags (20 in 26.3), so this is the shape the next bump will have.

    The guard itself has never had a committed test; Leia proved it non-vacuous
    by hand and found the hole. These are the two specs that walked through it.
    """

    def _spec(self, path, tags):
        return {"paths": {path: {"get": {
            "tags": tags, "operationId": "doThing", "responses": {"200": {}},
        }}}}

    def test_unmapped_tag_alone_is_caught(self):
        """The case that always worked — kept so a regression is visible."""
        spec = self._spec("/api/topology/v1/x", ["Totally New Tag"])
        assert unmapped_tags(spec) == {"Totally New Tag": 1}
        with pytest.raises(SystemExit):
            assert_every_tag_mapped(spec)

    def test_unmapped_tag_beside_a_mapped_sibling_is_caught(self):
        """Leia's case (a): a new tag hiding behind a known one.

        `Site Templates (NEW 26.8)` is invisible if the guard skips any
        operation that has at least one mapped tag.
        """
        spec = self._spec(
            "/api/topology/v1/site-templates/{id}",
            ["Sites", "Site Templates (NEW 26.8)"],
        )
        assert unmapped_tags(spec) == {"Site Templates (NEW 26.8)": 1}
        with pytest.raises(SystemExit):
            assert_every_tag_mapped(spec)

    def test_incidental_sibling_routing_the_wrong_way_is_caught(self):
        """Leia's case (b), the damaging shape.

        The operation is a flows operation by path, carries a brand-new flow
        tag, and routes to `policy` on an incidental `Device` tag. The routing
        is not corrected here — resolve_group()'s first-match behaviour is
        deliberately untouched so this fix re-routes nothing — but generation
        now refuses until a human maps the tag.
        """
        spec = self._spec("/api/flows/v1/newthing", ["Brand New Flow Tag", "Device"])
        group, matched_by = resolve_group(["Brand New Flow Tag", "Device"],
                                          "/api/flows/v1/newthing")
        assert (group, matched_by) == ("policy", "tag")   # unchanged behaviour
        assert unmapped_tags(spec) == {"Brand New Flow Tag": 1}
        with pytest.raises(SystemExit):
            assert_every_tag_mapped(spec)

    def test_counts_are_per_tag_not_per_operation(self):
        spec = {"paths": {
            "/api/topology/v1/a": {"get": {"tags": ["Sites", "New A"],
                                           "operationId": "a", "responses": {"200": {}}}},
            "/api/topology/v1/b": {"get": {"tags": ["New A", "New B"],
                                           "operationId": "b", "responses": {"200": {}}}},
        }}
        assert unmapped_tags(spec) == {"New A": 2, "New B": 1}

    def test_fully_mapped_specs_still_generate(self):
        """The fix must not turn either shipped spec into a generation failure.

        Both 26.3 and 26.7 have every tag mapped, including on the 20/21
        double-tagged operations, so widening the guard changes nothing for them
        — asserted rather than assumed.
        """
        for spec_path in (SPEC_267, SPEC_263):
            if not spec_path.exists():
                pytest.skip(f"{spec_path.name} not staged in this checkout")
            spec = json.loads(spec_path.read_text())
            assert unmapped_tags(spec) == {}
            assert_every_tag_mapped(spec)   # must not raise

    def test_double_tagged_but_fully_mapped_still_generates(self):
        """The real 26.7 double-tag pair, without needing the spec file.

        PUT /api/policy/v1/insights/policy-groups/{id} carries
        ["Suggestion", "Dynamic Policy Group Insights"] — both mapped. Widening
        the guard must not turn a fully-mapped co-tagged operation into a
        failure.
        """
        spec = self._spec(
            "/api/policy/v1/insights/policy-groups/{id}",
            ["Suggestion", "Dynamic Policy Group Insights"],
        )
        assert unmapped_tags(spec) == {}
        assert_every_tag_mapped(spec)

    def test_double_tagged_operations_exist_in_the_shipped_specs(self):
        """Guards the test above against being vacuous on a single-tag spec."""
        if not SPEC_267.exists():
            pytest.skip("api-docs-26.7.json not staged in this checkout")
        spec = json.loads(SPEC_267.read_text())
        multi = [
            (path, method)
            for path, methods in spec.get("paths", {}).items()
            for method, op in methods.items()
            if isinstance(op, dict) and len(op.get("tags") or []) > 1
        ]
        assert len(multi) >= 20, len(multi)


def _drive_generated_command(module_source, argv):
    """Run a generated command through Click against a recording fake client.

    Returns the endpoint and params the command actually put on the wire. This
    is the only way to catch the silent-wrong-request class: the code compiles,
    exits 0, and sends something other than what the user typed.
    """
    import types

    import click as _click

    from elisity_cli import context as ctxmod

    namespace = types.ModuleType("generated_under_test")
    namespace.__dict__["__name__"] = "generated_under_test"
    exec(compile(module_source, "generated_under_test.py", "exec"), namespace.__dict__)

    sent = {}

    class RecordingClient:
        def _record(self, endpoint, params=None, data=None):
            sent.update({"endpoint": endpoint, "params": params, "data": data})
            return [{"ok": True}]

        get = post = put = patch = delete = get_ndjson = _record

    @_click.group()
    @_click.pass_context
    def root(ctx):
        ctx.obj = ctxmod.CliContext()

    root.add_command(namespace.group)

    original = ctxmod.CliContext.ensure_client
    ctxmod.CliContext.ensure_client = lambda self: RecordingClient()
    try:
        result = CliRunner().invoke(root, [namespace.group.name] + argv)
    finally:
        ctxmod.CliContext.ensure_client = original

    assert result.exit_code == 0, result.output
    return sent


class TestParameterCollisions:
    """A spec parameter must never collide with an identifier the command owns.

    Every case below produced `def cmd_x(ctx, foo, ..., foo)` — a SyntaxError.
    _register_groups() catches import errors and only prints a warning, so the
    whole group (up to 117 commands) would vanish from the CLI silently. On a
    DELETE that also means losing the --confirm gate.
    """

    def test_delete_with_a_confirm_query_param_still_compiles_and_stays_gated(self):
        module = _generate_one("delete", "/api/topology/v2/sites/{id}", [
            {"name": "id", "in": "path", "required": True, "schema": {"type": "string"}},
            {"name": "confirm", "in": "query", "schema": {"type": "boolean"}},
        ])
        compile(module, "topology.py", "exec")

        assert "Use --confirm to execute this destructive operation." in module
        assert '@click.option("--confirm/--no-confirm"' in module
        # The spec parameter is renamed, but still sent under its wire name.
        assert 'params["confirm"]' in module

    def test_path_and_query_param_sharing_a_name_compiles(self):
        module = _generate_one("get", "/api/topology/v2/x/{id}", [
            {"name": "id", "in": "path", "required": True, "schema": {"type": "string"}},
            {"name": "id", "in": "query", "schema": {"type": "string"}},
        ])
        compile(module, "topology.py", "exec")
        assert 'params["id"]' in module

    def test_params_normalizing_to_the_same_identifier_compile(self):
        """`foo.bar` and `foo-bar` both sanitize to `foo_bar`."""
        module = _generate_one("get", "/api/topology/v2/y", [
            {"name": "foo.bar", "in": "query", "schema": {"type": "string"}},
            {"name": "foo-bar", "in": "query", "schema": {"type": "string"}},
        ])
        compile(module, "topology.py", "exec")
        assert 'params["foo.bar"]' in module
        assert 'params["foo-bar"]' in module

    def test_format_and_query_params_are_renamed_but_sent_verbatim(self):
        """`format`/`query` collide with the CLI's own output overrides."""
        module = _generate_one("get", "/api/topology/v2/z", [
            {"name": "format", "in": "query", "schema": {"type": "string"}},
            {"name": "query", "in": "query", "schema": {"type": "string"}},
        ])
        compile(module, "topology.py", "exec")

        assert '"--format-param"' in module
        assert '"--query-param"' in module
        assert 'params["format"]' in module
        assert 'params["query"]' in module

    @pytest.mark.parametrize("label,names", [
        ("context arg", ["ctx"]),
        ("body args", ["body", "body_file"]),
        ("output override dests", ["cmd_fmt", "cmd_query"]),
        ("python keywords", ["from", "class", "type"]),
        ("body locals", ["params", "endpoint"]),
        ("every body local", ["endpoint", "params", "body", "client", "result"]),
        ("all at once", ["ctx", "confirm", "format", "query", "cmd_fmt", "body_file"]),
    ])
    def test_reserved_identifier_names_reach_the_wire(self, label, names):
        """Any spec param name must be absorbable, not just the ones seen so far.

        Asserted by DRIVING the generated command, not by scanning its source.
        The source-text version of this test passed on code that corrupted the
        request: for a parameter named `params` the broken module emits
        `params["params"] = params` — which contains the literal the assertion
        looked for, compiles, and at exit 0 sends the params dict as its own
        value while the user's input never leaves the process. A test that
        cannot fail on the bug it names is worse than no test; it is a claim of
        coverage.
        """
        module = _generate_one("get", "/api/topology/v2/w", [
            {"name": n, "in": "query", "schema": {"type": "string"}} for n in names
        ])
        compile(module, "topology.py", "exec")
        for n in names:
            assert f'params["{n}"]' in module, f"{n} is no longer sent on the wire"

        # Drive with the flags the generator ACTUALLY emits: a name colliding
        # with one of the CLI's own flags (--format, --body, ...) is renamed,
        # while the wire name stays the spec name.
        _, resolved = resolve_parameter_names(
            "get", [], [(n, "str", False, "", None) for n in names],
            "/api/topology/v2/w",
        )
        argv = ["do-thing"]
        for spec in resolved:
            argv += [spec["flag"], f"VALUE-{spec['spec_name']}"]
        sent = _drive_generated_command(module, argv)
        assert sent["params"] == {n: f"VALUE-{n}" for n in names}, (
            f"{label}: the user's values did not reach the wire intact"
        )
        assert sent["endpoint"] == "/api/topology/v2/w"

    def test_worst_case_delete_keeps_its_gate(self):
        """Path param, query param and the guard all named `confirm`."""
        module = _generate_one("delete", "/api/topology/v2/v/{confirm}", [
            {"name": "confirm", "in": "path", "required": True, "schema": {"type": "string"}},
            {"name": "confirm", "in": "query", "schema": {"type": "string"}},
            {"name": "format", "in": "query", "schema": {"type": "string"}},
        ])
        compile(module, "topology.py", "exec")

        assert "Use --confirm to execute this destructive operation." in module
        assert '@click.option("--confirm/--no-confirm"' in module
        assert 'params["confirm"]' in module

    def test_undeclared_path_template_gets_an_argument(self):
        """The spec's path declares {id} but omits the parameter. Without a
        synthesized argument the f-string resolved `id` to Python's builtin and
        sent '<built-in function id>' in the URL, at exit code 0."""
        module = _generate_one("post", "/api/x/{id}/import/{uploadId}/cancel", [
            {"name": "uploadId", "in": "path", "required": True,
             "schema": {"type": "string"}},
        ])
        compile(module, "topology.py", "exec")

        assert '@click.argument("id")' in module
        assert '@click.argument("uploadid")' in module
        assert "def cmd_do_thing(ctx, id, uploadid," in module

    def test_no_committed_endpoint_has_an_unsubstituted_placeholder(self):
        """Whole-tree sweep: every f-string placeholder in a generated endpoint
        must correspond to an argument of its own function."""
        offenders = []
        for path in sorted(COMMANDS_DIR.glob("*.py")):
            source = path.read_text()
            for block in source.split("@group.command(")[1:]:
                name = block.split('"')[1]
                sig = re.search(r"def cmd_\w+\(([^)]*)\):", block)
                endpoint = re.search(r'endpoint = f"([^"]*)"', block)
                if not sig or not endpoint:
                    continue
                args = {a.strip() for a in sig.group(1).split(",")}
                for placeholder in re.findall(r"\{([^}]*)\}", endpoint.group(1)):
                    if placeholder not in args:
                        offenders.append(f"{path.stem} {name}: {{{placeholder}}}")
        assert offenders == [], (
            "endpoint placeholders with no matching function argument (these "
            "resolve against builtins or raise NameError at runtime): "
            + ", ".join(offenders)
        )

    def test_cancel_import_builds_a_correct_url(self):
        """Regression for the live bug — end-to-end through Click."""
        captured = {}

        class FakeClient:
            def post(self, endpoint, data=None, params=None):
                captured["endpoint"] = endpoint
                return {}

        import elisity_cli.context as ctxmod
        original = ctxmod.CliContext.ensure_client
        ctxmod.CliContext.ensure_client = lambda self: FakeClient()
        try:
            result = CliRunner().invoke(
                cli, ["connectors", "cancel-import", "CONN42", "UPLOAD123"]
            )
        finally:
            ctxmod.CliContext.ensure_client = original

        assert result.exit_code == 0, result.output
        assert captured["endpoint"] == (
            "/api/identity-graph/v1/custom-connector/CONN42/import/UPLOAD123/cancel"
        )

    def test_unusable_path_template_is_a_generation_error(self):
        """A template with no usable name must fail generation, not emit
        code that cannot compile."""
        with pytest.raises(ValueError, match="no usable name"):
            merge_path_templates("/api/x/{}/y", [])

    def test_declared_path_param_absent_from_template_is_kept(self):
        merged = merge_path_templates("/api/x/{id}", [
            ("id", "str", ""), ("orphan", "str", ""),
        ])
        assert [m[0] for m in merged] == ["id", "orphan"]

    def test_every_committed_module_compiles(self):
        """Net that catches any collision class not enumerated above."""
        for path in sorted(COMMANDS_DIR.glob("*.py")):
            compile(path.read_text(), str(path), "exec")

    def test_no_command_declares_a_duplicate_flag(self):
        """The live regression this caught: `flows get-pg-data` declared
        --format twice, so the required spec param could never be satisfied and
        the command was impossible to invoke (exit 2, 'Missing option')."""
        offenders = []
        for group_name in COMMAND_GROUPS:
            mod = __import__(f"elisity_cli.commands.{group_name}", fromlist=["group"])
            for cmd_name, cmd in mod.group.commands.items():
                seen = set()
                for param in cmd.params:
                    for opt in param.opts + param.secondary_opts:
                        if opt in seen:
                            offenders.append(f"{group_name} {cmd_name}: {opt}")
                        seen.add(opt)
        assert offenders == [], "duplicate option flags: " + ", ".join(offenders)

    def test_loading_every_group_emits_no_click_warnings(self):
        """Click warns 'parameter used more than once' on a duplicate flag."""
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            runner = CliRunner()
            for group_name in COMMAND_GROUPS:
                runner.invoke(cli, [group_name, "--help"])
        duplicates = [str(w.message) for w in caught if "more than once" in str(w.message)]
        assert duplicates == [], f"Click duplicate-parameter warnings: {duplicates}"

    def test_renamed_flag_still_sends_the_spec_parameter_name(self):
        """End-to-end through Click: --format-param must put `format` on the wire."""
        captured = {}

        class FakeClient:
            def post(self, endpoint, data=None, params=None):
                captured["params"] = params
                return [{"ok": True}]

        import elisity_cli.context as ctxmod
        original = ctxmod.CliContext.ensure_client
        ctxmod.CliContext.ensure_client = lambda self: FakeClient()
        try:
            result = CliRunner().invoke(
                cli, ["flows", "get-pg-data", "--format-param", "csv", "--size", "10"]
            )
        finally:
            ctxmod.CliContext.ensure_client = original

        assert result.exit_code == 0, result.output
        # `size` goes on the wire as an int, not a string: CCC 26.7 declares it
        # {"type": "integer", "format": "int32"} where 26.3 declared only
        # {"format": "int32"} with no `type` key, which the generator could only
        # treat as a string. Seven query parameters gained a type this way in
        # 26.7. The renamed --format-param flag must still send `format`.
        assert captured["params"] == {"format": "csv", "size": 10}


# --------------------------------------------------------------------------
# 2. Hand-coded surface survival
# --------------------------------------------------------------------------


class TestHandCodedGroupsSurvive:
    def test_handcoded_groups_are_registered(self):
        for name in HANDCODED_GROUPS:
            assert name in COMMAND_GROUPS, (
                f"hand-coded group '{name}' is missing from COMMAND_GROUPS — "
                "regeneration unregistered it"
            )

    def test_handcoded_modules_exist_and_have_commands(self, counts):
        for name in HANDCODED_GROUPS:
            assert (COMMANDS_DIR / f"{name}.py").exists()
            assert counts["perGroup"].get(name, 0) > 0

    def test_handcoded_modules_are_not_marked_auto_generated(self):
        """A hand-coded module carrying the generator header means it was clobbered."""
        for name in HANDCODED_GROUPS:
            source = (COMMANDS_DIR / f"{name}.py").read_text()
            assert "Auto-generated from the Elisity CCC OpenAPI specification" not in source

    def test_render_init_keeps_handcoded_groups_when_spec_yields_none(self):
        """The regression this guards: __init__.py was rebuilt from generated
        groups only, silently dropping `reporting` and `glossary`."""
        rendered = render_init_module(["topology", "policy"])

        for name in HANDCODED_GROUPS:
            assert f'"{name}",' in rendered

    def test_render_init_is_deterministic_and_sorted(self):
        rendered = render_init_module(["topology", "ad", "policy"])
        names = re.findall(r'^\s*"([a-z_]+)",$', rendered, re.MULTILINE)

        assert names == sorted(names)
        assert rendered == render_init_module(["policy", "ad", "topology"])

    def test_generator_refuses_to_overwrite_a_handcoded_group(self, tmp_path):
        """If a future spec tag ever maps onto `reporting`/`glossary`, the
        generator must abort rather than overwrite hand-written commands."""
        import generate_commands

        spec_file = tmp_path / "spec.json"
        spec_file.write_text('{"paths": {"/api/reporting/v1/data": {"get": '
                             '{"tags": ["Bogus Reporting"], "operationId": "x", '
                             '"responses": {}}}}}')

        original = dict(generate_commands.TAG_TO_GROUP)
        generate_commands.TAG_TO_GROUP["Bogus Reporting"] = "reporting"
        try:
            with pytest.raises(SystemExit) as exc:
                generate_commands.main([
                    "--spec", str(spec_file), "--output-dir", str(tmp_path / "out"),
                ])
            assert "hand-coded" in str(exc.value)
            assert not (tmp_path / "out" / "reporting.py").exists()
        finally:
            generate_commands.TAG_TO_GROUP.clear()
            generate_commands.TAG_TO_GROUP.update(original)


# --------------------------------------------------------------------------
# 3. Documentation counts
# --------------------------------------------------------------------------


class TestDocumentedCounts:
    def test_docs_agree_with_source(self, counts):
        """README.md / command-reference.md numbers match a fresh source audit."""
        failures = [r for r in check_docs(counts) if r["status"] != "OK"]
        detail = "\n".join(f"  {r['claim']}: {r['detail']}" for r in failures)
        assert not failures, (
            f"{len(failures)} documented count(s) disagree with the source "
            f"tree:\n{detail}\n"
            "Run `python3 tools/audit_counts.py` and update the docs."
        )

    def test_structural_invariants_hold(self, counts):
        assert check_invariants(counts) == []

    def test_audit_script_exits_zero(self):
        """The script is wired into CI — it must be runnable standalone."""
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "audit_counts.py")],
            capture_output=True, text=True, cwd=str(REPO_ROOT),
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr

    def test_command_reference_is_regenerated(self):
        """docs/command-reference.md must match what the source would produce.

        It is a generated file, but nothing stops a regeneration from landing
        without it. When that happened on the 26.7 bump the doc listed 45
        commands that no longer existed and none of the 192 new ones — and a
        command reference that confidently documents removed commands is worse
        than none, because a reader cannot tell which entries are real.
        """
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "gen_command_reference.py"), "--check"],
            capture_output=True, text=True, cwd=str(REPO_ROOT),
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr

    def test_audit_script_json_mode_is_parseable(self):
        import json

        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "audit_counts.py"), "--json"],
            capture_output=True, text=True, cwd=str(REPO_ROOT),
        )
        payload = json.loads(proc.stdout)

        assert payload["counts"]["totals"]["total"] > 0
        assert payload["invariantFailures"] == []

    def test_audit_detects_injected_doc_drift(self, tmp_path, monkeypatch):
        """Negative test: the audit must FAIL on a wrong number, or it is
        worthless as a guard."""
        import tools.audit_counts as ac

        # Derive the claim from the source rather than hardcoding it. A literal
        # count here goes stale on the next spec bump, and a stale literal makes
        # the replace a no-op: no drift is injected, the audit correctly reports
        # nothing, and this negative test fails for the wrong reason. That is
        # exactly what happened on the 26.7 bump (466 -> 613).
        total = collect_counts()["totals"]["total"]
        marker = f"**{total} commands** total"
        original = ac.README.read_text()
        assert marker in original, (
            f"README does not state its total as {marker!r}; this test can no "
            "longer inject drift and must be updated with the README's wording."
        )

        fake = tmp_path / "README.md"
        fake.write_text(original.replace(marker, "**999999 commands** total"))
        monkeypatch.setattr(ac, "README", fake)

        failures = [r for r in ac.check_docs(collect_counts()) if r["status"] != "OK"]
        assert any("total commands" in r["claim"] for r in failures)


# --------------------------------------------------------------------------
# 4. Loadability
# --------------------------------------------------------------------------


class TestGroupsLoad:
    def test_every_registered_group_imports(self):
        for name in COMMAND_GROUPS:
            mod = __import__(f"elisity_cli.commands.{name}", fromlist=["group"])
            assert hasattr(mod, "group"), f"{name} module exposes no `group`"

    def test_root_help_lists_every_registered_group(self):
        result = CliRunner().invoke(cli, ["--help"])

        assert result.exit_code == 0
        for name in COMMAND_GROUPS:
            assert name in result.output, f"group '{name}' missing from root --help"

    def test_no_group_fails_to_load(self):
        """_register_groups swallows import errors with a warning — catch that."""
        result = CliRunner().invoke(cli, ["--help"])

        assert "Failed to load" not in result.output

    def test_every_module_on_disk_is_registered(self, counts):
        assert counts["registration"]["onDiskNotRegistered"] == []
        assert counts["registration"]["registeredNotOnDisk"] == []

    def test_group_command_counts_match_click_registry(self, counts):
        """Source-scan counts must equal what Click actually registered."""
        modules = audit_group_modules()
        for name, info in modules.items():
            mod = __import__(f"elisity_cli.commands.{name}", fromlist=["group"])
            assert len(mod.group.commands) == info["commands"], (
                f"{name}: source scan found {info['commands']} commands but "
                f"Click registered {len(mod.group.commands)}"
            )


# --------------------------------------------------------------------------
# Command-name overrides (CCC 26.9)
# --------------------------------------------------------------------------

DATA_DIR = REPO_ROOT / "tests" / "data"
# Naming skeletons of the 26.7 / 26.9 specs (tools/spec_skeleton.py): every
# operation's path, method, tags and operationId in spec order — all that
# naming and grouping read. Committed, so the naming guards below run in CI,
# where the full specs are not staged.
SKELETON_267 = DATA_DIR / "ccc-26.7-operations.json"
SKELETON_269 = DATA_DIR / "ccc-26.9-operations.json"
OVERLAY_269 = REPO_ROOT / "spec-overlays" / "ccc-26.9-hotpatch-device-patch.json"
OVERLAY_269_AD = REPO_ROOT / "spec-overlays" / "ccc-26.9-ad-group-views-body.json"
# Every overlay the committed tree is generated with, in the order the README gives.
OVERLAYS_269 = [OVERLAY_269, OVERLAY_269_AD]


def _emitted_names(spec):
    """{(METHOD, path): (group, command)} exactly as the generator emits them."""
    from generate_commands import dedupe_command_names

    groups, _ = build_groups(spec)
    return {
        (method.upper(), path): (group, name)
        for group, commands in groups.items()
        for method, path, _op, name in dedupe_command_names(commands)
    }


def _require(spec_path):
    if not spec_path.exists():
        # Where the specs are meant to be staged, a missing one must not turn
        # the byte-identity check into a quiet skip (Leia round 2, L-1).
        if os.environ.get("ELISITY_REQUIRE_SPECS") == "1":
            pytest.fail(f"{spec_path.name} not staged, and ELISITY_REQUIRE_SPECS=1")
        pytest.skip(f"{spec_path.name} not staged in this checkout")
    return json.loads(spec_path.read_text())


def _naming_spec(full_path, skeleton_path):
    """The full spec when staged, else its committed naming skeleton."""
    path = full_path if full_path.exists() else skeleton_path
    return json.loads(path.read_text())


def _spec_269():
    """What the committed tree is generated from: 26.9 + its overlays."""
    from generate_commands import apply_overlays

    spec, _notes = apply_overlays(_naming_spec(SPEC_269, SKELETON_269), OVERLAYS_269)
    return spec


def _spec_267():
    return _naming_spec(SPEC_267, SKELETON_267)


class TestCommandNameOverrides:
    """COMMAND_NAME_OVERRIDES pins names the operationId gets wrong.

    The 26.9 failure it exists for: new /v1/workloads/attach[ed] operations
    carried the operationIds `attach` / `attached`, so dedupe moved the shipped
    `devices attach` / `devices attached` to `attach-post` / `attached-post` and
    gave their names to a different endpoint. Nothing failed; the command
    count went up by exactly the right number.
    """

    def test_there_is_one_override_map(self):
        """PR #7 and the 26.9 regeneration each defined COMMAND_NAME_OVERRIDES;
        the second definition silently replaced the first."""
        source = (REPO_ROOT / "generate_commands.py").read_text()
        assert len(re.findall(r"^COMMAND_NAME_OVERRIDES\s*=", source, re.MULTILINE)) == 1

    def test_override_beats_the_operation_id(self):
        from generate_commands import make_command_name

        name = make_command_name(
            "get", "list_2", "/api/identity-graph/v1/workload-distribution-zones", "x"
        )
        assert name == "list-workload-distribution-zones"

    def test_operations_without_an_override_still_use_the_operation_id(self):
        from generate_commands import make_command_name

        assert make_command_name("get", "getAllSitesV2", "/api/x/v2/sites", "Sites") == (
            "get-all-sites-v2"
        )

    def test_a_colliding_override_fails_generation(self, monkeypatch):
        import generate_commands as gen

        spec = {"paths": {
            "/api/topology/v1/a": {"get": {"tags": ["Sites"], "operationId": "getThing",
                                           "responses": {"200": {}}}},
            "/api/topology/v1/b": {"get": {"tags": ["Sites"], "operationId": "other",
                                           "responses": {"200": {}}}},
        }}
        monkeypatch.setattr(gen, "COMMAND_NAME_OVERRIDES",
                            {("GET", "/api/topology/v1/b"): "get-thing"})
        groups, _ = gen.build_groups(spec)
        with pytest.raises(SystemExit, match="get-thing"):
            gen.assert_overrides_emitted(groups)

    def test_an_override_that_displaces_a_shipped_command_fails_generation(self, monkeypatch):
        """Leia M-1: the override comes FIRST in spec order, so dedupe suffixes
        the other, already-shipped command and the override itself is intact."""
        import generate_commands as gen

        spec = {"paths": {
            "/api/topology/v1/b": {"get": {"tags": ["Sites"], "operationId": "other",
                                           "responses": {"200": {}}}},
            "/api/topology/v1/a": {"get": {"tags": ["Sites"], "operationId": "getThing",
                                           "responses": {"200": {}}}},
        }}
        monkeypatch.setattr(gen, "COMMAND_NAME_OVERRIDES",
                            {("GET", "/api/topology/v1/b"): "get-thing"})
        groups, _ = gen.build_groups(spec)
        names = [n for _m, _p, _o, n in gen.dedupe_command_names(groups["topology"])]
        assert names == ["get-thing", "get-thing-get"]   # the displacement is real
        with pytest.raises(SystemExit, match="displaced by an override 'get-thing'"):
            gen.assert_overrides_emitted(groups)

    def test_leias_displacement_probe_fails_on_the_real_26_9_operations(self, monkeypatch):
        """The exact M-1 probe: an override taking `get-virtual-edge-by-id`
        used to pass the guard and push the shipped command to `-get`."""
        import generate_commands as gen

        monkeypatch.setitem(
            gen.COMMAND_NAME_OVERRIDES,
            ("GET", "/api/identity-graph/v1/workload-distribution-zones"),
            "get-virtual-edge-by-id",
        )
        groups, _ = gen.build_groups(_spec_269())
        with pytest.raises(SystemExit, match="get-virtual-edge-by-id"):
            gen.assert_overrides_emitted(groups)

    def test_the_committed_map_passes_the_guard(self):
        from generate_commands import assert_overrides_emitted

        for spec in (_spec_269(), _spec_267()):
            groups, _ = build_groups(spec)
            assert_overrides_emitted(groups)   # must not raise

    def test_every_override_exists_in_the_26_9_spec_and_is_emitted_verbatim(self):
        """Catches a typo in an override path, which would silently do nothing."""
        from generate_commands import COMMAND_NAME_OVERRIDES

        emitted = _emitted_names(_spec_269())
        for key, want in COMMAND_NAME_OVERRIDES.items():
            assert key in emitted, f"override for {key} matches no 26.9 operation"
            assert emitted[key][1] == want, (key, emitted[key])

    def test_platform_internal_operations_are_not_emitted(self):
        """The platform-internal operations in OMITTED_OPERATIONS (value None)
        get no command, in 26.9 and in 26.7 where some of them already existed."""
        from generate_commands import OMITTED_OPERATIONS

        internal = {(m.upper(), p) for (m, p), repl in OMITTED_OPERATIONS.items()
                    if repl is None}
        assert ("POST", "/api/identity-graph/v1/workloads/attach") in internal
        assert ("POST", "/api/identity-graph/v1/devices/attach") in internal
        assert ("POST", "/api/policy/v1/state/resync") in internal
        for spec in (_spec_269(), _spec_267()):
            emitted = _emitted_names(spec)
            assert not internal & set(emitted), sorted(internal & set(emitted))

    def test_no_26_9_addition_ships_a_generic_or_suffixed_name(self):
        old = _emitted_names(_spec_267())
        new = _emitted_names(_spec_269())
        generic = {"list", "usage", "export", "search", "attach", "attached", "get",
                   "create", "update", "delete"}
        bad = []
        for key in set(new) - set(old):
            group, name = new[key]
            if name in generic or re.search(r"-(get|post|put|patch|delete)(-\d+)?$", name):
                bad.append(f"{group} {name} ({key[0]} {key[1]})")
        assert bad == []

    def test_no_26_7_command_changes_name_or_group_except_the_documented_ones(self):
        old = _emitted_names(_spec_267())
        new = _emitted_names(_spec_269())
        moved = {k: (old[k], new[k]) for k in set(old) & set(new) if old[k] != new[k]}
        assert moved == {
            ("GET", "/api/reporting/v1/snapshots/{id}.pdf"):
                (("system", "retrieve-snapshot-image"), ("system", "retrieve-snapshot-pdf")),
        }

    def test_overrides_rename_exactly_one_26_7_command(self, monkeypatch):
        """Against 26.7 the map only renames suppression-list `get-users`.

        This is the README's regeneration check made executable: the 26.7
        command set still regenerates byte-for-byte apart from that one name.
        """
        import generate_commands as gen

        spec = _spec_267()
        with_map = _emitted_names(spec)
        monkeypatch.setattr(gen, "COMMAND_NAME_OVERRIDES", {})
        without = _emitted_names(spec)
        assert {k: (without[k], with_map[k]) for k in with_map if with_map[k] != without[k]} == {
            ("GET", "/api/identity-graph/v1/suppression"):
                (("devices", "get-users"), ("devices", "search-suppression-list")),
        }


class TestSpecSkeletons:
    """The committed skeletons are what the CI-side naming guards run on."""

    @pytest.mark.parametrize("full, skeleton", [(SPEC_269, SKELETON_269),
                                                (SPEC_267, SKELETON_267)])
    def test_skeleton_matches_the_full_spec(self, full, skeleton):
        import hashlib
        from tools.spec_skeleton import skeleton as make_skeleton

        _require(full)
        committed = json.loads(skeleton.read_text())
        assert committed["x-skeleton-of"]["sha256"] == hashlib.sha256(full.read_bytes()).hexdigest()
        assert committed["paths"] == make_skeleton(json.loads(full.read_text()))["paths"]

    def test_skeleton_names_match_the_full_spec(self):
        """Naming reads nothing the skeleton dropped."""
        from generate_commands import apply_overlays

        full, _ = apply_overlays(_require(SPEC_269), OVERLAYS_269)
        skel, _ = apply_overlays(json.loads(SKELETON_269.read_text()), OVERLAYS_269)
        assert _emitted_names(full) == _emitted_names(skel)


def _committed_commands():
    """{(METHOD, path-with-{}): (group, command)} read from the committed modules."""
    found = {}
    for module in sorted(COMMANDS_DIR.glob("*.py")):
        if module.stem in HANDCODED_GROUPS or module.name == "__init__.py":
            continue
        for block in module.read_text().split("@group.command(")[1:]:
            name = block.split('"')[1]
            endpoint = re.search(r'endpoint = f"([^"]+)"', block).group(1)
            verb = re.search(r"client\.(get|post|put|patch|delete)(?:_ndjson)?\(", block).group(1)
            found[(verb.upper(), re.sub(r"\{[^}]*\}", "{}", endpoint))] = (module.stem, name)
    return found


class TestCommittedTreeMatchesTheSpec:
    """The committed commands/ are exactly what the generator emits for 26.9."""

    def test_regenerating_from_26_9_reproduces_the_committed_modules(self, tmp_path):
        import generate_commands as gen

        _require(SPEC_269)
        overlay_args = [arg for o in OVERLAYS_269 for arg in ("--overlay", str(o))]
        assert gen.main(["--spec", str(SPEC_269), *overlay_args,
                         "--output-dir", str(tmp_path)]) == 0
        generated = {p.name for p in tmp_path.glob("*.py")}
        for name in sorted(generated):
            assert (tmp_path / name).read_text() == (COMMANDS_DIR / name).read_text(), (
                f"{name} differs from a fresh 26.9 regeneration"
            )
        on_disk = {p.name for p in COMMANDS_DIR.glob("*.py")}
        assert on_disk - generated == {f"{g}.py" for g in HANDCODED_GROUPS}

    def test_a_missing_spec_fails_when_specs_are_required(self, monkeypatch, tmp_path):
        """ELISITY_REQUIRE_SPECS=1 turns the byte-identity skip into a failure."""
        missing = tmp_path / "api-docs-26.9.0-release-demos.json"
        monkeypatch.setenv("ELISITY_REQUIRE_SPECS", "1")
        with pytest.raises(pytest.fail.Exception, match="ELISITY_REQUIRE_SPECS=1"):
            _require(missing)
        monkeypatch.delenv("ELISITY_REQUIRE_SPECS")
        with pytest.raises(pytest.skip.Exception):
            _require(missing)

    def test_committed_names_and_endpoints_match_26_9(self):
        """CI's stand-in for the byte-identity test above: every committed
        command has the name, group, method and path 26.9 (+ overlay) gives it."""
        want = {
            (method, re.sub(r"\{[^}]*\}", "{}", path)): name
            for (method, path), name in _emitted_names(_spec_269()).items()
        }
        assert _committed_commands() == want


class TestDeviceUpdateIsPatchOnly:
    """ENG-31333 on CCC 26.9: update-device = PATCH, and no device PUT."""

    def test_update_device_sends_patch_and_no_command_sends_the_device_put(self):
        committed = _committed_commands()
        assert committed[("PATCH", "/api/identity-graph/v1/devices/{}")] == (
            "devices", "update-device")
        assert ("PUT", "/api/identity-graph/v1/devices/{}") not in committed

    def test_26_9_without_the_overlay_refuses_to_generate(self, tmp_path):
        """Without the overlay, omitting the PUT would silently drop update-device."""
        import generate_commands as gen

        spec = json.loads(SKELETON_269.read_text())
        assert "patch" not in spec["paths"]["/api/identity-graph/v1/devices/{id}"]
        with pytest.raises(SystemExit, match="does not declare"):
            gen.assert_omitted_operations_replaced(spec)
        if SPEC_269.exists():
            with pytest.raises(SystemExit, match="--overlay"):
                gen.main(["--spec", str(SPEC_269), "--output-dir", str(tmp_path)])

    def test_overlay_clones_the_put_and_records_provenance(self):
        from generate_commands import DEVICE_PATH, apply_overlays

        base = _naming_spec(SPEC_269, SKELETON_269)
        spec, notes = apply_overlays(base, [OVERLAY_269])
        ops = spec["paths"][DEVICE_PATH]
        assert list(ops) == ["put", "patch", "delete"]   # PATCH sits where PUT did
        patch = ops["patch"]
        assert patch["x-elisity-overlay"] == "CCC 26.9 hot patch, ENG-31142/ENG-31333, 2026-10-15"
        assert patch["tags"] == ops["put"]["tags"]
        assert patch.get("parameters") == ops["put"].get("parameters")
        assert patch.get("requestBody") == ops["put"].get("requestBody")
        assert "204" in patch["responses"]
        assert "omitted" in patch["description"] and "ip" in patch["description"]
        assert "patch" not in base["paths"][DEVICE_PATH]   # input not mutated
        assert len(notes) == 1 and "added PATCH" in notes[0]

    def test_overlay_yields_to_a_spec_that_declares_the_patch(self):
        from generate_commands import DEVICE_PATH, apply_overlays

        native = {"tags": ["Device - CRUD"], "operationId": "patchDevice", "summary": "native"}
        spec = {"paths": {DEVICE_PATH: {"put": {"tags": ["Device - CRUD"]}, "patch": native}}}
        out, notes = apply_overlays(spec, [OVERLAY_269])
        assert out["paths"][DEVICE_PATH]["patch"] == native
        assert "already in the spec" in notes[0]

    def test_overlay_that_no_longer_fits_the_spec_fails(self):
        from generate_commands import DEVICE_PATH, apply_overlays

        with pytest.raises(SystemExit, match="does not fit"):
            apply_overlays({"paths": {DEVICE_PATH: {"delete": {}}}}, [OVERLAY_269])

    def test_malformed_overlay_entry_fails_with_a_message(self, tmp_path):
        from generate_commands import apply_overlays

        bad = tmp_path / "bad.json"
        bad.write_text(json.dumps({"provenance": "x", "operations": [{"path": "/a"}]}))
        with pytest.raises(SystemExit, match="missing method, cloneFrom"):
            apply_overlays({"paths": {}}, [bad])


class TestSetGroupsDefaultEnabledIsGated:
    """The 26.9 AD groups "master reset" requires --confirm (Obiwan, round 1 Q2)."""

    def test_classified_destructive(self):
        assert is_destructive_operation("PUT", "/api/ad-connector-service/v1/groups/default-enabled")
        assert not is_destructive_operation("GET", "/api/ad-connector-service/v1/groups/default-enabled")

    def test_refuses_without_confirm_and_sends_with_it(self, monkeypatch):
        import elisity_cli.context as ctxmod

        calls = []

        class RecordingClient:
            def put(self, endpoint, **kwargs):
                calls.append(("put", endpoint, kwargs))
                return {}

        monkeypatch.setattr(ctxmod.CliContext, "ensure_client", lambda self: RecordingClient())
        argv = ["ad", "set-groups-default-enabled", "--body", '{"enabled": true}']
        refused = CliRunner().invoke(cli, argv)
        assert refused.exit_code == 1 and calls == []
        assert "Use --confirm" in refused.output

        sent = CliRunner().invoke(cli, argv + ["--confirm"])
        assert sent.exit_code == 0, sent.output
        assert calls == [("put", "/api/ad-connector-service/v1/groups/default-enabled",
                          {"data": {"enabled": True}, "params": None})]
