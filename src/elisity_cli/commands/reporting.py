"""Reporting / GraphQL — Zero Trust scores, threat vectors, risk attribution.

The CCC reporting API at ``POST /api/reporting/v1/data`` is a GraphQL endpoint.
It is **not** in the OpenAPI spec — so unlike the other command groups, these
commands are hand-coded rather than generated. They wrap the GraphQL queries
the CCC dashboard UI uses for:

- Zero Trust page — per-policy-group device & policy coverage scores, restricted
  vs total flows, L4 port exposure, MITRE-style threat vectors.
- Malware lateral movement page — same threat vector data viewed by technique.
- Per-device risk attribution — Zero Trust metrics with the device MAC included.

Snapshots are taken at top-of-hour UTC; not every hour has data. Use
``elisity reporting list-snapshots`` to find available snapshot times.
"""

import json as _json
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import click

from elisity_cli.context import pass_context
from elisity_cli.output import render

GRAPHQL_PATH = "/api/reporting/v1/data"

# Exact query the CCC dashboard sends. Preserved verbatim so the server-side
# variable-validation step accepts it (@include directives reference the
# `includeMac` and `includeL4Detail` variables — dropping them produces a
# `ValidationError: Unused variable` response).
#
# CCC 26.7: the per-device selectors (macAddress, deviceId, ipAddress, …) are no
# longer top-level arguments on `zeroTrustMetrics` — they live in the
# `ZeroTrustFilters` input object passed as `filters`. Passing `macAddress` at
# the top level is rejected at validation time:
#   Validation error (UnknownArgument@[policyMetrics/zeroTrustMetrics])
# so the argument was moved into `filters` rather than dropped. `$macAddress`
# went with it — an orphaned variable declaration would itself be a
# `ValidationError: Unused variable`.
#
# CCC 26.7, second breakage (the SELECTION SET, one layer below the arguments):
# `avgDeviceCoverage` and `avgPolicyCoverage` no longer exist on
# `ZeroTrustMetrics`:
#   Validation error (FieldUndefined@[policyMetrics/zeroTrustMetrics/avgDeviceCoverage])
#   Validation error (FieldUndefined@[policyMetrics/zeroTrustMetrics/avgPolicyCoverage])
# This is a RESHAPE, not a rename: the coverage numbers now live inside the
# nested `policyDeploymentMetrics` object, which carries six fields
# (policyDeviceCoverage, deviceCoverage, policyWorkloadCoverage,
# workloadCoverage, devicePolicyCounts, workloadPolicyCounts). The two selected
# below are the ones that answer the question this command has always asked;
# they are returned as a nested object rather than flattened onto the row,
# because flattening would assert a 1:1 equivalence with the old tenant-level
# averages that nobody has established. See README "What changed in CCC 26.7".
#
# `zeroTrustMetrics` takes no `dateTime` argument on a live tenant: it is absent
# from the field's argument set and the server rejects it outright --
#
#   Validation error (UnknownArgument@[policyMetrics/zeroTrustMetrics]):
#       Unknown field argument 'dateTime'
#
# On the staged 26.7 capture the argument DOES exist, but its type is a plain
# LIST (nullable), so it is optional there. Omitting it is therefore valid
# against both: the only shape that satisfies every tenant we can reach.
# Verified live 2026-09-08 against ot.elisity.io (30 rows) and by introspecting
# `PolicyMetrics.zeroTrustMetrics`, whose args are exactly {site, filters}.
#
# The other four `policyDeploymentMetrics` fields are deliberately NOT selected:
# the live introspection handoff carried field NAMES only, not type kinds, so we
# cannot tell a scalar from an object here, and selecting an object without a
# sub-selection fails validation for the whole query. `devicePolicyCounts` /
# `workloadPolicyCounts` read as aggregates and are the likeliest objects.
_ZERO_TRUST_QUERY = """query GetRiskAttributionScores($site: [Site!], $includeMac: Boolean!, $includeL4Detail: Boolean = false, $filters: ZeroTrustFilters) {
  policyMetrics {
    zeroTrustMetrics(
      site: $site
      filters: $filters
    ) {
      dateTime
      deviceId @include(if: $includeMac)
      macAddress @include(if: $includeMac)
      siteId
      siteName
      policyGroupId
      policyGroupName
      policySetId
      policySetName
      distributionZoneId
      distributionZoneName
      deviceCount
      totalFlows
      restrictedFlows
      policyDeploymentMetrics {
        deviceCoverage
        policyDeviceCoverage
        __typename
      }
      l4Metrics {
        avgAllowedPorts
        avgAllowedTcp @include(if: $includeL4Detail)
        avgAllowedUdp @include(if: $includeL4Detail)
        avgIcmp @include(if: $includeL4Detail)
        __typename
      }
      threatVectorMetrics {
        ...ThreatVectorMetricsFields
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment PortExposureMetricFields on PortExposureMetricValue {
  port
  value
  __typename
}

fragment ThreatVectorMetricFields on ThreatVectorMetricValue {
  technique
  value
  __typename
}

fragment ThreatVectorMetricsFields on ThreatVectorMetrics {
  portExposure {
    ...PortExposureMetricFields
    __typename
  }
  threatVectors {
    ...ThreatVectorMetricFields
    __typename
  }
  __typename
}"""


@click.group("reporting")
def group():
    """CCC reporting (GraphQL) — Zero Trust scores, threat vectors, risk attribution.

    These commands query the /api/reporting/v1/data GraphQL endpoint that powers
    the CCC dashboard Zero Trust page, the malware lateral movement page, and
    per-device risk views. The endpoint is not in the OpenAPI spec, so these
    commands are hand-coded.
    """


def _post_graphql(ctx, operation_name: str, variables: dict, query: str):
    client = ctx.ensure_client()
    body = {
        "operationName": operation_name,
        "variables": variables,
        "query": query,
    }
    return client.post(GRAPHQL_PATH, data=body)


def _default_snapshot() -> str:
    """Top-of-hour timestamp for the previous full hour (UTC)."""
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    return (now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S.000Z")


# Keys of the CCC 26.7 `ZeroTrustFilters` input object. Every one of these was a
# top-level argument on `zeroTrustMetrics` before 26.7. Kept as an explicit tuple
# so a typo'd key is caught here rather than by the server.
_ZERO_TRUST_FILTER_KEYS = (
    "ipAddress",
    "macAddress",
    "deviceId",
    "siteId",
    "policySetId",
    "policyGroupId",
    "distributionZoneId",
)


def _zero_trust_filters(**selectors) -> Optional[dict]:
    """Build the ``ZeroTrustFilters`` value from the selectors a command exposes.

    Returns ``None`` when nothing was selected, so the variable is omitted
    entirely rather than sent as an empty object.
    """
    unknown = sorted(set(selectors) - set(_ZERO_TRUST_FILTER_KEYS))
    if unknown:
        raise ValueError(
            f"not ZeroTrustFilters keys: {unknown} "
            f"(valid: {list(_ZERO_TRUST_FILTER_KEYS)})"
        )
    filters = {key: list(value) for key, value in selectors.items() if value}
    return filters or None


def _check_errors(result) -> None:
    """Raise on GraphQL-level errors."""
    if isinstance(result, dict) and result.get("errors"):
        click.echo("GraphQL errors:", err=True)
        for e in result["errors"]:
            click.echo(f"  - {e.get('message', e)}", err=True)
        raise SystemExit(1)


def _lookup_sites(ctx, site_names: List[str]) -> List[dict]:
    """Resolve site names to the Site input objects the GraphQL endpoint requires.

    The reporting endpoint's ``Site`` input type is a Map with three non-null
    fields: ``id`` (UUID), ``numericId`` (Long), ``label`` (String). Users
    pass site names on the CLI; we look them up against
    ``GET /api/topology/v2/sites`` and build the input objects.
    """
    client = ctx.ensure_client()
    sites = client.get("/api/topology/v2/sites") or []
    if isinstance(sites, dict):
        sites = sites.get("content") or sites.get("items") or []
    by_label = {s.get("label"): s for s in sites if isinstance(s, dict)}

    out: List[dict] = []
    missing: List[str] = []
    for name in site_names:
        s = by_label.get(name)
        if not s:
            missing.append(name)
            continue
        out.append(
            {
                "id": s.get("id"),
                "numericId": int(s.get("numericId")) if s.get("numericId") is not None else 0,
                "label": s.get("label"),
            }
        )
    if missing:
        available = sorted(by_label.keys())
        click.echo(
            f"Unknown site name(s): {missing}. Available: {available}", err=True
        )
        raise SystemExit(1)
    return out


@group.command("get-zero-trust-metrics")
@click.option(
    "--snapshot",
    "snapshots",
    multiple=True,
    default=None,
    help="DEPRECATED and ignored: zeroTrustMetrics takes no dateTime argument; "
    "the endpoint serves the current snapshot only.",
)
@click.option(
    "--site",
    "sites",
    multiple=True,
    default=None,
    help="Filter to one or more site names (server-side filter). Repeatable. "
    "Use the site label as shown by `elisity topology get-all-sites`. "
    "Alternative: omit and post-filter with `-q \"[?siteName=='Boston']\"`.",
)
@click.option(
    "--mac-address",
    "mac_addresses",
    multiple=True,
    default=None,
    help="Filter to one or more device MAC addresses (server-side filter, "
    "CCC 26.7 `ZeroTrustFilters.macAddress`). Repeatable. Implies --include-mac "
    "so the filtered rows carry the MAC they matched on.",
)
@click.option(
    "--include-mac",
    is_flag=True,
    default=False,
    help="Include per-device deviceId + macAddress in results.",
)
@click.option(
    "--include-l4-detail",
    is_flag=True,
    default=False,
    help="Include TCP/UDP/ICMP breakdown in l4Metrics.",
)
@pass_context
def cmd_zero_trust(
    ctx,
    snapshots,
    sites,
    mac_addresses,
    include_mac,
    include_l4_detail,
):
    """Get Zero Trust scores (the metrics from CCC's Zero Trust page).

    Returns the rows CCC's `zeroTrustMetrics` serves for the snapshot, each
    carrying deviceCount, totalFlows, restrictedFlows, the site / policy-set /
    policy-group / distribution-zone identifiers, L4 port exposure and
    threat-vector metrics (MITRE techniques + port exposure scores), plus a
    nested `policyDeploymentMetrics` object holding `deviceCoverage` and
    `policyDeviceCoverage`.

    CHANGED IN CCC 26.7 — read this before reusing a 26.3 script or query.
    The flat `avgDeviceCoverage` / `avgPolicyCoverage` fields are gone from the
    schema; the coverage numbers now arrive nested under
    `policyDeploymentMetrics`. That is a reshape, not a rename: the fields are
    not documented as the same measurement, so this command reports the
    server's shape verbatim rather than flattening them back onto the row under
    the old names. Any JMESPath/jq expression that referenced `avgDeviceCoverage`
    must be repointed at `policyDeploymentMetrics.deviceCoverage`, and any
    threshold written against the old 0–100 scale must be re-checked against
    real output before it is trusted — the units of the new fields have not
    been confirmed against a live tenant.

    IMPORTANT — a low score does NOT tell you *why* it is low. A 0% coverage
    row can mean the group has no policy, has only simulation (MONITOR_ONLY)
    policies, or has active policies that don't cover its real traffic — three
    causes with different fixes. Do not assume "simulation" and recommend
    `policy change-status` from this command's output. To tell them apart, list
    the group's policies and look at their `monitorMode`:

      elisity -q '[?srcId==`<policyGroupId>` || dstId==`<policyGroupId>`].{name: name, mode: monitorMode, disabled: disabled}' \\
        -f table policy get-all-policies-as-nd-json

    (`reporting diagnose-low-score` used to do that join automatically. It was
    removed in the 26.7 update — see README "What changed in CCC 26.7".)

    Examples (note: -q / -f are top-level flags — place them BEFORE the
    group name):

      elisity reporting get-zero-trust-metrics
      elisity reporting get-zero-trust-metrics --snapshot 2026-05-22T11:00:00.000Z
      elisity reporting get-zero-trust-metrics --site Boston --site CORK
      elisity reporting get-zero-trust-metrics --include-l4-detail
      elisity reporting get-zero-trust-metrics --mac-address 00:11:22:33:44:55

      # Coverage per row
      elisity -q '[].{site: siteName, pg: policyGroupName, devices: deviceCount, devCov: policyDeploymentMetrics.deviceCoverage, polDevCov: policyDeploymentMetrics.policyDeviceCoverage}' \\
        -f table reporting get-zero-trust-metrics

      # Tenant total device count covered by the snapshot
      elisity -q 'sum([].deviceCount)' reporting get-zero-trust-metrics

      # Device-weighted average coverage via jq (JMESPath lacks generic
      # arithmetic; null-safe with `// 0`)
      elisity reporting get-zero-trust-metrics | jq '
        (map((.policyDeploymentMetrics.deviceCoverage // 0) * .deviceCount) | add) /
        (map(.deviceCount) | add)
      '
    """
    if snapshots:
        click.echo(
            "warning: --snapshot is ignored — zeroTrustMetrics takes no dateTime "
            "argument; the endpoint serves the current snapshot only.",
            err=True,
        )
    variables = {
        # A MAC filter with no MAC in the rows is useless output — imply the flag.
        "includeMac": include_mac or bool(mac_addresses),
        "includeL4Detail": include_l4_detail,
    }
    if sites:
        variables["site"] = _lookup_sites(ctx, list(sites))
    filters = _zero_trust_filters(macAddress=mac_addresses)
    if filters:
        variables["filters"] = filters

    result = _post_graphql(ctx, "GetRiskAttributionScores", variables, _ZERO_TRUST_QUERY)
    _check_errors(result)

    metrics = (
        result.get("data", {}).get("policyMetrics", {}).get("zeroTrustMetrics") or []
    )
    render(metrics, ctx.format, ctx.query)


# ---------------------------------------------------------------------------
# REMOVED IN CCC 26.7: `diagnose-low-score`
#
# The command joined the Zero Trust coverage metric with each policy group's
# actual policy status so a low/zero score could be attributed to the right
# cause (NO_POLICY / SIMULATION_ONLY / EXTERNAL_ONLY / MIXED_LOW_COVERAGE /
# ACTIVE_LOW_COVERAGE) instead of being blamed on "simulation" by default.
#
# Its filter was `avgDeviceCoverage < threshold OR avgPolicyCoverage <
# threshold`, and BOTH of those fields were deleted from `ZeroTrustMetrics` in
# 26.7. The coverage numbers moved into the nested `policyDeploymentMetrics`
# object, which is a reshape rather than a rename — two things about the new
# shape are unknown from a static handoff and neither can be guessed safely:
#
#   1. Units. `--threshold` is documented and defaulted as a PERCENTAGE (50.0,
#      "use 100 to classify every group"). If `deviceCoverage` is a 0.0–1.0
#      fraction rather than 0–100, every row falls under the default threshold
#      and the command confidently reports the entire tenant as low-coverage.
#   2. Grain. 26.7 serves per-device rows; the diagnosis is per policy group.
#      Collapsing rows to a group verdict needs an aggregation (plain mean vs
#      device-weighted mean vs worst-case) that changes which groups are
#      flagged, and no source states which one CCC's own UI uses.
#
# Shipping a guess here is worse than shipping nothing: the whole point of the
# command was to stop an agent recommending `policy change-status` on a group
# that has no policy at all, and a mis-scaled threshold makes it recommend that
# for every group in the tenant. Removed on the same rule that removed
# `get-policy-count-needed` and `get-policy-set-enforcement-score` — a
# plausible-but-wrong number is worse than an absent command.
#
# To restore it, someone with live 26.7 tenant access must establish (a) the
# range of `policyDeploymentMetrics.deviceCoverage` on real rows and (b) the
# row grain actually returned for a policy group; the classification logic
# itself (policy-stream tally -> NO_POLICY / SIMULATION_ONLY / ... ) was
# correct and is preserved in git history at commit d212e72.
#
# The manual equivalent is in `get-zero-trust-metrics`'s help text: take a
# low-scoring row's policyGroupId and inspect the monitorMode of the policies
# that reference it via `policy get-all-policies-as-nd-json`.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Additional metric queries discovered via GraphQL introspection of
# /api/reporting/v1/data. The reporting endpoint exposes 4 metric domains
# (policyMetrics, identityGraphMetrics, trafficVectorsMetrics, topologyMetrics)
# — these commands wrap the most operationally useful queries for tenant
# summary, posture scoring, and per-site dashboards.
# ---------------------------------------------------------------------------


_AGGREGATE_SCORE_QUERY = """query AggregateEnforcementScore($dt: [DateTime!]!, $site: [Site!]) {
  policyMetrics {
    aggregatePolicyEnforcementScore(dateTime: $dt, site: $site) {
      ... on FloatMetricValue {
        value
        dateTime
        __typename
      }
    }
  }
}"""

# NOTE (CCC 26.7): `policyMetrics.policySetEnforcementScore` was REMOVED from the
# schema — the query that backed `reporting get-policy-set-enforcement-score`
# now fails with FieldUndefined. The command was removed rather than rewritten:
# no 26.7 field answers "enforcement score for this one policy set", and
# `coverage(policySetId: …)` is a coverage measure, not that score. See README
# "What changed in CCC 26.7".

_DEVICE_COUNT_QUERY = """query DeviceCount($dt: DateTimeSelectionInput!, $online: Boolean, $site: [Site!]) {
  identityGraphMetrics {
    devices {
      count(dateTime: $dt, online: $online, site: $site) {
        dateTime
        online
        value
      }
    }
  }
}"""

_SITE_KPIS_QUERY = """query SiteKPIs($dt: DateTime!, $site: [Site!]) {
  topologyMetrics {
    siteKPIs(dateTime: $dt, site: $site) {
      dateTime
      siteName
      onlineDevices
      virtualEdgeNodes
      localPolicyGroups
      simulatedPolicies
      activatedPolicies
      policyEnforcementScore
    }
  }
}"""


@group.command("get-aggregate-enforcement-score")
@click.option(
    "--snapshot",
    "snapshots",
    multiple=True,
    default=None,
    help="ISO-8601 snapshot time (top-of-hour UTC). Repeatable. Default: previous full hour.",
)
@click.option(
    "--site",
    "sites",
    multiple=True,
    default=None,
    help="Filter to one or more site names. Repeatable.",
)
@pass_context
def cmd_aggregate_score(ctx, snapshots, sites):
    """Tenant-wide Zero Trust enforcement score (single number per snapshot).

    This is the actual "Zero Trust score" headline number that the CCC UI
    shows. Returns a list of FloatMetricValue, one per requested snapshot
    (most users want a single recent snapshot — that's the default).

    Examples:
      elisity reporting get-aggregate-enforcement-score
      elisity reporting get-aggregate-enforcement-score --snapshot 2026-05-22T11:00:00.000Z
      elisity reporting get-aggregate-enforcement-score --site Boston --site CORK
    """
    snaps = list(snapshots) if snapshots else [_default_snapshot()]
    variables = {"dt": snaps}
    if sites:
        variables["site"] = _lookup_sites(ctx, list(sites))

    result = _post_graphql(ctx, "AggregateEnforcementScore", variables, _AGGREGATE_SCORE_QUERY)
    _check_errors(result)
    data = (
        result.get("data", {}).get("policyMetrics", {}).get("aggregatePolicyEnforcementScore")
        or []
    )
    render(data, ctx.format, ctx.query)


@group.command("get-device-count")
@click.option(
    "--snapshot",
    "snapshots",
    multiple=True,
    default=None,
    help="ISO-8601 snapshot time (top-of-hour UTC). Repeatable. Default: previous full hour.",
)
@click.option(
    "--online",
    type=click.Choice(["true", "false"]),
    default=None,
    help="Filter to online=true or online=false only. Omit to get both as separate rows.",
)
@click.option(
    "--site",
    "sites",
    multiple=True,
    default=None,
    help="Filter to one or more site names. Repeatable.",
)
@pass_context
def cmd_device_count(ctx, snapshots, online, sites):
    """Device count from CCC's metrics snapshot — broken out by online state.

    Returns one row per (snapshot, online-state). With no --online filter,
    you get two rows per snapshot (online=true, online=false) — useful for
    tenant-wide online/offline counts in a single call without paginating
    through devices/view.

    Examples:
      # Online + offline counts for the latest snapshot
      elisity reporting get-device-count

      # Just online devices
      elisity reporting get-device-count --online true

      # Per site
      elisity reporting get-device-count --site Boston
      elisity reporting get-device-count --site Boston --site CORK
    """
    snaps = list(snapshots) if snapshots else [_default_snapshot()]
    variables = {"dt": {"dateTimes": snaps}}
    if online is not None:
        variables["online"] = (online == "true")
    if sites:
        variables["site"] = _lookup_sites(ctx, list(sites))

    result = _post_graphql(ctx, "DeviceCount", variables, _DEVICE_COUNT_QUERY)
    _check_errors(result)
    data = (
        result.get("data", {}).get("identityGraphMetrics", {}).get("devices", {}).get("count")
        or []
    )
    render(data, ctx.format, ctx.query)


@group.command("get-site-kpis")
@click.option(
    "--snapshot",
    "snapshot",
    default=None,
    help="ISO-8601 snapshot time (top-of-hour UTC). Default: previous full hour.",
)
@click.option(
    "--site",
    "sites",
    multiple=True,
    default=None,
    help="Filter to one or more site names. Repeatable.",
)
@pass_context
def cmd_site_kpis(ctx, snapshot, sites):
    """Per-site KPI dashboard — devices, VENs, policy counts, enforcement score.

    Returns one row per site with: onlineDevices, virtualEdgeNodes,
    localPolicyGroups, simulatedPolicies, activatedPolicies,
    policyEnforcementScore. This is the data behind CCC's per-site
    dashboard cards — the single best query for a tenant summary.

    Examples:
      elisity -f table reporting get-site-kpis
      elisity reporting get-site-kpis --site Boston
    """
    snap = snapshot or _default_snapshot()
    variables = {"dt": snap}
    if sites:
        variables["site"] = _lookup_sites(ctx, list(sites))

    result = _post_graphql(ctx, "SiteKPIs", variables, _SITE_KPIS_QUERY)
    _check_errors(result)
    data = result.get("data", {}).get("topologyMetrics", {}).get("siteKPIs") or []
    render(data, ctx.format, ctx.query)


# ---------------------------------------------------------------------------
# Additional GraphQL queries — round 2. Wraps every remaining /reporting/v1/data
# query the CCC dashboard uses, derived via Apollo-style introspection.
# ---------------------------------------------------------------------------

_POLICY_COUNT_QUERY = """query PolicyCount($dt: DateTimeSelectionInput!, $monitorMode: MonitorMode, $site: [Site!]) {
  policyMetrics {
    count(dateTime: $dt, monitorMode: $monitorMode, site: $site) {
      dateTime
      monitorMode
      value
    }
  }
}"""

# NOTE (CCC 26.7): `policyMetrics.countNeeded` was REMOVED from the schema —
# the query that backed `reporting get-policy-count-needed` now fails with
# FieldUndefined. The command was removed rather than rewritten onto
# `coverage`: coverage answers "how covered are the groups I have", not "how
# many more policies are needed", and a plausible-but-wrong number is worse
# than an absent command. See README "What changed in CCC 26.7".

_POLICY_GROUPS_COUNT_QUERY = """query PolicyGroupsCount($dt: [DateTime!]!, $local: Boolean, $site: [Site!]) {
  policyMetrics {
    policyGroups {
      count(dateTime: $dt, local: $local, site: $site) {
        dateTime
        value
      }
    }
  }
}"""

_DEVICES_BY_CONNECTOR_QUERY = """query DevicesByConnector($dt: DateTime!, $site: [Site!]) {
  identityGraphMetrics {
    devices {
      countByConnector(dateTime: $dt, site: $site) {
        connector
        connectorName
        value
      }
    }
  }
}"""

_ACTIVE_SITES_COUNT_QUERY = """query ActiveSitesCount($dt: [DateTime!]!, $site: [Site!]) {
  topologyMetrics {
    activeSites {
      count(dateTime: $dt, site: $site) {
        dateTime
        value
      }
    }
  }
}"""

_ACTIVE_SITES_WAP_COUNT_QUERY = """query ActiveSitesWithActivatedPoliciesCount($dt: [DateTime!]!, $site: [Site!]) {
  topologyMetrics {
    activeSitesWithActivatedPolicies {
      count(dateTime: $dt, site: $site) {
        dateTime
        value
      }
    }
  }
}"""

_VIRTUAL_EDGES_COUNT_QUERY = """query VirtualEdgesCount($dt: DateTimeSelectionInput!, $site: [Site!]) {
  topologyMetrics {
    virtualEdges {
      count(dateTime: $dt, site: $site) {
        dateTime
        value
      }
    }
  }
}"""

_VIRTUAL_EDGE_NODES_COUNT_QUERY = """query VirtualEdgeNodesCount($dt: DateTimeSelectionInput!, $model: [String!], $site: [Site!]) {
  topologyMetrics {
    virtualEdgeNodes {
      count(dateTime: $dt, model: $model, site: $site) {
        dateTime
        model
        type
        value
      }
    }
  }
}"""

_TARGET_SITES_QUERY = """query TargetSites($dt: DateTime!) {
  topologyMetrics {
    targetSites(dateTime: $dt) {
      type
      value
      startDate
      endDate
    }
  }
}"""

_TRAFFIC_VECTORS_COUNT_QUERY = """query TrafficVectorsCount($dt: DateTimeWindow!, $kind: TrafficVectorKind!, $policyStatus: PolicyStatus, $site: [Site!]) {
  trafficVectorsMetrics {
    count(dateTime: $dt, kind: $kind, policyStatus: $policyStatus, site: $site) {
      fromDateTime
      toDateTime
      value
    }
  }
}"""

_TRAFFIC_VECTORS_BY_PG_QUERY = """query TrafficVectorsByPG($dt: DateTimeWindow!, $kind: TrafficVectorKind!, $top: Int!, $site: [Site!]) {
  trafficVectorsMetrics {
    countByPG(dateTime: $dt, kind: $kind, top: $top, site: $site) {
      pgNumericId
      pgDisplayName
      kind
      value
    }
  }
}"""

_TRAFFIC_VECTORS_BY_IP_QUERY = """query TrafficVectorsByIP($dt: DateTimeWindow!, $kind: TrafficVectorKind!, $top: Int!, $site: [Site!]) {
  trafficVectorsMetrics {
    countByIP(dateTime: $dt, kind: $kind, top: $top, site: $site) {
      ip
      kind
      value
    }
  }
}"""


def _maybe_sites(ctx, sites_arg):
    """Return the resolved [Site!] list or None to omit the variable."""
    return _lookup_sites(ctx, list(sites_arg)) if sites_arg else None


def _default_window(hours_back: int = 24, step_hours: int = 1) -> dict:
    """A DateTimeWindow covering the last <hours_back> hours."""
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    return {
        "fromDateTime": (now - timedelta(hours=hours_back)).strftime(
            "%Y-%m-%dT%H:%M:%S.000Z"
        ),
        "toDateTime": now.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "stepHours": step_hours,
    }


# --- Policy metric counts -------------------------------------------------


@group.command("get-policy-count")
@click.option("--snapshot", "snapshots", multiple=True, default=None,
              help="ISO-8601 snapshot time. Repeatable. Default: previous full hour.")
@click.option("--monitor-mode",
              type=click.Choice(["MONITOR_ONLY", "MONITOR_AND_ENFORCE", "MONITOR_EXTERNAL"]),
              default=None, help="Optional MonitorMode filter.")
@click.option("--site", "sites", multiple=True, default=None,
              help="Filter to one or more site names. Repeatable.")
@pass_context
def cmd_policy_count(ctx, snapshots, monitor_mode, sites):
    """Policy counts by MonitorMode for a snapshot.

    Returns rows of {dateTime, monitorMode, value}.
    """
    snaps = list(snapshots) if snapshots else [_default_snapshot()]
    variables = {"dt": {"dateTimes": snaps}}
    if monitor_mode:
        variables["monitorMode"] = monitor_mode
    sl = _maybe_sites(ctx, sites)
    if sl is not None:
        variables["site"] = sl
    result = _post_graphql(ctx, "PolicyCount", variables, _POLICY_COUNT_QUERY)
    _check_errors(result)
    render(result.get("data", {}).get("policyMetrics", {}).get("count") or [],
           ctx.format, ctx.query)


@group.command("get-policy-groups-count")
@click.option("--snapshot", "snapshots", multiple=True, default=None,
              help="ISO-8601 snapshot time. Repeatable. Default: previous full hour.")
@click.option("--local/--no-local", "local", default=None,
              help="Filter to local=true or local=false policy groups only.")
@click.option("--site", "sites", multiple=True, default=None,
              help="Filter to one or more site names. Repeatable.")
@pass_context
def cmd_policy_groups_count(ctx, snapshots, local, sites):
    """Policy group counts, optionally filtered by local vs global."""
    snaps = list(snapshots) if snapshots else [_default_snapshot()]
    variables = {"dt": snaps}
    if local is not None:
        variables["local"] = bool(local)
    sl = _maybe_sites(ctx, sites)
    if sl is not None:
        variables["site"] = sl
    result = _post_graphql(ctx, "PolicyGroupsCount", variables, _POLICY_GROUPS_COUNT_QUERY)
    _check_errors(result)
    render(result.get("data", {}).get("policyMetrics", {}).get("policyGroups", {}).get("count") or [],
           ctx.format, ctx.query)


# --- Identity graph (devices) ---------------------------------------------


@group.command("get-devices-by-connector")
@click.option("--snapshot", default=None,
              help="ISO-8601 snapshot time. Default: previous full hour. Only one allowed.")
@click.option("--site", "sites", multiple=True, default=None,
              help="Filter to one or more site names. Repeatable.")
@pass_context
def cmd_devices_by_connector(ctx, snapshot, sites):
    """Device counts grouped by connector.

    Returns one row per connector with {connector, connectorName, value}.
    Useful for answering "which connector contributes the most devices?".
    """
    snap = snapshot or _default_snapshot()
    variables = {"dt": snap}
    sl = _maybe_sites(ctx, sites)
    if sl is not None:
        variables["site"] = sl
    result = _post_graphql(ctx, "DevicesByConnector", variables, _DEVICES_BY_CONNECTOR_QUERY)
    _check_errors(result)
    render(result.get("data", {}).get("identityGraphMetrics", {}).get("devices", {}).get("countByConnector") or [],
           ctx.format, ctx.query)


# --- Topology counts ------------------------------------------------------


@group.command("get-active-sites-count")
@click.option("--snapshot", "snapshots", multiple=True, default=None,
              help="ISO-8601 snapshot time. Repeatable. Default: previous full hour.")
@click.option("--site", "sites", multiple=True, default=None,
              help="Filter to one or more site names. Repeatable.")
@pass_context
def cmd_active_sites_count(ctx, snapshots, sites):
    """Count of active sites at the given snapshots."""
    snaps = list(snapshots) if snapshots else [_default_snapshot()]
    variables = {"dt": snaps}
    sl = _maybe_sites(ctx, sites)
    if sl is not None:
        variables["site"] = sl
    result = _post_graphql(ctx, "ActiveSitesCount", variables, _ACTIVE_SITES_COUNT_QUERY)
    _check_errors(result)
    render(result.get("data", {}).get("topologyMetrics", {}).get("activeSites", {}).get("count") or [],
           ctx.format, ctx.query)


@group.command("get-active-sites-with-activated-policies-count")
@click.option("--snapshot", "snapshots", multiple=True, default=None,
              help="ISO-8601 snapshot time. Repeatable. Default: previous full hour.")
@click.option("--site", "sites", multiple=True, default=None,
              help="Filter to one or more site names. Repeatable.")
@pass_context
def cmd_active_sites_wap_count(ctx, snapshots, sites):
    """Count of sites with activated policies at the given snapshots.

    Difference vs `get-active-sites-count`: this only counts sites that
    have at least one activated policy.
    """
    snaps = list(snapshots) if snapshots else [_default_snapshot()]
    variables = {"dt": snaps}
    sl = _maybe_sites(ctx, sites)
    if sl is not None:
        variables["site"] = sl
    result = _post_graphql(ctx, "ActiveSitesWithActivatedPoliciesCount", variables,
                           _ACTIVE_SITES_WAP_COUNT_QUERY)
    _check_errors(result)
    render(result.get("data", {}).get("topologyMetrics", {})
                  .get("activeSitesWithActivatedPolicies", {}).get("count") or [],
           ctx.format, ctx.query)


@group.command("get-virtual-edges-count")
@click.option("--snapshot", "snapshots", multiple=True, default=None,
              help="ISO-8601 snapshot time. Repeatable. Default: previous full hour.")
@click.option("--site", "sites", multiple=True, default=None,
              help="Filter to one or more site names. Repeatable.")
@pass_context
def cmd_virtual_edges_count(ctx, snapshots, sites):
    """Virtual Edge counts at the given snapshots."""
    snaps = list(snapshots) if snapshots else [_default_snapshot()]
    variables = {"dt": {"dateTimes": snaps}}
    sl = _maybe_sites(ctx, sites)
    if sl is not None:
        variables["site"] = sl
    result = _post_graphql(ctx, "VirtualEdgesCount", variables, _VIRTUAL_EDGES_COUNT_QUERY)
    _check_errors(result)
    render(result.get("data", {}).get("topologyMetrics", {}).get("virtualEdges", {}).get("count") or [],
           ctx.format, ctx.query)


@group.command("get-virtual-edge-nodes-count")
@click.option("--snapshot", "snapshots", multiple=True, default=None,
              help="ISO-8601 snapshot time. Repeatable. Default: previous full hour.")
@click.option("--model", "models", multiple=True, default=None,
              help="Filter to specific VEN model string(s), e.g. 'C9300-48T'. Repeatable.")
@click.option("--site", "sites", multiple=True, default=None,
              help="Filter to one or more site names. Repeatable.")
@pass_context
def cmd_virtual_edge_nodes_count(ctx, snapshots, models, sites):
    """Virtual Edge Node counts at the given snapshots.

    Returns rows with {dateTime, model, type, value} — group by model in
    the result to answer "VENs per vendor/model".

    Examples:
      elisity -f table reporting get-virtual-edge-nodes-count
      elisity reporting get-virtual-edge-nodes-count --model C9300-48T
      elisity reporting get-virtual-edge-nodes-count --model C9300-48T --model C9300-24T
    """
    snaps = list(snapshots) if snapshots else [_default_snapshot()]
    variables = {"dt": {"dateTimes": snaps}}
    if models:
        variables["model"] = list(models)
    sl = _maybe_sites(ctx, sites)
    if sl is not None:
        variables["site"] = sl
    result = _post_graphql(ctx, "VirtualEdgeNodesCount", variables, _VIRTUAL_EDGE_NODES_COUNT_QUERY)
    _check_errors(result)
    render(result.get("data", {}).get("topologyMetrics", {}).get("virtualEdgeNodes", {}).get("count") or [],
           ctx.format, ctx.query)


@group.command("get-target-sites")
@click.option("--snapshot", default=None,
              help="ISO-8601 snapshot time. Default: previous full hour.")
@pass_context
def cmd_target_sites(ctx, snapshot):
    """Target-sites data (site activation targets).

    Returns rows of {type, value, startDate, endDate}. NOTE: this endpoint
    has been observed to return `INTERNAL_ERROR` on tenants without
    target-site configuration — that's a CCC-side condition, not a CLI bug.
    """
    snap = snapshot or _default_snapshot()
    variables = {"dt": snap}
    result = _post_graphql(ctx, "TargetSites", variables, _TARGET_SITES_QUERY)
    _check_errors(result)
    render(result.get("data", {}).get("topologyMetrics", {}).get("targetSites") or [],
           ctx.format, ctx.query)


# --- Traffic vectors ------------------------------------------------------


@group.command("get-traffic-count")
@click.option("--kind", type=click.Choice(["ALL", "ALLOWED", "DENIED"]), default="ALL",
              help="Traffic vector kind (default ALL).")
@click.option("--policy-status",
              type=click.Choice(["ACTIVE", "SIMULATION", "NO_POLICY"]), default=None,
              help="Optional PolicyStatus filter.")
@click.option("--from-time", "from_time", default=None,
              help="ISO-8601 start (UTC). Default: 24h ago top-of-hour.")
@click.option("--to-time", "to_time", default=None,
              help="ISO-8601 end (UTC). Default: now top-of-hour.")
@click.option("--step-hours", type=int, default=1,
              help="Window step in hours (default 1).")
@click.option("--site", "sites", multiple=True, default=None,
              help="Filter to one or more site names. Repeatable.")
@pass_context
def cmd_traffic_count(ctx, kind, policy_status, from_time, to_time, step_hours, sites):
    """Total traffic vector count over a time window.

    Default window is the last 24 hours. Returns a single MetricWindow
    object (not a list) — fromDateTime, toDateTime, value.

    Examples:
      elisity reporting get-traffic-count --kind DENIED
      elisity reporting get-traffic-count --kind ALL --site CORK
    """
    if from_time or to_time:
        window = _default_window()
        if from_time: window["fromDateTime"] = from_time
        if to_time:   window["toDateTime"] = to_time
        window["stepHours"] = step_hours
    else:
        window = _default_window(step_hours=step_hours)

    variables = {"dt": window, "kind": kind}
    if policy_status:
        variables["policyStatus"] = policy_status
    sl = _maybe_sites(ctx, sites)
    if sl is not None:
        variables["site"] = sl

    result = _post_graphql(ctx, "TrafficVectorsCount", variables, _TRAFFIC_VECTORS_COUNT_QUERY)
    _check_errors(result)
    render(result.get("data", {}).get("trafficVectorsMetrics", {}).get("count") or {},
           ctx.format, ctx.query)


@group.command("get-top-policy-groups-by-traffic")
@click.option("--kind", type=click.Choice(["ALL", "ALLOWED", "DENIED"]), default="ALL",
              help="Traffic vector kind (default ALL).")
@click.option("--top", type=int, default=10,
              help="How many top policy groups to return (default 10).")
@click.option("--from-time", "from_time", default=None,
              help="ISO-8601 start (UTC). Default: 24h ago top-of-hour.")
@click.option("--to-time", "to_time", default=None,
              help="ISO-8601 end (UTC). Default: now top-of-hour.")
@click.option("--step-hours", type=int, default=1,
              help="Window step in hours (default 1).")
@click.option("--site", "sites", multiple=True, default=None,
              help="Filter to one or more site names. Repeatable.")
@pass_context
def cmd_top_pgs(ctx, kind, top, from_time, to_time, step_hours, sites):
    """Top N policy groups by traffic-vector count over a time window.

    Returns rows of {pgNumericId, pgDisplayName, kind, value}.

    Example:
      elisity -f table reporting get-top-policy-groups-by-traffic --kind DENIED --top 5
    """
    window = _default_window(step_hours=step_hours)
    if from_time: window["fromDateTime"] = from_time
    if to_time:   window["toDateTime"] = to_time

    variables = {"dt": window, "kind": kind, "top": top}
    sl = _maybe_sites(ctx, sites)
    if sl is not None:
        variables["site"] = sl

    result = _post_graphql(ctx, "TrafficVectorsByPG", variables, _TRAFFIC_VECTORS_BY_PG_QUERY)
    _check_errors(result)
    render(result.get("data", {}).get("trafficVectorsMetrics", {}).get("countByPG") or [],
           ctx.format, ctx.query)


@group.command("get-top-ips-by-traffic")
@click.option("--kind", type=click.Choice(["ALL", "ALLOWED", "DENIED"]), default="ALL",
              help="Traffic vector kind (default ALL).")
@click.option("--top", type=int, default=10,
              help="How many top IPs to return (default 10).")
@click.option("--from-time", "from_time", default=None,
              help="ISO-8601 start (UTC). Default: 24h ago top-of-hour.")
@click.option("--to-time", "to_time", default=None,
              help="ISO-8601 end (UTC). Default: now top-of-hour.")
@click.option("--step-hours", type=int, default=1,
              help="Window step in hours (default 1).")
@click.option("--site", "sites", multiple=True, default=None,
              help="Filter to one or more site names. Repeatable.")
@pass_context
def cmd_top_ips(ctx, kind, top, from_time, to_time, step_hours, sites):
    """Top N IPs by traffic-vector count over a time window.

    Returns rows of {ip, kind, value}.

    Example:
      elisity -f table reporting get-top-ips-by-traffic --kind DENIED --top 10
    """
    window = _default_window(step_hours=step_hours)
    if from_time: window["fromDateTime"] = from_time
    if to_time:   window["toDateTime"] = to_time

    variables = {"dt": window, "kind": kind, "top": top}
    sl = _maybe_sites(ctx, sites)
    if sl is not None:
        variables["site"] = sl

    result = _post_graphql(ctx, "TrafficVectorsByIP", variables, _TRAFFIC_VECTORS_BY_IP_QUERY)
    _check_errors(result)
    render(result.get("data", {}).get("trafficVectorsMetrics", {}).get("countByIP") or [],
           ctx.format, ctx.query)


@group.command("list-snapshots")
@click.option(
    "--hours",
    type=int,
    default=None,
    help="DEPRECATED and ignored: only the current snapshot is addressable.",
)
@pass_context
def cmd_list_snapshots(ctx, hours):
    """Discover which top-of-hour snapshots have data on this tenant.

    /api/reporting/v1/data serves point-in-time snapshots. Not every hour has
    data. `zeroTrustMetrics` takes no `dateTime` argument on a live tenant, so
    only the current snapshot is addressable: this reports that snapshot's
    server-side dateTime and its row count. `--hours` is accepted but ignored.

    Example:
      elisity reporting list-snapshots
    """
    # Without a `dateTime` argument every probe returns the same rows, so
    # walking back N hours would report the current snapshot N times. Ask once
    # and report the snapshot the endpoint actually serves.
    if hours is not None:
        click.echo(
            "warning: --hours is ignored — zeroTrustMetrics takes no dateTime "
            "argument, so only the current snapshot is addressable.",
            err=True,
        )
    result = _post_graphql(
        ctx,
        "GetRiskAttributionScores",
        {"includeMac": False, "includeL4Detail": False},
        _ZERO_TRUST_QUERY,
    )
    _check_errors(result)
    rows = (
        result.get("data", {}).get("policyMetrics", {}).get("zeroTrustMetrics") or []
    )
    available = []
    if rows:
        available.append({"snapshot": rows[0].get("dateTime"), "rows": len(rows)})
    render(available, ctx.format, ctx.query)


@group.command("query")
@click.option(
    "--body-file",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="JSON file containing {operationName, variables, query}.",
)
@pass_context
def cmd_raw_query(ctx, body_file):
    """Execute a raw GraphQL request from a JSON payload file.

    Escape hatch for ad-hoc GraphQL queries other than the predefined ones.
    The file must contain a complete GraphQL request body:

      {
        "operationName": "<name>",
        "variables": { ... },
        "query": "<gql string>"
      }

    Example:
      elisity reporting query --body-file ./my-query.json
    """
    with open(body_file) as f:
        payload = _json.load(f)

    client = ctx.ensure_client()
    result = client.post(GRAPHQL_PATH, data=payload)
    render(result, ctx.format, ctx.query)
