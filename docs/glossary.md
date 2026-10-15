# Elisity Glossary — UI Terms and CLI Recipes

This appendix is the human-readable counterpart to the `elisity glossary` command
group. Each section covers one canonical Elisity term: the synonyms a user might
say in the UI, the official context, and the CLI commands that implement the
concept.

The data here is generated from `data/ui-to-cli-mapping.json` and reflects the
658-command CLI surface. Synonyms are derived from the upstream
`Elisity/ccc:product-glossary.json` — if a term you expect is missing, run
`elisity glossary list` to see the full set.

For an AI-agent operating contract, see [AGENTS.md](AGENTS.md). For runtime
lookup, use `elisity glossary search "<phrase>"` or `elisity glossary explain
"<phrase>"`.

---

## Policy domain

### Simulation

> "monitor mode", "passive mode", "audit mode", "dry run", "simulated"

**Context:** Policy enforcement state where traffic is logged but not blocked.
UI actions: 'Save as Simulation'. Enum: `MONITOR_ONLY`.

**CLI recipes:**

```bash
# Count policies currently in Simulation (monitor-only) mode
elisity reporting get-policy-count --monitor-mode MONITOR_ONLY

# Traffic that hit Simulation policies over the last 24h
elisity reporting get-traffic-count --policy-status SIMULATION

# Filter the full policy stream to only Simulation policies
elisity policy get-all-policies-as-nd-json -q '[?monitorMode==`MONITOR_ONLY`]'
```

### Active

> "enforcement mode", "inline mode", "blocking mode", "enforce mode"

**Context:** Policy enforcement state where traffic is actively permitted/denied.
UI actions: 'Activate Policy', 'Save as Active'. Enum: `MONITOR_AND_ENFORCE`.

**CLI recipes:**

```bash
# Count policies currently in Active (monitor-and-enforce) mode
elisity reporting get-policy-count --monitor-mode MONITOR_AND_ENFORCE

# Traffic that hit Active policies over the last 24h
elisity reporting get-traffic-count --policy-status ACTIVE

# Filter the full policy stream to only Active policies
elisity policy get-all-policies-as-nd-json -q '[?monitorMode==`MONITOR_AND_ENFORCE`]'

# Activate a simulation policy (read --help first — requires --body)
elisity policy change-status --help
```

### Independent Control

> "external monitoring", "third-party enforcement", "external mode"

**Context:** Policy mode where enforcement is handled by an external system.
Enum: `MONITOR_EXTERNAL`.

**CLI recipes:**

```bash
# Count policies in Independent Control mode
elisity reporting get-policy-count --monitor-mode MONITOR_EXTERNAL

# Filter the policy stream to Independent Control policies
elisity policy get-all-policies-as-nd-json -q '[?monitorMode==`MONITOR_EXTERNAL`]'
```

### Policy Group

> "security group", "endpoint group", "segment", "zone", "PG"

**Context:** Collection of devices receiving the same security treatment. Can be
Dynamic or Static, Global or Local.

**CLI recipes:**

```bash
# List all policy groups (ndjson — one per line)
elisity policy get-policy-groups-json

# Get a single policy group with full detail
elisity policy get-policy-group-by-id <POLICY_GROUP_ID>

# List devices currently in a policy group
elisity policy get-policy-group-devices <POLICY_GROUP_ID>

# Count policy groups (local vs global)
elisity reporting get-policy-groups-count --local true
```

### Security Profile

> "ACL", "access control list", "firewall rule", "rule set"

**Context:** Reusable L4 traffic filtering template defining protocol, ports, and
permit/deny actions.

**CLI recipes:**

```bash
# List all security profiles
elisity policy get-all-security-profiles-as-nd-json

# Read a single security profile
elisity policy read-security-profile <SECURITY_PROFILE_ID>

# Find every policy referencing a given security profile
elisity policy get-policies-for-security-profile <SECURITY_PROFILE_ID>
```

### Policy Matrix

> "rule table", "policy table", "access matrix", "segmentation matrix"

**Context:** Visual PG-to-PG grid. Colors: Allow (green), Deny (red), Custom
(blue), No Policy (gray).

**CLI recipes:**

```bash
# Get the full policy matrix as JSON
elisity policy get-matrix

# Stream every policy in matrix form
elisity policy get-all-policies-as-nd-json
```

### Unassigned (Policy Group)

> "default group", "ungrouped", "uncategorized", "catch-all", "unassigned PG"

**Context:** System Policy Group where devices land when they don't match any
Dynamic or Static Policy Group.

**CLI recipes:**

```bash
# Find the Unassigned PG (by canonical name)
elisity policy get-policy-groups-json -q '[?name==`Unassigned`]'

# List every device in the Unassigned PG (use the id from above)
elisity policy get-policy-group-devices <UNASSIGNED_PG_ID>
```

---

## Reporting domain

### Policy Enforcement Score

> "security score", "risk score", "compliance score", "posture score",
> "enforcement score", "Zero Trust score", "policy deployment score"

**Context:** 0-100 metric for policy coverage quality. Also referred to as Policy
Deployment Score. Active (enforced) policies count fully; Simulation
(MONITOR_ONLY) policies contribute only a fraction of that weight (the ratio is
tenant-configurable and CCC 26.7 replaced the endpoint that read it — see the
note below — so don't assume a fixed number).

**A low or zero score has more than one cause — don't assume "simulation".** A
group scoring 0 may have *no policy at all* (nothing to enforce), only
*simulation* policies (activate them), or *active* policies that don't cover its
real traffic (reclassify devices / add rules). These need opposite fixes, so
recommending "activate the simulation policies" for a no-policy group is wrong.
Tell them apart before acting by reading the `monitorMode` of the policies that
reference the group (recipe below).

**CLI recipes:**

```bash
# Tenant-wide headline number (the CCC dashboard "Zero Trust score" tile)
elisity reporting get-aggregate-enforcement-score

# Per-site enforcement score (CCC 26.7 removed the per-policy-set field
# policyMetrics.policySetEnforcementScore, so this is the narrowest score left)
elisity reporting get-site-kpis --site <SITE>

# Per-PG device + policy coverage breakdown
elisity reporting get-zero-trust-metrics

# WHY a group scores low: no-policy vs simulation vs uncovered.
# Step 1 gives you the policyGroupId; step 2 gives you the cause.
elisity -f table \
  -q '[].{pg: policyGroupName, pgId: policyGroupId, devCov: policyDeploymentMetrics.deviceCoverage}' \
  reporting get-zero-trust-metrics
elisity -f table \
  -q '[?srcId==`PG_ID` || dstId==`PG_ID`].{name: name, mode: monitorMode, disabled: disabled}' \
  policy get-all-policies-as-nd-json
#   no rows = no policy | all MONITOR_ONLY = simulation | any
#   MONITOR_AND_ENFORCE = active but uncovered
```

> **Removed in CCC 26.7.** `policy get-enforcement-score` and
> `policy get-enforcement-score-weight-settings` are gone from the spec (both
> `/api/policy/v1/enforcement-score/*` paths were dropped), and
> `reporting diagnose-low-score` — which did the two-step above in one call —
> was removed with them because CCC 26.7 deleted the two coverage fields it
> filtered on. For the weighting config, `policy get-coverage-weight-settings`
> (`/api/policy/v1/coverage/settings`, new in 26.7) is the closest surviving
> surface; confirm it carries the Active-vs-Simulation ratio before relying on
> it — CCC did not document the two as equivalent.

---

## Topology domain

### Virtual Edge (VE)

> "edge gateway", "edge appliance", "SD-WAN edge", "VE"

**Context:** Logical grouping of Virtual Edge Nodes. Software-defined, not a
physical appliance.

**CLI recipes:**

```bash
# Get a single Virtual Edge by id
elisity topology get-virtual-edge-by-id <VIRTUAL_EDGE_ID>

# Count Virtual Edges at the latest snapshot
elisity reporting get-virtual-edges-count

# Export every Virtual Edge to JSON
elisity topology export-virtual-edges
```

### Virtual Edge Node (VEN)

> "network agent", "sensor", "enforcement point", "appliance", "VEN", "switch"

**Context:** Existing switch onboarded as an Elisity enforcement point. No new
hardware required.

**CLI recipes:**

```bash
# List every VEN
elisity topology get-virtual-edge-nodes

# Get a single VEN
elisity topology get-single-ven <VEN_ID>

# VEN counts by model
elisity reporting get-virtual-edge-nodes-count

# Export every VEN
elisity topology export-virtual-edge-nodes
```

### Visibility-Only Virtual Edge Node

> "visibility ven", "visibility only ven", "visibility mode", "monitor-only ven",
> "read-only ven", "passive ven"

**Context:** A VEN deployment mode that monitors and reports network traffic
without enforcing any policies. Used for pre-deployment network discovery,
baselining traffic, and compliance auditing before activating policy enforcement.

**CLI recipes:**

```bash
# Inspect VEN list — filter on the deployment-mode field once you know
# its name on your tenant (it's a per-VEN attribute)
elisity topology get-virtual-edge-nodes

# Single VEN detail (includes the deployment mode)
elisity topology get-single-ven <VEN_ID>

# Traffic from a visibility-only site (no enforcement)
elisity reporting get-traffic-count --kind ALL --site <SITE_NAME>
```

### Distribution Zone

> "network zone", "VLAN", "subnet", "security zone", "broadcast domain", "DZ"

**Context:** Elisity logical enforcement boundary. Can span multiple VLANs.

**CLI recipes:**

```bash
# List every Distribution Zone
elisity topology get-all-distribution-zones

# Get a single DZ
elisity topology get-distribution-zone <DZ_ID>

# Export every DZ
elisity topology export-distribution-zones

# Online devices grouped by DZ
elisity policy get-online-devices-for-distribution-zones
```

---

## Devices domain

### IdentityGraph

> "device inventory", "CMDB", "asset database", "network inventory"

**Context:** Dynamic multi-source identity engine that constructs a holistic view
of every network entity.

**CLI recipes:**

```bash
# Inspect device-attribute layer specs
elisity devices read-all-layer-instances-specification

# Paginated devices view (note nested `pageable` wrapper)
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":50}}'

# Device counts by source connector
elisity reporting get-devices-by-connector

# Tenant-wide online/offline counts (cheaper than paginating get-devices-view)
elisity reporting get-device-count
```

### Security Level (SL1-SL4)

> "priority", "severity", "risk level", "classification level", "SL1", "SL2",
> "SL3", "SL4", "IEC 62443"

**Context:** IEC 62443 aligned criticality. SL1=Low Impact, SL2=Medium, SL3=High,
SL4=Critical.

**CLI recipes:**

```bash
# Discover which device attribute carries Security Level on your tenant
elisity devices read-all-layer-instances-specification

# List the values currently in use for that attribute
elisity devices get-values-for-device-attribute <ATTRIBUTE_NAME>
```

> Security Level is modeled as a device attribute, not a top-level field.
> Per-tenant attribute names vary — confirm via the first command before
> writing filter logic.

---

## Insights domain

### Insights

> "recommendations", "AI suggestions", "analytics", "anomaly detection"

**Context:** ML/LLM engine for device classification, policy group suggestions,
and policy activation recommendations.

**CLI recipes:**

```bash
# All Insights suggestions
elisity insights get-suggestions

# Policy-activation suggestions
elisity insights get-policy-suggestion-list

# Re-run the policy-suggestion pipeline (heavy)
elisity insights recreate-policy-suggestions

# Inspect engine settings
elisity insights get-settings
```

### Adjudication

> "approval", "review", "validation", "triage", "confirmation"

**Context:** Accept/reject workflow for Insights classification recommendations.
Statuses: `PENDING`, `ACCEPTED`, `REJECTED`.

**CLI recipes:**

```bash
# List suggestions awaiting adjudication
elisity insights get-suggestions

# Policy-group classification suggestions (most common adjudication surface)
elisity insights get-policy-group-suggestions

# Accept or reject a suggestion (read --help for the body shape)
elisity insights update-suggestion --help
```

---

## Flows domain

### Traffic Analytics

> "traffic analysis", "flow analysis", "network monitoring", "traffic monitoring",
> "top talkers"

**Context:** CCC feature for analyzing network traffic flows, top talkers, and
policy action breakdowns.

**CLI recipes:**

```bash
# Dashboard summary cards (totals, allowed vs denied)
elisity flows get-dash-board-summary-data

# Raw flow records (CCC 26.7 removed get-latest-data)
elisity flows get-traffic-record

# Top N policy groups by traffic
elisity reporting get-top-policy-groups-by-traffic --kind ALL --top 10

# Top N IPs by denied traffic
elisity reporting get-top-ips-by-traffic --kind DENIED --top 10
```

---

## Terminology-only (no direct CLI surface)

These terms describe product features that don't have a single corresponding
CLI command. They are listed here so users hitting these terms know to broaden
the search rather than chase a non-existent verb.

### Cloud Control Center (CCC)

> "management console", "controller", "dashboard", "management plane", "CCC"

**Context:** Elisity's SaaS management platform.

CCC is the platform the CLI talks to — there is no single CLI command that
represents "CCC". To verify CLI connectivity to a specific CCC tenant use
`elisity auth test`; to inspect the active connection use `elisity config show`.

### Elisity Assistant

> "AI assistant", "chatbot", "copilot", "virtual assistant"

**Context:** The AI-powered chat feature in CCC for network security operations
assistance.

Elisity Assistant is a CCC web-app feature — no direct CLI surface. Agents using
the CLI play a similar role: see [AGENTS.md](AGENTS.md).

---

## Where this data comes from

The 19 canonical terms originate from
`Elisity/ccc:esaas/backend/insights/src/main/resources/assistant/product-glossary.json`.
A pinned copy ships with the CLI at `data/product-glossary.json` (with a
`_source` block tracking the upstream import). The CLI mapping table at
`data/ui-to-cli-mapping.json` adds the synonym → CLI command translation.

Updates flow upstream → CLI repo → wheel package. If a glossary entry is missing
a real CLI command (the `cli_recipes` list is empty and `domain` is
`terminology-only`), that's deliberate: we do not invent commands. If you find
a recipe that *should* exist, open a ticket against `mkorenbaum/elisity-cli`.
