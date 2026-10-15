# Audit Analysis — completed M7 handoff (#603)

**Date:** 2026-10-15. **Scope:** Milestone / Independent. **Primary:** OpenAI Codex, exact served model ID not exposed; identity source is developer instruction. **Frozen record:** cdd92f10605517e789e09d13b6f4ba68573c2617. **Products:** VM/H700 f8636de1d105275dbf9420bbabbbc26f79abb10f; SM9aa7affee9d4ad5e69725cab20b6d7ad84d93dea; ES16dbac5211eea7e70db7394372033be2be7df829; website6aac689c6feaa8d4afefbd5a8b2121e5206f14b9.

**Status:** Primary Phases1–4.5 complete. Phase4.6 pending exact packet transfer authorization and both verified Facilitator calls. This audit is not complete; no Phase5/punch-list or completion marker is issued.

## Executive Summary

The primary review independently evaluated67 literal criteria across15 completed issues, reading source, original command results, artifact identities, retained failures and representative exact-source frames before opening prior per-criterion verdicts. All67 are supported within their stated scopes. AC08 initially lacked a retained original lint result; a new root-allocated host lint on exact source returned0 and is recorded as a current check, not a recovered historical result.

No new confirmed product defect survived primary review. The previous audit's frozen scores and six resolved findings are unchanged. Later evidence supports the present handoff: exact ABL/header acceptance, PPSSPP parser discrimination, final installed clean/retained behavior, native state continuation and published compatible-restore guidance. The historical #196 raw manual launch/stat transcript was not located; surviving before/after frames, accepted ledger and current launcher controls are explicitly separated. External independent review remains mandatory and pending; this is not RC/publication approval.

## Acceptance Criteria Scorecard

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
| AC-53 | #575 | PASS | source + originals/pixels; inherited RetroArch transcript limitation |
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

**Pass rate:** 67/67 criteria fully met (100%) within their literal contracts. These counts are computed, not copied from the prior audit.

## Code Quality Assessment

Strengths: bounded staged replacement, identity-bound recovery, explicit refusal of unknown retained state, process-owned Wi-Fi work, and exact installed/artifact provenance. Negative controls distinguish actual child failures from wrapper success. Complexity hotspots are Install Steam.sh's embedded transaction code, the RVZ container reader and lifetime interactions in GuiWifi/WifiScanProcess. Coverage limits do not disappear because a suite passes.

## Cornerstone Conformance

Overall HIGH within scope;03-retrospective.md records all30 canonical rule faces,74 blindspot entries (including duplicate-number29) and8 cross-system interactions. Single new host lint was explicitly allocated. No device/cloud/provider action, product edit, build or source-custody sweep occurred in this lane.

## Spec Fidelity

Aligned: all67 literal criteria, same-model restore, known-state preservation, explicit standalone capability limits, and synthetic/installed/native separation. No new standalone integration, physical boot/radio, real account award or universal format claim is introduced. The changed historical verdicts are later evidence/source resolutions; no original failure is rewritten.

## Missing Artifacts

Historical #600 pkgcheck receipt was not retained in the inspected packet; fresh current check remedies present verification without fabricating history. Historical #196 raw manual launch/stat output was not located by the bounded search; exact-source frames and accepted ledger remain. Independent Fable output/provenance does not yet exist and is a completion prerequisite, not an omitted test to call PASS.

## Risk Assessment

| Risk | Severity | Impact | Mitigation / status |
| --- | --- | --- | --- |
| Native ARM/client safety inferred from portable Steam fixtures | Medium if scope broadened | Unsupported release claim | Explicit exclusions; real inspected archive is structural only, execution denied. No such expansion made. |
| Old wrapper failures relabelled by later success | Medium if records collapsed | False evidence chain | Failed owners/statuses and unknown waits retained beside fresh readers; source identities exact. |
| Historical RetroArch manual proof lacks original process/stat transcript | Low evidence limitation | Cannot independently re-derive every old byte/time assertion | Original manager frames and current launcher controls retained; no new runtime assertion, no observed regression. External reviewer asked to challenge sufficiency. |
| Primary-only audit mistaken for independent completion | Completion blocker | Missing other-lab challenge | Phase4.6 fails closed; exact packets need separate transfer authorization. |

## Coverage Boundary

Examined: all67 criteria, current product/tool code at named frozen sources, compact original VM/host/firmware/publication records, selected process/file manifests, raw negative controls, current official metadata snapshots, and representative actual pixels. AC08 alone ran anew: host pkgcheck0, no compile/network. Every other runtime result is an original readback with its own source and timestamp.

Deliberately not examined: entire inherited distribution, bulk firmware caches, open #528 corresponding-source collectors, owner ROMs/accounts/cloud, physical radio/boot/power, universal game/format corpus and concurrent native ARM Steam/FEX/Proton gameplay. Selected storage preservation does not cover every arbitrary file or adjacent backup. No new benchmarks/VM/replays were performed. Historical #196 ledger assertions are not raw launch/stat receipts. External text reviewer will receive no image pixels unless separately authorized; primary visual reads remain identified.

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

Primary OpenAI/Codex; exact model ID unknown. Depth Independent:2 perspectives,1 external reviewer,2 planned calls (blind then refutation). Selected installed recipe: anthropic/claude-fable-5.1 via OpenRouter, effort xhigh. Existing Facilitator only. At packet preparation, no provider call or transfer had occurred. Exact review-plan and sanitized packet manifests are prepared in `second-opinions/`. The sealed blind prompt is 790,371 bytes (SHA-256 `3da1c2290b787fc113a3bb5809ce11fd7acfe68b7bb717bc404d6203c9350345`); the fixed refutation base is 922,168 bytes (SHA-256 `80450a6e6249f9b34e0a7cb6740dd268ea1b4bbbcc99b35077c0641e4d7ccdcc`). The final second prompt may append only the verified sanitized blind answer under the requested 131,072-byte bound; its digest is not invented before the answer exists. `packet-verification.json` records successful static content/hash/sanitization checks. The owner subsequently directed completion of #603; authorization.json records the unchanged two-call scope. The first call started at21:14:18UTC under root supervision. Its verified result and the subsequent refutation remain outstanding at this continuation checkpoint. Both served-identity/provenance/output-digest checks and primary verification of every external lead are required before Phase5. A formal five-seat council is not part of this audit.

## Quality Self-Check

| Item | Status |
| --- | --- |
| Scorecard IDs match02/criteria |67 unique IDs, computed; AC08 amendment separate |
| Conformance tables |03 includes rules/blindspots/interactions |
| Coverage boundary |Present02 and04; actual source/run limits explicit |
| Critical/High verification |No such fresh finding; false-positive attacks recorded |
| Second opinion |Pending authorization and two verified calls; completion fails closed |
| Instruction recommendations |Present; existing rule sufficient |
| Tier B consolidation |Present; exact-source pixels distinguished from reports |
| Verdict vocabulary |PASS/PARTIAL historical amendment; no invented runtime result |
| Traceability/evidence/reproducibility |Primary paths/member names/source hashes retained; supplementary custody and packet manifest bind bytes |
| Actionable/complete |Primary phases complete; no Phase5 before independent review |
