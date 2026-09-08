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

# Query shape matches the CCC dashboard (schema as of CCC 26.x: zeroTrustMetrics
# takes only `site` + `filters`; the snapshot argument was removed server-side
# and the coverage fields were renamed zeroTrustScore / leastPrivilegeScore).
# Preserved close to verbatim so the server-side
# variable-validation step accepts it (@include directives reference the
# `includeMac` and `includeL4Detail` variables — dropping them produces a
# `ValidationError: Unused variable` response).
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
      zeroTrustScore
      leastPrivilegeScore
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
    """Top-of-hour timestamp for the CURRENT hour (UTC).

    CCC publishes the current hour's snapshot as soon as the hour starts, and the
    dashboard queries with the current time, so the freshest value lives at the
    current top-of-hour. Requesting the *previous* hour (the pre-2026-09-08
    behaviour) returned a stale score — e.g. 57.5 for 17:00 while the UI, and any
    agent passing `now`, already saw 86.0 for 18:00.
    """
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    return now.strftime("%Y-%m-%dT%H:%M:%S.000Z")


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
    help="DEPRECATED and ignored: CCC 26.x serves only the current snapshot. "
    "Accepted for backward compatibility; a warning is written to stderr.",
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
    include_mac,
    include_l4_detail,
):
    """Get Zero Trust scores (the metrics from CCC's Zero Trust page).

    Returns one row per (site, policy group) for the current snapshot with deviceCount,
    totalFlows, restrictedFlows, zeroTrustScore (Zero Trust device score),
    leastPrivilegeScore (least-privilege policy score), plus L4 port exposure and
    threat-vector metrics (MITRE techniques + port exposure scores).

    IMPORTANT — the score alone does NOT tell you *why* it is low. A 0%
    coverage row can mean the group has no policy, has only simulation
    (MONITOR_ONLY) policies, or has active policies that don't cover its real
    traffic — three causes with different fixes. Do not assume "simulation" and
    recommend `policy change-status` from this command's output. To attribute a
    low score to the right cause, use `reporting diagnose-low-score`, which
    joins these scores with each group's actual policy status.

    Examples (note: -q / -f are top-level flags — place them BEFORE the
    group name):

      elisity reporting get-zero-trust-metrics
      elisity reporting get-zero-trust-metrics --site Boston --site CORK
      elisity reporting get-zero-trust-metrics --include-l4-detail

      # Per-policy-group coverage scores
      elisity -q '[].{site: siteName, pg: policyGroupName, devices: deviceCount, zt: zeroTrustScore, lp: leastPrivilegeScore}' \\
        -f table reporting get-zero-trust-metrics

      # Tenant total device count covered by the snapshot
      elisity -q 'sum([].deviceCount)' reporting get-zero-trust-metrics

      # Device-weighted average coverage via jq (JMESPath lacks generic
      # arithmetic; null-safe with `// 0`)
      elisity reporting get-zero-trust-metrics | jq '
        (map((.zeroTrustScore // 0) * .deviceCount) | add) /
        (map(.deviceCount) | add)
      '
    """
    if snapshots:
        click.echo(
            "warning: --snapshot is ignored — the CCC reporting schema now serves "
            "the current snapshot only (argument removed server-side in CCC 26.x).",
            err=True,
        )
    variables = {
        "includeMac": include_mac,
        "includeL4Detail": include_l4_detail,
    }
    if sites:
        variables["site"] = _lookup_sites(ctx, list(sites))

    result = _post_graphql(ctx, "GetRiskAttributionScores", variables, _ZERO_TRUST_QUERY)
    _check_errors(result)

    metrics = (
        result.get("data", {}).get("policyMetrics", {}).get("zeroTrustMetrics") or []
    )
    render(metrics, ctx.format, ctx.query)


# ---------------------------------------------------------------------------
# diagnose-low-score — joins the Zero Trust coverage metric with the actual
# per-policy-group policy status so a low/zero score can be attributed to the
# RIGHT root cause. A 0% coverage score alone is ambiguous: it can mean the
# group has no policy at all, has only simulation (MONITOR_ONLY) policies, or
# has active policies that don't cover the group's real traffic. Each case has
# a different fix — recommending "activate the simulation policies" for a group
# that has no policy (or whose policies are already active) is a fabricated
# remediation. This command makes the distinction explicit.
# ---------------------------------------------------------------------------

_POLICIES_ENDPOINT = "/api/policy/v1/policy-sets/policies"

# Remediation guidance keyed by diagnosis. Kept terse and pointing at real
# commands so an agent can act without inventing verbs.
_DIAGNOSIS_REMEDIATION = {
    "NO_POLICY": (
        "No policy governs this group — the score is 0 because nothing is "
        "defined, NOT because a policy is in simulation. Create policy "
        "(`elisity policy create-policy`), check `elisity insights "
        "get-policy-suggestion-list` for AI-suggested policies, or — if these "
        "devices belong in another group — reclassify them. Do NOT recommend "
        "`change-status`: there is no policy to change."
    ),
    "SIMULATION_ONLY": (
        "Every policy for this group is in Simulation (MONITOR_ONLY). Review "
        "the simulated traffic, then activate with `elisity policy "
        "change-status` (MONITOR_ONLY -> MONITOR_AND_ENFORCE)."
    ),
    "EXTERNAL_ONLY": (
        "Policies for this group are in Independent Control (MONITOR_EXTERNAL) "
        "— enforcement is delegated to an external system, so CCC reports low "
        "coverage by design. Confirm this is intentional before changing it."
    ),
    "MIXED_LOW_COVERAGE": (
        "This group has BOTH active and simulation policies, yet coverage is "
        "still low. Activating the remaining simulation policies may help, but "
        "active policies already exist and coverage is low — verify the "
        "group's real flows actually match those policies "
        "(`elisity reporting get-traffic-count --policy-status NO_POLICY "
        "--site <site>`) before assuming activation alone fixes the score."
    ),
    "ACTIVE_LOW_COVERAGE": (
        "Policies for this group are already active (MONITOR_AND_ENFORCE), so "
        "this is NOT a simulation problem. Low coverage means the group's real "
        "traffic isn't covered by those policies — typically unclassified "
        "devices in a catch-all group, or flows hitting PG-pairs with no rule. "
        "Reclassify devices into specific groups and/or add policies for the "
        "uncovered flows; inspect with `elisity reporting get-traffic-count "
        "--policy-status NO_POLICY --site <site>`."
    ),
}


def _classify_pg(active: int, simulation: int, external: int):
    """Map a policy-mode tally for one policy group to a diagnosis label."""
    total = active + simulation + external
    if total == 0:
        return "NO_POLICY"
    if active > 0 and simulation > 0:
        return "MIXED_LOW_COVERAGE"
    if active > 0:
        return "ACTIVE_LOW_COVERAGE"
    if simulation > 0:
        return "SIMULATION_ONLY"
    return "EXTERNAL_ONLY"


@group.command("diagnose-low-score")
@click.option(
    "--snapshot",
    "snapshot",
    default=None,
    help="ISO-8601 snapshot time (top-of-hour UTC). Default: previous full hour. "
    "Use `elisity reporting list-snapshots` to find a populated snapshot.",
)
@click.option(
    "--site",
    "sites",
    multiple=True,
    default=None,
    help="Filter to one or more site names (server-side). Repeatable.",
)
@click.option(
    "--threshold",
    type=float,
    default=50.0,
    help="Flag policy groups whose device OR policy coverage is below this "
    "percentage (default 50.0). Use 100 to classify every group.",
)
@pass_context
def cmd_diagnose_low_score(ctx, snapshot, sites, threshold):
    """Explain WHY policy groups score low — no-policy vs simulation vs uncovered.

    A Zero Trust coverage score of 0 is ambiguous on its own. This command
    joins the coverage metric (`get-zero-trust-metrics`) with the actual policy
    status of each group (from the policy stream) and assigns one of:

    \b
      NO_POLICY           no policy references the group at all -> create one
      SIMULATION_ONLY     all policies are MONITOR_ONLY          -> activate them
      EXTERNAL_ONLY       all policies are MONITOR_EXTERNAL       -> by design
      MIXED_LOW_COVERAGE  active + simulation, still low coverage -> verify flows
      ACTIVE_LOW_COVERAGE policies already active, still low      -> reclassify devices

    Each row carries a `remediation` string. This is what stops an agent from
    recommending "activate the simulation policies" for a group that has no
    policy (nothing to activate) or whose policies are already active.

    Heuristic + limitation: a group is matched to a policy when it appears as
    the source OR destination of a non-disabled policy. System groups shared
    across sites (e.g. Unassigned) match policies authored at other sites, so
    their policy counts are tenant-wide, not site-scoped — the diagnosis label
    is still correct, but treat the raw counts as an upper bound.

    Examples:
      elisity -f table reporting diagnose-low-score
      elisity reporting diagnose-low-score --site Hospital --threshold 100
    """
    # 1. Coverage metrics for the snapshot.
    if snapshot:
        click.echo(
            "warning: --snapshot is ignored — the CCC reporting schema now serves "
            "the current snapshot only.",
            err=True,
        )
    variables = {
        "includeMac": False,
        "includeL4Detail": False,
    }
    if sites:
        variables["site"] = _lookup_sites(ctx, list(sites))

    result = _post_graphql(ctx, "GetRiskAttributionScores", variables, _ZERO_TRUST_QUERY)
    _check_errors(result)
    metrics = (
        result.get("data", {}).get("policyMetrics", {}).get("zeroTrustMetrics") or []
    )

    # 2. Policy stream -> per-PG mode tally (keyed by PG id, src or dst).
    client = ctx.ensure_client()
    policies = client.get_ndjson(_POLICIES_ENDPOINT) or []
    by_pg: dict = {}
    for p in policies:
        if p.get("disabled"):
            continue
        mode = p.get("monitorMode")
        for key in ("srcId", "dstId"):
            pg_id = p.get(key)
            if not pg_id:
                continue
            tally = by_pg.setdefault(
                pg_id, {"MONITOR_AND_ENFORCE": 0, "MONITOR_ONLY": 0, "MONITOR_EXTERNAL": 0}
            )
            if mode in tally:
                tally[mode] += 1

    # 3. Join: flag rows below threshold, classify, attach remediation.
    rows = []
    for m in metrics:
        dev_cov = m.get("zeroTrustScore")
        pol_cov = m.get("leastPrivilegeScore")
        low = (dev_cov is None or dev_cov < threshold) or (
            pol_cov is None or pol_cov < threshold
        )
        if not low:
            continue
        tally = by_pg.get(m.get("policyGroupId"), {})
        active = tally.get("MONITOR_AND_ENFORCE", 0)
        simulation = tally.get("MONITOR_ONLY", 0)
        external = tally.get("MONITOR_EXTERNAL", 0)
        diagnosis = _classify_pg(active, simulation, external)
        rows.append(
            {
                "siteName": m.get("siteName"),
                "policyGroupName": m.get("policyGroupName"),
                "policyGroupId": m.get("policyGroupId"),
                "deviceCount": m.get("deviceCount"),
                "zeroTrustScore": dev_cov,
                "leastPrivilegeScore": pol_cov,
                "policiesActive": active,
                "policiesSimulation": simulation,
                "policiesExternal": external,
                "diagnosis": diagnosis,
                "remediation": _DIAGNOSIS_REMEDIATION[diagnosis],
            }
        )

    rows.sort(key=lambda r: (r["zeroTrustScore"] if r["zeroTrustScore"] is not None else -1))
    render(rows, ctx.format, ctx.query)


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

_POLICY_SET_SCORE_QUERY = """query PolicySetEnforcementScore($id: UUID!, $dt: [DateTime!]!, $site: [Site!]) {
  policyMetrics {
    policySetEnforcementScore(policySetId: $id, dateTime: $dt, site: $site) {
      ... on FloatMetricValue {
        value
        dateTime
        __typename
      }
    }
  }
}"""

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


@group.command("get-policy-set-enforcement-score")
@click.argument("policy_set_id")
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
def cmd_policy_set_score(ctx, policy_set_id, snapshots, sites):
    """Per-policy-set enforcement score (GraphQL — works where the REST
    `policy get-enforcement-score` returns 404).

    Examples:
      # Get every policy set ID
      elisity policy get-all-as-nd-json -q '[].{id: id, name: name}'

      # Pull score for one
      elisity reporting get-policy-set-enforcement-score <POLICY_SET_ID>

      # Fan out across all policy sets
      for id in $(elisity policy get-all-as-nd-json -q '[].id' -f csv | tail -n +2); do
        echo "=== $id ==="
        elisity reporting get-policy-set-enforcement-score "$id"
      done
    """
    snaps = list(snapshots) if snapshots else [_default_snapshot()]
    variables = {"id": policy_set_id, "dt": snaps}
    if sites:
        variables["site"] = _lookup_sites(ctx, list(sites))

    result = _post_graphql(ctx, "PolicySetEnforcementScore", variables, _POLICY_SET_SCORE_QUERY)
    _check_errors(result)
    data = (
        result.get("data", {}).get("policyMetrics", {}).get("policySetEnforcementScore")
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

_POLICY_COUNT_NEEDED_QUERY = """query PolicyCountNeeded($dt: [DateTime!]!, $site: [Site!]) {
  policyMetrics {
    countNeeded(dateTime: $dt, site: $site) {
      dateTime
      value
    }
  }
}"""

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


@group.command("get-policy-count-needed")
@click.option("--snapshot", "snapshots", multiple=True, default=None,
              help="ISO-8601 snapshot time. Repeatable. Default: previous full hour.")
@click.option("--site", "sites", multiple=True, default=None,
              help="Filter to one or more site names. Repeatable.")
@pass_context
def cmd_policy_count_needed(ctx, snapshots, sites):
    """Policies needed for full policy-group coverage.

    Surfaces the count of *additional* policies CCC thinks would be needed
    to fully cover the policy groups at this snapshot.
    """
    snaps = list(snapshots) if snapshots else [_default_snapshot()]
    variables = {"dt": snaps}
    sl = _maybe_sites(ctx, sites)
    if sl is not None:
        variables["site"] = sl
    result = _post_graphql(ctx, "PolicyCountNeeded", variables, _POLICY_COUNT_NEEDED_QUERY)
    _check_errors(result)
    render(result.get("data", {}).get("policyMetrics", {}).get("countNeeded") or [],
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
    help="DEPRECATED and ignored: the server no longer addresses snapshots by hour.",
)
@pass_context
def cmd_list_snapshots(ctx, hours):
    """Report the snapshot the reporting endpoint currently serves.

    CCC 26.x removed per-hour snapshot addressing from /api/reporting/v1/data;
    the endpoint serves the current snapshot only. This returns that snapshot's
    server-side dateTime and row count. `--hours` is accepted but ignored.

    Example:
      elisity reporting list-snapshots
    """
    # CCC 26.x removed the snapshot argument from zeroTrustMetrics: the endpoint
    # serves only the current snapshot. Report that one (with its server-side
    # dateTime) rather than probing hours that can no longer be addressed.
    if hours is not None:
        click.echo(
            "warning: --hours is ignored — the CCC reporting schema now serves "
            "the current snapshot only.",
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
        snap = rows[0].get("dateTime")
        available.append({"snapshot": snap, "rows": len(rows)})
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
