"""
`devices update-device` must not knock a device offline (ENG-31142).

A PUT to /api/identity-graph/v1/devices/{id} without `ip` is a static-IP removal
in CCC: the device detaches and goes Offline. CCC 26.10 adds PATCH on the same
path (omitted ip keeps the current one); 26.9 and earlier answer PATCH with 405.
So the command GETs the device, fills unset ip/mac/venId, sends PATCH, and falls
back to PUT with the same filled body on 405.

The HTTP layer is mocked with `responses` (as in test_client.py) behind a real
CCCClient, so the 405 path goes through real `requests` errors. No live tenant
is contacted.
"""

import json
import re
import sys
from pathlib import Path

import pytest
import responses
from click.testing import CliRunner

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import generate_commands as gen  # noqa: E402
from elisity_cli.client import CCCClient
from elisity_cli.context import CliContext
from elisity_cli.main import cli

BASE_URL = "https://test-ccc.elisity.io"
TOKEN_URL = f"{BASE_URL}/auth/realms/elisity/protocol/openid-connect/token"
DEVICE_ID = "ffffffe3-3398-885e-0000-001ccc6777a1"
WRITE_URL = f"{BASE_URL}/api/identity-graph/v1/devices/{DEVICE_ID}"
READ_URL = f"{BASE_URL}/api/identity-graph/v2/devices/{DEVICE_ID}"
DEVICE_PATH = "/api/identity-graph/v1/devices/{id}"

ONLINE_DEVICE = {
    "id": DEVICE_ID,
    "ip": "10.20.30.40",
    "mac": "00:1C:CC:67:77:A1",
    "venId": "3",
    "status": "Online",
}
LABEL_BODY = {"attributes": {"label": ["Quarantine"]}, "auditComment": "SOAR quarantine action"}

DEVICES_MODULE = REPO_ROOT / "src" / "elisity_cli" / "commands" / "devices.py"


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def ccc(monkeypatch):
    """A real CCCClient behind `responses`, installed as the CLI's client."""
    client = CCCClient(base_url=BASE_URL, client_id="id", client_secret="secret")
    monkeypatch.setattr(CliContext, "ensure_client", lambda self: client)
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.POST, TOKEN_URL, json={"access_token": "t", "expires_in": 300})
        yield rsps


def run(runner, *args, body=LABEL_BODY):
    argv = ["devices", "update-device", DEVICE_ID]
    if body is not None:
        argv += ["--body", json.dumps(body)]
    return runner.invoke(cli, argv + list(args))


def api_calls(rsps):
    """(method, url-without-query, json-body) for every call except the token."""
    out = []
    for call in rsps.calls:
        req = call.request
        if req.url.startswith(TOKEN_URL):
            continue
        sent = json.loads(req.body) if req.body else None
        out.append((req.method, req.url.split("?")[0], sent))
    return out


def writes(rsps):
    return [c for c in api_calls(rsps) if c[0] in ("PUT", "PATCH")]


# ---------------------------------------------------------------------------
# CCC 26.10: PATCH accepted
# ---------------------------------------------------------------------------

def test_label_only_body_is_patched_with_current_ip_mac_venid(runner, ccc):
    ccc.add(responses.GET, READ_URL, json=ONLINE_DEVICE)
    ccc.add(responses.PATCH, WRITE_URL, status=204)

    result = run(runner)

    assert result.exit_code == 0, result.output
    expected = dict(LABEL_BODY, ip="10.20.30.40", mac="00:1C:CC:67:77:A1", venId="3")
    assert api_calls(ccc) == [("GET", READ_URL, None), ("PATCH", WRITE_URL, expected)]
    assert "kept the device's current ip, mac, venId" in result.stderr
    assert "PUT" not in result.stderr.split("Use --allow-ip-removal")[0]


def test_target_enrichment_layer_is_sent_on_the_patch(runner, ccc):
    ccc.add(responses.GET, READ_URL, json=ONLINE_DEVICE)
    ccc.add(responses.PATCH, WRITE_URL, status=204)

    result = run(runner, "--target-enrichment-layer", "STATIC")

    assert result.exit_code == 0, result.output
    patch = [c for c in ccc.calls if c.request.method == "PATCH"][0]
    assert "target-enrichment-layer=STATIC" in patch.request.url


def test_body_file_is_filled_the_same_way(runner, ccc, tmp_path):
    ccc.add(responses.GET, READ_URL, json=ONLINE_DEVICE)
    ccc.add(responses.PATCH, WRITE_URL, status=204)
    body_file = tmp_path / "body.json"
    body_file.write_text(json.dumps(LABEL_BODY))

    result = runner.invoke(cli, ["devices", "update-device", DEVICE_ID, "--body-file", str(body_file)])

    assert result.exit_code == 0, result.output
    assert writes(ccc)[0][2]["ip"] == "10.20.30.40"


# ---------------------------------------------------------------------------
# CCC 26.9 and earlier: PATCH -> 405 -> PUT with the same filled body
# ---------------------------------------------------------------------------

def test_patch_405_falls_back_to_put_with_the_same_filled_body(runner, ccc):
    ccc.add(responses.GET, READ_URL, json=ONLINE_DEVICE)
    ccc.add(responses.PATCH, WRITE_URL, status=405,
            json={"message": "Request method 'PATCH' is not supported"})
    ccc.add(responses.PUT, WRITE_URL, status=204)

    result = run(runner, "--target-enrichment-layer", "STATIC")

    assert result.exit_code == 0, result.output
    (m1, u1, b1), (m2, u2, b2) = writes(ccc)
    assert (m1, m2) == ("PATCH", "PUT")
    assert b1 == b2
    assert b2["ip"] == "10.20.30.40" and b2["mac"] == "00:1C:CC:67:77:A1" and b2["venId"] == "3"
    put = [c for c in ccc.calls if c.request.method == "PUT"][0]
    assert "target-enrichment-layer=STATIC" in put.request.url
    note_lines = [line for line in result.stderr.splitlines() if line.startswith("Note:")]
    assert len(note_lines) == 1
    assert "PUT" in note_lines[0] and "26.9" in note_lines[0]


@pytest.mark.parametrize("status", [400, 404, 412, 500])
def test_only_405_falls_back(runner, ccc, status):
    ccc.add(responses.GET, READ_URL, json=ONLINE_DEVICE)
    ccc.add(responses.PATCH, WRITE_URL, status=status, json={"message": "nope"})

    result = run(runner)

    assert result.exit_code == 1
    assert [c[0] for c in writes(ccc)] == ["PATCH"]


def test_failed_put_fallback_exits_1_and_says_so(runner, ccc):
    ccc.add(responses.GET, READ_URL, json=ONLINE_DEVICE)
    ccc.add(responses.PATCH, WRITE_URL, status=405)
    ccc.add(responses.PUT, WRITE_URL, status=412)

    result = run(runner)

    assert result.exit_code == 1
    assert "PUT fallback failed" in result.stderr


# ---------------------------------------------------------------------------
# What gets filled
# ---------------------------------------------------------------------------

def test_user_supplied_ip_is_respected(runner, ccc):
    ccc.add(responses.GET, READ_URL, json=ONLINE_DEVICE)
    ccc.add(responses.PATCH, WRITE_URL, status=204)

    result = run(runner, body=dict(LABEL_BODY, ip="10.99.99.99"))

    assert result.exit_code == 0, result.output
    sent = writes(ccc)[0][2]
    assert sent["ip"] == "10.99.99.99"
    assert sent["mac"] == "00:1C:CC:67:77:A1" and sent["venId"] == "3"
    assert "current mac, venId" in result.stderr


def test_user_supplied_ip_mac_venid_send_no_note(runner, ccc):
    ccc.add(responses.GET, READ_URL, json=ONLINE_DEVICE)
    ccc.add(responses.PATCH, WRITE_URL, status=204)
    body = dict(LABEL_BODY, ip="10.99.99.99", mac="AA:BB:CC:DD:EE:FF", venId="7")

    result = run(runner, body=body)

    assert result.exit_code == 0, result.output
    assert writes(ccc)[0][2] == body
    assert "Note:" not in result.stderr


@pytest.mark.parametrize("unset", [None, ""])
def test_null_or_empty_ip_counts_as_unset(runner, ccc, unset):
    ccc.add(responses.GET, READ_URL, json=ONLINE_DEVICE)
    ccc.add(responses.PATCH, WRITE_URL, status=204)

    result = run(runner, body=dict(LABEL_BODY, ip=unset))

    assert result.exit_code == 0, result.output
    assert writes(ccc)[0][2]["ip"] == "10.20.30.40"


def test_ipaddress_is_not_ip(runner, ccc):
    ccc.add(responses.GET, READ_URL, json=ONLINE_DEVICE)
    ccc.add(responses.PATCH, WRITE_URL, status=204)

    result = run(runner, body=dict(LABEL_BODY, ipAddress="10.99.99.99"))

    assert result.exit_code == 0, result.output
    assert writes(ccc)[0][2]["ip"] == "10.20.30.40"


@pytest.mark.parametrize("no_ip", [{}, {"ip": None}, {"ip": ""}])
def test_device_without_ip_gets_the_body_unchanged(runner, ccc, no_ip):
    device = dict(ONLINE_DEVICE, status="Offline")
    device.pop("ip")
    device.update(no_ip)
    ccc.add(responses.GET, READ_URL, json=device)
    ccc.add(responses.PATCH, WRITE_URL, status=204)

    result = run(runner)

    assert result.exit_code == 0, result.output
    assert writes(ccc) == [("PATCH", WRITE_URL, LABEL_BODY)]
    assert "Note:" not in result.stderr


def test_device_without_ip_on_26_9_puts_the_body_unchanged(runner, ccc):
    device = {k: v for k, v in ONLINE_DEVICE.items() if k != "ip"}
    ccc.add(responses.GET, READ_URL, json=device)
    ccc.add(responses.PATCH, WRITE_URL, status=405)
    ccc.add(responses.PUT, WRITE_URL, status=204)

    result = run(runner)

    assert result.exit_code == 0, result.output
    assert writes(ccc) == [("PATCH", WRITE_URL, LABEL_BODY), ("PUT", WRITE_URL, LABEL_BODY)]
    assert "PUT" in result.stderr


# ---------------------------------------------------------------------------
# Opt-out
# ---------------------------------------------------------------------------

def test_allow_ip_removal_puts_the_body_as_given_without_reading(runner, ccc):
    ccc.add(responses.PUT, WRITE_URL, status=204)

    result = run(runner, "--allow-ip-removal")

    assert result.exit_code == 0, result.output
    assert api_calls(ccc) == [("PUT", WRITE_URL, LABEL_BODY)]
    assert "Note:" not in result.stderr


def test_allow_ip_removal_is_in_help(runner):
    result = runner.invoke(cli, ["devices", "update-device", "--help"])
    assert result.exit_code == 0
    assert "--allow-ip-removal" in result.output


# ---------------------------------------------------------------------------
# Fail closed: no device read, no write
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("read", [
    {"status": 404, "json": {"message": "not found"}},
    {"status": 500, "json": {"message": "boom"}},
    {"status": 200, "body": ""},
    {"status": 200, "body": "<html>not json</html>"},
    {"status": 200, "json": []},
])
def test_unreadable_device_exits_1_without_writing(runner, ccc, read):
    ccc.add(responses.GET, READ_URL, **read)

    result = run(runner)

    assert result.exit_code == 1
    assert writes(ccc) == []
    assert "nothing was sent" in result.stderr


def test_get_connection_error_exits_1_without_writing(runner, ccc, monkeypatch):
    import requests
    import tenacity

    # Skip the client's retry back-off; the failure is what matters.
    monkeypatch.setattr(CCCClient._request.retry, "wait", tenacity.wait_none())
    ccc.add(responses.GET, READ_URL, body=requests.exceptions.ConnectionError("down"))

    result = run(runner)

    assert result.exit_code == 1
    assert writes(ccc) == []


@pytest.mark.parametrize("body", [None, ["not", "an", "object"]])
def test_non_object_body_exits_1_without_any_request(runner, ccc, body):
    result = run(runner, body=body)

    assert result.exit_code == 1
    assert api_calls(ccc) == []


# ---------------------------------------------------------------------------
# Survives generate_commands.py
# ---------------------------------------------------------------------------

def _spec_put_operation():
    """The 26.7 spec's PUT /api/identity-graph/v1/devices/{id}, as declared there."""
    return {
        "tags": ["Device - CRUD"],
        "summary": "Update device by ID",
        "operationId": "updateDevice",
        "parameters": [
            {"name": "id", "in": "path", "required": True, "description": "ID of device (UUID)",
             "schema": {"type": "string", "format": "uuid"}},
            {"name": "target-enrichment-layer", "in": "query", "required": False,
             "schema": {"type": "string"}},
            {"name": "If-Match", "in": "header", "required": False, "schema": {"type": "string"}},
        ],
        "requestBody": {"content": {"application/json": {
            "schema": {"$ref": "#/components/schemas/DeviceUpdateRequest"}}}, "required": True},
        "responses": {"204": {"description": "No Content"}},
    }


def _committed_block(name):
    src = DEVICES_MODULE.read_text()
    m = re.search(rf'^@group\.command\("{name}"\)\n.*?(?=\n\n@group\.command|\n\Z)', src, re.S | re.M)
    assert m, f"{name} not found in {DEVICES_MODULE}"
    return m.group(0)


def test_committed_update_device_is_what_the_generator_emits():
    emitted = gen.generate_command("put", DEVICE_PATH, _spec_put_operation(), "update-device")
    assert _committed_block("update-device") == emitted


def test_generator_emits_patch_path_and_opt_out_for_update_device():
    emitted = gen.generate_command("put", DEVICE_PATH, _spec_put_operation(), "update-device")
    assert "update_device(client, endpoint, id, body, params, allow_ip_removal=allow_ip_removal)" in emitted
    assert '"--allow-ip-removal"' in emitted
    assert "client.put(" not in emitted


def test_no_other_generated_command_carries_the_guard():
    hits = []
    for module in DEVICES_MODULE.parent.glob("*.py"):
        for m in re.finditer(r'@group\.command\("([^"]+)"\)(.*?)(?=\n@group\.command|\Z)',
                             module.read_text(), re.S):
            if "= update_device(client" in m.group(2) or "--allow-ip-removal" in m.group(2):
                hits.append(f"{module.stem} {m.group(1)}")
    assert hits == ["devices update-device"]


def test_guard_on_another_operation_is_not_emitted():
    op = _spec_put_operation()
    emitted = gen.generate_command("put", "/api/identity-graph/v1/devices/bulk", op, "bulk-update-devices")
    assert "update_device(" not in emitted and "--allow-ip-removal" not in emitted


def _groups(*ops):
    return {"devices": [(m, p, _spec_put_operation(), n) for m, p, n in ops]}


def test_generator_refuses_when_the_device_path_is_gone():
    with pytest.raises(SystemExit) as exc:
        gen.assert_device_attachment_guarded(_groups(("put", "/api/identity-graph/v1/device/{id}", "update-device")))
    assert "is not in the spec" in str(exc.value)


def test_generator_refuses_when_another_operation_takes_the_name():
    # e.g. a 26.10 PATCH whose operationId also sanitizes to update-device, listed first.
    groups = _groups(("patch", DEVICE_PATH, "update-device"), ("put", DEVICE_PATH, "update-device"))
    with pytest.raises(SystemExit) as exc:
        gen.assert_device_attachment_guarded(groups)
    assert "update-device-put" in str(exc.value)


def test_generator_accepts_the_current_layout():
    gen.assert_device_attachment_guarded(_groups(("put", DEVICE_PATH, "update-device")))
