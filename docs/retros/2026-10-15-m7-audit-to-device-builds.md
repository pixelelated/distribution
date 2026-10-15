# Mini-retro: M7 audit to device builds

**Reviewed:** 2026-10-15. **Boundary:** completed #590/#596 audit corrections,
#597 reporting recovery, and final installed/native qualification → #555 device
refresh. This closes a phase, not M7 or RC readiness. Product source is
`f8636de1d105275dbf9420bbabbbc26f79abb10f`, ES
`16dbac5211eea7e70db7394372033be2be7df829`; #597 tooling is
`26d2f6abce201692a8f0e4de851780129e483756`. Audit publication `dd38444c30`
and subsequent records `8478bb1565`/`dbc60c9828` change no product bytes.

The two available standalone phase retros are [October2](2026-10-02-cloud-runs-95-101.md)
and [October9](2026-10-09-owner-alignment-preparation.md). For additional continuity,
this review read the retrospective-summary sections of the
[October8 audit](../audits/2026_10_08-milestone-m7-p5-delta-507/03-retrospective.md#retrospective-summary),
[October11 network/cloud audit](../audits/2026_10_11-epic-m7-network-cloud-344/03-retrospective.md#retrospective-summary),
and [October11 post-review audit](../audits/2026_10_11-epic-553-post-review-344/03-retrospective.md#retrospective-summary).
Those three are audit retrospectives, not additional phase retros. Their recurring
lessons were fixture state, actual visible readiness, source identity, and preserving
publication boundaries.

## What worked well?

- The audit separated discovery from remediation. Its frozen115-criterion score
  remains **80 PASS / 16 PARTIAL / 16 SKIP / 3 FAIL / 0 UNTESTABLE**, while six
  findings have independently verified resolutions. Original failures remain
  evidence; later success did not rewrite them. The [final resolution table](../audits/2026_10_14-milestone-m7-next-candidate/05-punch-list.md#phase-7-resolution-gate)
  names each correction and its limits.
- Source review, the verified blind/refutation passes, and actual execution
  answered different questions. Dolphin lifecycle correction exposed a separate
  immutable resource-path defect; retained-session and Wi-Fi application-exit
  checks then found boundaries that earlier component tests had not established.
  The primary exact model remains unverified; no new reviewer was invoked here.
- Narrow continuations preserved expensive accepted work. Final clean and genuine
  retained-update evidence bound actual installed files, and four native launches
  established Wii manual rollback and Flycast manual/native-auto state behavior.
  The [native readback](../audits/2026_10_14-milestone-m7-next-candidate/native-state02-readback.md#observed-flows)
  distinguishes cold restoration before input from a screen that merely looks right.
- #597 preserved successful producer stages and a failed reporting channel
  separately. The reviewed recovery settled custody without manufacturing a
  launcher result; a separate reader verified109 installed mappings and raw/update
  equality. Neither operation converted the original submission into a qualified
  launcher success.

## What was harder than expected?

Several fixture assumptions survived source review and failed before the intended
assertion: an optional proc interface, a conditional NETWORK NAME row, a config
mount rejected by an existing save-path guard, and an omitted global Off setting.
The initial installed-launcher validator also compared raw source against packaged
bytes without the recipe's three substitutions; root caught that before execution.
These were proof-construction errors, not demonstrated product defects. The
[work-log entries at02:37,03:08,03:14 and04:32](../work-logs/2026_10-work_logs/2026_10_15-work_log.md)
and [installed-source review](../audits/2026_10_14-milestone-m7-next-candidate/affected-installed-source-review.md)
retain the actual failed branches and corrections.

The first Back measurement included fixed control-tool setup and took2.28499s,
failing the1s limit. The continuation moved connection setup before the clock,
then measured key send through a complete, byte-identical reviewed frame at
59.060466ms. It did not subtract elapsed time or relax the criterion. Final
installed clean/retained measurements were57.909324/57.258077ms.

Root also wrote `tool-wrapper.rc` while its launcher still owned exclusive
publication. The four build stages and runner returned0, but launcher reporting
failed with Errno17 and its final wait status is unknown. The [collision review](../audits/2026_10_14-milestone-m7-next-candidate/build-launcher-collision-review.md)
records that mistake, the68 isolated controls, actual nonqualifying recovery,
and the later reader's separate pre-admission tool-identity refusal125.

### Housekeeping and test scope

No runtime or full suite was replayed for this retro, as explicitly scoped by the
coordinator. The actual unfiltered `vm-qa` baseline on fac608 contains15 suite
rows:13 PASS, scripts FAIL and frame-diff FAIL. The original scripts seven
assertion failures and65 unclaimed frames remain in
[qualification-followups](../qa-logs/2026-10-15-qualification-followups/README.md).
The [same-image continuation](../qa-logs/2026-10-15-baseline-continuation/README.md)
ran the repaired scripts row and pending SFTP/S3 rows; the
[frame continuation](../qa-logs/2026-10-15-frame-claims/README.md)
retains its old-negative control,20 controls and78-frame comparison. These are
explicit continuations, not a new unfiltered f863 run. Final f863 proof is the
named affected installed/native scope. No failure is called pre-existing merely
from its filename or history.

Native01 remains a pre-launch failure with guest forced cleanup and incomplete
export, despite successful outer cleanup. Native02 excludes its mislabeled
selection and loading frames from acceptance. Observed native wait status remains
unknown; supervisor/runemu success is not substituted for it. These distinctions
are retained in the [native failure](../audits/2026_10_14-milestone-m7-next-candidate/native-state01-failure-readback.md)
and [successful readbacks](../audits/2026_10_14-milestone-m7-next-candidate/native-state02-readback.md).

## What did we discover?

The most useful checks crossed ownership boundaries: ES page versus application
lifetime, achievements helper versus actual launcher, Flycast native auto-state
versus the global frontend setting, and runner completion versus launcher reporting.
A helper's success or a generic250 exit did not prove the intended full flow.
Positive intended-helper logs, actual frames, original process results and exact
before/after identities made those claims reviewable.

The phase's acceptance criteria were reconciled inline against original issue
bodies and source-bound receipts; this was not delegated wholesale to the audit.
#590/#596 and #597 read back closed/completed. #593/#594/#595 retained closed
readbacks include all4/4/3 criteria checked. No criterion was silently retired by
a migration; the corrections retain the affected paths and make their failure
handling explicit.

| Criteria checked | Concrete implementation and acceptance |
| --- | --- |
| #590, all4 bullets | Frozen source/spec map, independent forward/interaction review, both verified Facilitator passes, and final artifacts/resolutions: [analysis](../audits/2026_10_14-milestone-m7-next-candidate/04-analysis.md#second-opinion-phase46), [final validation](../audits/2026_10_14-milestone-m7-next-candidate/phase7-final-validation.json), [closed tracker custody](../audits/2026_10_14-milestone-m7-next-candidate/checks/delivery/tracker-completion.json). |
| #596 PL-001/002 | `9aaaaa0f64`: Dolphin NoGUI lifecycle and bounded metadata requests; installed lifecycle and actual curl/Bash controls. [PL-001/002 rows](../audits/2026_10_14-milestone-m7-next-candidate/05-punch-list.md#phase-7-resolution-gate). |
| #596 PL-003 | `6616cc36cb`: immutable Sys alias, image resource hashes and installed startup evidence. [PL-003 row](../audits/2026_10_14-milestone-m7-next-candidate/05-punch-list.md#phase-7-resolution-gate). |
| #596 PL-004; #594 all4 | `d9054efc46`: atomic disabled-session publication, logged-out path, fail-closed launcher and reviewed EN/FR640/1280 refusal/return;15 controls plus final installed helper/exact launcher blocks with synthetic engine markers. [Full-flow readback](../audits/2026_10_14-milestone-m7-next-candidate/audit-ui1280-02-readback.md). |
| #596 PL-005; #593 all4 | ES16dbac, pin342eec66: baseline orphan, explicit/atexit/completed cancellation controls, actual Back/reopen and normal exit, then fresh/retained installed qualification. [Back/reopen readback](../audits/2026_10_14-milestone-m7-next-candidate/wifi-back-reopen-readback.md). SIGTERM/fatal exit remains outside the guarantee. |
| #596 PL-006; #595 all3 | `d9054efc46`: isolated Python invocation; installed-interpreter old-negative/new-positive synthetic transaction and unchanged final installed source binding. [Controls readback](../audits/2026_10_14-milestone-m7-next-candidate/source-controls02-readback.md). No ARM Steam execution claim. |
| #597, all5 bullets | `26d2f6abce`: exact collision evidence; guarded custody recovery;68 isolated positive/negative controls; independent review and actual consumption; separately reviewed109-row reader plus producer-ownership rule. [Implementation, actual recovery and reader sections](../audits/2026_10_14-milestone-m7-next-candidate/build-launcher-collision-review.md#reviewed-597-implementation-and-verifier). |

One remaining documentation gap emerged here: the live #344 body retrieved during
this retro still presents October11 image20/device results as the current route
and says no build is running. Those accepted historical results remain valid, but
the current handoff is #555's f863 refresh. Exact replacement text is prepared for
root; it preserves the release/publication criteria and historical evidence.

## What adjustments are needed?

1. **#555:** carry the completed audit/installed/native evidence as its prerequisite,
   then keep new H700 and SM8550 build/readback acceptance on their own original
   receipts. Bind the frozen checkout's ordinary admission tool, actual package
   substitutions and current generated inputs. The #597 recovery is restricted to
   its known producer; it is not a generic fallback for either device build.
2. **#344:** add this completion breadcrumb and current f863 handoff, label the
   October11 route historical, and replace its stale runtime sentence with a link
   to the live #555/milestone status. Keep #528 source/licence/custody, hardware,
   asset and publication gates open. VM qualification is not physical, real-account
   or native ARM Steam proof, and does not allocate an RC.
3. **#493/#597:** retain separate submission observations and producer receipts.
   Consumption releases a reservation, not held outputs or deletion authority.
   Reclaim only after the existing named dependency and compact evidence/source
   custody conditions are satisfied. No new recovery mechanism is requested.
4. **#585:** no further adjustment. The [published queue reconciliation](../upstream/2026-10-15-queue-reconciliation/README.md)
   already preserves focused contributions and D-WORKFLOW-165's submission gate.
   Queue maintenance does not claim an upstream submission.

### Scoped audit findings (Step2.5)

Delegation below is per check. Git readback at `dbc60c9828` found no changes since
`dd38444c30` to the sealed audit, rules, tools or product paths, and no product
changes since f863. Historical provisional rows are read together with the final
resolution supplements, never promoted as current unresolved defects.

| Check | Verdict and exact evidence |
| --- | --- |
| 1. AC conformance | PASS within the phase: inline table above covers4+6+5 parent/recovery bullets and4+4+3 correction bullets; original closed readbacks agree. #555/#344 remain open and are not claimed complete. |
| 2. Project principles | PASS scoped, delegated to [instruction conformance and invariants](../audits/2026_10_14-milestone-m7-next-candidate/03-retrospective.md#instruction-file-conformance) plus [final resolution](../audits/2026_10_14-milestone-m7-next-candidate/05-punch-list.md#phase-7-resolution-gate). Five sampled contracts: immutable packaged resources, preserved retained state, bounded child ownership, exact-source/UI binding, and producer-owned results; #597's delivered rule/tool supplies the last contract. |
| 3. Interactions | PASS scoped, delegated to [cross-system interactions](../audits/2026_10_14-milestone-m7-next-candidate/03-retrospective.md#cross-system-interactions), [fresh](../audits/2026_10_14-milestone-m7-next-candidate/final-clean-affected-readback.md), [retained](../audits/2026_10_14-milestone-m7-next-candidate/final-retained-affected-readback.md), and [native observed flows](../audits/2026_10_14-milestone-m7-next-candidate/native-state02-readback.md#observed-flows). Source-only, synthetic, installed and native claims stay distinct. |
| 4. Futro predictions | SKIP ratio: no separate prediction list for this audit/recovery phase was found in the phase issues or futro inventory. Earlier cloud/rename/swap futros are different scopes; no calibration percentage is invented. |
| 5. Housekeeping | PARTIAL by execution scope: original full15-row baseline and named continuations reviewed as described above; no full-suite replay or new all-green f863 aggregate. Physical/publication deferrals retain #555/#344/#528. |
| 6. UI review | PASS scoped, delegated to [640/1280 refusal readback](../audits/2026_10_14-milestone-m7-next-candidate/audit-ui1280-02-readback.md), [actual Back/reopen](../audits/2026_10_14-milestone-m7-next-candidate/wifi-back-reopen-readback.md), and [35 reviewed native frames](../audits/2026_10_14-milestone-m7-next-candidate/supplements/native-state02-result/frame-index.json). Disposable GENERIC_X64, explicit candidate overlays versus final installed source, and rejected frames are stated. Canonical [menu/flow map](../es-menu-map.md) links these proofs. |
| 7. Harness self-coverage | PASS scoped, delegated to [#597 implementation and actual recovery](../audits/2026_10_14-milestone-m7-next-candidate/build-launcher-collision-review.md#reviewed-597-implementation-and-verifier). Original68 controls cover the motivating collision and negative custody cases; ordinary consume remains unchanged. Corrected fixture/parser/measurement proofs remain narrow controls, not a universal fixture validator. |
| 8. Docs/glossary | PARTIAL pending propagation: canonical flow, recovery runbook and upstream queue match the completed changes; #344's stale current-status framing needs the prepared update. No new product noun or provisional-name policy is introduced. |
| 9. Build versus adopt | SKIP new architecture: bounded bug fixes and extension of existing admission tooling. Applicable upstream disposition is already recorded in #585/dbc60; no new build/adopt choice or submission. |
| 10. Decision propagation | PASS scoped for settled decisions: D-CLOUD-133 still excludes broad SIGTERM handling; D-INFRA-022 still governs held-output retirement; D-WORKFLOW-165 still governs upstream posting. None was reopened. Current-status propagation remains the explicit check8 action. |

### Practice adjustments and handoff

No additional rule or skill change is justified. October2/9 already identified
fixture-state and visible-readiness mistakes. Existing artifact-over-report,
source/intent and readiness rules cover the repeated review misses; this phase
made the checks concrete at the affected surfaces. The new producer-ownership
rule and narrow recovery tool already landed under #597 in
[device-builds](../../.claude/rules/device-builds.md) and the
[admission runbook](../../tools/host-maintenance/build-admission.md).

Root owns publication and tracker propagation. Prepared private text includes a
#344 body amendment, #555 completion breadcrumb/body addition, and a short
#493/#597 recovery-boundary note. At this review checkpoint those postings and
this retro's commit are **pending**, not claimed executed. No sealed audit,
product, runtime, compiler, cache or device was changed by this retro.

**Propagation completed:** Source9ad2f966fe was published on next before the
tracker links. #344's body and #555's additive handoff were read back exactly;
comments [#344](https://github.com/pixelelated/distribution/issues/344#issuecomment-6185470174),
[#555](https://github.com/pixelelated/distribution/issues/555#issuecomment-6185470595),
[#493](https://github.com/pixelelated/distribution/issues/493#issuecomment-6185470981)
and [#597](https://github.com/pixelelated/distribution/issues/597#issuecomment-6185471339)
match their prepared text. Check8's current-status propagation is now complete;
its original pending observation above remains historical. Compact exact custody:
[publication receipt](../qa-logs/2026-10-15-phase-retro/publication.json).
