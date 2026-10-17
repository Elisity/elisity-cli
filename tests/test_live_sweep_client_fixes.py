"""Client defects found by the 26.9 live sweep (release-demos.idp02, 2026-10-15).

1. `Accept: application/json` on every request: the server answers the 26.9
   operations whose only 2xx is text/plain with 406.
2. Required header parameters were dropped by the generator: the state-sync
   task calls (X-Elisity-VE) and policy-group sibling-order (If-Match) could
   not be made.
3. A failed call printed only `400 Client Error: ... for url: ...`; the
   server's own message never reached the user.
"""

import json
import re

import pytest
import responses
from click.testing import CliRunner

import elisity_cli.context as ctxmod
from elisity_cli.client import CCCClient
from elisity_cli.main import cli

BASE_URL = "https://test-ccc.elisity.io"
TOKEN_URL = f"{BASE_URL}/auth/realms/elisity/protocol/openid-connect/token"
TOKEN = "tok-SECRET-123"


@pytest.fixture
def fake():
    """A fake CCC; yields (rsps, run) where run(argv) invokes the CLI."""
    client = CCCClient(base_url=BASE_URL, client_id="id", client_secret="secret")
    mp = pytest.MonkeyPatch()
    mp.setattr(ctxmod.CliContext, "ensure_client", lambda self: client)
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.POST, TOKEN_URL, json={"access_token": TOKEN, "expires_in": 300})
        yield rsps, lambda argv: CliRunner().invoke(cli, argv)
    mp.undo()


def _api_calls(rsps):
    return [c.request for c in rsps.calls if c.request.url != TOKEN_URL]


# --- 1. Accept ---------------------------------------------------------------

def _admits_text_plain(accept):
    for item in (accept or "").split(","):
        media, *params = [x.strip() for x in item.split(";")]
        q = next((float(p[2:]) for p in params if p.startswith("q=")), 1.0)
        if media in ("text/plain", "text/*", "*/*") and q > 0:
            return True
    return False


def _text_plain_only(body):
    """Spring's behaviour on a text/plain-only handler."""
    def callback(request):
        if not _admits_text_plain(request.headers.get("Accept")):
            return (406, {"Content-Type": "application/json"}, json.dumps(
                {"status": 406, "error": "Not Acceptable",
                 "message": "Acceptable representations: [text/plain]."}))
        return (200, {"Content-Type": "text/plain"}, body)
    return callback


@pytest.mark.parametrize("method, path, argv, body", [
    ("GET", "/api/identity-graph/v1/devices/attach/can-accept-from/ven-1",
     ["devices", "check-ven-availability", "ven-1"], "true"),
    ("POST", "/api/identity-graph/v1/labels",
     ["policy", "create", "--body", '{"name": "clisweep-x"}'], "5f2c-label-id"),
])
def test_text_plain_only_operation_succeeds(fake, method, path, argv, body):
    rsps, run = fake
    rsps.add_callback(method, BASE_URL + path, callback=_text_plain_only(body))

    result = run(argv)

    assert result.exit_code == 0, result.output
    assert body in result.stdout
    assert _api_calls(rsps)[0].headers["Accept"].startswith("application/json")


# --- 2. Required header parameters -------------------------------------------

HEADER_OPS = [
    ("GET", "/api/state-sync/v1/tasks/next", ["system", "get-next-task-for-ve"],
     "--x-elisity-ve", "X-Elisity-VE"),
    ("PUT", "/api/state-sync/v1/tasks/t-1/release", ["system", "release-execution-of-task", "t-1"],
     "--x-elisity-ve", "X-Elisity-VE"),
    ("PUT", "/api/state-sync/v1/tasks/t-1/ack", ["system", "ack-execution-of-task", "t-1"],
     "--x-elisity-ve", "X-Elisity-VE"),
    ("POST", "/api/state-sync/v1/tasks/t-1/ack", ["system", "ack-execution-of-task-post", "t-1"],
     "--x-elisity-ve", "X-Elisity-VE"),
    ("PUT", "/api/policy/v2/policy-groups/dynamic/g-1/sibling-order",
     ["policy", "reorder-siblings", "g-1"], "--if-match", "If-Match"),
]


@pytest.mark.parametrize("method, path, argv, flag, header", HEADER_OPS,
                         ids=[op[2][1] for op in HEADER_OPS])
class TestRequiredHeader:
    def test_value_is_sent_as_the_header(self, fake, method, path, argv, flag, header):
        rsps, run = fake
        rsps.add(method, re.compile(re.escape(BASE_URL + path) + r"(\?.*)?$"), json={})

        result = run(argv + [flag, "ve-42"])

        assert result.exit_code == 0, result.output
        sent = _api_calls(rsps)
        assert len(sent) == 1
        assert sent[0].headers[header] == "ve-42"

    def test_omitting_it_is_a_usage_error_with_no_http_call(self, fake, method, path, argv,
                                                          flag, header):
        rsps, run = fake

        result = run(argv)

        assert result.exit_code == 2
        assert f"Missing option '{flag}'" in result.output
        assert len(rsps.calls) == 0


# --- 3. Server message on errors ---------------------------------------------

VIEW = "/api/policy/v1/policy-views/00000000-0000-0000-0000-000000000000"
STATUS_LINE = f"400 Client Error: Bad Request for url: {BASE_URL}{VIEW}"


@pytest.mark.parametrize("body, shown", [
    ({"status": 400, "message": "Firewall rules can only be managed for Palo Alto vendors."},
     "Firewall rules can only be managed for Palo Alto vendors."),
    ({"errors": [{"message": "name must not be blank"}, {"message": "Unknown Match Criteria x"}]},
     "name must not be blank; Unknown Match Criteria x"),
    ({"timestamp": "t", "status": 400, "error": "Bad Request", "path": VIEW}, "Bad Request"),
    ("upstream says no\n  at line 2", "upstream says no at line 2"),
    ("x" * 1000, "x" * 300),
    ({"message": "m" * 1000}, "m" * 300),
    ({"message": "\x1b[31mred\nsecond line\x07"}, "[31mred second line"),
    ({"message": f"bad token Bearer {TOKEN}"}, "bad token Bearer ***"),
], ids=["message", "spring-errors", "error-only", "text", "long-text", "long-message",
        "control-chars", "token-masked"])
def test_server_message_reaches_stderr(fake, body, shown):
    rsps, run = fake
    kwargs = {"json": body} if isinstance(body, dict) else {"body": body}
    rsps.add(responses.GET, BASE_URL + VIEW, status=400, **kwargs)

    result = run(["policy", "read-policy-view", VIEW.rsplit("/", 1)[1]])

    assert result.exit_code == 1
    assert result.stderr.strip() == f"Error: {STATUS_LINE} — server message: {shown}"
    assert TOKEN not in result.stderr


def test_empty_error_body_keeps_the_bare_status_line(fake):
    rsps, run = fake
    rsps.add(responses.GET, BASE_URL + VIEW, status=400, body="")

    result = run(["policy", "read-policy-view", VIEW.rsplit("/", 1)[1]])

    assert result.exit_code == 1
    assert result.stderr.strip() == f"Error: {STATUS_LINE}"
