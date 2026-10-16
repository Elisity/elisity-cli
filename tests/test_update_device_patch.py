"""`devices update-device` sends PATCH so attribute-only edits keep the device's IP."""

import json

import pytest
import responses
from click.testing import CliRunner

import elisity_cli.context as ctxmod
from elisity_cli.main import cli
from elisity_cli.client import CCCClient
from generate_commands import DEVICE_PATH, build_groups, generate_module

BASE_URL = "https://test-ccc.elisity.io"
TOKEN_URL = f"{BASE_URL}/auth/realms/elisity/protocol/openid-connect/token"
DEVICE_URL = f"{BASE_URL}/api/identity-graph/v1/devices/dev-1"


@pytest.fixture
def client():
    return CCCClient(base_url=BASE_URL, client_id="id", client_secret="secret")


def _run(argv):
    calls = []

    class RecordingClient:
        def __getattr__(self, verb):
            def call(endpoint, **kwargs):
                calls.append((verb, endpoint, kwargs))
                return {}

            return call

    original = ctxmod.CliContext.ensure_client
    ctxmod.CliContext.ensure_client = lambda self: RecordingClient()
    try:
        result = CliRunner().invoke(cli, argv)
    finally:
        ctxmod.CliContext.ensure_client = original
    return result, calls


class TestUpdateDeviceCommand:
    def test_sends_patch_with_the_body_untouched(self):
        body = {"attributes": {"label": "Quarantine"}}
        result, calls = _run(["devices", "update-device", "dev-1", "--body", json.dumps(body)])

        assert result.exit_code == 0, result.output
        assert calls == [
            ("patch", "/api/identity-graph/v1/devices/dev-1", {"data": body, "params": {}}),
        ]

    def test_ip_in_body_is_passed_through(self):
        body = {"ip": "10.0.0.7"}
        result, calls = _run(["devices", "update-device", "dev-1", "--body", json.dumps(body)])

        assert result.exit_code == 0, result.output
        assert calls[0][0] == "patch"
        assert calls[0][2]["data"] == body

    def test_target_enrichment_layer_is_sent_as_a_query_parameter(self):
        result, calls = _run(
            ["devices", "update-device", "dev-1", "--target-enrichment-layer", "STATIC", "--body", "{}"]
        )

        assert result.exit_code == 0, result.output
        assert calls[0][2]["params"] == {"target-enrichment-layer": "STATIC"}


class TestPatchClient:
    @responses.activate
    def test_patch_forwards_query_params_and_accepts_an_empty_204(self, client):
        responses.add(responses.POST, TOKEN_URL, json={"access_token": "t", "expires_in": 300})
        responses.add(responses.PATCH, DEVICE_URL, status=204)

        result = client.patch(
            "/api/identity-graph/v1/devices/dev-1",
            data={"attributes": {}},
            params={"target-enrichment-layer": "STATIC"},
        )

        assert result == {}
        sent = responses.calls[-1].request
        assert sent.method == "PATCH"
        assert sent.url.endswith("?target-enrichment-layer=STATIC")


class TestGeneratorOverrides:
    SPEC = {
        "paths": {
            DEVICE_PATH: {
                "put": {"tags": ["Device"], "operationId": "updateDevice", "responses": {"204": {}}},
                "patch": {"tags": ["Device"], "operationId": "patchDevice", "responses": {"204": {}},
                          "requestBody": {"content": {"application/json": {"schema": {"type": "object"}}}}},
            }
        }
    }

    def _commands(self):
        groups, _ = build_groups(self.SPEC)
        return [name for g in groups.values() for (_, _, _, name) in g], groups

    def test_put_is_omitted_and_patch_takes_the_update_device_name(self):
        names, groups = self._commands()
        assert names == ["update-device"]
        [(method, _, _, _)] = [c for g in groups.values() for c in g]
        assert method == "patch"

    def test_generated_command_calls_patch_with_params(self):
        _, groups = self._commands()
        [group] = groups.values()
        module = generate_module("devices", group)
        assert "client.patch(endpoint, data=body, params=params)" in module
        assert "client.put(" not in module
