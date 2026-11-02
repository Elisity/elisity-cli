# Elisity Glossary — UI Terms and CLI Recipes

This appendix is the human-readable counterpart to the `elisity glossary` command
group. Each section covers one canonical Elisity term: the synonyms a user might
say in the UI, the official context, and the CLI commands that implement the
concept.

The entries here follow the glossary data that ships with the CLI and reflect
the 517-command CLI surface. Synonyms are derived from the Elisity product
glossary — if a term you expect is missing, run
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

# Activate a simulation policy: set monitorMode to MONITOR_AND_ENFORCE
# (read --help first — requires --body; send the policy's other fields back unchanged)
elisity policy update-policy --help
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

### Custom Application

> "application definition", "custom app", "app definition"

**Context:** User-defined application definition referenced by policy rules,
added as a first-class surface in CCC 26.7. Each application owns one or more
definitions.

**CLI recipes:**

```bash
# List custom applications
elisity policy list-applications

# Create a custom application (state-changing — get human approval first)
elisity policy create-application --body '{...}'
```

### Vendor

> "device vendor", "manufacturer", "vendor record"

**Context:** Vendor record, added in CCC 26.7. Used to classify devices for
policy matching.

**CLI recipes:**

```bash
# List all vendors
elisity policy list-vendors

# Get a vendor by ID
elisity policy get-vendor <VENDOR_ID>

# Create a vendor (state-changing — get human approval first)
elisity policy create-vendor --body '{...}'
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

# Per-site enforcement score (CCC 26.7 removed the per-policy-set score,
# so this is the narrowest score left)
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

> **Removed in CCC 26.7.** `policy get-enforcement-score`,
> `policy get-enforcement-score-weight-settings` and
> `reporting diagnose-low-score` are gone. For the score, use the commands
> above; for the low-score diagnosis, use the two-step recipe above. For the
> weighting settings, `policy get-coverage-weight-settings` is the closest
> command; confirm it carries the Active-vs-Simulation ratio before relying
> on it.

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

### Workload Distribution Zone

> "workload DZ", "workload zone", "cloud distribution zone"

**Context:** Distribution Zone that holds cloud workloads discovered through a
workload-discovery connector endpoint, added in CCC 26.9. Unlike a network
Distribution Zone it cannot be assigned to a VEN, VE or VE Group, so
`topology get-all-distribution-zones` leaves it out unless asked.

**CLI recipes:**

```bash
# List Workload Distribution Zones (optional --id matches the zone's numericId or UUID)
elisity topology list-workload-distribution-zones

# Check whether a Workload Distribution Zone is in use (do this before deleting one)
elisity topology get-workload-distribution-zone-usage <ZONE_ID>

# Include Workload DZs in the full Distribution Zone listing
elisity topology get-all-distribution-zones --includeWorkload true
```

### Maintenance Mode

> "maintenance", "maintenance window", "ve maintenance"

**Context:** Virtual Edge state introduced in CCC 26.7 that suspends normal
operation for servicing. Can be applied to a single VE or to a batch of VEs in a
VE group.

**CLI recipes:**

```bash
# Enable maintenance mode on a Virtual Edge
# (state-changing on live infrastructure — get human approval first)
elisity topology enable-maintenance <VIRTUAL_EDGE_ID>

# Disable maintenance mode on a Virtual Edge
elisity topology disable-maintenance <VIRTUAL_EDGE_ID>

# Enable maintenance on a batch of Virtual Edges in a VE group (read --help for the body shape)
elisity topology enable-maintenance-for-group <VE_GROUP_ID> --body '{...}'
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

### Cloud Workload

> "workload", "cloud asset", "ec2 instance", "cloud instance", "vm workload"

**Context:** Cloud compute asset tracked in the IdentityGraph alongside devices,
added in CCC 26.7. Workloads carry the same STATIC attribute layer as devices.

**CLI recipes:**

```bash
# List workloads (read-only despite the POST; takes a filter body like get-devices-view)
elisity devices get-workloads-view

# Aggregate workload counts, grouped by attribute
elisity devices get-workload-aggregate

# Get a single workload by ID
elisity devices get-workload-details <WORKLOAD_ID>
```

### Workload Discovery

> "cloud discovery", "aws discovery", "ec2 discovery", "cloud onboarding",
> "azure discovery", "azure workload discovery", "azure vm discovery"

**Context:** Flow that discovers cloud workloads through a cloud connector. CCC
26.7 shipped AWS: onboarding mints an external ID and a trust policy for an IAM
role, then discovery enumerates EC2 instances. CCC 26.9 adds Azure: the
onboarding wizard validates the connection, permissions and region filter, then
previews the subscriptions, resource groups and VM count a scope resolves to,
both before the connector exists (`*-pre-creation`) and for an existing endpoint
(`*-existing`).

**CLI recipes:**

```bash
# Get the IAM trust policy JSON to apply in AWS (read-only; read --help for the body shape)
elisity devices generate-trust-policy --body '{...}'

# Discover EC2 workloads for an existing connector
# (state-changing: triggers real discovery work — get human approval first)
elisity devices discover-ec2workloads <CONNECTOR_ID>

# List the Azure (ARM) permissions the connector needs, by tier
elisity devices list-azure-required-permissions

# Preview what an Azure scope resolves to before creating the connector (read-only)
elisity devices preview-azure-scope-pre-creation --body '{...}'
```

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

## System domain

### Snapshot

> "report snapshot", "scheduled report", "snapshot schedule", "pdf report",
> "snapshot markdown", "snapshot evidence"

**Context:** Point-in-time reporting artifact introduced in CCC 26.7, optionally
produced on a schedule. Retrievable as PDF, and from CCC 26.9 also as Markdown
and as a JSON evidence package. The CLI groups these commands under `system`.

**CLI recipes:**

```bash
# List snapshots
elisity system search-snapshots

# Download a snapshot as PDF (renamed from retrieve-snapshot-image in CCC 26.9)
elisity system retrieve-snapshot-pdf <SNAPSHOT_ID>

# Get a snapshot as Markdown (CCC 26.9+)
elisity system retrieve-snapshot-markdown <SNAPSHOT_ID>

# Get a snapshot's JSON evidence package (CCC 26.9+)
elisity system retrieve-snapshot-evidence <SNAPSHOT_ID>

# Pause a snapshot schedule (state-changing — stops future scheduled runs)
elisity system pause-snapshot-schedule <SCHEDULE_ID>
```

---

## Connectors domain

### Tanium Sensor Mapping

> "tanium sensor", "tanium mapping", "sensor mapping", "tanium sensor catalog"

**Context:** Mapping of a Tanium sensor (and one of its registered parameter
combinations) to a device attribute on the Tanium connector, added in CCC 26.9.
The CLI exposes the reads behind the mapping editor: the live sensor catalog,
one sensor's detail, and a probe that shows what a draft mapping would return
for live devices.

**CLI recipes:**

```bash
# Fetch the Tanium sensor catalog (read-only despite the POST; a live read from
# Tanium — the body carries the connector endpoint block, including credentials)
elisity connectors fetch-tanium-sensor-catalog --harvested_only true --body '{...}'

# Look up one Tanium sensor by exact name (only harvested parameter
# combinations return data)
elisity connectors fetch-tanium-sensor-detail --body '{...}'

# Probe a draft sensor mapping against live devices (read-only; reports per
# device what the attribute would hold and never affects connector health)
elisity connectors probe-tanium-sensor-mapping --body '{...}'
```

---

## AD domain

### AD Group

> "active directory group", "ad groups", "ad group enablement",
> "enable ad groups", "ad group count"

**Context:** Active Directory group as listed by the AD connector. CCC 26.9
adds a groups view with counts and member listings, per-group enable/disable
(one row, or many through Bulk Actions), an 'enable all groups by default'
setting for newly discovered groups, and an XLSX export.

**CLI recipes:**

```bash
# Count AD groups
elisity ad get-groups-count

# List AD groups (read-only despite the POST; filter with --globalFilter)
elisity ad get-groups-view --size 50

# List the users that are direct members of a group (get-group-devices for devices)
elisity ad get-group-users <GROUP_ID>

# Read the 'enable all groups by default' setting
elisity ad get-groups-default-enabled

# Enable or disable groups (state-changing — get human approval first)
elisity ad set-groups-enabled --body '{"ids": [<GROUP_ID>], "enabled": true}'
```

> `ad set-groups-default-enabled` changes the default for new groups. It is
> destructive and requires `--confirm`.

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

The 28 canonical terms originate from
the Elisity product glossary maintained alongside the product.
The glossary ships with the CLI, together with the synonym → CLI command
translation, so `elisity glossary list` shows every term for the version you
have installed.

If a glossary entry has no CLI command (`elisity glossary search` shows an
empty `cli_recipes` list and the `terminology-only` domain), that's deliberate:
we do not invent commands. If you find a recipe that *should* exist, report it
to Elisity Support (support@elisity.com).
