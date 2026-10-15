# Punch List — completed M7 handoff (#603)

**Punch-list tracker:** [#612](https://github.com/pixelelated/distribution/issues/612).

Generated2026-10-15. Source:04-analysis.md. Seven items:0 Critical,0 High,3 Medium,4 Low.

Independent review and all seven punch outcomes are complete; exact tracker/marker validation records closure. Product
findings remain tracked and must be fixed before an affected deployment/public RC.
D-WORKFLOW-168 permits a separately qualified owner-only H700 route; source selection
alone does not prove installed absence. Actual H700 payload/menu inspection and #606 proof pass; retained custom mappings still require inspection before handoff.

## PL-001: Preserve existing Steam registry

- **Severity:** Medium
- **Category:** Interaction Defect
- **Source Finding:** G-02
- **Owner area:** Steam installer
- **What:** Preserve an existing player registry and create the template only for a genuinely absent destination.
- **Where:** `projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh:2367`
- **Why:** Preserve player state, bounded work and truthful source/evidence claims.
- **Evidence:** See second-opinions/primary-verification.md and its exact-source/receipt packets. No new target runtime is implied.
- **Acceptance:** Exact VM full-caller fresh/retained/race controls preserve non-template bytes, modes and unrelated state.
- **Tracked work:** #607.

## PL-002: Verify durable client recovery after mount changes

- **Severity:** Medium
- **Category:** Test Gap
- **Source Finding:** G-01
- **Owner area:** Steam recovery
- **What:** Reproduce cross-boot/remount volatile-identity refusal and implement durable identity only if safely justified. Trigger remains unmeasured.
- **Where:** `projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh:1470`
- **Why:** Preserve player state, bounded work and truthful source/evidence claims.
- **Evidence:** See second-opinions/primary-verification.md and its exact-source/receipt packets. No new target runtime is implied.
- **Acceptance:** Original interruption/remount control plus repaired recovery and replaced/missing-storage negative controls; no weakened ownership guards.
- **Tracked work:** #608.

## PL-003: Bound repeated failed RVZ automatic hashing

- **Severity:** Medium
- **Category:** Interaction Defect
- **Source Finding:** G-11
- **Owner area:** Frontend achievements
- **What:** Stop unchanged permanent failures from causing a full automatic hash attempt at every eligible indexing start.
- **Where:** `es-app/src/GameCubeRvzHashRetry.h:16`
- **Why:** Preserve player state, bounded work and truthful source/evidence claims.
- **Evidence:** See second-opinions/primary-verification.md and its exact-source/receipt packets. No new target runtime is implied.
- **Acceptance:** VM failure classes, explicit retry/file-version change and existing valid ID/hash/queue preservation; installed frontend proof.
- **Tracked work:** #609.

## PL-004: Keep release metadata out of shell evaluation

- **Severity:** Low
- **Category:** Code Quality
- **Source Finding:** G-21
- **Owner area:** Steam metadata
- **What:** Replace eval-based data assignment with literal assignment while retaining downstream validation.
- **Where:** `projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh:240`
- **Why:** Preserve player state, bounded work and truthful source/evidence claims.
- **Evidence:** See second-opinions/primary-verification.md and its exact-source/receipt packets. No new target runtime is implied.
- **Acceptance:** Safe VM original/control cases preserve quotes and shell-like bytes without executing them; normal metadata works.
- **Tracked work:** #610.

## PL-005: Bind RetroArch exit saving to a current process

- **Severity:** Low
- **Category:** Missing Artifact
- **Source Finding:** AC-53 refutation
- **Owner area:** VM save proof
- **What:** Run one focused current disposable VM proof for the missing exit-auto-state process/stat link; preserve prior evidence.
- **Where:** `docs/audits/2026_10_15-milestone-603-completed-handoff/02-forward-audit.md:813`
- **Why:** Preserve player state, bounded work and truthful source/evidence claims.
- **Evidence:** See second-opinions/primary-verification.md and its exact-source/receipt packets. No new target runtime is implied.
- **Acceptance:** Exact image/core/frontend and process/wait/file records plus numbered/auto manager frames; no survivors and compact evidence before disk retirement.
- **Tracked work:** #606.

## PL-006: Correct preservation and evidence precision

- **Severity:** Low
- **Category:** Documentation Gap
- **Source Finding:** G-06/G-14..20/G-25..27/G-29
- **Owner area:** Audit records
- **What:** Withdraw whole-installer/no-defect generalizations; retain exact source/receipt boundaries and supplied bindings.
- **Where:** `docs/audits/2026_10_15-milestone-603-completed-handoff/04-analysis.md`
- **Why:** Preserve player state, bounded work and truthful source/evidence claims.
- **Evidence:** See second-opinions/primary-verification.md and its exact-source/receipt packets. No new target runtime is implied.
- **Acceptance:** Independent packet hashes, explicit criterion caveats, corrected arithmetic and pre-issue/resolution artifact lint; scoped record commit.
- **Tracked work:** #603.

## PL-007: Clarify safe retained-stage recovery

- **Severity:** Low
- **Category:** Improvement
- **Source Finding:** G-04/G-28
- **Owner area:** Recovery guidance
- **What:** Document intentional Dolphin/Proton refusal and safe inspection/recovery without assuming leftover-name ownership.
- **Where:** `docs/es-menu-map.md:379`
- **Why:** Preserve player state, bounded work and truthful source/evidence claims.
- **Evidence:** See second-opinions/primary-verification.md and its exact-source/receipt packets. No new target runtime is implied.
- **Acceptance:** Guidance names exact states and preservation; any UI copy change carries updated flow/frames; no blanket deletion or website gate.
- **Tracked work:** #611.

## Pre-existing tracked scope (not punch items; exempt from Phase7)

- #563/#344: native ARM Steam/FEX payload, real-link adequacy and first-launch lifecycle; G-03/G-22/G-23/G-24 do not turn synthetic proof into native readiness.
- #528: remaining public source/licence dispositions, delivery/retrieval/backup custody; separate from private testing.
- #511/#605: website/disclosure work, separate lane and no private/public firmware gate added by this audit.
- #558/#561: existing physical shutdown/LED observations; no new diagnosis from this review.

## Phase 7 resolution gate

| Item | Outcome | Evidence / reason |
| --- | --- | --- |
| PL-001 | Deferred | #607; owner M7 integrator; P2/M7.P5 before affected deployment/public RC. Requires a packaged full-caller preservation change and fresh/retained/race VM controls, then affected firmware binding. The exact current H700 SYSTEM contains no Steam installer; this is deferred from the H700-only audit closeout to the affected Steam deployment work, not waived. |
| PL-002 | Deferred | #608; owner M7 integrator; P2/M7.P5 before affected deployment/public RC. Requires a reboot/remount recovery experiment and safe durable-identity change with replaced/missing-storage controls, then affected firmware proof. H700 has no Steam installer. The risk is source-confirmed but its reboot trigger remains unmeasured; it is not relabelled fixed. |
| PL-003 | Deferred | #609; owner M7 integrator; P2/M7.P5 before affected deployment/public RC. Requires frontend retry-state design, VM failure/file-version/explicit-retry controls and a newly pinned frontend. The current H700 shipped menu has no GameCube system. Private H700 handoff additionally requires checking retained custom system mappings; this finding remains a gate if a GameCube mapping exists. Affected GameCube-capable deployments and public RC stay blocked on the fix. |
| PL-004 | Deferred | #610; owner M7 integrator; P2/M7.P5 before affected deployment/public RC. Requires a product script change and target-shell full-caller negative controls, grouped with the Steam preservation repair before affected firmware qualification. H700 has no Steam installer, so this is outside the private H700 path; shell injection or quoting correctness is not waived. |
| PL-005 | Resolved | #606; evidence commit `cd894172871ee1655986c8c7045342b219601b14`. Exact branch containment/path log and current077197/ES16dbac save/process/wait/frame proof verified; retained-originals reader0 accepts behavior while producer03 remains1, marker stat unobserved and prior failures retained. All owners gone and media retired after compact custody. |
| PL-006 | Resolved | Record commit `236d59e2109a7157e676b97f74e72f8046021987`; branch containment and exact path log verified in checks/phase7-record-resolution/. Primary packet hashes, current criterion caveats and66/1 arithmetic are retained. Final resolution lint remains part of the whole-audit closeout, not a new runtime claim. |
| PL-007 | Deferred | #611; owner M7 integrator; P3/backlog before related recovery UI change. Intentionally refused unknown retained state remains protected. Clearer recovery guidance is a separate documentation/UI task, with flow/frames required for any screen change; no unsafe automatic deletion is introduced for audit closure. |

## Machine-readable index

```yaml
punch_index:
- id: PL-001
  severity: Medium
  category: Interaction Defect
  source_finding: "G-02"
  owner_area: "Steam installer"
  where: "projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh:2367"
  acceptance: "Exact VM full-caller fresh/retained/race controls preserve non-template bytes, modes and unrelated state."
  outcome: deferred
- id: PL-002
  severity: Medium
  category: Test Gap
  source_finding: "G-01"
  owner_area: "Steam recovery"
  where: "projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh:1470"
  acceptance: "Original interruption/remount control plus repaired recovery and replaced/missing-storage negative controls; no weakened ownership guards."
  outcome: deferred
- id: PL-003
  severity: Medium
  category: Interaction Defect
  source_finding: "G-11"
  owner_area: "Frontend achievements"
  where: "es-app/src/GameCubeRvzHashRetry.h:16"
  acceptance: "VM failure classes, explicit retry/file-version change and existing valid ID/hash/queue preservation; installed frontend proof."
  outcome: deferred
- id: PL-004
  severity: Low
  category: Code Quality
  source_finding: "G-21"
  owner_area: "Steam metadata"
  where: "projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh:240"
  acceptance: "Safe VM original/control cases preserve quotes and shell-like bytes without executing them; normal metadata works."
  outcome: deferred
- id: PL-005
  severity: Low
  category: Missing Artifact
  source_finding: "AC-53 refutation"
  owner_area: "VM save proof"
  where: "docs/audits/2026_10_15-milestone-603-completed-handoff/02-forward-audit.md:813"
  acceptance: "Exact image/core/frontend and process/wait/file records plus numbered/auto manager frames; no survivors and compact evidence before disk retirement."
  outcome: resolved
- id: PL-006
  severity: Low
  category: Documentation Gap
  source_finding: "G-06/G-14..20/G-25..27/G-29"
  owner_area: "Audit records"
  where: "docs/audits/2026_10_15-milestone-603-completed-handoff/04-analysis.md"
  acceptance: "Independent packet hashes, explicit criterion caveats, corrected arithmetic and pre-issue/resolution artifact lint; scoped record commit."
  outcome: resolved
- id: PL-007
  severity: Low
  category: Improvement
  source_finding: "G-04/G-28"
  owner_area: "Recovery guidance"
  where: "docs/es-menu-map.md:379"
  acceptance: "Guidance names exact states and preservation; any UI copy change carries updated flow/frames; no blanket deletion or website gate."
  outcome: deferred
```
