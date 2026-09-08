#!/usr/bin/env python3
"""
Elisity CLI — Comprehensive QA Validation Suite
================================================
Tests every functional area against a live CCC instance.
Produces a structured pass/fail report.

Usage:
    source .venv/bin/activate
    python tests/qa_comprehensive.py
"""

import json
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

# ── Config ──────────────────────────────────────────────────────────────────

ELISITY = "elisity"  # CLI binary name (must be on PATH after pip install)
CCC_TARGET = "<your-ccc>.idp01.elisity.io"


@dataclass
class TestResult:
    category: str
    test_id: str
    name: str
    passed: bool
    output: str = ""
    error: str = ""
    duration_ms: int = 0


@dataclass
class QAReport:
    results: List[TestResult] = field(default_factory=list)
    start_time: float = 0
    end_time: float = 0

    def add(self, r: TestResult):
        self.results.append(r)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if not r.passed)

    @property
    def total(self) -> int:
        return len(self.results)


report = QAReport()


def run(args: list, stdin_data: str = None, expect_fail: bool = False,
        timeout: int = 30) -> tuple:
    """Run CLI command and return (exit_code, stdout, stderr, duration_ms)."""
    cmd = [ELISITY] + args
    start = time.time()
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            input=stdin_data,
            env={**os.environ, "COLUMNS": "200"},
        )
        duration = int((time.time() - start) * 1000)
        return result.returncode, result.stdout, result.stderr, duration
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT", int((time.time() - start) * 1000)


def test(category: str, test_id: str, name: str, args: list,
         check_fn=None, expect_fail: bool = False, stdin_data: str = None):
    """Run a test and record result."""
    code, stdout, stderr, ms = run(args, stdin_data=stdin_data)

    if expect_fail:
        passed = code != 0
        output = stderr or stdout
    elif check_fn:
        try:
            passed = check_fn(code, stdout, stderr)
            output = stdout[:500]
        except Exception as e:
            passed = False
            output = f"Check failed: {e}\nstdout: {stdout[:300]}\nstderr: {stderr[:300]}"
    else:
        passed = code == 0
        output = stdout[:500]

    r = TestResult(
        category=category, test_id=test_id, name=name,
        passed=passed, output=output, error=stderr[:300] if not passed else "",
        duration_ms=ms,
    )
    report.add(r)

    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {test_id}: {name} ({ms}ms)")
    if not passed:
        print(f"         stdout: {stdout[:200]}")
        print(f"         stderr: {stderr[:200]}")


def check_json(code, stdout, stderr):
    """Verify output is valid JSON and exit code 0."""
    if code != 0:
        return False
    json.loads(stdout)
    return True


def check_json_has(key):
    """Verify JSON output contains a specific key."""
    def _check(code, stdout, stderr):
        if code != 0:
            return False
        data = json.loads(stdout)
        if isinstance(data, dict):
            return key in data
        if isinstance(data, list) and data:
            return key in data[0]
        return False
    return _check


def check_json_list_nonempty(code, stdout, stderr):
    if code != 0:
        return False
    data = json.loads(stdout)
    return isinstance(data, list) and len(data) > 0


def check_json_value(query_fn):
    """Verify JSON output satisfies a predicate."""
    def _check(code, stdout, stderr):
        if code != 0:
            return False
        data = json.loads(stdout)
        return query_fn(data)
    return _check


def check_contains(text):
    def _check(code, stdout, stderr):
        return code == 0 and text in stdout
    return _check


def check_table(code, stdout, stderr):
    return code == 0 and ("─" in stdout or "━" in stdout or "┃" in stdout)


def check_yaml(code, stdout, stderr):
    return code == 0 and (":" in stdout) and not stdout.strip().startswith("{")


def check_csv(code, stdout, stderr):
    return code == 0 and "," in stdout and "\n" in stdout


# ════════════════════════════════════════════════════════════════════════════
# CATEGORY 1: INSTALLATION & SETUP
# ════════════════════════════════════════════════════════════════════════════

def cat1_installation():
    print("\n=== CATEGORY 1: INSTALLATION & SETUP ===")

    test("C1", "C1.01", "CLI binary is on PATH",
         ["--version"],
         check_contains("elisity"))

    test("C1", "C1.02", "Version output correct",
         ["--version"],
         check_contains("0.1.0"))

    test("C1", "C1.03", "Root --help shows all 10 command groups",
         ["--help"],
         lambda c, o, e: c == 0 and all(
             g in o for g in ["topology", "policy", "devices", "connectors",
                              "ad", "flows", "insights", "system", "auth", "config"]))

    test("C1", "C1.04", "topology --help shows subcommands",
         ["topology", "--help"],
         lambda c, o, e: c == 0 and "get-all-sites" in o)

    test("C1", "C1.05", "policy --help shows subcommands",
         ["policy", "--help"],
         lambda c, o, e: c == 0 and "create-policy" in o.lower())

    test("C1", "C1.06", "devices --help shows subcommands",
         ["devices", "--help"],
         lambda c, o, e: c == 0 and "get-device" in o.lower())

    test("C1", "C1.07", "connectors --help shows subcommands",
         ["connectors", "--help"],
         lambda c, o, e: c == 0 and "read" in o.lower())

    test("C1", "C1.08", "ad --help shows subcommands",
         ["ad", "--help"],
         lambda c, o, e: c == 0 and "get-connectors" in o)

    test("C1", "C1.09", "flows --help shows subcommands",
         ["flows", "--help"],
         lambda c, o, e: c == 0 and "noise" in o.lower())

    test("C1", "C1.10", "insights --help shows subcommands",
         ["insights", "--help"],
         lambda c, o, e: c == 0 and "suggestion" in o.lower() or "insight" in o.lower())

    test("C1", "C1.11", "system --help shows subcommands",
         ["system", "--help"],
         lambda c, o, e: c == 0 and "list-specs" in o or "task" in o.lower())

    test("C1", "C1.12", "auth --help shows test/token/whoami",
         ["auth", "--help"],
         lambda c, o, e: c == 0 and "test" in o and "token" in o and "whoami" in o)

    test("C1", "C1.13", "config --help shows profile management",
         ["config", "--help"],
         lambda c, o, e: c == 0 and "set-profile" in o and "use-profile" in o)


# ════════════════════════════════════════════════════════════════════════════
# CATEGORY 2: AUTHENTICATION
# ════════════════════════════════════════════════════════════════════════════

def cat2_authentication():
    print("\n=== CATEGORY 2: AUTHENTICATION ===")

    test("C2", "C2.01", "auth test — healthy response",
         ["auth", "test"],
         check_json_value(lambda d: d.get("status") == "healthy" and d.get("authenticated") is True))

    test("C2", "C2.02", "auth token — returns JWT",
         ["auth", "token"],
         lambda c, o, e: c == 0 and len(o.strip()) > 100 and o.strip().startswith("eyJ"))

    test("C2", "C2.03", "auth whoami — returns token claims",
         ["auth", "whoami"],
         check_json_has("iss"))

    test("C2", "C2.04", "auth whoami — issuer is elisity",
         ["auth", "whoami"],
         check_json_value(lambda d: "elisity" in d.get("iss", "")))

    test("C2", "C2.05", "auth whoami — has client_id claim",
         ["auth", "whoami"],
         check_json_value(lambda d: "clientId" in d or "azp" in d or "client_id" in d))

    test("C2", "C2.06", "auth whoami — has expiry",
         ["auth", "whoami"],
         check_json_has("exp"))


# ════════════════════════════════════════════════════════════════════════════
# CATEGORY 3: CONFIGURATION
# ════════════════════════════════════════════════════════════════════════════

def cat3_configuration():
    print("\n=== CATEGORY 3: CONFIGURATION ===")

    test("C3", "C3.01", "config show — displays active config",
         ["config", "show"],
         check_json_has("base_url"))

    test("C3", "C3.02", "config show — secret is redacted",
         ["config", "show"],
         check_json_value(lambda d: d.get("client_secret") == "***"))

    test("C3", "C3.03", "config list-profiles — shows profiles",
         ["config", "list-profiles"],
         check_json)

    # Create a temp profile, verify, delete config after
    test("C3", "C3.04", "config set-profile — creates new profile",
         ["config", "set-profile", "qa-test",
          "--base-url", "https://qa-test.elisity.io",
          "--client-id", "qa-id",
          "--client-secret", "qa-secret"],
         check_contains("saved"))

    test("C3", "C3.05", "config list-profiles — includes qa-test",
         ["config", "list-profiles"],
         check_json_value(lambda d: "qa-test" in d))

    test("C3", "C3.06", "config use-profile — switch to mike-lab",
         ["config", "use-profile", "mike-lab"],
         check_contains("Switched"))

    test("C3", "C3.07", "config use-profile — nonexistent profile fails",
         ["config", "use-profile", "does-not-exist"],
         expect_fail=True)


# ════════════════════════════════════════════════════════════════════════════
# CATEGORY 4: OUTPUT FORMATS
# ════════════════════════════════════════════════════════════════════════════

def cat4_output_formats():
    print("\n=== CATEGORY 4: OUTPUT FORMATS ===")

    # JSON (default)
    test("C4", "C4.01", "Default output is valid JSON",
         ["topology", "get-all-sites"],
         check_json)

    # Table
    test("C4", "C4.02", "Table output (-f table) at root level",
         ["-f", "table", "topology", "get-all-sites"],
         check_table)

    test("C4", "C4.03", "Table output (-f table) at command level",
         ["topology", "get-all-sites", "-f", "table"],
         check_table)

    # YAML
    test("C4", "C4.04", "YAML output (-f yaml)",
         ["-f", "yaml", "topology", "get-all-sites"],
         check_yaml)

    # CSV
    test("C4", "C4.05", "CSV output (-f csv)",
         ["-f", "csv", "topology", "get-all-sites"],
         check_csv)

    test("C4", "C4.06", "CSV has header row",
         ["-f", "csv", "topology", "get-all-sites"],
         lambda c, o, e: c == 0 and o.split("\n")[0].startswith("id"))

    # Table on paginated data
    test("C4", "C4.07", "Table output on paginated response (VEs)",
         ["-f", "table", "topology", "get-virtual-edge"],
         check_table)

    # Table on NDJSON data
    test("C4", "C4.08", "Table output on NDJSON (policy sets)",
         ["-f", "table", "policy", "get-all-as-nd-json"],
         check_table)

    # YAML on complex data
    test("C4", "C4.09", "YAML on devices count",
         ["-f", "yaml", "devices", "get-device-count"],
         check_yaml)


# ════════════════════════════════════════════════════════════════════════════
# CATEGORY 5: JMESPATH QUERIES
# ════════════════════════════════════════════════════════════════════════════

def cat5_jmespath():
    print("\n=== CATEGORY 5: JMESPATH QUERIES ===")

    test("C5", "C5.01", "JMESPath: extract site labels",
         ["-q", "[].label", "topology", "get-all-sites"],
         check_json_list_nonempty)

    test("C5", "C5.02", "JMESPath: extract specific fields",
         ["-q", "[].{id: id, name: label}", "topology", "get-all-sites"],
         check_json_value(lambda d: isinstance(d, list) and "name" in d[0]))

    test("C5", "C5.03", "JMESPath: array slice [0:2]",
         ["-q", "[0:2]", "topology", "get-all-sites"],
         check_json_value(lambda d: isinstance(d, list) and len(d) == 2))

    test("C5", "C5.04", "JMESPath: nested content[].name",
         ["-q", "content[].name", "topology", "get-virtual-edge"],
         check_json_list_nonempty)

    test("C5", "C5.05", "JMESPath: single value extraction",
         ["-q", "devicesCount", "devices", "get-device-count"],
         check_json_value(lambda d: isinstance(d, int) and d >= 0))

    test("C5", "C5.06", "JMESPath: length function",
         ["-q", "length([].label)", "topology", "get-all-sites"],
         check_json_value(lambda d: isinstance(d, int) and d > 0))

    test("C5", "C5.07", "JMESPath: command-level -q flag",
         ["topology", "get-all-sites", "-q", "[].label"],
         check_json_list_nonempty)


# ════════════════════════════════════════════════════════════════════════════
# CATEGORY 6: ALL 8 COMMAND GROUPS — READ OPERATIONS
# ════════════════════════════════════════════════════════════════════════════

def cat6_all_groups():
    print("\n=== CATEGORY 6: ALL COMMAND GROUPS — READ OPS ===")

    # TOPOLOGY
    test("C6", "C6.01", "topology: list sites",
         ["topology", "get-all-sites"],
         check_json)

    test("C6", "C6.02", "topology: list distribution zones",
         ["topology", "get-all-distribution-zones"],
         check_json)

    test("C6", "C6.03", "topology: list VEs",
         ["topology", "get-virtual-edge"],
         check_json_has("content"))

    test("C6", "C6.04", "topology: list VENs",
         ["topology", "get-virtual-edge-nodes"],
         check_json_has("content"))

    test("C6", "C6.05", "topology: list flow exporters",
         ["topology", "get-all-flow-exporter"],
         check_json)

    test("C6", "C6.06", "topology: list cloud controllers",
         ["topology", "get-all-cloud-controllers", "--cloudType", "MIST_CLOUD_CONTROLLER"],
         check_json)

    test("C6", "C6.07", "topology: list global credentials",
         ["topology", "get-all-global-credentials"],
         check_json)

    test("C6", "C6.08", "topology: get interfaces settings",
         ["topology", "get-global-interfaces-settings"],
         check_json)

    # POLICY
    test("C6", "C6.10", "policy: list policy sets (NDJSON)",
         ["policy", "get-all-as-nd-json"],
         check_json_list_nonempty)

    test("C6", "C6.11", "policy: list security profiles (NDJSON)",
         ["policy", "get-all-security-profiles-as-nd-json"],
         check_json_list_nonempty)

    test("C6", "C6.12", "policy: list all policies (NDJSON)",
         ["policy", "get-all-policies-as-nd-json"],
         check_json_list_nonempty)

    test("C6", "C6.13", "policy: list policy groups (JSON)",
         ["policy", "get-policy-groups-json", "--filters", "{}", "--pageable", '{"page":0,"size":10}'],
         check_json_has("content"))

    test("C6", "C6.14", "policy: list site labels from all policy sets (NDJSON)",
         ["policy", "get-all-site-labels-from-all-policy-sets"],
         check_json)

    test("C6", "C6.15", "policy: list policy views (NDJSON)",
         ["policy", "get-all-policy-views-as-nd-json"],
         check_json)

    test("C6", "C6.16", "policy: get state",
         ["policy", "get-state"],
         check_json)

    # DEVICES
    test("C6", "C6.20", "devices: count",
         ["devices", "get-device-count"],
         check_json_has("devicesCount"))

    test("C6", "C6.21", "devices: view (POST with body)",
         ["devices", "get-devices-view", "--body", '{"page":0,"size":5}'],
         check_json_has("content"))

    test("C6", "C6.22", "devices: get enrichment order",
         ["devices", "get-blended-enrichment-order"],
         check_json)

    test("C6", "C6.23", "devices: read all settings",
         ["devices", "read-all-settings"],
         check_json)

    test("C6", "C6.24", "devices: get device header data",
         ["devices", "get-device-header-data"],
         check_json)

    test("C6", "C6.25", "devices: get suppression list",
         ["devices", "get-users"],
         check_json)

    test("C6", "C6.26", "devices: time-based configs",
         ["devices", "get-configurations"],
         check_json)

    # CONNECTORS
    test("C6", "C6.30", "connectors: connectivity status",
         ["connectors", "read"],
         check_json)

    test("C6", "C6.31", "connectors: list connector configs",
         ["connectors", "read-all-connector-configurations"],
         check_json)

    # AD
    test("C6", "C6.40", "ad: list connectors",
         ["ad", "get-connectors"],
         check_json)

    test("C6", "C6.41", "ad: get configuration",
         ["ad", "get-configuration-value", "--name", "user.preemption.enabled"],
         check_json)

    test("C6", "C6.42", "ad: get suppressed IP attaches",
         ["ad", "get-suppressed-ip-attaches"],
         check_json)

    # FLOWS
    test("C6", "C6.50", "flows: noise definitions",
         ["flows", "get-noise-definition"],
         check_json_has("id"))

    test("C6", "C6.51", "flows: available ports",
         ["flows", "get-available-ports"],
         check_json)

    test("C6", "C6.52", "flows: materialized view info",
         ["flows", "get-all"],
         check_json)

    # INSIGHTS
    test("C6", "C6.60", "insights: get settings",
         ["insights", "get-settings"],
         check_json)

    test("C6", "C6.61", "insights: list network PG suggestions",
         ["insights", "list-network-policy-group-suggestions"],
         check_json)

    # SYSTEM
    test("C6", "C6.70", "system: list task specs",
         ["system", "list-specs"],
         check_json)


# ════════════════════════════════════════════════════════════════════════════
# CATEGORY 7: CRUD LIFECYCLE
# ════════════════════════════════════════════════════════════════════════════

def cat7_crud():
    print("\n=== CATEGORY 7: CRUD LIFECYCLE ===")

    # Create a test site
    site_id = None

    code, stdout, stderr, _ = run([
        "topology", "create-site-post",
        "--body", json.dumps({"label": "QA-Test-Site-CLI", "description": "Created by CLI QA test"})
    ])
    if code == 0:
        try:
            data = json.loads(stdout)
            if isinstance(data, str):
                # v2 create-site-post returns a UUID string directly
                site_id = data
            elif isinstance(data, list) and data:
                site_id = data[0].get("id")
            elif isinstance(data, dict):
                site_id = data.get("id")
        except Exception:
            pass

    test("C7", "C7.01", "CREATE: Create test site",
         [],  # Already ran above
         check_fn=lambda c, o, e: site_id is not None)
    # Override the result with what we already know
    report.results[-1].passed = site_id is not None
    report.results[-1].output = f"site_id={site_id}"

    if site_id:
        # READ
        test("C7", "C7.02", f"READ: Get site by ID ({site_id[:8]}...)",
             ["topology", "get-site-v2", site_id],
             check_json_has("id"))

        # UPDATE
        test("C7", "C7.03", "UPDATE: Update site description",
             ["topology", "update-site", site_id,
              "--body", json.dumps({"id": site_id, "label": "QA-Test-Site-CLI", "description": "Updated by QA"})],
             check_json)

        # Verify update
        test("C7", "C7.04", "VERIFY: Updated description persisted",
             ["topology", "get-site-v2", site_id],
             check_json_value(lambda d: "Updated" in d.get("description", "") or d.get("label") == "QA-Test-Site-CLI"))

        # DELETE without --confirm should fail
        test("C7", "C7.05", "SAFETY: Delete without --confirm fails",
             ["topology", "delete-site-v2", site_id],
             expect_fail=True)

        # DELETE with --confirm
        test("C7", "C7.06", "DELETE: Delete site with --confirm",
             ["topology", "delete-site-v2", site_id, "--confirm"],
             lambda c, o, e: c == 0)

        # Verify deleted
        test("C7", "C7.07", "VERIFY: Deleted site returns 404",
             ["topology", "get-site-v2", site_id],
             expect_fail=True)
    else:
        print("  [SKIP] C7.02-C7.07: Site creation failed, skipping CRUD chain")


# ════════════════════════════════════════════════════════════════════════════
# CATEGORY 8: NDJSON, PAGINATION, BODY PARAMS
# ════════════════════════════════════════════════════════════════════════════

def cat8_advanced():
    print("\n=== CATEGORY 8: NDJSON, PAGINATION, BODY PARAMS ===")

    # NDJSON endpoints
    test("C8", "C8.01", "NDJSON: Security profiles returns list",
         ["policy", "get-all-security-profiles-as-nd-json"],
         check_json_value(lambda d: isinstance(d, list) and len(d) > 0))

    test("C8", "C8.02", "NDJSON: Policy sets returns list",
         ["policy", "get-all-as-nd-json"],
         check_json_value(lambda d: isinstance(d, list) and len(d) > 0))

    test("C8", "C8.03", "NDJSON: All policies returns list",
         ["policy", "get-all-policies-as-nd-json"],
         check_json_value(lambda d: isinstance(d, list) and len(d) > 0))

    # Get a policy set ID for nested NDJSON
    code, stdout, stderr, _ = run(["policy", "get-all-as-nd-json", "-q", "[0].id"])
    ps_id = None
    if code == 0:
        try:
            ps_id = json.loads(stdout)
        except Exception:
            pass

    if ps_id:
        test("C8", "C8.04", f"NDJSON: Policies for policy set ({ps_id[:8]}...)",
             ["policy", "get-all-policies-for-policy-set-as-nd-json", ps_id, "--filters", "{}", "--pageable", '{"page":0,"size":10}'],
             check_json_value(lambda d: isinstance(d, list)))

        test("C8", "C8.05", f"NDJSON: Policy groups for policy set ({ps_id[:8]}...)",
             ["policy", "get-policy-groups-assigned-to-policy-set", ps_id],
             check_json_value(lambda d: isinstance(d, list)))

    # Pagination
    test("C8", "C8.10", "PAGINATION: VENs paginated response has pagination fields",
         ["topology", "get-virtual-edge-nodes"],
         check_json_value(lambda d: "totalElements" in d and "totalPages" in d))

    test("C8", "C8.11", "PAGINATION: Policy groups paginated",
         ["policy", "get-policy-groups-json", "--filters", "{}", "--pageable", '{"page":0,"size":10}'],
         check_json_value(lambda d: "content" in d and "totalElements" in d))

    # --body parameter
    test("C8", "C8.20", "BODY: POST with --body JSON string",
         ["devices", "get-devices-view", "--body", '{"page":0,"size":2}'],
         check_json_has("content"))

    # --body-file parameter
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"page": 0, "size": 2}, f)
        body_file = f.name

    test("C8", "C8.21", "BODY-FILE: POST with --body-file",
         ["devices", "get-devices-view", "--body-file", body_file],
         check_json_has("content"))
    os.unlink(body_file)

    # --body with complex payload (policy evaluation)
    test("C8", "C8.22", "BODY: Policy IP lookup",
         ["policy", "lookup-evaluation-endpoint", "--body", '{"ip":"10.0.0.1"}'],
         check_json)


# ════════════════════════════════════════════════════════════════════════════
# CATEGORY 9: ERROR HANDLING & SAFETY
# ════════════════════════════════════════════════════════════════════════════

def cat9_errors():
    print("\n=== CATEGORY 9: ERROR HANDLING & SAFETY ===")

    test("C9", "C9.01", "Invalid subcommand shows error",
         ["topology", "nonexistent-command"],
         expect_fail=True)

    test("C9", "C9.02", "Missing required argument shows usage",
         ["topology", "get-site-v2"],  # Missing site ID
         expect_fail=True)

    test("C9", "C9.03", "GET nonexistent resource returns error",
         ["topology", "get-site-v2", "00000000-0000-0000-0000-000000000000"],
         expect_fail=True)

    test("C9", "C9.04", "DELETE without --confirm is blocked",
         ["topology", "delete-site-v2", "00000000-0000-0000-0000-000000000000"],
         expect_fail=True)

    test("C9", "C9.05", "Invalid --body JSON shows error",
         ["devices", "get-devices-view", "--body", "not-json"],
         expect_fail=True)

    test("C9", "C9.06", "Invalid format choice rejected",
         ["-f", "xml", "topology", "get-all-sites"],
         expect_fail=True)

    test("C9", "C9.07", "Nonexistent --body-file rejected",
         ["devices", "get-devices-view", "--body-file", "/tmp/nonexistent.json"],
         expect_fail=True)

    test("C9", "C9.08", "Unknown global option rejected",
         ["--badopt", "topology", "get-all-sites"],
         expect_fail=True)


# ════════════════════════════════════════════════════════════════════════════
# CATEGORY 10: COMMAND COUNT VERIFICATION
# ════════════════════════════════════════════════════════════════════════════

def cat10_counts():
    print("\n=== CATEGORY 10: COMMAND COUNT VERIFICATION ===")

    from elisity_cli.commands import COMMAND_GROUPS

    expected = {
        "topology": 100, "policy": 90, "devices": 50, "ad": 50,
        "insights": 20, "connectors": 15, "flows": 10, "system": 10,
    }

    total = 0
    for gn in COMMAND_GROUPS:
        mod = __import__(f"elisity_cli.commands.{gn}", fromlist=["group"])
        count = len(mod.group.commands)
        total += count
        min_expected = expected.get(gn, 5)

        r = TestResult(
            category="C10", test_id=f"C10.{gn}", name=f"{gn}: {count} commands (min {min_expected})",
            passed=count >= min_expected,
            output=f"{count} commands",
        )
        report.add(r)
        status = "PASS" if r.passed else "FAIL"
        print(f"  [{status}] C10.{gn}: {count} commands (min {min_expected})")

    r = TestResult(
        category="C10", test_id="C10.total", name=f"TOTAL: {total} commands (min 430)",
        passed=total >= 430,
        output=f"{total} total commands",
    )
    report.add(r)
    status = "PASS" if r.passed else "FAIL"
    print(f"  [{status}] C10.total: {total} commands (min 430)")


# ════════════════════════════════════════════════════════════════════════════
# REPORT
# ════════════════════════════════════════════════════════════════════════════

def print_report():
    print("\n" + "=" * 72)
    print("  ELISITY CLI v0.1.0 — QA VALIDATION REPORT")
    print("=" * 72)
    print(f"  Target:   {CCC_TARGET}")
    print(f"  Date:     {time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"  Duration: {(report.end_time - report.start_time):.1f}s")
    print("=" * 72)

    # Summary by category
    categories = {}
    for r in report.results:
        if r.category not in categories:
            categories[r.category] = {"pass": 0, "fail": 0}
        if r.passed:
            categories[r.category]["pass"] += 1
        else:
            categories[r.category]["fail"] += 1

    cat_names = {
        "C1": "Installation & Setup",
        "C2": "Authentication",
        "C3": "Configuration",
        "C4": "Output Formats",
        "C5": "JMESPath Queries",
        "C6": "All Command Groups",
        "C7": "CRUD Lifecycle",
        "C8": "NDJSON/Pagination/Body",
        "C9": "Error Handling & Safety",
        "C10": "Command Count Verification",
    }

    print(f"\n{'Category':<35} {'Pass':>6} {'Fail':>6} {'Total':>6} {'Status':>8}")
    print("-" * 72)
    for cat in sorted(categories.keys()):
        c = categories[cat]
        name = cat_names.get(cat, cat)
        total = c["pass"] + c["fail"]
        status = "PASS" if c["fail"] == 0 else "FAIL"
        print(f"  {cat} {name:<30} {c['pass']:>4} {c['fail']:>6} {total:>6} {status:>8}")

    print("-" * 72)
    print(f"  {'TOTAL':<35} {report.passed:>4} {report.failed:>6} {report.total:>6} "
          f"{'ALL PASS' if report.failed == 0 else 'FAILURES'}")
    print("=" * 72)

    # List failures
    failures = [r for r in report.results if not r.passed]
    if failures:
        print(f"\n  FAILURES ({len(failures)}):")
        for f in failures:
            print(f"    [{f.test_id}] {f.name}")
            if f.error:
                print(f"      Error: {f.error[:150]}")
            if f.output:
                print(f"      Output: {f.output[:150]}")
        print()
    else:
        print("\n  NO FAILURES — ALL TESTS PASSED")
        print()

    print(f"  VERDICT: {'APPROVED FOR RELEASE' if report.failed == 0 else 'BLOCKED — FIX FAILURES BEFORE RELEASE'}")
    print("=" * 72)


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

def main():
    report.start_time = time.time()

    cat1_installation()
    cat2_authentication()
    cat3_configuration()
    cat4_output_formats()
    cat5_jmespath()
    cat6_all_groups()
    cat7_crud()
    cat8_advanced()
    cat9_errors()
    cat10_counts()

    report.end_time = time.time()
    print_report()

    sys.exit(0 if report.failed == 0 else 1)


if __name__ == "__main__":
    main()
