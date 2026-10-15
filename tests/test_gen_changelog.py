"""Tests for tools/gen_changelog.py.

The changelog is the artifact a customer reads to find out what broke, so the
cases that matter are the ones that mislead when rendered wrongly: a removal
that is not flagged breaking, a rename shown as an addition, a body-only change
implying a signature break, and a parameter whose type went missing.
"""

import importlib.util
import json
import re
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent / "tools"


def _load_module():
    spec = importlib.util.spec_from_file_location("gen_changelog", TOOLS / "gen_changelog.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gen = _load_module()


def _diff(added=None, removed=None, changed=None, **summary):
    base = {
        "oldPathCount": 1,
        "newPathCount": 1,
        "oldOperationCount": 1,
        "newOperationCount": 1,
    }
    base.update(summary)
    return {
        "added": added or [],
        "removed": removed or [],
        "changed": changed or [],
        "summary": base,
    }


def _op(command="do-thing", group="policy", method="GET", path="/api/x", summary="", tags=None):
    return {
        "command": command,
        "group": group,
        "method": method,
        "path": path,
        "summary": summary,
        "tags": tags or ["Some Tag"],
    }


def _changed(command="do-thing", group="policy", changes=None):
    return {
        "command": command,
        "group": group,
        "method": "GET",
        "path": "/api/x",
        "changes": changes or {},
    }


def render(diff):
    return gen.render(diff, version="26.7", source="tenant.example", baseline="26.3")


# --------------------------------------------------------------------------
# Removals — the breaking case
# --------------------------------------------------------------------------


class TestRemovals:
    def test_removed_commands_are_listed_and_flagged_breaking(self):
        out = render(_diff(removed=[_op(command="delete-user", group="ad", summary="Delete AD user")]))
        assert "Removed commands (breaking)" in out
        assert "`elisity ad delete-user` — Delete AD user" in out

    def test_removals_are_grouped_by_spec_tag(self):
        out = render(
            _diff(
                removed=[
                    _op(command="a", tags=["AD User"]),
                    _op(command="b", tags=["AD User"]),
                    _op(command="c", tags=["AD Group"]),
                ]
            )
        )
        assert "**AD User** (2)" in out
        assert "**AD Group** (1)" in out

    def test_no_removals_says_none_rather_than_omitting_the_section(self):
        # A missing section reads as "not checked"; an explicit None reads as
        # "checked, nothing to report".
        out = render(_diff(added=[_op()]))
        removed_section = out.split("### Removed commands (breaking)")[1].split("###")[0]
        assert "None." in removed_section


# --------------------------------------------------------------------------
# Change classification
# --------------------------------------------------------------------------


class TestChangeClassification:
    def test_parameter_change_is_a_signature_change(self):
        entry = _changed(changes={"parameters": {"added": [{"name": "q", "required": False, "type": "string"}]}})
        assert gen._classify_change(entry) == "signature"

    def test_request_body_change_is_not_a_signature_change(self):
        # The generator emits the body as one opaque --body option, so a body
        # schema change cannot alter the command's flags. Calling it a
        # signature change would overstate the breakage.
        entry = _changed(changes={"requestBody": {"status": "changed"}})
        assert gen._classify_change(entry) == "body"

    def test_response_only_change_is_classified_response_only(self):
        entry = _changed(changes={"responses": {"added": ["202"]}})
        assert gen._classify_change(entry) == "response-only"

    def test_response_only_changes_are_counted_not_enumerated(self):
        out = render(_diff(changed=[_changed(command="quiet-cmd", changes={"responses": {"added": ["202"]}})]))
        assert "1 operations changed only in their response schema" in out
        assert "quiet-cmd" not in out

    def test_rename_is_reported_as_a_change_not_an_addition(self):
        out = render(_diff(changed=[_changed(command="get-state", changes={"command": {"from": "get-state-get", "to": "get-state"}})]))
        assert "renamed from `get-state-get`" in out
        assert "### Added commands" in out
        added_section = out.split("### Added commands")[1]
        assert "get-state" not in added_section


# --------------------------------------------------------------------------
# Signature detail rendering
# --------------------------------------------------------------------------


class TestSignatureDetail:
    def test_added_parameter_reports_name_requiredness_and_type(self):
        entry = _changed(changes={"parameters": {"added": [{"name": "size", "required": True, "type": "integer"}]}})
        assert gen._signature_detail(entry) == "new required `--size` (integer)"

    def test_removed_parameter_is_reported(self):
        entry = _changed(changes={"parameters": {"removed": [{"name": "columnFilter"}]}})
        assert "dropped `--columnFilter`" in gen._signature_detail(entry)

    def test_retype_uses_the_from_to_shape_spec_diff_actually_emits(self):
        # Regression guard: an earlier version assumed {"name":..,"type":{"from","to"}}
        # and silently rendered every retype as a bare "parameters changed".
        entry = _changed(
            changes={
                "parameters": {
                    "changed": [
                        {
                            "parameter": "query:size",
                            "from": {"name": "size", "type": "unknown", "required": True},
                            "to": {"name": "size", "type": "integer", "required": True},
                        }
                    ]
                }
            }
        )
        detail = gen._signature_detail(entry)
        assert "`--size`" in detail
        assert "integer" in detail
        assert detail != "parameters changed"

    def test_requiredness_flip_is_reported(self):
        entry = _changed(
            changes={
                "parameters": {
                    "changed": [
                        {
                            "parameter": "query:filters",
                            "from": {"name": "filters", "type": "object", "required": False},
                            "to": {"name": "filters", "type": "object", "required": True},
                        }
                    ]
                }
            }
        )
        assert "became required" in gen._signature_detail(entry)

    def test_untyped_is_explained_rather_than_shown_as_unknown(self):
        # "unknown -> integer" reads like a tooling gap. It is really the spec
        # gaining a type it never had, and the CLI sent a string meanwhile.
        assert gen._type_label("unknown") == "untyped (sent as string)"
        assert gen._type_label(None) == "untyped (sent as string)"
        assert gen._type_label("integer") == "integer"


# --------------------------------------------------------------------------
# Descriptions must come from the spec, never be invented
# --------------------------------------------------------------------------


class TestDescriptions:
    def test_summary_is_used_when_present(self):
        assert gen._describe(_op(summary="List all Vendors")) == "List all Vendors"

    def test_missing_summary_falls_back_to_method_and_path(self):
        # Inventing a description would put words in the API's mouth.
        assert gen._describe(_op(summary="", method="PUT", path="/api/y")) == "`PUT /api/y`"

    def test_multiline_summary_is_flattened_to_one_line(self):
        assert "\n" not in gen._describe(_op(summary="Line one\nline two"))


# --------------------------------------------------------------------------
# Totals
# --------------------------------------------------------------------------


class TestTotals:
    def test_headline_counts_match_the_diff_contents(self):
        out = render(
            _diff(
                added=[_op(command="a"), _op(command="b")],
                removed=[_op(command="c")],
                changed=[_changed(command="d", changes={"responses": {}})],
            )
        )
        assert "**2 commands added, 1 removed, 1 operations changed.**" in out

    def test_spec_path_and_operation_totals_are_rendered(self):
        out = render(_diff(oldOperationCount=436, newOperationCount=583, oldPathCount=329, newPathCount=441))
        assert "| Spec operations | 436 | 583 |" in out
        assert "| Spec paths | 329 | 441 |" in out


# --------------------------------------------------------------------------
# Reconciliation — "Removed" must not list commands that still exist
# --------------------------------------------------------------------------


def _full_op(group, command, method, path, parameters=None, tags=None):
    return {
        "group": group, "command": command, "method": method, "path": path,
        "tags": tags or ["Device - CRUD - v2"], "summary": "",
        "parameters": parameters or {}, "requestBody": None, "responses": {},
    }


def _param(name, where="query", required=False, ptype="string"):
    return {"name": name, "in": where, "required": required, "type": ptype}


class TestReconciliation:
    """A path rename is not a removal.

    spec_diff keys by (METHOD, path), so renaming the path of a SURVIVING
    operation reads as one removal plus one addition — while the command name,
    derived from the operationId, never moved. Rendered naively, the changelog
    listed 3 commands as "Removed (breaking) ... will now fail with No such
    command" that all still exist, two of them also under "Added" in the same
    document.
    """

    def _renamed_path_diff(self):
        """The real 26.7 case: the path gained a mandatory {attributeName}."""
        before = _full_op(
            "devices", "get-device-attribute-values-with-display-names", "GET",
            "/api/identity-graph/v2/devices/attributes/trustAttributes/values",
        )
        after = _full_op(
            "devices", "get-device-attribute-values-with-display-names", "GET",
            "/api/identity-graph/v2/devices/attributes/{attributeName}/values",
            parameters={
                "path:attributeName": _param("attributeName", "path", True),
                "query:queryString": _param("queryString"),
            },
        )
        return {"summary": {}, "added": [after], "removed": [before], "changed": []}

    def test_a_renamed_path_is_not_reported_as_a_removal(self):
        out = render(self._renamed_path_diff())
        removed_section = out.split("### Removed commands")[1].split("###")[0]
        assert "get-device-attribute-values-with-display-names" not in removed_section
        added_section = out.split("### Added commands")[1]
        assert "get-device-attribute-values-with-display-names" not in added_section

    def test_the_hidden_breaking_change_is_now_stated(self):
        """The worse half of the bug: the rename made an argument MANDATORY.

        Filed under "Removed", the reader got no migration guidance at all for a
        change that makes every existing invocation fail with
        `Missing argument 'ATTRIBUTENAME'`.
        """
        out = render(self._renamed_path_diff())
        sig = out.split("### Changed command signatures")[1].split("###")[0]
        assert "get-device-attribute-values-with-display-names" in sig
        assert "path moved from" in sig
        assert "new required `ATTRIBUTENAME`" in sig
        assert "new optional `--queryString`" in sig

    def test_a_genuine_removal_still_appears(self):
        """Reconciliation must not swallow real removals."""
        diff = {"summary": {}, "added": [],
                "removed": [_full_op("policy", "get-enforcement-score", "GET",
                                "/api/policy/v1/enforcement-score")],
                "changed": []}
        out = render(diff)
        removed_section = out.split("### Removed commands")[1].split("###")[0]
        assert "`elisity policy get-enforcement-score`" in removed_section
        assert "This command is gone" in removed_section

    def test_a_name_taken_over_by_another_operation_gets_its_own_section(self):
        """The quiet one. `/api/policy/v1/state` was deleted; the surviving
        `/api/state-sync/v1/state` inherited the freed name `policy get-state`.

        Nothing fails — the name still resolves and calls a different endpoint.
        Listing it under "will now fail with No such command" is backwards.
        """
        diff = {
            "summary": {}, "added": [],
            "removed": [_full_op("policy", "get-state", "GET", "/api/policy/v1/state")],
            "changed": [{
                "method": "GET", "path": "/api/state-sync/v1/state",
                "command": "get-state", "group": "policy", "parametersAfter": {},
                "changes": {"command": {"from": "get-state-get", "to": "get-state"}},
            }],
        }
        out = render(diff)
        removed_section = out.split("### Removed commands")[1].split("###")[0]
        assert "get-state" not in removed_section
        takeover = out.split("### Command names now pointing at a different endpoint")[1]
        assert "`elisity policy get-state`" in takeover
        assert "/api/policy/v1/state" in takeover
        assert "/api/state-sync/v1/state" in takeover
        assert "does not fail" in takeover

    def test_reconcile_is_a_no_op_when_nothing_overlaps(self):
        added = [_full_op("devices", "brand-new", "GET", "/api/x/new")]
        removed = [_full_op("devices", "long-gone", "GET", "/api/x/old")]
        assert gen.reconcile(added, removed, []) == (added, removed, [], [])


# --------------------------------------------------------------------------
# Flags, not spec names
# --------------------------------------------------------------------------


class TestFlagRendering:
    """The changelog must name the flag that works.

    It rendered `--{spec name}`, so it advertised `--format` on
    `devices export-devices` — where `--format` is the CLI's own output-format
    override. Leia drove it: `export-devices --format csv --body {}` exits 0
    with `params={}` (the value absorbed, never sent); `--format-param csv`
    exits 0 with `params={'format': 'csv'}`. Silent, no warning.
    """

    def _entry(self, **kwargs):
        base = {
            "method": "POST", "path": "/api/identity-graph/v2/devices/export",
            "command": "export-devices", "group": "devices",
            "parametersAfter": {"query:format": _param("format")},
            "changes": {"parameters": {"added": [_param("format")]}},
        }
        base.update(kwargs)
        return base

    def test_a_colliding_flag_renders_as_the_renamed_flag(self):
        detail = gen._signature_detail(self._entry())
        assert "`--format-param`" in detail
        assert "(sends `format`)" in detail
        assert "`--format` " not in detail

    def test_a_non_colliding_flag_renders_unchanged_with_no_noise(self):
        detail = gen._signature_detail(self._entry(
            parametersAfter={"query:siteId": _param("siteId")},
            changes={"parameters": {"added": [_param("siteId")]}},
        ))
        assert detail == "new optional `--siteId` (string)"

    def test_a_path_parameter_renders_as_a_positional_argument(self):
        """A path parameter has no flag at all — Click makes it positional."""
        detail = gen._signature_detail(self._entry(
            path="/api/x/{attributeName}/values",
            parametersAfter={"path:attributeName": _param("attributeName", "path", True)},
            changes={"parameters": {"added": [_param("attributeName", "path", True)]}},
        ))
        assert "new required `ATTRIBUTENAME`" in detail
        assert "--attributeName" not in detail

    def test_a_changed_parameter_also_uses_the_emitted_flag(self):
        detail = gen._signature_detail(self._entry(
            changes={"parameters": {"changed": [{
                "parameter": "query:format",
                "from": _param("format", ptype="unknown"),
                "to": _param("format"),
            }]}},
        ))
        assert "`--format-param`" in detail

    def test_the_real_diff_advertises_only_flags_that_exist(self):
        """Whole-changelog sweep against the live CLI surface.

        Every flag the rendered changelog names must actually be accepted by the
        command it names it on.
        """
        if not REAL_DIFF.exists():
            pytest.skip("26.7 diff artifact not present")
        from click.testing import CliRunner

        from elisity_cli.main import cli

        out = render(json.loads(REAL_DIFF.read_text()))
        pattern = re.compile(
            r"^- `elisity (?P<group>\S+) (?P<command>\S+)` — (?P<detail>.*)$", re.M
        )
        runner = CliRunner()
        offenders = []
        for match in pattern.finditer(out):
            # Only flags a caller is being told they can USE. A "dropped
            # `--columnFilter`" clause names a flag that is supposed to be gone;
            # demanding it still exist would invert the check.
            usable = "; ".join(
                bit for bit in match["detail"].split("; ")
                if not bit.startswith("dropped ")
            )
            flags = set(re.findall(r"`(--[A-Za-z0-9][\w.-]*)`", usable))
            if not flags:
                continue
            help_text = runner.invoke(
                cli, [match["group"], match["command"], "--help"]
            ).output
            for flag in flags:
                # Whole-token match. A substring test passes `--format` against
                # a help line that only offers `--format-param`, which is the
                # exact confusion this test exists to catch — the first version
                # of this assertion was vacuous for that reason.
                if not re.search(re.escape(flag) + r"(?![\w-])", help_text):
                    offenders.append(f"{match['group']} {match['command']}: {flag}")
        assert offenders == [], (
            "changelog advertises flags the command does not accept: "
            + ", ".join(offenders)
        )


# --------------------------------------------------------------------------
# End to end against the real 26.7 diff, when it is present
# --------------------------------------------------------------------------


REAL_DIFF = Path(__file__).resolve().parent.parent.parent / "output" / "SPEC-DIFF-26.7.json"


@pytest.mark.skipif(not REAL_DIFF.exists(), reason="26.7 diff artifact not present")
class TestAgainstRealDiff:
    def test_every_signature_change_renders_a_specific_reason(self):
        diff = json.loads(REAL_DIFF.read_text())
        vague = [
            c["command"]
            for c in diff["changed"]
            if gen._classify_change(c) == "signature"
            and gen._signature_detail(c) == "parameters changed"
        ]
        assert not vague, f"signature changes rendered without detail: {vague}"

    def test_renders_without_error_and_covers_every_removal(self):
        diff = json.loads(REAL_DIFF.read_text())
        out = render(diff)
        for op in diff["removed"]:
            assert f"`elisity {op['group']} {op['command']}`" in out
