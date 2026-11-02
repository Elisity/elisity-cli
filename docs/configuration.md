# Configuration Reference

The Elisity CLI stores connection profiles in `~/.elisity/config.yaml` and supports
environment variable overrides for CI/CD and scripting use cases. This document covers
the full configuration system: profiles, environment variables, authentication,
output formatting, and query filtering.

---

## Quick Setup

In the examples below, use your CCC URL, the address you open the CCC UI at, in
place of the `example.com` hosts.

**Interactive use** -- create a named profile:

```bash
elisity config set-profile prod \
  --base-url https://prod-ccc.example.com \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET
```

**CI/CD and scripting** -- export environment variables (no config file needed):

```bash
export CCC_BASE_URL=https://ccc.example.com
export CCC_CLIENT_ID=YOUR_CLIENT_ID
export CCC_CLIENT_SECRET=YOUR_CLIENT_SECRET
elisity auth test
```

Verify connectivity:

```bash
elisity auth test
```

---

## Config File

**Location:** `~/.elisity/config.yaml`

The file is created automatically on the first `elisity config set-profile` call.
The `~/.elisity/` directory is created if it does not exist.

### Structure

```yaml
profiles:
  prod:
    base_url: https://prod-ccc.example.com
    client_id: YOUR_PROD_CLIENT_ID
    client_secret: YOUR_PROD_CLIENT_SECRET
    timeout: 30
    default_format: json
  staging:
    base_url: https://staging-ccc.example.com
    client_id: YOUR_STAGING_CLIENT_ID
    client_secret: YOUR_STAGING_CLIENT_SECRET
    timeout: 60
    default_format: table
  lab:
    base_url: https://lab-ccc.example.com
    client_id: YOUR_LAB_CLIENT_ID
    client_secret: YOUR_LAB_CLIENT_SECRET
    verify_ssl: false
    timeout: 30
    default_format: json
active_profile: prod
```

### Profile Fields

| Field | Type | Default | Description |
|---|---|---|---|
| `base_url` | string | *(required)* | CCC instance URL (e.g., `https://ccc.example.com`) |
| `client_id` | string | *(required)* | OAuth2 service account client ID |
| `client_secret` | string | *(required)* | OAuth2 service account client secret |
| `timeout` | integer | `30` | HTTP request timeout in seconds |
| `default_format` | string | `json` | Output format: `json`, `table`, `yaml`, or `csv` |
| `verify_ssl` | boolean | `true` | Verify TLS certificates. Set `false` for lab/self-signed environments. |

---

## Profile Management

### Create or update a profile

```bash
elisity config set-profile NAME \
  --base-url URL \
  --client-id ID \
  --client-secret SECRET \
  [--timeout 30] \
  [--default-format json]
```

If no `active_profile` is set yet, the first profile created becomes the active profile
automatically.

### Switch the active profile

```bash
elisity config use-profile NAME
```

Fails with an error if `NAME` does not exist in the config file.

### List all profiles

```bash
elisity config list-profiles
```

Returns JSON with all profiles. Each profile includes an `_active: true|false` marker
indicating which profile is currently active.

### Show active configuration

```bash
elisity config show
```

Displays the resolved active configuration with **secrets redacted** (`***`). Useful for
confirming which base URL, client ID, and settings are in effect. Respects the `-f` flag:

```bash
elisity -f table config show
```

### Delete a profile

Edit `~/.elisity/config.yaml` directly and remove the profile entry. If the deleted
profile was the `active_profile`, update `active_profile` to another profile name.

---

## Environment Variables

Environment variables override the corresponding field in the active profile. This is
the recommended approach for CI/CD pipelines, containers, and scripted automation.

| Variable | Overrides Profile Field | Description |
|---|---|---|
| `CCC_BASE_URL` | `base_url` | CCC instance URL |
| `CCC_CLIENT_ID` | `client_id` | OAuth2 service account client ID |
| `CCC_CLIENT_SECRET` | `client_secret` | OAuth2 service account client secret |
| `CCC_TIMEOUT` | `timeout` | HTTP request timeout in seconds |

### Resolution Order

Each configuration field is resolved independently using this priority:

1. **Environment variable** (highest priority)
2. **Active profile** in `~/.elisity/config.yaml`

If a field is set in the environment, the profile value for that specific field is
ignored. Other fields still come from the profile. For example, you can set
`CCC_BASE_URL` in the environment to temporarily point at a different instance while
still using the profile's client credentials.

### Per-Command Profile Override

The `-p` / `--profile` flag overrides the active profile for a single command:

```bash
elisity -p staging topology get-all-sites-v2
```

When `-p` is used, the named profile's values are merged on top of the resolved
configuration, so they take precedence over environment variables. A field the
`-p` profile does not set still comes from the environment or the active profile.

Effective resolution order with `-p`:

1. Profile specified by `-p` (highest)
2. Environment variable
3. Active profile in config.yaml (lowest)

---

## Authentication

### OAuth2 Client Credentials

The CLI authenticates using the OAuth2 `client_credentials` grant. This is a
machine-to-machine flow -- no browser login, no user interaction.

**Token endpoint:** the CCC token endpoint on your `base_url`.

**Grant parameters:**

| Parameter | Value |
|---|---|
| `grant_type` | `client_credentials` |
| `client_id` | From profile or `CCC_CLIENT_ID` |
| `client_secret` | From profile or `CCC_CLIENT_SECRET` |
| `scope` | `openid` |

### Token Lifecycle

- Tokens are obtained lazily on the first API call in a session.
- The token is cached in memory for the duration of the CLI invocation.
- The client auto-refreshes the token **60 seconds before expiry** to prevent
  mid-request failures.
- On a **401 response**, the client invalidates the cached token and retries the
  request with a fresh token automatically.

### Retry Policy

Connection errors and timeouts are retried with exponential backoff:

| Parameter | Value |
|---|---|
| Max attempts | 3 |
| Backoff | Exponential, 2s minimum, 10s maximum |
| Retried errors | `ConnectionError`, `Timeout` |
| Not retried | HTTP 4xx/5xx (except 401 token refresh) |

### Auth Commands

```bash
# Test connectivity and authentication
elisity auth test

# Get a raw access token (for use in scripts or curl)
elisity auth token

# Decode and display the current JWT claims
elisity auth whoami
```

---

## Global CLI Options

These options apply to all commands when they appear before the command group name.

| Option | Short | Type | Default | Description |
|---|---|---|---|---|
| `--version` | | flag | | Print CLI version and exit |
| `--format` | `-f` | choice | `json` | Output format: `json`, `table`, `yaml`, `csv` |
| `--query` | `-q` | string | | JMESPath expression to filter/reshape output |
| `--debug` | | flag | `false` | Enable debug logging (one log line per HTTP request: method, path, status) |
| `--profile` | `-p` | string | | Use a named profile for this invocation only |

### Syntax

```bash
elisity [GLOBAL OPTIONS] COMMAND [COMMAND OPTIONS] [ARGS]
```

Global options before the command group work for every command:

```bash
elisity -f table -q '[].name' topology get-all-sites-v2
elisity -f table reporting get-site-kpis
```

Commands in the API groups (`ad`, `connectors`, `devices`, `flows`, `insights`,
`policy`, `system`, `topology`) also accept `-f` and `-q` after the command
name, although `--help` does not list them. `reporting`, `glossary`, `auth` and
`config` commands do not, and `--version`, `--debug` and `-p` only work before
the group:

```bash
# Also correct -- topology commands accept -f/-q after the command name
elisity topology get-all-sites-v2 -f table

# WRONG -- reporting commands do not; this exits 2 with "No such option"
elisity reporting get-site-kpis -f table
```

---

## Output Formats

The `-f` flag controls how results are rendered to stdout. The default format is `json`
unless the active profile sets `default_format` to something else.

### json (default)

Pretty-printed JSON with 2-space indentation. Suitable for piping to `jq`, storing as
files, or feeding into other tools.

```bash
elisity topology get-all-sites-v2
```

```json
[
  {
    "id": "site-001",
    "name": "HQ",
    "status": "ACTIVE"
  }
]
```

### table

Rich terminal table with colored headers (bold cyan). Columns auto-wrap at 60
characters. Nested objects and arrays are serialized to JSON and truncated to 80
characters for readability.

Paginated responses (those containing a `content` array) are automatically unwrapped
so the table displays the items directly.

```bash
elisity -f table topology get-all-sites-v2
```

### yaml

YAML serialization with block style (no flow style). Keys preserve their original
order.

```bash
elisity -f yaml topology get-all-sites-v2
```

### csv

CSV with a header row derived from the first item's keys. Paginated responses are
automatically unwrapped from the `content` array.

Suitable for import into spreadsheets or processing with `awk`/`cut`:

```bash
elisity -f csv devices get-devices-view --body '{"pageable":{"page":0,"size":500}}' > devices.csv
```

---

## JMESPath Query Reference

The `-q` flag accepts a [JMESPath](https://jmespath.org/) expression applied to the
API response before formatting. The full JMESPath specification is supported.

### Practical Examples

**Extract a single field from a list:**

```bash
elisity -q '[].name' topology get-all-sites-v2
```

**Filter by field value:**

```bash
elisity -q "[?status=='ACTIVE']" devices get-devices-view --body '{"pageable":{"page":0,"size":500}}'
```

**First N items:**

```bash
elisity -q '[0:5]' topology get-all-sites-v2
```

**Count items:**

```bash
elisity -q 'length(@)' topology get-all-sites-v2
```

**Select specific fields:**

```bash
elisity -q '[].{id: id, name: name, status: status}' topology get-all-sites-v2
```

**Select fields from a paginated response:**

```bash
elisity -q 'content[].{id: id, name: name}' devices get-devices-view
```

**Reshape into a summary object:**

```bash
elisity -q '{names: [].name, total: length(@)}' topology get-all-sites-v2
```

**Nested field access:**

```bash
elisity -q '[].config.vlanId' connectors read-all-connectors
```

**Sort by field:**

```bash
elisity -q 'sort_by(@, &name)' topology get-all-sites-v2
```

**Combine filter and projection:**

```bash
elisity -q "[?status=='ACTIVE'].{name: name, id: id}" devices get-devices-view --body '{"pageable":{"page":0,"size":500}}'
```

**Get the first matching item:**

```bash
elisity -q "[?name=='HQ'] | [0]" topology get-all-sites-v2
```

**Check for existence:**

```bash
elisity -q "[?description != null].name" topology get-all-sites-v2
```

**Multi-select with computed fields:**

```bash
elisity -q '{active: length([?status==`ACTIVE`]), total: length(@)}' devices get-devices-view --body '{"pageable":{"page":0,"size":500}}'
```

### Error Handling

If the JMESPath expression is invalid, the CLI prints the error to stderr and exits
with a non-zero status code. The raw API response is not printed.

---

## Multi-Environment Workflow

### Profile per Environment

Create a profile for each CCC instance:

```bash
# Production
elisity config set-profile prod \
  --base-url https://prod-ccc.example.com \
  --client-id YOUR_PROD_CLIENT_ID \
  --client-secret YOUR_PROD_CLIENT_SECRET

# Staging
elisity config set-profile staging \
  --base-url https://staging-ccc.example.com \
  --client-id YOUR_STAGING_CLIENT_ID \
  --client-secret YOUR_STAGING_CLIENT_SECRET \
  --timeout 60

# Lab (self-signed certs)
elisity config set-profile lab \
  --base-url https://lab-ccc.example.com \
  --client-id YOUR_LAB_CLIENT_ID \
  --client-secret YOUR_LAB_CLIENT_SECRET
```

Switch between environments:

```bash
elisity config use-profile staging
elisity auth test

elisity config use-profile prod
elisity auth test
```

Or use `-p` for one-off commands without switching:

```bash
elisity -p staging topology get-all-sites-v2
elisity -p prod topology get-all-sites-v2
```

### CI/CD Integration

Use environment variables exclusively. No config file is required.
For installing, upgrading and uninstalling the CLI, see [Getting Started](getting-started.md#install-upgrade-and-uninstall).

**GitHub Actions example:**

```yaml
jobs:
  deploy-policy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install CLI
        # Pin the release wheel; see https://github.com/Elisity/elisity-cli/releases
        run: pip install https://github.com/Elisity/elisity-cli/releases/download/v<version>/elisity_cli-<version>-py3-none-any.whl
      - name: Apply policy
        env:
          CCC_BASE_URL: ${{ secrets.CCC_BASE_URL }}
          CCC_CLIENT_ID: ${{ secrets.CCC_CLIENT_ID }}
          CCC_CLIENT_SECRET: ${{ secrets.CCC_CLIENT_SECRET }}
        run: |
          elisity auth test
          elisity policy get-all-as-nd-json -f json
```

**Shell script example:**

```bash
#!/usr/bin/env bash
set -euo pipefail

export CCC_BASE_URL="https://ccc.example.com"
export CCC_CLIENT_ID="${CCC_CLIENT_ID:?missing}"
export CCC_CLIENT_SECRET="${CCC_CLIENT_SECRET:?missing}"

elisity auth test
elisity -f csv devices get-devices-view --body '{"pageable":{"page":0,"size":500}}' > inventory.csv
```

### Cross-Environment Comparison

```bash
# Compare site counts between staging and prod
echo "Staging sites:"
elisity -p staging -q 'length(@)' topology get-all-sites-v2

echo "Prod sites:"
elisity -p prod -q 'length(@)' topology get-all-sites-v2
```

---

## Security Considerations

### Secret Storage

- **`~/.elisity/config.yaml` contains client secrets in plain text.** Set restrictive
  file permissions:

  ```bash
  chmod 600 ~/.elisity/config.yaml
  ```

- For CI/CD, use environment variables backed by your platform's secrets manager
  (GitHub Secrets, Vault, AWS Secrets Manager). Do not store secrets in pipeline
  definition files.

- The `elisity config show` command **redacts secrets** by replacing any field
  containing `secret` in the key name with `***`. This makes it safe to share output
  for debugging without exposing credentials.

### Token Handling

- Access tokens are held in memory only. They are never written to disk.
- The `elisity auth token` command outputs the raw token to stdout. Pipe carefully --
  avoid logging it.

### SSL Verification

- SSL verification is **enabled by default** (`verify_ssl: true`).
- Set `verify_ssl: false` in a profile only for lab environments with self-signed
  certificates. Do not disable SSL verification in production.
- `verify_ssl` can only be set in the config file (not via environment variable).

### Least Privilege

- Use dedicated service accounts per environment.
- Do not share client credentials across production and non-production environments.

---

## Troubleshooting

### "No CCC_BASE_URL configured"

The CLI cannot find a base URL. Either:
- No active profile is set, or
- The active profile does not have `base_url` defined, and `CCC_BASE_URL` is not set.

Fix:

```bash
elisity config set-profile default \
  --base-url https://ccc.example.com \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET
```

Or export the environment variable:

```bash
export CCC_BASE_URL=https://ccc.example.com
```

### "Missing CCC_CLIENT_ID or CCC_CLIENT_SECRET"

Client credentials are not configured. Provide them via a profile or environment
variables.

### "Profile 'X' does not exist"

You tried to switch to or use a profile that is not defined. List available profiles:

```bash
elisity config list-profiles
```

### "CCC authentication failed. Check credentials."

The OAuth2 token request failed. Common causes:
- Incorrect `client_id` or `client_secret`
- Wrong `base_url` (not reaching the correct CCC instance)
- Network connectivity issue
- Service account is disabled or expired

The CLI writes the token endpoint's HTTP status and the start of its error
response to stderr. For more detail, run:

```bash
elisity --debug auth test
```

This adds a log line for each HTTP request the CLI makes (host, method, path and
response status), so you can confirm which CCC instance it reached.

### Connection timeouts

If requests are timing out, increase the timeout:

```bash
# Via environment variable
export CCC_TIMEOUT=120

# Via profile
elisity config set-profile prod \
  --base-url https://prod-ccc.example.com \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET \
  --timeout 120
```

### SSL certificate errors

For lab environments with self-signed certificates, edit `~/.elisity/config.yaml`
directly and add `verify_ssl: false` to the profile:

```yaml
profiles:
  lab:
    base_url: https://lab-ccc.example.com
    client_id: YOUR_LAB_CLIENT_ID
    client_secret: YOUR_LAB_CLIENT_SECRET
    verify_ssl: false
```

Do not disable SSL verification in production environments.

### Debug mode

Use `--debug` to enable HTTP logging. This sets the Python `logging` level to `DEBUG`
(including `urllib3`), which writes to stderr a line for each connection opened and
for each HTTP request: method, path with query string, response status and size, plus
the CLI's own token-refresh messages. It does not print request or response headers
or bodies, and it has no effect on commands that make no API call (`config`,
`glossary`):

```bash
elisity --debug auth test
elisity --debug topology get-all-sites-v2
```
