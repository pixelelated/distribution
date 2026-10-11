# Punch list — post-review component and qualification changes

Source: [04-analysis.md](04-analysis.md). Audit tracking: #553.

Four audit-discovered items: 0 Critical, 0 High, 1 Medium, 3 Low. All are open. No confirmed product runtime defect; no device build starts before these repairs and the audit closeout pass.

Can this be done on the VM? These repairs affect host qualification tools, source comments and audit evidence. Local isolated fixtures and byte-level artifact checks are the appropriate platform; no physical device or account is involved. Existing installed clean/retained VM qualification remains explicitly source-bound.

## PL-001: Bind the audit to current and complete evidence

- **Severity:** Medium
- **Category:** Missing Artifact
- **Source finding:** G-01 (F-1, F-2, F-3, F-4, F-13)
- **Owner area:** audit evidence and component dispositions
- **What:** Add the current rclone1.75.2 binding without rewriting old dispositions; link the executed upgrade manifest/diff, actual original build failures, pinned container controls, tracker closure readbacks, freshness and source/fixture/image evidence; distinguish13 names from14 recipes.
- **Where:** 02-forward-audit.md; 04-analysis.md; docs/qa-logs/2026-10-11-component-inputs/
- **Why:** A current verdict must identify the exact constituent artifacts and their limits.
- **Evidence:** checks/adjudication/source-probes.json; rehearsal.diff; supplemental-evidence.json; unfiltered-head.txt
- **Acceptance:** A command rehashes every supplemental artifact, validates the current rclone recipe/archive bindings and retained publication hold, verifies the original upgrade manifest and all three original build20 rc2 channels, and counts14 recipe files for13 names.

## PL-002: Discover fork tests without importing upstream test methods

- **Severity:** Low
- **Category:** Test Gap
- **Source finding:** G-02 (F-9)
- **Owner area:** proxy integration qualification
- **What:** Collect methods owned by fork-defined unittest classes, including new fork classes, and exclude imported/inherited upstream test methods.
- **Where:** tools/raofflineproxy-integration-test:233
- **Why:** Upstream fixture changes must not silently change the fork test count or run unrelated assertions.
- **Evidence:** checks/adjudication/pix553-lead-tests02/upstream-injected.log: original14 tests,2 injected failures
- **Acceptance:** The fixed real runner executes12 passing fork tests despite an injected failing upstream method, automatically includes an added fork test (13 passing), and still rejects the wrong cooldown duration.

## PL-003: Report unsupported historical rehearsal input cleanly

- **Severity:** Low
- **Category:** Code Quality
- **Source finding:** G-03 (F-12)
- **Owner area:** upgrade readiness qualification
- **What:** Validate the source read and complete wait_for_storage function boundary before extracting it; return a clear CLI diagnostic on missing, incomplete or unreadable input.
- **Where:** tools/vm-upgrade-readiness-test:14
- **Why:** Historical negative runs should fail deliberately rather than by an uncaught IndexError.
- **Evidence:** checks/adjudication/pix553-lead-tests02/old-rehearsal.log: original traceback/exit1
- **Acceptance:** All7 readiness controls pass; historical/missing-function, unterminated-function and unreadable-file controls exit2 with a meaningful diagnostic and no traceback.

## PL-004: Describe proxy pacing and VM ownership paths precisely

- **Severity:** Low
- **Category:** Documentation Gap
- **Source finding:** G-04 (F-8, F-10)
- **Owner area:** proxy patch and VM helper documentation
- **What:** Clarify deliberate per-ROM request throttle/batch cooldown versus background queue pacing; document the shared custom runtime root and requirement to retain the same owner environment for shutdown.
- **Where:** projects/ROCKNIX/packages/network/raofflineproxy/patches/004-no-cap-on-cached-games.patch:3; tools/vm-pair:17
- **Why:** Descriptions must match the preserved behavior and must not imply discovery of unrelated owners.
- **Evidence:** rom_browser.py requested>0 pace condition; checks/adjudication/literal-socket-search.txt
- **Acceptance:** The patch diff payload is byte-identical before/after; vm-pair changes are comments only, shell syntax and all9 launch controls pass; current references no longer hardcode custom sockets under/tmp.

## Pre-existing tracked scope (not punch items)

#528: source/licence/vendor/retrieval/off-host custody; #349/#511: public documentation; #265/#337/#359: release/publication and physical gates. These remain tracked independently and are not deferred audit findings.

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-001 | Open | Resolution and command evidence pending |
| PL-002 | Open | Resolution and command evidence pending |
| PL-003 | Open | Resolution and command evidence pending |
| PL-004 | Open | Resolution and command evidence pending |

## Machine-readable index

```yaml
punch_index:
- id: PL-001
  severity: "Medium"
  category: "Missing Artifact"
  source_finding: "G-01 (F-1, F-2, F-3, F-4, F-13)"
  owner_area: "audit evidence and component dispositions"
  where: "02-forward-audit.md; 04-analysis.md; docs/qa-logs/2026-10-11-component-inputs/"
  acceptance: "A command rehashes every supplemental artifact, validates the current rclone recipe/archive bindings and retained publication hold, verifies the original upgrade manifest and all three original build20 rc2 channels, and counts14 recipe files for13 names."
  outcome: open
- id: PL-002
  severity: "Low"
  category: "Test Gap"
  source_finding: "G-02 (F-9)"
  owner_area: "proxy integration qualification"
  where: "tools/raofflineproxy-integration-test:233"
  acceptance: "The fixed real runner executes12 passing fork tests despite an injected failing upstream method, automatically includes an added fork test (13 passing), and still rejects the wrong cooldown duration."
  outcome: open
- id: PL-003
  severity: "Low"
  category: "Code Quality"
  source_finding: "G-03 (F-12)"
  owner_area: "upgrade readiness qualification"
  where: "tools/vm-upgrade-readiness-test:14"
  acceptance: "All7 readiness controls pass; historical/missing-function, unterminated-function and unreadable-file controls exit2 with a meaningful diagnostic and no traceback."
  outcome: open
- id: PL-004
  severity: "Low"
  category: "Documentation Gap"
  source_finding: "G-04 (F-8, F-10)"
  owner_area: "proxy patch and VM helper documentation"
  where: "projects/ROCKNIX/packages/network/raofflineproxy/patches/004-no-cap-on-cached-games.patch:3; tools/vm-pair:17"
  acceptance: "The patch diff payload is byte-identical before/after; vm-pair changes are comments only, shell syntax and all9 launch controls pass; current references no longer hardcode custom sockets under/tmp."
  outcome: open
```


Repair tracker: [#554 — M7.P5 post-review evidence and tool gaps](https://github.com/pixelelated/distribution/issues/554), child of #344; audit #553.
