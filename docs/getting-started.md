# Getting Started with the Elisity CCC CLI

The Elisity CCC CLI is a command-line interface to the Elisity Cloud Control Center API. It provides 658 commands across 12 command groups covering topology, policy, devices, connectors, AD/Entra integration, traffic flows, insights, reporting, and system operations. The command set is generated from the CCC 26.9 OpenAPI spec.

This guide walks you through installation, configuration, authentication, and your first commands.

---

## Prerequisites

- **Python 3.10 or later** (`python3 --version` to check)
- **Network access** to your Elisity CCC instance (e.g., `https://your-ccc.idp01.elisity.io`)
- **API credentials** — an OAuth2 client ID and client secret with appropriate scopes, obtained from your CCC administrator

---

## Installation

### Option A: Install from source (development)

```bash
git clone <repo-url> elisity-cli
cd elisity-cli
pip install -e .
```

### Option B: Install from PyPI (when published)

```bash
pip install elisity-cli
```

### Option C: Clone and use a virtual environment

```bash
git clone <repo-url> elisity-cli
cd elisity-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Verify the installation

```bash
elisity --version
```

Expected output:

```
elisity, version 0.1.0
```

All dependencies (click, requests, tenacity, rich, pyyaml, jmespath) are installed automatically.

---

## Configure Your First Profile

The CLI needs three things to connect to a CCC instance: the base URL, a client ID, and a client secret. You can provide these two ways.

### Method 1: Named profiles (recommended)

Named profiles are stored in `~/.elisity/config.yaml` and persist across sessions. Use this for interactive work and when you manage multiple CCC instances.

```bash
elisity config set-profile prod \
  --base-url https://prod-ccc.idp01.elisity.io \
  --client-id YOUR_CLIENT_ID \
  --client-secret 'YOUR_CLIENT_SECRET'
```

Output:

```
Profile 'prod' saved to ~/.elisity/config.yaml
```

The first profile you create becomes the active profile automatically. To switch between profiles:

```bash
# Switch active profile
elisity config use-profile prod

# List all profiles
elisity config list-profiles

# Show active configuration (secrets redacted)
elisity config show
```

You can also select a profile per-command with the `-p` flag:

```bash
elisity -p staging topology get-all-sites
```

### Method 2: Environment variables (CI/scripting)

Environment variables override profile values. Useful in CI pipelines or one-off scripts.

```bash
export CCC_BASE_URL=https://your-ccc.idp01.elisity.io
export CCC_CLIENT_ID=your-client-id
export CCC_CLIENT_SECRET='your-client-secret'
```

Optional: `CCC_TIMEOUT` sets the request timeout in seconds (default: 30).

---

## Verify Authentication

Run the auth test to confirm the CLI can reach your CCC and authenticate:

```bash
elisity auth test
```

Expected output:

```json
{
  "status": "healthy",
  "code": 200,
  "authenticated": true
}
```

If authentication fails, verify:
- Your CCC instance is reachable (`curl -s https://your-ccc.idp01.elisity.io`)
- The client ID and secret are correct
- Your network allows outbound HTTPS to the CCC

Two additional auth commands are available:

```bash
# Decode your current JWT token claims (issuer, roles, expiry)
elisity auth whoami

# Print the raw bearer token (pipe into other tools or curl)
elisity auth token
```

---

## Run Your First Commands

### List all sites

```bash
elisity topology get-all-sites
```

### List virtual edges

```bash
elisity topology get-virtual-edge
```

### Get device count

```bash
elisity devices get-device-header-data
```

(CCC 26.7 renamed this command from `get-device-count`.)

### List policy sets

```bash
elisity policy get-all-as-nd-json
```

### Get a specific site by ID

```bash
elisity topology get-site-v2 <site-id>
```

### Query devices with a request body

Commands that accept a request body use `--body` (inline JSON) or `--body-file` (path to a JSON file):

```bash
# Inline JSON — first 5 devices
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":5}}'

# From a file
elisity devices get-devices-view --body-file request.json
```

### Destructive commands require confirmation

Destructive operations require `--confirm`. That is every `DELETE`, and also any
command whose API path names a destructive action — the POST bulk deletes, the
PUT `decommission`, and the Insights reset/recreate commands:

```bash
elisity topology delete-site-v2 <site-id> --confirm
elisity topology bulk-delete-ve-ns --body '{"ids":["..."]}' --confirm
```

Without the flag the CLI prints `Use --confirm to execute this destructive
operation.` and exits 1 without contacting the API.

---

## Output Formats

Every command supports four output formats via the `-f` flag:

| Flag | Format | Best for |
|------|--------|----------|
| `-f json` | Pretty-printed JSON (default) | Scripting, piping to `jq` |
| `-f table` | Rich terminal table | Interactive browsing |
| `-f yaml` | YAML | Human-readable config review |
| `-f csv` | CSV | Spreadsheet import, reporting |

### Examples

```bash
# Table view of all sites
elisity topology get-all-sites -f table

# YAML output
elisity topology get-all-sites -f yaml

# CSV for export
elisity topology get-all-sites -f csv > sites.csv
```

You can set a default format per profile:

```bash
elisity config set-profile prod \
  --base-url https://prod-ccc.idp01.elisity.io \
  --client-id YOUR_ID \
  --client-secret 'YOUR_SECRET' \
  --default-format table
```

---

## Filter Results with JMESPath

Use `-q` to apply a [JMESPath](https://jmespath.org/) expression to any command's output. This filters and reshapes the JSON response before rendering.

### Extract a single field from each item

```bash
# Site names only
elisity topology get-all-sites -q '[].name'
```

```json
[
  "headquarters",
  "branch-east",
  "branch-west"
]
```

### Count results

```bash
elisity topology get-all-sites -q 'length(@)'
```

```
3
```

### Filter by condition

```bash
# Sites where name contains "branch"
elisity topology get-all-sites -q "[?contains(name, 'branch')]"
```

### Select specific fields

```bash
# Name and ID only, as a table
elisity topology get-all-sites -q '[].{name: name, id: id}' -f table
```

### Combine with output format

JMESPath filtering applies before formatting, so you can query and then render:

```bash
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":10}}' \
  -q 'content[].{ip: ipAddress, mac: macAddress, name: deviceName}' \
  -f table
```

---

## Explore Available Commands

The CLI is organized into 12 command groups:

| Group | Description | Commands |
|-------|-------------|----------|
| `policy` | Policy sets, policies, policy groups, security profiles, labels, access policy (LPA) | 191 |
| `topology` | Sites, distribution zones, VE groups, VEs, VENs, flow exporters | 158 |
| `devices` | Device identity, enrichment, CRUD, bulk operations, cloud workloads (AWS, Azure) | 107 |
| `ad` | Active Directory and Entra ID integration | 57 |
| `connectors` | Connector management and configuration, Tanium sensor mappings | 38 |
| `insights` | Policy suggestions, dynamic/network group recommendations | 31 |
| `system` | Tasks, specs, state sync, report snapshots + schedules | 31 |
| `flows` | Traffic flow search, device state, noise definitions, flow ingestion | 18 |
| `reporting` | GraphQL dashboard data — Zero Trust scores, site KPIs, threat vectors | 17 |
| `config` | CLI profile and configuration management | 4 |
| `auth` | Authentication test, token, whoami | 3 |
| `glossary` | Map Elisity UI terminology to CLI commands | 3 |

### Use `--help` at any level

```bash
# All command groups
elisity --help

# All commands in a group
elisity topology --help

# Parameters for a specific command
elisity topology get-site-v2 --help
```

### Debug mode

Add `--debug` to see HTTP request details (URLs, status codes, timing):

```bash
elisity --debug topology get-all-sites
```

---

## Next Steps

- **[User Guide](user-guide.md)** — Detailed usage patterns, scripting recipes, and advanced workflows
- **[Configuration Reference](configuration.md)** — Profile options, environment variables, SSL settings
- **[Command Reference](command-reference.md)** — Full list of all 658 commands with parameters and examples
