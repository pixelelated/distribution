# Punch list — M6 T41 shipped kernel patches and configuration (#688)

**Stage:** D filing packet; outcomes remain open pending coordinator stream disposition. **Source:** 04 § Finding Verification, F-01 / L-01. **Total:** 1 finding (0 Critical, 1 High, 0 Medium, 0 Low). Local: Codex / GPT-6-Astra / xhigh; observed live footer, not provider-attested. Reactive bug: [#1408](https://github.com/pixelelated/distribution/issues/1408); audit issue: [#1409](https://github.com/pixelelated/distribution/issues/1409), an M6 sub-issue of #688.

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

## Disposition of the analysis concerns

| Analysis item | Disposition at D |
| --- | --- |
| F-01 | Confirmed High source defect: PL-001, bug #1408, audit #1409; open for integration/coordinator disposition. |
| F-02 | Inherited duplicate-policy question, L-03/T11, posted as 6585346506; no source defect asserted solely because equal files are duplicated. |
| F-03 | Provenance limitation represented by explicit unknown/headerless cells and the carrying history; no new authorship claim or verified defect requiring a fix. |
| F-04 | Pre-existing coordinator/T4 rule erratum, L-09; owner matrix retained in 02, no duplicate T41 work item. |
| F-05 | Audit-method issue resolved by D-WORKFLOW-222 and accepted corrected receipts; original failures preserved/refuted, no product bug. |

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
