# Audit Analysis — M7.P5 scoped delta #507

**Audit tracker:** [#524](https://github.com/pixelelated/distribution/issues/524).

**Auditor:** Code Auditor skill; sole serial owner `/root/m7_fresh_audit_owner`, Codex/OpenAI (exact served variant unknown).
**Date:** 2026-10-08
**Spec:** frozen #507/M7 and30issue snapshots in inputs/;130criteria.
**Frozen input:** distribution ac64c80628ad6d5a69b803d82f186472529f7cd7; product e6645cb5ea5ae3c7f699390a74b22d098fbeb7fb; ES4e410dc9a816cc947f16235ad2b24824b29dd84e.
**Baseline:** candidate16 ee014909137e03706e0b3020b8396be589aaa705 / ES72494bc72e3d64d4dcfeb4e6478052bbdf166c5b.
**Status:** Phases 0–7 complete: all four findings are independently verified resolved. Current outcomes and exact published commits are in 05; original frozen findings and criterion verdicts remain historical. Tracker closure and compact publication receipts accompany this analysis. This is not an RC designation.

## Executive Summary

The audited delta is coherent and substantially qualified at the source/affected-runtime level. Explicit manual cloud folder selection replaces automatic migration; bounded category checks distinguish readiness from integrity. Actual standalone save writers, custom filter preservation and native DuckStation screenshot/package prerequisites have source-bound target evidence. Build, retention and audit-cadence repairs retain original failures as well as successful controls. Candidate16 qualification is preserved as historical evidence, without replaying its full matrix or promoting a source overlay into assembled firmware.

The frozen review identified four audit findings. The original two were tracker bodies describing completed work as active, and two documented folder regression tools depending on the retired implicit-seeding contract. All four now have primary acceptance receipts under resolution/PL-001 through PL-004 and exact published fixes. The proposed #504custody-wording finding was withdrawn after the complete body refuted its premise. A fresh synthetic case reproduces the test-tool failure. Independent review adds Low malformed-receipt handling and Medium loss of actionable path-refusal guidance, verified respectively by host controls and source-bound target frames. There is no newly confirmed High/Critical runtime defect. A narrow UI-confirmation-to-worker configuration race remains an unverified source lead. Both approved cross-lab calls passed identity, effort, outcome and digest gates; every lead is primary-graded below. The final punch list records four resolved outcomes; completion and publication receipts preserve the lifecycle gates separately.

## Acceptance-criteria scorecard

Independent Phase2 verdicts are historical observations of the frozen scope, including future and private/self-audit gates. They are not a release pass rate. The scorecard below applies the explicit Phase4.5 regrade of AC-504-04toUNTESTABLE; the original ledger remains unchanged for auditable independence. Later lifecycle fulfillment is recorded separately.

| Issue | PASS | PARTIAL | FAIL | SKIP | UNTESTABLE | Count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| #461 | 4 | 0 | 0 | 0 | 0 | 4 |
| #489 | 3 | 0 | 0 | 0 | 0 | 3 |
| #490 | 3 | 0 | 0 | 0 | 0 | 3 |
| #491 | 3 | 0 | 0 | 0 | 0 | 3 |
| #492 | 3 | 2 | 0 | 0 | 0 | 5 |
| #494 | 3 | 0 | 0 | 0 | 2 | 5 |
| #495 | 3 | 0 | 0 | 0 | 0 | 3 |
| #496 | 3 | 0 | 0 | 0 | 0 | 3 |
| #497 | 3 | 1 | 0 | 0 | 0 | 4 |
| #498 | 4 | 0 | 0 | 0 | 0 | 4 |
| #499 | 3 | 0 | 0 | 0 | 0 | 3 |
| #500 | 4 | 0 | 0 | 0 | 0 | 4 |
| #501 | 3 | 0 | 0 | 0 | 0 | 3 |
| #502 | 5 | 0 | 0 | 0 | 0 | 5 |
| #503 | 4 | 0 | 0 | 0 | 0 | 4 |
| #504 | 0 | 1 | 0 | 3 | 1 | 5 |
| #506 | 3 | 0 | 0 | 0 | 0 | 3 |
| #507 | 1 | 1 | 0 | 3 | 0 | 5 |
| #508 | 3 | 4 | 0 | 0 | 0 | 7 |
| #510 | 4 | 1 | 1 | 0 | 0 | 6 |
| #512 | 4 | 0 | 0 | 0 | 0 | 4 |
| #513 | 5 | 0 | 0 | 0 | 0 | 5 |
| #514 | 4 | 0 | 0 | 0 | 0 | 4 |
| #515 | 3 | 1 | 0 | 1 | 0 | 5 |
| #517 | 2 | 2 | 0 | 3 | 0 | 7 |
| #519 | 0 | 2 | 0 | 2 | 0 | 4 |
| #520 | 6 | 0 | 0 | 0 | 0 | 6 |
| #521 | 5 | 0 | 0 | 0 | 0 | 5 |
| #522 | 4 | 0 | 0 | 0 | 0 | 4 |
| #523 | 4 | 0 | 0 | 0 | 0 | 4 |
| **Total** | 99 | 15 | 1 | 12 | 3 | 130 |

**Pass rate:** 99/130 criteria fully met (76.15%).

| ID | Verdict | Criterion source |
| --- | --- | --- |
| AC-461-01 | PASS | inputs/issues/461.json:body-line19; full exact criterion and primary evidence in02 |
| AC-461-02 | PASS | inputs/issues/461.json:body-line20; full exact criterion and primary evidence in02 |
| AC-461-03 | PASS | inputs/issues/461.json:body-line21; full exact criterion and primary evidence in02 |
| AC-461-04 | PASS | inputs/issues/461.json:body-line22; full exact criterion and primary evidence in02 |
| AC-489-01 | PASS | inputs/issues/489.json:body-line20; full exact criterion and primary evidence in02 |
| AC-489-02 | PASS | inputs/issues/489.json:body-line22; full exact criterion and primary evidence in02 |
| AC-489-03 | PASS | inputs/issues/489.json:body-line24; full exact criterion and primary evidence in02 |
| AC-490-01 | PASS | inputs/issues/490.json:body-line17; full exact criterion and primary evidence in02 |
| AC-490-02 | PASS | inputs/issues/490.json:body-line19; full exact criterion and primary evidence in02 |
| AC-490-03 | PASS | inputs/issues/490.json:body-line21; full exact criterion and primary evidence in02 |
| AC-491-01 | PASS | inputs/issues/491.json:body-line20; full exact criterion and primary evidence in02 |
| AC-491-02 | PASS | inputs/issues/491.json:body-line22; full exact criterion and primary evidence in02 |
| AC-491-03 | PASS | inputs/issues/491.json:body-line25; full exact criterion and primary evidence in02 |
| AC-492-01 | PARTIAL | inputs/issues/492.json:body-line19; full exact criterion and primary evidence in02 |
| AC-492-02 | PASS | inputs/issues/492.json:body-line20; full exact criterion and primary evidence in02 |
| AC-492-03 | PASS | inputs/issues/492.json:body-line21; full exact criterion and primary evidence in02 |
| AC-492-04 | PASS | inputs/issues/492.json:body-line22; full exact criterion and primary evidence in02 |
| AC-492-05 | PARTIAL | inputs/issues/492.json:body-line23; full exact criterion and primary evidence in02 |
| AC-494-01 | PASS | inputs/issues/494.json:body-line26; full exact criterion and primary evidence in02 |
| AC-494-02 | PASS | inputs/issues/494.json:body-line27; full exact criterion and primary evidence in02 |
| AC-494-03 | UNTESTABLE | inputs/issues/494.json:body-line28; full exact criterion and primary evidence in02 |
| AC-494-04 | UNTESTABLE | inputs/issues/494.json:body-line29; full exact criterion and primary evidence in02 |
| AC-494-05 | PASS | inputs/issues/494.json:body-line30; full exact criterion and primary evidence in02 |
| AC-495-01 | PASS | inputs/issues/495.json:body-line11; full exact criterion and primary evidence in02 |
| AC-495-02 | PASS | inputs/issues/495.json:body-line12; full exact criterion and primary evidence in02 |
| AC-495-03 | PASS | inputs/issues/495.json:body-line13; full exact criterion and primary evidence in02 |
| AC-496-01 | PASS | inputs/issues/496.json:body-line7; full exact criterion and primary evidence in02 |
| AC-496-02 | PASS | inputs/issues/496.json:body-line8; full exact criterion and primary evidence in02 |
| AC-496-03 | PASS | inputs/issues/496.json:body-line9; full exact criterion and primary evidence in02 |
| AC-497-01 | PASS | inputs/issues/497.json:body-line11; full exact criterion and primary evidence in02 |
| AC-497-02 | PASS | inputs/issues/497.json:body-line12; full exact criterion and primary evidence in02 |
| AC-497-03 | PASS | inputs/issues/497.json:body-line13; full exact criterion and primary evidence in02 |
| AC-497-04 | PARTIAL | inputs/issues/497.json:body-line14; full exact criterion and primary evidence in02 |
| AC-498-01 | PASS | inputs/issues/498.json:body-line8; full exact criterion and primary evidence in02 |
| AC-498-02 | PASS | inputs/issues/498.json:body-line9; full exact criterion and primary evidence in02 |
| AC-498-03 | PASS | inputs/issues/498.json:body-line10; full exact criterion and primary evidence in02 |
| AC-498-04 | PASS | inputs/issues/498.json:body-line11; full exact criterion and primary evidence in02 |
| AC-499-01 | PASS | inputs/issues/499.json:body-line6; full exact criterion and primary evidence in02 |
| AC-499-02 | PASS | inputs/issues/499.json:body-line7; full exact criterion and primary evidence in02 |
| AC-499-03 | PASS | inputs/issues/499.json:body-line8; full exact criterion and primary evidence in02 |
| AC-500-01 | PASS | inputs/issues/500.json:body-line15; full exact criterion and primary evidence in02 |
| AC-500-02 | PASS | inputs/issues/500.json:body-line16; full exact criterion and primary evidence in02 |
| AC-500-03 | PASS | inputs/issues/500.json:body-line17; full exact criterion and primary evidence in02 |
| AC-500-04 | PASS | inputs/issues/500.json:body-line18; full exact criterion and primary evidence in02 |
| AC-501-01 | PASS | inputs/issues/501.json:body-line13; full exact criterion and primary evidence in02 |
| AC-501-02 | PASS | inputs/issues/501.json:body-line14; full exact criterion and primary evidence in02 |
| AC-501-03 | PASS | inputs/issues/501.json:body-line15; full exact criterion and primary evidence in02 |
| AC-502-01 | PASS | inputs/issues/502.json:body-line57; full exact criterion and primary evidence in02 |
| AC-502-02 | PASS | inputs/issues/502.json:body-line58; full exact criterion and primary evidence in02 |
| AC-502-03 | PASS | inputs/issues/502.json:body-line59; full exact criterion and primary evidence in02 |
| AC-502-04 | PASS | inputs/issues/502.json:body-line60; full exact criterion and primary evidence in02 |
| AC-502-05 | PASS | inputs/issues/502.json:body-line61; full exact criterion and primary evidence in02 |
| AC-503-01 | PASS | inputs/issues/503.json:body-line21; full exact criterion and primary evidence in02 |
| AC-503-02 | PASS | inputs/issues/503.json:body-line22; full exact criterion and primary evidence in02 |
| AC-503-03 | PASS | inputs/issues/503.json:body-line23; full exact criterion and primary evidence in02 |
| AC-503-04 | PASS | inputs/issues/503.json:body-line24; full exact criterion and primary evidence in02 |
| AC-504-01 | SKIP | inputs/issues/504.json:body-line13; full exact criterion and primary evidence in02 |
| AC-504-02 | SKIP | inputs/issues/504.json:body-line14; full exact criterion and primary evidence in02 |
| AC-504-03 | PARTIAL | inputs/issues/504.json:body-line15; full exact criterion and primary evidence in02 |
| AC-504-04 | UNTESTABLE | inputs/issues/504.json:body-line16; full exact criterion and primary evidence in02 |
| AC-504-05 | SKIP | inputs/issues/504.json:body-line32; full exact criterion and primary evidence in02 |
| AC-506-01 | PASS | inputs/issues/506.json:body-line13; full exact criterion and primary evidence in02 |
| AC-506-02 | PASS | inputs/issues/506.json:body-line14; full exact criterion and primary evidence in02 |
| AC-506-03 | PASS | inputs/issues/506.json:body-line15; full exact criterion and primary evidence in02 |
| AC-507-01 | PASS | inputs/issues/507.json:body-line20; full exact criterion and primary evidence in02 |
| AC-507-02 | PARTIAL | inputs/issues/507.json:body-line21; full exact criterion and primary evidence in02 |
| AC-507-03 | SKIP | inputs/issues/507.json:body-line22; full exact criterion and primary evidence in02 |
| AC-507-04 | SKIP | inputs/issues/507.json:body-line23; full exact criterion and primary evidence in02 |
| AC-507-05 | SKIP | inputs/issues/507.json:body-line24; full exact criterion and primary evidence in02 |
| AC-508-01 | PASS | inputs/issues/508.json:body-line34; full exact criterion and primary evidence in02 |
| AC-508-02 | PARTIAL | inputs/issues/508.json:body-line35; full exact criterion and primary evidence in02 |
| AC-508-03 | PARTIAL | inputs/issues/508.json:body-line36; full exact criterion and primary evidence in02 |
| AC-508-04 | PARTIAL | inputs/issues/508.json:body-line37; full exact criterion and primary evidence in02 |
| AC-508-05 | PASS | inputs/issues/508.json:body-line38; full exact criterion and primary evidence in02 |
| AC-508-06 | PASS | inputs/issues/508.json:body-line39; full exact criterion and primary evidence in02 |
| AC-508-07 | PARTIAL | inputs/issues/508.json:body-line40; full exact criterion and primary evidence in02 |
| AC-510-01 | PASS | inputs/issues/510.json:body-line33; full exact criterion and primary evidence in02 |
| AC-510-02 | PASS | inputs/issues/510.json:body-line34; full exact criterion and primary evidence in02 |
| AC-510-03 | PASS | inputs/issues/510.json:body-line35; full exact criterion and primary evidence in02 |
| AC-510-04 | PASS | inputs/issues/510.json:body-line36; full exact criterion and primary evidence in02 |
| AC-510-05 | PARTIAL | inputs/issues/510.json:body-line37; full exact criterion and primary evidence in02 |
| AC-510-06 | FAIL | inputs/issues/510.json:body-line38; full exact criterion and primary evidence in02 |
| AC-512-01 | PASS | inputs/issues/512.json:body-line15; full exact criterion and primary evidence in02 |
| AC-512-02 | PASS | inputs/issues/512.json:body-line16; full exact criterion and primary evidence in02 |
| AC-512-03 | PASS | inputs/issues/512.json:body-line17; full exact criterion and primary evidence in02 |
| AC-512-04 | PASS | inputs/issues/512.json:body-line18; full exact criterion and primary evidence in02 |
| AC-513-01 | PASS | inputs/issues/513.json:body-line19; full exact criterion and primary evidence in02 |
| AC-513-02 | PASS | inputs/issues/513.json:body-line20; full exact criterion and primary evidence in02 |
| AC-513-03 | PASS | inputs/issues/513.json:body-line21; full exact criterion and primary evidence in02 |
| AC-513-04 | PASS | inputs/issues/513.json:body-line22; full exact criterion and primary evidence in02 |
| AC-513-05 | PASS | inputs/issues/513.json:body-line23; full exact criterion and primary evidence in02 |
| AC-514-01 | PASS | inputs/issues/514.json:body-line15; full exact criterion and primary evidence in02 |
| AC-514-02 | PASS | inputs/issues/514.json:body-line16; full exact criterion and primary evidence in02 |
| AC-514-03 | PASS | inputs/issues/514.json:body-line17; full exact criterion and primary evidence in02 |
| AC-514-04 | PASS | inputs/issues/514.json:body-line18; full exact criterion and primary evidence in02 |
| AC-515-01 | PASS | inputs/issues/515.json:body-line36; full exact criterion and primary evidence in02 |
| AC-515-02 | PARTIAL | inputs/issues/515.json:body-line37; full exact criterion and primary evidence in02 |
| AC-515-03 | SKIP | inputs/issues/515.json:body-line38; full exact criterion and primary evidence in02 |
| AC-515-04 | PASS | inputs/issues/515.json:body-line39; full exact criterion and primary evidence in02 |
| AC-515-05 | PASS | inputs/issues/515.json:body-line40; full exact criterion and primary evidence in02 |
| AC-517-01 | SKIP | inputs/issues/517.json:body-line17; full exact criterion and primary evidence in02 |
| AC-517-02 | SKIP | inputs/issues/517.json:body-line18; full exact criterion and primary evidence in02 |
| AC-517-03 | PARTIAL | inputs/issues/517.json:body-line19; full exact criterion and primary evidence in02 |
| AC-517-04 | PASS | inputs/issues/517.json:body-line20; full exact criterion and primary evidence in02 |
| AC-517-05 | SKIP | inputs/issues/517.json:body-line21; full exact criterion and primary evidence in02 |
| AC-517-06 | PARTIAL | inputs/issues/517.json:body-line22; full exact criterion and primary evidence in02 |
| AC-517-07 | PASS | inputs/issues/517.json:body-line28; full exact criterion and primary evidence in02 |
| AC-519-01 | SKIP | inputs/issues/519.json:body-line21; full exact criterion and primary evidence in02 |
| AC-519-02 | PARTIAL | inputs/issues/519.json:body-line22; full exact criterion and primary evidence in02 |
| AC-519-03 | SKIP | inputs/issues/519.json:body-line23; full exact criterion and primary evidence in02 |
| AC-519-04 | PARTIAL | inputs/issues/519.json:body-line24; full exact criterion and primary evidence in02 |
| AC-520-01 | PASS | inputs/issues/520.json:body-line24; full exact criterion and primary evidence in02 |
| AC-520-02 | PASS | inputs/issues/520.json:body-line25; full exact criterion and primary evidence in02 |
| AC-520-03 | PASS | inputs/issues/520.json:body-line26; full exact criterion and primary evidence in02 |
| AC-520-04 | PASS | inputs/issues/520.json:body-line27; full exact criterion and primary evidence in02 |
| AC-520-05 | PASS | inputs/issues/520.json:body-line28; full exact criterion and primary evidence in02 |
| AC-520-06 | PASS | inputs/issues/520.json:body-line29; full exact criterion and primary evidence in02 |
| AC-521-01 | PASS | inputs/issues/521.json:body-line23; full exact criterion and primary evidence in02 |
| AC-521-02 | PASS | inputs/issues/521.json:body-line24; full exact criterion and primary evidence in02 |
| AC-521-03 | PASS | inputs/issues/521.json:body-line25; full exact criterion and primary evidence in02 |
| AC-521-04 | PASS | inputs/issues/521.json:body-line26; full exact criterion and primary evidence in02 |
| AC-521-05 | PASS | inputs/issues/521.json:body-line27; full exact criterion and primary evidence in02 |
| AC-522-01 | PASS | inputs/issues/522.json:body-line22; full exact criterion and primary evidence in02 |
| AC-522-02 | PASS | inputs/issues/522.json:body-line23; full exact criterion and primary evidence in02 |
| AC-522-03 | PASS | inputs/issues/522.json:body-line24; full exact criterion and primary evidence in02 |
| AC-522-04 | PASS | inputs/issues/522.json:body-line25; full exact criterion and primary evidence in02 |
| AC-523-01 | PASS | inputs/issues/523.json:body-line22; full exact criterion and primary evidence in02 |
| AC-523-02 | PASS | inputs/issues/523.json:body-line23; full exact criterion and primary evidence in02 |
| AC-523-03 | PASS | inputs/issues/523.json:body-line24; full exact criterion and primary evidence in02 |
| AC-523-04 | PASS | inputs/issues/523.json:body-line25; full exact criterion and primary evidence in02 |

## Code Quality Assessment

Strengths: explicit category arguments, bounded JSON parser/validator identity, selected-root discovery, progress/content separation, atomic default-filter merging and preserved custom writer paths. Target package mode and dependency closure are checked at actual installed consumers. The fresh finite checks cover42install/lifecycle cases,145cloud/integrity controls,15cadence/19retention/8cleanup controls,183ESunit cases/4752assertions, six syntax units and required package/instruction/catalog/map checks. These host controls corroborate separately bound target receipts; they are not new device-runtime qualification.

Concerns and complexity hotspots: cloud_setup's large shell dispatcher and repeated configuration/path grammar; GuiMenu's callbacks spanning a worker; many historical QA helpers retained beside their replacements. A tool can advertise current regression coverage while its first success expectation is obsolete. The source comment about scan locking also lags actual parent-held flock behavior (L-02), although the code and tested behavior are correct.

## Cornerstone Conformance

Overall HIGH for qualified source behavior, with specific process gaps.03contains30rule-file rows and74distinct blindspot dispositions (the register has two different29entries). Invariants for progress preservation, no secret exposure, allowlist semantics and upgrade/clean-install boundaries are individually assessed there. Rules match current distribution next; no source changes occurred in the audit. Confirmed gaps map to existing rules, rather than demonstrating a missing rule family.

## Spec Fidelity

Aligned: D-CLOUD175–181, ordinary explicit setup and folder selection, read-only readiness checks, instructions-only generic relocation disposition, native capture and standalone save layout, preserved custom state. Automatic migration/legacy join/follow are retired deliberately. Public ROCKNIX is the adoption baseline; unpublished fork layouts do not become fielded compatibility promises.

Diverged: #510 and #497 bodies retain active-work directions after exact integration/build/retirement evidence. These do not negate demonstrated product behavior, but they can cause a new agent to repeat work or misunderstand current readiness. Historical phase sections that clearly say historical are not defects.

## Missing Artifacts

No unsupported claim that current selected-category tests or source/visual evidence are absent: replacement controls and indexed target frames exist. The missing deliverable is a truthful, runnable current qualification contract for the old host/VM folder tools (F-03), or an explicit historical-only retirement with canonical pointers to current tools. Literal source searches, proximate commit history and adjacent tools are listed in03. No separate build-vs-adopt register was found by `rg --files | rg -i 'build.vs.adopt|adoption.register'` (rc1); that optional gate is not invented here.

## Verified findings and withdrawn inference

### F-01 — Reconcile current tracker bodies with completed integration/build state

**Severity:** Medium. **Category:** Spec Drift. **Owner area:** M7 tracking and source/build handoff.
**Primary evidence:** inputs/issues/510.json full body; AC-510-06FAIL and AC-515-02PARTIAL; current product integration e6645/ES4e410, closed children and retired source-overlay packet. inputs/issues/497.json latest current paragraph versus primary accepted185/187terminal receipts; AC-497-04PARTIAL. All sibling criteria re-derived independently.
**Required change:** preserve clearly historical evidence, remove or label obsolete active directions, state current assembled-image/public adoption gates, and reconcile checked/unchecked criteria only from primary artifacts. Re-read each complete body after writing. Root's corrected M7/checkpoint is already safe; do not undo it.

### F-02 — Withdrawn: no public-publication requirement in #504

The primary initially inferred that the retained-path criterion required public raw publication. Complete body readback explicitly says retained local evidence, not an already-published commit. The inference was wrong. No corrective issue/body edit is warranted; private custody remains correct. AC-504-04is UNTESTABLE because its private source-reading commands/outputs were not inspected. See inputs/post-forward-regrades.json and02's appended correction. This withdrawn item must not become a punch item.

### F-03 — Update or retire regression tools that call the removed implicit-seeding contract

**Severity:** Medium. **Category:** Test Gap. **Owner area:** cloud QA tooling.
**Primary evidence:** tools/pixelelated-cloud-folder-test:67/80/88and related calls expect no-category seeding; cloud_setup:785–786requires explicit categories. Fresh one-case command in checks/retrospective-controls01/commands.json exits1; raw output says backendrc2, `Choose which cloud folders to create.`; four terminal channels1 and actual host owner exits retained. tools/pixelelated-cloud-folder-vm-test:131/138/146/150/153expects the same retired success contract; its overlay list110–125also predates the validator dependency. Both tools are advertised as current explicit-folder qualification helpers in canonical instruction-files.md.
**Required change:** either adapt positive/refusal cases and complete installed dependency overlay to the current explicit contract, or make historical scope explicit and route current qualification to the replacement. Negative cases must prove the intended guard rather than pass on missing arguments. Classify the historical migration sibling tools and keep their original receipts intact. Current validator30controls and adapted round-trip/scripts harness are not missing and must remain green. No unchanged full VM tool run was launched merely to rediscover its known invalid invocation.

### G-01 — Reject malformed receipt shapes without aborting the checker

**Severity:** Low. **Category:** Code Quality. **Owner area:** host audit-cadence tooling.
**Primary evidence:** tools/ceremony-check85–120and370; checks/blind-host-leads02/{probe.py,results.json,execution-receipt.json}. Valid receipt accepted; marker/evidence/tracker/completion list shapes raise AttributeError outside the caller's handled exception set. Host guard was directly exercised; this is its native target. Crashing fails closed, but loses the complete ceremony report. Require object shapes and produce the normal invalid-marker diagnostic; keep valid receipts and15existingcontrols green.

### G-02 — Preserve actionable path-refusal guidance

**Severity:** Medium. **Category:** Code Quality. **Owner area:** cloud setup ES/backend interface.
**Primary evidence:** ES GuiMenu.cpp6504–6534discards setter stdout and uses one generic path/connection message; cloud_setup473–474prints why an invalid component is refused and a correction. Primary viewed indexed English/French640rejected-path frames and English1280unreachable control. second-opinions/path-refusal-frame-verification.json independently binds all3hashes and proves the captured editor callback byte-identical to frozen4e410. The actual dot-dot refusal loses its specific guidance. Bucket guidance at530–543shares the discarded channel, but no new bucket runtime claim is made.
**Required change:** present a bounded safe localized reason and useful next action while retaining refusal/no-pointer-mutation semantics. Do not expose raw unsanitized provider stderr. Check blank, invalid path, provider refusal and connectivity variants with exact-source EN/FRsmall/large proof and current canonical flow. Canonical CF05requires explanation; no deliberate trade accepting the loss was found in retained archaeology. Existing frames are present and accurate; this finding corrects the earlier quality judgment, not their provenance.

## Risk Assessment

| Risk | Severity | Impact | Mitigation |
| --- | --- | --- | --- |
| F-01 stale active directions | Medium | Repeated work, wrong next dependency, misleading readiness | Full-body reconciliation against exact evidence |
| F-02 withdrawn | None | No defect; private custody is explicit | Preserve boundary; do not publish private inputs |
| F-03 obsolete QA entrypoints | Medium | False failures or irrelevant refusal passes; wasted VM cycle | Adapt or explicitly retire full sibling contract |
| G-01 malformed receipt shape | Low | Checker aborts and loses report; remains fail-closed | Explicit JSON shape rejection and negative controls |
| G-02 discarded refusal explanation | Medium | Player cannot identify the path correction | Safe localized reason and target frames |
| L-01 post-confirmation config race | Unverified lead | Possible folder/note creation at worker-time path after external edit | Target reproduction or expected-context binding; no runtime defect asserted |
| L-02 scan recipe comment | Low lead | Misleading source navigation | Correct explanatory comment during authorized remediation |

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)

| Finding | Existing rule | Uncovered? |
| --- | --- | --- |
| F-01 | issue-tracking.md § Ticking an acceptance criterion; milestone-phase-naming.md § Sources of truth | No |
| F-02 withdrawn | engineering-practices.md artifact-first rule caught an auditor inference; no product rule change | No |
| F-03 | engineering-practices.md § Verify the artifact, not the report / guards; generic-x64-vm-testing.md § One command for every check; blindspots57/65/71 | No |
| G-01 | engineering-practices.md failure controls; blindspots6/8 | No |
| G-02 | player-language.md clarity/next action; es-player-text.md outcomes; canonical CF05 | No |

### Codification Gaps (needs-new-rule)

No new uncovered pattern recurs across three confirmed findings. Do not add a new reminder rule for already-covered tracker/test drift. Recommended action sequence: reconcile the two current bodies; preserve the existing private custody wording; fix or explicitly retire stale host/VM tool contracts and update their canonical mapping. No instruction-file edits are made by this auditor.

## Tier B visual-QA consolidation

The changed setup/validator/creation flows and follow-up French busy reason, wrapped help and scoped empty-state copy have source-bound indexed happy-path and branch frames. Original clipped/wrong-scope frames remain rejected evidence; corrected640×480 English/French and1280frames were directly read. Native DuckStation capture includes actual default/custom launch capture and a generated640×480PNG. Historical frames reused for unchanged presentation remain labeled by their original source, not claimed as freshly captured on the final pin. CF10/current assembled firmware is still a tracked image gate; audit does not manufacture it from source overlays.

## Coverage Boundary

**Examined:**130independent criteria across30public issues; candidate16→frozen product/tool/rule deltas and ES source; source writer/filter/default interactions; retained target proof, build/owner/cleanup receipts; fresh finite host mechanics; prior eight-item audit disposition only after independent verdict completion.02contains per-criterion code-read/test-run/target-receipt detail.03maps every relevant rule and blindspot.

**Deliberately not examined:** ignored private operational inventory, credentials, full private cleanup member set, private personal-cloud bytes, excluded #505diagnostic draft, untouched upstream emulators. No new physical action, personal-cloud operation, full candidate16 rerun, firmware build or fresh guest was launched by the audit. Exact private facts remain UNTESTABLE/SKIP. Local rclone fixtures cannot prove hosted-provider timing or OAuth; native synthetic tests do not prove a commercial game is playable.

**Dimensions not exercised:** new post-confirmation race target reproduction; full current assembled-image upgrade/clean-install acceptance, CF10and physical release behavior; separate release five-seat council. Existing tracked gates are not waived. The primary model lab is known but exact served model slug is not exposed. External review is complete. OAuth token-only config refresh, missing unit protocol during delayed creation, unusual invalid-context/marker-write wording and UI-thread context timing remain unverified runtime leads. No private provider probe or new target action was substituted for those missing facts.

## Finding Verification (Phase 4.5)

No provisional Critical/High finding exists, so none requires a severity-triggered runtime reproduction. Medium/Low findings were still refuted against primary evidence:

| Finding | Severity | Survived refutation? | What was checked |
| --- | --- | --- | --- |
| F-01 | Medium | yes | Full bodies, comments and terminal/integration receipts; clearly historical sections distinguished from current active directions. Root's corrected M7 does not repair subordinate bodies. |
| F-02 | Withdrawn | no | Complete literal body states retained local evidence, not already published. The primary had invented a public requirement; no defect. Private artifacts remain uninspected. |
| F-03 | Medium | yes | Current tool header/canonical entry, actual fresh failure, backend explicit-category branch, current replacement tests and sibling VM/migration tools. No product failure alleged. |
| L-01 | lead | not established as defect | End-to-end callback/start/backend read inspected; last UI check covers ordinary stale page, backend snapshot covers mid-seed changes. Only external edit between those points remains unmeasured. |
| L-02 | lead | explanatory mismatch only | Actual parent-held flock is correct; package comment alone is stale. |

## Second opinion (Phase 4.6)

**Depth:** independent, two model perspectives (Codex/OpenAI primary; Anthropic external), one external reviewer, two sequential calls. Exact primary served variant is unknown. Both calls observed `anthropic/claude-fable-5.1` from the provider response, `xhigh` effort PASS, successful outcome, no retries and matching output digests. Full provenance: `second-opinions/claude-blind.md.provenance.json` and `second-opinions/claude-audit.md.provenance.json`. Native process exits and four zero return channels per call are retained in each watched owner's verified-completion.json. This is not a five-seat council.

Commands: `timeout 2400 tools/council/run invoke --member claude --provider openrouter --prompt-file <claude-blind-brief.md or claude-brief.md> --output <claude-blind.md or claude-audit.md> --no-retry`, launched through fresh watch-build-submit owners. The user's exact two-packet approval is retained in transfer-approval.json; refutation-assembly.json binds base+unchanged suffix+exact verified blind response, no added material. Previous untransmitted packets remain explicitly superseded.

## 2026-10-08T15:35Z — first blind dispositions

| Seat item | Primary grade | Primary artifact and scope |
| --- | --- | --- |
| Blind F-1 | confirmed; fold into F-03 | Frozen cloud_setup785–786, tools/pixelelated-cloud-folder-test and VM sibling; fresh retrospective-controls01 failure already read. Independent sibling-pointer expectation also stale. No player-runtime failure alleged. |
| Blind F-8 | confirmed, Low; G-01 | tools/ceremony-check85–120and370. Fresh checks/blind-host-leads02/probe.py and results.json: valid object accepted; marker/evidence/tracker/completion list shapes each raise uncaught AttributeError. Source digest unchanged. Existing15cadence controls do not cover these object-shape failures. Correct target is host Python, not VM. This is diagnostic/control robustness, not a fail-open approval bypass: crashing still returns failure. |
| Blind F-9 | disagree, with artifact, as a shipped translation defect | ES locale/CMakeLists.txt1–37generates POT with xgettext, merges PO and compiles MO on i18n ALL; stale checked-in POT and unused translation entries do not establish missing shipped text. GuiMenu5083–5096remaining setCompletedAction supplies PRESS ANY BUTTON TO RESTART, not removed CONTINUE. Whole-source call-site search found this sole production caller. Source cleanup alone optional, no defect finding. |
| Blind F-10 | agree, narrowed to pre-existing tracked scope | #519/#516already retain private alignment boundary; no new private read or action. Unpublished folder suppression is conservative noncreation, not adoption claim. Do not inflate punch list with already tracked owner-state work. |
| Blind F-12 | agree, re-graded to Medium tracker drift; fold F-01 | #510full frozen body contradicts actual e6645/ES4e410qualified integration and retirement; #497actual185/187receipts already independently read in02. #504fifth power criterion omitted deliberately from safe excerpt; original full public issue/criteria provenance exists and remains outside provider packet. No claim external reviewer verified omitted artifacts. Minor stale comments retained as comments, not runtime findings. |

Host probe custody: initial checks/blind-host-leads01 durable submission refused rc2 because the current refutation owner already owns the worktree; probe never ran. Retained refusal unchanged. The35ms host probe ran in fresh blind-host-leads02 as a finite foreground command with15s hard bound and direct completion receipt. No background watcher is claimed for it; no provider retry or in-flight tool edit.

Remaining blind F-2–7and11need full source/evidence grading. Refutation call remains active; no Phase5.

## 2026-10-08T15:44Z — remaining blind and refutation dispositions

Both approved calls verified: checks/fable-blind01/verified-completion.json and checks/fable-refutation01/verified-completion.json. All four channels0 per call; all24/31seals unchanged; actual recorded host processes absent. Provider-observed anthropic/claude-fable-5.1, xhigh PASS, successful outcomes, no retries, exact digests. Blind output17829bytes/3fc6ce05bca865c1f8be448e29d1634ba894bab15e620f6d3bf0a0ce6d149770; refutation19752bytes/c9d2fe15aae6e7397afe76df19e5f8851e93532e315292d6a45a1a305b12d428. Console content-unit counts are not file byte counts. Original packets and responses preserved unchanged.

| Seat item | Primary grade | Primary artifact and scope |
| --- | --- | --- |
| Blind F-2 / Refutation F-2 | could not verify runtime consequence; source lead L-03 | cloud_setup548–566and cloud_scan171–189hash full config bytes; cloud_folder_validate265–269rejects changed identity; prior candidate16 cloud_migrate_layout remote_fingerprint deliberately removes token. This corroborates mechanism. No expired-OAuth target run was done, no current private config was opened, and no real-provider failure is claimed. A synthetic token-only rewrite on an owned VM can test the identity boundary without personal cloud data. Existing ordinary selected-category controls do not prove this case; preserve it as explicit coverage gap, not PASS. |
| Blind F-3 / Refutation F-3 | agree, narrowed; G-02 Medium | ES GuiMenu6504–6534discards all setter stdout and displays one localized generic sentence. cloud_setup473–474supplies the concrete invalid-component explanation and correction;530–543bucket-specific advice is also discarded by this same branch, but bucket runtime was not newly tested. Actual retained EN640/FR640rejected-path frames display only generic path/connection advice. Primary viewed them and EN1280unreachable control; path-refusal-frame-verification.json proves3hashes and byte-identical callback at captured baeea2/1d5397/4e410and frozen4e410. Canonical CF05flow says explain refusal; player-language requires clear next action. No decision accepting loss of the reason found in bounded archaeology/history. This is lost actionable guidance, not permission bypass, path mutation on refusal, missing frames, or a claim every refusal needs raw provider text. Restore a safe bounded localized explanation; do not expose unsanitized provider stderr. |
| Blind F-4 / Refutation F-4 | disagree, with artifact, as a new selected-root discovery defect | D-CLOUD123explicitly retains parent existence witnesses for ambiguous provider not-found behavior; D-CLOUD178bounds category validation and prohibits cloud-wide absence inference. Frozen validator and restore are bounded; cloud_setup's older parent witness tests presence of the chosen name, does not discover/select/adopt alternate paths. No new account-wide absence or implicit adoption demonstrated. Source difference is real and named; do not silently widen the current specification into a prohibition of every parent metadata probe. |
| Blind F-5 / Refutation F-5 | could not verify running-screen defect; source lead L-04 | cloud_setup785–868emits no unit/doing; GuiMenu6989passes selected count; CloudTransferJob31/354–376and GuiCloudTransfer927–940clear the counter while item index0, show PREPARING. Primary viewed accepted create-failure and create-result frames: terminal failure is truthful and success advances to results; neither proves mid-run feedback/timing. D-UI026starts counting on the first unit announcement. No measured waiting defect/new runtime finding. A delayed synthetic create flow would settle it. |
| Blind F-6 / Refutation F-6 | agree, narrowed to unverified nonstandard failure variants; no new confirmed finding | Existing canonical CF12explicitly specifies generic unusable-result fallback; ordinary stale-page CF06correctly refuses and preserves state. Full invalid-context vs config-changed vs marker-write runtime variants are not individually demonstrated by the cited frames; source has these broad fallbacks. Do not infer all messages wrong from possible return paths. Track scope in coverage; G-02covers only independently proven path-setter reason loss. |
| Blind F-7 / Refutation F-7 | disagree, with artifact, as a supported-image defect | Missing cloud_scan guard indeed cannot continue into stamp-gated options. Frozen rclone package makeinstall installs required cloud_scan and actual installed-consumer check succeeded. This is fail-closed handling of incomplete unsupported composition, not a new failure on the qualified pinned image. Stale fallback comment is optional source hygiene, not a separate punch item. |
| Blind F-11 / Refutation F-11 | could not verify target timing; source lead L-05 | GuiMenu6866/6941/6962and4183–4190synchronously run bounded local context/stamp commands. No actual target timing/visible freeze was measured for these calls. Existing transition frames demonstrate navigation but cannot certify latency. A disposable guest timing control is sufficient first; no need to claim physical A53 necessity. |
| Refutation primary F-01 | confirmed; remains Medium F-01 | Full frozen issue bodies and actual product/terminal receipts independently verified in02; live full-body readback required during resolution to distinguish any later coordinator repair. |
| Refutation primary F-03 and extensions | confirmed; remains Medium F-03 | Both stale no-category seed calls and derived sibling-pointer expectations read directly. VM overlay110–125omits cloud_folder_validate; frozen cloud_setup650–653requires it for --content-location. Remediation must cover complete stale contract or retire entrypoints explicitly, not merely add seed arguments. |
| Refutation withdrawn primary F-02 / #504provenance | agree, narrowed to retained custody; no finding | Re-read exact inputs/issues/504.json checklist line32(power readbacks) and original criterion source. It was intentionally omitted from the safe packet's operational excerpt, not invented. Private data stays unopened; UNTESTABLEcustody criterion remains. |
| Refutation primary L-01 | could not verify runtime; unchanged lead | stillSelected checks before confirmation and at YES; detached worker then reads current paths. No exact-context parameter. Narrow external-edit window remains unmeasured and must be considered with token-stable identity L-03before any binding fix. |
| Refutation primary L-02 | confirmed explanatory mismatch only; fold into F-03documentation cleanup | rclone/package.mk84says no lock; actual cloud_scan355–359holds parent flock. Package install/lock mechanics are correct. Correct comment alongside QA contract cleanup; no separate runtime defect. |
| Refutation questioned ACs | disagree with blanket regrading; original effective scorecard retained | Literal AC51302concerns category meaning/selection; AC51402concerns empty-restore adjacent category advice. Path-setter explanation is a separate G-02gap, not evidence those corrections failed. AC50806frames really exist and match source; G-02corrects their quality assessment, not missing-frame provenance. AC48902requires malformed records not be counted; AttributeError fails closed but harms the checker report, giving G-01without inventing a fail-open requirement. OAuth/creation timing remain explicit not-exercised dimensions of broader criteria. |
| Blind consistent-traces section B / both coverage sections / refutation closing comparison | agree, narrowed to packet-only scope | No extra provider verdicts counted as primary evidence.02/03retain primary source/check/target receipts for the limited packet's unassessed areas. Omitted frames/manifest/private data do not become missing-publication defects; external prose cannot establish served identity. Facilitator provenance does. No fifth seat or council claim. |

Three-way result: primary F-01andF-03survive Medium; blind F-1/F-12fold into them. Add G-01Low host receipt robustness and G-02Medium actionable path-refusal guidance. F-02stays withdrawn. Runtime OAuth, create-progress and interface timing leads stay explicitly unverified; no newly confirmed High/Critical finding. No source mutation occurred during review.

## Quality Self-Check

| Item | Status |
| --- | --- |
| Scorecard present, IDs match02 | present; computed130rows and per-issue totals |
| Cornerstone conformance tables | present in03;30rules,74distinct blindspots |
| Coverage Boundary in02and04 | present |
| Finding Verification for all Critical/High | present; none provisional, all lower findings also refuted |
| Second opinion Phase4.6 | complete; two verified calls, all seat items graded against primary artifacts |
| Instruction File Recommendations | present; existing rules cover findings |
| Tier B consolidation | present, with source/overlay/assembled boundary |
| Defined verdict vocabulary | yes, original130entries preserved |
| Traceability / Evidence / Reproducible / Actionable / Complete | review dimensions checked; all four Phase 7 outcomes verified, with tracker and publication receipts retained separately |

## Phase 7 verified outcomes

The frozen findings above are unchanged. Tracker drift was corrected with exact whole-body readbacks; obsolete folder QA contracts now refuse current execution and name current coverage; actionable localized path refusals passed 44 exact-source EN/FR small/large outcomes before ES promotion; malformed audit receipt objects now produce normal diagnostics while preserving the rest of the report. The host fix passed 28 focused and 15 existing controls; the frozen negative failed 25 added controls. See `05-punch-list.md` and the four `resolution/PL-*/acceptance.json` records for direct source, process, tracker, remote and byte-identity verification. No audit finding is deferred. Existing image/release work and explicitly unverified runtime leads retain their stated boundaries.
