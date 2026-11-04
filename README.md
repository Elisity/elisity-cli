# Elisity CCC CLI

Command-line interface to the Elisity Cloud Control Center (CCC) API. Covers 498 REST endpoints from the OpenAPI spec, plus 17 hand-coded GraphQL commands for the CCC reporting API (Zero Trust scores, threat vectors, per-site KPIs, traffic vectors), plus a 3-command CLI-native `glossary` group that maps Elisity UI terminology to CLI commands.

This release matches **CCC 26.10**. What changed between releases is in [CHANGELOG.md](CHANGELOG.md).

> **For AI agents:** see [docs/AGENTS.md](docs/AGENTS.md) for a UI-term → CLI-command operating guide. The `elisity glossary` group is the runtime lookup surface.

## Features

- **525 commands** total (498 auto-generated from the CCC OpenAPI spec + 17 hand-coded GraphQL reporting commands + 7 CLI-native auth/config + 3 CLI-native glossary commands)
- **Multi-profile configuration** — manage multiple CCC environments (prod, staging, lab)
- **4 output formats** — JSON (default), table, YAML, CSV
- **JMESPath filtering** — reshape and filter output with `-q` expressions
- **OAuth2 authentication** — client_credentials grant with auto-refresh
- **NDJSON support** — transparent parsing of newline-delimited JSON endpoints
- **GraphQL reporting** — the `reporting` group wraps the CCC dashboard's reporting queries (Zero Trust scores, site KPIs, threat vectors, traffic-by-PG/IP)
- **UI-term glossary** — `glossary` group answers "what command runs the Zero Trust Score tile?" without guesswork
- **Destructive-op safety** — `--confirm` required for all 48 destructive commands: every DELETE, plus PUT decommission, Insights reset/recreate, the AD groups "master reset" and the Entra ID instance update
- **Retry with backoff** — automatic retry on connection errors and timeouts

## Install

You need Python 3.10 or later. Download `elisity_cli-<version>-py3-none-any.whl` and
`SHA256SUMS` from https://github.com/Elisity/elisity-cli/releases into one folder, then:

```bash
# Check the download (macOS: shasum -a 256 -c SHA256SUMS)
sha256sum -c SHA256SUMS

# Install with pipx (recommended) ...
pipx install ./elisity_cli-<version>-py3-none-any.whl

# ... or into a virtual environment
python3 -m venv ~/.venvs/elisity
source ~/.venvs/elisity/bin/activate
pip install ./elisity_cli-<version>-py3-none-any.whl

elisity --version
```

Upgrade by installing the newer wheel (`pipx install --force <wheel>` or
`pip install --upgrade <wheel>`). Uninstall with `pipx uninstall elisity-cli` or
`pip uninstall elisity-cli`; your profiles stay in `~/.elisity` until you delete that
folder. Windows steps and details: [Install, upgrade and uninstall](docs/getting-started.md#install-upgrade-and-uninstall).

## Quick Start

Use your CCC URL, the address you open the CCC UI at, and the API client ID and secret
for your tenant (ask your CCC administrator or Elisity Support).

```bash
# Configure: the CLI asks for the client secret and does not echo it
elisity config set-profile myenv \
  --base-url https://ccc.example.com \
  --client-id YOUR_CLIENT_ID

# Verify
elisity auth test

# What command runs the "Zero Trust Score" tile in the UI?
elisity glossary explain "Zero Trust score"
```

**Or use environment variables:**

```bash
export CCC_BASE_URL=https://ccc.example.com
export CCC_CLIENT_ID=YOUR_CLIENT_ID
export CCC_CLIENT_SECRET='YOUR_CLIENT_SECRET'
elisity auth test
```

The profile, including the client secret, is stored in plain text in
`~/.elisity/config.yaml`. On Linux and macOS the CLI keeps that file readable by your
user only. See [Configuration](docs/configuration.md#security-considerations) for details.

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

# Tenant Zero Trust score (reporting API)
elisity reporting get-aggregate-enforcement-score

# Per-site KPI dashboard (devices, VENs, policy counts, enforcement score)
elisity -f table reporting get-site-kpis

# Map UI term → CLI command
elisity glossary search "monitor mode"
elisity glossary explain "VEN"

# Get bearer token for use in scripts
TOKEN=$(elisity auth token)
curl -H "Authorization: Bearer $TOKEN" https://ccc.example.com/api/topology/v2/sites
```

## Command Groups

| Group | Commands | Description |
|-------|----------|-------------|
| `topology` | 116 | Sites, distribution zones, workload distribution zones, VE groups, VEs, VENs, VE/VEN metrics summaries, flow exporters, cloud controllers, interface settings |
| `policy` | 177 | Policy sets, policies, policy groups, security profiles + access policy security profiles (search/export), policy reviews, site labels, label management, access policy (LPA), custom applications, vendors |
| `devices` | 73 | Device CRUD, bulk operations, enrichment, suppression list, custom attributes, cloud workloads + AWS and Azure discovery |
| `ad` | 39 | Active Directory / Entra ID connectors, Entra ID instances, agents, agent logs, AD group enablement |
| `connectors` | 35 | Connector configuration, custom connector devices/inventory, import/export, connectivity, Tanium sensor mappings |
| `insights` | 31 | Policy suggestions, dynamic/network group recommendations |
| `flows` | 15 | Traffic flow search, device state, noise definitions, device heatmap |
| `system` | 12 | Report snapshots (PDF, Markdown, evidence) and snapshot schedules |
| `reporting` | 17 | CCC reporting (GraphQL) API — Zero Trust scores, site KPIs, threat vectors, traffic-by-PG/IP |
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
# Create profiles for different environments (each asks for its client secret)
elisity config set-profile prod --base-url https://prod-ccc.example.com --client-id ID
elisity config set-profile lab  --base-url https://lab-ccc.example.com  --client-id ID

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
- Network access to your CCC
- OAuth2 API client credentials for your tenant (client ID + secret)

## Dependencies

Installed automatically with the wheel:

- [Click](https://click.palletsprojects.com/) — CLI framework
- [Requests](https://requests.readthedocs.io/) — HTTP client
- [Tenacity](https://tenacity.readthedocs.io/) — Retry logic
- [Rich](https://rich.readthedocs.io/) — Terminal table rendering
- [PyYAML](https://pyyaml.org/) — YAML output and config parsing
- [JMESPath](https://jmespath.org/) — Query language for JSON

## Documentation

- [Getting Started](docs/getting-started.md) — Install, upgrade, uninstall and first-time setup
- [User Guide](docs/user-guide.md) — Workflow-oriented guide with real examples
- [AI Agent Operating Guide](docs/AGENTS.md) — How an AI agent should run the CLI on a human's behalf
- [Glossary Appendix](docs/glossary.md) — UI term → CLI command reference (human-readable)
- [Configuration Reference](docs/configuration.md) — Profiles, env vars, output formats, JMESPath
- [Command Reference](docs/command-reference.md) — All 525 commands with descriptions
- [Changelog](CHANGELOG.md) — What changed in each release; read it before you upgrade

## Support

Contact Elisity Support (support@elisity.com). Include the command you ran, the output of
`elisity --version` and, if you can, the command's output with `--debug`. Remove client
secrets and tokens before you send anything.

## License

Proprietary - Elisity, Inc.
