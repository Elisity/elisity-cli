# Elisity CCC CLI — User Guide

This guide walks through real workflows against a Cloud Control Center (CCC) tenant
using the `elisity` command-line tool. Where the [Getting Started](getting-started.md)
guide gets you authenticated and the [Command Reference](command-reference.md) lists
every endpoint, this document connects the dots: how to inventory a tenant, read policy
state, page through devices, run scripts in CI, and debug when something goes sideways.

The examples use real CLI output captured against a test tenant and sanitized — UUIDs,
timestamps, and structure are authentic. Tenant URLs, client IDs, and secrets are
replaced with placeholders. Copy the commands; expect identical shapes (not identical
IDs) on your own tenant.

---

## Audience and scope

Read this guide if you fit one of these profiles:

- **Engineer** automating against CCC — building deploy pipelines, drift detectors,
  inventory dashboards, or anything that talks to the CCC REST API. You want a faster
  loop than writing `requests` calls by hand.
- **Field SE / TME** running demo workflows — you need to pull live tenant state
  during a customer call without clicking through the UI.
- **Customer or partner admin** doing day-2 operations — you have a tenant, you have
  service-account credentials, and you want to script the boring parts.
- **New CLI user coming from the UI** — every screen in CCC maps to one or more CLI
  command groups. This guide tells you which.

The guide assumes you have:

- A working `python3` (3.10 or later) and `pip` on your shell.
- OAuth2 client credentials (client ID + client secret) from a CCC tenant
  administrator, with API scopes appropriate for what you intend to do.
- Network reachability to the CCC base URL (`https://your-ccc.idp01.elisity.io` or
  similar).
- Some familiarity with another CLI such as `kubectl`, `aws`, `gh`, or `npm`. You do
  not need prior Elisity experience.

Out of scope for this guide:

- Product positioning, architecture explanations, or "why microsegmentation". Those
  belong in product docs.
- A command-by-command reference. See [Command Reference](command-reference.md) for
  all 466 commands.
- Building and deploying the CLI itself. See the repository README for development
  setup.

---

## Mental model

A few core concepts cover most of what you will hit on day one.

### Groups → commands → endpoints

Every CCC API endpoint shows up under a **command group** that matches its functional
area. There are 9 API-backed groups plus 3 CLI-native groups (`auth`, `config`,
`glossary`) — 12 groups in total, of which 11 represent product surfaces (the 9 API
groups plus `auth` and `config`; `glossary` is a documentation lookup with no API).

| Group | What lives here |
|---|---|
| `topology` | Sites, distribution zones, VE groups, VEs (Virtual Edges), VENs (Virtual Edge Nodes), flow exporters, cloud controllers |
| `policy` | Policy sets, policies, policy groups, security profiles, site labels, rules |
| `devices` | Device CRUD, bulk operations, enrichment, suppression, custom attributes |
| `ad` | Active Directory / Entra ID connectors, users, groups, agents |
| `connectors` | Custom connector configurations, import/export, connectivity tests |
| `insights` | Policy suggestions, dynamic and network group recommendations |
| `flows` | Traffic flow search, device state, noise definitions |
| `system` | Tasks, specs, state sync |
| `reporting` | **GraphQL.** Zero Trust scores, site KPIs, threat vectors, traffic-by-PG/IP, port exposure. Wraps the CCC dashboard's `/api/reporting/v1/data` GraphQL endpoint (not in OpenAPI). |
| `glossary` | CLI-native. Maps Elisity UI terminology to CLI commands. No remote API. |
| `auth` | Test connection, get token, decode JWT |
| `config` | Profile management, configuration display |

A command takes the form:

```bash
elisity [GLOBAL OPTIONS] <group> <command> [COMMAND OPTIONS] [ARGS]
```

So `elisity -f table topology get-all-sites` is a `topology` group command with the
global `-f table` formatter.

### Profiles, OAuth, env vars

The CLI obtains a bearer token via OAuth2 `client_credentials` and caches it in
memory for the life of the process. It refreshes the token automatically on expiry,
and silently retries once on a 401 with a fresh token.

Credentials come from two places:

1. A **profile** stored in `~/.elisity/config.yaml`. Profiles are named (`prod`,
   `staging`, `lab`). The active profile is whichever one `active_profile` points at.
2. **Environment variables** — `CCC_BASE_URL`, `CCC_CLIENT_ID`, `CCC_CLIENT_SECRET`,
   `CCC_TIMEOUT`. These override profile fields one-by-one, so you can hold most of a
   config in a profile and override only the base URL in CI.

The `-p` (or `--profile`) global flag picks a different profile for a single
invocation without changing the active profile.

### Output formats, JMESPath, debug mode

Three orthogonal global flags shape the output of every command:

- `-f json|table|yaml|csv` — render format. JSON is the default and is also what
  scripts should consume.
- `-q '<jmespath>'` — apply a JMESPath expression to the response before rendering.
  Use it to extract fields, filter rows, count items, or reshape into a summary.
- `--debug` — print HTTP request URLs, status codes, and headers to stderr. Use this
  when something looks wrong.

Pagination is handled three different ways depending on the endpoint:

1. **Most listing endpoints** return all results in a single response — no pagination needed.
2. **POST search endpoints** (e.g. `devices get-devices-view`) take a body with the page
   info nested under `pageable`: `--body '{"pageable":{"page":N,"size":M}}'`. A flat
   `{"page":N,"size":M}` body is silently ignored by the API.
3. **GET search endpoints** (e.g. `ad get-entra-users`, `topology get-virtual-edge`)
   expose `--page` and `--size` as query-parameter flags directly on the command.

`--body-file path/to/body.json` works wherever `--body` does. NDJSON
endpoints (which stream newline-delimited JSON) are parsed transparently and rendered
the same as any other response.

Destructive operations (delete, bulk-delete, decommission) require `--confirm` on the
command line. Without it, the CLI refuses to send the request. This is intentional
friction.

---

## Glossary — speak the right names

Elisity uses specific product terms that often diverge from generic industry vocabulary:
"monitor mode" is **Simulation**, "Zero Trust score" is the **Policy Enforcement Score**,
"security group" is a **Policy Group**, and so on. The CLI ships a `glossary` group that
maps the synonyms you might type to the canonical term and the exact CLI command that
implements it. This matters most when you (or an AI agent acting for you) need a recipe
without guessing.

```bash
elisity glossary list                       # all 19 terms with domain + enum
elisity glossary search "monitor mode"      # JSON entry for any synonym
elisity glossary explain "Zero Trust score" # prose + ready-to-paste commands
```

For a human-readable appendix grouped by domain, see [docs/glossary.md](glossary.md).
For an AI-agent operating contract (when humans say X, run Y), see
[docs/AGENTS.md](AGENTS.md).

---

## Setup

If you have not run `elisity` before, this is the shortest path to a working setup.
See [Getting Started](getting-started.md) for the long version, including virtualenv
recipes and PyPI install.

### Install

From a clone of the repository:

```bash
pip install -e .
```

Or, with a virtualenv if you prefer to isolate dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Confirm:

```bash
elisity --version
```

```text
elisity, version 0.1.0
```

### Create your first profile

You will need three values from your CCC administrator: the base URL, a client ID,
and a client secret.

```bash
elisity config set-profile lab \
  --base-url https://your-ccc.idp01.elisity.io \
  --client-id your-client-id \
  --client-secret 'your-client-secret'
```

The first profile you create becomes the active profile automatically. The file
`~/.elisity/config.yaml` is created if it does not exist.

Restrict access immediately — the file holds secrets in plain text:

```bash
chmod 600 ~/.elisity/config.yaml
```

### Verify auth

```bash
elisity auth test
```

```json
{
  "status": "healthy",
  "code": 200,
  "authenticated": true
}
```

If you get something other than that, jump to [Common errors](#common-errors) before
continuing.

### Env-var-only alternative

Skip the profile entirely. Useful for CI, ephemeral shells, or one-off scripts:

```bash
export CCC_BASE_URL=https://your-ccc.idp01.elisity.io
export CCC_CLIENT_ID=your-client-id
export CCC_CLIENT_SECRET='your-client-secret'

elisity auth test
```

Environment variables take precedence over profile values on a field-by-field basis.
You can keep a profile with most settings and override just `CCC_BASE_URL` to point
the same credentials at a different tenant for a single shell session.

---

## Common workflows

The sections below cover the day-to-day tasks. Each one shows a goal, the commands
that get there, the actual output you should expect, and the pitfalls that bite new
users.

### 1. Inventory: what's on this tenant?

When you first connect a tenant — or when something is wrong and you need to know
what's actually deployed — start with a top-down sweep.

#### List sites

A **site** is the top-level grouping for a physical or logical location (a hospital,
a campus, a regional office). Sites contain distribution zones, which contain VE
groups, which contain VEs (Virtual Edges).

```bash
elisity topology get-all-sites
```

```json
[
  {
    "id": "fbce7a2c-9dcf-45e7-aed7-35de0f0ec208",
    "label": "Default",
    "numericId": "1",
    "createdAt": "2026-04-28T20:08:04.448888Z",
    "modifiedAt": null,
    "assignedAt": "2026-05-05T12:10:46.400820Z",
    "deleteValidationErrors": null
  },
  {
    "id": "80490113-5847-4a6a-a785-99033d39208e",
    "label": "Boston",
    "numericId": "7",
    "createdAt": "2026-05-05T19:23:52.791584Z",
    "modifiedAt": "2026-05-14T17:42:28.480190Z",
    "assignedAt": "2026-05-14T13:46:31.449112Z",
    "deleteValidationErrors": null
  },
  {
    "id": "1934f482-5128-4312-8e66-93e68235d8a0",
    "label": "Hospital",
    "numericId": "6",
    "createdAt": "2026-05-05T19:23:52.759674Z",
    "modifiedAt": "2026-05-05T19:23:52.759674Z",
    "assignedAt": "2026-05-06T13:23:10.511445Z",
    "deleteValidationErrors": null
  },
  {
    "id": "1724c64a-a07b-4836-8cb7-e32418da04b5",
    "label": "CORK",
    "numericId": "5",
    "createdAt": "2026-04-28T20:57:08.806744Z",
    "modifiedAt": "2026-04-28T20:57:08.806744Z",
    "assignedAt": "2026-04-29T15:18:27.870690Z",
    "deleteValidationErrors": null
  }
]
```

Four sites: `Default`, `Boston`, `Hospital`, `CORK`. The `label` field is what shows
in the UI — there is no `name` field on the v1 sites endpoint. Keep that in mind when
you write JMESPath filters; we'll come back to it below.

Same data, table view:

```bash
elisity -f table topology get-all-sites
```

```text
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ id                                   ┃ label    ┃ numericId ┃ createdAt                   ┃ modifiedAt                  ┃ assignedAt                  ┃ deleteValidationErrors ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ fbce7a2c-9dcf-45e7-aed7-35de0f0ec208 │ Default  │ 1         │ 2026-04-28T20:08:04.448888Z │                             │ 2026-05-05T12:10:46.400820Z │                        │
│ 80490113-5847-4a6a-a785-99033d39208e │ Boston   │ 7         │ 2026-05-05T19:23:52.791584Z │ 2026-05-14T17:42:28.480190Z │ 2026-05-14T13:46:31.449112Z │                        │
│ 1934f482-5128-4312-8e66-93e68235d8a0 │ Hospital │ 6         │ 2026-05-05T19:23:52.759674Z │ 2026-05-05T19:23:52.759674Z │ 2026-05-06T13:23:10.511445Z │                        │
│ 1724c64a-a07b-4836-8cb7-e32418da04b5 │ CORK     │ 5         │ 2026-04-28T20:57:08.806744Z │ 2026-04-28T20:57:08.806744Z │ 2026-04-29T15:18:27.870690Z │                        │
└──────────────────────────────────────┴──────────┴───────────┴─────────────────────────────┴─────────────────────────────┴─────────────────────────────┴────────────────────────┘
```

The table format auto-sizes columns to terminal width. For wide records (distribution
zones, devices), the rendering can get messy; pair `-f table` with `-q` to project
only the columns you care about.

#### Count items quickly

```bash
elisity topology get-all-sites -q 'length(@)'
```

```text
4
```

`length(@)` is the JMESPath idiom for "size of the current node". Use it whenever you
want a number, not a record set.

#### List distribution zones

A **distribution zone** is the next level down — a logical grouping of VE-group
endpoints attached to a site. The `topology get-all-distribution-zones` command
returns all zones across all sites:

```bash
elisity -f table topology get-all-distribution-zones
```

The full table is wide and noisy on a normal terminal. Project just the useful
columns with JMESPath:

```bash
elisity topology get-all-distribution-zones \
  -q '[].{name: name, siteName: siteName, type: type, veCount: virtualEdgeCount, venCount: virtualEdgeNodeCount}' \
  -f table
```

This drops most of the audit-trail and validation columns and keeps the four numbers
you actually want: zone name, parent site, type, VE count, VEN count.

For the full record, JSON is still the way:

```bash
elisity topology get-all-distribution-zones
```

#### List virtual edges

The CCC concept of a **Virtual Edge** (VE) is a logical enforcement context attached
to a switch. There is no `get-virtual-edge` command — that name is intuitive but
not what was wired up. The actual commands are:

```bash
# Search and filter virtual edges (GET)
elisity topology get-virtual-edge-get

# Same data via POST for richer filter bodies
elisity topology get-virtual-edge-by-post

# Single virtual edge by ID
elisity topology get-virtual-edge-by-id <ve-id>
```

If you guess the wrong name, the CLI tells you:

```bash
elisity topology get-virtual-edge
```

```text
Usage: elisity topology [OPTIONS] COMMAND [ARGS]...
Try 'elisity topology --help' for help.

Error: No such command 'get-virtual-edge'.
```

When in doubt, list the group:

```bash
elisity topology --help
```

That prints all 100+ topology commands with a one-line description for each. The
output is paginated by your terminal — pipe to `less` for browsing:

```bash
elisity topology --help | less
```

#### List virtual edge nodes (VENs)

```bash
# Paginated list with full record
elisity topology get-virtual-edge-nodes

# Single VEN by ID
elisity topology get-single-ven <ven-id>

# Topology for a given VEN (the switches it's programming)
elisity topology get-topology <ven-id>
```

#### Devices

A **device** is anything the system has classified — a workstation, an IoT camera, a
medical device, a server. Devices live underneath sites and policy groups.

```bash
# Total device count
elisity devices get-device-count

# Paginated browsing
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":10}}'
```

The devices endpoint paginates, so it always needs a request body. The `--body` flag
takes inline JSON; `--body-file` takes a path. We'll cover devices in depth in
[Working with devices](#3-working-with-devices) below.

#### Flow exporters

```bash
elisity topology get-all-flow-exporter
```

If none are configured, you'll get an empty array:

```json
[]
```

That is a successful response, not an error. The exit code is `0`.

#### Filter and reshape with JMESPath

JMESPath is the cheapest way to make a noisy response useful. A few patterns:

**Names (labels) only:**

```bash
elisity topology get-all-sites -q '[].label'
```

```json
[
  "Default",
  "Boston",
  "Hospital",
  "CORK"
]
```

**Pitfall** — there is no `.name` on the v1 sites endpoint. If you JMESPath against
the wrong field, the projection returns nothing useful:

```bash
elisity topology get-all-sites -q '[].name'
```

```json
[]
```

That's not an error; it's JMESPath telling you "no objects had a `name` field".
Inspect the raw response first to learn the field names, then write the query.

**Count:**

```bash
elisity topology get-all-sites -q 'length(@)'
```

```text
4
```

**Select specific fields:**

```bash
elisity topology get-all-sites -q '[].{label: label, id: id}'
```

**First three results:**

```bash
elisity topology get-all-sites -q '[0:3]'
```

**Filter by substring:**

```bash
elisity topology get-all-sites -q "[?contains(label, 'or')]"
```

That returns the sites whose label contains "or" — `Boston` and `CORK`. Note the
single-quote `'or'` inside double-quoted shell arg.

**Sort:**

```bash
elisity topology get-all-sites -q 'sort_by(@, &label)'
```

#### Multiple output formats

The same `get-all-sites` data, four ways:

JSON (default):

```bash
elisity topology get-all-sites
```

```json
[
  {
    "id": "fbce7a2c-9dcf-45e7-aed7-35de0f0ec208",
    "label": "Default",
    "numericId": "1",
    "createdAt": "2026-04-28T20:08:04.448888Z",
    "modifiedAt": null,
    "assignedAt": "2026-05-05T12:10:46.400820Z",
    "deleteValidationErrors": null
  }
]
```

Table:

```bash
elisity -f table topology get-all-sites
```

```text
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┓
┃ id                                   ┃ label    ┃ numericId ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━┩
│ fbce7a2c-9dcf-45e7-aed7-35de0f0ec208 │ Default  │ 1         │
│ 80490113-5847-4a6a-a785-99033d39208e │ Boston   │ 7         │
│ 1934f482-5128-4312-8e66-93e68235d8a0 │ Hospital │ 6         │
│ 1724c64a-a07b-4836-8cb7-e32418da04b5 │ CORK     │ 5         │
└──────────────────────────────────────┴──────────┴───────────┘
```

(Date columns dropped for brevity — the real output includes them.)

YAML:

```bash
elisity -f yaml topology get-all-sites
```

```yaml
- id: fbce7a2c-9dcf-45e7-aed7-35de0f0ec208
  label: Default
  numericId: '1'
  createdAt: '2026-04-28T20:08:04.448888Z'
  modifiedAt: null
  assignedAt: '2026-05-05T12:10:46.400820Z'
  deleteValidationErrors: null
- id: 80490113-5847-4a6a-a785-99033d39208e
  label: Boston
  numericId: '7'
  createdAt: '2026-05-05T19:23:52.791584Z'
  modifiedAt: '2026-05-14T17:42:28.480190Z'
  assignedAt: '2026-05-14T13:46:31.449112Z'
  deleteValidationErrors: null
- id: 1934f482-5128-4312-8e66-93e68235d8a0
  label: Hospital
  numericId: '6'
  createdAt: '2026-05-05T19:23:52.759674Z'
  modifiedAt: '2026-05-05T19:23:52.759674Z'
  assignedAt: '2026-05-06T13:23:10.511445Z'
  deleteValidationErrors: null
- id: 1724c64a-a07b-4836-8cb7-e32418da04b5
  label: CORK
  numericId: '5'
  createdAt: '2026-04-28T20:57:08.806744Z'
  modifiedAt: '2026-04-28T20:57:08.806744Z'
  assignedAt: '2026-04-29T15:18:27.870690Z'
  deleteValidationErrors: null
```

CSV:

```bash
elisity -f csv topology get-all-sites
```

```text
id,label,numericId,createdAt,modifiedAt,assignedAt,deleteValidationErrors
fbce7a2c-9dcf-45e7-aed7-35de0f0ec208,Default,1,2026-04-28T20:08:04.448888Z,,2026-05-05T12:10:46.400820Z,
80490113-5847-4a6a-a785-99033d39208e,Boston,7,2026-05-05T19:23:52.791584Z,2026-05-14T17:42:28.480190Z,2026-05-14T13:46:31.449112Z,
1934f482-5128-4312-8e66-93e68235d8a0,Hospital,6,2026-05-05T19:23:52.759674Z,2026-05-05T19:23:52.759674Z,2026-05-06T13:23:10.511445Z,
1724c64a-a07b-4836-8cb7-e32418da04b5,CORK,5,2026-04-28T20:57:08.806744Z,2026-04-28T20:57:08.806744Z,2026-04-29T15:18:27.870690Z,
```

When to use which? See [Output formats — when to use which](#output-formats--when-to-use-which).

---

### 2. Day-2: list policy state

Once a tenant is set up, day-2 work is mostly reading and comparing state — what
policies exist, which policy groups are bound where, which sites carry which policy
set.

#### Policy sets

A **policy set** is a named bundle of policies attached to a site label and a set of
policy groups. A site can have multiple policy sets active. The primary listing
command returns NDJSON:

```bash
elisity policy get-all-as-nd-json
```

The CLI parses the newline-delimited JSON stream transparently. You see a normal JSON
array; the underlying transport is NDJSON so the server can stream large policy
stores without buffering everything.

A typical record:

```json
{
  "id": "29eef758-a1e3-49c0-a531-779ef835c325",
  "description": null,
  "createdBy": "service-account@your-org.example",
  "createdAt": "2026-05-14T17:48:01.990534Z",
  "modifiedBy": "service-account@your-org.example",
  "modifiedAt": "2026-05-14T17:49:05.514081Z",
  "status": "Active",
  "isProtected": false,
  "deviceCoverage": 100.0,
  "policyCoverage": 100.0,
  "policyGroupLabels": [
    {
      "id": "8ef8f860-4ee0-4d38-862d-a61224c96236",
      "name": "Boston"
    },
    {
      "id": "40dcbb75-5960-4070-bb2a-208779c2f4d0",
      "name": "System"
    }
  ],
  "siteLabels": [
    {
      "siteLabel": "7",
      "siteName": "Boston",
      "nodeIds": [
        "56"
      ]
    }
  ],
  "parentName": null,
  "parentId": null,
  "replicasCount": 0,
  "deleteValidationErrors": [
    "Active Policy Sets associated with Site Labels or Policies cannot be deleted."
  ],
  "name": "Boston",
  "noOfPolicies": "81",
  "noOfVirtualEdges": "1"
}
```

Things to notice:

- `deviceCoverage` and `policyCoverage` are percentages (0.0–100.0) describing how
  much of the site this policy set covers.
- `noOfPolicies` and `noOfVirtualEdges` are stringly-typed — JMESPath comparisons
  like `[?noOfPolicies > \`50\`]` will not work without a `to_number()` cast.
- `deleteValidationErrors` is populated whenever the system has a reason you cannot
  delete the record. An empty array means "deletable".
- A policy set carries its **policy groups** by reference (`policyGroupLabels`) and
  its **site labels** by reference (`siteLabels`). Cross-reference these to traverse.

#### Useful policy projections

**One-line summary per policy set:**

```bash
elisity policy get-all-as-nd-json \
  -q '[].{name: name, status: status, deviceCoverage: deviceCoverage, policies: noOfPolicies, ves: noOfVirtualEdges}' \
  -f table
```

**Only Active policy sets:**

```bash
elisity policy get-all-as-nd-json \
  -q "[?status=='Active'].name"
```

**Policy sets whose name starts with a string:**

```bash
elisity policy get-all-as-nd-json \
  -q "[?starts_with(name, 'Hospital')]"
```

**Top-coverage policy sets:**

```bash
elisity policy get-all-as-nd-json \
  -q 'sort_by(@, &deviceCoverage) | reverse(@) | [0:5].{name: name, coverage: deviceCoverage}' \
  -f table
```

(The `|` here is the JMESPath pipe operator, not the shell pipe. The whole expression
is a single argument to `-q`.)

#### Policy groups

A **policy group** is a logical container of devices on which policies are
enforced. The listing endpoint returns every policy group across the tenant.

```bash
elisity policy get-all-as-nd-json-get-2 \
  -q '[].{name: name, type: type}'
```

```json
[
  {
    "name": "Boston",
    "type": null
  },
  {
    "name": "CORK",
    "type": null
  },
  {
    "name": "Default",
    "type": null
  },
  {
    "name": "FRSTR-HOSPITAL",
    "type": null
  }
]
```

A `null` type field usually means "user-created policy group" — system-managed
groups (such as the Default group) are marked with explicit type values when they
exist.

#### NDJSON streaming for large policy stores

The NDJSON endpoints are the recommended way to read large policy state because the
server flushes records as it produces them. The CLI buffers internally and emits a
single JSON array at the end, so from a user perspective you don't have to think
about NDJSON parsing. But it has implications:

- Memory: the CLI holds the whole result in memory before rendering. On tenants with
  100,000+ policies, prefer JMESPath projections (`-q`) to reduce the result before
  rendering, or paginate via the `-by-post` variants when available.
- Failures mid-stream: if the connection drops after some records arrive, the CLI
  reports the error and exits non-zero. Partial output is not flushed.

For a quick gut-check that the stream is alive on a large tenant:

```bash
elisity --debug policy get-all-as-nd-json -q 'length(@)'
```

The debug output shows you when bytes are arriving and when the request completes.

#### Cross-referencing policy groups to devices

If you have a policy group name and want to see which devices it covers:

1. Get the policy group ID:

   ```bash
   elisity policy get-all-as-nd-json-get-2 \
     -q "[?name=='Boston'].id | [0]"
   ```

2. Use the policy-group's device-listing endpoint with that ID. The exact command
   name depends on your CCC version — list the group:

   ```bash
   elisity policy --help | grep -i 'device'
   ```

3. Or, walk the other way: get a device, look at its `policyGroupName` field, and
   query that group.

The point is that the CLI exposes the same graph the UI navigates. Once you know the
shape of one node, JMESPath plus a second command will get you to anything connected.

---

### 3. Working with devices

The `devices` group is the most-used in day-2 work. It includes paginated views,
bulk operations, enrichment, and search.

#### Paginated views

The primary listing endpoint paginates and requires a body:

```bash
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":10}}'
```

The body is **POST request body**, not a CLI flag. A common new-user mistake:

```bash
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":10}}'
```

```text
Usage: elisity devices get-devices-view [OPTIONS]
Try 'elisity devices get-devices-view --help' for help.

Error: No such option: --data
```

The flag is `--body`. Always.

For larger bodies, store them in a file:

```bash
cat > device-page.json <<EOF
{
  "page": 0,
  "size": 100,
  "sort": ["deviceName,asc"]
}
EOF

elisity devices get-devices-view --body-file device-page.json
```

#### Reading paginated responses

Pagination responses have a top-level shape like:

```json
{
  "content": [ ... actual records ... ],
  "totalElements": 1234,
  "totalPages": 13,
  "size": 100,
  "number": 0
}
```

To drill into just the records and rename common fields:

```bash
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":50}}' \
  -q 'content[].{name: deviceName, ip: ipAddress, mac: macAddress, group: policyGroupName}' \
  -f table
```

The `content[]` prefix unwraps the page envelope. Use it for any paginated endpoint.
The table and CSV formatters also auto-unwrap `content` when you don't supply a `-q`.

#### Iterating through pages in a script

```bash
#!/usr/bin/env bash
set -euo pipefail

PAGE=0
SIZE=200
while :; do
  RESPONSE=$(elisity devices get-devices-view --body "{\"page\":$PAGE,\"size\":$SIZE}")
  COUNT=$(echo "$RESPONSE" | jq '.content | length')
  echo "$RESPONSE" | jq '.content[] | {name: .deviceName, ip: .ipAddress}'
  if [ "$COUNT" -lt "$SIZE" ]; then break; fi
  PAGE=$((PAGE + 1))
done
```

This is the simplest possible loop. For production use, paginate with the documented
`totalPages` field instead, and handle non-zero exit codes explicitly.

#### Bulk operations

The CLI exposes the same bulk endpoints the UI uses for multi-row actions: attach,
detach, suppress, classify, delete. Each takes a JSON body listing IDs and an action.
The full set is in [Command Reference](command-reference.md) — search for `bulk-` in
the `devices` group.

A representative example (do not run it without thought — bulk delete is permanent):

```bash
cat > delete-batch.json <<EOF
{
  "ids": [
    "device-uuid-1",
    "device-uuid-2"
  ]
}
EOF

elisity devices bulk-delete-devices --body-file delete-batch.json --confirm
```

The `--confirm` flag is required for any destructive operation. Without it, the
command refuses to send the request.

#### Search and filter

For ad-hoc lookups, JMESPath against the paginated view is usually fastest:

```bash
# Devices whose name contains a string
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":1000}}' \
  -q "content[?contains(deviceName, 'wkst')]" -f table

# Devices with no policy group assigned
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":1000}}' \
  -q 'content[?policyGroupName == null]' -f table
```

For server-side filtering at scale, use the dedicated search endpoints — `devices
search-devices`, `devices get-devices-by-criteria`, etc. — which accept a filter
body and avoid pulling the whole inventory.

---

### 4. AD / IdentityGraph

The `ad` group covers the Active Directory and Entra ID integration: connectors that
sync directory state, users and groups discovered by those connectors, and the
agents that run on-prem to relay LDAP/Kerberos traffic.

#### List connectors

The exact command name is environment-dependent. If you guess wrong, the CLI tells
you:

```bash
elisity ad get-connectors
```

```text
Usage: elisity ad [OPTIONS] COMMAND [ARGS]...
Try 'elisity ad --help' for help.

Error: No such command 'get-connectors'.
```

Use `--help` to find the right name:

```bash
elisity ad --help | head -30
```

The current command names start with `get-` and include `ad-connector` or
`directory-connector`. They differ between CCC versions; `--help` is always the
authoritative source. The same pattern applies to `ad get-`-prefixed commands for
users, groups, and agents.

#### Look up users and groups

Once you've identified the right user-listing command for your CCC version, the
pattern is the same as everywhere else:

```bash
# Paginated — uses query-parameter flags, not a body
elisity ad get-entra-users --page 0 --size 50

# Specific user by SID + domain (the way CCC stores AD identity)
elisity ad get-user-by-sid-and-domain <DOMAIN> <SID>

# Lookup by Entra user object id (Entra-only)
elisity ad get-entra-users -q "[?id=='<entra-user-id>']"
```

You normally don't need to manage AD state from the CLI — that's the IdP's job. The
read-only views are useful for verifying that a sync ran, that the user counts look
right, and that a specific user's group memberships are reaching CCC.

---

### 5. Insights and suggestions

The `insights` group surfaces policy recommendations the system has generated based
on observed traffic and learned device behavior. Treat them as proposals; the human
operator decides whether to apply them.

```bash
# Look for the suggestion-listing command in the help
elisity insights --help
```

If you call the wrong name, you'll see the standard not-found message:

```bash
elisity insights get-policy-groups-suggestion-list
```

```text
Usage: elisity insights [OPTIONS] COMMAND [ARGS]...
Try 'elisity insights --help' for help.

Error: No such command 'get-policy-groups-suggestion-list'.
```

The current names live under `insights get-` — for example
`get-policy-groups-suggestion-list`, `get-dynamic-group-suggestions`,
`get-network-group-suggestions`. The exact set depends on which CCC features are
enabled on your tenant.

#### Use insights to inform automation

A common pattern: dump suggestions to JSON, review them out-of-band (a teammate, a
ticket, a spreadsheet), then apply the approved ones via the corresponding
create/update endpoints.

```bash
# Pull current suggestions (this endpoint returns all suggestions in one shot —
# no pagination parameters required or accepted)
elisity insights get-policy-groups-suggestion-list \
  > suggestions-$(date +%F).json

# Hand to whoever owns approval
mail -s "Policy suggestions for review" team@example \
  -A suggestions-$(date +%F).json < /dev/null

# After approval, apply
elisity policy create-policy --body-file approved-suggestion-12.json
```

The insights group is read-mostly — it observes and recommends. Application happens
through the `policy` group.

---

### 6. Multi-environment operations

Most engineers running this CLI for real work end up with at least three tenants —
prod, staging, and a lab. The CLI supports this directly through profiles and a
`-p` override flag.

#### Profile switching (prod / staging / lab)

Define a profile per tenant:

```bash
elisity config set-profile prod \
  --base-url https://prod-ccc.idp01.elisity.io \
  --client-id prod-client-id \
  --client-secret 'prod-secret'

elisity config set-profile staging \
  --base-url https://staging-ccc.idp01.elisity.io \
  --client-id staging-client-id \
  --client-secret 'staging-secret' \
  --timeout 60

elisity config set-profile lab \
  --base-url https://lab-ccc.idp01.elisity.io \
  --client-id lab-client-id \
  --client-secret 'lab-secret'
```

Verify with `config list-profiles`:

```bash
elisity config list-profiles
```

```json
{
  "prod": {
    "base_url": "https://prod.idp01.elisity.io",
    "client_id": "<YOUR_CLIENT_ID>",
    "_active": true
  },
  "staging": {
    "base_url": "https://staging.idp01.elisity.io",
    "client_id": "<YOUR_CLIENT_ID>",
    "_active": false
  },
  "lab": {
    "base_url": "https://lab.idp01.elisity.io",
    "client_id": "<YOUR_CLIENT_ID>",
    "timeout": 30,
    "default_format": "json",
    "_active": false
  }
}
```

(The `client_secret` field is shown as `***` in this output. See
`elisity config show` for the same masking on the active profile.)

Switch the active profile:

```bash
elisity config use-profile staging
elisity auth test
```

```json
{
  "status": "healthy",
  "code": 200,
  "authenticated": true
}
```

#### The `-p` flag for one-off runs

`-p` is a global flag. Use it to run a single command against a different profile
without touching the active profile:

```bash
elisity -p lab topology get-all-sites
elisity -p prod -q 'length(@)' topology get-all-sites
```

This is the right flag for cross-tenant comparisons. A few examples:

```bash
# Compare site counts
echo "Prod sites:    $(elisity -p prod -q 'length(@)' topology get-all-sites)"
echo "Staging sites: $(elisity -p staging -q 'length(@)' topology get-all-sites)"
echo "Lab sites:     $(elisity -p lab -q 'length(@)' topology get-all-sites)"

# Drift check on a specific policy group name
PROD=$(elisity -p prod policy get-all-as-nd-json-get-2 -q "[?name=='Boston'] | [0].id")
STAGING=$(elisity -p staging policy get-all-as-nd-json-get-2 -q "[?name=='Boston'] | [0].id")
echo "Prod Boston ID:    $PROD"
echo "Staging Boston ID: $STAGING"
```

#### Env-var override pattern for CI

Profiles work for interactive shells. Pipelines should use environment variables:

```yaml
# GitHub Actions example
jobs:
  policy-drift-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install CLI
        run: pip install elisity-cli
      - name: Check policy set count
        env:
          CCC_BASE_URL: ${{ secrets.CCC_URL }}
          CCC_CLIENT_ID: ${{ secrets.CCC_ID }}
          CCC_CLIENT_SECRET: ${{ secrets.CCC_KEY }}
        run: |
          elisity auth test
          elisity policy get-all-as-nd-json -q 'length(@)'
```

A common hybrid pattern: keep a profile in the runner image with defaults, override
the base URL via env var per environment:

```bash
# Profile holds client credentials for the prod-tooling service account
# Env var picks which tenant to target this run
export CCC_BASE_URL=https://staging-ccc.idp01.elisity.io
elisity auth test
```

Environment variables override only the fields you set. Other fields still come from
the active profile.

#### Precedence order

Resolution order, highest to lowest:

1. Environment variable (e.g. `CCC_BASE_URL`)
2. Profile specified by `-p`
3. Active profile in `~/.elisity/config.yaml`

If a field is set in the environment, the profile value for that specific field is
ignored. Other fields still come from the profile. This is field-by-field, not
all-or-nothing — set `CCC_BASE_URL` alone and the rest of the resolved config still
comes from the active profile.

---

### 7. Scripting and automation

The CLI is built to be scripted. Stable exit codes, JSON output, predictable errors.

#### Bearer token extraction

For tools that can't speak through the CLI (a Postman collection, a `curl` snippet,
a third-party SIEM), pull the bearer token directly:

```bash
elisity auth token
```

```text
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.<truncated-jwt-payload>.<truncated-signature>
```

Use it in a script:

```bash
TOKEN=$(elisity auth token)
curl -s -H "Authorization: Bearer $TOKEN" \
  https://your-ccc.idp01.elisity.io/api/topology/v2/sites \
  | jq '.[] | .label'
```

A few things to know:

- The token is a JWT. Validity is short (typically minutes to an hour, set by the
  CCC tenant). Re-extract for long-running scripts.
- `elisity auth token` is a separate process from your other CLI calls, so each
  process re-authenticates. Cache the token in a variable for a single script run;
  do not write it to disk.
- The same token works for any CCC endpoint, including ones the CLI doesn't expose.

#### Piping CLI JSON into other tools

The default JSON output is designed for `jq`, `python -c`, `node -e`, or any other
JSON consumer.

```bash
# Top 5 policy sets by device coverage
elisity policy get-all-as-nd-json \
  | jq 'sort_by(.deviceCoverage) | reverse | .[0:5] | .[] | {name, deviceCoverage}'

# Count devices by policy group
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":1000}}' \
  | jq '.content | group_by(.policyGroupName) | map({group: .[0].policyGroupName, count: length})'

# Generate kubectl-style describe output
elisity topology get-all-sites \
  | jq -r '.[] | "Site: \(.label)\n  ID: \(.id)\n  Created: \(.createdAt)\n"'
```

JMESPath via `-q` and `jq` cover the same ground; use whichever you find more
readable. JMESPath has the advantage of running before render, so non-JSON formats
(table, YAML, CSV) also benefit. `jq` only works on the JSON output.

#### Using CSV output for spreadsheets

CSV output is automatically unwrapped for paginated responses (`content` array) and
emits a header row derived from the first record:

```bash
elisity -f csv devices get-devices-view --body '{"pageable":{"page":0,"size":1000}}' \
  > devices.csv

elisity -f csv topology get-all-sites > sites.csv
```

For LibreOffice or Excel, CSV imports cleanly. Numeric columns that are strings in
the API (`numericId`, `noOfPolicies`) will need a conversion step in the spreadsheet
if you want to sort or aggregate them as numbers.

#### Idempotent re-runs

Read commands are inherently idempotent — running them twice yields the same data.
Write commands need a little more thought:

- Create endpoints will return an error on duplicate names (e.g. `Site with label
  'Boston' already exists`). Handle that as success in idempotent scripts.
- Update endpoints (`set-*`, `update-*`) are idempotent when the body matches the
  desired state.
- Delete endpoints require `--confirm` and return an error if the target doesn't
  exist. Wrap delete calls with a "exists?" check.

A safe `delete-if-exists` pattern:

```bash
SITE_ID=$(elisity topology get-all-sites -q "[?label=='to-delete'] | [0].id" -f json)
if [ "$SITE_ID" != "null" ] && [ -n "$SITE_ID" ]; then
  elisity topology delete-site-v2 "$SITE_ID" --confirm
fi
```

#### Exit codes

The CLI returns a non-zero exit code for any failure that should halt a script. The
specific codes are:

| Exit | Meaning |
|---|---|
| `0` | Success. Response (possibly empty) printed to stdout. |
| `1` | Generic error — usage error, JMESPath syntax error, validation error. |
| `2` | Configuration error — missing base URL, missing credentials, profile not found. |
| `3` | HTTP error — non-2xx status from CCC. Stderr carries the body. |
| `4` | Network error — DNS, connect, timeout (after retries exhausted). |

Scripts should check for `0` and `3` explicitly when calling write endpoints. A `3`
with a body matching "already exists" is often safe to swallow; a `3` from anything
else should halt.

#### Common automation recipes

**Daily inventory snapshot:**

```bash
#!/usr/bin/env bash
set -euo pipefail

SNAPSHOT_DIR="/var/log/elisity-snapshots/$(date +%F)"
mkdir -p "$SNAPSHOT_DIR"

elisity topology get-all-sites              > "$SNAPSHOT_DIR/sites.json"
elisity topology get-all-distribution-zones > "$SNAPSHOT_DIR/zones.json"
elisity topology get-virtual-edge-get       > "$SNAPSHOT_DIR/ves.json"
elisity topology get-virtual-edge-nodes     > "$SNAPSHOT_DIR/vens.json"
elisity policy   get-all-as-nd-json > "$SNAPSHOT_DIR/policy-sets.json"
elisity policy   get-all-policy-groups      > "$SNAPSHOT_DIR/policy-groups.json"

echo "Snapshot written to $SNAPSHOT_DIR"
```

**Diff between two tenants:**

```bash
elisity -p prod    topology get-all-sites -q 'sort_by([].label, &@)' > /tmp/prod-sites.json
elisity -p staging topology get-all-sites -q 'sort_by([].label, &@)' > /tmp/staging-sites.json
diff /tmp/prod-sites.json /tmp/staging-sites.json
```

**Send a Slack notification on policy-set drift:**

```bash
EXPECTED=24
ACTUAL=$(elisity policy get-all-as-nd-json -q 'length(@)')
if [ "$ACTUAL" != "$EXPECTED" ]; then
  curl -X POST "$SLACK_WEBHOOK" -d "{\"text\":\"Policy set drift: expected $EXPECTED, got $ACTUAL\"}"
fi
```

---

### 8. Debugging

When the CLI says something other than what you expected, the first three steps are
the same.

#### `--debug` flag

```bash
elisity --debug auth test
```

`--debug` is a global flag — it must appear before the command name. It enables
verbose HTTP logging to stderr: full request URLs, headers, status codes, request
timing, and (where relevant) response bodies. The actual command output still goes to
stdout, so you can pipe normally:

```bash
elisity --debug topology get-all-sites 2> debug.log | jq '.[].label'
```

`debug.log` will contain the HTTP trace; `jq` sees only the clean JSON.

#### HTTP request/response inspection

A typical successful trace:

```text
DEBUG urllib3.connectionpool:_make_request:537 https://your-ccc.idp01.elisity.io:443 "POST /auth/realms/elisity/protocol/openid-connect/token HTTP/1.1" 200 None
DEBUG urllib3.connectionpool:_make_request:537 https://your-ccc.idp01.elisity.io:443 "GET /api/topology/v2/sites HTTP/1.1" 200 None
```

Things to look for in the trace:

- **First call is to `/auth/realms/elisity/protocol/openid-connect/token`** — that's
  the OAuth2 token grant. Status `200` means credentials are good. Status `401`
  means the client ID or secret is wrong. Status `404` means the base URL is wrong.
- **Subsequent calls are to `/api/...`** — that's the API itself. Same status
  rules apply.
- **`POST /token` happens once per CLI invocation** because the token is cached in
  memory. If you see two token grants in one run, that means the first token was
  rejected (401) and the CLI refreshed.

If something looks slow, the debug output prints request timing — look for the gap
between request and response.

#### Common 400 / 403 / 404 patterns

**400 Bad Request** on a POST / PUT command almost always means a missing or wrong
field in the request body. The CLI prints the response body to stderr; read it:

```text
HTTP 400: {"error":"Validation failed","field":"label","message":"label must not be blank"}
```

Fix the body, retry.

**403 Forbidden** means authentication succeeded (good credentials) but the service
account does not have permission for that endpoint. Talk to your CCC administrator
about the service account's role.

```text
HTTP 403: {"error":"Forbidden","message":"User does not have required scope: policy.write"}
```

**404 Not Found** has two flavors:

- *Resource not found* — the ID you passed doesn't exist. Common after a delete
  or in cross-tenant scripts where the IDs don't match.
- *Endpoint not enabled on this CCC version* — older CCC tenants may not have all
  466 commands implemented. Run the corresponding `--help` to see what's available.

```text
HTTP 404: {"error":"Not Found"}
```

If `--debug` shows the request URL going somewhere unexpected (a typo in your base
URL, for example), the body will often be HTML rather than JSON.

#### Common usage errors

Reading the CLI's own error messages saves time. A few examples:

**Wrong flag name:**

```bash
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":10}}'
```

```text
Usage: elisity devices get-devices-view [OPTIONS]
Try 'elisity devices get-devices-view --help' for help.

Error: No such option: --data
```

The correct flag for a request body is `--body` (inline JSON) or `--body-file` (path).

**Wrong command name:**

```bash
elisity topology get-virtual-edge
```

```text
Usage: elisity topology [OPTIONS] COMMAND [ARGS]...
Try 'elisity topology --help' for help.

Error: No such command 'get-virtual-edge'.
```

The real names are `get-virtual-edge-get` (GET, query-string filtering) and
`get-virtual-edge-by-post` (POST, body filtering). Use `topology --help` to find
the actual command names.

**Missing positional argument:**

```bash
elisity topology get-site-v2
```

```text
Usage: elisity topology get-site-v2 [OPTIONS] ID
Try 'elisity topology get-site-v2 --help' for help.

Error: Missing argument 'ID'.
```

Run the corresponding `get-all-*` command first, pluck the ID, then pass it.

**Missing or empty body:**

```bash
elisity devices get-devices-view
```

```text
Error: Endpoint requires a request body. Pass one with --body or --body-file.
```

```bash
elisity devices get-devices-view --body '{}'
```

This will usually return the first default-sized page. Pass `--body '{"pageable":{"page":0,"size":50}}'`
explicitly when you want a specific window.

#### Tracing a failing script

If a longer script fails partway through, replay just the failing command with
`--debug`:

```bash
elisity --debug devices bulk-attach-devices --body-file attach.json --confirm 2> debug.log
```

Then read `debug.log` from top to bottom — token grant, then the failing request and
response. The response body almost always contains the operative error message.

---

### 9. Zero Trust / posture scores

The Zero Trust score data — what powers the CCC dashboard Zero Trust page,
the malware lateral movement page, and per-device risk views — lives in a
GraphQL endpoint at `POST /api/reporting/v1/data`. **This endpoint is not
in the OpenAPI spec** (GraphQL is a different API surface), so the CLI ships
a hand-coded `reporting` group that wraps the most useful queries.

GraphQL introspection on the endpoint is open; the schema exposes four
metric domains (`policyMetrics`, `identityGraphMetrics`,
`trafficVectorsMetrics`, `topologyMetrics`). The commands below cover the
operationally important queries.

#### Quick answers

```bash
# THE tenant-wide Zero Trust score — single number from the headline metric
elisity reporting get-aggregate-enforcement-score

# Per-site dashboard summary (devices, VENs, policy counts, score)
elisity -f table reporting get-site-kpis

# Tenant-wide device counts, broken out by online status
elisity reporting get-device-count

# Per-policy-set enforcement score (real GraphQL value — the REST
# `policy get-enforcement-score` 404s on most tenants)
elisity reporting get-policy-set-enforcement-score <POLICY_SET_ID>

# The original per-policy-group ZT row data (deviceCoverage / policyCoverage,
# threat-vector metrics, port exposure)
elisity reporting get-zero-trust-metrics

# Find which snapshot times have data
elisity reporting list-snapshots
```

#### Worked example: tenant summary from a single call

```bash
elisity -f table reporting get-site-kpis
```

```text
┌──────────┬────────────────┬────────────────┬─────────────────┬──────────────────┬──────────────────┬─────────────────────────┐
│ siteName │ onlineDevices  │ virtualEdgeNodes│ localPolicyGroups│ simulatedPolicies│ activatedPolicies│ policyEnforcementScore  │
├──────────┼────────────────┼────────────────┼─────────────────┼──────────────────┼──────────────────┼─────────────────────────┤
│ Boston   │ 143            │ 1              │ 7               │ 0                │ 81               │ 100.0                   │
│ CORK     │ 1071           │ 6              │ 9               │ 3                │ 245              │ 84.9                    │
│ Default  │ 142            │ 4              │ 0               │ 2                │ 29               │ 2.7                     │
│ Hospital │ 51             │ 2              │ 0               │ 62               │ 2                │ 8.2                     │
└──────────┴────────────────┴────────────────┴─────────────────┴──────────────────┴──────────────────┴─────────────────────────┘
```

One call. Per-site devices, VEN count, policy group count, policies, and
enforcement score. The same data the CCC UI's per-site cards display.

#### Per-policy-group detail

For the richer per-policy-group rows that the original Zero Trust page
shows (with threat-vector breakdowns), use `get-zero-trust-metrics`:

```bash
# Pull all Zero Trust scores for the latest available snapshot
elisity reporting get-zero-trust-metrics

# Per-snapshot retrieval was removed server-side in CCC 26.x; the endpoint serves the current snapshot.

# Server-side site filter (use the site label, e.g. Boston / CORK / Default)
elisity reporting get-zero-trust-metrics --site Boston

# L4 detail (TCP / UDP / ICMP breakdown of avgAllowedPorts)
elisity reporting get-zero-trust-metrics --include-l4-detail

# Per-device rows (deviceId + macAddress included)
elisity reporting get-zero-trust-metrics --include-mac
```

**The relevant fields on each row:**

| Field | Meaning |
|---|---|
| `siteName` / `policyGroupName` / `policySetName` | Where this row lives |
| `deviceCount` | Devices counted in this row |
| `totalFlows` / `restrictedFlows` | Flow totals; `restrictedFlows / totalFlows` ≈ blocked-ratio |
| `zeroTrustScore` | **Zero Trust score (0–100)** — UI's Zero Trust Device Score |
| `leastPrivilegeScore` | **Zero Trust policy-coverage score (0–100)** — UI's Zero Trust Policy Score |
| `l4Metrics.avgAllowedPorts` | Average open-port count per device |
| `threatVectorMetrics.portExposure[]` | Per-port exposure scores (the malware-lateral-movement page) |
| `threatVectorMetrics.threatVectors[]` | MITRE ATT&CK technique codes + scores |

**Computing a tenant-wide Zero Trust score** (device-weighted average,
null-safe — JMESPath has no general arithmetic so do this in jq):

```bash
elisity reporting get-zero-trust-metrics | jq '
  {
    snapshot: .[0].dateTime,
    total_devices: (map(.deviceCount) | add),
    weighted_device_coverage: ((map((.zeroTrustScore // 0) * .deviceCount) | add)
                              / (map(.deviceCount) | add)),
    weighted_policy_coverage: ((map((.leastPrivilegeScore // 0) * .deviceCount) | add)
                              / (map(.deviceCount) | add))
  }'
```

**Per-policy-group breakdown as a table** (note: `-q` and `-f` are
top-level flags — place them BEFORE the group name):

```bash
elisity -q '[].{site: siteName, pg: policyGroupName,
              devices: deviceCount, devCov: zeroTrustScore, polCov: leastPrivilegeScore}' \
  -f table reporting get-zero-trust-metrics
```

**Threat-vector scores for the malware lateral-movement page:**

```bash
elisity -q '[].{site: siteName, pg: policyGroupName, topVectors: threatVectorMetrics.threatVectors[0:5]}' \
  reporting get-zero-trust-metrics
```

#### Raw GraphQL escape hatch

For ad-hoc queries that aren't in the hand-coded set (additional `operationName`
values used by the CCC UI such as `GetDeviceRiskAttribution`,
`GetThreatVectorTrend`, etc.), drop the full GraphQL payload in a JSON file
and use `elisity reporting query`:

```bash
cat > /tmp/q.json <<'EOF'
{
  "operationName": "MyCustomQuery",
  "variables": {...},
  "query": "query MyCustomQuery(...) { ... }"
}
EOF
elisity reporting query --body-file /tmp/q.json
```

#### The legacy enforcement-score REST endpoint

CCC also has an older per-policy-set "enforcement score" REST endpoint:

```
GET /api/policy/v1/enforcement-score/{policySetId}
```

This is the auto-generated `elisity policy get-enforcement-score <POLICY_SET_ID>`
command. On many tenants (older CCC versions, demo tenants, feature-flagged
deployments) it returns `404 Client Error: Not Found`. The GraphQL
`reporting` endpoint above is the authoritative source for live Zero Trust
scores; use the REST endpoint only when you need its specific weighted-score
schema. The per-policy-set fields on `policy get-all-as-nd-json`
(`deviceCoverage`, `policyCoverage`) are also a usable fallback for
broad posture summaries.

### 10. Flow search

The flow-search endpoints (`/nflowsearch/api/v1/*`) all live under the `flows` group
and all accept a POST body. Empty bodies return `400 Bad Request` — the schemas have
required fields you must supply.

```bash
# Dashboard summary — querytype is required
elisity flows get-dash-board-summary-data --body '{
  "querytype": "summary",
  "interval": {"from": "now-1h", "to": "now"}
}'

# Traffic summary — interval is the main filter
elisity flows get-raw-traffic-summary --body '{
  "interval": {"from": "now-15m", "to": "now"}
}'

# Per-policy-group breakdown
elisity flows get-pg-data --body '{
  "interval": {"from": "now-1h", "to": "now"}
}'

# Export flows to CSV (note: --offset is also required)
elisity flows flows-export --offset 0 --size 100 --body '{
  "interval": {"from": "now-15m", "to": "now"},
  "sortfield": "timestamp",
  "sortdesc": true
}'

# Unique values for a single column (GET; --parameter is required)
elisity flows get-unique-values --parameter source.ip
```

**Body fields most commands accept** (from the spec — not all are required, but
all are honoured if supplied):

| Field | Purpose | Example |
|---|---|---|
| `interval` | Time range — most endpoints require this | `{"from": "now-1h", "to": "now"}` |
| `querytype` | Required for `get-dash-board-summary-data` | `"summary"` |
| `source` / `destination` | Filter by source or destination criteria | `{"ip": "10.0.0.1"}` |
| `filter` | Server-side filter expression | `{"action": "ALLOW"}` |
| `range` | Pagination range | `{"from": 0, "to": 100}` |
| `size` / `offset` | Page size / offset on `flows-export` | `100` / `0` |
| `sortfield` / `sortdesc` | Sort by column, descending boolean | `"timestamp"` / `true` |

If you get a 400 back, decode the response body with `--debug 2> /tmp/d.log` and
look at the validation message — it will name the missing required field.

---

## Using the CLI from an AI agent

If you are wiring the CLI into an autonomous agent (Claude Code, a CI script that
shells out to an LLM, etc.), Claude Code's default permission mode will prompt for
human approval on every `git`, `pip`, `curl`, and `elisity` invocation. That breaks
non-interactive use.

For sandboxed agentic use, run with `--permission-mode bypassPermissions`:

```bash
echo "Use the elisity-cli repo to summarize my CCC tenant" \
  | claude --print --permission-mode bypassPermissions
```

Other valid modes are `auto` (auto-accept all), `acceptEdits` (file edits only), and
`plan` (read-only planning). Only use `bypassPermissions` inside a container or VM
that you've already constrained — it disables the safety prompt entirely.

For non-agent CLI use (a human at a terminal), no special flag is needed; the agent
permission gate doesn't apply.

---

## Output formats — when to use which

The four output formats serve different consumers. Pick by the consumer.

| Format | When to use | When not to |
|---|---|---|
| `json` (default) | Piping to `jq`, storing to disk, programmatic consumption, returning from scripts | Reading interactively if there's a lot of data — terminal scrolling is brutal |
| `table` | Interactive exploration in your terminal, screenshots in a ticket, talk-through with a teammate | Anything that gets piped further — the table characters break downstream parsing |
| `yaml` | Human review of a config-shaped record, diffing two versions side-by-side, dropping into a config repo | Programmatic consumption — YAML parsing varies in subtle ways across libraries |
| `csv` | Spreadsheets, BI tools, mass review by non-technical stakeholders | Nested data — CSV flattens objects to `[object Object]`-shaped strings |

Same `topology get-all-sites` data, four ways, side-by-side. (Headers only, abridged
for length.)

JSON:

```bash
elisity topology get-all-sites
```

```json
[
  {
    "id": "fbce7a2c-9dcf-45e7-aed7-35de0f0ec208",
    "label": "Default",
    "numericId": "1"
  }
]
```

Table:

```bash
elisity -f table topology get-all-sites
```

```text
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┓
┃ id                                   ┃ label    ┃ numericId ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━┩
│ fbce7a2c-9dcf-45e7-aed7-35de0f0ec208 │ Default  │ 1         │
└──────────────────────────────────────┴──────────┴───────────┘
```

YAML:

```bash
elisity -f yaml topology get-all-sites
```

```yaml
- id: fbce7a2c-9dcf-45e7-aed7-35de0f0ec208
  label: Default
  numericId: '1'
```

CSV:

```bash
elisity -f csv topology get-all-sites
```

```text
id,label,numericId
fbce7a2c-9dcf-45e7-aed7-35de0f0ec208,Default,1
```

### Pick a default per profile

If you spend most of your time browsing in a terminal, set `default_format: table`
on a profile. Override per-command when you need to pipe:

```bash
elisity config set-profile lab \
  --base-url https://lab-ccc.idp01.elisity.io \
  --client-id lab-client-id \
  --client-secret 'lab-secret' \
  --default-format table
```

```bash
# Uses table because profile says so
elisity topology get-all-sites

# Force JSON for piping
elisity -f json topology get-all-sites | jq '.[].label'
```

### What table format does on nested data

The table renderer flattens nested objects and arrays to JSON strings, then
truncates at 80 characters. So for records with `policyGroupLabels` (an array of
objects), the table cell shows something like:

```text
[{"id": "8ef8f860-4ee0-4d38-862d-a61224c96236", "name": "Boston"}, {"id": "40dcbb...
```

That's readable but rarely what you want. Either:

- Use JMESPath to project the nested field into a top-level string before
  rendering: `-q '[].{name: name, groups: policyGroupLabels[].name | join(`, `, @)}'`
- Switch to JSON output and read with `jq`.

### Auto-unwrapping `content`

Paginated responses have a `content` array under a wrapper object. The `table` and
`csv` formatters automatically unwrap `content` before rendering, so you don't have
to:

```bash
elisity -f table devices get-devices-view --body '{"pageable":{"page":0,"size":5}}'
```

That just shows 5 device rows, not a one-row table containing a JSON blob. JSON and
YAML output preserves the wrapper — if you want the records only in JSON/YAML, add
`-q 'content'`.

---

## JMESPath — the secret weapon

JMESPath is a query language for JSON. The CLI applies your `-q` expression to the
API response before rendering, so non-JSON formats benefit too. The full JMESPath
specification is supported; the recipes below cover what most people actually need.

Cheatsheet:

| Expression | What it does |
|---|---|
| `[].name` | Project the `name` field across an array of objects |
| `length(@)` | Count items |
| `[?status=='Active']` | Filter by field value |
| `[?contains(name, 'Hospital')]` | Filter by substring |
| `[].{a: name, b: id}` | Build a new object per item |
| `[0:5]` | First 5 items (slice) |
| `[-3:]` | Last 3 items (slice) |
| `sort_by(@, &createdAt)` | Sort by a field |
| `reverse(@)` | Reverse order |
| `[?status=='Active'].name` | Filter then project |
| `content[]` | Unwrap a paginated `content` array |
| `[].config.vlanId` | Nested field access |
| `{total: length(@), names: [].name}` | Build a summary object |

### Names only

```bash
elisity topology get-all-sites -q '[].label'
```

```json
[
  "Default",
  "Boston",
  "Hospital",
  "CORK"
]
```

If you query against a field that does not exist (`[].name` here, since the v1 sites
endpoint uses `label` not `name`), JMESPath returns an empty array:

```bash
elisity topology get-all-sites -q '[].name'
```

```json
[]
```

That's a useful signal — "no rows had the field you asked for" — rather than an
error. Inspect the raw response, then write the query.

### Count

```bash
elisity topology get-all-sites -q 'length(@)'
```

```text
4
```

### Filter

```bash
# Active records
elisity policy get-all-as-nd-json -q "[?status=='Active']"

# Substring match
elisity policy get-all-as-nd-json \
  -q "[?contains(name, 'CORK')]"

# Records with non-null field
elisity policy get-all-as-nd-json \
  -q '[?description != null]'

# Comparison on numeric field
elisity policy get-all-as-nd-json \
  -q '[?deviceCoverage > `50`]'
```

Note the backticks `` ` `` around literal numeric values in JMESPath — they are
required when the comparison value is a number. Strings use single quotes.

### Project specific fields

```bash
elisity topology get-all-sites \
  -q '[].{label: label, id: id, created: createdAt}'
```

```json
[
  {"label": "Default",  "id": "fbce7a2c-9dcf-45e7-aed7-35de0f0ec208", "created": "2026-04-28T20:08:04.448888Z"},
  {"label": "Boston",   "id": "80490113-5847-4a6a-a785-99033d39208e", "created": "2026-05-05T19:23:52.791584Z"},
  {"label": "Hospital", "id": "1934f482-5128-4312-8e66-93e68235d8a0", "created": "2026-05-05T19:23:52.759674Z"},
  {"label": "CORK",     "id": "1724c64a-a07b-4836-8cb7-e32418da04b5", "created": "2026-04-28T20:57:08.806744Z"}
]
```

For policy groups specifically:

```bash
elisity policy get-all-as-nd-json-get-2 -q '[].{name: name, type: type}'
```

```json
[
  {"name": "Boston", "type": null},
  {"name": "CORK", "type": null},
  {"name": "Default", "type": null},
  {"name": "FRSTR-HOSPITAL", "type": null}
]
```

### Slicing

```bash
# First 3
elisity topology get-all-sites -q '[0:3]'

# Last 3
elisity topology get-all-sites -q '[-3:]'

# Skip first 2
elisity topology get-all-sites -q '[2:]'
```

### Nested access

```bash
# Policy sets' first site label name
elisity policy get-all-as-nd-json -q '[].siteLabels[0].siteName'

# All policy-group names across all policy sets, flattened
elisity policy get-all-as-nd-json -q '[].policyGroupLabels[].name'
```

### Sort and reverse

```bash
elisity topology get-all-sites -q 'sort_by(@, &label)'
elisity topology get-all-sites -q 'sort_by(@, &createdAt) | reverse(@)'
```

The `|` here is JMESPath's pipe — chain expressions inside the single `-q` argument.

### Build a summary object

```bash
elisity policy get-all-as-nd-json \
  -q '{total: length(@), active: length([?status==`Active`]), names: [].name}'
```

That returns a single object with three computed fields. Useful for snapshot reports
and tests.

### Slicing a paginated response

The `content[]` prefix unwraps a paginated envelope before further filtering:

```bash
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":1000}}' \
  -q 'content[?policyGroupName == null].{name: deviceName, ip: ipAddress}' \
  -f table
```

### Practical combinations

**Top-N report:**

```bash
elisity policy get-all-as-nd-json \
  -q 'sort_by(@, &deviceCoverage) | reverse(@) | [0:5].{name: name, coverage: deviceCoverage, ves: noOfVirtualEdges}' \
  -f table
```

**Find a specific record by name:**

```bash
elisity topology get-all-sites -q "[?label=='Boston'] | [0]"
```

The `| [0]` extracts the first matching object so you get an object back, not a
single-element array.

**Existence check:**

```bash
elisity topology get-all-sites -q "length([?label=='Boston'])"
```

Returns `1` if `Boston` exists, `0` otherwise. Use this in shell conditionals.

**Cross-reference two fields:**

```bash
elisity policy get-all-as-nd-json \
  -q '[].{name: name, sites: siteLabels[].siteName, groups: policyGroupLabels[].name}'
```

### When JMESPath errors

Invalid JMESPath expressions exit non-zero with an error to stderr. The raw API
response is not printed:

```bash
elisity topology get-all-sites -q '[].nam'
```

A typo like `nam` here just returns nulls (since the field doesn't exist) — no error.

```bash
elisity topology get-all-sites -q '['
```

This is a syntax error and produces something like:

```text
Error: Invalid JMESPath expression at position 1: unexpected end of input
```

When in doubt, run the command without `-q` first, then iterate on the expression
against the raw JSON.

---

## Common errors

A field guide to the messages you'll see, what they mean, and how to fix them.

| Error | Likely cause | Fix |
|---|---|---|
| `Error: 401 Unauthorized` | Bad `client_id` or `client_secret`, or account is locked | Verify with `elisity auth test`. Re-run `config set-profile` if needed. |
| `Error: 403 Forbidden` | Service account is authenticated but lacks the right scope | Talk to your CCC admin — the account needs the role for that endpoint. |
| `Error: 404 Not Found` (endpoint) | Endpoint not enabled on this CCC version | Check version. Use `elisity <group> --help` to confirm the command exists. |
| `Error: 404 Not Found` (resource) | The ID you passed doesn't exist | Re-run the corresponding `get-all-*` to confirm the ID. |
| `Error: 400 Bad Request` | POST/PUT missing required body fields | Read the response body — it names the missing field. Check `--help` for `--body`. |
| `Error: No such command 'X'` | Mis-typed command name | Run `elisity <group> --help` to list the actual commands. |
| `Error: No such option: '--X'` | Mis-typed flag (e.g. `--data` instead of `--body`) | Run `elisity <group> <command> --help` for the actual flags. |
| `Error: Missing argument 'ID'` | Command takes a positional UUID | Run the corresponding `get-all-*` first to pluck the ID. |
| `Error: No CCC_BASE_URL configured` | No active profile and no env var | Run `elisity config set-profile` or `export CCC_BASE_URL=...`. |
| `Error: Missing CCC_CLIENT_ID or CCC_CLIENT_SECRET` | Creds not yet set | Same fix — profile or env vars. |
| `Error: Profile 'X' does not exist` | `-p X` referenced an undefined profile | `elisity config list-profiles` shows what's defined. |
| `CCC authentication failed. Check credentials.` | OAuth2 token request failed | Run `elisity --debug auth test` to see the underlying error. |
| Connection timeout | Slow tenant, slow link, or stalled CCC | Bump `CCC_TIMEOUT` or the profile's `timeout`. |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Lab tenant using a self-signed cert | Set `verify_ssl: false` in the lab profile (do not do this in prod). |

### Worked examples

**Wrong flag (the `--data` / `--body` confusion):**

```bash
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":10}}'
```

```text
Usage: elisity devices get-devices-view [OPTIONS]
Try 'elisity devices get-devices-view --help' for help.

Error: No such option: --data
```

Fix:

```bash
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":10}}'
```

**Wrong command name (intuitive but not implemented):**

```bash
elisity topology get-virtual-edge
```

```text
Usage: elisity topology [OPTIONS] COMMAND [ARGS]...
Try 'elisity topology --help' for help.

Error: No such command 'get-virtual-edge'.
```

Fix — list the group and pick the actual command:

```bash
elisity topology --help | grep -i virtual-edge
```

**Wrong command in another group:**

```bash
elisity ad get-connectors
```

```text
Usage: elisity ad [OPTIONS] COMMAND [ARGS]...
Try 'elisity ad --help' for help.

Error: No such command 'get-connectors'.
```

```bash
elisity insights get-policy-groups-suggestion-list
```

```text
Usage: elisity insights [OPTIONS] COMMAND [ARGS]...
Try 'elisity insights --help' for help.

Error: No such command 'get-policy-groups-suggestion-list'.
```

```bash
elisity system list-tasks
```

```text
Usage: elisity system [OPTIONS] COMMAND [ARGS]...
Try 'elisity system --help' for help.

Error: No such command 'list-tasks'.
```

The pattern is the same in every case — the CLI tells you exactly which command did
not match, and `--help` on the group lists the real names.

**Missing positional ID:**

```bash
elisity topology get-site-v2
```

```text
Usage: elisity topology get-site-v2 [OPTIONS] ID
Try 'elisity topology get-site-v2 --help' for help.

Error: Missing argument 'ID'.
```

Fix — get an ID from the list endpoint first:

```bash
SITE_ID=$(elisity topology get-all-sites -q "[0].id")
elisity topology get-site-v2 "$SITE_ID"
```

**Empty response is not an error:**

```bash
elisity topology get-all-flow-exporter
```

```json
[]
```

Exit code `0`. The tenant simply has no flow exporters configured. Same for
`[].name` projections where the field doesn't exist — JMESPath returns `[]`, exit
code `0`.

---

## Appendix A: full command tree

The CLI exposes 466 commands. The full reference, including parameters and return
types for each, lives at:

- [Command Reference](command-reference.md)

For a quick on-shell listing of any group:

```bash
elisity --help                          # All groups
elisity topology --help                 # All topology commands
elisity policy --help                   # All policy commands
elisity devices --help                  # All device commands
elisity topology get-site-v2 --help     # Flags and arguments for one command
```

The root help is also a useful tenant-readiness check — it'll fail before printing
if your install is broken:

```bash
elisity --help
```

```text
Usage: elisity [OPTIONS] COMMAND [ARGS]...

  Elisity CCC CLI — command-line interface to the Cloud Control Center API.

  Manages topology, policies, devices, connectors, AD/Entra integration,
  traffic flows, and system operations — 466 commands across 12 groups.

  Configuration:   Set CCC_BASE_URL, CCC_CLIENT_ID, CCC_CLIENT_SECRET env
  vars, or   run 'elisity config set-profile' to store credentials.

  Examples:   elisity topology get-site-v2 <site-id>   elisity devices get-
  devices-view --body '{"pageable":{"page":0,"size":10}}'   elisity policy get-all-as-nd-
  json --format table

Options:
  --version                       Show the version and exit.
  -f, --format [json|table|yaml|csv]
                                  Output format (default: json)
  -q, --query TEXT                JMESPath query to filter output
  --debug                         Enable debug logging (show HTTP requests)
  -p, --profile TEXT              Use a named profile from
                                  ~/.elisity/config.yaml
  --help                          Show this message and exit.

Commands:
  ad          Active Directory / Entra ID integration — connectors,...
  auth        Authentication operations — test connection, get token info.
  config      Manage CLI configuration — profiles, credentials, defaults.
  connectors  Connector management — custom connectors, configurations,...
  devices     Device identity and enrichment — CRUD, bulk, attach,...
  flows       Traffic analytics — device state, flow search, noise...
  glossary    Map Elisity UI terms (e.g. 'monitor mode') to CLI commands.
  insights    Policy insights and suggestions — dynamic/network group...
  policy      Manage microsegmentation policies — policy sets, policies,...
  reporting   CCC reporting (GraphQL) — Zero Trust scores, threat vectors,...
  system      System operations — tasks, specs, state sync
  topology    Manage network topology — sites, zones, VE groups, VEs,...
```

(The example line in the root help shows `--data` — that example predates the rename
to `--body`. The actual flag the CLI accepts is `--body`. The Command Reference is
authoritative; the embedded help text in the entry-point may lag.)

### A representative group: topology

```bash
elisity topology --help
```

```text
Usage: elisity topology [OPTIONS] COMMAND [ARGS]...

  Manage network topology — sites, zones, VE groups, VEs, VENs, flow exporters

Options:
  --help  Show this message and exit.

Commands:
  ack-registration                Acknowledge registration of...
  batch-create-or-update-multiple-rules
                                  Bulk create or update rules...
  bulk-create-site-labels         Create list of sites.
  bulk-delete-cloud-controllers   Bulk delete cloud controllers.
  bulk-delete-credentials         Bulk delete credentials.
  bulk-delete-distribution-zone   Bulk delete distribution zone.
  bulk-delete-site                Bulk delete site labels.
  bulk-delete-site-v2             Bulk delete site labels.
  change-virtual-edge-group       Change virtual edge group for...
  create-cloud-controller         Create a new cloud controller.
  create-distribution-zone        Create list of distribution...
  create-flow-exporter            Create Flow Exporter
  create-global-credentials       Create a new global credentials.
  create-or-update-bulk-target-site
                                  Creates or updates multiple...
  create-or-update-multiple-rules
                                  Create or update rules for...
  create-or-update-target-site    Creates a new target or...
  create-site                     Create list of sites.
  create-site-post                Create site label.
  create-task-list                Create a task list, managing...
  create-ven                      Create a new virtual edge node.
  create-virtual-edge             Create new virtual edge
  create-virtual-edge-group       Create new virtual edge group
  decommission-virtual-edge-node  Trigger decommission of a...
  delete-cloud-controller         Delete cloud controller.
  delete-distribution-zone        Delete distribution zone.
  delete-flow-exporter            Delete Flow Exporter.
  delete-global-credentials       Delete global credentials.
  delete-site                     Delete site.
  delete-site-v2                  Delete site.
  delete-target-site              Permanently deletes the target...
  delete-ven                      Delete virtual edge node.
  delete-virtual-edge             Delete existing virtual edge
  delete-virtual-edge-group       Delete existing virtual edge...
  exclude-adjacent-vens           Exclude adjacent VENs and...
  export-distribution-zones       Generate all distribution...
  export-site-labels              Generate all site labels as CSV
  export-virtual-edge-nodes       Generate all virtual edge...
  export-virtual-edges            Generate all virtual edges as CSV
  get-all-cloud-controllers       Get cloud controllers
  get-all-distribution-zones      Get all Distribution Zones
  get-all-distribution-zones-get  Get all Distribution Zones
  get-all-flow-exporter           Get all Flow Exporter
  get-all-global-credentials      Get global credentials
  get-all-sites                   Get all Sites
  get-all-sites-v2                Get all Sites
  get-all-tags                    Get all Tags used for Site Labels
  get-all-target-sites            Retrieves all configured...
  get-all-ve-ns-for-global-credentials
                                  Get global credentials
  get-dashboard-count             Get VE and VEN dashboard count
  get-dashboard-metrics           Get VE and VEN dashboard metrics
  get-distribution-zone           Get single Distribution Zone
  get-flow-exporter               Get single Flow Exporter
  get-global-interfaces-settings  Get global interfaces settings...
  get-logger                      GET...
  get-loggers-for-all-virtual-edges
                                  GET...
  get-manifest                    Get manifest with versions for...
  get-ports-configuration         Get ports configuration for a VEN
  get-single-ven                  Get single Virtual Edge Node
  get-site                        Get single Site
  get-site-count                  Get site count
  get-site-count-v2               Get site count
  get-site-v2                     Get single Site
  get-target-site                 Retrieves the target for a...
  get-target-types                Retrieves all available target...
  get-topology                    Get topology for a VEN
  get-ve-ns-overview-response     Returns a non-paginated...
  get-ve-variables                Download variables for a VE
  get-virtual-edge                Search and filter virtual edge
  get-virtual-edge-by-id          Get a virtual edge by ID
  get-virtual-edge-by-post        Search and filter virtual edge
  get-virtual-edge-by-post-post   Search and filter virtual edge
  get-virtual-edge-get            Search and filter Virtual Edge...
  get-virtual-edge-group-by-id    Get a virtual edge group by ID
  get-virtual-edge-node-firewall-rules
                                  List of Firewalls and Firewall...
  get-virtual-edge-nodes          List Virtual Edge Nodes with...
  get-virtual-edge-nodes-by-post  List Virtual Edge Nodes with...
  heartbeat                       Register heartbeat for a VE
  heartbeat-post                  Register heartbeat from...
  is-imbalanced                   Check if Virtual Edge Group is...
  metrics                         Publish operational metrics...
  metrics-post                    Publish operational metrics...
  publish-ve-variables            Publish variables for a VE
  re-initialize-virtual-edge-node
                                  Trigger re-initialization of a...
  rebalance-virtual-edge-group    Rebalance Virtual Edge Group
  recommission-virtual-edge-node  Trigger recommission of a...
```

(The list continues — the rest of the topology commands are visible in the actual
help output. Use `elisity topology --help | less` to scroll.)

---

## Appendix B: troubleshooting

A short list of the things that bite people repeatedly.

### Resetting a profile

The fastest way to "reset" a profile is to re-run `config set-profile` with the same
name and corrected values:

```bash
elisity config set-profile prod \
  --base-url https://prod-ccc.idp01.elisity.io \
  --client-id new-client-id \
  --client-secret 'new-client-secret'
```

That overwrites the previous values. The other profile fields (timeout,
default_format, verify_ssl) keep their previous values unless you pass them again.

To delete a profile entirely, edit `~/.elisity/config.yaml` and remove the YAML
block. If you delete the `active_profile`, update `active_profile:` to point at
another profile.

### Clearing the token cache

The token is cached in memory for the duration of a single CLI invocation only.
Each new shell command re-authenticates. There is no on-disk token cache to clear.

If you're scripting and want a fresh token explicitly, just run `elisity auth token`
again — every invocation gets a fresh grant from the CCC token endpoint.

### Where config lives

The on-disk config file:

```text
~/.elisity/config.yaml
```

The directory is created on first `config set-profile`. The file holds secrets in
plain text. Set restrictive permissions:

```bash
chmod 600 ~/.elisity/config.yaml
```

For multi-user systems or CI runners, prefer environment variables backed by a
secrets manager (GitHub Secrets, Vault, AWS Secrets Manager). Do not check
`~/.elisity/config.yaml` into source control.

### `config show` redacts secrets

`elisity config show` displays the resolved active configuration with secrets
masked. It's safe to paste in tickets and PRs:

```bash
elisity config show
```

```json
{
  "base_url": "https://<your-ccc>.idp01.elisity.io",
  "client_id": "<YOUR_CLIENT_ID>",
  "client_secret": "***",
  "verify_ssl": true,
  "timeout": 30,
  "default_format": "json"
}
```

Any field whose key name contains `secret` (case-insensitive) is replaced with
`***`. If you ever see a literal secret in `config show` output, treat it as a bug
and report it.

### Listing profiles

```bash
elisity config list-profiles
```

```json
{
  "prod": {
    "base_url": "https://prod.idp01.elisity.io",
    "client_id": "<YOUR_CLIENT_ID>",
    "client_secret": "***",
    "_active": true
  },
  "staging": {
    "base_url": "https://staging.idp01.elisity.io",
    "client_id": "<YOUR_CLIENT_ID>",
    "client_secret": "***",
    "_active": false
  },
  "lab": {
    "base_url": "https://lab.idp01.elisity.io",
    "client_id": "<YOUR_CLIENT_ID>",
    "client_secret": "***",
    "timeout": 30,
    "default_format": "json",
    "_active": false
  }
}
```

The `_active: true` marker shows which profile is currently selected. The same
redaction (`***` on `secret`-named fields) applies.

### Bumping the request timeout

Default is 30 seconds. For slow tenants or large responses, raise it:

```bash
# Per shell session
export CCC_TIMEOUT=120

# Or, persist in a profile
elisity config set-profile prod \
  --base-url https://prod-ccc.idp01.elisity.io \
  --client-id prod-client-id \
  --client-secret 'prod-secret' \
  --timeout 120
```

### Disabling SSL verification (lab only)

For tenants using self-signed certs (typically lab/dev tenants), set `verify_ssl:
false` directly in the profile YAML:

```yaml
profiles:
  lab:
    base_url: https://lab-ccc.idp01.elisity.io
    client_id: lab-client-id
    client_secret: lab-secret
    verify_ssl: false
```

`verify_ssl` is config-file-only — there is no environment variable for it. Do not
set this for production tenants.

### When `auth test` fails

The full ladder:

1. **`Error: No CCC_BASE_URL configured`** — no profile and no env var. Set one.
2. **`Error: Missing CCC_CLIENT_ID or CCC_CLIENT_SECRET`** — base URL is set but
   credentials aren't. Set them.
3. **`CCC authentication failed. Check credentials.`** — the OAuth2 token request
   came back non-2xx. Run with `--debug`:

   ```bash
   elisity --debug auth test
   ```

   In the debug output, look at the response from `/auth/realms/elisity/protocol/openid-connect/token`:

   - `401` — wrong `client_id` or `client_secret`. Reset and retry.
   - `404` — wrong `base_url`. Verify the tenant URL.
   - `connection refused` / `timeout` — network. Check VPN, firewall, DNS.
   - HTML body — the URL is reaching a non-CCC endpoint. Double-check the base URL.

4. **`SSL: CERTIFICATE_VERIFY_FAILED`** — lab cert. Set `verify_ssl: false` in the
   profile.

### When everything looks right but the response is empty

Empty array `[]`, empty pagination `{"content":[]}`, or `null` is usually correct.
A few common cases:

- The endpoint genuinely has no records (e.g. `get-all-flow-exporter` on a tenant
  with no flow exporters).
- Your JMESPath filtered everything out — re-run without `-q` to confirm.
- The service account has scopes that limit what it can see — drop to a more
  privileged account temporarily to confirm.
- You're hitting the wrong tenant — `elisity config show` to confirm `base_url`.

### When the CLI hangs

The retry policy is 3 attempts with exponential backoff (2s min, 10s max), so a
single hang can stretch to ~30 seconds before failing. If a request is hanging:

- `Ctrl-C` to abort; the CLI prints a partial trace if `--debug` is on.
- Test base connectivity:

  ```bash
  curl -v -m 5 https://your-ccc.idp01.elisity.io
  ```

- Drop the timeout to fail fast while you debug:

  ```bash
  CCC_TIMEOUT=5 elisity --debug auth test
  ```

- If a specific endpoint is slow but others are fine, that's a server-side issue —
  report to the CCC team with the request URL and timing from `--debug`.

---

## Where to go next

- [Getting Started](getting-started.md) — install, first profile, first commands.
- [Configuration Reference](configuration.md) — all profile fields, env vars,
  precedence rules, security guidance.
- [Command Reference](command-reference.md) — every one of the 466 commands with
  parameters and return shapes.

This guide is workflow-first. For exact arguments on a specific command, always
trust `elisity <group> <command> --help` over any doc — the help text is generated
from the same source the CLI itself runs on.

---

## NOTES

Judgment calls made while writing this guide. Surfaced here for reviewer awareness.

- **`name` vs `label` on sites.** Sample 07 (`-q '[].name'`) returns `[]` because the
  v1 sites endpoint exposes `label`, not `name`. The guide turns that gotcha into a
  teaching point in the JMESPath section rather than hiding it.
- **`--data` vs `--body`.** Sample 18 (root help) shows `--data` in the embedded
  example string, but sample 10 confirms the CLI rejects `--data` with `No such
  option: --data`. The actual flag is `--body`. The guide documents `--body` as the
  truth and calls out the help-text drift in Appendix A. The Command Reference is
  authoritative; the help-text example is a known artifact.
- **Non-existent guessed command names.** Samples 12, 13, 15, 17 capture
  `No such command` errors for plausible-but-wrong names (`get-connectors`,
  `get-virtual-edge`, `get-policy-groups-suggestion-list`, `list-tasks`).
  The guide uses these as honest "what you'll see if you guess" examples rather than
  pretending the commands work. The remedy in each case is `<group> --help`.
- **Sample 18 author attribution.** The captured sample includes a real email
  (`mike.korenbaum@elisity.com`) in the `createdBy` field for one policy set. The
  guide replaces it with `service-account@your-org.example` in the displayed JSON
  blob to keep the file tenant-neutral. Other capture data (UUIDs, timestamps,
  numericIds) is preserved verbatim.
- **Sample 18 root-help command count.** The root help text reads "466 commands"
  (436 REST + 20 GraphQL reporting + 7 CLI-native auth/config + 3 CLI-native
  glossary). Older copy in the project may reference "443" (pre-reporting),
  "441", "436", "462", or "465" (pre-`diagnose-low-score`) — all stale. The guide
  uses 466 in prose, matching what the captured help output says. Anyone updating
  these docs should re-capture if the count changes.
- **Sample 09 (distribution zones table).** The captured table is 19 columns wide
  and unreadable on a normal terminal. The guide does not paste the raw table;
  instead it shows the projection-with-JMESPath pattern that produces a usable
  view. The raw command is still listed so a reader can reproduce.
- **CSV format tag.** The CLI emits CSV that doesn't fit cleanly under any of
  `bash` / `json` / `yaml`. Per the task brief allowed list, CSV blocks use the
  `text` language tag in this guide.
- **Exit codes.** The exit-code table in Scripting and automation reflects the
  current implementation behavior. If the CLI changes its exit-code policy, the
  table needs updating — there is no autogeneration link.
- **Insights / AD command names.** Both groups had their list commands renamed
  between CCC versions. Rather than name a specific command that may be wrong on
  some tenants, the guide directs the reader to `<group> --help` to find the
  current command. The Command Reference has the version-pinned names.
- **No mention of architecture or VE internals.** Per the brief, this guide is a
  tool guide, not a product positioning doc. Architecture, enforcement, and
  authentication models are deliberately omitted.
