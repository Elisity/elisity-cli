#!/usr/bin/env python3
"""
Auto-generate Click CLI commands from the Elisity CCC OpenAPI spec.
Reads an OpenAPI JSON spec and produces Python modules under
src/elisity_cli/commands/.

Spec resolution (first match wins):
    1. --spec <path>            explicit CLI argument
    2. $ELISITY_API_SPEC        environment variable
    3. DEFAULT_SPEC_PATH        the historical host location

Usage:
    python3 generate_commands.py --spec ./api-docs-26.7.json
    python3 generate_commands.py --spec ./api-docs-26.9.json \
        --overlay spec-overlays/ccc-26.9-hotpatch-device-patch.json
    ELISITY_API_SPEC=./api-docs-26.7.json python3 generate_commands.py
"""

import argparse
import copy
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# Historical host path. Kept as the last-resort default so existing host
# workflows (`python3 generate_commands.py` with no arguments) keep working,
# but it is no longer the only way to point the generator at a spec — it does
# not exist inside agent containers or CI.
DEFAULT_SPEC_PATH = os.path.expanduser("~/.claude/skills/elisity-api-expert/api-docs.json")
SPEC_PATH_ENV_VAR = "ELISITY_API_SPEC"

DEFAULT_OUTPUT_DIR = Path(__file__).parent / "src" / "elisity_cli" / "commands"

# Hand-written command groups that are NOT in the OpenAPI spec and therefore
# can never be produced by this generator. They must survive regeneration:
# their modules are never rewritten, and they stay registered in
# commands/__init__.py's COMMAND_GROUPS. Dropping them here would silently
# unregister `elisity reporting` / `elisity glossary` from the CLI.
HANDCODED_GROUPS = ("glossary", "reporting")

DEVICE_PATH = "/api/identity-graph/v1/devices/{id}"

# PUT replaces a device's IP and VEN, so an attribute-only body detaches a
# dynamically attached device. The CLI exposes no PUT for these operations.
#
# Each omitted operation maps to the operation that replaces it. Generation
# fails when a spec has the omitted operation but not its replacement
# (assert_omitted_operations_replaced): the published CCC 26.9 spec declares the
# device PUT and no PATCH — the PATCH is a 26.9 hot patch — so omitting the PUT
# without the spec overlay would silently drop `devices update-device`.
OMITTED_OPERATIONS = {("put", DEVICE_PATH): ("patch", DEVICE_PATH)}

# Spec overlays add operations a tenant serves but its published spec does not
# declare yet. Each is checked in with its provenance and applied with
# `--overlay`; see apply_overlays().
SPEC_OVERLAY_DIR = Path(__file__).parent / "spec-overlays"

# Map OpenAPI tags to CLI command group names
#
# CCC 26.7 renamed a large set of tags from `kebab-case-controller` style to
# human-readable names ("site-controller" -> "Sites"). The 26.3 names are
# deliberately KEPT alongside the 26.7 ones: they cost nothing, and they let the
# generator still reproduce the 26.3 command set byte-for-byte, which is the
# regression check that proves a generator edit changed nothing it should not.
#
# Every tag in a spec MUST resolve here. `main()` fails the generation and names
# the offenders if any do not — see the assert_every_tag_mapped guard. The
# path-prefix fallback in resolve_group() is a safety net for reading a spec,
# not a licence to leave tags unmapped: it silently routed 6 renamed
# `Connectors Configurations` operations from `connectors` into `devices` on the
# 26.7 bump, which is exactly the class of drift the guard now prevents.
TAG_TO_GROUP = {
    # Topology
    "site-controller": "topology",
    # NOTE: site-label-controller intentionally NOT mapped here.
    # It is mapped to "policy" below (site labels are a policy concept).
    "distribution-zone-controller": "topology",
    "distribution-zone-controller-v-2": "topology",
    "Virtual Edge Group": "topology",
    "Virtual Edge": "topology",
    "virtual-edge-node-controller": "topology",
    "virtual-edge-node-overview-controller": "topology",
    "virtual-edgne-node-topology-controller": "topology",
    "virtual-edges-logging-controller": "topology",
    "Bulk Update": "topology",
    "Bulk Validation": "topology",
    "flow-exporter-controller": "topology",
    "cloud-controller": "topology",
    "dashboard-controller": "topology",
    "global-credentials-controller": "topology",
    "global-interfaces-settings-controller": "topology",
    "targets-controller": "topology",
    "Task Manager": "topology",
    # Policy
    "Policy": "policy",
    "Policy Bulk": "policy",
    "Policy Set": "policy",
    "policy-set-controller": "policy",
    "Policy Group": "policy",
    "Policy Group Bulk": "policy",
    "Policy Group Label": "policy",
    "Policy Group with Device Group Bulk": "policy",
    "Policy View": "policy",
    "Security Profile": "policy",
    "Evaluator": "policy",
    "Device": "policy",
    "Image": "policy",
    "Matched Assets": "policy",
    "State Sync": "policy",
    "Feature Flag": "policy",
    "site-label-controller": "policy",
    # Insights (policy intelligence)
    "Insights": "insights",
    "Dynamic Policy Group Insights": "insights",
    "Network Policy Group Insights": "insights",
    "Suggestion": "insights",
    # Devices / Identity Graph
    "Device - CRUD": "devices",
    "Device - CRUD - v2": "devices",
    "Device - Bulk": "devices",
    "Device - Attach": "devices",
    "Device - Enrich": "devices",
    "Device - recalculate-attributes": "devices",
    "Device Event History": "devices",
    "Data": "devices",
    "Settings": "devices",
    "Suppression List": "devices",
    "Time-Based Configuration": "devices",
    "Feature Flag - Identity Graph": "devices",
    # Connectors
    "Connectors Configurations": "connectors",
    "Custom Connector Devices": "connectors",
    "Custom Connector Inventory - CRUD": "connectors",
    "Connector - connectivity-status": "connectors",
    # AD Connector Service
    "AD Agent": "ad",
    "AD Attributes": "ad",
    "AD Connector": "ad",
    "AD Device": "ad",
    "AD Domain": "ad",
    "AD Group": "ad",
    "AD Member": "ad",
    "AD User": "ad",
    "ADCS Parameters Configuration": "ad",
    "DC Status": "ad",
    "Entra ID": "ad",
    "IP Attach": "ad",
    "Time": "ad",
    # Flows
    "Device State Cache": "flows",
    "Noise Definitions": "flows",
    "Port Information": "flows",
    "Search API": "flows",
    "materialized-view-information-controller": "flows",
    # System / State
    "Spec controller": "system",
    "Task Broker": "system",
    # ------------------------------------------------------------------
    # CCC 26.7 tags
    #
    # Renames keep their 26.3 group so no existing command moves. Genuinely new
    # tags are grouped by domain, following the established concept-over-path
    # precedent (site-label-controller is mapped to `policy`, not `topology`,
    # because site labels are a policy concept).
    # ------------------------------------------------------------------
    # Topology — renames of the 26.3 *-controller tags
    "Sites": "topology",                        # was site-controller
    "Distribution Zones (DZs)": "topology",     # was distribution-zone-controller[-v-2]
    "Virtual Edges": "topology",                # was "Virtual Edge"
    "VE Groups": "topology",                    # was "Virtual Edge Group"
    "Virtual Edge Nodes (VENs)": "topology",    # was virtual-edge-node[-overview]-controller
    "VEN Topology Discovery": "topology",       # was virtual-edgne-node-topology-controller (sic)
    "Virtual Edge Logging": "topology",         # was virtual-edges-logging-controller
    "Flow Exporters": "topology",               # was flow-exporter-controller
    "Cloud Controller": "topology",             # was cloud-controller
    "Dashboard": "topology",                    # was dashboard-controller
    "Global Credentials": "topology",           # was global-credentials-controller
    "Interface Settings": "topology",           # was global-interfaces-settings-controller
    "Targets": "topology",                      # was targets-controller
    # Topology — new in 26.7
    "Virtual Edges (VEs)": "topology",
    "Topology Settings": "topology",
    # Policy — new in 26.7
    "Access Policy (LPA)": "policy",
    "Policy History": "policy",
    # Labels drive policy groups; same reasoning as site-label-controller above.
    "Label Management": "policy",
    "Label Management - Folders": "policy",
    "Label Management - Import": "policy",
    # Vendor CRUD is served by the policy service (/api/policy/v1/vendor) and
    # vendor records are policy-matching constructs.
    "Vendor": "policy",
    # Custom application definitions are consumed by policy rules. Served under
    # /api/flows/v1/applications, so this is a concept-over-path call — see
    # output/OPEN-QUESTIONS.md, reversible by moving this one line to "flows".
    "Custom Applications": "policy",
    # Devices / Identity Graph — new in 26.7
    # NOTE: the /api/identity-graph-view/ paths do NOT match the
    # "/identity-graph/" path-prefix fallback, so without these entries they
    # fall through to `system`. Mapping them explicitly is what keeps the
    # read-only device surface in `devices` where a user will look for it.
    "Devices (Read-Only)": "devices",
    "Devices Digest": "devices",
    "Devices - View Sync": "devices",
    "Offline Device Purge Settings": "devices",
    # Cloud workload discovery (/api/identity-graph/workloads/**) is one
    # coherent feature: onboard AWS -> discover -> sync -> manage workloads.
    # Kept together in `devices` because workloads are identity-graph assets
    # with the same STATIC-layer CRUD shape as devices, and splitting the
    # workflow across groups would fragment a single user task.
    "Workloads": "devices",
    "Workload Discovery": "devices",
    "Workload Connector Sync": "devices",
    "AWS Setup": "devices",
    # Connectors — new + renamed in 26.7
    "Connector Configuration": "connectors",    # the new /v1/connectors surface
    # Renamed from "Connectors Configurations". Without this entry the six
    # /api/identity-graph/v1/conf/** operations fall through to the
    # "/identity-graph/" path prefix and land in `devices`, silently moving six
    # shipped commands out of `elisity connectors`.
    "Connectors Configurations (Deprecated)": "connectors",
    "Connector - status": "connectors",
    # AD Connector Service — new in 26.7
    "AD Agent V2": "ad",
    "AD Agent Logs": "ad",
    "Subscription Refresh": "ad",
    # Distinct from topology's "Distribution Zones (DZs)": this is the AD
    # service's own DZ listing (/api/ad-connector-service/v1/distribution-zones).
    # Kept in `ad` with the service that serves it, which also avoids colliding
    # with the topology distribution-zone command names.
    "Distribution Zones": "ad",
    # Flows — new in 26.7
    "Device Heatmap": "flows",
    # System — new in 26.7
    # Snapshot/schedule endpoints are served under /api/reporting/v1/ but must
    # NOT map to `reporting`: that group is hand-coded GraphQL and the
    # HANDCODED_GROUPS collision guard would (correctly) refuse to generate.
    "Snapshot Schedules": "system",
    "Snapshots": "system",
    "Task Broker Config": "system",
    # ------------------------------------------------------------------
    # CCC 26.9 tags — every one is new; 26.9 renamed no existing tag.
    # ------------------------------------------------------------------
    # Sits beside "Security Profile": same rule-search/export surface, served
    # by the policy service under /api/policy/v2/.
    "Access Policy Security Profile": "policy",
    # Azure onboarding and the workload attach/attached calls are the same
    # cloud-workload-discovery feature the 26.7 Workloads / AWS Setup tags
    # already keep in `devices` (see the note above them).
    "Azure Workload Discovery": "devices",
    "Workload - Attach": "devices",
    # Served under /api/identity-graph/v1/connectors/tanium/, configures a
    # connector — so it lives with the connectors, not with the devices that
    # the "/identity-graph/" path-prefix fallback would have picked.
    "Tanium Sensor Mappings": "connectors",
    # Distribution zones are a topology concept; the fallback would have put
    # these two read-only calls in `devices` under the names `list`/`usage`.
    "Workload Distribution Zones": "topology",
    # Flow ingestion (/api/flows/v1/flows, /flow/api/*flowdata). The fallback
    # split these between `flows` and `system` by path prefix.
    "ingest-controller": "flows",
}

GROUP_DESCRIPTIONS = {
    "topology": "Manage network topology — sites, zones, VE groups, VEs, VENs, flow exporters",
    "policy": "Manage microsegmentation policies — policy sets, policies, groups, security profiles",
    "insights": "Policy insights and suggestions — dynamic/network group recommendations",
    "devices": "Device identity and enrichment — CRUD, bulk, attach, enrich, events",
    "connectors": "Connector management — custom connectors, configurations, connectivity",
    "ad": "Active Directory / Entra ID integration — connectors, users, groups, agents",
    "flows": "Traffic analytics — device state, flow search, noise definitions",
    "system": "System operations — tasks, specs, state sync",
}


def sanitize_name(name: str) -> str:
    """Convert an operationId or tag to a Python-safe Click command name."""
    # Remove version suffixes like _1, _2
    name = re.sub(r"_(\d+)$", "", name)
    # camelCase to kebab-case
    name = re.sub(r"([a-z])([A-Z])", r"\1-\2", name)
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", name)
    name = name.lower()
    # Clean up
    name = re.sub(r"[^a-z0-9]+", "-", name)
    name = name.strip("-")
    return name


PYTHON_KEYWORDS = {
    "from", "import", "class", "return", "def", "if", "else", "elif",
    "for", "while", "try", "except", "finally", "with", "as", "pass",
    "break", "continue", "and", "or", "not", "is", "in", "lambda",
    "global", "nonlocal", "yield", "raise", "del", "True", "False", "None",
    "assert", "async", "await", "type",
}


def python_safe(name: str) -> str:
    """Make a name safe for Python identifiers."""
    safe = name.replace("-", "_")
    if safe in PYTHON_KEYWORDS:
        safe = safe + "_param"
    return safe


# Function-argument names the generated command body owns. A spec parameter that
# normalizes onto one of these would emit `def cmd_x(ctx, confirm, ..., confirm)`
# — a SyntaxError, which _register_groups() swallows as a warning, silently
# dropping the ENTIRE group (up to 117 commands) from the CLI. For a DELETE that
# also means losing the --confirm gate. See _unique_name().
# Identifiers the generated command owns. Two groups, one rule: a spec parameter
# that normalizes onto any of them must be renamed.
#
#   Signature names — a collision emits `def cmd_x(ctx, confirm, ..., confirm)`,
#   a SyntaxError that _register_groups() swallows as a warning, silently
#   dropping the ENTIRE group (up to 181 commands) from the CLI.
#
#   Body locals — a collision compiles and runs at exit 0 while sending the
#   WRONG REQUEST. `endpoint` and `params` are the dangerous pair because both
#   are assigned before the query dict is populated: a spec parameter named
#   `params` emits `params = {}` then `params["params"] = params`, putting the
#   dict inside itself, and one named `endpoint` sends the URL as a query value.
#   The user's value never reaches the wire and nothing complains. Same silent-
#   wrong-request family as the two bugs Phase 1 fixed.
#
# `body`, `client`, `result`, `f`, `_json` and `e` are assigned after the query
# dict is built, so they cannot corrupt the request today. They are reserved
# anyway: the ordering is an implementation detail of this emitter, renaming an
# identifier is free, and the wire name is never touched either way.
RESERVED_DESTS = frozenset({
    # signature
    "ctx", "cmd_fmt", "cmd_query", "body_data", "body_file",
    # body locals
    "endpoint", "params", "body", "client", "result", "f", "_json", "e",
})
RESERVED_FLAGS = frozenset({"--format", "-f", "--query", "-q", "--body", "--body-file"})
CONFIRM_GUARD_DEST = "confirm"
CONFIRM_GUARD_FLAGS = frozenset({"--confirm", "--no-confirm"})

# --------------------------------------------------------------------------
# Which operations need --confirm
# --------------------------------------------------------------------------
# The gate used to key on the DELETE verb. That is the wrong axis: CCC deletes
# things over POST and PUT too, so `topology bulk-force-delete-ve-ns` (POST, many
# VENs) shipped ungated while `topology force-delete-ven` (DELETE, one VEN) was
# gated — and both docs told agents that every delete and bulk-delete requires
# --confirm. Gate on what the operation DOES.
#
# The path is the source of truth, not the command name: command names come from
# the spec's operationId and CCC renames them across releases, while the path
# names the action the server performs.
#
# Whole-segment matching, never substring. `/devices/purge-settings` configures
# the offline-purge policy and destroys nothing; a substring match on "purge"
# would gate it.
DESTRUCTIVE_PATH_SEGMENTS = frozenset({
    "delete",             # .../bulk/delete
    "bulk-delete",        # .../labels/bulk-delete
    "force-delete",       # .../virtual-edge-nodes/bulk/force-delete
    "force",              # .../virtual-edge-nodes/{id}/force  (force-delete a VEN)
    "purge",              # .../devices/bulk/purge
    "decommission",       # .../virtual-edge-nodes/{id}/decommission
    "detach",             # .../devices/{id}/detach
    "reset-to-default",   # .../insights/policy-groups/reset-to-default
    "recreate",           # .../insights/policy-groups/recreate — CCC's own summary
                          # for these two is "Delete and Create all suggestions"
})

# A dry-run sibling of a destructive path. `/virtual-edges/bulk/delete/validate`
# carries the `delete` segment but only reports what a delete WOULD do, so gating
# it would be friction with no safety value — and, worse, would teach users that
# --confirm on these paths is meaningless.
DRY_RUN_PATH_SEGMENTS = frozenset({"validate"})

# Operations that destroy state although no path segment says so. Keyed by
# (METHOD, path); keep this list short — the path rule above is the norm.
DESTRUCTIVE_OPERATIONS = frozenset({
    # CCC 26.9 `ad set-groups-default-enabled`: the spec calls it a "master
    # reset" of the enable-all-groups default.
    ("PUT", "/api/ad-connector-service/v1/groups/default-enabled"),
})


def is_destructive_operation(method: str, path: str) -> bool:
    """Does this operation need the --confirm gate?

    True for every DELETE (kept as a floor — the README, AGENTS.md and the
    user guide have always promised it, and narrowing it would be a silent
    behaviour regression), plus any verb whose path names a destructive action,
    plus the few operations listed in DESTRUCTIVE_OPERATIONS.

    This predicate is the single definition of "destructive" in the project.
    `tools/audit_counts.py` imports it to build its coverage denominator rather
    than re-deriving the rule, because a coverage metric measured against a
    different set than the gate enforces is how "100% covered" stayed true while
    ten destructive commands sat ungated.
    """
    if method.upper() == "DELETE" or (method.upper(), path) in DESTRUCTIVE_OPERATIONS:
        return True
    segments = {s for s in path.split("/") if s and not s.startswith("{")}
    if segments & DRY_RUN_PATH_SEGMENTS:
        return False
    return bool(segments & DESTRUCTIVE_PATH_SEGMENTS)


# Words that make a COMMAND NAME look destructive. Not used to decide the gate —
# the path decides that — but used by tools/audit_counts.py as a watchdog: any
# command whose name matches while its path does not classify is surfaced for a
# human to rule on, so the two can never drift apart silently.
DESTRUCTIVE_NAME_WORDS = frozenset({
    "delete", "purge", "decommission", "detach", "destroy", "remove", "wipe",
    "erase", "revoke", "terminate", "force",
})


def _unique_name(base: str, used: set, suffix: str = "") -> str:
    """Return `base` if free, else a numbered variant. Records the result.

    Collisions are rare but real: a path param and a query param sharing a name,
    two query params differing only by a character that normalizes away
    (`foo.bar` / `foo-bar`), or a spec param named `confirm` on a DELETE.
    """
    candidate = f"{base}{suffix}" if base in used and suffix else base
    counter = 2
    while candidate in used:
        candidate = f"{base}{suffix}_{counter}" if suffix else f"{base}_{counter}"
        counter += 1
    used.add(candidate)
    return candidate


def resolve_parameter_names(method: str, path_params: list, query_params: list,
                            path: str = "") -> tuple:
    """Assign a collision-free Click flag + Python dest to every parameter.

    The wire name (what goes into the URL path or query string) is never
    changed — only the Python identifier, and the CLI flag if and only if it
    would collide with one the command already owns.

    The request-body flags are reserved unconditionally, not just when the
    operation has a body — a parameter named `body` on a body-less operation is
    harmless to rename and keeps the rule simple. `path` is needed because the
    --confirm guard is now emitted for destructive non-DELETE operations too, so
    the identifier it occupies must be reserved for exactly the same set.
    """
    used_dests = set(RESERVED_DESTS)
    used_flags = set(RESERVED_FLAGS)
    if is_destructive_operation(method, path):
        used_dests.add(CONFIRM_GUARD_DEST)
        used_flags |= CONFIRM_GUARD_FLAGS

    resolved_path = []
    for pname, ptype, pdesc in path_params:
        base = python_safe(pname.replace("-", "_")).lower()
        resolved_path.append({
            "spec_name": pname,
            "dest": _unique_name(base, used_dests),
        })

    resolved_query = []
    for pname, ptype, preq, pdesc, pdefault in query_params:
        base = python_safe(pname.replace(".", "_").replace("-", "_"))
        flag = _unique_name(f"--{pname}", used_flags, suffix="-param")
        resolved_query.append({
            "spec_name": pname,
            "dest": _unique_name(base, used_dests),
            "flag": flag,
            "type": ptype,
            "required": preq,
            "desc": pdesc,
            "default": pdefault,
        })

    return resolved_path, resolved_query


# Per-operation command names, keyed by (METHOD, path) because the path is
# stable across releases while operationIds are not. Used only where the
# operationId yields a name that is generic in its group (`list`, `usage`,
# `export`), carries a dedupe suffix (`-post`), or would take a shipped name.
#
# Regenerating the 26.7 spec with this map changes exactly one command: the
# suppression-list GET (`get-users` in 26.7) becomes `search-suppression-list`.
# Every other path below is new in CCC 26.9 (the device PATCH via the 26.9
# hot-patch overlay), and the two device-attach pins name what 26.7 already
# emitted. assert_overrides_emitted() fails generation if a
# collision would make dedupe_command_names() suffix one of these names.
COMMAND_NAME_OVERRIDES = {
    # ENG-31333: the device PATCH (omitted ip/venId keep the current value)
    # takes the `update-device` name; the PUT is in OMITTED_OPERATIONS.
    ("PATCH", DEVICE_PATH): "update-device",
    # CCC 26.9 added /v1/workloads/attach[ed] with operationIds `attach` and
    # `attached`, which moved the shipped device commands to `attach-post` /
    # `attached-post` and gave their names to the workload calls. Pinned so the
    # device commands keep their names whatever the workload ids become.
    ("POST", "/api/identity-graph/v1/devices/attach"): "attach",
    ("POST", "/api/identity-graph/v1/devices/attached"): "attached",
    ("POST", "/api/identity-graph/v1/workloads/attach"): "attach-workload",
    # Batch form; the plural follows create-security-profile/-profiles.
    ("POST", "/api/identity-graph/v1/workloads/attached"): "attach-workloads",
    # Suppression List: 26.9 renamed the GET's operationId getUsers -> search
    # (which would ship as `devices search`) and added an export with
    # operationId `export`. `get-users` never fit — it lists suppression
    # entries, not users — and 26.9 makes `filters` required, so the old
    # invocation breaks whatever the name.
    ("GET", "/api/identity-graph/v1/suppression"): "search-suppression-list",
    ("POST", "/api/identity-graph/v1/suppression/export"): "export-suppression-list",
    # Workload Distribution Zones (operationIds `list_2` and `usage`).
    ("GET", "/api/identity-graph/v1/workload-distribution-zones"):
        "list-workload-distribution-zones",
    ("GET", "/api/identity-graph/v1/workload-distribution-zones/{id}/usage"):
        "get-workload-distribution-zone-usage",
    # Azure Workload Discovery shares `devices` with the 26.7 AWS discovery
    # commands (validate-permissions-pre-creation, list-available-regions, ...);
    # without `azure` in the name two of these collided and got `-post`.
    ("GET", "/api/identity-graph/workloads/discovery/azure/setup/permissions"):
        "list-azure-required-permissions",
    ("POST", "/api/identity-graph/workloads/discovery/azure/regions"):
        "list-azure-regions-pre-creation",
    ("POST", "/api/identity-graph/workloads/discovery/azure/resource-groups"):
        "list-azure-resource-groups-pre-creation",
    ("POST", "/api/identity-graph/workloads/discovery/azure/scope-preview"):
        "preview-azure-scope-pre-creation",
    ("POST", "/api/identity-graph/workloads/discovery/azure/subscriptions"):
        "list-azure-subscriptions-pre-creation",
    ("POST", "/api/identity-graph/workloads/discovery/azure/validate-connection"):
        "validate-azure-connection-pre-creation",
    ("POST", "/api/identity-graph/workloads/discovery/azure/validate-permissions"):
        "validate-azure-permissions-pre-creation",
    ("POST", "/api/identity-graph/workloads/discovery/azure/validate-region-permissions"):
        "validate-azure-region-permissions-pre-creation",
    ("POST", "/api/identity-graph/workloads/discovery/azure/{connectorId}/{endpointId}/regions"):
        "list-azure-regions-existing",
    ("POST", "/api/identity-graph/workloads/discovery/azure/{connectorId}/{endpointId}/resource-groups"):
        "list-azure-resource-groups-existing",
    ("POST", "/api/identity-graph/workloads/discovery/azure/{connectorId}/{endpointId}/scope-preview"):
        "preview-azure-scope-existing",
    ("POST", "/api/identity-graph/workloads/discovery/azure/{connectorId}/{endpointId}/subscriptions"):
        "list-azure-subscriptions-existing",
    ("POST", "/api/identity-graph/workloads/discovery/azure/{connectorId}/{endpointId}/validate-connection"):
        "validate-azure-connection-existing",
    ("POST", "/api/identity-graph/workloads/discovery/azure/{connectorId}/{endpointId}/validate-permissions"):
        "validate-azure-permissions-existing",
    ("POST", "/api/identity-graph/workloads/discovery/azure/{connectorId}/{endpointId}/validate-region-permissions"):
        "validate-azure-region-permissions-existing",
    # Tanium Sensor Mappings land in `connectors`, next to every other
    # connector, where `fetch-catalog` / `probe-mapping` say nothing.
    ("POST", "/api/identity-graph/v1/connectors/tanium/sensors"):
        "fetch-tanium-sensor-catalog",
    ("POST", "/api/identity-graph/v1/connectors/tanium/sensors/detail"):
        "fetch-tanium-sensor-detail",
    ("POST", "/api/identity-graph/v1/connectors/tanium/sensor-mappings/probe"):
        "probe-tanium-sensor-mapping",
    # Access Policy Security Profile v2 sits beside the Security Profile v2
    # search/export commands; `search-profiles` / `export-rules` would not say
    # which profile type.
    ("POST", "/api/policy/v2/access-policy-security-profiles/search"):
        "search-access-policy-security-profiles",
    ("POST", "/api/policy/v2/access-policy-security-profiles/export"):
        "export-access-policy-security-profiles",
    ("POST", "/api/policy/v2/access-policy-security-profiles/{id}/rules/search"):
        "search-access-policy-security-profile-rules",
    ("POST", "/api/policy/v2/access-policy-security-profiles/{id}/rules/export"):
        "export-access-policy-security-profile-rules",
    # AD Group "enable all groups by default" toggle.
    ("GET", "/api/ad-connector-service/v1/groups/default-enabled"):
        "get-groups-default-enabled",
    ("PUT", "/api/ad-connector-service/v1/groups/default-enabled"):
        "set-groups-default-enabled",
    # Flow ingestion: two operationIds sanitize to `accept-flows`.
    ("POST", "/api/flows/v1/flows"): "accept-flows",
    ("POST", "/flow/api/flowdata"): "accept-flow-data",
    ("POST", "/flow/api/appflowdata"): "accept-app-flow-data",
}


def make_command_name(method: str, op_id: str, path: str, tag: str) -> str:
    """Generate a human-friendly command name from operation context.

    COMMAND_NAME_OVERRIDES wins outright. Otherwise the name comes from the
    operationId, falling back to method + last path segment when there is no
    operationId, or when the operationId sanitizes to nothing (e.g. an id of
    only punctuation). Without that second check the command would be
    registered under an empty name and be impossible to invoke — a silently
    lost command.
    """
    override = COMMAND_NAME_OVERRIDES.get((method.upper(), path))
    if override:
        return override
    name = sanitize_name(op_id) if op_id else ""
    if not name:
        name = f"{method.lower()}-{sanitize_name(path.split('/')[-1])}"
    if not name.strip("-"):
        name = f"{method.lower()}-{sanitize_name(path) or 'unnamed'}"
    return name


def schema_base_type(schema: dict) -> str:
    """The non-null base type of a parameter schema, across OpenAPI 3.0 and 3.1.

    3.0.1 spells an optional string `{"type": "string", "nullable": true}`.
    3.1.0 spells it `{"type": ["string", "null"]}` — a *list*. CCC moved from
    3.0.1 (26.3) to 3.1.0 (26.7), and a plain `schema.get("type") == "integer"`
    comparison silently returns False for the list form, degrading an int
    parameter to a string. That surfaces as a runtime error for the user rather
    than a generation error for us, so normalize both spellings here.

    The 26.7 spec happens to use no type arrays, but it declares 3.1.0 and the
    next revision is free to use them.
    """
    t = schema.get("type") if isinstance(schema, dict) else None
    if isinstance(t, list):
        non_null = [x for x in t if x != "null"]
        return non_null[0] if len(non_null) == 1 else ""
    return t if isinstance(t, str) else ""


def extract_params(op: dict) -> tuple:
    """Extract path params, query params from operation."""
    path_params = []
    query_params = []
    for p in op.get("parameters", []):
        param_in = p.get("in", "")
        param_name = p.get("name", "")
        param_type = "str"
        schema = p.get("schema", {})
        base_type = schema_base_type(schema)
        if base_type == "integer":
            param_type = "int"
        elif base_type == "boolean":
            param_type = "bool"
        required = p.get("required", False)
        desc = p.get("description", "")

        if param_in == "path":
            path_params.append((param_name, param_type, desc))
        elif param_in == "query":
            query_params.append((param_name, param_type, required, desc, schema.get("default")))
    return path_params, query_params


def merge_path_templates(path: str, path_params: list) -> list:
    """Ensure every `{placeholder}` in the path has a corresponding argument.

    OpenAPI requires each path-template expression to be backed by a declared
    path parameter, but the CCC spec does not always comply. Example from the
    26.3 baseline:

        POST /api/identity-graph/v1/custom-connector/{id}/import/{uploadId}/cancel

    declares only `uploadId`. With `{id}` left unsubstituted, the generated
    f-string resolved it against Python's builtin `id`, producing

        /api/identity-graph/v1/custom-connector/<built-in function id>/import/...

    — a nonsense URL sent with exit code 0. Synthesizing the missing argument
    is not inventing an endpoint: the placeholder is literally in the spec's
    path. Parameters are returned in path order so the positional Click
    arguments read left-to-right like the URL.
    """
    declared = {p[0]: p for p in path_params}
    ordered, seen = [], set()

    for name in re.findall(r"\{([^}]*)\}", path):
        if not sanitize_name(name):
            raise ValueError(
                f"path template {{{name}}} in {path} has no usable name — "
                "cannot generate a safe argument for it"
            )
        if name in seen:
            continue
        seen.add(name)
        if name in declared:
            ordered.append(declared[name])
        else:
            ordered.append((name, "str", f"Path parameter (undeclared in spec) — {name}"))

    # Keep any declared path param that the template does not reference, rather
    # than silently dropping it.
    ordered.extend(p for p in path_params if p[0] not in seen)
    return ordered


def has_request_body(op: dict) -> bool:
    return bool(op.get("requestBody"))


def produces_ndjson(op: dict) -> bool:
    """Check if an endpoint produces NDJSON responses."""
    for code, r in op.get("responses", {}).items():
        content = r.get("content", {})
        for ct in content:
            if "ndjson" in ct:
                return True
    return False


def generate_command(method: str, path: str, op: dict, cmd_name: str) -> str:
    """Generate a single Click command function."""
    path_params, query_params = extract_params(op)
    path_params = merge_path_templates(path, path_params)
    has_body = has_request_body(op)
    is_ndjson = produces_ndjson(op)
    raw_summary = op.get("summary", op.get("description", "")) or f"{method.upper()} {path}"
    summary = raw_summary.split("\n")[0].replace('"', '\\"').replace("\\", "\\\\")[:120]
    func_name = python_safe(cmd_name)

    # Collision-free Click flags + Python identifiers. Wire names are unchanged.
    rpath, rquery = resolve_parameter_names(method, path_params, query_params, path)
    destructive = is_destructive_operation(method, path)

    lines = []

    # Build decorator chain
    lines.append(f'@group.command("{cmd_name}")')

    # Path params as Click arguments
    # Click lowercases argument names when passing as kwargs, so we must
    # use lowercase names everywhere to avoid TypeError mismatches.
    for p in rpath:
        lines.append(f'@click.argument("{p["dest"]}")')

    # Query params as Click options
    for q in rquery:
        type_map = {"int": "int", "bool": "bool", "str": "str"}
        click_type = type_map.get(q["type"], "str")
        pdesc, pname = q["desc"], q["spec_name"]
        help_str = pdesc.replace('"', '\\"').replace('\n', ' ').replace('\r', '')[:80] if pdesc else pname
        if q["flag"] != f"--{pname}":
            # Flag renamed to avoid colliding with one the command already owns
            # (e.g. a spec param named `confirm` on a DELETE). The query string
            # still carries the spec name — say so in the help text.
            help_str = f"[sends {pname}] {help_str}"[:80]
        # Enforce required=True when OpenAPI spec says required and no default value
        if q["required"] and q["default"] is None:
            lines.append(f'@click.option("{q["flag"]}", "{q["dest"]}", type={click_type}, required=True, help="{help_str}")')
        else:
            pdefault = q["default"]
            default_str = f'"{pdefault}"' if isinstance(pdefault, str) else str(pdefault) if pdefault is not None else "None"
            lines.append(f'@click.option("{q["flag"]}", "{q["dest"]}", type={click_type}, default={default_str}, help="{help_str}")')

    # Request body as --data JSON option
    if has_body:
        lines.append('@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")')
        lines.append('@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")')

    # Output format/query overrides (allow per-command -f/-q)
    lines.append('@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)')
    lines.append('@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)')

    # Confirm for destructive ops — every DELETE, plus any verb whose path names
    # a destructive action (bulk deletes over POST, decommission over PUT, ...).
    if destructive:
        lines.append('@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")')

    lines.append("@pass_context")

    # Function signature
    sig_parts = ["ctx"]
    sig_parts.extend(p["dest"] for p in rpath)
    sig_parts.extend(q["dest"] for q in rquery)
    if has_body:
        sig_parts.extend(["body_data", "body_file"])
    sig_parts.extend(["cmd_fmt", "cmd_query"])
    if destructive:
        sig_parts.append("confirm")

    lines.append(f'def cmd_{func_name}({", ".join(sig_parts)}):')
    lines.append(f'    """{summary}"""')
    lines.append('    if cmd_fmt:')
    lines.append('        ctx.format = cmd_fmt')
    lines.append('    if cmd_query:')
    lines.append('        ctx.query = cmd_query')

    # Destructive-operation confirmation
    if destructive:
        lines.append('    if not confirm:')
        lines.append('        click.echo("Use --confirm to execute this destructive operation.", err=True)')
        lines.append('        raise SystemExit(1)')

    # Build the endpoint path with substitutions
    endpoint = path
    for p in rpath:
        endpoint = endpoint.replace("{" + p["spec_name"] + "}", f'{{{p["dest"]}}}')
    lines.append(f'    endpoint = f"{endpoint}"')

    # Build query params dict — keyed by the SPEC name, not the Python dest,
    # so a renamed identifier still sends the parameter the API expects.
    if rquery:
        lines.append("    params = {}")
        for q in rquery:
            lines.append(f'    if {q["dest"]} is not None:')
            lines.append(f'        params["{q["spec_name"]}"] = {q["dest"]}')
    else:
        lines.append("    params = None")

    # Handle request body
    if has_body:
        lines.append("    body = None")
        lines.append("    if body_file:")
        lines.append("        import json as _json")
        lines.append("        with open(body_file) as f:")
        lines.append("            body = _json.load(f)")
        lines.append("    elif body_data:")
        lines.append("        import json as _json")
        lines.append("        body = _json.loads(body_data)")

    # Make the API call
    lines.append("    client = ctx.ensure_client()")
    lines.append("    try:")
    method_lower = method.lower()
    if method_lower == "get":
        if is_ndjson:
            lines.append("        result = client.get_ndjson(endpoint, params=params)")
        else:
            lines.append("        result = client.get(endpoint, params=params)")
    elif method_lower == "post":
        if has_body:
            lines.append("        result = client.post(endpoint, data=body, params=params)")
        else:
            lines.append("        result = client.post(endpoint, params=params)")
    elif method_lower == "put":
        if has_body:
            lines.append("        result = client.put(endpoint, data=body, params=params)")
        else:
            lines.append("        result = client.put(endpoint, params=params)")
    elif method_lower == "patch":
        if has_body:
            lines.append("        result = client.patch(endpoint, data=body, params=params)")
        else:
            lines.append("        result = client.patch(endpoint, params=params)")
    elif method_lower == "delete":
        if has_body:
            lines.append("        result = client.delete(endpoint, params=params, data=body)")
        else:
            lines.append("        result = client.delete(endpoint, params=params)")

    lines.append("    except Exception as e:")
    lines.append('        click.echo(f"Error: {e}", err=True)')
    lines.append("        raise SystemExit(1)")
    lines.append("    render(result, ctx.format, ctx.query)")

    return "\n".join(lines)


def dedupe_command_names(commands: list) -> list:
    """Resolve command-name collisions within a group.

    On the first collision, append `-<method>`; if that also collides (3-way or
    N-way collision), append `-<method>-<n>` with a counter starting at 2. Every
    emitted name is recorded so downstream collisions are also detected.

    Shared with tools/spec_diff.py so the diff reports the command name the
    generator will actually emit, not the pre-dedup candidate.
    """
    seen_names = set()
    deduped = []
    for method, path, op, cmd_name in commands:
        if cmd_name in seen_names:
            candidate = f"{cmd_name}-{method.lower()}"
            counter = 2
            while candidate in seen_names:
                candidate = f"{cmd_name}-{method.lower()}-{counter}"
                counter += 1
            cmd_name = candidate
        seen_names.add(cmd_name)
        deduped.append((method, path, op, cmd_name))
    return deduped


def generate_module(group_name: str, commands: list) -> str:
    """Generate a full Python module for a command group."""
    desc = GROUP_DESCRIPTIONS.get(group_name, f"{group_name} commands")

    header = f'''"""
{desc}

Auto-generated from the Elisity CCC OpenAPI specification.
"""

import click

from elisity_cli.context import CliContext, pass_context
from elisity_cli.output import render


@click.group("{group_name}")
@pass_context
def group(ctx):
    """{desc}"""
    pass

'''

    deduped_commands = dedupe_command_names(commands)

    cmd_blocks = []
    for method, path, op, cmd_name in deduped_commands:
        try:
            block = generate_command(method, path, op, cmd_name)
            cmd_blocks.append(block)
        except Exception as e:
            cmd_blocks.append(f"# SKIPPED: {cmd_name} — {e}")

    return header + "\n\n".join(cmd_blocks) + "\n"


HTTP_METHODS = ("get", "post", "put", "delete", "patch")


def resolve_spec_path(cli_arg: str = None) -> str:
    """Resolve the OpenAPI spec path: --spec > $ELISITY_API_SPEC > default."""
    if cli_arg:
        return cli_arg
    env_value = os.environ.get(SPEC_PATH_ENV_VAR)
    if env_value:
        return env_value
    return DEFAULT_SPEC_PATH


def load_spec(spec_path: str) -> dict:
    """Load an OpenAPI spec, failing with an actionable message."""
    try:
        with open(spec_path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(
            f"ERROR: OpenAPI spec not found at {spec_path}\n"
            f"Pass --spec <path> or set {SPEC_PATH_ENV_VAR}."
        )
    except json.JSONDecodeError as e:
        raise SystemExit(f"ERROR: {spec_path} is not valid JSON — {e}")


def resolve_group(tags: list, path: str) -> tuple:
    """Map an operation to a CLI group.

    Returns (group_name, matched_by) where matched_by is "tag" when a tag hit
    TAG_TO_GROUP and "path-prefix" when the fallback was used. The path-prefix
    fallback means the tag is unmapped and probably needs a human decision —
    spec_diff.py surfaces those separately.
    """
    for tag in tags:
        if tag in TAG_TO_GROUP:
            return TAG_TO_GROUP[tag], "tag"

    # Default assignment by path prefix
    if "/topology/" in path:
        return "topology", "path-prefix"
    if "/policy/" in path:
        return "policy", "path-prefix"
    if "/identity-graph/" in path:
        return "devices", "path-prefix"
    if "/ad-connector-service/" in path:
        return "ad", "path-prefix"
    if "/flows/" in path or "/nflowsearch/" in path:
        return "flows", "path-prefix"
    if "/state-sync/" in path:
        return "system", "path-prefix"
    return "system", "path-prefix"


def iter_operations(spec: dict):
    """Yield (path, method, op, tags, op_id) for every HTTP operation in a spec.

    This is the single source of truth for "what counts as an operation" —
    generate_commands.py and tools/spec_diff.py both use it so their counts
    can never disagree.
    """
    for path, ops in (spec.get("paths") or {}).items():
        if not isinstance(ops, dict):
            continue
        for method, op in ops.items():
            if method not in HTTP_METHODS:
                continue
            if not isinstance(op, dict):
                continue
            tags = op.get("tags") or ["untagged"]
            op_id = op.get("operationId", "")
            yield path, method, op, tags, op_id


def build_groups(spec: dict) -> tuple:
    """Bucket every spec operation into its CLI group.

    Returns (groups, unmapped) where groups maps group_name ->
    [(method, path, op, cmd_name)] and unmapped lists the (tags, method, path)
    triples that fell through to the path-prefix fallback.
    """
    groups = defaultdict(list)
    unmapped = []

    for path, method, op, tags, op_id in iter_operations(spec):
        group_name, matched_by = resolve_group(tags, path)
        if matched_by == "path-prefix":
            unmapped.append((tags, method, path))
        if (method, path) in OMITTED_OPERATIONS:
            continue
        cmd_name = make_command_name(method, op_id, path, tags[0])
        groups[group_name].append((method, path, op, cmd_name))

    return groups, unmapped


def unmapped_tags(spec: dict) -> dict:
    """Tags present in the spec that TAG_TO_GROUP does not resolve.

    Returns {tag: operation_count}, counted per TAG and independent of its
    siblings.

    This used to skip any operation carrying at least one mapped tag, on the
    reasoning that resolve_group() takes the first tag that hits so the routing
    is still "correct". It is not: first-match means whichever mapped tag comes
    first wins, and that may have nothing to do with the new tag's meaning. A
    26.7 operation tagged ["Brand New Flow Tag", "Device"] routes to `policy` on
    the incidental Device tag even though its path is /api/flows/v1/..., and the
    guard never says a word. 21 operations in 26.7 already carry two tags (20 in
    26.3), so CCC adding a third to one of them is exactly this input.

    The whole point of the guard is that a new CCC tag is a human decision — a
    tag that is invisible because it shares an operation with a known one is
    the same silent misrouting the guard exists to prevent, just harder to see.
    Sibling tags do not make a new tag decided.

    resolve_group()'s first-match behaviour is deliberately left alone, so
    fixing the guard re-routes nothing; it only makes the decision visible.
    """
    counts = defaultdict(int)
    for path, method, op, tags, op_id in iter_operations(spec):
        for t in tags:
            if t not in TAG_TO_GROUP:
                counts[t] += 1
    return dict(counts)


def assert_every_tag_mapped(spec: dict) -> None:
    """Fail generation if any spec tag has no TAG_TO_GROUP entry.

    The path-prefix fallback in resolve_group() will happily absorb an unmapped
    tag into a plausible-looking group, so an unmapped tag is not a loud error —
    it is a silent, wide misrouting. CCC 26.7 renamed 16 tags; six
    `Connectors Configurations` operations moved from `connectors` to `devices`
    that way, and the command count stayed plausible throughout. Refusing to
    generate is the only thing that makes this class of drift visible before it
    ships.
    """
    unmapped = unmapped_tags(spec)
    if not unmapped:
        return
    lines = [
        f"ERROR: {len(unmapped)} spec tag(s) have no TAG_TO_GROUP mapping, "
        f"covering {sum(unmapped.values())} operation(s).",
        "",
        "Each would be silently routed by the path-prefix fallback, which is how",
        "commands quietly change group across a spec bump. Add each tag to",
        "TAG_TO_GROUP in generate_commands.py, then regenerate:",
        "",
    ]
    for tag, count in sorted(unmapped.items(), key=lambda kv: (-kv[1], kv[0])):
        would_be, _ = resolve_group([tag], _sample_path_for_tag(spec, tag))
        lines.append(f'    "{tag}": "{would_be}",   # {count} operation(s) — '
                     f"fallback would pick {would_be}")
    raise SystemExit("\n".join(lines))


def assert_overrides_emitted(groups: dict) -> None:
    """Fail generation on any dedupe collision that involves an override name.

    dedupe_command_names() resolves a collision by suffixing whichever command
    comes second in spec order. If the override comes second, it ships as
    `<name>-post`; if it comes first, the OTHER command — possibly a shipped
    one — is pushed to the suffix instead, which is exactly what 26.9 did to
    `devices attach`. Both directions fail here: any command whose name dedupe
    changed, where the name it wanted is an override name in its group.
    Overrides absent from the spec are ignored, so one map serves every spec
    version.
    """
    wrong = []
    for group_name, commands in groups.items():
        override_names = {
            COMMAND_NAME_OVERRIDES[(m.upper(), p)]
            for m, p, _op, _name in commands
            if (m.upper(), p) in COMMAND_NAME_OVERRIDES
        }
        for (method, path, _op, wanted), (_m, _p, _o, emitted) in zip(
                commands, dedupe_command_names(commands)):
            if wanted in override_names and emitted != wanted:
                kind = ("override" if COMMAND_NAME_OVERRIDES.get((method.upper(), path)) == wanted
                        else "command displaced by an override")
                wrong.append(f"    {method.upper()} {path}: {kind} '{wanted}' "
                             f"would be emitted as '{group_name} {emitted}'")
    if wrong:
        raise SystemExit(
            "ERROR: command-name override(s) collide with another command in the "
            "same group, so dedupe would rename them:\n" + "\n".join(wrong)
            + "\nPick a unique name in COMMAND_NAME_OVERRIDES."
        )


def assert_omitted_operations_replaced(spec: dict) -> None:
    """Fail generation if an omitted operation's replacement is missing.

    OMITTED_OPERATIONS drops an operation because another one replaces it. A
    spec that has the omitted operation but not the replacement would lose the
    command outright — the published 26.9 spec has the device PUT and no PATCH,
    so `devices update-device` would vanish while the count still looked
    plausible.
    """
    paths = spec.get("paths") or {}
    missing = [
        (omitted, replacement)
        for omitted, replacement in OMITTED_OPERATIONS.items()
        if omitted[0] in (paths.get(omitted[1]) or {})
        and replacement[0] not in (paths.get(replacement[1]) or {})
    ]
    if missing:
        overlays = sorted(p.name for p in SPEC_OVERLAY_DIR.glob("*.json"))
        raise SystemExit(
            "ERROR: the spec has an operation the CLI omits, but not the one that "
            "replaces it:\n"
            + "\n".join(f"    {o[0].upper()} {o[1]} is omitted in favour of "
                        f"{r[0].upper()} {r[1]}, which this spec does not declare"
                        for o, r in missing)
            + "\nApply the spec overlay for this release with --overlay "
            f"(available in {SPEC_OVERLAY_DIR.name}/: {', '.join(overlays) or 'none'})."
        )


def load_overlay(overlay_path) -> dict:
    """Load a spec overlay, failing with an actionable message."""
    try:
        with open(overlay_path) as f:
            overlay = json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"ERROR: spec overlay not found at {overlay_path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"ERROR: {overlay_path} is not valid JSON — {e}")
    if not overlay.get("provenance") or not isinstance(overlay.get("operations"), list):
        raise SystemExit(f"ERROR: {overlay_path} needs a 'provenance' and an 'operations' list")
    for i, entry in enumerate(overlay["operations"]):
        missing = [k for k in ("path", "method", "cloneFrom") if not entry.get(k)]
        if missing:
            raise SystemExit(f"ERROR: {overlay_path} operation #{i} is missing {', '.join(missing)}")
    return overlay


def apply_overlays(spec: dict, overlay_paths) -> tuple:
    """Return (spec with the overlays' operations added, notes).

    Each overlay operation is `{"path", "method", "cloneFrom", "set"}`: the
    operation `cloneFrom` at the same path is copied, `set` replaces top-level
    keys of the copy, and the result is added as `method`. The copy carries
    `x-elisity-overlay` with the overlay's provenance. The input spec is not
    modified.

    An operation the spec already declares is left alone: the published spec
    has caught up and wins over the overlay. An overlay whose `cloneFrom`
    operation is missing fails generation — it no longer fits the spec.
    """
    if not overlay_paths:
        return spec, []
    spec = copy.deepcopy(spec)
    paths = spec.setdefault("paths", {})
    notes = []
    for overlay_path in overlay_paths:
        overlay = load_overlay(overlay_path)
        for entry in overlay["operations"]:
            path, method = entry["path"], entry["method"].lower()
            source = entry["cloneFrom"].lower()
            ops = paths.get(path) or {}
            if method in ops:
                notes.append(f"overlay {Path(overlay_path).name}: {method.upper()} {path} "
                             "is already in the spec; the spec's definition is used")
                continue
            if source not in ops:
                raise SystemExit(
                    f"ERROR: overlay {overlay_path} clones {source.upper()} {path}, "
                    "which this spec does not declare. The overlay does not fit this spec."
                )
            op = copy.deepcopy(ops[source])
            op.update(copy.deepcopy(entry.get("set") or {}))
            op["x-elisity-overlay"] = overlay["provenance"]
            # Inserted right after the operation it was cloned from, so command
            # order in the generated module matches a spec that declares it.
            paths[path] = {}
            for m, o in ops.items():
                paths[path][m] = o
                if m == source:
                    paths[path][method] = op
            notes.append(f"overlay {Path(overlay_path).name}: added {method.upper()} {path} "
                         f"({overlay['provenance']})")
    return spec, notes


def _sample_path_for_tag(spec: dict, tag: str) -> str:
    """First path carrying `tag`, so the guard can show the fallback's choice."""
    for path, method, op, tags, op_id in iter_operations(spec):
        if tag in tags:
            return path
    return ""


def render_init_module(generated_groups) -> str:
    """Render commands/__init__.py, keeping hand-coded groups registered."""
    all_groups = sorted(set(generated_groups) | set(HANDCODED_GROUPS))
    lines = [
        '"""Command groups.',
        "",
        "Most groups are auto-generated from the CCC OpenAPI spec by",
        "`generate_commands.py`. `reporting` is hand-coded because the CCC reporting",
        "API at /api/reporting/v1/data is GraphQL and isn't in the OpenAPI spec.",
        "`glossary` is hand-coded — it's a CLI-native group (no remote API surface)",
        "that maps Elisity UI terminology to CLI commands.",
        '"""',
        "",
        "COMMAND_GROUPS = [",
    ]
    lines.extend(f'    "{gn}",' for gn in all_groups)
    lines.append("]")
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate Click CLI command modules from the CCC OpenAPI spec."
    )
    parser.add_argument(
        "--spec",
        default=None,
        help=f"Path to the OpenAPI JSON spec (default: ${SPEC_PATH_ENV_VAR}, "
             f"then {DEFAULT_SPEC_PATH})",
    )
    parser.add_argument(
        "--overlay",
        action="append",
        default=[],
        metavar="PATH",
        help="Spec overlay to apply before generating (repeatable). CCC 26.9 needs "
             f"{SPEC_OVERLAY_DIR.name}/ccc-26.9-hotpatch-device-patch.json",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help=f"Directory to write command modules into (default: {DEFAULT_OUTPUT_DIR})",
    )
    args = parser.parse_args(argv)

    spec_path = resolve_spec_path(args.spec)
    output_dir = Path(args.output_dir) if args.output_dir else DEFAULT_OUTPUT_DIR

    print(f"Spec:   {spec_path}")
    print(f"Output: {output_dir}")

    spec, overlay_notes = apply_overlays(load_spec(spec_path), args.overlay)
    for note in overlay_notes:
        print(f"Spec overlay: {note}")

    # Refuse to generate from a spec with unmapped tags — see the guard's
    # docstring. Checked before build_groups() so the failure names the tags
    # rather than emitting quietly-misrouted modules.
    assert_every_tag_mapped(spec)
    assert_omitted_operations_replaced(spec)

    groups, unmapped = build_groups(spec)
    assert_overrides_emitted(groups)

    # A spec tag must never be allowed to overwrite a hand-coded module.
    collisions = sorted(set(groups) & set(HANDCODED_GROUPS))
    if collisions:
        raise SystemExit(
            "ERROR: spec operations were mapped to hand-coded group(s) "
            f"{', '.join(collisions)}. Regenerating would overwrite hand-written "
            "commands. Fix TAG_TO_GROUP (or HANDCODED_GROUPS) before regenerating."
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "__init__.py", "w") as f:
        f.write(render_init_module(groups.keys()))

    # Write each group module
    stats = {}
    skipped = []
    for group_name, commands in sorted(groups.items()):
        module_code = generate_module(group_name, commands)
        module_path = output_dir / f"{group_name}.py"
        with open(module_path, "w") as f:
            f.write(module_code)
        stats[group_name] = len(commands)
        module_skips = re.findall(r"^# SKIPPED: (.+)$", module_code, re.MULTILINE)
        skipped.extend(f"{group_name}: {s}" for s in module_skips)
        print(f"  Generated {group_name}.py — {len(commands)} commands")

    print(f"\nTotal: {sum(stats.values())} commands across {len(stats)} groups")
    print(f"Hand-coded groups preserved: {', '.join(sorted(HANDCODED_GROUPS))}")
    if unmapped:
        print(f"Note: {len(unmapped)} endpoints mapped by path prefix (no direct tag match)")

    if skipped:
        # A skipped command is a silently missing command. Never let this pass quietly.
        print(f"\nERROR: {len(skipped)} command(s) failed to generate:", file=sys.stderr)
        for s in skipped:
            print(f"  - {s}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
