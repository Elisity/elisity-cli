# Elisity CLI — Comprehensive QA Test Plan

**Version:** 1.0
**Status:** Draft
**Created:** 2026-04-06
**Target:** elisity-cli v0.1.0 (442 commands across 10 groups)
**CCC Target:** <your-ccc>.idp01.elisity.io

---

## Overview

This test plan validates every functional area of the `elisity` CLI tool. Tests are organized into categories that progress from basic installation through full CRUD lifecycle operations. Each test specifies the exact command, expected outcome, and verification method.

**Test Environment:**
- Host: 10.0.0.175 (Ubuntu Linux)
- Python: 3.x with venv at `/home/elisity/Projects/elisity-cli/.venv`
- Profile: `mike-lab` (stored in `~/.elisity/config.yaml`)
- CCC: `https://<your-ccc>.idp01.elisity.io`
- Credentials: Service account `<your-service-account-id>`

---

## Category 1: Installation & Help System

### 1.1 Package Installation
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 1.1.1 | pip install in editable mode | `pip install -e .` | Installs without errors | Exit code 0 |
| 1.1.2 | CLI entry point exists | `which elisity` | Returns path to binary | Path exists in .venv/bin |
| 1.1.3 | Version flag | `elisity --version` | Prints `elisity, version 0.1.0` | Output matches |

### 1.2 Help System
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 1.2.1 | Root help | `elisity --help` | Lists all 10 groups (topology, policy, devices, connectors, ad, flows, insights, system, auth, config) | All 10 present |
| 1.2.2 | Topology group help | `elisity topology --help` | Lists 100+ topology commands | Command count ≥ 100 |
| 1.2.3 | Policy group help | `elisity policy --help` | Lists 90+ policy commands | Command count ≥ 90 |
| 1.2.4 | Devices group help | `elisity devices --help` | Lists 50+ device commands | Command count ≥ 50 |
| 1.2.5 | Connectors group help | `elisity connectors --help` | Lists 15+ connector commands | Command count ≥ 15 |
| 1.2.6 | AD group help | `elisity ad --help` | Lists 50+ AD commands | Command count ≥ 50 |
| 1.2.7 | Flows group help | `elisity flows --help` | Lists 10+ flow commands | Command count ≥ 10 |
| 1.2.8 | Insights group help | `elisity insights --help` | Lists 20+ insight commands | Command count ≥ 20 |
| 1.2.9 | System group help | `elisity system --help` | Lists 10+ system commands | Command count ≥ 10 |
| 1.2.10 | Auth group help | `elisity auth --help` | Lists: test, token, whoami | All 3 present |
| 1.2.11 | Config group help | `elisity config --help` | Lists: set-profile, use-profile, list-profiles, show | All 4 present |
| 1.2.12 | Individual command help | `elisity topology get-all-sites --help` | Shows command description, options | Has --help output |
| 1.2.13 | Total command count | Python: sum all group.commands | ≥ 430 generated commands | Assert total ≥ 430 |

---

## Category 2: Authentication

### 2.1 OAuth2 Flow
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 2.1.1 | Auth test (healthy) | `elisity auth test` | `{"status": "healthy", "authenticated": true, ...}` | JSON has status=healthy |
| 2.1.2 | Auth token | `elisity auth token` | Prints JWT (long string, 3 dot-separated parts) | len > 50, contains 2 dots |
| 2.1.3 | Auth whoami | `elisity auth whoami` | JSON with `iss`, `sub`, `exp` claims | Has `iss` containing "elisity" |
| 2.1.4 | Auth with bad credentials | Set bad env vars, run `elisity auth test` | Error message, non-zero exit | exit_code != 0 |
| 2.1.5 | Token auto-refresh | Make 2 API calls separated by token expiry | Second call succeeds (auto re-auth) | No 401 errors |

### 2.2 Profile-Based Auth
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 2.2.1 | Use named profile | `elisity --profile mike-lab auth test` | Authenticates using mike-lab profile | status=healthy |
| 2.2.2 | Invalid profile name | `elisity --profile nonexistent auth test` | Error: profile not found | Error message + exit 1 |

---

## Category 3: Configuration Management

### 3.1 Profile CRUD
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 3.1.1 | Set new profile | `elisity config set-profile test-qa --base-url https://test.io --client-id x --client-secret y` | "Profile 'test-qa' saved" | Output contains "saved" |
| 3.1.2 | List profiles | `elisity config list-profiles` | Shows mike-lab and test-qa | Both names in output |
| 3.1.3 | Switch active profile | `elisity config use-profile mike-lab` | "Switched to profile 'mike-lab'" | Output contains "Switched" |
| 3.1.4 | Show config (redacted) | `elisity config show` | Shows config with secrets as `***` | "client_secret": "***" |
| 3.1.5 | Switch to invalid profile | `elisity config use-profile nonexistent` | Error message | exit_code = 1 |

### 3.2 Environment Variable Override
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 3.2.1 | Env vars take precedence | Set CCC_BASE_URL/CCC_CLIENT_ID/CCC_CLIENT_SECRET env vars | Auth uses env vars, not config file | Successful auth against env-specified CCC |
| 3.2.2 | Partial env vars | Set only CCC_BASE_URL | Falls back to config for missing values | Mixed source works |

---

## Category 4: Output Formats

All format tests use `elisity topology get-all-sites` as the reference command (returns a list of site objects).

### 4.1 JSON Output
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 4.1.1 | Default format (JSON) | `elisity topology get-all-sites` | Valid JSON array | `json.loads()` succeeds |
| 4.1.2 | Explicit JSON flag | `elisity -f json topology get-all-sites` | Same as default | `json.loads()` succeeds |
| 4.1.3 | JSON dict response | `elisity devices get-device-count` | Valid JSON object | Has `devicesCount` key |

### 4.2 Table Output
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 4.2.1 | Table format (list) | `elisity -f table topology get-all-sites` | Rich table with headers | Contains table border chars (─ or ━) |
| 4.2.2 | Table format (dict) | `elisity -f table devices get-device-count` | Key-value table | Contains "devicesCount" |
| 4.2.3 | Table format (paginated) | `elisity -f table devices get-devices-view --body '{"page":0,"size":5}'` | Table of content items | Contains column headers |

### 4.3 YAML Output
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 4.3.1 | YAML format | `elisity -f yaml topology get-all-sites` | Valid YAML | Contains `- id:` or `label:` |
| 4.3.2 | YAML dict | `elisity -f yaml devices get-device-count` | YAML key-value | Contains `devicesCount:` |

### 4.4 CSV Output
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 4.4.1 | CSV format (list) | `elisity -f csv topology get-all-sites` | CSV with headers | First line has `id` |
| 4.4.2 | CSV handles nested | `elisity -f csv topology get-all-sites` | Nested objects serialized | No crash |

---

## Category 5: JMESPath Query Filtering

| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 5.1 | Extract field list | `elisity -q '[].label' topology get-all-sites` | JSON array of strings | All items are strings |
| 5.2 | Filter expression | `elisity -q '[?id!=null].id' topology get-all-sites` | Filtered list | Only non-null IDs |
| 5.3 | Nested access | `elisity -q 'devicesCount' devices get-device-count` | Single integer value | Is a number |
| 5.4 | Slice expression | `elisity -q '[:2]' topology get-all-sites` | First 2 items | len = 2 |
| 5.5 | Combined with format | `elisity -f table -q '[].{Name:label,ID:id}' topology get-all-sites` | Table with Name and ID columns | Table has both columns |
| 5.6 | Invalid query | `elisity -q 'invalid[[[' topology get-all-sites` | Error message (graceful) | No Python traceback |

---

## Category 6: Command Group Read Operations

Each group is tested with at least 2-3 read-only (GET) operations to verify the auto-generated commands work end-to-end against the live CCC.

### 6.1 Topology (116 commands)
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 6.1.1 | List all sites | `elisity topology get-all-sites` | JSON array of sites | Has id, label fields |
| 6.1.2 | Get site v2 (by ID) | `elisity topology get-site-v2 <site-id>` | Single site JSON | Has matching id |
| 6.1.3 | List virtual edges | `elisity topology get-virtual-edge` | Paginated response | Has `content` key |
| 6.1.4 | List VENs | `elisity topology get-virtual-edge-nodes` | Paginated response | Has `content` key |
| 6.1.5 | List switches | `elisity topology get-switch` | Response with switches | Valid JSON |
| 6.1.6 | Get dashboard topology | `elisity topology get-site-topology-for-dashboard <site-id>` | Topology data | Valid JSON |

### 6.2 Policy (116 commands)
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 6.2.1 | List all policy sets (NDJSON) | `elisity policy get-all-as-nd-json` | JSON array of policies | Has `name` field |
| 6.2.2 | List security profiles (NDJSON) | `elisity policy get-all-security-profiles-as-nd-json` | JSON array | Is a list |
| 6.2.3 | Get policy groups | `elisity policy get-policy-groups-json` | Paginated response | Has `content` key |
| 6.2.4 | List service definitions | `elisity policy get-all-service-definitions-json` | JSON array | Valid JSON |
| 6.2.5 | Get policy stats | `elisity policy get-policy-details-count` | Stats object | Valid JSON |

### 6.3 Devices (59 commands)
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 6.3.1 | Device count | `elisity devices get-device-count` | `{"devicesCount": N}` | devicesCount ≥ 0 |
| 6.3.2 | Devices view (POST with body) | `elisity devices get-devices-view --body '{"page":0,"size":5}'` | Paginated device list | Has totalElements, content |
| 6.3.3 | Device categories | `elisity devices get-device-asset-categories` | Category list | Valid JSON |
| 6.3.4 | Device group count | `elisity devices get-device-group-count` | Count object | Valid JSON |

### 6.4 Connectors (22 commands)
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 6.4.1 | List connectors | `elisity connectors read` | JSON array of connectors | Is a list |
| 6.4.2 | Connector health | `elisity connectors get-all-connector-health` | Health data | Valid JSON |

### 6.5 AD / Entra (61 commands)
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 6.5.1 | List AD configurations | `elisity ad get-all-ad-config` | AD config list | Valid JSON |
| 6.5.2 | AD connection status | `elisity ad get-ad-connection-status` | Status data | Valid JSON |
| 6.5.3 | Entra configurations | `elisity ad get-all-entra-config` | Entra config list | Valid JSON |

### 6.6 Flows (18 commands)
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 6.6.1 | Noise definitions | `elisity flows get-noise-definition` | Noise def object | Has `id` key |
| 6.6.2 | Flow categories | `elisity flows get-flow-categories` | Category data | Valid JSON |

### 6.7 Insights (30 commands)
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 6.7.1 | Dashboard stats | `elisity insights get-dashboard-device-count` | Device count stats | Valid JSON |
| 6.7.2 | Compliance stats | `elisity insights get-compliance-stats` | Compliance data | Valid JSON |

### 6.8 System (12 commands)
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 6.8.1 | System settings | `elisity system get-systems-settings-v2` | Settings object | Valid JSON |
| 6.8.2 | SMTP config | `elisity system get-smtp-config` | SMTP settings | Valid JSON |
| 6.8.3 | Audit trail | `elisity system get-audit-trail --body '{"page":0,"size":5}'` | Paginated audit entries | Has content key |

---

## Category 7: CRUD Lifecycle Operations

End-to-end create → read → update → delete cycle using a test resource.

### 7.1 Site Lifecycle
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 7.1.1 | Create test site | `elisity topology create-site-v2 --body '{"label":"qa-test-site","description":"QA automation test"}'` | Site created, returns ID | Has `id` in response |
| 7.1.2 | Read created site | `elisity topology get-site-v2 <new-site-id>` | Returns created site | label = "qa-test-site" |
| 7.1.3 | Update site | `elisity topology update-site-v2 <new-site-id> --body '{"label":"qa-test-site-updated","description":"Updated by QA"}'` | Site updated | Successful response |
| 7.1.4 | Verify update | `elisity topology get-site-v2 <new-site-id>` | Returns updated site | label = "qa-test-site-updated" |
| 7.1.5 | Delete site | `elisity topology delete-site-v2 <new-site-id> --confirm` | Site deleted | Successful response |
| 7.1.6 | Verify deletion | `elisity topology get-site-v2 <new-site-id>` | 404 or error | Not found |

### 7.2 Policy Lifecycle
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 7.2.1 | Create service definition | `elisity policy create-service-definition --body '{"name":"qa-svcdef","protocol":"TCP","port":"9999"}'` | Created | Has id |
| 7.2.2 | Read service definition | `elisity policy get-service-definition <id>` | Returns created | name = "qa-svcdef" |
| 7.2.3 | Delete service definition | `elisity policy delete-service-definition <id> --confirm` | Deleted | Success |

---

## Category 8: Special Endpoint Types

### 8.1 NDJSON Endpoints
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 8.1.1 | Policy sets (NDJSON) | `elisity policy get-all-as-nd-json` | Parsed NDJSON → JSON array | Is a list, len > 0 |
| 8.1.2 | Security profiles (NDJSON) | `elisity policy get-all-security-profiles-as-nd-json` | Parsed NDJSON → JSON array | Is a list |
| 8.1.3 | Service definitions (NDJSON) | `elisity policy get-all-service-definitions-nd-json` | Parsed NDJSON → JSON array | Is a list |

### 8.2 Pagination
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 8.2.1 | Page 0, size 5 | `elisity devices get-devices-view --body '{"page":0,"size":5}'` | 5 or fewer items | len(content) ≤ 5 |
| 8.2.2 | Page 1, size 5 | `elisity devices get-devices-view --body '{"page":1,"size":5}'` | Next page | Different content from page 0 |

### 8.3 Request Body (POST/PUT)
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 8.3.1 | --body inline JSON | `elisity devices get-devices-view --body '{"page":0,"size":5}'` | Accepted | Valid response |
| 8.3.2 | --body-file from file | Write JSON to /tmp/test-body.json, then `elisity devices get-devices-view --body-file /tmp/test-body.json` | Accepted | Valid response |
| 8.3.3 | Missing required body | `elisity devices get-devices-view` (no --body) | Graceful error or empty body sent | No Python traceback |

### 8.4 Path Parameters
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 8.4.1 | Single path param | `elisity topology get-site-v2 <site-id>` | Site data | Valid response |
| 8.4.2 | Multiple path params | Command with 2+ path params (if exists) | Correct URL construction | Valid response |
| 8.4.3 | Missing path param | `elisity topology get-site-v2` (no ID) | Click usage error | "Missing argument" |

### 8.5 Query Parameters
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 8.5.1 | Query param passed | Command with --page, --size options | Params in URL | Valid filtered response |

---

## Category 9: Error Handling & Safety

### 9.1 Authentication Errors
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 9.1.1 | Bad client ID | Set CCC_CLIENT_ID=invalid | Auth error message | Non-zero exit, error text |
| 9.1.2 | Bad secret | Set CCC_CLIENT_SECRET=invalid | Auth error message | Non-zero exit, error text |
| 9.1.3 | Bad base URL | Set CCC_BASE_URL=https://nonexistent.example.com | Connection error | Non-zero exit, error text |

### 9.2 Delete Safety
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 9.2.1 | Delete without --confirm | `elisity topology delete-site-v2 <id>` | Prompts for confirmation or rejects | Not executed silently |
| 9.2.2 | Delete with --confirm | `elisity topology delete-site-v2 <id> --confirm` | Executes delete | Successful |

### 9.3 Invalid Input
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 9.3.1 | Invalid format choice | `elisity -f xml topology get-all-sites` | Click error: invalid choice | Error message |
| 9.3.2 | Unknown command | `elisity topology nonexistent-cmd` | Click error: no such command | Error message |
| 9.3.3 | Unknown group | `elisity nonexistent-group` | Click error: no such command | Error message |

### 9.4 Debug Mode
| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 9.4.1 | Debug flag | `elisity --debug auth test` | Shows HTTP request details | Additional debug output |

---

## Category 10: Unit Test Suite

Run the full pytest suite (unit tests only, no live CCC required).

| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 10.1 | All unit tests pass | `pytest tests/ -m "not integration" -v` | All pass | 0 failures |
| 10.2 | Client auth tests | `pytest tests/test_client.py -v` | 12 tests pass | TestAuthentication + TestHTTPMethods + TestPagination + TestHealthCheck |
| 10.3 | Output formatter tests | `pytest tests/test_output.py -v` | 12 tests pass | TestOutputFormatters + TestJMESPath |
| 10.4 | CLI structure tests | `pytest tests/test_cli.py -v` | 23 tests pass | TestCLIStructure + TestCommandCounts + TestConfigCommands |
| 10.5 | Config tests | `pytest tests/test_config.py -v` | 5 tests pass | Config CRUD |

---

## Category 11: Integration Tests (Live CCC)

Run integration test suite against the live CCC.

| # | Test | Command | Expected | Verify |
|---|------|---------|----------|--------|
| 11.1 | All integration tests | `pytest tests/test_integration.py -v` | All pass | 0 failures |
| 11.2 | Auth integration | TestAuthIntegration (3 tests) | auth test, whoami, token | All pass |
| 11.3 | Topology integration | TestTopologyIntegration (5 tests) | sites, VEs, VENs | All pass |
| 11.4 | Policy integration | TestPolicyIntegration (3 tests) | policy sets, profiles, groups | All pass |
| 11.5 | Devices integration | TestDevicesIntegration (2 tests) | count, view | All pass |
| 11.6 | Connectors integration | TestConnectorsIntegration (1 test) | connector list | All pass |
| 11.7 | Flows integration | TestFlowsIntegration (1 test) | noise defs | All pass |
| 11.8 | Output formats integration | TestOutputFormats (4 tests) | JSON, table, YAML, CSV | All pass |

---

## Category 12: Cross-Cutting Concerns

| # | Test | Expected | Verify |
|---|------|----------|--------|
| 12.1 | No Python tracebacks in user output | All error paths show user-friendly messages | Manual review of error scenarios |
| 12.2 | Secrets never printed | Config show redacts secrets; no secrets in debug output | Manual review |
| 12.3 | Consistent exit codes | 0 = success, 1 = error across all commands | Spot check 10+ commands |
| 12.4 | All 434 generated commands loadable | `elisity <group> --help` works for all 8 groups | No import errors on startup |
| 12.5 | Command naming consistency | All commands use kebab-case | Visual inspection of --help |

---

## Execution Plan

**Phase 1 — Unit Tests (no CCC required)**
1. Run Category 10 (pytest unit suite)
2. Run Category 1 (installation, help, structure)
3. Run Category 9.3 (invalid input handling)

**Phase 2 — Live CCC Required**
1. Verify CCC is reachable: `elisity auth test`
2. Run Category 2 (authentication)
3. Run Category 3 (configuration)
4. Run Category 4 (output formats)
5. Run Category 5 (JMESPath)
6. Run Category 6 (all 8 command group reads)
7. Run Category 8 (NDJSON, pagination, body params)
8. Run Category 9.1-9.2 (auth errors, delete safety)

**Phase 3 — Destructive (careful)**
1. Run Category 7 (CRUD lifecycle) — creates and deletes test resources
2. Clean up any test resources left behind

**Phase 4 — Report**
1. Run Category 11 (full integration suite)
2. Compile Category 12 (cross-cutting review)
3. Produce final QA Report with pass/fail for every test

---

## QA Report Template

The final report will follow this structure:

```
# Elisity CLI — QA Report
Date: YYYY-MM-DD
Tester: Obiwan (automated) + Mike (review)
CCC Target: <your-ccc>.idp01.elisity.io

## Summary
- Total Tests: N
- Passed: N
- Failed: N
- Skipped: N
- Pass Rate: N%

## Results by Category
[Each category with pass/fail per test, actual output snippets for failures]

## Unit Test Results
[pytest output]

## Integration Test Results
[pytest output]

## Issues Found
[Any bugs, with severity and reproduction steps]

## Recommendation
[Ship / Fix-then-ship / Block]
```

---

## Prerequisites Checklist

- [ ] venv activated: `source .venv/bin/activate`
- [ ] Package installed: `pip install -e .`
- [ ] Profile configured: `~/.elisity/config.yaml` has `mike-lab`
- [ ] CCC reachable: `elisity auth test` returns healthy
- [ ] pytest and dependencies installed: `pip install pytest responses`
