# AI Agent Operating Guide for elisity-cli

This document is the operating contract for AI agents (Claude, ChatGPT, copilots,
custom orchestrators) running `elisity-cli` on a human's behalf. It is *not* a
generic CLI tutorial — for that, read [user-guide.md](user-guide.md) first. This
guide assumes you already know how to authenticate and how to read JSON.

The job here is precise: when a human says "give me the Zero Trust score" or
"list our VENs in monitor mode", you (the agent) translate that to the *exact*
CLI command that runs against the live tenant — without guessing, without
inventing flags, and without paraphrasing UI terminology into the wrong API
verb.

The CLI ships with the answers. Use them.

---

## Core operating principle

**When a human term is ambiguous, ask the CLI before you ask the human.**

```bash
elisity glossary search "<phrase>"     # JSON — full mapping entry
elisity glossary explain "<phrase>"    # Prose — ready-to-paste commands
```

If `glossary explain` returns recipes, you have a verified mapping. Use it.
If it returns "no direct CLI surface for this term — terminology only",
clarify scope with the human before running anything API-side.

If `glossary search` errors with `No glossary term matched`, the phrase is
not a known synonym. Either pick a closer phrasing, or fall back to
`elisity <best-guess-group> --help` to inspect the surface — *then* report
to the human what you found, instead of running a destructive command on
a hunch.

---

## When humans say X, run Y

The 26 most common UI-term → CLI mappings. This is a flat lookup table for
copy-paste. For the long-form rationale, run `elisity glossary explain "<term>"`
or read [glossary.md](glossary.md).

| Human says | Canonical | Run |
|---|---|---|
| "monitor mode policies" / "simulation policies" | Simulation | `elisity reporting get-policy-count --monitor-mode MONITOR_ONLY` |
| "active policies" / "enforce mode" | Active | `elisity reporting get-policy-count --monitor-mode MONITOR_AND_ENFORCE` |
| "external monitoring" / "independent control" | Independent Control | `elisity reporting get-policy-count --monitor-mode MONITOR_EXTERNAL` |
| "list all policy groups" / "list segments" | Policy Group | `elisity policy get-policy-groups-json` |
| "show me policy group X" | Policy Group | `elisity policy get-policy-group-by-id <PG_ID>` |
| "what devices are in PG X" | Policy Group | `elisity policy get-policy-group-devices <PG_ID>` |
| "list ACLs" / "list firewall rules" | Security Profile | `elisity policy get-all-security-profiles-as-nd-json` |
| "show the policy matrix" | Policy Matrix | `elisity policy get-matrix` |
| "Zero Trust score" / "posture score" / "compliance score" | Policy Enforcement Score | `elisity reporting get-aggregate-enforcement-score` |
| "Zero Trust score for site X" | Policy Enforcement Score | `elisity reporting get-site-kpis --site <SITE>` (CCC 26.7 removed the per-policy-set score) |
| "per-PG Zero Trust breakdown" | Policy Enforcement Score | `elisity reporting get-zero-trust-metrics` |
| "why is the score low" / "what should I fix to improve the score" | Policy Enforcement Score | `elisity reporting get-zero-trust-metrics` then `elisity policy search-policies-for-policy-set` — see [Diagnosing a low/zero Zero Trust score](#diagnosing-a-lowzero-zero-trust-score-do-not-guess-the-cause) |
| "list our VENs" / "list switches" | Virtual Edge Node | `elisity topology get-virtual-edge-nodes` |
| "VEN inventory by model" | Virtual Edge Node | `elisity reporting get-virtual-edge-nodes-count` |
| "list Virtual Edges" | Virtual Edge | `elisity reporting get-virtual-edges-count` |
| "list distribution zones" / "list VLAN zones" | Distribution Zone | `elisity topology get-all-distribution-zones` |
| "list sites" | (Site — not glossary) | `elisity topology get-all-sites` |
| "per-site KPIs" / "site dashboard" | Policy Enforcement Score | `elisity -f table reporting get-site-kpis` |
| "device inventory" / "show the CMDB" | IdentityGraph | `elisity devices get-devices-view --body '{"pageable":{"page":0,"size":50}}'` |
| "online device count" | IdentityGraph | `elisity reporting get-device-count --online true` |
| "devices by connector" | IdentityGraph | `elisity reporting get-devices-by-connector` |
| "list Insights suggestions" / "AI recommendations" | Insights | `elisity insights get-suggestions` |
| "pending adjudications" / "things to approve" | Adjudication | ``elisity insights get-suggestions -q '[?status==`PENDING`]'`` |
| "top talkers" / "traffic analytics dashboard" | Traffic Analytics | `elisity flows get-dash-board-summary-data` |
| "top denied IPs" | Traffic Analytics | `elisity reporting get-top-ips-by-traffic --kind DENIED --top 10` |
| "what's in the Unassigned PG" | Unassigned (Policy Group) | ``elisity policy get-policy-groups-json -q '[?name==`Unassigned`]'`` then `get-policy-group-devices <ID>` |

If a row in the table above resolves to a destructive or state-changing operation,
**do not run it without explicit human approval** — see [Destructive operations](#destructive-operations) below.

---

## Using `elisity glossary` for runtime lookup

The `glossary` group is your disambiguation surface. Three subcommands, all
read-only, all data-local (no API call needed).

### `elisity glossary list`

Returns the 29 canonical terms with their domain and (where applicable) enum
value. Use this to confirm a domain mapping when you're unsure which API group
backs a UI feature.

```bash
elisity glossary list
elisity -f table glossary list           # human-readable table
elisity -q "[?domain==\`policy\`]" glossary list   # just policy-domain terms
```

### `elisity glossary search "<phrase>"`

Looks up the full mapping entry for any synonym. Output is JSON by default —
easy to feed back into your own prompt context.

```bash
elisity glossary search "monitor mode"
elisity glossary search "Zero Trust score"
elisity glossary search VEN
elisity glossary search "audit mode"     # also resolves to Simulation
```

If no synonym matches, the command exits with status 1 and writes the failure
to stderr. Trap the exit code in agentic shells:

```bash
if ! elisity glossary search "$phrase" > /tmp/match.json 2>/dev/null; then
  echo "Unknown term — falling back to <group> --help" >&2
fi
```

### `elisity glossary explain "<phrase>"`

This is the agent-optimised path. Plain text output, no JSON parsing required,
includes inline command recipes ready to copy:

```bash
$ elisity glossary explain "Zero Trust score"
Term: Policy Enforcement Score
Domain: reporting
Also called: security score, risk score, ...

Context:
  0-100 metric for policy coverage quality. ...

CLI recipes:

  # Get the tenant-wide Zero Trust / Policy Enforcement Score headline number
  elisity reporting get-aggregate-enforcement-score
  # Returns the single FloatMetricValue the CCC dashboard tile shows. ...
```

Use `explain` when you need to *report back* to the human ("the CLI command for
that is …"), and `search` when you need structured data to act on.

---

## Default workflow for unknown terms

When a human asks for something using a phrase you don't immediately recognise:

1. **Try `elisity glossary search "<phrase>"`.** If a match returns, the
   mapping entry tells you the canonical term, the domain, and at least one
   verified CLI command. Run that command.

2. **If no glossary match**, ask `elisity <best-guess-group> --help` to list
   commands in the most likely group. Match by name; do not invent commands.

3. **If still ambiguous**, return to the human with the candidate canonical
   terms you considered, the command you intend to run, and a yes/no question.
   Do not act on a guess for non-trivial operations.

4. **Never paraphrase a UI feature into a plausible-but-fake CLI command.**
   The CLI has 525 commands; if a verb you imagine isn't in `--help`, it
   doesn't exist. The honesty rule is non-negotiable — fabricated commands
   waste human review cycles and damage trust.

---

## Diagnosing a low/zero Zero Trust score (do not guess the cause)

This is the single most common reasoning error agents make on this CLI, so it
gets its own section. When a human asks "which devices have the worst Zero Trust
score and what should I fix?", the trap is to read a 0% score off
`get-zero-trust-metrics` and conclude "the policies are in simulation —
activate them." **A 0% coverage score does not tell you the cause.** It has
three distinct root causes with *opposite* fixes:

| Cause | What you'd see | Correct fix |
|---|---|---|
| **No policy** | the group has no policy at all | *create* a policy / check Insights suggestions / reclassify the devices — there is nothing to activate |
| **Simulation only** | policies exist, all `MONITOR_ONLY` | activate them: `policy update-policy` with `monitorMode` set to `MONITOR_AND_ENFORCE` |
| **Active but uncovered** | policies are already `MONITOR_AND_ENFORCE`, score still low | the group's real traffic isn't covered — reclassify catch-all devices / add rules for the uncovered flows |

Recommending activation for a *no-policy* group, or for a group
whose policies are *already active*, is a fabricated remediation — it names a
fix that does nothing. That violates the honesty rule.

**Do not infer the cause from the score. Read the group's actual policy status.**
That is two steps:

```bash
# 1. The low scorers, with the policyGroupId you need for step 2.
elisity -f table \
  -q '[].{site: siteName, pg: policyGroupName, pgId: policyGroupId, devices: deviceCount, devCov: policyDeploymentMetrics.deviceCoverage}' \
  reporting get-zero-trust-metrics

# 2. The policies that reference that group, and what mode they are in.
#    This is the cause. Substitute the pgId from step 1.
#    Policies live in policy sets: repeat per POLICY_SET_ID
#    (elisity policy get-all-as-nd-json -q '[].id').
#    CCC filters by group, once as source and once as destination.
elisity -f json policy search-policies-for-policy-set <POLICY_SET_ID> \
  --body '{"srcPolicyGroupIds":["PG_ID"],"size":250}' \
  -q '{total: totalElements, last: last, policies: content[].{name: name, mode: monitorMode, status: status}}'
elisity -f json policy search-policies-for-policy-set <POLICY_SET_ID> \
  --body '{"dstPolicyGroupIds":["PG_ID"],"size":250}' \
  -q '{total: totalElements, last: last, policies: content[].{name: name, mode: monitorMode, status: status}}'
#    Each answer is one page. `total` counts every matching policy; while
#    `last` is false, repeat the call with "page":1, 2, ... in the body.
```

Read step 2 like this — the mapping is mechanical, so do not editorialise.
Classify only after both calls, every page and every policy set:

| What step 2 returns | Cause | What to propose |
|---|---|---|
| `total` 0 in every call | **no policy** | create a policy, check `insights get-policy-suggestion-list`, or reclassify the devices. Do **not** propose activation — there is nothing to activate |
| all policies `MONITOR_ONLY` | **simulation only** | review the simulated traffic, then activate the policies with `policy update-policy` |
| all policies `MONITOR_EXTERNAL` | **independent control** | enforcement is delegated to another system; low coverage is by design. Confirm before changing |
| any policy `MONITOR_AND_ENFORCE` | **active but uncovered** | policies are already active — activating anything else will not move the score. Reclassify catch-all devices / add rules for the uncovered flows |

Only when step 2 shows `MONITOR_ONLY` policies should you propose activating
them. `policy update-policy <POLICY_SET_ID> <POLICY_ID>` takes the policy as
JSON: read its current fields first
(`policy get-policy-by-id <POLICY_ID>`), change
only `monitorMode` to `MONITOR_AND_ENFORCE`, and send the rest back unchanged.
Activation changes enforcement on a live tenant, so it still needs explicit
human approval (see [Destructive operations](#destructive-operations)).

> **Removed in CCC 26.7: `reporting diagnose-low-score`.** Use the two steps
> above instead; they do the same diagnosis.

---

## Common pitfalls

These bite new users and agents both. Skim this section once; the failure
modes are non-obvious.

### Pagination wrapper

POST search endpoints require the pageable wrapper. A flat body is silently ignored:

```bash
# WRONG — silently returns the unpaginated default
elisity devices get-devices-view --body '{"page":0,"size":10}'

# RIGHT — body is wrapped in `pageable`
elisity devices get-devices-view --body '{"pageable":{"page":0,"size":10}}'
```

GET search endpoints (e.g. `ad get-entra-users`) use `--page` and `--size` flags
directly. See [user-guide.md](user-guide.md) for the full breakdown.

### `--body` not `--data`

The flag for JSON request bodies is `--body` (or `--body-file <path>`). Older
help text shows `--data` — that's stale; the CLI rejects it.

### `--confirm` required for destructive commands

Every command the CLI classifies as destructive requires `--confirm` on the
command line. Without it, the CLI refuses to send the request — it prints
`Use --confirm to execute this destructive operation.` and exits 1, having made
no HTTP call. Do not work around this; it is intentional friction.

The classification is made from the API path, not the HTTP verb and not the
command name:

- **every** `DELETE` — 40 commands, all gated;
- **plus** any verb whose path names a destructive action — a `delete`,
  `force-delete`, `force`, `purge`, `decommission`, `reset-to-default` or
  `recreate` segment, among others. That is 6 more commands: one PUT
  (`topology decommission-virtual-edge-node`) and the Insights reset/recreate
  commands, whose `--help` describes each as "Delete and Create all …
  suggestions".
- Two commands whose paths name no action but which reset or delete state:
  `ad set-groups-default-enabled` (CCC 26.9), which CCC describes as a reset of
  the "enable all groups by default" setting, and `ad update-entra-instance`
  (CCC 26.10), because a new `tenantId` on an instance deletes its data.

That makes 48 destructive commands, and every one of them requires `--confirm`.

**Do not read `--confirm` as the whole safety story.** State-changing is
broader than destructive: `create-*`, `update-*`, `change-active-ve`,
`enable-maintenance` and everything else in the
[Destructive operations](#destructive-operations) P0 list changes live tenant
state and takes **no** `--confirm`. The absence of the flag is not permission
to run them unattended — the human-approval rule below is what governs those.

### Global flags go BEFORE the group

`-f`, `-q`, `--debug`, and `-p` are options on the root `elisity` command.
Placed *before* the group name, they work with every command:

```bash
elisity -f table topology get-all-sites
elisity -q '[].label' topology get-all-sites
elisity -f table reporting get-site-kpis
```

Commands in the API groups (`ad`, `connectors`, `devices`, `flows`, `insights`,
`policy`, `system`, `topology`) also accept `-f` and `-q` *after* the command
name, although `--help` does not list them. `reporting`, `glossary`, `auth` and
`config` commands do not, and `--debug` and `-p` only work before the group:

```bash
# Works — topology commands accept -f/-q after the command name
elisity topology get-all-sites -f table

# WRONG — reporting commands don't; this exits 2 with "No such option"
elisity reporting get-site-kpis -f table

# WRONG — nothing accepts -f between the group and the command
elisity topology -f table get-all-sites
```

Putting them before the group always works, so make that your default.

### `label` vs `name` on sites

The v1 sites endpoint exposes `label`, not `name`. JMESPath like `[].name`
returns an empty list — use `[].label`:

```bash
elisity topology get-all-sites -q '[].label'
```

### Snapshot times for reporting

The reporting commands (the CCC reporting (GraphQL) API) operate on top-of-hour
UTC snapshots. Not every hour has data. Default is the previous full hour. Use
`elisity reporting list-snapshots` to find available snapshots before passing a
custom `--snapshot`.

### Stream endpoints are ndjson, not JSON arrays

`elisity policy get-all-as-nd-json` and friends stream newline-delimited JSON.
The CLI parses them transparently into a JSON array on output — `-q '[?…]'` works.
Do not pipe the raw bytes into `jq` expecting a JSON document; pipe the CLI's
parsed output, or use the CLI's own `-q` filter.

---

## Destructive operations

The following verbs change live tenant state. Treat each as a P0 confirmation
gate: report the exact command to the human, get explicit go/no-go, then run.

- `delete-*`, `bulk-*` (create/delete/move/update), `decommission-*`,
  `force-delete-*` — every one of these that actually destroys something also
  requires `--confirm`, including `topology decommission-virtual-edge-node`.
  `bulk-*` commands that create, move or update do not take `--confirm` — they
  still need human approval
- `create-*`, `update-*`, `patch-*`, `replace-*`, `overwrite-*`, `rename-*`
- `add-*`, `remove-*`, `move-*`, `reorder-*` — including
  `add-definition` / `remove-definition` on custom applications, and
  `move-policy-group-scope`
- `change-active-ve`, `change-ven-group`, `change-virtual-edge-group`
- `enable-*` / `disable-*` — policy groups, and VE/VEN **maintenance mode**
  (`enable-maintenance`, `enable-maintenance-for-group`, and their `disable-`
  counterparts) — maintenance mode changes enforcement behaviour on live
  infrastructure
- `set-*` — `set-distribution-zones`, and the CCC 26.9 AD group toggles
  `ad set-groups-enabled` and `ad set-groups-default-enabled` (the latter
  resets the "enable all groups by default" setting and requires `--confirm`)
- `execute-activate-workflow`, `recreate-policy-suggestions`,
  `reset-suggestions-to-default` — the recreate/reset pair discards the existing
  suggestion set ("Delete and Create all suggestions"), so both require
  `--confirm` as well
- `import-*` / `cancel-import`, `upload-*` (bulk VE/VEN JSON)
- `sync-*`, `refresh-*`, `resync`, `re-initialize-*`,
  `discover-ec2workloads` — these trigger real work against live infrastructure
  even though they create nothing directly
- `restart` (restarts an AD connector), `pull-logs`
- `pause-snapshot-schedule`, `resume-snapshot-schedule`
- `generate-external-id` — mints and persists an AWS external ID / account ID
- `create-access-policy-review`, `create-policy-review` — write an audit-trail
  record ("configuration review completed"); the policy itself is not modified

A safe rule of thumb: if a command in the glossary mapping starts with anything
other than `get-`, `list-`, `read-`, `search-`, `count-`, or `export-`, get
human approval before running.

### POST commands that are read-only

The rule of thumb above is deliberately strict, and it will flag a handful of
commands that only read. CCC uses `POST` for queries whose filter payload is too
large for a query string, so the HTTP verb is not a reliable signal on its own.
These are safe to run without approval — each only reads:

| Command | What it does |
|---------|--------------|
| `devices devices-view` | Query devices with CSearch filters |
| `devices devices-aggregate` | Get device aggregate counts |
| `devices get-devices-view` | Paginated device listing |
| `policy lookup` | Resolve a batch of label IDs to metadata |
| `policy bulk-impact` | Aggregated impact for several labels — a read, despite the `bulk-` prefix |
| `policy lookup-network`, `lookup-network-export` | Assets expected to match a Network Policy Group |
| `policy lookup-dynamic`, `lookup-dynamic-totals`, `lookup-dynamic-export` | Assets expected to match a Dynamic Policy Group |
| `policy lookup-evaluation-endpoint` | Evaluation-endpoint IP lookup |
| `policy evaluate-policy`, `evaluate-policy-export` | Evaluate policy against a payload and return / export the result |
| `policy evaluate-policy-group-for-device` | Which policy group a given device would classify into |
| `policy preview-operation` | Preview the scope of a matrix operation — explicitly a dry run |
| `topology validate-*` | Validate a bulk VE/VEN payload without applying it |
| `insights *-preview` (`day0workflow-preview`, `day7workflow-preview`, `day15workflow-preview`, `day30workflow-preview`, `all-workflows-preview`, `post-policy-group-suggestions-preview`) | Preview a workflow or suggestion set without applying it |
| `flows traffic-record-export`, `flows flows-export` | Export traffic records / flow data as CSV |
| `devices generate-trust-policy` | Render the IAM trust-policy JSON for the operator to apply in AWS |
| `devices preview-azure-scope-*` | Azure workload discovery: preview the subscriptions and VM count a scope resolves to. Nothing is persisted |
| `connectors fetch-tanium-sensor-catalog`, `fetch-tanium-sensor-detail`, `probe-tanium-sensor-mapping` | Live reads from Tanium; CCC documents that the probe never affects connector health |

Anything not in this table gets the rule of thumb. When a new command appears
and you cannot tell, treat it as destructive and ask.

**The direction that matters holds.** Of the 405 state-changing-by-verb
commands, 61 are classified safe by the prefix rule above, and every one of them is
genuinely a read — no destructive command is misclassified as safe.
The table is an allowlist and is deliberately incomplete in the other direction:
missing an entry costs you an approval round you did not need, which is the
error worth making.

---

## Worked examples

Two end-to-end agent workflows that exercise the patterns above.

### Example 1 — "What's our Zero Trust score and which policy sets are dragging it down?"

```bash
# 1. Disambiguate (agent reflex — always start here)
elisity glossary explain "Zero Trust score"
#   → Term: Policy Enforcement Score
#   → Recipe: elisity reporting get-aggregate-enforcement-score
#   → Recipe: elisity reporting get-site-kpis --site <SITE>

# 2. Headline number
elisity reporting get-aggregate-enforcement-score
#   → [{"value": 73.4, ...}]

# 3. Per-site breakdown. CCC 26.7 removed the per-policy-set score, so
#    per-site is the narrowest enforcement score available; go to
#    policy-group granularity in step 4.
elisity -f table \
  -q '[].{site: siteName, score: policyEnforcementScore}' \
  reporting get-site-kpis
#   → lowest scores are the drag.

# 4. WHY they drag — per-group coverage, with the policyGroupId for step 5.
elisity -f table \
  -q '[].{site: siteName, pg: policyGroupName, pgId: policyGroupId, devCov: policyDeploymentMetrics.deviceCoverage}' \
  reporting get-zero-trust-metrics

# 5. The cause, per low-scoring group. Don't infer "simulation" from a low
#    score — read the monitorMode of the policies that reference the group.
#    Policies live in policy sets: repeat per POLICY_SET_ID
#    (elisity policy get-all-as-nd-json -q '[].id'), and run it once with
#    srcPolicyGroupIds and once with dstPolicyGroupIds.
elisity -f json policy search-policies-for-policy-set <POLICY_SET_ID> \
  --body '{"srcPolicyGroupIds":["PG_ID"],"size":250}' \
  -q '{total: totalElements, last: last, policies: content[].{name: name, mode: monitorMode, status: status}}'
#   → page while `last` is false ("page":1, 2, ...). Over every call and page:
#     `total` 0 = no policy; all MONITOR_ONLY = simulation; any
#     MONITOR_AND_ENFORCE = active but uncovered. See "Diagnosing a low/zero
#     Zero Trust score".
```

### Example 2 — "List our switches in visibility-only mode at the Boston site."

```bash
# 1. Disambiguate
elisity glossary explain "visibility ven"
#   → Term: Visibility-Only Virtual Edge Node
#   → Recipe: elisity topology get-virtual-edge-nodes (inspect mode field)

# 2. Pull all VENs at the site (sites are referenced by label)
elisity topology get-virtual-edge-nodes -q "content[?siteName==\`Boston\`]"

# 3. Filter to visibility-only mode
#    Per-tenant mode-field naming varies; first inspect a sample row:
elisity topology get-virtual-edge-nodes -q "content[0]"
#    Then once you know the field (e.g. `deploymentMode`):
elisity topology get-virtual-edge-nodes -q "content[?deploymentMode==\`VISIBILITY_ONLY\` && siteName==\`Boston\`]"
```

The honesty rule applies inside the filter, too — if the deployment-mode field
name on this tenant differs, report what you see in `content[0]` and ask the
human to confirm the field name rather than fabricating one.

---

## Where the mapping data lives

The mapping ships with the CLI, so it always matches the version you have
installed. `elisity glossary list` shows every term, and `glossary search` /
`glossary explain` read the same data without an API call. The terms come from
the Elisity product glossary.

If you find a glossary term that's missing a real CLI command, *do not*
invent one. Report it to Elisity Support (support@elisity.com) so the recipe
can be added. The honesty rule holds for every entry: a recipe names a real
command, or the recipe list is empty.
