# Punch List — M7.P5 scoped delta #507

**Audit tracker:** [#524](https://github.com/pixelelated/distribution/issues/524).

Generated2026-10-08 from [04-analysis.md](04-analysis.md). Four audit-discovered items:0Critical,0High,3Medium,1Low. Frozen distro ac64c80628 / product e6645cb5ea / ES4e410dc9. These are source/QA/tracker findings; no RC designation or candidate16rerun follows.

Resolve sequentially at the Phase7 gate. Root owns tracker and ES/UI remediation; the sole auditor owns isolated QA/host-control remediation and verifies every result. Original frozen observations remain unchanged. Confirmed fixes need source commits and direct acceptance artifacts; deferral requires a named open follow-up, priority, owner/milestone and rationale.

## Acceptance criteria

- [x] PL-001: Reconcile complete #510/#497 bodies against accepted integration/build evidence; retain exact final readbacks.
- [x] PL-002: Retire or adapt both stale folder QA entrypoints and their full contracts; prove current routing and historical boundaries.
- [x] PL-003: Restore safe localized actionable path-refusal guidance and verify exact-source target frames/unchanged pointers.
- [x] PL-004: Reject malformed audit receipt shapes normally; retain valid and negative controls.

## PL-001 — Reconcile current tracker bodies

- **Severity:** Medium
- **Category:** Spec Drift
- **Source finding:** F-01; blind F-12/refutation convergence; AC-510-06, AC-515-02, AC-497-04.
- **Owner area:** root coordinator, M7 tracking/build handoff.
- **What/where:** Full live #510and#497bodies, including appended current-state sections. Replace obsolete active/unintegrated/build-in-progress assertions using exact e6645/ES4e410integration and accepted185/187terminal receipts; preserve clearly historical evidence. Do not inflate assembled-image readiness.
- **Why/evidence:** Frozen bodies in inputs/issues contradict accepted source/build/retirement artifacts cited in02and04.
- **Acceptance:** Exact complete-body readbacks show current dependency/order/state and accurately checked evidence-backed criteria. Re-read after writing; keep history labeled. Root coordinates related M7/checkpoint state.
- **Already written:** No product/device state affected; conflicting live directions only.

## PL-002 — Make retained folder QA entrypoints truthful

- **Severity:** Medium
- **Category:** Test Gap
- **Source finding:** F-03; blind/refutation F-1; primary L-02comment cleanup.
- **Owner area:** sole auditor, isolated cloud-QA remediation; root applies any canonical instruction recommendation.
- **What/where:** tools/pixelelated-cloud-folder-test and tools/pixelelated-cloud-folder-vm-test. Either adapt all seed arguments, independent-pointer expectations, dependency overlay and discriminating refusal assertions, or explicitly retire the old contracts with a fail-closed historical-only entry and current replacement pointer. Classify related historical tools; preserve prior receipts. Correct rclone/package.mk84no-lock comment to match parent-held flock.
- **Why/evidence:** Frozen host case exits1because backend no-category call exits2; VM positive/refusal paths share stale assumptions. Current validator30controls and adapted round-trip/last-good harness already exist.
- **Acceptance:** Current/default invocation cannot claim qualification with the old contract; current qualification command is named. If historical mode remains, it requires explicit historical source selection and refuses current source before fixture/device work. Relevant host positive/negative controls and current validator suite pass. If adapting VM mode, prove actual complete guest overlay and intended refusal causes; explicit retirement needs no redundant current VM run. Canonical helper listing accurately names scope; package lint passes after comment edit.
- **Already written:** Synthetic test fixtures/receipts only; product selected-category contract remains intended.

## PL-003 — Explain why a selected cloud path was refused

- **Severity:** Medium
- **Category:** Code Quality
- **Source finding:** G-02; blind/refutation F-3.
- **Owner area:** root coordinator, ES/backend cloud setup.
- **What/where:** ES GuiMenu.cpp6504–6534path editor and bounded backend reason interface; cloud_setup473–474and530–543. Present a safe localized explanation/next action without exposing raw provider output. Preserve rejection and current pointers.
- **Why/evidence:** Actual indexed EN/FR640rejected-path frames show only generic advice; path-refusal-frame-verification.json proves hashes and callback identity. Backend specific invalid-component guidance is discarded. This is not a missing-frame or permission-bypass claim.
- **Acceptance:** Invalid-component, blank, provider-refusal and unreachable variants retain correct pointers and distinguish actionable safe reasons. Required syntax/catalog/package checks pass; affected EN/FR640×480and1280×800target frames match the final committed source and canonical CF05flow. If source/pin changes, source-bound proof precedes integration/promotion. Original generic frames remain historical/rejected-quality evidence with identities intact.
- **Already written:** Refused values did not replace selected paths; no cloud relocation/data repair required. Fix changes guidance only.

## PL-004 — Handle malformed JSON receipt object shapes

- **Severity:** Low
- **Category:** Code Quality
- **Source finding:** G-01; blind/refutation F-8.
- **Owner area:** sole auditor, isolated host-cadence remediation.
- **What/where:** tools/ceremony-check85–120/370and focused receipt controls. Validate expected JSON object shapes before get/items and return normal invalid-marker diagnostics for wrong types.
- **Why/evidence:** checks/blind-host-leads02/results.json: valid accepted; marker/evidence/tracker/completion lists raise AttributeError. Existing caller does not catch it. Crashing fails closed but loses the full report.
- **Acceptance:** Valid receipt still accepted; all4malformed object positions and representative scalar shapes reject without uncaught traceback; complete checker remains able to report other ceremonies. Existing15cadence controls remain green, invalid receipts never reset cadence. Test unchanged frozen source fails the added assertions, fixed source passes.
- **Already written:** No invalid completion counted through this crash; no prior device state or receipt rewriting needed.

## Pre-existing tracked scope (NOT punch items — exempt from Phase7)

#508current engineering-image inclusion/CF10/public ROCKNIX adoption, #492build sequence, #494runtime/release gates, #517integrity follow-up, #519owner alignment, #516private operation and #511public guides remain their existing scoped work. No private inventory is required in this public audit. Candidate16baseline qualification remains historical; no automatic full rerun.

## Unverified leads and coverage limits (no confirmed runtime verdict)

L-01post-confirmation external-config edit window; L-03OAuth token refresh vs whole-config digest; L-04delayed creation progress with no unit protocol; L-05UI-thread local-context timing; unusual invalid-context/marker-write fallback wording. Synthetic owned-VM probes can settle these without personal-cloud data. No new defect severity or PASS is manufactured. Full grading, rejected claims and three-way comparison are in04andsecond-opinions/primary-verification.md.

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-001 | Resolved | #497closed completed and#510image gate retained; independent exact full-body/primary-artifact readback in resolution/PL-001/acceptance.json at2026-10-08T15:55:53.060003+00:00 |
| PL-002 | Resolved | `2cc6ce30e3181d4dd570d42651d3f6492582feb7` source and`95a03b2eb1b0ec1ab501a752be4f40d5f425bb43` canonical mapping published;10retirement/30validator controls and package/rule checks; resolution/PL-002/acceptance.json |
| PL-003 | Resolved | ES `1d76b3da7da75794066df1c089931b890304da7a`, pin `59a3a321d105672234561339517337abb7eabe00` and proof `6caa839c8741585efe480dc99d63183d6982996c` published; 44 reviewed outcomes and host controls; resolution/PL-003/acceptance.json |
| PL-004 | Resolved | `8e8ad7c4060824ad5b43b3a471b79dfa385e28e5` published; 28 new controls and 15 existing controls pass, frozen source fails 25 new controls; resolution/PL-004/acceptance.json |

## Machine-readable index

```yaml
punch_index:
- id: PL-001
  severity: Medium
  category: Spec Drift
  source_finding: F-01
  owner_area: M7 coordinator
  where: GitHub issues 510 and 497
  acceptance: Exact complete-body readbacks agree with accepted integration and build state.
  outcome: resolved
- id: PL-002
  severity: Medium
  category: Test Gap
  source_finding: F-03
  owner_area: cloud QA tools
  where: tools/pixelelated-cloud-folder-test and tools/pixelelated-cloud-folder-vm-test
  acceptance: Current invocation has a truthful contract; historical gate and current controls pass.
  outcome: resolved
- id: PL-003
  severity: Medium
  category: Code Quality
  source_finding: G-02
  owner_area: ES cloud setup
  where: es-app/src/guis/GuiMenu.cpp path editor
  acceptance: Safe localized refusal reasons with unchanged pointers and source-bound affected frames.
  outcome: resolved
- id: PL-004
  severity: Low
  category: Code Quality
  source_finding: G-01
  owner_area: host audit cadence
  where: tools/ceremony-check
  acceptance: Valid receipts pass; malformed object shapes reject without checker traceback.
  outcome: resolved
```
