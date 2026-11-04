# Getting Started with the Elisity CCC CLI

The Elisity CCC CLI is a command-line interface to the Elisity Cloud Control Center API. It provides 525 commands across 12 command groups covering topology, policy, devices, connectors, AD/Entra integration, traffic flows, insights, reporting, and system operations. This release matches CCC 26.10.

This guide walks you through installation, configuration, authentication, and your first commands.

---

## Prerequisites

- **Python 3.10 or later** (`python3 --version` to check)
- **Network access** to your CCC. Use your CCC URL, the address you open the CCC UI at; the examples use `https://ccc.example.com`.
- **API credentials**: an OAuth2 client ID and client secret for your tenant. Ask your CCC administrator, or Elisity Support (support@elisity.com).

---

## Install, upgrade and uninstall

The CLI ships as a wheel attached to each release at
https://github.com/Elisity/elisity-cli/releases. The release version matches the CCC
release the commands were built for (for example `26.10.0` for CCC 26.10).

### 1. Download and check the files

Download `elisity_cli-<version>-py3-none-any.whl` and `SHA256SUMS` from the release into
one folder, then check the wheel against the checksum file:

```bash
# Linux
sha256sum -c SHA256SUMS

# macOS
shasum -a 256 -c SHA256SUMS
```

On Windows (PowerShell), print the hash and compare it with the line for the wheel in
`SHA256SUMS`:

```powershell
Get-FileHash .\elisity_cli-<version>-py3-none-any.whl -Algorithm SHA256
```

### 2. Install

Pick one of the two ways. Both install the `elisity` command and its dependencies
(click, requests, tenacity, rich, pyyaml, jmespath).

**pipx (recommended).** [pipx](https://pipx.pypa.io/) installs the CLI into its own
environment and puts `elisity` on your `PATH`:

```bash
pipx install ./elisity_cli-<version>-py3-none-any.whl
```

**Virtual environment.** If you do not use pipx, install into a venv. Modern Linux
distributions block system-wide `pip install` (PEP 668), so do not skip the venv:

```bash
python3 -m venv ~/.venvs/elisity
source ~/.venvs/elisity/bin/activate
pip install ./elisity_cli-<version>-py3-none-any.whl
```

On Windows (PowerShell):

```powershell
py -m venv $HOME\.venvs\elisity
& $HOME\.venvs\elisity\Scripts\Activate.ps1
pip install .\elisity_cli-<version>-py3-none-any.whl
```

Activate the venv again in every new shell before you run `elisity`.

### 3. Verify the installation

```bash
elisity --version
```

It prints the installed version, for example `elisity, version 26.10.0`.

### Upgrade

Download the new wheel and `SHA256SUMS`, check them as in step 1, then install the new
wheel over the old one. Your profiles in `~/.elisity/config.yaml` are kept.

```bash
# pipx
pipx install --force ./elisity_cli-<new-version>-py3-none-any.whl

# venv (activate it first)
pip install --upgrade ./elisity_cli-<new-version>-py3-none-any.whl
```

Read [CHANGELOG.md](../CHANGELOG.md) before you upgrade: a new CCC release can rename or
remove commands that your scripts call.

### Uninstall

```bash
# pipx
pipx uninstall elisity-cli

# venv (activate it first)
pip uninstall elisity-cli
```

If you installed into a venv only for the CLI, you can delete the venv folder instead
(`rm -rf ~/.venvs/elisity`). Uninstalling does not touch your configuration. To remove
the saved profiles and client secrets as well, delete the configuration folder:

```bash
rm -rf ~/.elisity
```

On Windows, the folder is `%USERPROFILE%\.elisity`.

---

## Configure Your First Profile

The CLI needs three things to connect to a CCC instance: the base URL, a client ID, and a client secret. You can provide these two ways.

### Method 1: Named profiles (recommended)

Named profiles are stored in `~/.elisity/config.yaml` and persist across sessions. Use this for interactive work and when you manage multiple CCC instances.

```bash
elisity config set-profile prod \
  --base-url https://prod-ccc.example.com \
  --client-id YOUR_CLIENT_ID
```

The CLI asks for the client secret and does not echo what you type:

```
Client secret:
Profile 'prod' saved to ~/.elisity/config.yaml
```

If `CCC_CLIENT_SECRET` is set, the CLI uses it instead of asking. Avoid
`--client-secret`: a secret on the command line stays in your shell history.

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
export CCC_BASE_URL=https://ccc.example.com
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
- Your CCC instance is reachable (`curl -s https://ccc.example.com`)
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
command whose API path names a destructive action — the PUT `decommission` and
the Insights reset/recreate commands:

```bash
elisity topology delete-site-v2 <site-id> --confirm
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
  --base-url https://prod-ccc.example.com \
  --client-id YOUR_ID \
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
| `policy` | Policy sets, policies, policy groups, security profiles, labels, access policy (LPA) | 177 |
| `topology` | Sites, distribution zones, VE groups, VEs, VENs, flow exporters | 116 |
| `devices` | Device identity, enrichment, CRUD, bulk operations, cloud workloads (AWS, Azure) | 73 |
| `ad` | Active Directory and Entra ID integration | 39 |
| `connectors` | Connector management and configuration, Tanium sensor mappings | 35 |
| `insights` | Policy suggestions, dynamic/network group recommendations | 31 |
| `system` | Report snapshots and snapshot schedules | 12 |
| `flows` | Traffic flow search, device state, noise definitions | 15 |
| `reporting` | CCC reporting (GraphQL) API — Zero Trust scores, site KPIs, threat vectors | 17 |
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

Add `--debug` to log each HTTP request (URL and status code):

```bash
elisity --debug topology get-all-sites
```

---

## Next Steps

- **[User Guide](user-guide.md)** — Detailed usage patterns, scripting recipes, and advanced workflows
- **[Configuration Reference](configuration.md)** — Profile options, environment variables, SSL settings
- **[Command Reference](command-reference.md)** — Every command with its description
- **[Changelog](../CHANGELOG.md)** — What changed in each release

## Support

Questions, problems, or a command that does not behave as documented: contact Elisity
Support (support@elisity.com). Include the command you ran, the CLI version
(`elisity --version`) and, if you can, the output of the command with `--debug`.
Remove client secrets and tokens before you send output.
