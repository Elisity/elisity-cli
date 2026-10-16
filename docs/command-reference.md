# Elisity CLI -- Command Reference

> The 623 REST commands below are auto-generated from the Elisity CCC OpenAPI
> specification. The `reporting` group (17 commands) is hand-coded against the
> CCC GraphQL endpoint at `/api/reporting/v1/data` and is NOT listed in this
> reference — see [user-guide.md](user-guide.md) section 9 for the full
> reporting catalog.
>
> **647 commands** total: 623 auto-generated REST + 17 hand-coded GraphQL
> reporting + 7 CLI-native (auth + config). 11 groups total. (Excludes the 3
> CLI-native `glossary` commands; see README for the full 650-command count.)
>
> This file is generated — run `python3 tools/gen_command_reference.py` after
> regenerating commands. Do not edit it by hand.

## Quick Find by Operation Type

### List / Get operations (215 commands)

| Group | Command | Description |
|-------|---------|-------------|
| ad | `agent-manifest` | Get AD Agent version manifest |
| ad | `get-activity-logs` | Query agent activity log |
| ad | `get-ad-agent-config` | Get config for specific AD Agent |
| ad | `get-agent-service-credentials` | Get AD Agent service credentials |
| ad | `get-agents-and-dcs` | Get list of AD Agents and DCs |
| ad | `get-attribute-values` | Get attribute values |
| ad | `get-auth` | Get Entra authentication |
| ad | `get-configuration-value` | Get configuration value |
| ad | `get-connector-by-id` | Get the connector |
| ad | `get-connector-deletion-context` | Get connector deletion context |
| ad | `get-connectors` | Get connectors |
| ad | `get-connectors-get` | Get loggers for all active AD Agents |
| ad | `get-dc-bookmark` | Get DC bookmark for specific AD Agent and DC hostname |
| ad | `get-distribution-zone-assignments` | Get distribution zone assignments per connector |
| ad | `get-entra-users` | Entra users |
| ad | `get-groups-count` | Get groups count |
| ad | `get-groups-default-enabled` | Get the 'enable all groups by default' toggle |
| ad | `get-isolated-distribution-zones` | GET /api/ad-connector-service/v1/distribution-zones |
| ad | `get-pull-status` | Get the status of a previously-initiated log pull; on success streams the ZIP bytes |
| ad | `get-suppressed-ip-attaches` | Get all suppressed IP attaches |
| ad | `get-syslog-credentials` | Get syslog credentials |
| ad | `get-users-count-data` | Get users count |
| ad | `get-users-logon-history` | Retrieve user logon history for a device |
| ad | `get-users-view` | Get users view |
| ad | `status` | Entra status |
| connectors | `download-export-file` | Download generated XLSX for the export task |
| connectors | `download-import-template` | Download sample XLSX import template for Custom Connector |
| connectors | `get-custom-connector-devices` | Get devices from custom connector for given layer |
| connectors | `get-endpoint` | Get a single endpoint |
| connectors | `get-export-status` | Get status of ongoing or completed export task |
| connectors | `get-status` | Get status of ongoing or completed import task |
| connectors | `list-endpoints` | List all endpoints for a connector |
| connectors | `read` | Get hierarchical connector status with per-endpoint details |
| connectors | `read-all-connector-configurations` | Read all connector configuration entries |
| connectors | `read-all-connectors` | Read all connector configuration entries |
| connectors | `read-connector` | Read connector configuration by ID |
| connectors | `read-connector-configuration` | Read connector configuration by ID |
| connectors | `read-endpoints` | Get connectivity status of connector endpoints by type |
| connectors | `read-get` | Get connectivity status of all configured connectors |
| devices | `check` | Check ig-view-service sync state against the identity-graph DB (no dispatch) |
| devices | `check-ven-availability` | Check if VEN is able to accept device attach |
| devices | `devices-count` | Get device counts |
| devices | `feature-flag-ig` | Get current status of a feature flag |
| devices | `get-all-settings` | Get all offline purge settings grouped by configuration |
| devices | `get-auth-methods` | List available AWS authentication methods |
| devices | `get-blended-enrichment-order` | Read enrichment order |
| devices | `get-configuration-by-id` | Get time-based configuration by ID |
| devices | `get-configurations` | Get time-based configurations |
| devices | `get-custom-oui-mappings` | Get custom OUI mappings |
| devices | `get-device-attribute-values` | Get device attribute values |
| devices | `get-device-attribute-values-with-display-names` | Get values with displayNames for an attribute |
| devices | `get-device-header-data` | Get devices count |
| devices | `get-device-header-data-get` | Get devices count |
| devices | `get-enrichment-order-dto` | Read enrichment order settings entry |
| devices | `get-permissions-policy` | Get the IAM permissions policy for ElisityCloudDiscoveryPolicy |
| devices | `get-raw-enrichment-order` | Read raw enrichment order settings entry |
| devices | `get-specification` | Read workload attribute specification |
| devices | `get-values-for-device-attribute` | Get values for device attribute |
| devices | `get-workload-count` | Get workload count |
| devices | `get-workload-details` | Get workload by ID |
| devices | `list-all-custom-connector-icons-base64` | List all Custom Connector icons (base64) |
| devices | `list-azure-required-permissions` | List the ARM permissions the connector needs, by tier |
| devices | `read-all-layer-instances-specification` | Read dynamic specification of all layers |
| devices | `read-all-settings` | Read all settings entries |
| devices | `read-device` | Get device by ID |
| devices | `read-history-for-device` | Read device event history by device ID |
| devices | `read-static-layer-specification` | Read static layer specification |
| devices | `search-by-name` | Search time-based configurations by name |
| devices | `search-device` | Search device by MAC |
| devices | `search-suppression-list` | Get all entries (paged, searchable and filterable) |
| devices | `stream-digest` | Stream device digest |
| flows | `get-available-ports` | Get all available ports and their names |
| flows | `get-capabilities` | Get analytics capabilities |
| flows | `get-exclusion-filter-candidates` | Get exclusion filter candidate port+protocol pairs ranked by traffic usage |
| flows | `get-heatmap` | GET /nflowsearch/api/v1/devices/{deviceId}/heatmap |
| flows | `get-noise-definition` | GET /api/flows/v1/noisedefinition |
| flows | `get-unique-values` | Get unique values |
| flows | `search-noise-definitions` | GET /api/flows/v1/noisedefinition/search |
| insights | `get-categories-list` | Get Categories list |
| insights | `get-policy-group-suggestions` | Get Policy Groups suggestions |
| insights | `get-policy-groups-suggestion-list` | Get all suggestions (including 'disabled' suggestions) |
| insights | `get-policy-groups-suggestion-list-get` | Get suggestions by Category |
| insights | `get-policy-suggestion-list` | Get all Policy suggestions |
| insights | `get-settings` | Get settings for Policy Suggestion |
| insights | `get-suggestion-match-criteria` | Get Suggestion match criteria for a Policy Group |
| insights | `get-suggestions` | Get suggestion for Network Policy Suggestion |
| insights | `get-suggestions-ok-status-only` | Get suggestion for Network Policy Suggestion |
| insights | `list-network-policy-group-suggestions` | Get settings for Network Policy Suggestion |
| policy | `can-disable-nested-policy-groups` | Check if nested policy groups can be disabled |
| policy | `colors` | Allowed label colours (single source of truth for UI palette + XLSX legend) |
| policy | `download-template` | Download a blank label import template (XLSX) |
| policy | `export-csv` | GET /api/flows/v1/applications/export |
| policy | `get-access-policies` | List access policies on a policy set (the Access Policy column) |
| policy | `get-access-policies-for-profile` | Get access policies using this profile (where used) |
| policy | `get-all` | Get all access policy security profiles |
| policy | `get-all-as-nd-json` | Get all policy sets |
| policy | `get-all-as-nd-json-get` | Get all policy group labels |
| policy | `get-all-as-nd-json-get-2` | Get all policy groups |
| policy | `get-all-matching-criteria` | Get match criteria labels and constant values |
| policy | `get-all-policies-as-nd-json` | Get all policies |
| policy | `get-all-policies-for-policy-group-as-nd-json` | Get all policies for given policy group (NDJSON) |
| policy | `get-all-policies-for-policy-set-as-nd-json` | Search and filter Policies in given Policy Set |
| policy | `get-all-policies-for-policy-view-as-nd-json` | Get all Policies for given Policy View |
| policy | `get-all-policy-views-as-nd-json` | Get all policy views |
| policy | `get-all-security-profiles-as-nd-json` | Get all security profiles |
| policy | `get-all-site-labels-from-all-policy-sets` | Get all site labels assigned to policy sets |
| policy | `get-application` | GET /api/flows/v1/applications/{id} |
| policy | `get-auto-group-tag-value-settings` | Get Group Tag Value settings |
| policy | `get-by-id` | Get a single label by id |
| policy | `get-count-of-all-policies-for-policy-set` | Get count of all Policies for given Policy Set |
| policy | `get-coverage` | Get Coverage With Info |
| policy | `get-coverage-weight-settings` | Get settings for Coverage Weights |
| policy | `get-current-local-policy-groups-flag` | Get current local policy groups flag |
| policy | `get-current-multiple-policy-set-enablement-flag` | Get Security Profile Log enablement flag |
| policy | `get-current-nested-policy-groups-flag` | Get current nested policy groups flag |
| policy | `get-device-details` | Get device details by id |
| policy | `get-history-entries` | Search and filter policy history |
| policy | `get-image` | Get an image |
| policy | `get-import-status` | Get status of an ongoing or completed label import |
| policy | `get-label-by-id` | Get a policy group label by ID. |
| policy | `get-local-policy-group-sites` | Get saved Site Labels with number of Local Policy Groups created for Site Label |
| policy | `get-matching-criteria-dynamic-values` | Get values for dynamic match criteria |
| policy | `get-matching-criteria-inheritance` | Get matching criteria inheritance chain for a policy group |
| policy | `get-nodes-assigned-to-policy-set` | Get virtual edge nodes assigned to Policy Set |
| policy | `get-policies-count` | Get Policies count |
| policy | `get-policies-for-security-profile` | Get policies for given security profile |
| policy | `get-policy-by-id` | Get a policy by ID |
| policy | `get-policy-group-by-id` | Get a policy group by ID |
| policy | `get-policy-group-devices` | Search and filter devices for a policy group |
| policy | `get-policy-group-labels` | Search and filter Policy Group Labels |
| policy | `get-policy-group-tree` | Get policy groups as a flat tree list |
| policy | `get-policy-group-workloads` | Search and filter workloads for a policy group |
| policy | `get-policy-groups-assigned-to-policy-set` | Get Policy Groups assigned to Policy Set |
| policy | `get-policy-groups-for-ven` | Get Policy Groups assigned to a VEN |
| policy | `get-policy-groups-json` | Search and filter policy groups |
| policy | `get-policy-groups-with-device-groups-for-ven` | Get Policy Groups with Device Names assigned to a VEN |
| policy | `get-policy-set-by-id` | Get a policy set by ID |
| policy | `get-state` | Get paginated policy resource states |
| policy | `get-status` | Get current status of a feature flag |
| policy | `get-template-by-id` | Get a Policy Group Template by ID |
| policy | `get-vendor` | Get a vendor |
| policy | `impact` | List devices currently assigned this label (impact analysis before delete) |
| policy | `list` | List labels (paged), with optional folder filter and free-text search on name+description |
| policy | `list-applications` | GET /api/flows/v1/applications |
| policy | `list-get` | List folders for a type with cumulative label counts (folder + descendants) |
| policy | `list-images` | List all images |
| policy | `list-vendors` | List all Vendors |
| policy | `read-by-id` | Read an access policy security profile by ID |
| policy | `read-policy-view` | Read a policy view by ID |
| policy | `read-security-profile` | Read a security profile by ID |
| policy | `search-templates` | Search and filter Policy Group Templates |
| system | `get-all-configs` | Get all task broker configs |
| system | `get-effective-config` | Get effective config for a VE |
| system | `get-next-task-for-ve` | Poll next task for VE |
| system | `get-spec` | Get spec by VE ID |
| system | `get-spec-by-site-id` | Get specs by site ID |
| system | `get-spec-group-id` | Get specs by VE group ID |
| system | `get-task` | Get task by ID |
| system | `list-specs` | List all specs |
| system | `list-tasks` | List tasks |
| system | `retrieve-snapshot` | Get snapshot by ID |
| system | `retrieve-snapshot-evidence` | Get snapshot evidence package |
| system | `retrieve-snapshot-markdown` | Get snapshot Markdown |
| system | `retrieve-snapshot-pdf` | Get snapshot PDF |
| system | `retrieve-snapshot-schedule` | Get snapshot schedule by ID |
| system | `search-snapshot-schedules` | Search snapshot schedules |
| system | `search-snapshots` | Search snapshots |
| topology | `get-all-cloud-controllers` | Get cloud controllers |
| topology | `get-all-distribution-zones` | Get all Distribution Zones |
| topology | `get-all-distribution-zones-get` | Get all Distribution Zones (paginated) |
| topology | `get-all-flow-exporter` | Get all flow exporters |
| topology | `get-all-global-credentials` | Get all global credentials |
| topology | `get-all-sites` | Get all Sites |
| topology | `get-all-sites-v2` | Get all Sites (paginated) |
| topology | `get-all-tags` | Get all Tags used for Site Labels |
| topology | `get-all-target-sites` | Get all configured deployment targets |
| topology | `get-all-ve-ns-for-global-credentials` | Get Virtual Edge Nodes using a global credential |
| topology | `get-configuration` | Get VEN configuration |
| topology | `get-dashboard-count` | Get VE and VEN dashboard count |
| topology | `get-details` | Get VEN details |
| topology | `get-distribution-zone` | Get single Distribution Zone |
| topology | `get-flow-exporter` | Get a single flow exporter |
| topology | `get-global-interfaces-settings` | Get global interface settings |
| topology | `get-independent-control-mappings` | Get all Independent Control Mappings for Distribution Zones |
| topology | `get-logger` | Get logger level |
| topology | `get-loggers-for-all-virtual-edges` | Get loggers for all virtual edges |
| topology | `get-manifest` | Get manifest with versions for Central VE |
| topology | `get-metrics` | Get VEN metrics |
| topology | `get-permissions` | Get VEN permissions |
| topology | `get-ports-configuration` | Get ports configuration for a VEN |
| topology | `get-reconciled-variables` | Reconciled environment variables for a VE |
| topology | `get-settings` | Get topology settings |
| topology | `get-single-ven` | Get single Virtual Edge Node |
| topology | `get-site` | Get single Site |
| topology | `get-site-count` | Get site count |
| topology | `get-site-count-v2` | Get site count |
| topology | `get-site-label-independent-control-mappings` | Get all Independent Control Mappings for Site Labels |
| topology | `get-site-v2` | Get single Site |
| topology | `get-status` | Get VEN status |
| topology | `get-target-site` | Get target for a specific type |
| topology | `get-target-site-history` | Retrieves the full history for a specific target type. |
| topology | `get-target-types` | Get all available target types |
| topology | `get-topology` | Get topology for a VEN |
| topology | `get-ve-ns-overview-response` | Returns a non-paginated overview, having name and status, of Virtual Edge Nodes. |
| topology | `get-ve-variables` | Download variables for a VE |
| topology | `get-virtual-edge` | Search and filter virtual edge |
| topology | `get-virtual-edge-by-id` | Get a virtual edge by ID |
| topology | `get-virtual-edge-get` | Search and filter Virtual Edge Group |
| topology | `get-virtual-edge-group-by-id` | Get a virtual edge group by ID |
| topology | `get-virtual-edge-node-firewall-rules` | List of Firewalls and Firewall rules for given Virtual Edge Node with pagination |
| topology | `get-virtual-edge-nodes` | List Virtual Edge Nodes with pagination and sorting |
| topology | `get-virtual-edge-nodes-for-distribution-zone` | Get all Virtual Edge Nodes for a Distribution Zone |
| topology | `get-workload-distribution-zone-usage` | Report whether a Workload Distribution Zone is referenced by any workload-discovery connector endpoint |
| topology | `is-imbalanced` | Check if Virtual Edge Group is imbalanced |
| topology | `list-workload-distribution-zones` | List Workload Distribution Zones known to Identity Graph |

### Create operations (263 commands)

| Group | Command | Description |
|-------|---------|-------------|
| ad | `agent-status` | Set AD Agent and DC status |
| ad | `export` | Generate AD Agents export as CSV |
| ad | `export-groups` | Generate groups export as XLSX |
| ad | `export-users` | Generate users export as CSV |
| ad | `export-users-logon-history` | Generate users logon export as CSV |
| ad | `export-users-post` | Generate Entra users export as CSV |
| ad | `get-group-devices` | Get devices that are direct members of a group |
| ad | `get-group-users` | Get users that are direct members of a group |
| ad | `get-groups-view` | Get groups view |
| ad | `pull-logs` | Initiate a log pull from an AD Agent |
| ad | `refresh-all-ad-on-prem` | Refresh all AD on-prem subscriptions |
| ad | `refresh-all-entra` | Refresh all Entra subscriptions |
| ad | `register-connector` | Register the connector |
| ad | `restart` | Restart the connector |
| ad | `resync` | Resync the connector |
| ad | `save-activity-logs` | Receive activity log events from agent |
| ad | `save-ad-agent-config` | Save new config for specific AD Agent |
| ad | `save-logger-change` | Save log level for specific AD Agent |
| ad | `sync` | Sync Entra |
| ad | `update-agent-description` | Save AD Agent description |
| ad | `update-agent-service-credentials` | Save AD Agent service credentials |
| ad | `update-agent-to-version` | Update AD Agent to specific or latest version |
| ad | `update-all-agents-to-latest-version` | Update all AD Agents to latest version |
| ad | `update-auth` | Update Entra authentication |
| ad | `upload-logs` | Upload agent logs |
| connectors | `add-endpoint` | Add an endpoint to a connector |
| connectors | `async-export-devices` | Start async export of devices for custom connector as XLSX |
| connectors | `cancel-current-export` | Cancel the current ongoing export (without exportId) |
| connectors | `cancel-current-import` | Cancel the current ongoing import (without uploadId) |
| connectors | `cancel-import` | Cancel ongoing import for a custom connector |
| connectors | `create` | Create a single inventory record |
| connectors | `create-connector` | Create new connector configuration |
| connectors | `create-connector-configuration` | Create new connector configuration |
| connectors | `export-devices` | Export devices for custom connector as XLSX |
| connectors | `fetch-tanium-sensor-catalog` | Fetch the Tanium sensor catalog |
| connectors | `fetch-tanium-sensor-detail` | Look up one Tanium sensor by exact name |
| connectors | `import-file` | Import XLS/XLSX file with Custom Connector data |
| connectors | `probe-tanium-sensor-mapping` | Probe a draft sensor mapping |
| connectors | `validate-connector-endpoint-configuration` | Validate connector endpoint configuration |
| connectors | `validate-endpoint-for-connector` | Validate endpoint configuration for existing connector |
| connectors | `validate-endpoint-pre-creation` | Validate endpoint configuration before connector creation |
| devices | `bulk-create-devices` | Create new devices |
| devices | `bulk-create-devices-from-file` | Create new devices from XLSX file |
| devices | `create` | Create a new suppression entry |
| devices | `create-configuration` | Create new time-based configuration |
| devices | `create-device` | Create a new device |
| devices | `create-workload` | Create a static workload |
| devices | `detach` | Detach device by ID |
| devices | `detach-by-mac` | Detach device by MAC and IP |
| devices | `devices-aggregate` | Get device aggregate counts |
| devices | `devices-view` | Query devices with CSearch filters |
| devices | `discover-ec2workloads` | Discover EC2 workloads for an existing connector |
| devices | `duplicate-configuration` | Duplicate time-based configuration |
| devices | `enrich-by-id` | Enrich device by ID. |
| devices | `enrich-by-ip` | Enrich device by IP. |
| devices | `execute-bulk-refresh` | Execute a asynchronous on-demand enrichment of given devices for given sources (bulk) |
| devices | `execute-synchronous-on-demand-enrichment` | Execute a synchronous on demand enrichment of given device with a given source |
| devices | `execute-synchronous-on-demand-enrichment-post` | Execute a synchronous on demand enrichment of given device for all sources |
| devices | `export-devices` | Generate devices export |
| devices | `export-devices-from-view` | Export devices to CSV or XLSX |
| devices | `export-suppression-list` | Export entries as CSV |
| devices | `generate-external-id` | Generate external ID and account ID for IAM role setup |
| devices | `generate-trust-policy` | Generate trust policy JSON for the customer's IAM role |
| devices | `get-configurations-by-ids` | Get multiple time-based configurations by IDs |
| devices | `get-device-aggregate` | Get devices aggregated count |
| devices | `get-devices-view` | Get devices view |
| devices | `get-workload-aggregate` | Get workload aggregated counts |
| devices | `get-workloads-view` | List workloads |
| devices | `list-available-regions` | List available AWS regions for an endpoint's credentials |
| devices | `list-available-regions-existing` | List available AWS regions for an existing connector endpoint |
| devices | `list-azure-regions-existing` | List Azure regions available to an existing endpoint's subscriptions |
| devices | `list-azure-regions-pre-creation` | List Azure regions available to a new endpoint's subscriptions (pre-creation) |
| devices | `list-azure-resource-groups-existing` | List Azure resource groups (with VM counts) for an existing endpoint |
| devices | `list-azure-resource-groups-pre-creation` | List Azure resource groups (with VM counts) for a new endpoint's scope |
| devices | `list-azure-subscriptions-existing` | List Azure subscriptions for an existing connector endpoint |
| devices | `list-azure-subscriptions-pre-creation` | List Azure subscriptions for a new endpoint (pre-creation) |
| devices | `preview-azure-scope-existing` | Preview the scope of an existing endpoint (post-creation scope edit) |
| devices | `preview-azure-scope-pre-creation` | Preview a scope before creating the connector |
| devices | `refresh-devices-view` | Refresh DevicesView |
| devices | `set-feature-flag-ig` | Set value of a feature flag |
| devices | `sync` | Synchronize ig-view-service from identity-graph by republishing out-of-sync devices |
| devices | `sync-connector` | Trigger immediate workload sync for all endpoints of a connector |
| devices | `sync-endpoint` | Trigger immediate workload sync for a specific endpoint |
| devices | `upsert-enrichment-order` | Update/create settings entry |
| devices | `validate-azure-connection-existing` | Validate the Azure connection of an existing endpoint, optionally with edited credentials |
| devices | `validate-azure-connection-pre-creation` | Validate Azure connection for a new endpoint (pre-creation) |
| devices | `validate-azure-permissions-existing` | Validate Azure permissions for an existing connector endpoint |
| devices | `validate-azure-permissions-pre-creation` | Validate Azure permissions for a new endpoint (pre-creation) |
| devices | `validate-azure-region-permissions-existing` | Validate an existing endpoint's region filter against its subscriptions |
| devices | `validate-azure-region-permissions-pre-creation` | Validate a new endpoint's region filter against its subscriptions (pre-creation) |
| devices | `validate-permissions-existing` | Validate AWS permissions for an existing connector endpoint |
| devices | `validate-permissions-pre-creation` | Validate AWS permissions for a new endpoint (pre-creation) |
| flows | `flows-export` | Generate flows export as CSV |
| flows | `get-dash-board-summary-data` | POST /nflowsearch/api/v1/dashboardSummary |
| flows | `get-distribution-zone-sankey` | Get distribution zone sankey data |
| flows | `get-pg-data` | POST /nflowsearch/api/v1/pgdata |
| flows | `get-raw-traffic-summary` | Get traffic summary data |
| flows | `get-traffic-record` | POST /nflowsearch/api/v1/trafficRecord |
| flows | `traffic-record-export` | Export traffic records as CSV |
| flows | `update-noise-definition` | POST /api/flows/v1/noisedefinition |
| insights | `all-workflows-preview` | Preview all activation workflows |
| insights | `create-suggestion` | Create new suggestion |
| insights | `create-suggestions` | Create Network Policy Suggestions |
| insights | `day0workflow-preview` | Preview Policy Day 0 workflow |
| insights | `day15workflow-preview` | Preview Policy Day 15 workflow |
| insights | `day30workflow-preview` | Preview Policy Day 30 workflow |
| insights | `day7workflow-preview` | Preview Policy Day 7 workflow |
| insights | `execute-activate-workflow` | Execute activation workflow |
| insights | `execute-create-workflow` | Execute creation workflow |
| insights | `post-policy-group-suggestions-preview` | Get Policy Groups suggestions Preview |
| insights | `recreate-policy-suggestions` | Delete and Create all Policy suggestions |
| insights | `recreate-suggestions` | Delete and Create all suggestions |
| insights | `reset-policy-suggestions-to-default` | Delete and Create all default Policy Suggestions |
| insights | `reset-suggestions-to-default` | Delete and Create all default suggestions |
| insights | `reset-suggestions-to-default-post` | Delete and Create all default Network Suggestions |
| policy | `add-definition` | POST /api/flows/v1/applications/{id}/definitions |
| policy | `bulk-create` | Create several labels atomically (Add Another Label drawer) |
| policy | `bulk-create-post` | Bulk-create access policies (Multi-Create) — best-effort / partial success |
| policy | `bulk-delete` | Bulk delete labels |
| policy | `bulk-impact` | Aggregated impact for several labels (deduplicated devices) — bulk delete dialog |
| policy | `bulk-move` | Move labels to a folder (or to root if targetFolderId is null) |
| policy | `cancel-import` | Cancel an ongoing label import |
| policy | `change-status` | Enable/disable feature flag |
| policy | `clone-policy-set` | Clone Policy Set |
| policy | `create` | Create a new label |
| policy | `create-1` | Create new access policy security profile |
| policy | `create-access-policy-review` | Record a completed configuration review for an Access Policy |
| policy | `create-application` | POST /api/flows/v1/applications |
| policy | `create-dynamic-policy-group` | Create new dynamic policy group |
| policy | `create-dynamic-policy-groups` | Bulk create of Dynamic Policy Group |
| policy | `create-image` | Create a new image |
| policy | `create-network-policy-group` | Create new network policy group |
| policy | `create-network-policy-groups` | Bulk create of Network Policy Group |
| policy | `create-policy` | Bulk create Policy |
| policy | `create-policy-group-label` | Create a new policy group label. |
| policy | `create-policy-post` | Create Policy |
| policy | `create-policy-review` | Record a completed configuration review for a Policy |
| policy | `create-policy-set` | Create Policy Set |
| policy | `create-policy-view` | Create a policy view |
| policy | `create-post` | Create a new folder (max depth 3, name globally unique per type) |
| policy | `create-post-2` | Create an access policy on a policy set |
| policy | `create-replica-policy-set` | Create Replica Policy Set |
| policy | `create-security-profile` | Create new security profile |
| policy | `create-security-profiles` | Bulk create of Security Profiles |
| policy | `create-template` | Create new Policy Group Template |
| policy | `create-vendor` | Create a new Vendor |
| policy | `enable-local-policy-groups` | Enable/disable local policy groups |
| policy | `enable-nested-policy-groups` | Enable/disable nested policy groups |
| policy | `evaluate-policy` | Evaluate Policy |
| policy | `evaluate-policy-export` | Evaluate Policy and export result as CSV |
| policy | `evaluate-policy-group-for-device` | Find Policy Group, that provided Device would be classified to |
| policy | `export-access-policy-security-profile-rules` | Generate a CSV export of one Access Policy Security Profile's rules |
| policy | `export-access-policy-security-profiles` | Generate an Access Policy Security Profiles CSV export |
| policy | `export-policies-to-csv` | Generate policies export as CSV |
| policy | `export-policy-group-labels` | Export Policy Group Labels to CSV |
| policy | `export-policy-group-to-csv` | Generate Policy Groups export as CSV |
| policy | `export-security-profiles` | Generate a Security Profiles CSV export |
| policy | `export-security-rules` | Generate a CSV export of one Security Profile's rules |
| policy | `export-templates` | Export Policy Group Templates to CSV |
| policy | `get-devices-current-pg-and-new-pg-after-evaluation` | Get current and expected policy groups after the devices will be unlocked |
| policy | `get-matrix` | Get matrix data |
| policy | `get-matrix-with-search` | Get matrix data with search filters |
| policy | `get-matrix-with-search-post` | Get matrix data with search filters |
| policy | `get-online-devices-for-distribution-zones` | Get count of online devices for distribution zones |
| policy | `get-online-devices-for-site-labels` | Get count of online devices for site labels |
| policy | `get-policy-groups-by-ids` | Search and filter policy groups by ids |
| policy | `get-policy-groups-summary` | Get Policy Groups summary |
| policy | `import-labels` | Bulk import labels from an XLSX or CSV file (max 3 MB, async) |
| policy | `lookup` | Resolve a batch of label ids to metadata |
| policy | `lookup-dynamic` | Get Assets that are expected to Match the Dynamic Policy Group |
| policy | `lookup-dynamic-export` | Export Assets that are expected to Match the Dynamic Policy Group to CSV |
| policy | `lookup-dynamic-totals` | Count Assets that are expected to Match the Dynamic Policy Group |
| policy | `lookup-evaluation-endpoint` | Evaluation Endpoint IP lookup |
| policy | `lookup-network` | Get Assets that are expected to Match the Network Policy Group |
| policy | `lookup-network-export` | Export Assets that are expected to Match the Network Policy Group to CSV |
| policy | `overwrite-policy` | Overwrite an inherited/reflection Policy cell and re-cascade |
| policy | `partial-reorder-policy-group` | Reorder (partial) policy group |
| policy | `post-local-policy-group-site` | Save Site Label for creating Local Policy Groups |
| policy | `preview-operation` | Preview the scope of a matrix operation (create / overwrite / delete) before running it |
| policy | `search-access-policy-security-profile-rules` | Search, filter and page the rules of one Access Policy Security Profile |
| policy | `search-access-policy-security-profiles` | Search, filter and page Access Policy Security Profiles |
| policy | `search-policies-for-policy-set` | Search and filter Policies in given Policy Set: filters in the JSON body |
| policy | `search-security-profiles` | Search, filter and page Security Profiles |
| policy | `search-security-rules` | Search, filter and page the Security Rules of one Security Profile |
| policy | `send-state-of-all-devices-to-identity-graph` | Send current state of all Devices to Identity Graph |
| policy | `send-state-of-device-to-identity-graph` | Send current state of the Devices to Identity Graph |
| policy | `validate-application` | POST /api/flows/v1/applications/validate |
| policy | `validate-match-criteria` | Validate Match Criteria |
| policy | `validate-match-criteria-for-existing-policy-group` | Validate Match Criteria for existing Policy Group |
| policy | `validate-policy-group-name` | Validate Policy Group Name |
| policy | `validate-policy-group-name-for-existing-policy-group` | Validate Policy Group Name for existing Policy Group |
| policy | `validate-subnet-dynamic-policy-group` | Validate subnet for Dynamic Policy Group |
| policy | `validate-subnet-static-policy-group` | Validate subnet for Static Policy Group |
| policy | `validate-subnet-static-policy-group-post` | Bulk validate subnet for Static Policy Group |
| system | `ack-execution-of-task-post` | Acknowledge task with result payload |
| system | `create-snapshot-schedule` | Create snapshot schedule |
| system | `create-task` | Create a new task |
| system | `pause-snapshot-schedule` | Pause snapshot schedule |
| system | `register-specs` | Register or update VE specs |
| system | `resume-snapshot-schedule` | Resume snapshot schedule |
| topology | `batch-create-or-update-multiple-rules` | Bulk create or update rules for given Palo Alto VEN and Firewall |
| topology | `bulk-change-ven-group` | Bulk change Virtual Edge Group for multiple VENs |
| topology | `bulk-create-site-labels` | Bulk create site labels |
| topology | `bulk-delete-distribution-zone` | Bulk delete Distribution Zones |
| topology | `bulk-delete-site` | Bulk delete site labels. |
| topology | `bulk-delete-site-v2` | Bulk delete site labels |
| topology | `bulk-delete-ve-ns` | Bulk delete Virtual Edge Nodes |
| topology | `bulk-delete-virtual-edges` | Bulk delete Virtual Edges |
| topology | `bulk-force-delete-ve-ns` | Bulk force delete Virtual Edge Nodes |
| topology | `bulk-recommission-ve-ns` | Bulk recommission Virtual Edge Nodes |
| topology | `create-cloud-controller` | Create a new cloud controller |
| topology | `create-distribution-zone` | Create Distribution Zones |
| topology | `create-flow-exporter` | Create a flow exporter |
| topology | `create-global-credentials` | Create new global credentials |
| topology | `create-independent-control-mappings` | Create Independent Control Mappings between Distribution Zones |
| topology | `create-or-update-bulk-target-site` | Bulk create or update targets |
| topology | `create-or-update-multiple-rules` | Create or update rules for given Palo Alto VEN and Firewall |
| topology | `create-or-update-target-site` | Create or update target for a specific type |
| topology | `create-site` | Create list of sites. |
| topology | `create-site-label-independent-control-mappings` | Create Independent Control Mappings between Site Labels |
| topology | `create-site-post` | Create site label |
| topology | `create-task-list` | Create a task list |
| topology | `create-ven` | Create a new virtual edge node |
| topology | `create-virtual-edge` | Create new virtual edge |
| topology | `create-virtual-edge-group` | Create new virtual edge group |
| topology | `disable-maintenance` | Disable Maintenance mode on a Virtual Edge |
| topology | `disable-maintenance-for-group` | Disable Maintenance mode on a batch of Virtual Edges in a group |
| topology | `enable-maintenance` | Enable Maintenance mode on a Virtual Edge |
| topology | `enable-maintenance-for-group` | Enable Maintenance mode on a batch of Virtual Edges in a group |
| topology | `export-distribution-zones` | Export Distribution Zones as CSV |
| topology | `export-site-labels` | Export site labels as CSV |
| topology | `export-virtual-edge-nodes` | Generate all virtual edge nodes as XLSX |
| topology | `export-virtual-edges` | Generate all virtual edges as XLSX |
| topology | `get-dashboard-metrics` | Get VE and VEN dashboard metrics |
| topology | `get-virtual-edge-by-post` | Search and filter virtual edge |
| topology | `get-virtual-edge-by-post-post` | Search and filter virtual edge group |
| topology | `get-virtual-edge-nodes-by-post` | List Virtual Edge Nodes with pagination and sorting |
| topology | `get-virtual-edge-nodes-metrics-summary` | Aggregated VEN counts grouped per dimension (metrics summary) |
| topology | `get-virtual-edges-metrics-summary` | Aggregated VE counts grouped per dimension (metrics summary) |
| topology | `heartbeat` | Register heartbeat for a VE |
| topology | `heartbeat-post` | Register heartbeat from virtual edge node |
| topology | `metrics` | Publish operational metrics for a VE |
| topology | `metrics-post` | Publish operational metrics for a VEN |
| topology | `publish-ve-variables` | Publish variables for a VE |
| topology | `register` | Register a VE |
| topology | `register-ven` | Register virtual edge node |
| topology | `search-virtual-edge-nodes` | List Virtual Edge Nodes with pagination and sorting |
| topology | `set-logger-level` | Set logger level |
| topology | `set-logger-levels-bulk` | Set logger levels in bulk |
| topology | `sxp-password-regenerate` | Regenerate SXP password for Virtual Edge Node |
| topology | `topology` | Publish topology seen from a VEN |
| topology | `update-virtual-edge-post` | Regenerate OTP for existing virtual edge |
| topology | `upload-virtual-edge-nodes-bulk-json` | Bulk upload VEN rows (V2, JSON streaming) |
| topology | `upload-virtual-edges-bulk-json` | Bulk upload VE rows (V2, JSON streaming) |
| topology | `validate-virtual-edge-bulk-delete` | Validate Virtual Edges before bulk delete |
| topology | `validate-virtual-edge-bulk-upload` | Validate XLSX file for Virtual Edge bulk upload |
| topology | `validate-virtual-edge-node-bulk-delete` | Validate Virtual Edge Nodes before bulk delete |
| topology | `validate-virtual-edge-nodes-bulk-json` | Validate VEN rows for bulk upload (V2, JSON streaming) |
| topology | `validate-virtual-edge-nodes-bulk-upload` | Validate XLSX file for Virtual Edge Node bulk upload |
| topology | `validate-virtual-edges-bulk-json` | Validate VE rows for bulk upload (V2, JSON streaming) |
| topology | `virtual-edge-bulk-change-group` | Bulk change Virtual Edge group |
| topology | `virtual-edge-bulk-upload` | Bulk upload Virtual Edges from XLSX file |
| topology | `virtual-edge-node-bulk-upload` | Bulk upload Virtual Edge Nodes from XLSX file |

### Update operations (83 commands)

| Group | Command | Description |
|-------|---------|-------------|
| ad | `ping` | Health check |
| ad | `put-configuration-value` | Update configuration value |
| ad | `set-distribution-zones` | Set distribution zones for a connector |
| ad | `set-groups-default-enabled` | Set the 'enable all groups by default' toggle (master reset) |
| connectors | `update` | Update a single inventory record |
| connectors | `update-connector` | Update connector configuration by ID |
| connectors | `update-connector-configuration` | Update connector configuration by ID |
| connectors | `update-endpoint` | Update an endpoint |
| devices | `add-device-unique-attribute-value` | Add device attribute unique value |
| devices | `apply-custom-oui-mappings` | Upload custom OUI mappings and override existing ones |
| devices | `bulk-recalculate-effective-attributes` | Recalculate effective attributes by ID |
| devices | `bulk-update-devices` | Update devices by ID |
| devices | `recalculate-attributes` | Recalculate attributes on all devices |
| devices | `update` | Update suppression entry |
| devices | `update-configuration` | Update time-based configuration |
| devices | `update-settings` | Update offline purge settings (global and policy groups) |
| insights | `reorder-suggestion` | Reorder Suggestion |
| insights | `save-settings` | Save settings for Policy Suggestion |
| insights | `update-suggestion` | Update Suggestion |
| insights | `update-suggestion-put` | Update Network Policy Suggestion |
| policy | `enable-multiple-policy-sets` | Enable Security Profile Log |
| policy | `lock-device` | Lock Device by serviceDeviceIds |
| policy | `lock-policy-group` | Lock policy group |
| policy | `move-policy-group-scope` | Move a root dynamic policy group between Global/Local scope |
| policy | `reorder-siblings` | Reorder a dynamic policy group among its siblings |
| policy | `toggle-lock-bulk` | Bulk toggle lock/unlock Devices by serviceDeviceIds, creates DelayedTask for each device |
| policy | `unlock-device` | Unlock Device by serviceDeviceIds |
| policy | `unlock-policy-group` | Unlock policy group |
| policy | `update-1` | Update an access policy security profile |
| policy | `update-application` | PUT /api/flows/v1/applications/{id} |
| policy | `update-auto-group-tag-value-settings` | Save Group Tag Value settings |
| policy | `update-coverage-weight-settings` | Save settings for Coverage Weights |
| policy | `update-definition` | PUT /api/flows/v1/applications/{id}/definitions/{defId} |
| policy | `update-dynamic-policy-group` | Update dynamic policy group |
| policy | `update-image` | Update an existing image |
| policy | `update-network-policy-group` | Update network policy group |
| policy | `update-policy` | Update policy |
| policy | `update-policy-group-label` | Update an existing policy group label |
| policy | `update-policy-groups` | Bulk update of Policy Group |
| policy | `update-policy-groups-with-device-groups` | Bulk update of Policy Group with Device Group |
| policy | `update-policy-put` | Bulk update Policy |
| policy | `update-policy-set` | Update Policy Set |
| policy | `update-policy-view` | Update a policy view |
| policy | `update-put` | Update an access policy |
| policy | `update-security-profile` | Update a security profile |
| policy | `update-template` | Update a Policy Group Template |
| policy | `update-vendor` | Update an existing Vendor |
| system | `ack-execution-of-task` | Acknowledge task without result payload |
| system | `release-execution-of-task` | Release task |
| system | `replace-for-ve` | Replace per-VE disabled task types |
| system | `replace-tenant-default` | Replace tenant-wide disabled task types |
| system | `update-snapshot-schedule` | Update snapshot schedule |
| system | `update-task` | Update task |
| topology | `ack-registration` | Acknowledge registration of Central VE |
| topology | `change-active-ve` | Change Active Virtual Edge for a Virtual Edge Node (VEN) |
| topology | `change-ven-group` | Change Virtual Edge Group for a Virtual Edge Node (VEN) |
| topology | `change-virtual-edge-group` | Change virtual edge group for existing virtual edge |
| topology | `decommission-virtual-edge-node` | Trigger decommission of a registered virtual edge node |
| topology | `exclude-adjacent-vens` | Exclude adjacent VEN from topology |
| topology | `re-initialize-virtual-edge-node` | Trigger re-initialization of a unsuccessful recommission or onboard |
| topology | `rebalance-virtual-edge-group` | Rebalance Virtual Edge Group |
| topology | `recommission-virtual-edge-node` | Trigger recommission of a decommissioned virtual edge node |
| topology | `rediscover-adjacent-vens` | Rediscover adjacent VENs and recreate missing ones |
| topology | `set-version` | Set desired version in manifest of Central VE for nodeId |
| topology | `update-cloud-controller` | Update cloud controller |
| topology | `update-distribution-zone` | Update Distribution Zone |
| topology | `update-flow-exporter` | Update a flow exporter |
| topology | `update-global-credentials` | Update global credentials |
| topology | `update-global-interfaces-settings` | Update global interface settings |
| topology | `update-interfaces-settings` | Update interface settings by ID (deprecated) |
| topology | `update-ports-configuration` | Update ports configuration for a VEN |
| topology | `update-settings` | Update topology settings |
| topology | `update-site` | Update site |
| topology | `update-site-put` | Update site. |
| topology | `update-site-put-2` | Update site. |
| topology | `update-target-site-by-id` | Updates an existing target site entry by ID (for active or future entries). |
| topology | `update-task-list` | Update a task list |
| topology | `update-task-status` | Update task status report |
| topology | `update-ven` | Update existing virtual edge node |
| topology | `update-virtual-edge` | Update existing virtual edge |
| topology | `update-virtual-edge-group` | Update existing virtual edge group |
| topology | `update-virtual-edge-put` | Override OTP for existing virtual edge |
| topology | `validate-virtual-edge-nodes-bulk-update` | Bulk update VEN credentials |

### Delete operations (52 commands)

| Group | Command | Description |
|-------|---------|-------------|
| ad | `delete-auth` | Delete Entra authentication and all related data |
| ad | `unregister-connector` | Unregister the connector |
| connectors | `delete` | Delete a single inventory record |
| connectors | `delete-connector` | Delete connector configuration by ID |
| connectors | `delete-connector-configuration` | Delete connector configuration by ID |
| connectors | `delete-endpoint` | Delete an endpoint |
| devices | `bulk-delete-devices` | Delete device |
| devices | `bulk-purge-device-layers` | Bulk purge device layers |
| devices | `delete` | Delete suppression entry |
| devices | `delete-configuration` | Delete time-based configuration |
| devices | `delete-device` | Delete device |
| devices | `delete-enrichment-order` | Delete enrichment order settings entry |
| devices | `purge-device-layer` | Purge device layer |
| insights | `delete-suggestion` | Delete Suggestion |
| insights | `delete-suggestion-delete` | Delete Network Policy Suggestions |
| policy | `delete` | Delete a label |
| policy | `delete-1` | Delete an access policy security profile |
| policy | `delete-application` | DELETE /api/flows/v1/applications/{id} |
| policy | `delete-delete` | Delete a folder (only if no subfolders) |
| policy | `delete-delete-2` | Delete an access policy |
| policy | `delete-image` | Delete an image |
| policy | `delete-label` | Delete a policy group label by ID |
| policy | `delete-local-policy-group-site-by-id` | Remove Site Label from list of site labels for Local Policy Groups |
| policy | `delete-policy` | Delete Policy |
| policy | `delete-policy-delete` | Bulk delete Policy |
| policy | `delete-policy-group` | Delete a policy group |
| policy | `delete-policy-groups` | Bulk delete Policy Group |
| policy | `delete-policy-set` | Delete Policy Set |
| policy | `delete-policy-view` | Delete a policy view |
| policy | `delete-security-profiles` | Delete a security profile |
| policy | `delete-template` | Delete a Policy Group Template |
| policy | `delete-vendor` | Delete a Vendor |
| policy | `remove-definition` | DELETE /api/flows/v1/applications/{id}/definitions/{defId} |
| system | `cancel-task` | Cancel task |
| system | `delete-for-ve` | Remove per-VE override |
| system | `delete-snapshot-schedule` | Delete snapshot schedule |
| topology | `bulk-delete-cloud-controllers` | Bulk delete Mist cloud controllers |
| topology | `bulk-delete-credentials` | Bulk delete global credentials |
| topology | `delete-cloud-controller` | Delete Mist cloud controller |
| topology | `delete-distribution-zone` | Delete Distribution Zone |
| topology | `delete-flow-exporter` | Delete a flow exporter |
| topology | `delete-global-credentials` | Delete global credentials |
| topology | `delete-independent-control-mappings` | Delete Independent Control Mappings |
| topology | `delete-site` | Delete site. |
| topology | `delete-site-label-independent-control-mappings` | Delete Independent Control Mappings for Site Labels |
| topology | `delete-site-v2` | Delete site |
| topology | `delete-target-site` | Delete target for a specific type |
| topology | `delete-ven` | Delete virtual edge node |
| topology | `delete-virtual-edge` | Delete existing virtual edge |
| topology | `delete-virtual-edge-group` | Delete existing virtual edge group |
| topology | `force-delete-ven` | Force delete a Virtual Edge Node in decommission state |
| topology | `use-default-logger-level` | Reset logger to default level |

### Patch operations (10 commands)

| Group | Command | Description |
|-------|---------|-------------|
| ad | `set-groups-enabled` | Enable or disable one or many groups |
| devices | `enrich-by-id-append` | Enrich device by ID and append to existing data in layer (create layer if not exists). |
| devices | `enrich-by-ip-append` | Enrich device by IP and append to existing data in layer (create layer if not exists). |
| devices | `update-device` | Partially update device by ID |
| devices | `update-workload` | Update workload STATIC attributes |
| devices | `update-workload-interface` | Update STATIC layer of a workload interface |
| policy | `move` | Move a folder under a different parent |
| policy | `rename` | Rename a folder |
| policy | `update` | Update a label color/description (name is immutable in v1) |
| topology | `patch-virtual-edge-group` | Partial-update of a virtual edge group |

## Built-in Commands

### auth

Authentication and token management.

| Command | Description |
|---------|-------------|
| `auth test` | Test CCC authentication and connectivity |
| `auth token` | Get bearer token for use in scripts or curl |
| `auth whoami` | Decode and display JWT token claims |

### config

Profile and configuration management.

| Command | Description |
|---------|-------------|
| `config set-profile NAME` | Create or update a named connection profile |
| `config use-profile NAME` | Switch the active profile |
| `config list-profiles` | List all saved profiles |
| `config show` | Show active configuration (secrets redacted) |

---

## API Command Groups

### ad (57 commands)

| Command | Description |
|---------|-------------|
| `agent-manifest` | Get AD Agent version manifest |
| `agent-status` | Set AD Agent and DC status |
| `delete-auth` | Delete Entra authentication and all related data |
| `export` | Generate AD Agents export as CSV |
| `export-groups` | Generate groups export as XLSX |
| `export-users` | Generate users export as CSV |
| `export-users-logon-history` | Generate users logon export as CSV |
| `export-users-post` | Generate Entra users export as CSV |
| `get-activity-logs` | Query agent activity log |
| `get-ad-agent-config` | Get config for specific AD Agent |
| `get-agent-service-credentials` | Get AD Agent service credentials |
| `get-agents-and-dcs` | Get list of AD Agents and DCs |
| `get-attribute-values` | Get attribute values |
| `get-auth` | Get Entra authentication |
| `get-configuration-value` | Get configuration value |
| `get-connector-by-id` | Get the connector |
| `get-connector-deletion-context` | Get connector deletion context |
| `get-connectors` | Get connectors |
| `get-connectors-get` | Get loggers for all active AD Agents |
| `get-dc-bookmark` | Get DC bookmark for specific AD Agent and DC hostname |
| `get-distribution-zone-assignments` | Get distribution zone assignments per connector |
| `get-entra-users` | Entra users |
| `get-group-devices` | Get devices that are direct members of a group |
| `get-group-users` | Get users that are direct members of a group |
| `get-groups-count` | Get groups count |
| `get-groups-default-enabled` | Get the 'enable all groups by default' toggle |
| `get-groups-view` | Get groups view |
| `get-isolated-distribution-zones` | GET /api/ad-connector-service/v1/distribution-zones |
| `get-pull-status` | Get the status of a previously-initiated log pull; on success streams the ZIP bytes |
| `get-suppressed-ip-attaches` | Get all suppressed IP attaches |
| `get-syslog-credentials` | Get syslog credentials |
| `get-users-count-data` | Get users count |
| `get-users-logon-history` | Retrieve user logon history for a device |
| `get-users-view` | Get users view |
| `ping` | Health check |
| `pull-logs` | Initiate a log pull from an AD Agent |
| `put-configuration-value` | Update configuration value |
| `refresh-all-ad-on-prem` | Refresh all AD on-prem subscriptions |
| `refresh-all-entra` | Refresh all Entra subscriptions |
| `register-connector` | Register the connector |
| `restart` | Restart the connector |
| `resync` | Resync the connector |
| `save-activity-logs` | Receive activity log events from agent |
| `save-ad-agent-config` | Save new config for specific AD Agent |
| `save-logger-change` | Save log level for specific AD Agent |
| `set-distribution-zones` | Set distribution zones for a connector |
| `set-groups-default-enabled` | Set the 'enable all groups by default' toggle (master reset) |
| `set-groups-enabled` | Enable or disable one or many groups |
| `status` | Entra status |
| `sync` | Sync Entra |
| `unregister-connector` | Unregister the connector |
| `update-agent-description` | Save AD Agent description |
| `update-agent-service-credentials` | Save AD Agent service credentials |
| `update-agent-to-version` | Update AD Agent to specific or latest version |
| `update-all-agents-to-latest-version` | Update all AD Agents to latest version |
| `update-auth` | Update Entra authentication |
| `upload-logs` | Upload agent logs |

### connectors (38 commands)

| Command | Description |
|---------|-------------|
| `add-endpoint` | Add an endpoint to a connector |
| `async-export-devices` | Start async export of devices for custom connector as XLSX |
| `cancel-current-export` | Cancel the current ongoing export (without exportId) |
| `cancel-current-import` | Cancel the current ongoing import (without uploadId) |
| `cancel-import` | Cancel ongoing import for a custom connector |
| `create` | Create a single inventory record |
| `create-connector` | Create new connector configuration |
| `create-connector-configuration` | Create new connector configuration |
| `delete` | Delete a single inventory record |
| `delete-connector` | Delete connector configuration by ID |
| `delete-connector-configuration` | Delete connector configuration by ID |
| `delete-endpoint` | Delete an endpoint |
| `download-export-file` | Download generated XLSX for the export task |
| `download-import-template` | Download sample XLSX import template for Custom Connector |
| `export-devices` | Export devices for custom connector as XLSX |
| `fetch-tanium-sensor-catalog` | Fetch the Tanium sensor catalog |
| `fetch-tanium-sensor-detail` | Look up one Tanium sensor by exact name |
| `get-custom-connector-devices` | Get devices from custom connector for given layer |
| `get-endpoint` | Get a single endpoint |
| `get-export-status` | Get status of ongoing or completed export task |
| `get-status` | Get status of ongoing or completed import task |
| `import-file` | Import XLS/XLSX file with Custom Connector data |
| `list-endpoints` | List all endpoints for a connector |
| `probe-tanium-sensor-mapping` | Probe a draft sensor mapping |
| `read` | Get hierarchical connector status with per-endpoint details |
| `read-all-connector-configurations` | Read all connector configuration entries |
| `read-all-connectors` | Read all connector configuration entries |
| `read-connector` | Read connector configuration by ID |
| `read-connector-configuration` | Read connector configuration by ID |
| `read-endpoints` | Get connectivity status of connector endpoints by type |
| `read-get` | Get connectivity status of all configured connectors |
| `update` | Update a single inventory record |
| `update-connector` | Update connector configuration by ID |
| `update-connector-configuration` | Update connector configuration by ID |
| `update-endpoint` | Update an endpoint |
| `validate-connector-endpoint-configuration` | Validate connector endpoint configuration |
| `validate-endpoint-for-connector` | Validate endpoint configuration for existing connector |
| `validate-endpoint-pre-creation` | Validate endpoint configuration before connector creation |

### devices (103 commands)

| Command | Description |
|---------|-------------|
| `add-device-unique-attribute-value` | Add device attribute unique value |
| `apply-custom-oui-mappings` | Upload custom OUI mappings and override existing ones |
| `bulk-create-devices` | Create new devices |
| `bulk-create-devices-from-file` | Create new devices from XLSX file |
| `bulk-delete-devices` | Delete device |
| `bulk-purge-device-layers` | Bulk purge device layers |
| `bulk-recalculate-effective-attributes` | Recalculate effective attributes by ID |
| `bulk-update-devices` | Update devices by ID |
| `check` | Check ig-view-service sync state against the identity-graph DB (no dispatch) |
| `check-ven-availability` | Check if VEN is able to accept device attach |
| `create` | Create a new suppression entry |
| `create-configuration` | Create new time-based configuration |
| `create-device` | Create a new device |
| `create-workload` | Create a static workload |
| `delete` | Delete suppression entry |
| `delete-configuration` | Delete time-based configuration |
| `delete-device` | Delete device |
| `delete-enrichment-order` | Delete enrichment order settings entry |
| `detach` | Detach device by ID |
| `detach-by-mac` | Detach device by MAC and IP |
| `devices-aggregate` | Get device aggregate counts |
| `devices-count` | Get device counts |
| `devices-view` | Query devices with CSearch filters |
| `discover-ec2workloads` | Discover EC2 workloads for an existing connector |
| `duplicate-configuration` | Duplicate time-based configuration |
| `enrich-by-id` | Enrich device by ID. |
| `enrich-by-id-append` | Enrich device by ID and append to existing data in layer (create layer if not exists). |
| `enrich-by-ip` | Enrich device by IP. |
| `enrich-by-ip-append` | Enrich device by IP and append to existing data in layer (create layer if not exists). |
| `execute-bulk-refresh` | Execute a asynchronous on-demand enrichment of given devices for given sources (bulk) |
| `execute-synchronous-on-demand-enrichment` | Execute a synchronous on demand enrichment of given device with a given source |
| `execute-synchronous-on-demand-enrichment-post` | Execute a synchronous on demand enrichment of given device for all sources |
| `export-devices` | Generate devices export |
| `export-devices-from-view` | Export devices to CSV or XLSX |
| `export-suppression-list` | Export entries as CSV |
| `feature-flag-ig` | Get current status of a feature flag |
| `generate-external-id` | Generate external ID and account ID for IAM role setup |
| `generate-trust-policy` | Generate trust policy JSON for the customer's IAM role |
| `get-all-settings` | Get all offline purge settings grouped by configuration |
| `get-auth-methods` | List available AWS authentication methods |
| `get-blended-enrichment-order` | Read enrichment order |
| `get-configuration-by-id` | Get time-based configuration by ID |
| `get-configurations` | Get time-based configurations |
| `get-configurations-by-ids` | Get multiple time-based configurations by IDs |
| `get-custom-oui-mappings` | Get custom OUI mappings |
| `get-device-aggregate` | Get devices aggregated count |
| `get-device-attribute-values` | Get device attribute values |
| `get-device-attribute-values-with-display-names` | Get values with displayNames for an attribute |
| `get-device-header-data` | Get devices count |
| `get-device-header-data-get` | Get devices count |
| `get-devices-view` | Get devices view |
| `get-enrichment-order-dto` | Read enrichment order settings entry |
| `get-permissions-policy` | Get the IAM permissions policy for ElisityCloudDiscoveryPolicy |
| `get-raw-enrichment-order` | Read raw enrichment order settings entry |
| `get-specification` | Read workload attribute specification |
| `get-values-for-device-attribute` | Get values for device attribute |
| `get-workload-aggregate` | Get workload aggregated counts |
| `get-workload-count` | Get workload count |
| `get-workload-details` | Get workload by ID |
| `get-workloads-view` | List workloads |
| `list-all-custom-connector-icons-base64` | List all Custom Connector icons (base64) |
| `list-available-regions` | List available AWS regions for an endpoint's credentials |
| `list-available-regions-existing` | List available AWS regions for an existing connector endpoint |
| `list-azure-regions-existing` | List Azure regions available to an existing endpoint's subscriptions |
| `list-azure-regions-pre-creation` | List Azure regions available to a new endpoint's subscriptions (pre-creation) |
| `list-azure-required-permissions` | List the ARM permissions the connector needs, by tier |
| `list-azure-resource-groups-existing` | List Azure resource groups (with VM counts) for an existing endpoint |
| `list-azure-resource-groups-pre-creation` | List Azure resource groups (with VM counts) for a new endpoint's scope |
| `list-azure-subscriptions-existing` | List Azure subscriptions for an existing connector endpoint |
| `list-azure-subscriptions-pre-creation` | List Azure subscriptions for a new endpoint (pre-creation) |
| `preview-azure-scope-existing` | Preview the scope of an existing endpoint (post-creation scope edit) |
| `preview-azure-scope-pre-creation` | Preview a scope before creating the connector |
| `purge-device-layer` | Purge device layer |
| `read-all-layer-instances-specification` | Read dynamic specification of all layers |
| `read-all-settings` | Read all settings entries |
| `read-device` | Get device by ID |
| `read-history-for-device` | Read device event history by device ID |
| `read-static-layer-specification` | Read static layer specification |
| `recalculate-attributes` | Recalculate attributes on all devices |
| `refresh-devices-view` | Refresh DevicesView |
| `search-by-name` | Search time-based configurations by name |
| `search-device` | Search device by MAC |
| `search-suppression-list` | Get all entries (paged, searchable and filterable) |
| `set-feature-flag-ig` | Set value of a feature flag |
| `stream-digest` | Stream device digest |
| `sync` | Synchronize ig-view-service from identity-graph by republishing out-of-sync devices |
| `sync-connector` | Trigger immediate workload sync for all endpoints of a connector |
| `sync-endpoint` | Trigger immediate workload sync for a specific endpoint |
| `update` | Update suppression entry |
| `update-configuration` | Update time-based configuration |
| `update-device` | Partially update device by ID |
| `update-settings` | Update offline purge settings (global and policy groups) |
| `update-workload` | Update workload STATIC attributes |
| `update-workload-interface` | Update STATIC layer of a workload interface |
| `upsert-enrichment-order` | Update/create settings entry |
| `validate-azure-connection-existing` | Validate the Azure connection of an existing endpoint, optionally with edited credentials |
| `validate-azure-connection-pre-creation` | Validate Azure connection for a new endpoint (pre-creation) |
| `validate-azure-permissions-existing` | Validate Azure permissions for an existing connector endpoint |
| `validate-azure-permissions-pre-creation` | Validate Azure permissions for a new endpoint (pre-creation) |
| `validate-azure-region-permissions-existing` | Validate an existing endpoint's region filter against its subscriptions |
| `validate-azure-region-permissions-pre-creation` | Validate a new endpoint's region filter against its subscriptions (pre-creation) |
| `validate-permissions-existing` | Validate AWS permissions for an existing connector endpoint |
| `validate-permissions-pre-creation` | Validate AWS permissions for a new endpoint (pre-creation) |

### flows (15 commands)

| Command | Description |
|---------|-------------|
| `flows-export` | Generate flows export as CSV |
| `get-available-ports` | Get all available ports and their names |
| `get-capabilities` | Get analytics capabilities |
| `get-dash-board-summary-data` | POST /nflowsearch/api/v1/dashboardSummary |
| `get-distribution-zone-sankey` | Get distribution zone sankey data |
| `get-exclusion-filter-candidates` | Get exclusion filter candidate port+protocol pairs ranked by traffic usage |
| `get-heatmap` | GET /nflowsearch/api/v1/devices/{deviceId}/heatmap |
| `get-noise-definition` | GET /api/flows/v1/noisedefinition |
| `get-pg-data` | POST /nflowsearch/api/v1/pgdata |
| `get-raw-traffic-summary` | Get traffic summary data |
| `get-traffic-record` | POST /nflowsearch/api/v1/trafficRecord |
| `get-unique-values` | Get unique values |
| `search-noise-definitions` | GET /api/flows/v1/noisedefinition/search |
| `traffic-record-export` | Export traffic records as CSV |
| `update-noise-definition` | POST /api/flows/v1/noisedefinition |

### insights (31 commands)

| Command | Description |
|---------|-------------|
| `all-workflows-preview` | Preview all activation workflows |
| `create-suggestion` | Create new suggestion |
| `create-suggestions` | Create Network Policy Suggestions |
| `day0workflow-preview` | Preview Policy Day 0 workflow |
| `day15workflow-preview` | Preview Policy Day 15 workflow |
| `day30workflow-preview` | Preview Policy Day 30 workflow |
| `day7workflow-preview` | Preview Policy Day 7 workflow |
| `delete-suggestion` | Delete Suggestion |
| `delete-suggestion-delete` | Delete Network Policy Suggestions |
| `execute-activate-workflow` | Execute activation workflow |
| `execute-create-workflow` | Execute creation workflow |
| `get-categories-list` | Get Categories list |
| `get-policy-group-suggestions` | Get Policy Groups suggestions |
| `get-policy-groups-suggestion-list` | Get all suggestions (including 'disabled' suggestions) |
| `get-policy-groups-suggestion-list-get` | Get suggestions by Category |
| `get-policy-suggestion-list` | Get all Policy suggestions |
| `get-settings` | Get settings for Policy Suggestion |
| `get-suggestion-match-criteria` | Get Suggestion match criteria for a Policy Group |
| `get-suggestions` | Get suggestion for Network Policy Suggestion |
| `get-suggestions-ok-status-only` | Get suggestion for Network Policy Suggestion |
| `list-network-policy-group-suggestions` | Get settings for Network Policy Suggestion |
| `post-policy-group-suggestions-preview` | Get Policy Groups suggestions Preview |
| `recreate-policy-suggestions` | Delete and Create all Policy suggestions |
| `recreate-suggestions` | Delete and Create all suggestions |
| `reorder-suggestion` | Reorder Suggestion |
| `reset-policy-suggestions-to-default` | Delete and Create all default Policy Suggestions |
| `reset-suggestions-to-default` | Delete and Create all default suggestions |
| `reset-suggestions-to-default-post` | Delete and Create all default Network Suggestions |
| `save-settings` | Save settings for Policy Suggestion |
| `update-suggestion` | Update Suggestion |
| `update-suggestion-put` | Update Network Policy Suggestion |

### policy (190 commands)

| Command | Description |
|---------|-------------|
| `add-definition` | POST /api/flows/v1/applications/{id}/definitions |
| `bulk-create` | Create several labels atomically (Add Another Label drawer) |
| `bulk-create-post` | Bulk-create access policies (Multi-Create) — best-effort / partial success |
| `bulk-delete` | Bulk delete labels |
| `bulk-impact` | Aggregated impact for several labels (deduplicated devices) — bulk delete dialog |
| `bulk-move` | Move labels to a folder (or to root if targetFolderId is null) |
| `can-disable-nested-policy-groups` | Check if nested policy groups can be disabled |
| `cancel-import` | Cancel an ongoing label import |
| `change-status` | Enable/disable feature flag |
| `clone-policy-set` | Clone Policy Set |
| `colors` | Allowed label colours (single source of truth for UI palette + XLSX legend) |
| `create` | Create a new label |
| `create-1` | Create new access policy security profile |
| `create-access-policy-review` | Record a completed configuration review for an Access Policy |
| `create-application` | POST /api/flows/v1/applications |
| `create-dynamic-policy-group` | Create new dynamic policy group |
| `create-dynamic-policy-groups` | Bulk create of Dynamic Policy Group |
| `create-image` | Create a new image |
| `create-network-policy-group` | Create new network policy group |
| `create-network-policy-groups` | Bulk create of Network Policy Group |
| `create-policy` | Bulk create Policy |
| `create-policy-group-label` | Create a new policy group label. |
| `create-policy-post` | Create Policy |
| `create-policy-review` | Record a completed configuration review for a Policy |
| `create-policy-set` | Create Policy Set |
| `create-policy-view` | Create a policy view |
| `create-post` | Create a new folder (max depth 3, name globally unique per type) |
| `create-post-2` | Create an access policy on a policy set |
| `create-replica-policy-set` | Create Replica Policy Set |
| `create-security-profile` | Create new security profile |
| `create-security-profiles` | Bulk create of Security Profiles |
| `create-template` | Create new Policy Group Template |
| `create-vendor` | Create a new Vendor |
| `delete` | Delete a label |
| `delete-1` | Delete an access policy security profile |
| `delete-application` | DELETE /api/flows/v1/applications/{id} |
| `delete-delete` | Delete a folder (only if no subfolders) |
| `delete-delete-2` | Delete an access policy |
| `delete-image` | Delete an image |
| `delete-label` | Delete a policy group label by ID |
| `delete-local-policy-group-site-by-id` | Remove Site Label from list of site labels for Local Policy Groups |
| `delete-policy` | Delete Policy |
| `delete-policy-delete` | Bulk delete Policy |
| `delete-policy-group` | Delete a policy group |
| `delete-policy-groups` | Bulk delete Policy Group |
| `delete-policy-set` | Delete Policy Set |
| `delete-policy-view` | Delete a policy view |
| `delete-security-profiles` | Delete a security profile |
| `delete-template` | Delete a Policy Group Template |
| `delete-vendor` | Delete a Vendor |
| `download-template` | Download a blank label import template (XLSX) |
| `enable-local-policy-groups` | Enable/disable local policy groups |
| `enable-multiple-policy-sets` | Enable Security Profile Log |
| `enable-nested-policy-groups` | Enable/disable nested policy groups |
| `evaluate-policy` | Evaluate Policy |
| `evaluate-policy-export` | Evaluate Policy and export result as CSV |
| `evaluate-policy-group-for-device` | Find Policy Group, that provided Device would be classified to |
| `export-access-policy-security-profile-rules` | Generate a CSV export of one Access Policy Security Profile's rules |
| `export-access-policy-security-profiles` | Generate an Access Policy Security Profiles CSV export |
| `export-csv` | GET /api/flows/v1/applications/export |
| `export-policies-to-csv` | Generate policies export as CSV |
| `export-policy-group-labels` | Export Policy Group Labels to CSV |
| `export-policy-group-to-csv` | Generate Policy Groups export as CSV |
| `export-security-profiles` | Generate a Security Profiles CSV export |
| `export-security-rules` | Generate a CSV export of one Security Profile's rules |
| `export-templates` | Export Policy Group Templates to CSV |
| `get-access-policies` | List access policies on a policy set (the Access Policy column) |
| `get-access-policies-for-profile` | Get access policies using this profile (where used) |
| `get-all` | Get all access policy security profiles |
| `get-all-as-nd-json` | Get all policy sets |
| `get-all-as-nd-json-get` | Get all policy group labels |
| `get-all-as-nd-json-get-2` | Get all policy groups |
| `get-all-matching-criteria` | Get match criteria labels and constant values |
| `get-all-policies-as-nd-json` | Get all policies |
| `get-all-policies-for-policy-group-as-nd-json` | Get all policies for given policy group (NDJSON) |
| `get-all-policies-for-policy-set-as-nd-json` | Search and filter Policies in given Policy Set |
| `get-all-policies-for-policy-view-as-nd-json` | Get all Policies for given Policy View |
| `get-all-policy-views-as-nd-json` | Get all policy views |
| `get-all-security-profiles-as-nd-json` | Get all security profiles |
| `get-all-site-labels-from-all-policy-sets` | Get all site labels assigned to policy sets |
| `get-application` | GET /api/flows/v1/applications/{id} |
| `get-auto-group-tag-value-settings` | Get Group Tag Value settings |
| `get-by-id` | Get a single label by id |
| `get-count-of-all-policies-for-policy-set` | Get count of all Policies for given Policy Set |
| `get-coverage` | Get Coverage With Info |
| `get-coverage-weight-settings` | Get settings for Coverage Weights |
| `get-current-local-policy-groups-flag` | Get current local policy groups flag |
| `get-current-multiple-policy-set-enablement-flag` | Get Security Profile Log enablement flag |
| `get-current-nested-policy-groups-flag` | Get current nested policy groups flag |
| `get-device-details` | Get device details by id |
| `get-devices-current-pg-and-new-pg-after-evaluation` | Get current and expected policy groups after the devices will be unlocked |
| `get-history-entries` | Search and filter policy history |
| `get-image` | Get an image |
| `get-import-status` | Get status of an ongoing or completed label import |
| `get-label-by-id` | Get a policy group label by ID. |
| `get-local-policy-group-sites` | Get saved Site Labels with number of Local Policy Groups created for Site Label |
| `get-matching-criteria-dynamic-values` | Get values for dynamic match criteria |
| `get-matching-criteria-inheritance` | Get matching criteria inheritance chain for a policy group |
| `get-matrix` | Get matrix data |
| `get-matrix-with-search` | Get matrix data with search filters |
| `get-matrix-with-search-post` | Get matrix data with search filters |
| `get-nodes-assigned-to-policy-set` | Get virtual edge nodes assigned to Policy Set |
| `get-online-devices-for-distribution-zones` | Get count of online devices for distribution zones |
| `get-online-devices-for-site-labels` | Get count of online devices for site labels |
| `get-policies-count` | Get Policies count |
| `get-policies-for-security-profile` | Get policies for given security profile |
| `get-policy-by-id` | Get a policy by ID |
| `get-policy-group-by-id` | Get a policy group by ID |
| `get-policy-group-devices` | Search and filter devices for a policy group |
| `get-policy-group-labels` | Search and filter Policy Group Labels |
| `get-policy-group-tree` | Get policy groups as a flat tree list |
| `get-policy-group-workloads` | Search and filter workloads for a policy group |
| `get-policy-groups-assigned-to-policy-set` | Get Policy Groups assigned to Policy Set |
| `get-policy-groups-by-ids` | Search and filter policy groups by ids |
| `get-policy-groups-for-ven` | Get Policy Groups assigned to a VEN |
| `get-policy-groups-json` | Search and filter policy groups |
| `get-policy-groups-summary` | Get Policy Groups summary |
| `get-policy-groups-with-device-groups-for-ven` | Get Policy Groups with Device Names assigned to a VEN |
| `get-policy-set-by-id` | Get a policy set by ID |
| `get-state` | Get paginated policy resource states |
| `get-status` | Get current status of a feature flag |
| `get-template-by-id` | Get a Policy Group Template by ID |
| `get-vendor` | Get a vendor |
| `impact` | List devices currently assigned this label (impact analysis before delete) |
| `import-labels` | Bulk import labels from an XLSX or CSV file (max 3 MB, async) |
| `list` | List labels (paged), with optional folder filter and free-text search on name+description |
| `list-applications` | GET /api/flows/v1/applications |
| `list-get` | List folders for a type with cumulative label counts (folder + descendants) |
| `list-images` | List all images |
| `list-vendors` | List all Vendors |
| `lock-device` | Lock Device by serviceDeviceIds |
| `lock-policy-group` | Lock policy group |
| `lookup` | Resolve a batch of label ids to metadata |
| `lookup-dynamic` | Get Assets that are expected to Match the Dynamic Policy Group |
| `lookup-dynamic-export` | Export Assets that are expected to Match the Dynamic Policy Group to CSV |
| `lookup-dynamic-totals` | Count Assets that are expected to Match the Dynamic Policy Group |
| `lookup-evaluation-endpoint` | Evaluation Endpoint IP lookup |
| `lookup-network` | Get Assets that are expected to Match the Network Policy Group |
| `lookup-network-export` | Export Assets that are expected to Match the Network Policy Group to CSV |
| `move` | Move a folder under a different parent |
| `move-policy-group-scope` | Move a root dynamic policy group between Global/Local scope |
| `overwrite-policy` | Overwrite an inherited/reflection Policy cell and re-cascade |
| `partial-reorder-policy-group` | Reorder (partial) policy group |
| `post-local-policy-group-site` | Save Site Label for creating Local Policy Groups |
| `preview-operation` | Preview the scope of a matrix operation (create / overwrite / delete) before running it |
| `read-by-id` | Read an access policy security profile by ID |
| `read-policy-view` | Read a policy view by ID |
| `read-security-profile` | Read a security profile by ID |
| `remove-definition` | DELETE /api/flows/v1/applications/{id}/definitions/{defId} |
| `rename` | Rename a folder |
| `reorder-siblings` | Reorder a dynamic policy group among its siblings |
| `search-access-policy-security-profile-rules` | Search, filter and page the rules of one Access Policy Security Profile |
| `search-access-policy-security-profiles` | Search, filter and page Access Policy Security Profiles |
| `search-policies-for-policy-set` | Search and filter Policies in given Policy Set: filters in the JSON body |
| `search-security-profiles` | Search, filter and page Security Profiles |
| `search-security-rules` | Search, filter and page the Security Rules of one Security Profile |
| `search-templates` | Search and filter Policy Group Templates |
| `send-state-of-all-devices-to-identity-graph` | Send current state of all Devices to Identity Graph |
| `send-state-of-device-to-identity-graph` | Send current state of the Devices to Identity Graph |
| `toggle-lock-bulk` | Bulk toggle lock/unlock Devices by serviceDeviceIds, creates DelayedTask for each device |
| `unlock-device` | Unlock Device by serviceDeviceIds |
| `unlock-policy-group` | Unlock policy group |
| `update` | Update a label color/description (name is immutable in v1) |
| `update-1` | Update an access policy security profile |
| `update-application` | PUT /api/flows/v1/applications/{id} |
| `update-auto-group-tag-value-settings` | Save Group Tag Value settings |
| `update-coverage-weight-settings` | Save settings for Coverage Weights |
| `update-definition` | PUT /api/flows/v1/applications/{id}/definitions/{defId} |
| `update-dynamic-policy-group` | Update dynamic policy group |
| `update-image` | Update an existing image |
| `update-network-policy-group` | Update network policy group |
| `update-policy` | Update policy |
| `update-policy-group-label` | Update an existing policy group label |
| `update-policy-groups` | Bulk update of Policy Group |
| `update-policy-groups-with-device-groups` | Bulk update of Policy Group with Device Group |
| `update-policy-put` | Bulk update Policy |
| `update-policy-set` | Update Policy Set |
| `update-policy-view` | Update a policy view |
| `update-put` | Update an access policy |
| `update-security-profile` | Update a security profile |
| `update-template` | Update a Policy Group Template |
| `update-vendor` | Update an existing Vendor |
| `validate-application` | POST /api/flows/v1/applications/validate |
| `validate-match-criteria` | Validate Match Criteria |
| `validate-match-criteria-for-existing-policy-group` | Validate Match Criteria for existing Policy Group |
| `validate-policy-group-name` | Validate Policy Group Name |
| `validate-policy-group-name-for-existing-policy-group` | Validate Policy Group Name for existing Policy Group |
| `validate-subnet-dynamic-policy-group` | Validate subnet for Dynamic Policy Group |
| `validate-subnet-static-policy-group` | Validate subnet for Static Policy Group |
| `validate-subnet-static-policy-group-post` | Bulk validate subnet for Static Policy Group |

### system (31 commands)

| Command | Description |
|---------|-------------|
| `ack-execution-of-task` | Acknowledge task without result payload |
| `ack-execution-of-task-post` | Acknowledge task with result payload |
| `cancel-task` | Cancel task |
| `create-snapshot-schedule` | Create snapshot schedule |
| `create-task` | Create a new task |
| `delete-for-ve` | Remove per-VE override |
| `delete-snapshot-schedule` | Delete snapshot schedule |
| `get-all-configs` | Get all task broker configs |
| `get-effective-config` | Get effective config for a VE |
| `get-next-task-for-ve` | Poll next task for VE |
| `get-spec` | Get spec by VE ID |
| `get-spec-by-site-id` | Get specs by site ID |
| `get-spec-group-id` | Get specs by VE group ID |
| `get-task` | Get task by ID |
| `list-specs` | List all specs |
| `list-tasks` | List tasks |
| `pause-snapshot-schedule` | Pause snapshot schedule |
| `register-specs` | Register or update VE specs |
| `release-execution-of-task` | Release task |
| `replace-for-ve` | Replace per-VE disabled task types |
| `replace-tenant-default` | Replace tenant-wide disabled task types |
| `resume-snapshot-schedule` | Resume snapshot schedule |
| `retrieve-snapshot` | Get snapshot by ID |
| `retrieve-snapshot-evidence` | Get snapshot evidence package |
| `retrieve-snapshot-markdown` | Get snapshot Markdown |
| `retrieve-snapshot-pdf` | Get snapshot PDF |
| `retrieve-snapshot-schedule` | Get snapshot schedule by ID |
| `search-snapshot-schedules` | Search snapshot schedules |
| `search-snapshots` | Search snapshots |
| `update-snapshot-schedule` | Update snapshot schedule |
| `update-task` | Update task |

### topology (158 commands)

| Command | Description |
|---------|-------------|
| `ack-registration` | Acknowledge registration of Central VE |
| `batch-create-or-update-multiple-rules` | Bulk create or update rules for given Palo Alto VEN and Firewall |
| `bulk-change-ven-group` | Bulk change Virtual Edge Group for multiple VENs |
| `bulk-create-site-labels` | Bulk create site labels |
| `bulk-delete-cloud-controllers` | Bulk delete Mist cloud controllers |
| `bulk-delete-credentials` | Bulk delete global credentials |
| `bulk-delete-distribution-zone` | Bulk delete Distribution Zones |
| `bulk-delete-site` | Bulk delete site labels. |
| `bulk-delete-site-v2` | Bulk delete site labels |
| `bulk-delete-ve-ns` | Bulk delete Virtual Edge Nodes |
| `bulk-delete-virtual-edges` | Bulk delete Virtual Edges |
| `bulk-force-delete-ve-ns` | Bulk force delete Virtual Edge Nodes |
| `bulk-recommission-ve-ns` | Bulk recommission Virtual Edge Nodes |
| `change-active-ve` | Change Active Virtual Edge for a Virtual Edge Node (VEN) |
| `change-ven-group` | Change Virtual Edge Group for a Virtual Edge Node (VEN) |
| `change-virtual-edge-group` | Change virtual edge group for existing virtual edge |
| `create-cloud-controller` | Create a new cloud controller |
| `create-distribution-zone` | Create Distribution Zones |
| `create-flow-exporter` | Create a flow exporter |
| `create-global-credentials` | Create new global credentials |
| `create-independent-control-mappings` | Create Independent Control Mappings between Distribution Zones |
| `create-or-update-bulk-target-site` | Bulk create or update targets |
| `create-or-update-multiple-rules` | Create or update rules for given Palo Alto VEN and Firewall |
| `create-or-update-target-site` | Create or update target for a specific type |
| `create-site` | Create list of sites. |
| `create-site-label-independent-control-mappings` | Create Independent Control Mappings between Site Labels |
| `create-site-post` | Create site label |
| `create-task-list` | Create a task list |
| `create-ven` | Create a new virtual edge node |
| `create-virtual-edge` | Create new virtual edge |
| `create-virtual-edge-group` | Create new virtual edge group |
| `decommission-virtual-edge-node` | Trigger decommission of a registered virtual edge node |
| `delete-cloud-controller` | Delete Mist cloud controller |
| `delete-distribution-zone` | Delete Distribution Zone |
| `delete-flow-exporter` | Delete a flow exporter |
| `delete-global-credentials` | Delete global credentials |
| `delete-independent-control-mappings` | Delete Independent Control Mappings |
| `delete-site` | Delete site. |
| `delete-site-label-independent-control-mappings` | Delete Independent Control Mappings for Site Labels |
| `delete-site-v2` | Delete site |
| `delete-target-site` | Delete target for a specific type |
| `delete-ven` | Delete virtual edge node |
| `delete-virtual-edge` | Delete existing virtual edge |
| `delete-virtual-edge-group` | Delete existing virtual edge group |
| `disable-maintenance` | Disable Maintenance mode on a Virtual Edge |
| `disable-maintenance-for-group` | Disable Maintenance mode on a batch of Virtual Edges in a group |
| `enable-maintenance` | Enable Maintenance mode on a Virtual Edge |
| `enable-maintenance-for-group` | Enable Maintenance mode on a batch of Virtual Edges in a group |
| `exclude-adjacent-vens` | Exclude adjacent VEN from topology |
| `export-distribution-zones` | Export Distribution Zones as CSV |
| `export-site-labels` | Export site labels as CSV |
| `export-virtual-edge-nodes` | Generate all virtual edge nodes as XLSX |
| `export-virtual-edges` | Generate all virtual edges as XLSX |
| `force-delete-ven` | Force delete a Virtual Edge Node in decommission state |
| `get-all-cloud-controllers` | Get cloud controllers |
| `get-all-distribution-zones` | Get all Distribution Zones |
| `get-all-distribution-zones-get` | Get all Distribution Zones (paginated) |
| `get-all-flow-exporter` | Get all flow exporters |
| `get-all-global-credentials` | Get all global credentials |
| `get-all-sites` | Get all Sites |
| `get-all-sites-v2` | Get all Sites (paginated) |
| `get-all-tags` | Get all Tags used for Site Labels |
| `get-all-target-sites` | Get all configured deployment targets |
| `get-all-ve-ns-for-global-credentials` | Get Virtual Edge Nodes using a global credential |
| `get-configuration` | Get VEN configuration |
| `get-dashboard-count` | Get VE and VEN dashboard count |
| `get-dashboard-metrics` | Get VE and VEN dashboard metrics |
| `get-details` | Get VEN details |
| `get-distribution-zone` | Get single Distribution Zone |
| `get-flow-exporter` | Get a single flow exporter |
| `get-global-interfaces-settings` | Get global interface settings |
| `get-independent-control-mappings` | Get all Independent Control Mappings for Distribution Zones |
| `get-logger` | Get logger level |
| `get-loggers-for-all-virtual-edges` | Get loggers for all virtual edges |
| `get-manifest` | Get manifest with versions for Central VE |
| `get-metrics` | Get VEN metrics |
| `get-permissions` | Get VEN permissions |
| `get-ports-configuration` | Get ports configuration for a VEN |
| `get-reconciled-variables` | Reconciled environment variables for a VE |
| `get-settings` | Get topology settings |
| `get-single-ven` | Get single Virtual Edge Node |
| `get-site` | Get single Site |
| `get-site-count` | Get site count |
| `get-site-count-v2` | Get site count |
| `get-site-label-independent-control-mappings` | Get all Independent Control Mappings for Site Labels |
| `get-site-v2` | Get single Site |
| `get-status` | Get VEN status |
| `get-target-site` | Get target for a specific type |
| `get-target-site-history` | Retrieves the full history for a specific target type. |
| `get-target-types` | Get all available target types |
| `get-topology` | Get topology for a VEN |
| `get-ve-ns-overview-response` | Returns a non-paginated overview, having name and status, of Virtual Edge Nodes. |
| `get-ve-variables` | Download variables for a VE |
| `get-virtual-edge` | Search and filter virtual edge |
| `get-virtual-edge-by-id` | Get a virtual edge by ID |
| `get-virtual-edge-by-post` | Search and filter virtual edge |
| `get-virtual-edge-by-post-post` | Search and filter virtual edge group |
| `get-virtual-edge-get` | Search and filter Virtual Edge Group |
| `get-virtual-edge-group-by-id` | Get a virtual edge group by ID |
| `get-virtual-edge-node-firewall-rules` | List of Firewalls and Firewall rules for given Virtual Edge Node with pagination |
| `get-virtual-edge-nodes` | List Virtual Edge Nodes with pagination and sorting |
| `get-virtual-edge-nodes-by-post` | List Virtual Edge Nodes with pagination and sorting |
| `get-virtual-edge-nodes-for-distribution-zone` | Get all Virtual Edge Nodes for a Distribution Zone |
| `get-virtual-edge-nodes-metrics-summary` | Aggregated VEN counts grouped per dimension (metrics summary) |
| `get-virtual-edges-metrics-summary` | Aggregated VE counts grouped per dimension (metrics summary) |
| `get-workload-distribution-zone-usage` | Report whether a Workload Distribution Zone is referenced by any workload-discovery connector endpoint |
| `heartbeat` | Register heartbeat for a VE |
| `heartbeat-post` | Register heartbeat from virtual edge node |
| `is-imbalanced` | Check if Virtual Edge Group is imbalanced |
| `list-workload-distribution-zones` | List Workload Distribution Zones known to Identity Graph |
| `metrics` | Publish operational metrics for a VE |
| `metrics-post` | Publish operational metrics for a VEN |
| `patch-virtual-edge-group` | Partial-update of a virtual edge group |
| `publish-ve-variables` | Publish variables for a VE |
| `re-initialize-virtual-edge-node` | Trigger re-initialization of a unsuccessful recommission or onboard |
| `rebalance-virtual-edge-group` | Rebalance Virtual Edge Group |
| `recommission-virtual-edge-node` | Trigger recommission of a decommissioned virtual edge node |
| `rediscover-adjacent-vens` | Rediscover adjacent VENs and recreate missing ones |
| `register` | Register a VE |
| `register-ven` | Register virtual edge node |
| `search-virtual-edge-nodes` | List Virtual Edge Nodes with pagination and sorting |
| `set-logger-level` | Set logger level |
| `set-logger-levels-bulk` | Set logger levels in bulk |
| `set-version` | Set desired version in manifest of Central VE for nodeId |
| `sxp-password-regenerate` | Regenerate SXP password for Virtual Edge Node |
| `topology` | Publish topology seen from a VEN |
| `update-cloud-controller` | Update cloud controller |
| `update-distribution-zone` | Update Distribution Zone |
| `update-flow-exporter` | Update a flow exporter |
| `update-global-credentials` | Update global credentials |
| `update-global-interfaces-settings` | Update global interface settings |
| `update-interfaces-settings` | Update interface settings by ID (deprecated) |
| `update-ports-configuration` | Update ports configuration for a VEN |
| `update-settings` | Update topology settings |
| `update-site` | Update site |
| `update-site-put` | Update site. |
| `update-site-put-2` | Update site. |
| `update-target-site-by-id` | Updates an existing target site entry by ID (for active or future entries). |
| `update-task-list` | Update a task list |
| `update-task-status` | Update task status report |
| `update-ven` | Update existing virtual edge node |
| `update-virtual-edge` | Update existing virtual edge |
| `update-virtual-edge-group` | Update existing virtual edge group |
| `update-virtual-edge-post` | Regenerate OTP for existing virtual edge |
| `update-virtual-edge-put` | Override OTP for existing virtual edge |
| `upload-virtual-edge-nodes-bulk-json` | Bulk upload VEN rows (V2, JSON streaming) |
| `upload-virtual-edges-bulk-json` | Bulk upload VE rows (V2, JSON streaming) |
| `use-default-logger-level` | Reset logger to default level |
| `validate-virtual-edge-bulk-delete` | Validate Virtual Edges before bulk delete |
| `validate-virtual-edge-bulk-upload` | Validate XLSX file for Virtual Edge bulk upload |
| `validate-virtual-edge-node-bulk-delete` | Validate Virtual Edge Nodes before bulk delete |
| `validate-virtual-edge-nodes-bulk-json` | Validate VEN rows for bulk upload (V2, JSON streaming) |
| `validate-virtual-edge-nodes-bulk-update` | Bulk update VEN credentials |
| `validate-virtual-edge-nodes-bulk-upload` | Validate XLSX file for Virtual Edge Node bulk upload |
| `validate-virtual-edges-bulk-json` | Validate VE rows for bulk upload (V2, JSON streaming) |
| `virtual-edge-bulk-change-group` | Bulk change Virtual Edge group |
| `virtual-edge-bulk-upload` | Bulk upload Virtual Edges from XLSX file |
| `virtual-edge-node-bulk-upload` | Bulk upload Virtual Edge Nodes from XLSX file |

---

## Global Options

All API commands support these hidden flags:

| Flag | Description |
|------|-------------|
| `--format`, `-f` | Output format override: `json`, `table`, `yaml`, `csv` |
| `--query`, `-q` | JMESPath query to filter/reshape output |

Mutating commands (`POST`, `PUT`, `PATCH`) accept:

| Flag | Description |
|------|-------------|
| `--body JSON` | Request body as inline JSON string |
| `--body-file PATH` | Read request body from a JSON file |

Destructive commands require `--confirm` to execute. That is every `DELETE`, plus
any verb whose API path names a destructive action — bulk deletes over POST,
`decommission` over PUT, and the Insights `reset-to-default` / `recreate`
commands. Dry-run paths (`.../bulk/delete/validate`) are deliberately not gated.
