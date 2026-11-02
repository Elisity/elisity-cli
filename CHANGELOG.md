# Changelog

Each release of the Elisity CCC CLI matches a CCC release. The first two numbers of the
wheel version name the CCC release, and the third counts CLI fixes: wheel `26.9.0` carries
the commands for CCC 26.9, and a CLI fix for it would ship as `26.9.1`. Read the section for
the release you upgrade to before you upgrade. A renamed or removed command, or a changed
flag, breaks the scripts that call it.

## 26.9.0 (CCC 26.9)

### `devices update-device` sends PATCH

`elisity devices update-device <id>` now sends a `PATCH`. Fields you leave out, `null`, or
an empty `ip` / `venId` keep their current value, so an attribute-only update no longer
detaches a dynamically attached device. Attributes merge into the target enrichment layer,
and `--target-enrichment-layer` now reaches the request. The `If-Match` precondition and
the required permission are unchanged; the command returns 204.

The command needs a CCC 26.9 tenant that supports the device `PATCH`. On CCC 26.7, and on
26.9 tenants without the latest updates, it fails, most likely with
`405 Method Not Allowed`. Check your tenant's release before you rely on it.

### `ad set-groups-default-enabled` requires `--confirm`

The command resets the "enable all groups by default" setting, so, like the other
destructive commands, it runs only with `--confirm`.

### AD group views send a JSON body

`elisity ad get-groups-view`, `ad get-group-users <id>` and `ad get-group-devices <id>`
send the JSON body `{}` when you give neither `--body` nor `--body-file`; CCC rejects these
requests without a body. Both flags are accepted, and `elisity ad get-groups-view --size 5`
works with no other arguments.

### Install, upgrade and uninstall

[Getting Started](docs/getting-started.md#install-upgrade-and-uninstall) covers install,
upgrade and uninstall with pipx or a virtual environment, on Linux, macOS and Windows.

### Fixes

- **Commands whose response is plain text work.** The CLI asked only for JSON, and CCC
  answered `406 Not Acceptable` for the commands that return plain text (for example
  `policy create`). Plain-text responses print as
  before for other non-JSON responses: `{"raw": "..."}` for a GET, the text itself for
  POST and PUT.
- **Required header parameters are options.** `policy reorder-siblings` takes
  `--if-match`, sent as `If-Match`. It is required; leaving it out is a usage error
  (exit 2) and nothing is sent. Optional `If-Match` / `If-None-Match` headers are not
  exposed yet.
- **Errors show CCC's message.** A 4xx or 5xx prints the status line followed by what CCC
  said, for example `Error: 400 Client Error: Bad Request for url: ... — server message:
  Firewall rules can only be managed for Palo Alto vendors.` Exit codes are unchanged.
- **`elisity --version` prints the release version.** It printed `0.1.0`.
- **`elisity glossary` examples are fixed.** It gives `elisity policy update-policy` with
  `monitorMode` for enforcing a policy, and its `topology enable-maintenance-for-group`
  example passes the VE group ID.

### Removed commands (breaking)

A script that calls one of these commands fails with `No such command`.

- **`policy`** — `is-site-label-in-use`

### Changed command signatures

These commands changed shape — a renamed command or a changed flag can break an existing script.

**`devices`**

- `elisity devices search-suppression-list` — renamed from `get-users`; new required `--filters` (object). It lists suppression-list entries.

**`system`**

- `elisity system retrieve-snapshot-pdf` — renamed from `retrieve-snapshot-image`
- `elisity system search-snapshot-schedules` — new optional `--source` (string); dropped `--dashboard`
- `elisity system search-snapshots` — new optional `--source` (string); dropped `--dashboard`

**`topology`**

- `elisity topology get-all-distribution-zones` — new optional `--includeWorkload` (boolean)

### Changed request bodies

These commands take a different request body. Their flags are unchanged — the body is passed as JSON via `--body` / `--body-file` — but the JSON you send must match the new schema.

- **`policy`** — `bulk-create`, `create`, `create-dynamic-policy-group`, `create-dynamic-policy-groups`, `create-policy`, `create-policy-post`, `create-security-profile`, `create-security-profiles`, `export-policies-to-csv`, `overwrite-policy`, `update`, `update-dynamic-policy-group`
- **`system`** — `create-snapshot-schedule`
- **`topology`** — `create-distribution-zone`, `create-ven`, `update-distribution-zone`, `update-global-interfaces-settings`, `update-interfaces-settings`, `update-ven`

Other commands changed only in what they return; how you call them is unchanged.

### Added commands

New commands, grouped by CLI group.

#### `ad`

- `export-groups` — Generate groups export as XLSX
- `get-group-devices` — Get devices that are direct members of a group
- `get-group-users` — Get users that are direct members of a group
- `get-groups-count` — Get groups count
- `get-groups-default-enabled` — Get the 'enable all groups by default' toggle
- `get-groups-view` — Get groups view
- `set-groups-default-enabled` — Set the 'enable all groups by default' toggle (master reset)
- `set-groups-enabled` — Enable or disable one or many groups

#### `connectors`

- `fetch-tanium-sensor-catalog` — Fetch the Tanium sensor catalog
- `fetch-tanium-sensor-detail` — Look up one Tanium sensor by exact name
- `probe-tanium-sensor-mapping` — Probe a draft sensor mapping

#### `devices`

- `export-suppression-list` — Export entries as CSV
- `list-azure-regions-existing` — List Azure regions available to an existing endpoint's subscriptions
- `list-azure-regions-pre-creation` — List Azure regions available to a new endpoint's subscriptions (pre-creation)
- `list-azure-required-permissions` — List the ARM permissions the connector needs, by tier
- `list-azure-resource-groups-existing` — List Azure resource groups (with VM counts) for an existing endpoint
- `list-azure-resource-groups-pre-creation` — List Azure resource groups (with VM counts) for a new endpoint's scope
- `list-azure-subscriptions-existing` — List Azure subscriptions for an existing connector endpoint
- `list-azure-subscriptions-pre-creation` — List Azure subscriptions for a new endpoint (pre-creation)
- `preview-azure-scope-existing` — Preview the scope of an existing endpoint (post-creation scope edit)
- `preview-azure-scope-pre-creation` — Preview a scope before creating the connector

#### `policy`

- `create-access-policy-review` — Record a completed configuration review for an Access Policy
- `create-policy-review` — Record a completed configuration review for a Policy
- `export-access-policy-security-profile-rules` — Generate a CSV export of one Access Policy Security Profile's rules
- `export-access-policy-security-profiles` — Generate an Access Policy Security Profiles CSV export
- `export-security-profiles` — Generate a Security Profiles CSV export
- `export-security-rules` — Generate a CSV export of one Security Profile's rules
- `search-access-policy-security-profile-rules` — Search, filter and page the rules of one Access Policy Security Profile
- `search-access-policy-security-profiles` — Search, filter and page Access Policy Security Profiles
- `search-policies-for-policy-set` — Search and filter Policies in given Policy Set: filters in the JSON body
- `search-security-profiles` — Search, filter and page Security Profiles
- `search-security-rules` — Search, filter and page the Security Rules of one Security Profile

#### `system`

- `retrieve-snapshot-evidence` — Get snapshot evidence package
- `retrieve-snapshot-markdown` — Get snapshot Markdown

#### `topology`

- `get-virtual-edge-nodes-metrics-summary` — Aggregated VEN counts grouped per dimension (metrics summary)
- `get-virtual-edges-metrics-summary` — Aggregated VE counts grouped per dimension (metrics summary)
- `get-workload-distribution-zone-usage` — Report whether a Workload Distribution Zone is referenced by any workload-discovery connector endpoint
- `list-workload-distribution-zones` — List Workload Distribution Zones known to Identity Graph

## CCC 26.7

### `reporting` changes (breaking)

- **`get-zero-trust-metrics` — fixed.** A new repeatable `--mac-address` option selects
  devices (it implies `--include-mac`); `list-snapshots` is fixed the same way. The
  coverage numbers moved into a nested `policyDeploymentMetrics` object: read
  `.policyDeploymentMetrics.deviceCoverage` instead of `.avgDeviceCoverage`, and
  `.policyDeploymentMetrics.policyDeviceCoverage` instead of `.avgPolicyCoverage`. The
  new fields are not guaranteed to use the old 0–100 scale, so re-check any threshold
  against real output.
- **`diagnose-low-score` — removed.** CCC 26.7 removed the fields it filtered on. Use
  the two-step check in [docs/AGENTS.md](docs/AGENTS.md#diagnosing-a-lowzero-zero-trust-score-do-not-guess-the-cause)
  instead.
- **`get-policy-count-needed` — removed.** CCC 26.7 no longer reports the number. There is
  no replacement.
- **`get-policy-set-enforcement-score` — removed.** CCC 26.7 no longer reports a score per
  policy set. Use `get-aggregate-enforcement-score` (tenant-wide), `get-site-kpis`
  (`policyEnforcementScore` per site) or `get-zero-trust-metrics` (per policy group).

The `reporting` group has 17 commands, down from 20.

### Removed commands (breaking)

These commands were removed in CCC 26.7. A script that calls one fails with `No such command`.

- **`ad`** — `migrate-old-ad-agent-config`, `add-device-ad`, `attach-device`, `delete-device-ad`, `detach-device`, `get-device`, `get-device-by-sid-and-domain`, `refresh-device`, `update-device-ad`, `delete-domain-data`, `create-group-post`, `delete-group`, `delete-group-delete`, `get-group-by-sid-and-domain`, `get-groups-view`, `update-group`, `update-group-put`, `create-group`, `create-group-delete`, `attach-user`, `create-user`, `delete-user`, `detach-user`, `get-user-by-sid-and-domain`, `refresh-user`, `update-user`
- **`policy`** — `get-enforcement-score`, `get-enforcement-score-weight-settings`, `update-enforcement-score-weight-settings`

### Changed command signatures

These commands changed shape — a renamed command or a changed flag can break an existing script.

**`ad`**

- `elisity ad get-agents-and-dcs` — new optional `--page` (integer); new optional `--size` (integer); new optional `--sort` (string)
- `elisity ad unregister-connector` — new optional `--deleteAdData` (boolean)

**`connectors`**

- `elisity connectors read-get` — renamed from `read`

**`devices`**

- `elisity devices export-devices` — new optional `--format-param` (sends `format`) (string)
- `elisity devices get-device-attribute-values-with-display-names` — path moved from `/api/identity-graph/v2/devices/attributes/trustAttributes/values` to `/api/identity-graph/v2/devices/attributes/{attributeName}/values`; new required `ATTRIBUTENAME` (sends `attributeName`) (string); new optional `--queryString` (string)
- `elisity devices get-device-header-data` — renamed from `get-device-count`
- `elisity devices get-device-header-data-get` — renamed from `get-device-header-data`
- `elisity devices read-all-layer-instances-specification` — new optional `--includeWorkloads` (boolean)

**`flows`**

- `elisity flows flows-export` — `--offset` untyped (sent as string) -> integer; `--size` untyped (sent as string) -> integer
- `elisity flows get-available-ports` — `--page` untyped (sent as string) -> integer; `--search` untyped (sent as string) -> string; `--size` untyped (sent as string) -> integer
- `elisity flows get-pg-data` — `--format-param` (sends `format`) untyped (sent as string) -> string; `--size` untyped (sent as string) -> integer
- `elisity flows get-traffic-record` — `--offset` untyped (sent as string) -> integer; `--size` untyped (sent as string) -> integer
- `elisity flows get-unique-values` — `--parameter` untyped (sent as string) -> string
- `elisity flows search-noise-definitions` — `--query-param` (sends `query`) untyped (sent as string) -> string

**`policy`**

- `elisity policy get-all-matching-criteria` — new optional `--targetType` (string)
- `elisity policy get-matrix` — path moved from `/api/policy/v1/policy-views/{id}/matrix` to `/api/policy/v1/policy-views/{id}/matrix-legacy`
- `elisity policy get-policy-groups-by-ids` — new required `--filters` (object)
- `elisity policy get-policy-groups-json` — new optional `--targetType` (string)
- `elisity policy lookup-dynamic` — new required `--filters` (object)
- `elisity policy lookup-dynamic-totals` — new required `--filters` (object)
- `elisity policy lookup-network` — new required `--filters` (object)

**`topology`**

- `elisity topology export-virtual-edge-nodes` — new optional `--contextVeId` (string)
- `elisity topology get-all-distribution-zones-get` — new optional `--columnFilters` (string); dropped `--columnFilter`
- `elisity topology get-all-sites-v2` — new optional `--columnFilters` (string); dropped `--columnFilter`
- `elisity topology get-all-ve-ns-for-global-credentials` — new optional `--columnFilters` (string); dropped `--columnFilter`
- `elisity topology get-virtual-edge` — new optional `--columnFilters` (string); dropped `--columnFilter`
- `elisity topology get-virtual-edge-get` — new optional `--columnFilters` (string); dropped `--columnFilter`
- `elisity topology get-virtual-edge-node-firewall-rules` — new optional `--columnFilters` (string); dropped `--columnFilter`
- `elisity topology get-virtual-edge-nodes` — new optional `--columnFilters` (string); new optional `--contextVeId` (string); dropped `--columnFilter`
- `elisity topology get-virtual-edge-nodes-by-post` — new optional `--contextVeId` (string)

### Changed request bodies

These commands take a different request body. Their flags are unchanged — the body is passed as JSON via `--body` / `--body-file` — but the JSON you send must match the new schema.

- **`ad`** — `export`, `export-users`, `export-users-logon-history`, `export-users-post`
- **`connectors`** — `create`, `create-connector-configuration`, `update`, `update-connector-configuration`
- **`devices`** — `bulk-create-devices`, `bulk-update-devices`, `create`, `create-configuration`, `create-device`, `execute-bulk-refresh`, `get-configurations-by-ids`, `get-device-aggregate`, `get-devices-view`, `update-configuration`, `update-device`
- **`flows`** — `get-dash-board-summary-data`, `get-raw-traffic-summary`, `update-noise-definition`
- **`insights`** — `create-suggestion`, `execute-create-workflow`, `update-suggestion`
- **`policy`** — `clone-policy-set`, `create-dynamic-policy-group`, `create-dynamic-policy-groups`, `create-network-policy-group`, `create-network-policy-groups`, `create-policy`, `create-policy-group-label`, `create-policy-post`, `create-policy-set`, `create-policy-view`, `create-template`, `evaluate-policy-group-for-device`, `export-policies-to-csv`, `export-policy-group-to-csv`, `export-templates`, `get-policy-groups-summary`, `lookup-dynamic-export`, `lookup-network-export`, `toggle-lock-bulk`, `update-dynamic-policy-group`, `update-network-policy-group`, `update-policy`, `update-policy-group-label`, `update-policy-groups`, `update-policy-groups-with-device-groups`, `update-policy-put`, `update-policy-set`, `update-policy-view`, `update-template`
- **`topology`** — `bulk-create-site-labels`, `create-cloud-controller`, `create-distribution-zone`, `create-flow-exporter`, `create-global-credentials`, `create-or-update-bulk-target-site`, `create-or-update-target-site`, `create-site-post`, `create-ven`, `create-virtual-edge`, `create-virtual-edge-group`, `export-distribution-zones`, `export-site-labels`, `export-virtual-edges`, `get-dashboard-metrics`, `get-virtual-edge-by-post`, `get-virtual-edge-by-post-post`, `update-cloud-controller`, `update-distribution-zone`, `update-flow-exporter`, `update-global-credentials`, `update-global-interfaces-settings`, `update-interfaces-settings`, `update-ports-configuration`, `update-site`, `update-ven`, `update-virtual-edge`, `update-virtual-edge-group`, `update-virtual-edge-put`, `validate-virtual-edge-nodes-bulk-update`, `virtual-edge-bulk-change-group`, `virtual-edge-bulk-upload`, `virtual-edge-node-bulk-upload`

Other commands changed only in what they return; how you call them is unchanged.

### Added commands

New commands, grouped by CLI group.

#### `ad`

- `delete-auth` — Delete Entra authentication and all related data
- `get-activity-logs` — Query agent activity log
- `get-connector-deletion-context` — Get connector deletion context
- `get-distribution-zone-assignments` — Get distribution zone assignments per connector
- `get-isolated-distribution-zones` — `GET /api/ad-connector-service/v1/distribution-zones`
- `get-pull-status` — Get the status of a previously-initiated log pull; on success streams the ZIP bytes
- `pull-logs` — Initiate a log pull from an AD Agent
- `restart` — Restart the connector
- `set-distribution-zones` — Set distribution zones for a connector

#### `connectors`

- `add-endpoint` — Add an endpoint to a connector
- `create-connector` — Create new connector configuration
- `delete-connector` — Delete connector configuration by ID
- `delete-endpoint` — Delete an endpoint
- `get-endpoint` — Get a single endpoint
- `list-endpoints` — List all endpoints for a connector
- `read` — Get hierarchical connector status with per-endpoint details
- `read-all-connectors` — Read all connector configuration entries
- `read-connector` — Read connector configuration by ID
- `update-connector` — Update connector configuration by ID
- `update-endpoint` — Update an endpoint

#### `devices`

- `create-workload` — Create a static workload
- `devices-aggregate` — Get device aggregate counts
- `devices-count` — Get device counts
- `devices-view` — Query devices with CSearch filters
- `discover-ec2workloads` — Discover EC2 workloads for an existing connector
- `export-devices-from-view` — Export devices to CSV or XLSX
- `generate-external-id` — Generate external ID and account ID for IAM role setup
- `generate-trust-policy` — Generate trust policy JSON for the customer's IAM role
- `get-all-settings` — Get all offline purge settings grouped by configuration
- `get-auth-methods` — List available AWS authentication methods
- `get-permissions-policy` — Get the IAM permissions policy for ElisityCloudDiscoveryPolicy
- `get-specification` — Read workload attribute specification
- `get-workload-aggregate` — Get workload aggregated counts
- `get-workload-count` — Get workload count
- `get-workload-details` — Get workload by ID
- `get-workloads-view` — List workloads
- `list-available-regions` — List available AWS regions for an endpoint's credentials
- `list-available-regions-existing` — List available AWS regions for an existing connector endpoint
- `sync-connector` — Trigger immediate workload sync for all endpoints of a connector
- `sync-endpoint` — Trigger immediate workload sync for a specific endpoint
- `update-settings` — Update offline purge settings (global and policy groups)
- `update-workload` — Update workload STATIC attributes
- `update-workload-interface` — Update STATIC layer of a workload interface

#### `flows`

- `get-capabilities` — Get analytics capabilities
- `get-distribution-zone-sankey` — Get distribution zone sankey data
- `get-exclusion-filter-candidates` — Get exclusion filter candidate port+protocol pairs ranked by traffic usage
- `get-heatmap` — `GET /nflowsearch/api/v1/devices/{deviceId}/heatmap`
- `traffic-record-export` — Export traffic records as CSV

#### `insights`

- `get-suggestion-match-criteria` — Get Suggestion match criteria for a Policy Group

#### `policy`

- `add-definition` — `POST /api/flows/v1/applications/{id}/definitions`
- `bulk-create` — Create several labels atomically (Add Another Label drawer)
- `bulk-create-post` — Bulk-create access policies (Multi-Create) — best-effort / partial success
- `bulk-impact` — Aggregated impact for several labels (deduplicated devices) — bulk delete dialog
- `bulk-move` — Move labels to a folder (or to root if targetFolderId is null)
- `can-disable-nested-policy-groups` — Check if nested policy groups can be disabled
- `cancel-import` — Cancel an ongoing label import
- `colors` — Allowed label colours (single source of truth for UI palette + XLSX legend)
- `create` — Create a new label
- `create-1` — Create new access policy security profile
- `create-application` — `POST /api/flows/v1/applications`
- `create-post` — Create a new folder (max depth 3, name globally unique per type)
- `create-post-2` — Create an access policy on a policy set
- `create-vendor` — Create a new Vendor
- `delete` — Delete a label
- `delete-1` — Delete an access policy security profile
- `delete-application` — `DELETE /api/flows/v1/applications/{id}`
- `delete-delete` — Delete a folder (only if no subfolders)
- `delete-delete-2` — Delete an access policy
- `delete-vendor` — Delete a Vendor
- `download-template` — Download a blank label import template (XLSX)
- `enable-nested-policy-groups` — Enable/disable nested policy groups
- `export-csv` — `GET /api/flows/v1/applications/export`
- `export-policy-group-labels` — Export Policy Group Labels to CSV
- `get-access-policies` — List access policies on a policy set (the Access Policy column)
- `get-access-policies-for-profile` — Get access policies using this profile (where used)
- `get-all` — Get all access policy security profiles
- `get-application` — `GET /api/flows/v1/applications/{id}`
- `get-auto-group-tag-value-settings` — Get Group Tag Value settings
- `get-by-id` — Get a single label by id
- `get-coverage` — Get Coverage With Info
- `get-coverage-weight-settings` — Get settings for Coverage Weights
- `get-current-nested-policy-groups-flag` — Get current nested policy groups flag
- `get-history-entries` — Search and filter policy history
- `get-import-status` — Get status of an ongoing or completed label import
- `get-matching-criteria-inheritance` — Get matching criteria inheritance chain for a policy group
- `get-matrix-with-search` — Get matrix data with search filters
- `get-matrix-with-search-post` — Get matrix data with search filters
- `get-policy-group-labels` — Search and filter Policy Group Labels
- `get-policy-group-tree` — Get policy groups as a flat tree list
- `get-policy-group-workloads` — Search and filter workloads for a policy group
- `get-vendor` — Get a vendor
- `impact` — List devices currently assigned this label (impact analysis before delete)
- `import-labels` — Bulk import labels from an XLSX or CSV file (max 3 MB, async)
- `list` — List labels (paged), with optional folder filter and free-text search on name+description
- `list-applications` — `GET /api/flows/v1/applications`
- `list-get` — List folders for a type with cumulative label counts (folder + descendants)
- `list-vendors` — List all Vendors
- `lookup` — Resolve a batch of label ids to metadata
- `move` — Move a folder under a different parent
- `move-policy-group-scope` — Move a root dynamic policy group between Global/Local scope
- `overwrite-policy` — Overwrite an inherited/reflection Policy cell and re-cascade
- `preview-operation` — Preview the scope of a matrix operation (create / overwrite / delete) before running it
- `read-by-id` — Read an access policy security profile by ID
- `remove-definition` — `DELETE /api/flows/v1/applications/{id}/definitions/{defId}`
- `rename` — Rename a folder
- `reorder-siblings` — Reorder a dynamic policy group among its siblings
- `update` — Update a label color/description (name is immutable in v1)
- `update-1` — Update an access policy security profile
- `update-application` — `PUT /api/flows/v1/applications/{id}`
- `update-auto-group-tag-value-settings` — Save Group Tag Value settings
- `update-coverage-weight-settings` — Save settings for Coverage Weights
- `update-definition` — `PUT /api/flows/v1/applications/{id}/definitions/{defId}`
- `update-put` — Update an access policy
- `update-vendor` — Update an existing Vendor

#### `system`

- `create-snapshot-schedule` — Create snapshot schedule
- `delete-snapshot-schedule` — Delete snapshot schedule
- `pause-snapshot-schedule` — Pause snapshot schedule
- `resume-snapshot-schedule` — Resume snapshot schedule
- `retrieve-snapshot` — Get snapshot by ID
- `retrieve-snapshot-image` — Get snapshot PDF
- `retrieve-snapshot-schedule` — Get snapshot schedule by ID
- `search-snapshot-schedules` — Search snapshot schedules
- `search-snapshots` — Search snapshots
- `update-snapshot-schedule` — Update snapshot schedule

#### `topology`

- `bulk-change-ven-group` — Bulk change Virtual Edge Group for multiple VENs
- `bulk-recommission-ve-ns` — Bulk recommission Virtual Edge Nodes
- `change-active-ve` — Change Active Virtual Edge for a Virtual Edge Node (VEN)
- `change-ven-group` — Change Virtual Edge Group for a Virtual Edge Node (VEN)
- `disable-maintenance` — Disable Maintenance mode on a Virtual Edge
- `disable-maintenance-for-group` — Disable Maintenance mode on a batch of Virtual Edges in a group
- `enable-maintenance` — Enable Maintenance mode on a Virtual Edge
- `enable-maintenance-for-group` — Enable Maintenance mode on a batch of Virtual Edges in a group
- `force-delete-ven` — Force delete a Virtual Edge Node in decommission state
- `get-configuration` — Get VEN configuration
- `get-details` — Get VEN details
- `get-metrics` — Get VEN metrics
- `get-permissions` — Get VEN permissions
- `get-status` — Get VEN status
- `get-target-site-history` — Retrieves the full history for a specific target type.
- `get-virtual-edge-nodes-for-distribution-zone` — Get all Virtual Edge Nodes for a Distribution Zone
- `patch-virtual-edge-group` — Partial-update of a virtual edge group
- `search-virtual-edge-nodes` — List Virtual Edge Nodes with pagination and sorting
- `update-target-site-by-id` — Updates an existing target site entry by ID (for active or future entries).
- `upload-virtual-edge-nodes-bulk-json` — Bulk upload VEN rows (V2, JSON streaming)
- `upload-virtual-edges-bulk-json` — Bulk upload VE rows (V2, JSON streaming)
- `validate-virtual-edge-nodes-bulk-json` — Validate VEN rows for bulk upload (V2, JSON streaming)
- `validate-virtual-edges-bulk-json` — Validate VE rows for bulk upload (V2, JSON streaming)
