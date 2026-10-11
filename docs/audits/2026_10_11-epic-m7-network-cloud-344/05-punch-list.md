# Punch List — M7.P5 network/cloud feedback #344

Generated:2026-10-11. Source:[04-analysis.md](04-analysis.md).
Total:7 audit-discovered items (Critical:0, High:3, Medium:1, Low:3).
Independent review and all seven repairs are complete. Landed commits and actual-target evidence below resolve every finding. Combined-image qualification remains separate; no RC or deployed-image claim.

Work sequentially under the existing implementation authority. Preserve the frozen
inputs and failing controls; record each new source revision and actual guest
verification. Before any test: can it run on the VM? Yes; all listed probes use
the owned disposable guest, synthetic data and local aliases/endpoints.

## PL-001: Preserve a completed OAuth token during staged configuration

- **Severity:** High
- **Category:** Interaction Defect
- **Source finding:** G-01
- **Owner area:** cloud connection lifecycle / M7.P5 #537
- **What:** Pre-answer only the refresh-token question for an OAuth token already obtained; retain strict refusal of other unanswered provider questions.
- **Where:** cloud_oauth:544; cloud_connections.py:159
- **Why:** Preserve account-specific consent, safe credential state and accurate player guidance.
- **Evidence:** `checks/target-original/` for F-01–03; `checks/second-opinion-verification/` plus the lead grading table for G-01–04. Original outcomes are explicitly failing, not fixed-source results.
- **Acceptance:** Actual real-rclone create/update OAuth configuration proceeds without token refresh; staged save succeeds with a bounded synthetic verifier; unknown State still refuses, and cancellation/replacement preserve original config.

## PL-002: Bind scan stamps to selected-account state

- **Severity:** High
- **Category:** Interaction Defect
- **Source finding:** F-01
- **Owner area:** cloud connection lifecycle / M7.P5 #537
- **What:** Include active-connection presence and bytes in the local context; prove the ES consumer rejects stale stamps.
- **Where:** cloud_scan:171
- **Why:** Preserve account-specific consent, safe credential state and accurate player guidance.
- **Evidence:** `checks/target-original/` for F-01–03; `checks/second-opinion-verification/` plus the lead grading table for G-01–04. Original outcomes are explicitly failing, not fixed-source results.
- **Acceptance:** Actual guest completed and in-flight scans invalidate on selection change; missing, empty and selected states differ; unchanged context remains valid.

## PL-003: Bind destructive previews and content preflight to full configuration

- **Severity:** High
- **Category:** Interaction Defect
- **Source finding:** F-03, O-5
- **Owner area:** cloud connection lifecycle / M7.P5 #537
- **What:** Capture context before preflight, bind match plan to it, recheck under lock, reject and spend old/unbound/stale plans with an actionable reason. Cover same-name credential/path changes in ordinary content transfer.
- **Where:** cloud_content_restore:798,856,1484; cloud_content_backup:687
- **Why:** Preserve account-specific consent, safe credential state and accurate player guidance.
- **Evidence:** `checks/target-original/` for F-01–03; `checks/second-opinion-verification/` plus the lead grading table for G-01–04. Original outcomes are explicitly failing, not fixed-source results.
- **Acceptance:** Actual guest refuses selected-account, same-name config and folder changes plus old unbound plans with local/cloud sentinel hashes unchanged; unchanged-context apply still works; save exclusions and delete cap stay intact.

## PL-004: Hold the shared lock throughout folder creation

- **Severity:** Medium
- **Category:** Interaction Defect
- **Source finding:** F-02
- **Owner area:** cloud connection lifecycle / M7.P5 #537
- **What:** Take cloud_sync.lock before resolving the selected remote; hold through mkdir, notes and readback, with no inherited descriptor in rclone children.
- **Where:** cloud_setup:791
- **Why:** Preserve account-specific consent, safe credential state and accurate player guidance.
- **Evidence:** `checks/target-original/` for F-01–03; `checks/second-opinion-verification/` plus the lead grading table for G-01–04. Original outcomes are explicitly failing, not fixed-source results.
- **Acceptance:** Guest seed blocks select/replace/remove; busy seed exits75 before any write; unchanged creation succeeds and child does not keep lock after parent exit.

## PL-005: Explain explicit, missing and unselected cloud connections accurately

- **Severity:** Low
- **Category:** Interaction Defect
- **Source finding:** G-02 (O-3, O-4, O-6)
- **Owner area:** cloud connection lifecycle / M7.P5 #537
- **What:** Replace alphabetical-first setup guidance, retain missing-selection recovery in translated errors, distinguish no connection selected from no configuration. Keep safe no-fallback behavior.
- **Where:** GuiMenu.cpp:6825,7125; cloud_scan/content/saves selection refusals; rclone-cloud-sync.md
- **Why:** Preserve account-specific consent, safe credential state and accurate player guidance.
- **Evidence:** `checks/target-original/` for F-01–03; `checks/second-opinion-verification/` plus the lead grading table for G-01–04. Original outcomes are explicitly failing, not fixed-source results.
- **Acceptance:** Reviewed EN/FR affected flow/branch frames at640×480/1280×800; backend refusal controls preserve config and payload; canonical flow/index/translations and selection instructions match source.

## PL-006: Quote the connection name passed to CHECK CONNECTION

- **Severity:** Low
- **Category:** Interaction Defect
- **Source finding:** G-03 (O-7)
- **Owner area:** cloud connection lifecycle / M7.P5 #537
- **What:** Use the established shellQuote helper for the complete remote argument.
- **Where:** GuiMenu.cpp:6621
- **Why:** Preserve account-specific consent, safe credential state and accurate player guidance.
- **Evidence:** `checks/target-original/` for F-01–03; `checks/second-opinion-verification/` plus the lead grading table for G-01–04. Original outcomes are explicitly failing, not fixed-source results.
- **Acceptance:** Actual guest check for a saved name containing spaces succeeds with exact argv; regression/source check verifies quote path and reviewed flow still presents the right name.

## PL-007: Finish or cancel staged credentials before normal sign-in shutdown

- **Severity:** Low
- **Category:** Interaction Defect
- **Source finding:** G-04 (O-11)
- **Owner area:** cloud connection lifecycle / M7.P5 #537
- **What:** Give the complete staged transaction a safe normal-shutdown lifetime or cancellation boundary; cleanup must finish before the daemon collector can be abandoned.
- **Where:** cloud_oauth:2033; cloud_connections.py:159,167
- **Why:** Preserve account-specific consent, safe credential state and accurate player guidance.
- **Evidence:** `checks/target-original/` for F-01–03; `checks/second-opinion-verification/` plus the lead grading table for G-01–04. Original outcomes are explicitly failing, not fixed-source results.
- **Acceptance:** Guest staged two-call shutdown fixture returns with no collector and no .connection-* config; prior live config/selection unchanged; successful publication and cancelled/obsolete attempt tests still pass.

## Pre-existing tracked scope (not punch items)

#535–539: original delivery, canonical UI proof, integration/pins and installed-image qualification.
#511: public site guides. #528: release source/licence components.
These are not deferred audit findings. No source is promoted before the repair proof.

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-001 | Resolved | `bc2dceb406969a401d987de168acfb3ae60b7e01`; guest53/transactions.log: 26 actual-rclone transaction controls, including completed OAuth tokens, unknown State and preserved/cancelled replacements |
| PL-002 | Resolved | `bc2dceb406969a401d987de168acfb3ae60b7e01`; pix540-scan34/result.json: completed/in-flight invalidation, distinct missing/empty states and unchanged-context control |
| PL-003 | Resolved | `bc2dceb406969a401d987de168acfb3ae60b7e01`; pix540-content35/result.json: 9 context/plan controls; regression52 covers save exclusions/delete cap |
| PL-004 | Resolved | `bc2dceb406969a401d987de168acfb3ae60b7e01`; pix540-seed37/result.json: 6 shared-lock/busy75/child-descriptor controls |
| PL-005 | Resolved | `bc2dceb406969a401d987de168acfb3ae60b7e01` + ES `c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`; guest53/refusals.json: 15 byte-preserving refusals; QA repair-frame-index.json: NC14–NC16 EN/FR640/1280 |
| PL-006 | Resolved | `bc2dceb406969a401d987de168acfb3ae60b7e01` + ES `c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`; QA repair-frame-index.json: NC13 actual CHECK CONNECTION for two words succeeds in all four cohorts |
| PL-007 | Resolved | `bc2dceb406969a401d987de168acfb3ae60b7e01`; pix540-final-guest39/result.json: collector + HTTP worker drained, no stage/live worker, old config unchanged; guest53 successes/cancellations remain green |

Branch containment and per-path `git log -1` were re-derived in
[checks/resolution59/landed-readback.json](checks/resolution59/landed-readback.json).
Evidence paths in the table are under `checks/remediation/`; QA means
[the source-bound frame packet](../../qa-logs/2026-10-11-network-cloud-management/repair-frame-index.json).

## Machine-readable index

```yaml
punch_index:
- id: PL-001
  severity: High
  category: Interaction Defect
  source_finding: "G-01"
  owner_area: cloud connection lifecycle
  where: "cloud_oauth:544; cloud_connections.py:159"
  acceptance: "Actual real-rclone create/update OAuth configuration proceeds without token refresh; staged save succeeds with a bounded synthetic verifier; unknown State still refuses, and cancellation/replacement preserve original config."
  outcome: resolved
- id: PL-002
  severity: High
  category: Interaction Defect
  source_finding: "F-01"
  owner_area: cloud connection lifecycle
  where: "cloud_scan:171"
  acceptance: "Actual guest completed and in-flight scans invalidate on selection change; missing, empty and selected states differ; unchanged context remains valid."
  outcome: resolved
- id: PL-003
  severity: High
  category: Interaction Defect
  source_finding: "F-03, O-5"
  owner_area: cloud connection lifecycle
  where: "cloud_content_restore:798,856,1484; cloud_content_backup:687"
  acceptance: "Actual guest refuses selected-account, same-name config and folder changes plus old unbound plans with local/cloud sentinel hashes unchanged; unchanged-context apply still works; save exclusions and delete cap stay intact."
  outcome: resolved
- id: PL-004
  severity: Medium
  category: Interaction Defect
  source_finding: "F-02"
  owner_area: cloud connection lifecycle
  where: "cloud_setup:791"
  acceptance: "Guest seed blocks select/replace/remove; busy seed exits75 before any write; unchanged creation succeeds and child does not keep lock after parent exit."
  outcome: resolved
- id: PL-005
  severity: Low
  category: Interaction Defect
  source_finding: "G-02 (O-3, O-4, O-6)"
  owner_area: cloud connection lifecycle
  where: "GuiMenu.cpp:6825,7125; cloud_scan/content/saves selection refusals; rclone-cloud-sync.md"
  acceptance: "Reviewed EN/FR affected flow/branch frames at640\u00d7480/1280\u00d7800; backend refusal controls preserve config and payload; canonical flow/index/translations and selection instructions match source."
  outcome: resolved
- id: PL-006
  severity: Low
  category: Interaction Defect
  source_finding: "G-03 (O-7)"
  owner_area: cloud connection lifecycle
  where: "GuiMenu.cpp:6621"
  acceptance: "Actual guest check for a saved name containing spaces succeeds with exact argv; regression/source check verifies quote path and reviewed flow still presents the right name."
  outcome: resolved
- id: PL-007
  severity: Low
  category: Interaction Defect
  source_finding: "G-04 (O-11)"
  owner_area: cloud connection lifecycle
  where: "cloud_oauth:2033; cloud_connections.py:159,167"
  acceptance: "Guest staged two-call shutdown fixture returns with no collector and no .connection-* config; prior live config/selection unchanged; successful publication and cancelled/obsolete attempt tests still pass."
  outcome: resolved
```

Audit remediation tracker: [M7.P5 #540](https://github.com/pixelelated/distribution/issues/540), child of #344.
