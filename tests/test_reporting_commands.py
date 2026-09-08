"""
Behavioural tests for the hand-coded `reporting` commands.

`tests/test_reporting_graphql_schema.py` proves the queries agree with the CCC
26.7 schema. These tests prove the commands still *behave* correctly around
them: what goes on the wire, and what comes back out.

Two things are load-bearing here:

1. **The 26.7 filter move.** The per-device selectors now travel inside the
   `ZeroTrustFilters` input object. A test that only checks the query string
   would not notice the CLI silently dropping the selector it was asked for, so
   the request body itself is asserted.

2. **The 26.7 coverage reshape.** `avgDeviceCoverage` / `avgPolicyCoverage` were
   deleted from `ZeroTrustMetrics`; the numbers now arrive nested under
   `policyDeploymentMetrics`. The response fixtures below are shaped the new way,
   and the command must pass the nested object through rather than flatten it
   back onto the row under the old names — flattening would assert an
   equivalence nobody has established against a live tenant.

The GraphQL responses below are shaped as the live 26.7 endpoint returns them
(`data.policyMetrics.zeroTrustMetrics[]`). No live tenant is contacted.
"""

import json

import pytest
from click.testing import CliRunner

from elisity_cli.commands import reporting
from elisity_cli.context import CliContext
from elisity_cli.main import cli

GRAPHQL_PATH = "/api/reporting/v1/data"


class FakeClient:
    """Records every call and replays canned CCC responses."""

    def __init__(self, graphql_response=None, policies=None, sites=None):
        self.graphql_response = graphql_response or {"data": {"policyMetrics": {"zeroTrustMetrics": []}}}
        self.policies = policies or []
        self.sites = sites or []
        self.posts = []
        self.gets = []

    def post(self, endpoint, data=None, params=None):
        self.posts.append({"endpoint": endpoint, "body": data})
        return self.graphql_response

    def get(self, endpoint, params=None):
        self.gets.append(endpoint)
        return self.sites

    def get_ndjson(self, endpoint, params=None):
        self.gets.append(endpoint)
        return self.policies


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def fake(monkeypatch):
    """Install a FakeClient and hand it back for assertions."""
    holder = {}

    def install(**kwargs):
        client = FakeClient(**kwargs)
        monkeypatch.setattr(CliContext, "ensure_client", lambda self: client)
        holder["client"] = client
        return client

    install.get = lambda: holder["client"]  # noqa: E731
    return install


def _zt_row(**overrides):
    """One zeroTrustMetrics row in the 26.7 response shape."""
    row = {
        "dateTime": "2026-08-05T12:00:00.000Z",
        "siteId": "site-1",
        "siteName": "Boston",
        "policyGroupId": "pg-none",
        "policyGroupName": "Unassigned",
        "policySetId": "ps-1",
        "policySetName": "Default",
        "distributionZoneId": "dz-1",
        "distributionZoneName": "DZ1",
        "deviceCount": 10,
        "totalFlows": 100,
        "restrictedFlows": 0,
        "policyDeploymentMetrics": {
            "deviceCoverage": 0.0,
            "policyDeviceCoverage": 0.0,
        },
        "l4Metrics": {"avgAllowedPorts": 12.0},
        "threatVectorMetrics": {"portExposure": [], "threatVectors": []},
    }
    row.update(overrides)
    return row


def _zt_response(rows):
    return {"data": {"policyMetrics": {"zeroTrustMetrics": rows}}}


# --------------------------------------------------------------------------
# get-zero-trust-metrics — the 26.7 filter move, asserted on the wire
# --------------------------------------------------------------------------


class TestZeroTrustRequestShape:
    def test_mac_selector_is_sent_inside_filters(self, runner, fake):
        client = fake(graphql_response=_zt_response([_zt_row()]))
        result = runner.invoke(
            cli, ["reporting", "get-zero-trust-metrics", "--mac-address", "00:11:22:33:44:55"]
        )
        assert result.exit_code == 0, result.output

        body = client.posts[0]["body"]
        assert client.posts[0]["endpoint"] == GRAPHQL_PATH
        assert body["variables"]["filters"] == {"macAddress": ["00:11:22:33:44:55"]}
        # The 26.7 breakage was a top-level `macAddress`. It must be gone from
        # both the variables and the query text.
        assert "macAddress" not in body["variables"]
        assert "macAddress: $macAddress" not in body["query"]
        assert "filters: $filters" in body["query"]

    def test_mac_selector_implies_include_mac(self, runner, fake):
        client = fake(graphql_response=_zt_response([_zt_row()]))
        runner.invoke(
            cli, ["reporting", "get-zero-trust-metrics", "--mac-address", "aa:bb:cc:dd:ee:ff"]
        )
        assert client.posts[0]["body"]["variables"]["includeMac"] is True

    def test_repeatable_mac_selector(self, runner, fake):
        client = fake(graphql_response=_zt_response([]))
        runner.invoke(
            cli,
            ["reporting", "get-zero-trust-metrics", "--mac-address", "a", "--mac-address", "b"],
        )
        assert client.posts[0]["body"]["variables"]["filters"] == {"macAddress": ["a", "b"]}

    def test_filters_omitted_when_no_selector_given(self, runner, fake):
        """An empty filters object is not the same as no filter — omit it."""
        client = fake(graphql_response=_zt_response([_zt_row()]))
        result = runner.invoke(cli, ["reporting", "get-zero-trust-metrics"])
        assert result.exit_code == 0, result.output
        assert "filters" not in client.posts[0]["body"]["variables"]

    def test_no_datetime_argument_is_sent(self, runner, fake):
        """`zeroTrustMetrics` takes no `dateTime` argument on a live tenant.

        Sending one is not ignored — the server rejects the whole query with
        `Unknown field argument 'dateTime'`. The argument is absent from the
        field's argument set entirely (live introspection: {site, filters}),
        and on the staged 26.7 capture it is a nullable LIST, so omitting it is
        valid there too. This pins the one shape both tenants accept.
        """
        client = fake(graphql_response=_zt_response([]))
        runner.invoke(cli, ["reporting", "get-zero-trust-metrics"])
        body = client.posts[0]["body"]
        assert "dateTime:" not in body["query"]
        assert "$snapshotDateTimes" not in body["query"]
        assert "snapshotDateTimes" not in body["variables"]

    def test_deprecated_snapshot_flag_warns_on_stderr_only(self, runner, fake):
        """The flag survives for compatibility but must not corrupt stdout.

        An agent piping stdout to jq would choke on a warning mixed into JSON.
        """
        fake(graphql_response=_zt_response([]))
        result = runner.invoke(
            cli,
            ["reporting", "get-zero-trust-metrics", "--snapshot", "2026-09-08T18:00:00.000Z"],
        )
        assert result.exit_code == 0, result.output
        assert json.loads(result.stdout) == []

    def test_rows_are_rendered(self, runner, fake):
        fake(graphql_response=_zt_response([_zt_row(siteName="CORK")]))
        result = runner.invoke(cli, ["reporting", "get-zero-trust-metrics"])
        assert json.loads(result.output)[0]["siteName"] == "CORK"


class TestGraphQLErrorsSurface:
    """A validation error must fail loudly, not render as an empty result.

    This is how the 26.7 breakage looked to a user: the CLI was returning the
    server's `Validation error (UnknownArgument@…)`. If that ever regresses to a
    silent empty list, a broken command looks like an empty tenant.
    """

    def test_validation_error_exits_nonzero(self, runner, fake):
        fake(
            graphql_response={
                "errors": [
                    {
                        "message": "Validation error (UnknownArgument@[policyMetrics/zeroTrustMetrics]): "
                        "Unknown field argument 'macAddress'"
                    }
                ]
            }
        )
        result = runner.invoke(cli, ["reporting", "get-zero-trust-metrics"])
        assert result.exit_code == 1
        assert "UnknownArgument" in result.output


# --------------------------------------------------------------------------
# The 26.7 coverage reshape — nested, not flattened
# --------------------------------------------------------------------------


class TestCoverageReshape:
    """`avgDeviceCoverage` / `avgPolicyCoverage` are gone from the schema."""

    def test_query_selects_the_nested_deployment_metrics(self):
        query = reporting._ZERO_TRUST_QUERY
        assert "policyDeploymentMetrics {" in query
        assert "deviceCoverage" in query
        assert "policyDeviceCoverage" in query

    @pytest.mark.parametrize("field", ["avgDeviceCoverage", "avgPolicyCoverage"])
    def test_removed_fields_are_not_selected(self, field):
        """Selecting either one is the exact FieldUndefined 26.7 returned."""
        assert field not in reporting._ZERO_TRUST_QUERY

    def test_nested_object_reaches_the_user_unflattened(self, runner, fake):
        """The row is passed through as the server shapes it.

        Flattening `policyDeploymentMetrics.deviceCoverage` back up to
        `avgDeviceCoverage` would silently tell every existing script that the
        old measurement survived under the old name. It did not: the units and
        the row grain of the new fields are unconfirmed, so the CLI reports the
        server's shape and says so in `--help`.
        """
        fake(graphql_response=_zt_response([
            _zt_row(policyDeploymentMetrics={"deviceCoverage": 41.5,
                                             "policyDeviceCoverage": 12.0}),
        ]))
        result = runner.invoke(cli, ["reporting", "get-zero-trust-metrics"])
        assert result.exit_code == 0, result.output
        row = json.loads(result.output)[0]
        assert row["policyDeploymentMetrics"] == {
            "deviceCoverage": 41.5,
            "policyDeviceCoverage": 12.0,
        }
        assert "avgDeviceCoverage" not in row
        assert "avgPolicyCoverage" not in row


class TestListSnapshots:
    """list-snapshots shares the zero-trust query, so it broke with it.

    It also swallows per-snapshot errors by design (not every hour has data) —
    which is exactly why the 26.7 validation error was invisible here: every
    probe errored and the command returned an empty list rather than failing.
    """

    def test_reports_the_one_addressable_snapshot(self, runner, fake):
        """Only the current snapshot is addressable, so exactly one row.

        Previously this walked back `--hours` hours. With no `dateTime`
        argument every probe returns identical rows, so walking back N hours
        would report the same snapshot N times and read as N distinct
        snapshots — worse than useless.
        """
        client = fake(graphql_response=_zt_response([_zt_row(), _zt_row()]))
        result = runner.invoke(cli, ["reporting", "list-snapshots", "--hours", "2"])
        assert result.exit_code == 0, result.output
        snapshots = json.loads(result.stdout)
        assert len(snapshots) == 1
        assert snapshots[0]["rows"] == 2
        assert len(client.posts) == 1, "must ask once, not once per hour"

    def test_uses_the_filters_shaped_query(self, runner, fake):
        client = fake(graphql_response=_zt_response([]))
        runner.invoke(cli, ["reporting", "list-snapshots", "--hours", "1"])
        assert "filters: $filters" in client.posts[0]["body"]["query"]

    def test_errors_now_fail_loudly(self, runner, fake):
        """The per-probe error swallow is gone, and that is the point.

        Swallowing errors is exactly why the 26.7 breakage was invisible here:
        every probe errored and the command rendered `[]`, so a dead query read
        as an empty tenant. With one request there is nothing to skip, so a
        validation error surfaces instead of being hidden.
        """
        fake(graphql_response={"errors": [{"message": "Unknown field argument"}]})
        result = runner.invoke(cli, ["reporting", "list-snapshots"])
        assert result.exit_code != 0
        assert "Unknown field argument" in result.output


class TestRemovedCommands:
    """CCC 26.7 removed the fields these commands queried."""

    @pytest.mark.parametrize(
        "command",
        [
            "get-policy-count-needed",
            "get-policy-set-enforcement-score",
            # Removed in this round: its filter was `avgDeviceCoverage <
            # threshold OR avgPolicyCoverage < threshold` and both fields are
            # gone. Neither the units nor the row grain of the replacement
            # fields can be established without a live tenant, and a mis-scaled
            # threshold makes the command recommend `policy change-status` for
            # every group in the tenant -- the precise failure it existed to
            # prevent.
            "diagnose-low-score",
        ],
    )
    def test_command_is_gone(self, runner, command):
        result = runner.invoke(cli, ["reporting", command])
        assert result.exit_code != 0
        assert "No such command" in result.output

    def test_surviving_policy_metric_commands_still_work(self, runner, fake):
        """The neighbouring policyMetrics commands were not collateral damage."""
        fake(graphql_response={"data": {"policyMetrics": {"count": [{"value": 42}]}}})
        result = runner.invoke(cli, ["reporting", "get-policy-count"])
        assert result.exit_code == 0, result.output
        assert json.loads(result.output)[0]["value"] == 42
