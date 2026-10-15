# Audit Analysis — completed M7 handoff (#603)

**Punch-list tracker:** [#612](https://github.com/pixelelated/distribution/issues/612).

**Date:** 2026-10-15. **Scope:** Milestone / Independent. **Primary:** OpenAI Codex, exact served model ID not exposed; identity source is developer instruction. **Frozen record:** cdd92f10605517e789e09d13b6f4ba68573c2617. **Products:** VM/H700 f8636de1d105275dbf9420bbabbbc26f79abb10f; SM9aa7affee9d4ad5e69725cab20b6d7ad84d93dea; ES16dbac5211eea7e70db7394372033be2be7df829; website6aac689c6feaa8d4afefbd5a8b2121e5206f14b9.

**Status:** Phases1–6 complete, including both verified Fable calls and mandatory tracker#612. Seven punch items are graded; Phase7 reconciliation and focused #606 proof remain active. No audit-completion marker exists.

## Executive Summary

The independent review covers67 literal criteria across15 completed issues. Current
score is66 PASS and1 PARTIAL: AC-53 retains accepted Dolphin/Flycast and RetroArch
subclaims, but the historical RetroArch exit-auto-state process/stat binding is
missing. #606 supplies one focused current VM proof. Initial67/67 wording is
superseded; no old failure or prior audit score is rewritten.

Both Fable5.1/xhigh calls completed successfully through the Facilitator with
verified identity, provenance, output hashes and original result channels. Seven
punch items cover registry preservation, durable Steam recovery, repeated failed
RVZ indexing, shell metadata assignment, RetroArch evidence, record precision
and recovery guidance. No Critical/High finding was confirmed. Current-source
and original-receipt grading resolves the packet omissions without rerunning
accepted suites. Known product fixes retain affected-device/public RC gates;
private H700 applicability is established separately under D-WORKFLOW-168.

## Acceptance-criteria scorecard

Full literal text, evidence and attempted refutation are in02-forward-audit.md and criteria.json. IDs were counted from the67 unique `### AC-NN:` entries; the AC08 amendment is not an extra criterion.

| ID | Issue | Current verdict | Verification depth |
| --- | --- | --- | --- |
| AC-01 | #602 | PASS | code + original execution/receipt readback |
| AC-02 | #602 | PASS | code + original execution/receipt readback |
| AC-03 | #602 | PASS | code + original execution/receipt readback |
| AC-04 | #602 | PASS | code + original execution/receipt readback |
| AC-05 | #602 | PASS | code + original execution/receipt readback |
| AC-06 | #600 | PASS | code + original execution/receipt readback |
| AC-07 | #600 | PASS | code + original execution/receipt readback |
| AC-08 | #600 | PASS | code + fresh allocated host lint0; historical gap retained |
| AC-09 | #600 | PASS | code + original execution/receipt readback |
| AC-10 | #600 | PASS | code + original execution/receipt readback |
| AC-11 | #599 | PASS | code + original execution/receipt readback |
| AC-12 | #599 | PASS | code + original execution/receipt readback |
| AC-13 | #599 | PASS | code + original execution/receipt readback |
| AC-14 | #599 | PASS | code + original execution/receipt readback |
| AC-15 | #599 | PASS | code + original execution/receipt readback |
| AC-16 | #591 | PASS | code + original execution/receipt readback |
| AC-17 | #591 | PASS | code + original execution/receipt readback |
| AC-18 | #591 | PASS | code + original execution/receipt readback |
| AC-19 | #591 | PASS | code + original execution/receipt readback |
| AC-20 | #589 | PASS | code + original execution/receipt readback |
| AC-21 | #589 | PASS | code + original execution/receipt readback |
| AC-22 | #589 | PASS | code + original execution/receipt readback |
| AC-23 | #589 | PASS | code + original execution/receipt readback |
| AC-24 | #584 | PASS | code + original execution/receipt readback |
| AC-25 | #584 | PASS | code + original execution/receipt readback |
| AC-26 | #584 | PASS | code + original execution/receipt readback |
| AC-27 | #584 | PASS | code + original execution/receipt readback |
| AC-28 | #584 | PASS | code + original execution/receipt readback |
| AC-29 | #582 | PASS | code + original execution/receipt readback |
| AC-30 | #582 | PASS | code + original execution/receipt readback |
| AC-31 | #582 | PASS | code + original execution/receipt readback |
| AC-32 | #582 | PASS | code + original execution/receipt readback |
| AC-33 | #582 | PASS | code + original execution/receipt readback |
| AC-34 | #581 | PASS | code + original execution/receipt readback |
| AC-35 | #581 | PASS | code + original execution/receipt readback |
| AC-36 | #581 | PASS | code + original execution/receipt readback |
| AC-37 | #581 | PASS | code + original execution/receipt readback |
| AC-38 | #580 | PASS | code + original execution/receipt readback |
| AC-39 | #580 | PASS | code + original execution/receipt readback |
| AC-40 | #580 | PASS | code + original execution/receipt readback |
| AC-41 | #580 | PASS | code + original execution/receipt readback |
| AC-42 | #579 | PASS | code + original execution/receipt readback |
| AC-43 | #579 | PASS | code + original execution/receipt readback |
| AC-44 | #579 | PASS | code + original execution/receipt readback |
| AC-45 | #579 | PASS | code + original execution/receipt readback |
| AC-46 | #577 | PASS | code + original execution/receipt readback + reviewed pixels |
| AC-47 | #577 | PASS | code + original execution/receipt readback + reviewed pixels |
| AC-48 | #577 | PASS | code + original execution/receipt readback + reviewed pixels |
| AC-49 | #577 | PASS | code + original execution/receipt readback + reviewed pixels |
| AC-50 | #577 | PASS | code + original execution/receipt readback + reviewed pixels |
| AC-51 | #577 | PASS | code + original execution/receipt readback + reviewed pixels |
| AC-52 | #575 | PASS | code + original execution/receipt readback |
| AC-53 | #575 | PARTIAL | source + originals/pixels; inherited RetroArch transcript limitation |
| AC-54 | #575 | PASS | code + original execution/receipt readback + reviewed pixels |
| AC-55 | #575 | PASS | code + original execution/receipt readback |
| AC-56 | #574 | PASS | code + original execution/receipt readback |
| AC-57 | #574 | PASS | code + original execution/receipt readback |
| AC-58 | #574 | PASS | code + original execution/receipt readback |
| AC-59 | #574 | PASS | code + original execution/receipt readback |
| AC-60 | #564 | PASS | code + original execution/receipt readback |
| AC-61 | #564 | PASS | code + original execution/receipt readback |
| AC-62 | #564 | PASS | code + original execution/receipt readback |
| AC-63 | #564 | PASS | code + original execution/receipt readback |
| AC-64 | #349 | PASS | code + original execution/receipt readback |
| AC-65 | #349 | PASS | code + original execution/receipt readback + reviewed pixels |
| AC-66 | #349 | PASS | code + original execution/receipt readback + reviewed pixels |
| AC-67 | #349 | PASS | code + original execution/receipt readback |

**Pass rate:** 66/67 criteria fully met (98.5%); one PARTIAL (AC-53). These counts are computed from the current scorecard, not copied from the prior audit.

## Code Quality Assessment

Strengths: bounded staged replacement, identity-bound recovery, explicit refusal of unknown retained state, process-owned Wi-Fi work, and exact installed/artifact provenance. Negative controls distinguish actual child failures from wrapper success. Complexity hotspots are Install Steam.sh's embedded transaction code, the RVZ container reader and lifetime interactions in GuiWifi/WifiScanProcess. Coverage limits do not disappear because a suite passes.

## Cornerstone Conformance

Overall HIGH within scope;03-retrospective.md records all30 canonical rule faces,74 blindspot entries (including duplicate-number29) and8 cross-system interactions. The primary review allocated one new host lint and performed no device/cloud action, product edit, build or source-custody sweep. The root continuation subsequently ran the two authorized Facilitator calls serially; their actual outputs and exits are retained below.

## Spec Fidelity

All67 literal criteria were evaluated;66 pass and AC-53 remains PARTIAL. Verified alignment includes same-model restore, the enumerated preservation scope, explicit standalone capability limits, and synthetic/installed/native separation. No new standalone integration, physical boot/radio, real account award or universal format claim is introduced. The changed historical verdicts are later evidence/source resolutions; no original failure is rewritten.

## Missing Artifacts

Historical #600 pkgcheck receipt was not retained in the inspected packet; fresh current check remedies present verification without fabricating history. Historical #196 raw manual launch/stat output was not located by the bounded search; exact-source frames and accepted ledger remain. Both verified Fable outputs/provenance now exist. The remaining RetroArch process/stat evidence is #606; it is not counted PASS.

## Risk Assessment

| Risk | Severity | Impact | Mitigation / status |
| --- | --- | --- | --- |
| Native ARM/client safety inferred from portable Steam fixtures | Medium if scope broadened | Unsupported release claim | Explicit exclusions; real inspected archive is structural only, execution denied. No such expansion made. |
| Old wrapper failures relabelled by later success | Medium if records collapsed | False evidence chain | Failed owners/statuses and unknown waits retained beside fresh readers; source identities exact. |
| Historical RetroArch manual proof lacks original process/stat transcript | Low evidence limitation | Cannot independently re-derive every old byte/time assertion | Original manager frames and current launcher controls retained; no new runtime assertion, no observed regression. The external challenge identified the missing causal proof; #606 now owns it. |
| Missing RetroArch exit-auto-state process binding | Low evidence gap | Overstated complete native-state proof | AC-53 PARTIAL; #606 focused current VM proof. |

## Coverage Boundary

Examined: all67 criteria, current product/tool code at named frozen sources, compact original VM/host/firmware/publication records, selected process/file manifests, raw negative controls, current official metadata snapshots, and representative actual pixels. AC08 alone ran anew: host pkgcheck0, no compile/network. Every other runtime result is an original readback with its own source and timestamp.

Deliberately not examined: entire inherited distribution, bulk firmware caches, open #528 corresponding-source collectors, owner ROMs/accounts/cloud, physical radio/boot/power, universal game/format corpus and concurrent native ARM Steam/FEX/Proton gameplay. Selected storage preservation does not cover every arbitrary file or adjacent backup. No new benchmarks/VM/replays were performed. Historical #196 ledger assertions are not raw launch/stat receipts. Neither external text-review packet included image pixels; primary visual reads remain identified.

## Tier B visual-QA consolidation

| Surface | Source/original evidence | Primary visual read / boundary |
| --- | --- | --- |
| Wi-Fi geometry/status/focus | a7dc/bb9e component EN/FR640/1280 matrix;16dbac candidate/final source binding | Initial/results/failure/empty/pending/scroll actual frames viewed; final lifecycle original identities read; no radio claim. |
| Native capability text | library-vm capability matrix, later French copy frames, final native02 | English final support dialog and French640/1280 global guidance viewed. |
| Native states/ordinary saves | native03 + native02 actual installed sources | Wii changed/restore timer, Flycast native cold matching scene, cold score164 and Wii continued scene viewed; Wii top-row warnings limit pixel witness. |
| Restore offered/disabled | replacement19 a0f/ESc8dc original frame index | Paired640 model/date and foreign-disabled pixels viewed; current source and unchanged scripts verify continuity. |
| Retained frame matcher | original78 pairs and exact claim/mask identities | Selected carousel/cloud pairs viewed; matcher controls prove coverage; no claim all78 manually re-reviewed. |
| RetroArch inherited manager | RC11 66bfd/ES137309b7d frame originals | Before/after numbered/auto tiles viewed; no newly recovered raw manual process transcript. |

## Finding Verification (Phase4.5)

No new Critical or High finding exists. Refutation covered misleading baseline cleanup, wrapper0 versus child failure, generic ABL bypass, PPSSPP credential false negatives, copied-artifact agreement, synthetic engine versus actual NoGUI, state presence versus visible restoration, and scope changes after prior completion. The initial AC08 evidence shortfall was narrowed to missing historical lint custody, then independently resolved for current verification by original-zero lint. These are recorded in02, not erased.

## Instruction File Recommendations

No new mandatory rule is proposed: existing “verify the artifact” and retained-original requirements already address the observed custody limitations. Retaining stdout/stderr/exit/source hash for even short recipe lint is the concrete lesson captured in this audit's current check. Root owns any shared work-log entry.

## Second opinion (Phase4.6)

Independent depth: OpenAI/Codex primary plus Anthropic Fable5.1/xhigh through
OpenRouter/Facilitator, blind then refutation. Both served identities were
provider-observed, both effort checks PASS, no retries, all original result
channels0. Blind13649bytes/SHA097db216f847d83b0a1fb9be82f72aa50355937c08251e3b48a807ee428a0fd6;
refutation22673bytes/SHA2bbc57474fe0ce041fcd966d2fec31034831201eaa11a67dc3e291f54840464f.
The exact original authorized prompts remain unchanged. Provenance and original
invocation records are retained; all recorded process identities were observed
absent. No five-seat council, additional transfer or model substitution occurred.

Every external lead is graded in second-opinions/primary-verification.md, backed
by checks/lead-verification/. See05-punch-list.md for the seven actionable items
and pre-existing scope. The later ZeroTier delta remains separately reviewed,
outside these frozen external packets. No public or device authorization follows.

## Quality Self-Check

| Item | Status |
| --- | --- |
| Scorecard IDs match02/criteria |67 unique IDs, computed; AC08 amendment separate |
| Conformance tables |03 includes rules/blindspots/interactions |
| Coverage boundary |Present02 and04; actual source/run limits explicit |
| Critical/High verification |No such fresh finding; false-positive attacks recorded |
| Second opinion |Two verified completed calls; every lead graded |
| Instruction recommendations |Present; existing rule sufficient |
| Tier B consolidation |Present; exact-source pixels distinguished from reports |
| Verdict vocabulary |PASS/PARTIAL historical amendment; no invented runtime result |
| Traceability/evidence/reproducibility |Primary paths/member names/source hashes retained; supplementary custody and packet manifest bind bytes |
| Actionable/complete |Seven scoped punch items; Phase7 and #606 still active |

### Evidence precision after refutation

AC-10 distinguishes assembled image/artifact acceptance from original producer1.
AC-37/49/51 installed proof retains f863 producer-reporting qualificationfalse
and unknown launcher wait. AC-49 proves bounded joined-worker/group disappearance;
it does not claim every clean grandchild numeric wait status. AC-27/56 combine
source binding, controlled positive routing and separately scoped installed proof,
not a new live positive socket observation. AC-30/31/33 preserve the enumerated
transaction scope, excluding registry replacement. AC-62 recovery manifests/logs
prove rollback before the intentionally failed next download; retry exits remain1.
