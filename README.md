# Elisity CCC CLI

[![tests](https://github.com/mkorenbaum/elisity-cli/actions/workflows/test.yml/badge.svg)](https://github.com/mkorenbaum/elisity-cli/actions/workflows/test.yml)

Command-line interface to the Elisity Cloud Control Center (CCC) API. Provides complete coverage of the CCC API surface — all 631 REST endpoints from the OpenAPI spec, plus 17 hand-coded GraphQL commands for the `/api/reporting/v1/data` endpoint (Zero Trust scores, threat vectors, per-site KPIs, traffic vectors) that the OpenAPI spec doesn't include, plus a 3-command CLI-native `glossary` group that maps Elisity UI terminology to CLI commands.

Generated from the **CCC 26.9 (hot-patched)** OpenAPI spec: the published 26.9 spec plus a checked-in overlay for the device PATCH that 26.9 tenants are hot-patched to serve, so `devices update-device` sends **PATCH**. See [What changed in CCC 26.9](#what-changed-in-ccc-269) for the command-level delta, and [What changed in CCC 26.7](#what-changed-in-ccc-267) for the release before it.

> **For AI agents:** see [docs/AGENTS.md](docs/AGENTS.md) for a UI-term → CLI-command operating guide. The `elisity glossary` group is the runtime lookup surface.

## Features

- **658 commands** total (631 auto-generated from the CCC OpenAPI spec + 17 hand-coded GraphQL reporting commands + 7 CLI-native auth/config + 3 CLI-native glossary commands)
- **Multi-profile configuration** — manage multiple CCC environments (prod, staging, lab)
- **4 output formats** — JSON (default), table, YAML, CSV
- **JMESPath filtering** — reshape and filter output with `-q` expressions
- **OAuth2 authentication** — client_credentials grant with auto-refresh
- **NDJSON support** — transparent parsing of newline-delimited JSON endpoints
- **GraphQL reporting** — `reporting` group wraps the CCC dashboard's GraphQL queries (Zero Trust scores, site KPIs, threat vectors, traffic-by-PG/IP)
- **UI-term glossary** — `glossary` group answers "what command runs the Zero Trust Score tile?" without guesswork
- **Destructive-op safety** — `--confirm` required for all 68 destructive commands, classified by API path rather than HTTP verb (every DELETE, plus POST bulk deletes, PUT decommission, Insights reset/recreate, and the AD groups "master reset")
- **Retry with backoff** — automatic retry on connection errors and timeouts

## Quick Start

```bash
# Clone
git clone https://github.com/mkorenbaum/elisity-cli.git
cd elisity-cli

# Install (use a venv — modern Ubuntu/Debian block system-wide pip per PEP 668)
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Configure
elisity config set-profile myenv \
  --base-url https://your-ccc.idp01.elisity.io \
  --client-id YOUR_CLIENT_ID \
  --client-secret 'YOUR_CLIENT_SECRET'

# Verify
elisity auth test

# What command runs the "Zero Trust Score" tile in the UI?
elisity glossary explain "Zero Trust score"
```

**Or use environment variables:**

```bash
export CCC_BASE_URL=https://your-ccc.idp01.elisity.io
export CCC_CLIENT_ID=your-client-id
export CCC_CLIENT_SECRET='your-client-secret'
elisity auth test
```

> **For agents and humans new to Elisity:** read **[docs/user-guide.md](docs/user-guide.md)** before doing real work. It is the workflow-oriented guide and has worked examples for the most common queries (devices per site, VEN inventory, posture score, flow search, scripting). The README below is reference material; the user guide is the tutorial. AI agents should additionally read [docs/AGENTS.md](docs/AGENTS.md).

## Usage

```bash
# List sites
elisity topology get-all-sites

# List sites as a table
elisity -f table topology get-all-sites

# Extract just site names
elisity topology get-all-sites -q '[].name'

# View devices (paginated — note nested 'pageable' wrapper)
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":10}}'

# List policy sets
elisity policy get-all-as-nd-json

# Get a specific site by ID
elisity topology get-site-v2 <SITE_ID>

# Delete a site (requires confirmation)
elisity topology delete-site-v2 <SITE_ID> --confirm

# Tenant Zero Trust score (GraphQL reporting endpoint, not in OpenAPI spec)
elisity reporting get-aggregate-enforcement-score

# Per-site KPI dashboard (devices, VENs, policy counts, enforcement score)
elisity -f table reporting get-site-kpis

# Map UI term → CLI command
elisity glossary search "monitor mode"
elisity glossary explain "VEN"

# Get bearer token for use in scripts
TOKEN=$(elisity auth token)
curl -H "Authorization: Bearer $TOKEN" https://your-ccc.idp01.elisity.io/api/topology/v2/sites
```

## Command Groups

| Group | Commands | Description |
|-------|----------|-------------|
| `topology` | 158 | Sites, distribution zones, workload distribution zones, VE groups, VEs, VENs, VE/VEN metrics summaries, flow exporters, cloud controllers, interface + topology settings |
| `policy` | 191 | Policy sets, policies, policy groups, security profiles + access policy security profiles (search/export), policy reviews, site labels, label management, access policy (LPA), custom applications, vendors |
| `devices` | 107 | Device CRUD, bulk operations, enrichment, suppression list, custom attributes, cloud workloads + AWS and Azure discovery, workload attach |
| `ad` | 57 | Active Directory / Entra ID connectors, agents (V2), agent logs, subscription refresh, AD group enablement |
| `connectors` | 38 | Connector configuration, custom connector devices/inventory, import/export, connectivity, Tanium sensor mappings |
| `insights` | 31 | Policy suggestions, dynamic/network group recommendations |
| `flows` | 18 | Traffic flow search, device state, noise definitions, device heatmap, flow ingestion |
| `system` | 31 | Tasks, specs, state sync, task broker config, report snapshots (PDF, Markdown, evidence) + schedules |
| `reporting` | 17 | **GraphQL** — Zero Trust scores, site KPIs, threat vectors, traffic-by-PG/IP. Hand-coded (the CCC reporting API is GraphQL, not in OpenAPI). |
| `glossary` | 3 | Map Elisity UI terminology to CLI commands |
| `auth` | 3 | Test connection, get token, decode JWT |
| `config` | 4 | Profile management, configuration display |

**Explore any group:**

```bash
elisity --help                    # All groups
elisity topology --help           # All topology commands
elisity topology get-site-v2 --help  # Command-specific help
elisity glossary list             # All glossary terms
```

## Output Formats

```bash
elisity topology get-all-sites                    # JSON (default)
elisity -f table topology get-all-sites           # Rich terminal table
elisity -f yaml topology get-all-sites            # YAML
elisity -f csv topology get-all-sites             # CSV with headers
```

## JMESPath Queries

```bash
# Site names only
elisity topology get-all-sites -q '[].name'

# Count items
elisity topology get-all-sites -q 'length(@)'

# Filter by field
elisity topology get-virtual-edge -q 'content[?status==`ACTIVE`]'

# Select specific fields
elisity topology get-all-sites -q '[].{name: name, id: id}'

# First 3 results
elisity topology get-all-sites -q '[0:3]'
```

## Multi-Environment Profiles

```bash
# Create profiles for different environments
elisity config set-profile prod --base-url https://prod.idp01.elisity.io --client-id ID --client-secret SECRET
elisity config set-profile lab  --base-url https://lab.idp01.elisity.io  --client-id ID --client-secret SECRET

# Switch between them
elisity config use-profile prod
elisity config use-profile lab

# Or use -p flag for one-off commands
elisity -p lab topology get-all-sites

# List all profiles
elisity config list-profiles

# Show active config (secrets redacted)
elisity config show
```

## Requirements

- Python 3.10+
- Network access to a CCC instance
- OAuth2 service account credentials (client ID + secret)

## Dependencies

- [Click](https://click.palletsprojects.com/) — CLI framework
- [Requests](https://requests.readthedocs.io/) — HTTP client
- [Tenacity](https://tenacity.readthedocs.io/) — Retry logic
- [Rich](https://rich.readthedocs.io/) — Terminal table rendering
- [PyYAML](https://pyyaml.org/) — YAML output and config parsing
- [JMESPath](https://jmespath.org/) — Query language for JSON

## Development

```bash
# Clone and install in dev mode
git clone <repo-url>
cd elisity-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest

# Run QA validation against a live CCC
python3 tests/qa_comprehensive.py
```

### Regenerating commands from a new CCC OpenAPI spec

The API-backed groups are generated from the CCC OpenAPI specification, pulled from a
live tenant at `GET /v3/api-docs` (served unauthenticated). The current command set was
generated from the **CCC 26.9** spec — OpenAPI 3.1.0, 487 paths / 631 operations —
captured from `release-demos.idp02.elisity.io` (built on release-26.9.0, 2026-10-10) on
2026-10-15, plus the 26.9 hot-patch overlay (one operation, the device `PATCH`; see
[Spec overlays](#spec-overlays)). The previous set came from the CCC 26.7 spec (OpenAPI 3.1.0, 441 paths / 583
operations, captured from `insights-demo.idp01.elisity.io` on 2026-08-05), and the one
before that from the CCC 26.3-era spec (OpenAPI 3.0.1, 329 paths / 436 operations,
captured 2026-06-21).

> **The spec carries no CCC version stamp.** `info.version` reads `1.0.0` in 26.3, 26.7
> and 26.9 — that is the gateway API version and it does not track the CCC release. The
> CCC version above is cited from the tenant the spec was pulled from, so record that
> provenance whenever you refresh the baseline.

**Always diff before you regenerate.** The diff is what makes a version bump reviewable:

```bash
# 1. What changed between the two specs?
python3 tools/spec_diff.py old-api-docs.json new-api-docs.json

# Machine-readable form, and a mode that fails when a new tag has no group mapping
python3 tools/spec_diff.py old-api-docs.json new-api-docs.json --json > diff.json
python3 tools/spec_diff.py old-api-docs.json new-api-docs.json --strict
```

`spec_diff.py` reports added, removed and changed operations — including parameter
type/required changes, request-body and response schema changes (resolved through
`$ref`, so a change *inside* a referenced schema is visible), and the CLI command each
operation becomes. New tags with no `TAG_TO_GROUP` entry are surfaced separately: they
fall back to a path-prefix guess and need an explicit mapping decision.

```bash
# 2. Map any new tags in TAG_TO_GROUP (generate_commands.py), then regenerate.
python3 generate_commands.py --spec new-api-docs.json

# CCC 26.9 needs its hot-patch overlay (see "Spec overlays" below). Pass the same
# --overlay to spec_diff.py so the diff describes what the CLI ships.
python3 generate_commands.py --spec api-docs-26.9.json \
    --overlay spec-overlays/ccc-26.9-hotpatch-device-patch.json

# The spec path resolves as: --spec > $ELISITY_API_SPEC > the historical host path
ELISITY_API_SPEC=new-api-docs.json python3 generate_commands.py

# 3. Regenerate the changelog section of this README from the same diff.
python3 tools/gen_changelog.py --diff diff.json --version 26.10 \
    --source your-tenant.idp01.elisity.io --baseline 26.9

# 4. Refresh the committed naming skeleton, so the naming guards run in CI
#    (the full specs are not committed).
python3 tools/spec_skeleton.py new-api-docs.json --source your-tenant.idp01.elisity.io \
    > tests/data/ccc-26.10-operations.json

# 5. Confirm counts, the delete gate, and the docs all still agree.
python3 tools/audit_counts.py
pytest
```

The test that regenerates from the 26.9 spec and compares the result byte-for-byte with
the committed modules needs the full spec, which is not committed; without it the test
skips. Set `ELISITY_REQUIRE_SPECS=1` wherever the specs are staged (a release check, a
regeneration) and a missing spec fails the run instead of skipping.

**The generator refuses to run if any spec tag has no `TAG_TO_GROUP` entry**, printing
each unmapped tag, its operation count, and the group the path-prefix fallback would
otherwise have picked. This is deliberate: an unmapped tag is not a loud failure, it is
a silent misrouting. CCC 26.7 renamed 16 tags, and six `Connectors Configurations`
operations moved from `connectors` to `devices` that way while the totals stayed
entirely plausible. Map the tag, then regenerate.

The changelog is generated from the diff rather than hand-written, because a
hand-maintained list of ~200 command changes drifts the first time anyone regenerates.

`audit_counts.py` walks the source tree and emits the authoritative numbers — total,
per group, generated vs hand-coded, delete commands and `--confirm` coverage. It exits
non-zero when `README.md` or `docs/command-reference.md` disagree with the source, so
documentation drift fails CI instead of accumulating. It is also enforced from the test
suite (`tests/test_command_invariants.py`).

#### Spec overlays

A tenant can serve an operation its published spec does not declare yet — CCC 26.9
tenants are hot-patched to serve `PATCH /api/identity-graph/v1/devices/{id}`
(ENG-31142), which the 26.9 spec predates. `spec-overlays/*.json` add such operations at
generation time. Each file records its `provenance` and lists operations as
`{"path", "method", "cloneFrom", "set"}`: the generator copies the `cloneFrom`
operation at that path, replaces the keys in `set`, marks the copy with
`x-elisity-overlay`, and adds it. If the spec already declares the operation, the
spec's definition wins and the overlay entry is skipped with a note; if the operation
it clones is missing, generation fails.

The CLI omits the device `PUT` (`OMITTED_OPERATIONS`) because the `PATCH` replaces it.
Generation fails when a spec has an omitted operation but not its replacement, so
regenerating 26.9 without the overlay is an error, not a CLI that has quietly lost
`update-device`. Delete the overlay once the published spec declares the PATCH.

Two invariants are enforced mechanically because a bulk regeneration is too large to
review by eye:

- **Confirm gate** — every DESTRUCTIVE command requires `--confirm`, not merely every
  DELETE. The denominator is derived from the API path (`is_destructive_operation()` in
  `generate_commands.py`, the single definition in the project) and re-derived from the
  shipped source by the audit, so the gate and the metric cannot measure different sets.
  Coverage is asserted at 100% over 68 commands; a regression names the offending
  commands. A command whose *name* reads destructive while its path does not classify is
  also a failure until a human rules on it in `NON_DESTRUCTIVE_DESPITE_NAME` — three
  entries today, all dry-run or resync operations.
- **Hand-coded survival** — the `reporting` (GraphQL) and `glossary` (CLI-native) groups
  are not in the OpenAPI spec. Regeneration never rewrites their modules and always
  keeps them registered in `COMMAND_GROUPS`; the generator aborts if a spec tag is ever
  mapped onto one of them.

## What changed in CCC 26.9

The command set is generated from the CCC 26.9 OpenAPI spec, pulled from `release-demos.idp02.elisity.io`, with the 26.9 hot-patch overlay applied (see below). The previous set came from the 26.7 spec.

Provenance: `GET /v3/api-docs` on `release-demos.idp02.elisity.io` on 2026-10-15; that tenant was built on release-26.9.0 (2026-10-10). The spec itself carries no CCC version stamp (`info.version` is `1.0.0`).

| | 26.7 | 26.9 |
|---|---:|---:|
| Spec paths | 441 | 487 |
| Spec operations | 583 | 631 |
| Hot-patch overlay operations | — | 1 |
| Generated REST commands | 583 | 631 |

**49 commands added, 1 removed, 84 operations changed**, and `devices update-device` changed HTTP method.

### `devices update-device` sends PATCH (26.9 hot patch)

`elisity devices update-device <id>` now sends `PATCH /api/identity-graph/v1/devices/{id}` (ENG-31333). The CLI no longer has a command for the device `PUT`.

- **Why.** PUT replaces the device's IP and VEN, so an attribute-only body detached a dynamically attached device. With PATCH, an omitted, `null` or empty `ip` / `venId` keeps the current value, and attributes merge into the target enrichment layer. Same permission and `If-Match` precondition as PUT; returns 204.
- **Which tenants.** `update-device` needs a CCC 26.9 tenant with the ENG-31142 hot patch (Elisity/ccc PR #17262), or a later release that ships the PATCH. It fails, most likely with 405 Method Not Allowed, on CCC 26.7 tenants (the 26.7 spec has only PUT and DELETE at that path) and on 26.9 tenants without the hot patch. There is no PUT fallback, so check the tenant's release before you rely on it.
- **Where the PATCH comes from.** The published 26.9 spec predates the hot patch and declares only `PUT` and `DELETE` at that path. The generator adds the PATCH from [`spec-overlays/ccc-26.9-hotpatch-device-patch.json`](spec-overlays/ccc-26.9-hotpatch-device-patch.json), cloned from the PUT (parameters, request body), with its provenance recorded in the overlay. Without `--overlay` the generator refuses the 26.9 spec rather than silently dropping `update-device`.
- `--target-enrichment-layer` now reaches the request: generated PATCH commands pass query parameters through.
- The overlay makes `spec_diff.py` list the PATCH as an added `devices update-device`. It is not new: the command existed and now uses a different method, so it is not counted in the 49 additions below.

**`ad set-groups-default-enabled` requires `--confirm`.** The spec calls it a "master reset" of the enable-all-groups default, so it is gated like the other destructive commands (68 in total).

### Removed commands (breaking)

This command is gone because the operation was removed from the CCC spec. Any script invoking one will now fail with `No such command`. Commands whose underlying *path* moved are not listed here — they still exist, and are under [Changed command signatures](#changed-command-signatures).

**site-label-controller** (1)

- `elisity policy is-site-label-in-use` — Is Site Label used



### Changed command signatures

5 commands changed shape — a renamed command or a changed flag can break an existing script.

**`devices`**

- `elisity devices search-suppression-list` — renamed from `get-users`; new required `--filters` (object). CCC 26.9 renamed the operationId `getUsers` -> `search`; the CLI names it after what it lists (suppression-list entries, not users) instead of shipping a bare `devices search`.

**`system`**

- `elisity system retrieve-snapshot-pdf` — renamed from `retrieve-snapshot-image`
- `elisity system search-snapshot-schedules` — new optional `--source` (string); dropped `--dashboard`
- `elisity system search-snapshots` — new optional `--source` (string); dropped `--dashboard`

**`topology`**

- `elisity topology get-all-distribution-zones` — new optional `--includeWorkload` (boolean)


### Changed request bodies

25 commands take a different request body. The command's flags are unchanged — the body is passed as opaque JSON via `--body` / `--body-file` — but the JSON you send must match the new schema.

- **`ad`** — `save-ad-agent-config`
- **`devices`** — `validate-permissions-pre-creation`
- **`policy`** — `bulk-create`, `create`, `create-dynamic-policy-group`, `create-dynamic-policy-groups`, `create-policy`, `create-policy-post`, `create-security-profile`, `create-security-profiles`, `export-policies-to-csv`, `overwrite-policy`, `update`, `update-dynamic-policy-group`
- **`system`** — `create-snapshot-schedule`, `create-task`
- **`topology`** — `create-distribution-zone`, `create-ven`, `metrics`, `metrics-post`, `register-ven`, `update-distribution-zone`, `update-global-interfaces-settings`, `update-interfaces-settings`, `update-ven`


A further 54 operations changed only in their response schema or status codes. Invocation is unaffected, so they are not listed.

### Added commands

49 new commands, grouped by CLI group.

Where the operationId gave a name that was generic in its group (`devices list`, `devices usage`, `devices export`), carried a dedupe suffix (`validate-permissions-pre-creation-post`), or took a shipped name, the CLI sets the name per operation in `COMMAND_NAME_OVERRIDES` (`generate_commands.py`). In particular, 26.9's new `/v1/workloads/attach` and `/v1/workloads/attached` carry the operationIds `attach` / `attached`, which would have moved the existing `devices attach` / `devices attached` to `attach-post` / `attached-post`. Those device commands keep their names; the workload calls are `attach-workload` / `attach-workloads`.

#### `ad` (+8)

- `export-groups` — Generate groups export as XLSX
- `get-group-devices` — Get devices that are direct members of a group
- `get-group-users` — Get users that are direct members of a group
- `get-groups-count` — Get groups count
- `get-groups-default-enabled` — Get the 'enable all groups by default' toggle
- `get-groups-view` — Get groups view
- `set-groups-default-enabled` — Set the 'enable all groups by default' toggle (master reset)
- `set-groups-enabled` — Enable or disable one or many groups

#### `connectors` (+3)

- `fetch-tanium-sensor-catalog` — Fetch the Tanium sensor catalog
- `fetch-tanium-sensor-detail` — Look up one Tanium sensor by exact name
- `probe-tanium-sensor-mapping` — Probe a draft sensor mapping

#### `devices` (+18)

- `attach-workload` — Attach a workload reported by a VEN, creating it if it does not exist
- `attach-workloads` — Attach a batch of workloads reported by a VEN
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
- `validate-azure-connection-existing` — Validate the Azure connection of an existing endpoint, optionally with edited credentials
- `validate-azure-connection-pre-creation` — Validate Azure connection for a new endpoint (pre-creation)
- `validate-azure-permissions-existing` — Validate Azure permissions for an existing connector endpoint
- `validate-azure-permissions-pre-creation` — Validate Azure permissions for a new endpoint (pre-creation)
- `validate-azure-region-permissions-existing` — Validate an existing endpoint's region filter against its subscriptions
- `validate-azure-region-permissions-pre-creation` — Validate a new endpoint's region filter against its subscriptions (pre-creation)

#### `flows` (+3)

- `accept-app-flow-data` — `POST /flow/api/appflowdata`
- `accept-flow-data` — `POST /flow/api/flowdata`
- `accept-flows` — `POST /api/flows/v1/flows`

#### `policy` (+11)

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

#### `system` (+2)

- `retrieve-snapshot-evidence` — Get snapshot evidence package
- `retrieve-snapshot-markdown` — Get snapshot Markdown

#### `topology` (+4)

- `get-virtual-edge-nodes-metrics-summary` — Aggregated VEN counts grouped per dimension (metrics summary)
- `get-virtual-edges-metrics-summary` — Aggregated VE counts grouped per dimension (metrics summary)
- `get-workload-distribution-zone-usage` — Report whether a Workload Distribution Zone is referenced by any workload-discovery connector endpoint
- `list-workload-distribution-zones` — List Workload Distribution Zones known to Identity Graph

## What changed in CCC 26.7

The command set is generated from the CCC 26.7 OpenAPI spec, pulled from `insights-demo.idp01.elisity.io`. The previous set came from the 26.3 spec.

| | 26.3 | 26.7 |
|---|---:|---:|
| Spec paths | 329 | 441 |
| Spec operations | 436 | 583 |

**190 commands added, 42 removed, 276 operations changed, 1 command name(s) repointed at a different endpoint.**

### GraphQL `reporting` changes (breaking)

The `reporting` group is hand-coded against the CCC GraphQL endpoint
(`/api/reporting/v1/data`), which is not in the OpenAPI spec — so it is **not**
regenerated by a spec bump. CCC 26.7 changed that GraphQL schema underneath it,
which no static check in this repo could see: the suite passed, the spec diff was
clean, and the commands below failed only when executed against a live 26.7
tenant. `tools/gql_schema_check.py` + `tests/test_reporting_graphql_schema.py`
now validate every reporting query against a staged introspection of the live
schema, so the next drift fails the suite instead of shipping.

- **`get-zero-trust-metrics` — fixed, twice.** Two separate 26.7 changes broke
  this query, one layer apart.

  *Arguments.* The per-device selectors moved out of `zeroTrustMetrics`'s
  top-level arguments into a `ZeroTrustFilters` input object; passing
  `macAddress` at the top level is rejected with
  `Validation error (UnknownArgument@[policyMetrics/zeroTrustMetrics])`. The
  argument now travels in `filters`, and a new repeatable `--mac-address`
  option exposes it (it implies `--include-mac`). `list-snapshots` shares this
  query and is fixed by the same change.

  *Selection set.* `avgDeviceCoverage` and `avgPolicyCoverage` no longer exist
  on `ZeroTrustMetrics`
  (`FieldUndefined@[policyMetrics/zeroTrustMetrics/avgDeviceCoverage]`). This is
  a **reshape, not a rename**: the coverage numbers now live inside a nested
  `policyDeploymentMetrics` object. The command selects `deviceCoverage` and
  `policyDeviceCoverage` from it and returns the object **as the server shapes
  it** — deliberately not flattened back onto the row under the old names,
  because nothing in 26.7 states the new fields are the same measurement on the
  same 0–100 scale. **Any script reading `.avgDeviceCoverage` must be repointed
  at `.policyDeploymentMetrics.deviceCoverage`, and any threshold written for
  the old scale must be re-checked against real output.**

  The other four `policyDeploymentMetrics` fields (`policyWorkloadCoverage`,
  `workloadCoverage`, `devicePolicyCounts`, `workloadPolicyCounts`) are not
  selected: the introspection available carried field names but not type kinds,
  and selecting an object field without a sub-selection fails validation for the
  whole query.

- **`diagnose-low-score` — REMOVED.** It filtered on
  `avgDeviceCoverage < threshold OR avgPolicyCoverage < threshold`, and both
  fields are gone. It was not re-pointed at the nested replacements because two
  things about them cannot be established without a live tenant: their **units**
  (`--threshold` is documented and defaulted as a percentage — a 0.0–1.0
  fraction would flag every group in the tenant) and the **row grain** to
  aggregate over. Since the command existed precisely to stop an agent
  recommending `policy change-status` for a group that has no policy, a
  mis-scaled version would produce exactly the failure it was built to prevent.
  Same rule as the two removals below. The manual equivalent — take a low row's
  `policyGroupId`, then read the `monitorMode` of the policies referencing it
  via `policy get-all-policies-as-nd-json` — is documented in
  [docs/AGENTS.md](docs/AGENTS.md#diagnosing-a-lowzero-zero-trust-score-do-not-guess-the-cause)
  and in `get-zero-trust-metrics --help`.
- **`get-policy-count-needed` — REMOVED.** `policyMetrics.countNeeded` no longer
  exists in 26.7 (`FieldUndefined`). It was not rewritten onto `coverage`:
  coverage answers "how covered are the policy groups I have", not "how many
  more policies are needed", and a plausible-but-wrong number is worse than an
  absent command. Any script invoking it now fails with `No such command`.
- **`get-policy-set-enforcement-score` — REMOVED.**
  `policyMetrics.policySetEnforcementScore` no longer exists in 26.7
  (`FieldUndefined`). No 26.7 field answers "enforcement score for one policy
  set". Closest surviving surfaces: `get-aggregate-enforcement-score`
  (tenant-wide), `get-site-kpis` (`policyEnforcementScore` per site), and
  `get-zero-trust-metrics` (per policy group). Confirmed against live 26.7
  introspection: `PolicyMetrics` carries exactly `count`, `coverage`,
  `aggregatePolicyEnforcementScore`, `policyGroups`, `zeroTrustMetrics` — there
  is no `policySetEnforcementScore` on it.

The `reporting` group is therefore **17 commands**, down from 20.

`tools/gql_schema_check.py` was extended in the same round: it now validates
**selection sets and nested fields**, not just arguments, and resolves named and
inline fragments against their type condition. The first version passed the
query the server rejected — `zeroTrustMetrics`'s arguments were correct, and the
fields underneath it were filed as "unverified" because `ZeroTrustMetrics` had
never been staged. It now reports coverage over **field paths** rather than
queries, and fails outright if staging for a type a shipped query selects on
goes missing, so the denominator cannot quietly shrink again.

### Removed commands (breaking)

These 42 commands are gone because the operation was removed from the CCC spec. Any script invoking one will now fail with `No such command`. Commands whose underlying *path* moved are not listed here — they still exist, and are under [Changed command signatures](#changed-command-signatures).

**AD Agent** (1)

- `elisity ad migrate-old-ad-agent-config` — Migrate old config for specific AD Agent

**AD Device** (8)

- `elisity ad add-device-ad` — Add AD device
- `elisity ad attach-device` — Attach AD device
- `elisity ad delete-device-ad` — Delete AD device
- `elisity ad detach-device` — Detach AD device
- `elisity ad get-device` — Get AD device
- `elisity ad get-device-by-sid-and-domain` — Get AD device by SID and Domain
- `elisity ad refresh-device` — Refresh AD device
- `elisity ad update-device-ad` — Update AD device

**AD Domain** (1)

- `elisity ad delete-domain-data` — Delete all data related to the domain

**AD Group** (7)

- `elisity ad create-group-post` — Add AD group
- `elisity ad delete-group` — Delete AD group
- `elisity ad delete-group-delete` — Delete AD group
- `elisity ad get-group-by-sid-and-domain` — Get AD group by SID and Domain
- `elisity ad get-groups-view` — Get groups view
- `elisity ad update-group` — Update AD group
- `elisity ad update-group-put` — Update AD group

**AD Member** (2)

- `elisity ad create-group` — Update memberOf
- `elisity ad create-group-delete` — Delete memberOf

**AD User** (7)

- `elisity ad attach-user` — Attach AD user
- `elisity ad create-user` — Add AD user
- `elisity ad delete-user` — Delete AD user
- `elisity ad detach-user` — Detach AD user
- `elisity ad get-user-by-sid-and-domain` — Get AD user by SID and Domain
- `elisity ad refresh-user` — Refresh AD user
- `elisity ad update-user` — Update AD user

**DC Status** (1)

- `elisity ad process-dc-status` — Process DcStatus

**Device State Cache** (7)

- `elisity flows dump-all` — Get complete history for all devices
- `elisity flows dump-latest` — Get latest data for all devices
- `elisity flows get-device-data-history` — Get complete device data history
- `elisity flows get-device-data-in-time-range` — Get device data history in time range
- `elisity flows get-floor-data` — Get device data at or before timestamp
- `elisity flows get-latest-data` — Get latest device data
- `elisity flows get-latest-data-backward-compatible` — Get latest device data - backward compatible

**Policy Set** (3)

- `elisity policy get-enforcement-score` — Get Policy Enforcement Score With Info
- `elisity policy get-enforcement-score-weight-settings` — Get settings for Policy Enforcement Score Weights
- `elisity policy update-enforcement-score-weight-settings` — Save settings for Policy Enforcement Score Weights

**State Sync** (3)

- `elisity policy e-discovery-distribution-zones-state-sync` — Sends all Distribution Zones to eDiscovery.state-sync topic.
- `elisity policy e-discovery-sites-state-sync` — Sends all Sites to eDiscovery.state-sync topic.
- `elisity policy resync-state` — Sends details of all the VE and VENs to elisity.state-sync topic.

**Time** (1)

- `elisity ad get-current-time` — Get current time

**materialized-view-information-controller** (1)

- `elisity flows get-all` — `GET /api/flows/v1/refresh-info`


### Command names now pointing at a different endpoint (breaking, silent)

1 command name(s) survived the bump while the operation behind them did not. The old operation was deleted from the spec and a different surviving operation inherited the name, so **an existing script does not fail — it calls a different endpoint.** These are worth checking before anything else in this changelog.

- `elisity policy get-state` — was `GET /api/policy/v1/state` (deleted from the spec), now `GET /api/state-sync/v1/state`
  - the surviving operation also changed: renamed from `get-state-get`


### Changed command signatures

34 commands changed shape — a renamed command or a changed flag can break an existing script.

**`ad`**

- `elisity ad get-ad-agent-config` — new optional `--syslogVersion` (integer)
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
- `elisity policy get-state` — renamed from `get-state-get`
- `elisity policy lookup-dynamic` — new required `--filters` (object)
- `elisity policy lookup-dynamic-totals` — new required `--filters` (object)
- `elisity policy lookup-network` — new required `--filters` (object)

**`system`**

- `elisity system list-specs` — `--page` integer -> untyped (sent as string); `--size` integer -> untyped (sent as string); `--sort` string -> untyped (sent as string)
- `elisity system list-tasks` — `--columnFilter` string -> untyped (sent as string); `--globalFilter` string -> untyped (sent as string); `--page` integer -> untyped (sent as string); `--size` integer -> untyped (sent as string); `--sort` string -> untyped (sent as string)

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

124 commands take a different request body. The command's flags are unchanged — the body is passed as opaque JSON via `--body` / `--body-file` — but the JSON you send must match the new schema.

- **`ad`** — `agent-status`, `export`, `export-users`, `export-users-logon-history`, `export-users-post`, `put-configuration-value`, `register-connector`, `save-ad-agent-config`
- **`connectors`** — `create`, `create-connector-configuration`, `update`, `update-connector-configuration`, `validate-connector-endpoint-configuration`
- **`devices`** — `apply-custom-oui-mappings`, `attach`, `attached`, `bulk-create-devices`, `bulk-purge-device-layers`, `bulk-update-devices`, `create`, `create-configuration`, `create-device`, `enrich-by-id`, `enrich-by-id-append`, `enrich-by-ip`, `enrich-by-ip-append`, `execute-bulk-refresh`, `get-configurations-by-ids`, `get-device-aggregate`, `get-devices-view`, `update-configuration`, `update-device`
- **`flows`** — `get-dash-board-summary-data`, `get-raw-traffic-summary`, `update-noise-definition`
- **`insights`** — `create-suggestion`, `execute-create-workflow`, `update-suggestion`
- **`policy`** — `clone-policy-set`, `create-dynamic-policy-group`, `create-dynamic-policy-groups`, `create-network-policy-group`, `create-network-policy-groups`, `create-policy`, `create-policy-group-label`, `create-policy-post`, `create-policy-set`, `create-policy-view`, `create-template`, `evaluate-policy-group-for-device`, `export-policies-to-csv`, `export-policy-group-to-csv`, `export-templates`, `get-policy-groups-summary`, `lookup-dynamic-export`, `lookup-network-export`, `toggle-lock-bulk`, `update-dynamic-policy-group`, `update-network-policy-group`, `update-policy`, `update-policy-group-label`, `update-policy-groups`, `update-policy-groups-with-device-groups`, `update-policy-put`, `update-policy-set`, `update-policy-view`, `update-template`, `validate-subnet-dynamic-policy-group`, `validate-subnet-static-policy-group`, `validate-subnet-static-policy-group-post`
- **`system`** — `ack-execution-of-task-post`, `create-task`, `register-specs`, `release-execution-of-task`, `update-task`
- **`topology`** — `batch-create-or-update-multiple-rules`, `bulk-create-site-labels`, `create-cloud-controller`, `create-distribution-zone`, `create-flow-exporter`, `create-global-credentials`, `create-or-update-bulk-target-site`, `create-or-update-multiple-rules`, `create-or-update-target-site`, `create-site-post`, `create-task-list`, `create-ven`, `create-virtual-edge`, `create-virtual-edge-group`, `export-distribution-zones`, `export-site-labels`, `export-virtual-edges`, `get-dashboard-metrics`, `get-virtual-edge-by-post`, `get-virtual-edge-by-post-post`, `metrics`, `metrics-post`, `publish-ve-variables`, `register`, `register-ven`, `set-logger-level`, `set-version`, `topology`, `update-cloud-controller`, `update-distribution-zone`, `update-flow-exporter`, `update-global-credentials`, `update-global-interfaces-settings`, `update-interfaces-settings`, `update-ports-configuration`, `update-site`, `update-task-list`, `update-task-status`, `update-ven`, `update-virtual-edge`, `update-virtual-edge-group`, `update-virtual-edge-put`, `validate-virtual-edge-bulk-delete`, `validate-virtual-edge-bulk-upload`, `validate-virtual-edge-nodes-bulk-update`, `validate-virtual-edge-nodes-bulk-upload`, `virtual-edge-bulk-change-group`, `virtual-edge-bulk-upload`, `virtual-edge-node-bulk-upload`


A further 118 operations changed only in their response schema or status codes. Invocation is unaffected, so they are not listed.

### Added commands

190 new commands, grouped by CLI group.

#### `ad` (+16)

- `delete-auth` — Delete Entra authentication and all related data
- `get-activity-logs` — Query agent activity log
- `get-connector-deletion-context` — Get connector deletion context
- `get-dc-bookmark` — Get DC bookmark for specific AD Agent and DC hostname
- `get-distribution-zone-assignments` — Get distribution zone assignments per connector
- `get-isolated-distribution-zones` — `GET /api/ad-connector-service/v1/distribution-zones`
- `get-pull-status` — Get the status of a previously-initiated log pull; on success streams the ZIP bytes
- `get-syslog-credentials` — Get syslog credentials
- `pull-logs` — Initiate a log pull from an AD Agent
- `refresh-all-ad-on-prem` — Refresh all AD on-prem subscriptions
- `refresh-all-entra` — Refresh all Entra subscriptions
- `restart` — Restart the connector
- `save-activity-logs` — Receive activity log events from agent
- `set-distribution-zones` — Set distribution zones for a connector
- `update-all-agents-to-latest-version` — Update all AD Agents to latest version
- `upload-logs` — Upload agent logs

#### `connectors` (+13)

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
- `validate-endpoint-for-connector` — Validate endpoint configuration for existing connector
- `validate-endpoint-pre-creation` — Validate endpoint configuration before connector creation

#### `devices` (+30)

- `check` — Check ig-view-service sync state against the identity-graph DB (no dispatch)
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
- `refresh-devices-view` — Refresh DevicesView
- `set-feature-flag-ig` — Set value of a feature flag
- `stream-digest` — Stream device digest
- `sync` — Synchronize ig-view-service from identity-graph by republishing out-of-sync devices
- `sync-connector` — Trigger immediate workload sync for all endpoints of a connector
- `sync-endpoint` — Trigger immediate workload sync for a specific endpoint
- `update-settings` — Update offline purge settings (global and policy groups)
- `update-workload` — Update workload STATIC attributes
- `update-workload-interface` — Update STATIC layer of a workload interface
- `validate-permissions-existing` — Validate AWS permissions for an existing connector endpoint
- `validate-permissions-pre-creation` — Validate AWS permissions for a new endpoint (pre-creation)

#### `flows` (+5)

- `get-capabilities` — Get analytics capabilities
- `get-distribution-zone-sankey` — Get distribution zone sankey data
- `get-exclusion-filter-candidates` — Get exclusion filter candidate port+protocol pairs ranked by traffic usage
- `get-heatmap` — `GET /nflowsearch/api/v1/devices/{deviceId}/heatmap`
- `traffic-record-export` — Export traffic records as CSV

#### `insights` (+1)

- `get-suggestion-match-criteria` — Get Suggestion match criteria for a Policy Group

#### `policy` (+71)

- `add-definition` — `POST /api/flows/v1/applications/{id}/definitions`
- `bulk-create` — Create several labels atomically (Add Another Label drawer)
- `bulk-create-post` — Bulk-create access policies (Multi-Create) — best-effort / partial success
- `bulk-delete` — Bulk delete labels
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
- `validate-application` — `POST /api/flows/v1/applications/validate`
- `validate-match-criteria` — Validate Match Criteria
- `validate-match-criteria-for-existing-policy-group` — Validate Match Criteria for existing Policy Group
- `validate-policy-group-name` — Validate Policy Group Name
- `validate-policy-group-name-for-existing-policy-group` — Validate Policy Group Name for existing Policy Group

#### `system` (+17)

- `create-snapshot-schedule` — Create snapshot schedule
- `delete-for-ve` — Remove per-VE override
- `delete-snapshot-schedule` — Delete snapshot schedule
- `get-all-configs` — Get all task broker configs
- `get-effective-config` — Get effective config for a VE
- `get-spec-by-site-id` — Get specs by site ID
- `get-spec-group-id` — Get specs by VE group ID
- `pause-snapshot-schedule` — Pause snapshot schedule
- `replace-for-ve` — Replace per-VE disabled task types
- `replace-tenant-default` — Replace tenant-wide disabled task types
- `resume-snapshot-schedule` — Resume snapshot schedule
- `retrieve-snapshot` — Get snapshot by ID
- `retrieve-snapshot-image` — Get snapshot PDF
- `retrieve-snapshot-schedule` — Get snapshot schedule by ID
- `search-snapshot-schedules` — Search snapshot schedules
- `search-snapshots` — Search snapshots
- `update-snapshot-schedule` — Update snapshot schedule

#### `topology` (+37)

- `bulk-change-ven-group` — Bulk change Virtual Edge Group for multiple VENs
- `bulk-delete-ve-ns` — Bulk delete Virtual Edge Nodes
- `bulk-delete-virtual-edges` — Bulk delete Virtual Edges
- `bulk-force-delete-ve-ns` — Bulk force delete Virtual Edge Nodes
- `bulk-recommission-ve-ns` — Bulk recommission Virtual Edge Nodes
- `change-active-ve` — Change Active Virtual Edge for a Virtual Edge Node (VEN)
- `change-ven-group` — Change Virtual Edge Group for a Virtual Edge Node (VEN)
- `create-independent-control-mappings` — Create Independent Control Mappings between Distribution Zones
- `create-site-label-independent-control-mappings` — Create Independent Control Mappings between Site Labels
- `delete-independent-control-mappings` — Delete Independent Control Mappings
- `delete-site-label-independent-control-mappings` — Delete Independent Control Mappings for Site Labels
- `disable-maintenance` — Disable Maintenance mode on a Virtual Edge
- `disable-maintenance-for-group` — Disable Maintenance mode on a batch of Virtual Edges in a group
- `enable-maintenance` — Enable Maintenance mode on a Virtual Edge
- `enable-maintenance-for-group` — Enable Maintenance mode on a batch of Virtual Edges in a group
- `force-delete-ven` — Force delete a Virtual Edge Node in decommission state
- `get-configuration` — Get VEN configuration
- `get-details` — Get VEN details
- `get-independent-control-mappings` — Get all Independent Control Mappings for Distribution Zones
- `get-metrics` — Get VEN metrics
- `get-permissions` — Get VEN permissions
- `get-reconciled-variables` — Reconciled environment variables for a VE
- `get-settings` — Get topology settings
- `get-site-label-independent-control-mappings` — Get all Independent Control Mappings for Site Labels
- `get-status` — Get VEN status
- `get-target-site-history` — Retrieves the full history for a specific target type.
- `get-virtual-edge-nodes-for-distribution-zone` — Get all Virtual Edge Nodes for a Distribution Zone
- `patch-virtual-edge-group` — Partial-update of a virtual edge group
- `search-virtual-edge-nodes` — List Virtual Edge Nodes with pagination and sorting
- `set-logger-levels-bulk` — Set logger levels in bulk
- `update-settings` — Update topology settings
- `update-target-site-by-id` — Updates an existing target site entry by ID (for active or future entries).
- `upload-virtual-edge-nodes-bulk-json` — Bulk upload VEN rows (V2, JSON streaming)
- `upload-virtual-edges-bulk-json` — Bulk upload VE rows (V2, JSON streaming)
- `validate-virtual-edge-node-bulk-delete` — Validate Virtual Edge Nodes before bulk delete
- `validate-virtual-edge-nodes-bulk-json` — Validate VEN rows for bulk upload (V2, JSON streaming)
- `validate-virtual-edges-bulk-json` — Validate VE rows for bulk upload (V2, JSON streaming)

## Documentation

- [Getting Started](docs/getting-started.md) — First-time setup walkthrough
- [User Guide](docs/user-guide.md) — Workflow-oriented guide with real examples
- [AI Agent Operating Guide](docs/AGENTS.md) — How an AI agent should run the CLI on a human's behalf
- [Glossary Appendix](docs/glossary.md) — UI term → CLI command reference (human-readable)
- [Configuration Reference](docs/configuration.md) — Profiles, env vars, output formats, JMESPath
- [Command Reference](docs/command-reference.md) — All 658 commands with descriptions

## License

Proprietary - Elisity, Inc.
