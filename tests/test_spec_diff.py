"""
Tests for tools/spec_diff.py.

Synthetic before/after spec fixtures cover every category the diff claims to
report: added, removed, changed (params / request body / responses / required
fields / tags / command rename), new mapped tags, new UNmapped tags, and the
no-change case. The unhappy paths matter most — a diff tool that silently
misses a removal is worse than no diff tool.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "tools"))

from tools.spec_diff import (  # noqa: E402
    diff_specs,
    expand_schema,
    main,
    render_text,
    schema_fingerprint,
)


# --------------------------------------------------------------------------
# Fixture helpers
# --------------------------------------------------------------------------


def make_spec(paths, schemas=None):
    """Minimal but structurally valid OpenAPI document."""
    return {
        "openapi": "3.0.1",
        "info": {"title": "Test API", "version": "1.0.0"},
        "paths": paths,
        "components": {"schemas": schemas or {}},
    }


def op(op_id, tag="site-controller", params=None, body=None, responses=None):
    """One operation. `tag` defaults to a tag that IS in TAG_TO_GROUP."""
    out = {"tags": [tag], "operationId": op_id, "summary": f"{op_id} summary"}
    if params is not None:
        out["parameters"] = params
    if body is not None:
        out["requestBody"] = body
    out["responses"] = responses if responses is not None else {
        "200": {"content": {"application/json": {"schema": {"type": "object"}}}}
    }
    return out


def qparam(name, ptype="string", required=False):
    return {"name": name, "in": "query", "required": required, "schema": {"type": ptype}}


def json_body(schema, required=True):
    return {"required": required, "content": {"application/json": {"schema": schema}}}


BASE_PATHS = {"/api/topology/v2/sites": {"get": op("getAllSites")}}


# --------------------------------------------------------------------------
# Added / removed
# --------------------------------------------------------------------------


def test_added_operation_is_reported_with_command_name():
    old = make_spec(dict(BASE_PATHS))
    new = make_spec({
        **BASE_PATHS,
        "/api/topology/v2/sites/{id}": {"get": op("getSiteV2")},
    })
    result = diff_specs(old, new)

    assert result["summary"]["added"] == 1
    assert result["summary"]["removed"] == 0
    added = result["added"][0]
    assert added["method"] == "GET"
    assert added["path"] == "/api/topology/v2/sites/{id}"
    assert added["operationId"] == "getSiteV2"
    assert added["tags"] == ["site-controller"]
    assert added["group"] == "topology"
    assert added["command"] == "get-site-v2"


def test_removed_operation_is_reported():
    old = make_spec({
        **BASE_PATHS,
        "/api/topology/v2/sites/{id}": {"delete": op("deleteSiteV2")},
    })
    new = make_spec(dict(BASE_PATHS))
    result = diff_specs(old, new)

    assert result["summary"]["removed"] == 1
    assert result["summary"]["added"] == 0
    assert result["removed"][0]["command"] == "delete-site-v2"
    assert result["removed"][0]["method"] == "DELETE"


def test_new_method_on_existing_path_is_an_addition_not_a_change():
    """Identity is (METHOD, path) — a second verb on a path is a new command."""
    old = make_spec({"/api/topology/v2/sites": {"get": op("getAllSites")}})
    new = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites"), "post": op("createSite")},
    })
    result = diff_specs(old, new)

    assert result["summary"]["added"] == 1
    assert result["summary"]["changed"] == 0
    assert result["added"][0]["method"] == "POST"


def test_path_rename_shows_as_removal_plus_addition():
    old = make_spec({"/api/v1/sites": {"get": op("getAllSites")}})
    new = make_spec({"/api/v2/sites": {"get": op("getAllSites")}})
    result = diff_specs(old, new)

    assert result["summary"]["added"] == 1
    assert result["summary"]["removed"] == 1
    assert result["summary"]["changed"] == 0


# --------------------------------------------------------------------------
# No-change / false-positive guard
# --------------------------------------------------------------------------


def test_identical_specs_report_no_changes():
    spec = make_spec({
        "/api/topology/v2/sites": {
            "get": op("getAllSites", params=[qparam("page", "integer")]),
            "post": op("createSite", body=json_body({"type": "object"})),
        }
    })
    result = diff_specs(spec, json.loads(json.dumps(spec)))

    s = result["summary"]
    assert (s["added"], s["removed"], s["changed"]) == (0, 0, 0)
    assert s["unchanged"] == 2
    assert s["newTags"] == 0


def test_key_reordering_is_not_a_change():
    """Serialization order must not manufacture a diff."""
    old = make_spec({
        "/api/topology/v2/sites": {
            "get": op("getAllSites", params=[qparam("a"), qparam("b")])
        }
    })
    new = make_spec({
        "/api/topology/v2/sites": {
            "get": op("getAllSites", params=[qparam("b"), qparam("a")])
        }
    })
    assert diff_specs(old, new)["summary"]["changed"] == 0


# --------------------------------------------------------------------------
# Changed — parameters
# --------------------------------------------------------------------------


def test_parameter_added():
    old = make_spec({"/api/topology/v2/sites": {"get": op("getAllSites")}})
    new = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites", params=[qparam("page", "integer")])}
    })
    result = diff_specs(old, new)

    assert result["summary"]["changed"] == 1
    added = result["changed"][0]["changes"]["parameters"]["added"]
    assert added[0]["name"] == "page"
    assert added[0]["type"] == "integer"


def test_parameter_removed():
    old = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites", params=[qparam("page", "integer")])}
    })
    new = make_spec({"/api/topology/v2/sites": {"get": op("getAllSites", params=[])}})
    result = diff_specs(old, new)

    removed = result["changed"][0]["changes"]["parameters"]["removed"]
    assert removed[0]["name"] == "page"


def test_parameter_retyped():
    old = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites", params=[qparam("page", "string")])}
    })
    new = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites", params=[qparam("page", "integer")])}
    })
    result = diff_specs(old, new)

    changed = result["changed"][0]["changes"]["parameters"]["changed"]
    assert changed[0]["from"]["type"] == "string"
    assert changed[0]["to"]["type"] == "integer"


def test_parameter_became_required():
    """A param flipping to required changes generated Click options — must surface."""
    old = make_spec({
        "/api/topology/v2/sites": {
            "get": op("getAllSites", params=[qparam("siteId", required=False)])
        }
    })
    new = make_spec({
        "/api/topology/v2/sites": {
            "get": op("getAllSites", params=[qparam("siteId", required=True)])
        }
    })
    result = diff_specs(old, new)

    changed = result["changed"][0]["changes"]["parameters"]["changed"]
    assert changed[0]["from"]["required"] is False
    assert changed[0]["to"]["required"] is True


def test_parameter_moved_between_query_and_path_is_add_plus_remove():
    old = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites", params=[qparam("id")])}
    })
    new_param = {"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}
    new = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites", params=[new_param])}
    })
    params = diff_specs(old, new)["changed"][0]["changes"]["parameters"]

    assert params["added"][0]["in"] == "path"
    assert params["removed"][0]["in"] == "query"


# --------------------------------------------------------------------------
# Changed — request body
# --------------------------------------------------------------------------


def test_request_body_added():
    old = make_spec({"/api/topology/v2/sites": {"post": op("createSite")}})
    new = make_spec({
        "/api/topology/v2/sites": {"post": op("createSite", body=json_body({"type": "object"}))}
    })
    result = diff_specs(old, new)

    assert result["changed"][0]["changes"]["requestBody"]["status"] == "added"


def test_request_body_removed():
    old = make_spec({
        "/api/topology/v2/sites": {"post": op("createSite", body=json_body({"type": "object"}))}
    })
    new = make_spec({"/api/topology/v2/sites": {"post": op("createSite")}})
    result = diff_specs(old, new)

    assert result["changed"][0]["changes"]["requestBody"]["status"] == "removed"


def test_request_body_required_fields_added_and_removed():
    old_schema = {"type": "object", "required": ["name"], "properties": {"name": {"type": "string"}}}
    new_schema = {
        "type": "object",
        "required": ["siteId"],
        "properties": {"name": {"type": "string"}, "siteId": {"type": "string"}},
    }
    old = make_spec({"/api/topology/v2/sites": {"post": op("createSite", body=json_body(old_schema))}})
    new = make_spec({"/api/topology/v2/sites": {"post": op("createSite", body=json_body(new_schema))}})

    body = diff_specs(old, new)["changed"][0]["changes"]["requestBody"]
    assert body["status"] == "changed"
    req = body["schema"][0]["requiredFields"]
    assert req["added"] == ["siteId"]
    assert req["removed"] == ["name"]


def test_request_body_schema_change_behind_a_ref_is_detected():
    """The $ref name is stable but the schema behind it gained a field."""
    ref = {"$ref": "#/components/schemas/Site"}
    old = make_spec(
        {"/api/topology/v2/sites": {"post": op("createSite", body=json_body(ref))}},
        schemas={"Site": {"type": "object", "properties": {"name": {"type": "string"}}}},
    )
    new = make_spec(
        {"/api/topology/v2/sites": {"post": op("createSite", body=json_body(ref))}},
        schemas={
            "Site": {
                "type": "object",
                "properties": {"name": {"type": "string"}, "region": {"type": "string"}},
            }
        },
    )
    body = diff_specs(old, new)["changed"][0]["changes"]["requestBody"]
    assert body["status"] == "changed"
    assert "schemaFingerprint" in body["schema"][0]


def test_request_body_content_type_added():
    old = make_spec({
        "/api/topology/v2/sites": {"post": op("createSite", body=json_body({"type": "object"}))}
    })
    body = {
        "required": True,
        "content": {
            "application/json": {"schema": {"type": "object"}},
            "multipart/form-data": {"schema": {"type": "object"}},
        },
    }
    new = make_spec({"/api/topology/v2/sites": {"post": op("createSite", body=body)}})

    ct = diff_specs(old, new)["changed"][0]["changes"]["requestBody"]["contentTypes"]
    assert ct["added"] == ["multipart/form-data"]


# --------------------------------------------------------------------------
# Changed — responses
# --------------------------------------------------------------------------


def test_response_code_added_and_removed():
    old = make_spec({
        "/api/topology/v2/sites": {
            "get": op("getAllSites", responses={"200": {"content": {}}, "404": {"content": {}}})
        }
    })
    new = make_spec({
        "/api/topology/v2/sites": {
            "get": op("getAllSites", responses={"200": {"content": {}}, "500": {"content": {}}})
        }
    })
    responses = diff_specs(old, new)["changed"][0]["changes"]["responses"]

    assert responses["added"] == ["500"]
    assert responses["removed"] == ["404"]


def test_response_shape_change_is_detected():
    old = make_spec({
        "/api/topology/v2/sites": {
            "get": op("getAllSites", responses={
                "200": {"content": {"application/json": {"schema": {"type": "object"}}}}
            })
        }
    })
    new = make_spec({
        "/api/topology/v2/sites": {
            "get": op("getAllSites", responses={
                "200": {"content": {"application/json": {"schema": {"type": "array"}}}}
            })
        }
    })
    responses = diff_specs(old, new)["changed"][0]["changes"]["responses"]

    assert responses["changed"][0]["status"] == "200"
    assert responses["changed"][0]["schema"][0]["from"] != responses["changed"][0]["schema"][0]["to"]


def test_ndjson_response_content_type_change_is_detected():
    """NDJSON drives a different client method in the generator — never silent."""
    old = make_spec({
        "/api/policy/v1/all": {
            "get": op("getAllAsNdJson", tag="Policy", responses={
                "200": {"content": {"application/json": {"schema": {"type": "object"}}}}
            })
        }
    })
    new = make_spec({
        "/api/policy/v1/all": {
            "get": op("getAllAsNdJson", tag="Policy", responses={
                "200": {"content": {"application/x-ndjson": {"schema": {"type": "object"}}}}
            })
        }
    })
    responses = diff_specs(old, new)["changed"][0]["changes"]["responses"]

    assert responses["changed"][0]["contentTypes"]["added"] == ["application/x-ndjson"]
    assert responses["changed"][0]["contentTypes"]["removed"] == ["application/json"]


# --------------------------------------------------------------------------
# Changed — identity fields
# --------------------------------------------------------------------------


def test_operation_id_change_renames_the_command():
    old = make_spec({"/api/topology/v2/sites": {"get": op("getAllSites")}})
    new = make_spec({"/api/topology/v2/sites": {"get": op("listAllSites")}})
    changes = diff_specs(old, new)["changed"][0]["changes"]

    assert changes["operationId"]["from"] == "getAllSites"
    assert changes["command"]["from"] == "get-all-sites"
    assert changes["command"]["to"] == "list-all-sites"


def test_tag_change_moves_the_command_between_groups():
    old = make_spec({"/api/x/sites": {"get": op("getAllSites", tag="site-controller")}})
    new = make_spec({"/api/x/sites": {"get": op("getAllSites", tag="Policy")}})
    changes = diff_specs(old, new)["changed"][0]["changes"]

    assert changes["group"]["from"] == "topology"
    assert changes["group"]["to"] == "policy"


# --------------------------------------------------------------------------
# Tags
# --------------------------------------------------------------------------


def test_new_mapped_tag_is_not_flagged_for_human_decision():
    old = make_spec({"/api/topology/v2/sites": {"get": op("getAllSites", tag="site-controller")}})
    new = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites", tag="site-controller")},
        "/api/policy/v1/sets": {"get": op("getPolicySets", tag="Policy")},
    })
    result = diff_specs(old, new)

    assert result["newTags"] == ["Policy"]
    assert result["unmappedNewTags"] == []
    assert result["summary"]["unmappedNewTags"] == 0


def test_new_unmapped_tag_is_surfaced_with_fallback_group_and_samples():
    old = make_spec({"/api/topology/v2/sites": {"get": op("getAllSites")}})
    new = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites")},
        "/api/topology/v3/quantum": {"get": op("getQuantum", tag="quantum-controller")},
        "/api/topology/v3/quantum/{id}": {"get": op("getQuantumById", tag="quantum-controller")},
    })
    result = diff_specs(old, new)

    assert result["summary"]["unmappedNewTags"] == 1
    entry = result["unmappedNewTags"][0]
    assert entry["tag"] == "quantum-controller"
    assert entry["operationCount"] == 2
    # No TAG_TO_GROUP entry -> path-prefix fallback put it in topology.
    assert entry["fallbackGroups"] == ["topology"]
    assert "/api/topology/v3/quantum" in entry["samplePaths"]


def test_unmapped_tag_falling_through_to_system_is_still_reported():
    """No recognizable path prefix -> 'system'. Still needs a human decision."""
    old = make_spec({"/api/topology/v2/sites": {"get": op("getAllSites")}})
    new = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites")},
        "/api/brandnew/thing": {"get": op("getThing", tag="brand-new-controller")},
    })
    entry = diff_specs(old, new)["unmappedNewTags"][0]

    assert entry["tag"] == "brand-new-controller"
    assert entry["fallbackGroups"] == ["system"]


def test_pre_existing_unmapped_tag_is_not_reported_as_new():
    """Only tags that are new in this diff need a decision."""
    paths = {"/api/brandnew/thing": {"get": op("getThing", tag="brand-new-controller")}}
    result = diff_specs(make_spec(paths), make_spec(dict(paths)))

    assert result["newTags"] == []
    assert result["unmappedNewTags"] == []


def test_new_group_is_reported_in_summary():
    old = make_spec({"/api/topology/v2/sites": {"get": op("getAllSites", tag="site-controller")}})
    new = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites", tag="site-controller")},
        "/api/ad-connector-service/v1/users": {"get": op("getAdUsers", tag="AD User")},
    })
    assert diff_specs(old, new)["summary"]["newGroups"] == ["ad"]


# --------------------------------------------------------------------------
# Schema expansion internals
# --------------------------------------------------------------------------


def test_expand_schema_inlines_refs():
    spec = make_spec({}, schemas={"Site": {"type": "object", "properties": {"n": {"type": "string"}}}})
    out = expand_schema({"$ref": "#/components/schemas/Site"}, spec)

    assert out["type"] == "object"
    assert out["properties"]["n"]["type"] == "string"


def test_expand_schema_survives_circular_refs():
    """A self-referencing schema must not hang or blow the stack."""
    spec = make_spec({}, schemas={
        "Node": {
            "type": "object",
            "properties": {"child": {"$ref": "#/components/schemas/Node"}},
        }
    })
    out = expand_schema({"$ref": "#/components/schemas/Node"}, spec)

    assert out["properties"]["child"] == {"$circular": "#/components/schemas/Node"}


def test_expand_schema_marks_unresolvable_refs():
    out = expand_schema({"$ref": "#/components/schemas/Missing"}, make_spec({}))
    assert out == {"$unresolved": "#/components/schemas/Missing"}


def test_schema_fingerprint_is_order_insensitive_but_content_sensitive():
    a = {"type": "object", "properties": {"x": {"type": "string"}, "y": {"type": "int"}}}
    b = {"properties": {"y": {"type": "int"}, "x": {"type": "string"}}, "type": "object"}
    c = {"type": "object", "properties": {"x": {"type": "string"}}}

    assert schema_fingerprint(a) == schema_fingerprint(b)
    assert schema_fingerprint(a) != schema_fingerprint(c)


# --------------------------------------------------------------------------
# Output contracts
# --------------------------------------------------------------------------


def test_json_output_is_serializable_and_has_stable_top_level_keys():
    old = make_spec({"/api/topology/v2/sites": {"get": op("getAllSites")}})
    new = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites", params=[qparam("page", "integer")])},
        "/api/topology/v3/quantum": {"get": op("getQuantum", tag="quantum-controller")},
    })
    result = diff_specs(old, new)

    round_tripped = json.loads(json.dumps(result))
    assert set(round_tripped) == {
        "summary", "added", "removed", "changed", "newTags", "unmappedNewTags",
    }
    assert set(round_tripped["summary"]) == {
        "oldOperationCount", "newOperationCount", "oldPathCount", "newPathCount",
        "added", "removed", "changed", "unchanged", "newTags", "unmappedNewTags",
        "newGroups", "handcodedGroups",
    }


def test_text_render_shouts_about_unmapped_tags():
    old = make_spec({"/api/topology/v2/sites": {"get": op("getAllSites")}})
    new = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites")},
        "/api/topology/v3/quantum": {"get": op("getQuantum", tag="quantum-controller")},
    })
    text = render_text(diff_specs(old, new), "old.json", "new.json")

    assert "HUMAN DECISION REQUIRED" in text
    assert "quantum-controller" in text
    assert "elisity topology get-quantum" in text


def test_text_render_handles_empty_diff():
    spec = make_spec(dict(BASE_PATHS))
    text = render_text(diff_specs(spec, json.loads(json.dumps(spec))), "a", "b")

    assert "added=0" in text
    assert text.count("(none)") == 3


# --------------------------------------------------------------------------
# CLI entry point
# --------------------------------------------------------------------------


@pytest.fixture
def spec_files(tmp_path):
    old = make_spec({"/api/topology/v2/sites": {"get": op("getAllSites")}})
    new = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites")},
        "/api/topology/v3/quantum": {"get": op("getQuantum", tag="quantum-controller")},
    })
    old_p, new_p = tmp_path / "old.json", tmp_path / "new.json"
    old_p.write_text(json.dumps(old))
    new_p.write_text(json.dumps(new))
    return str(old_p), str(new_p)


def test_cli_text_mode_exits_zero(spec_files, capsys):
    assert main([spec_files[0], spec_files[1]]) == 0
    assert "ADDED OPERATIONS (1)" in capsys.readouterr().out


def test_cli_json_mode_emits_valid_json(spec_files, capsys):
    assert main([spec_files[0], spec_files[1], "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["summary"]["added"] == 1


def test_cli_strict_exits_nonzero_on_unmapped_new_tag(spec_files, capsys):
    assert main([spec_files[0], spec_files[1], "--strict"]) == 1
    assert "need a TAG_TO_GROUP mapping" in capsys.readouterr().err


def test_cli_strict_exits_zero_when_all_new_tags_are_mapped(tmp_path, capsys):
    old = make_spec({"/api/topology/v2/sites": {"get": op("getAllSites")}})
    new = make_spec({
        "/api/topology/v2/sites": {"get": op("getAllSites")},
        "/api/policy/v1/sets": {"get": op("getPolicySets", tag="Policy")},
    })
    old_p, new_p = tmp_path / "o.json", tmp_path / "n.json"
    old_p.write_text(json.dumps(old))
    new_p.write_text(json.dumps(new))

    assert main([str(old_p), str(new_p), "--strict"]) == 0


def test_cli_missing_spec_file_fails_with_actionable_message(tmp_path):
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "spec_diff.py"),
         str(tmp_path / "nope.json"), str(tmp_path / "nope.json")],
        capture_output=True, text=True,
    )
    assert proc.returncode != 0
    assert "not found" in (proc.stdout + proc.stderr)


def test_cli_malformed_json_fails_cleanly(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "spec_diff.py"), str(bad), str(bad)],
        capture_output=True, text=True,
    )
    assert proc.returncode != 0
    assert "not valid JSON" in (proc.stdout + proc.stderr)


def test_overlay_is_applied_to_the_new_spec(tmp_path, capsys):
    """--overlay makes the diff describe what the CLI ships (CCC 26.9 hot patch)."""
    device = "/api/identity-graph/v1/devices/{id}"
    replace_op = op("updateDevice", tag="Device - CRUD", body=json_body({"type": "object"}),
                    responses={"204": {"description": "ok"}})
    spec = make_spec({device: {"put": replace_op}})
    old_p, new_p = tmp_path / "o.json", tmp_path / "n.json"
    old_p.write_text(json.dumps(spec))
    new_p.write_text(json.dumps(spec))
    overlay = REPO_ROOT / "spec-overlays" / "ccc-26.9-hotpatch-device-patch.json"

    assert main([str(old_p), str(new_p), "--json", "--overlay", str(overlay)]) == 0
    out = capsys.readouterr()
    added = json.loads(out.out)["added"]
    assert [(a["method"], a["path"], a["command"]) for a in added] == [
        ("PATCH", device, "update-device")]
    assert "added PATCH" in out.err
