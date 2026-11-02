T41 Stage-D audit filing, authorized by #688 comment 6585065737. Parent work item #688; area epic #1054; milestone **M6: Codebase renovation**.

**One High finding (PL-001), routed to the base integration (#563/#559) through reactive bug #1408. All outcomes remain open.** No source fix or final slice acceptance is claimed; the lane stops at the Stage-D checkpoint for coordinator stream disposition.

## Accepted Stage-B executive summary (historical baseline)

All **120 complete patch applications over 106 patch paths succeeded** against the same cached pins: 43 applies, 48 applies with offset and 29 fuzz. Zero production candidates failed and zero successors were blocked. The deliberately failing fixture verifies that a partial candidate cannot advance the sequence. H700 011 remains the sole diagnostic disagreement: dry-run rc=1 but complete apply rc=0; the coordinator's D-WORKFLOW-222 resolves that method error without changing product source or discarding old receipts.

The 107-row provenance/coverage table is complete, including the SM8550 configuration and five non-kernel rows. Currency dispositions are **101 keep, 4 upstream-changed, 1 upstream-moved, 1 #585**. The known High source defect in both `0010-msm-resource-cleanup.patch` copies survives refutation: final patched SM8550 code writes through `cstate` before assignment. Upstream `9416eec2c2` supplies the fix; Stage D must file its bug and the integration owns landing it. Application success does not certify compilation, boot, runtime behavior or the rest of the 40,474 lines.

This is the complete Stage-B analysis, not final acceptance of #688. Stage C formal tool/reader-plan/lint work and Stage D issues/questions remain explicit. Local depth used one actual Codex reader and no reviewer or provider call.


## Accepted Stage-B criteria scorecard (historical baseline)

The following is the accepted source-audit assessment before C/D filing. Stage C is complete at `94b5b1c0b983313325dba101217761c6e5c9bca0`, including the formal actual-reader Local plan, generator and pre-issue lint; Stage D supplies this tracker, bug #1408, 06/07 and question readbacks. Remaining resolution/retro/final hand-back criteria are not ticked by this filing.

The exact current 28 criteria are retained in `stage-b/corrected/issue-688-body.txt`; 02 supplies criterion-level evidence and refutation. The scorecard includes future stages so no later obligation disappears at this checkpoint.

| ID | Criterion | Verdict | Evidence / remaining stage |
| --- | --- | --- | --- |
| AC-01 | Complete audit-folder contract | PARTIAL | 00–04 and both receipt generations present; 05, formal tools/ and second-opinions/ are Stage C/D work. |
| AC-02 | Artifact lint and Q1–Q7 contract | PARTIAL | Q1–Q7 written; pre-issue lint and punch index belong to C/D, resolution lint to F/H. |
| AC-03 | Actual Local reader and review plan | PARTIAL | Codex/OpenAI reader and historical Opus/Argon identities recorded; Stage-C formal plan not created early. |
| AC-04 | Punch issue outcomes and coordinator closure | PARTIAL | No Stage-D audit issue exists yet; no closure claimed. |
| AC-05 | Issue commit headers and protected-source/register guards | PARTIAL | Protected-source diff empty; reviewed-at/fixed-at issue fields remain for final hand-back. |
| AC-06 | Exact membership and both line totals | PASS | Accepted 99-line P1/seed receipts retained; rows and source bytes asserted again by table draft. |
| AC-07 | Stage-A Local positive/negative lint | PASS | Original lint-local-pass.out rc=0 and lint-local-fail.out rc=1 retained, not rerun. |
| AC-08 | 107 complete provenance rows and dispositions | PASS | Generated table below; no empty cells; five non-kernel rows identify T27/T11; dispositions total 107. |
| AC-09 | 107 exact coverage paths with escaped-name normalization | PASS | Coverage table generated from retained P1 rows; comparison decodes literal filename escape only. |
| AC-10 | Corrected 120-application packet and failure guard | PASS | 120 actual apply_rc=0, zero blocked; H700 011 dry_rc=1/apply_rc=0; failure fixture refuses promotion. |
| AC-11 | Generator three FAIL-first mutations then asserted tip output | PASS | drop/reach/header each rc=1 with distinct assertion, then all five modes rc=0; retained Stage-B draft, formal tools promotion later. |
| AC-12 | Ramoops node/config/upstream/pristine context | PASS | 38-line read, six numbered config lines, context at 108 instead of expected near 117, zero pristine ramoops. |
| AC-13 | Two #585 lines, including quoted regex, never sent | PASS | Both draft contributions below; five no-match output lines retained; no #585 write. |
| AC-14 | 0010 currency rows and filed bug | PARTIAL | Both upstream-changed; High source defect survives refutation; bug filing and its box-check belong to D. |
| AC-15 | Four configuration comparisons and method | PASS | 2609 / 3827 / 17 / 7-7 reproduced; helpers and oldconfig were read, not run. |
| AC-16 | 12 additions, move and four upstream changes | PASS | Exact name-status table below; 101 SAME/4 CHANGED/2 ABSENT, integration owns all changes. |
| AC-17 | Command/output/exit/time and hygiene evidence | PASS | Historical Stage-A producers retained; new per-command timings, full apply logs, positive hygiene controls in validation packet. |
| AC-18 | 31 leads and sixteen rulings | PASS | Each appears once in its indexed table below, with evidence and owner. |
| AC-19 | Renovation Q4 counts and Q3 bug numbers | PARTIAL | All currency counts and seven faces complete; Q3 bug number awaits Stage D. |
| AC-20 | Two maintainer questions posted at Stage D | PARTIAL | Exact questions drafted in 04; no premature question/approval relay. |
| AC-21 | All inherited leads by owner | PASS | Owner/line matrix below; no lane or integration source modified. |
| AC-22 | Bug/punch ladder and every take-up disposition | PARTIAL | Take-up reviewed in 01 and below; formal bug/punch outcomes belong to D/F. |
| AC-23 | Matching classified proof and running-log entries | PASS | Twelve classified proof records below, with twelve corresponding running-log lines. |
| AC-24 | Closing host-ledger no-write evidence | PARTIAL | No host action or write in command census; closing ledger delta check belongs to H, not repeated here. |
| AC-25 | Closing execution census and Stage-H scratch retirement | PARTIAL | Source-only Stage-B census complete; scratch intentionally retained until H. |
| AC-26 | Final retro and its posted timestamp | PARTIAL | 03 is the audit retrospective; final docs/retros artifact and post belong to G. |
| AC-27 | Branch and simulated-merge final checks | PARTIAL | Stage-B branch checks recorded; coordinator simulated merge and final resolution gates are later. |
| AC-28 | Single final hand-back and issue box-check | PARTIAL | This is the Stage-B checkpoint only, not final hand-back or issue acceptance. |

**Pass rate at Stage B:** 14/28 full-issue criteria fully met (50%); 14 PARTIAL, 0 FAIL. These are full-slice criteria, not a 50% Stage-B packet. Stage-B outputs 02/03/04 and the corrected packet are present; the partial rows name later C–H obligations.


## Acceptance criteria

- [ ] PL-001: `05-punch-list.md` and this issue record a verified Phase-7 outcome: the integration commit and two-copy source acceptance from bug #1408, or an explicit coordinator-recorded deferral to #1408 with owner and rationale; the machine-readable index and gate table agree, and `tools/box-check --issue <this audit>` reports 0 fail.

## Complete prioritized punch list

# Punch list — M6 T41 shipped kernel patches and configuration (#688)

**Stage:** D filing packet; outcomes remain open pending coordinator stream disposition. **Source:** 04 § Finding Verification, F-01 / L-01. **Total:** 1 finding (0 Critical, 1 High, 0 Medium, 0 Low). Local: Codex / GPT-6-Astra / xhigh; observed live footer, not provider-attested. Reactive bug: [#1408](https://github.com/pixelelated/distribution/issues/1408); audit issue assigned by this Stage-D filing.

This is a source-only table slice. The integration owns the carried upstream fix; T41 edits no patch, configuration, recipe or root tool. No Stage-E stream or final outcome is authorized by this draft. The twelve accepted proofs and all application receipts remain unchanged.

## PL-001 — Carry the upstream 0010 pointer-initialization fix into both kernel series

- **Question:** Q3 Bugs; currency relation Q4.
- **Severity:** High.
- **Category:** Code Quality.
- **Source finding:** F-01 / L-01; #688 criterion 14; 04 § Finding Verification.
- **Owner area:** `inherit:the integration` (#563/#559); T41 owns the trace and reactive bug filing only.
- **What:** Bring upstream `9416eec2c200ad969d9e421e686fc7cbfdaca36a` through the base integration so both carried copies initialize `cstate` before its first field write. Do not apply an isolated fix on this audit branch.
- **Where:** `projects/ROCKNIX/packages/linux/patches/7.0/0010-msm-resource-cleanup.patch:19` and `:37`; sibling `projects/ROCKNIX/packages/linux/patches/7.2/0010-msm-resource-cleanup.patch:19` and `:37`, unchanged at dispatch `d7dd766659` and accepted source `02aab33bd9842610b0d466c9c186454dc14373ee`.
- **Why:** The patch writes `cstate->num_mixers = 0` before assigning the local pointer. An enabled MSM DPU path can therefore write through an indeterminate pointer. Correct patch application is not code correctness; no observed crash is claimed.
- **Evidence / refutation:** Retained final patched SM8550 `dpu_crtc_assign_resources`, `stage-b/corrected/0010-final-function.txt`: declaration 1441, write 1453, first assignment 1470. The complete function has no earlier assignment; its error return does not initialize the successful path. SM8550 conf:4461 enables CONFIG_DRM_MSM; H700 and GENERIC_X64 do not enable it. Both carried patches are byte-identical. Upstream's message is “Previous version writes to field pointed by an uninitialized pointer.” The two-copy comparison with `651150fc88` is `2 files changed, 28 insertions(+), 22 deletions(-)`.
- **Reproduction probe (retained, not rerun):** Read the numbered complete function above and the two patch hunks; expected assignment before the first dereference, actual assignment after it. `git show 9416eec2c2` supplies the upstream correction. Normal application rc=0 is accepted separately under D-WORKFLOW-222 and does not refute this defect.
- **Acceptance:** The integration records its fixed-at and upstream base hashes; after that base merge, `git diff --stat <fixed-at> upstream/next -- projects/ROCKNIX/packages/linux/patches/7.0/0010-msm-resource-cleanup.patch projects/ROCKNIX/packages/linux/patches/7.2/0010-msm-resource-cleanup.patch` is empty, with the contemporaneous upstream/next hash recorded. A source trace of both fixed copies places the assignment before the write. The reactive bug names that evidence and passes `tools/box-check --issue <bug>` with 0 fail.
- **Enforcement ladder:** Detected by source/history review, confirmed by full-function refutation; upstream already fixed it. A bounded ordering assertion over the two resulting functions could hold the next source integration step; the recorded two-path diff proves uptake. No current mandatory guard is claimed, and **no tool can** turn the accepted application return codes into runtime correctness. The coordinator owns the next stream disposition.
- **Already written:** Image builds for H700, SM8550 and GENERIC_X64 using the fork's pre-fix source since the base consume these pre-fix patch bytes; this audit did not inspect built images or installed devices. The enabled affected driver is established here only for SM8550. The base merge changes future source/builds; already-installed images remain unchanged until their normal update. No storage schema, migration or cloud write is introduced by this source fix, and no existing device state was read or changed here.
- **Can this be done on the VM?** No — the tree, history and accepted touched-source artifact show this source defect; nothing a guest shows is a provenance fact. Physical runtime effects, builds and guests remain outside this lane's authorization.
- **Outcome:** Open, awaiting the coordinator's Stage-D stream disposition. Filing routed bug #1408 does not itself resolve or defer this punch item.

## Pre-existing tracked scope (not punch items; exempt from this Phase 7 gate)

- #563/#559 — the integration's broader base uptake, additions, move and configuration changes. PL-001 is the specific confirmed defect routed there, not a duplicate list of integration tasks.
- #585 — the two never-sent contribution drafts (ramoops distribution layer and upstream quoted-regex line); #369 remains parked. No post to those issues is authorized for T41.
- T11 / #1084 / #1099 — kernel/config/firmware context and duplicate policy; the three equal 7.0/7.2 pairs are question 1, not three additional bugs.
- T27 / T28 / #44 — U-Boot and device-specific configuration/disabled-patch context; T43 owns unshipped paths.
- #1049/#1056/#1086/#1101/#879/#1053 — inherited inventory/reach/tooling gaps. No new T41 application failure is established.
- Coordinator / #346 — kernel-patch directory rule erratum, tier/order interpretation and the two prepared Stage-D questions. The complete 31-lead owner matrix remains in 02. The lane neither files Backlog issues nor edits those owners' files.

## Phase 7 resolution gate

The Stage-D pause precedes resolution. Every item stays open until an explicit coordinator disposition; no checkbox is ticked merely because a bug exists.

| Item | Outcome | Evidence / next owner |
| --- | --- | --- |
| PL-001 | Open | Confirmed source trace above; reactive bug #1408, exact readback verified; the integration owns the fix and coordinator owns stream disposition. |

## Machine-readable index

```yaml
punch_index:

- id: PL-001
  question: Q3
  severity: High
  category: Code Quality
  source_finding: F-01 / L-01 / AC-14
  owner_area: "inherit:the integration (#563/#559)"
  where: "projects/ROCKNIX/packages/linux/patches/{7.0,7.2}/0010-msm-resource-cleanup.patch:19,37"
  acceptance: "Recorded base integration makes both patches equal to its named upstream base and places cstate assignment before its first write; reactive bug records trace and box-check 0 fail."
  ladder: "source/history detection; full-function refutation; next guard is bounded ordering assertion plus two-path base diff; no runtime correctness guard claimed"
  follow_up: "#1408"
  outcome: open
```


## Stage-D boundary

No outcome is selected here. The coordinator owns stream disposition and final issue closure. The two brief-mandated questions are posted on #688 and recorded in `07-questions-for-the-maintainer.md`; none authorizes a source/runtime/device/cloud action. `06-audit-summary.md` carries the Stage-D status and exact issue/parent/readback checks.

Primary: Codex / GPT-6-Astra / xhigh, `openai/gpt-6-astra`, lab `openai`; observed live Herdr footer, not provider-attested. Session `01a19d12-29e3-7fe0-9f41-038dac0a5deb`, T3 wN:p6. Local, empty reviewers; historical identities retained in review-plan.json.
