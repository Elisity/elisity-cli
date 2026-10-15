"""The 26.9 AD group views send a JSON body, `{}` unless the user gives one.

The 26.9 spec declares getGroupsView, getGroupUsers and getGroupDevices with
`requestBody: null`, and the server answers a bodiless POST with 400 (live,
release-demos.idp02, 2026-10-15: no body 400, `{}` 200).
spec-overlays/ccc-26.9-ad-group-views-body.json supplies the body.
"""

import json
import re
from pathlib import Path

import pytest
import responses
from click.testing import CliRunner

import elisity_cli.context as ctxmod
from elisity_cli.client import CCCClient
from elisity_cli.main import cli

REPO_ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIR = REPO_ROOT / "src" / "elisity_cli" / "commands"
OVERLAY_AD = REPO_ROOT / "spec-overlays" / "ccc-26.9-ad-group-views-body.json"

BASE_URL = "https://test-ccc.elisity.io"
TOKEN_URL = f"{BASE_URL}/auth/realms/elisity/protocol/openid-connect/token"
GROUPS = "/api/ad-connector-service/v1/groups"

# (argv, wire path) for each of the three views.
VIEWS = [
    (["ad", "get-groups-view", "--size", "5"], GROUPS),
    (["ad", "get-group-users", "g-1", "--size", "5"], f"{GROUPS}/g-1/users"),
    (["ad", "get-group-devices", "g-1", "--size", "5"], f"{GROUPS}/g-1/devices"),
]
SPRING_PAGE = {"content": [], "totalElements": 0}


@pytest.fixture
def wire(monkeypatch):
    """Run the CLI against a fake CCC that records every request it gets."""
    client = CCCClient(base_url=BASE_URL, client_id="id", client_secret="secret")
    monkeypatch.setattr(ctxmod.CliContext, "ensure_client", lambda self: client)
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, TOKEN_URL, json={"access_token": "t", "expires_in": 300})
        rsps.add(responses.POST, re.compile(re.escape(BASE_URL + GROUPS) + r".*"),
                 json=SPRING_PAGE)

        def run(argv):
            result = CliRunner().invoke(cli, argv)
            sent = [c.request for c in rsps.calls if c.request.url.startswith(BASE_URL + GROUPS)]
            return result, sent

        yield run


@pytest.mark.parametrize("argv, path", VIEWS, ids=[v[0][1] for v in VIEWS])
class TestOnTheWire:
    def test_sends_an_empty_json_object_by_default(self, wire, argv, path):
        result, sent = wire(argv)

        assert result.exit_code == 0, result.output
        assert len(sent) == 1
        assert sent[0].url == f"{BASE_URL}{path}?size=5"
        assert sent[0].headers["Content-Type"] == "application/json"
        assert json.loads(sent[0].body) == {}

    def test_passes_body_through(self, wire, argv, path):
        body = {"filters": [{"field": "name", "value": "Eng"}]}
        result, sent = wire(argv + ["--body", json.dumps(body)])

        assert result.exit_code == 0, result.output
        assert sent[0].headers["Content-Type"] == "application/json"
        assert json.loads(sent[0].body) == body

    def test_passes_body_file_through(self, wire, argv, path, tmp_path):
        body = {"globalFilter": "x"}
        body_file = tmp_path / "body.json"
        body_file.write_text(json.dumps(body))
        result, sent = wire(argv + ["--body-file", str(body_file)])

        assert result.exit_code == 0, result.output
        assert json.loads(sent[0].body) == body


def test_no_other_command_defaults_a_body():
    """Only the three views send a body the user did not give — in particular
    no bodiless action endpoint gains one."""
    defaulted = []
    for module in sorted(COMMANDS_DIR.glob("*.py")):
        for block in module.read_text().split("@group.command(")[1:]:
            if re.search(r"^    body = (?!None$)", block, re.MULTILINE):
                defaulted.append(f'{module.stem} {block.split(chr(34))[1]}')
    assert sorted(defaulted) == ["ad get-group-devices", "ad get-group-users", "ad get-groups-view"]


class TestOverlay:
    def _spec(self, **declared):
        op = {"tags": ["AD Groups"], "operationId": "getGroupsView", "requestBody": None}
        op.update(declared)
        return {"paths": {
            GROUPS: {"post": op},
            f"{GROUPS}/{{id}}/users": {"post": {"tags": ["AD Groups"], "requestBody": None}},
            f"{GROUPS}/{{id}}/devices": {"post": {"tags": ["AD Groups"], "requestBody": None}},
        }}

    def test_gives_each_view_an_optional_json_body_and_a_default(self):
        from generate_commands import DEFAULT_BODY_KEY, apply_overlays

        base = self._spec()
        spec, notes = apply_overlays(base, [OVERLAY_AD])
        for path in spec["paths"]:
            op = spec["paths"][path]["post"]
            assert op["requestBody"]["required"] is False
            assert op["requestBody"]["content"]["application/json"]["schema"] == {"type": "object"}
            assert op[DEFAULT_BODY_KEY] == {}
            assert op["x-elisity-overlay"] == (
                "26.9 spec declares no body; server requires one; live 400 vs 200, 2026-10-15")
        assert len(notes) == 3 and all("set requestBody" in n for n in notes)
        assert base["paths"][GROUPS]["post"]["requestBody"] is None   # input not mutated

    def test_a_spec_that_declares_the_body_keeps_its_own(self):
        from generate_commands import apply_overlays

        native = {"required": True, "content": {"application/json": {"schema": {"$ref": "#/x"}}}}
        spec, notes = apply_overlays(self._spec(requestBody=native), [OVERLAY_AD])
        assert spec["paths"][GROUPS]["post"]["requestBody"] == native
        assert any("already declares requestBody" in n for n in notes)

    def test_patching_an_operation_the_spec_lacks_fails(self):
        from generate_commands import apply_overlays

        spec = self._spec()
        del spec["paths"][f"{GROUPS}/{{id}}/devices"]
        with pytest.raises(SystemExit, match="does not fit"):
            apply_overlays(spec, [OVERLAY_AD])

    def test_an_entry_cannot_both_clone_and_patch(self, tmp_path):
        from generate_commands import apply_overlays

        bad = tmp_path / "bad.json"
        bad.write_text(json.dumps({"provenance": "x", "operations": [
            {"path": "/a", "method": "post", "cloneFrom": "put", "patch": {"summary": "s"}}]}))
        with pytest.raises(SystemExit, match="both cloneFrom and patch"):
            apply_overlays({"paths": {}}, [bad])

    def test_a_patch_must_be_an_object(self, tmp_path):
        from generate_commands import apply_overlays

        bad = tmp_path / "bad.json"
        bad.write_text(json.dumps({"provenance": "x", "operations": [
            {"path": "/a", "method": "post", "patch": ["requestBody"]}]}))
        with pytest.raises(SystemExit, match="patch must be an object"):
            apply_overlays({"paths": {}}, [bad])

    def test_a_default_body_needs_a_request_body(self):
        from generate_commands import DEFAULT_BODY_KEY, generate_command

        with pytest.raises(ValueError, match="needs a requestBody"):
            generate_command("post", GROUPS, {DEFAULT_BODY_KEY: {}}, "get-groups-view")
