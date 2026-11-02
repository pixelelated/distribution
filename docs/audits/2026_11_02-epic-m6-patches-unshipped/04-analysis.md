# Audit analysis — T43 patches-unshipped

## Executive summary

The table covers432 vendor-carried native paths at seed601e4694f9726b2228d3571efdb5cfc061c6d442, sourceafdec2bf8b88135befcb7ec56efb3a7ea327bd73. All432 match the fixed fork base. At fixed upstream651150fc88a8ee40e3f8e69c6d36feb6b005bde5,334 paths are identical,39 changed and59 absent without an identical blob elsewhere. This is a bounded source table, not a328,516-line body review.

There are779 successful normal applications including context,600 over333 native paths. Native results are330 clean,199 offset and71 fuzz calls.75 of114 plans qualify;38 are open and one is configuration-only.93 native paths have at least one specific open input, including6 that also have positive consumers;87 are wholly open.12 config rows remain source-only. No new reactive bug was confirmed. One Low evidence-gap punch item carries the93 per-path owner actions; missing inputs do not block publication of this qualified table.

Existing High #1408 and Medium #1410 retain their source owners and fix boundaries. Application success is not correctness. Both interface→first-frame and exit→next-first-frame remain unmeasured and untouched.

## Acceptance-criteria scorecard

D-stage assessment of the20 live690 criteria; final E–H acceptance is not claimed.15 PASS,3 PARTIAL,2 SKIP (future dispatched stages);75% fully met at this boundary. D check receipts qualify the record predicates.

| ID | Verdict | Evidence / remaining boundary |
| --- | --- | --- |
| AC-01 | PASS | 00–07 and A–D packet; no build artifact |
| AC-02 | PASS | stage-a exact helper outputs and bindings |
| AC-03 | PASS | both tables432; stage-c/table-controls.json |
| AC-04 | PASS | stage-b/group-census.json |
| AC-05 | PASS | stage-b/links.json; disjoint helper selectors |
| AC-06 | PASS | stage-b/recipes.json and plans.json (31/114) |
| AC-07 | PASS | stage-b/configurations.json (12) |
| AC-08 | PASS | observations.json and upstream-kernel-context.json |
| AC-09 | PASS | 779 normal calls, 600 native; named limits; actual partial-failure control |
| AC-10 | PASS | four exact gzip inputs refused then positive432 accepted |
| AC-11 | PASS | this report,03 and matching PROOF index |
| AC-12 | PASS | own footer and one Local review-plan; zero external calls |
| AC-13 | PARTIAL | pre-issue gate PASS with issue1412; Phase7 remains Open pending disposition |
| AC-14 | PASS | zero new reactive bugs; inherited #1408/#1410 not duplicated; D issue checks |
| AC-15 | PASS | scope negative and tree guard; per-commit check at publication |
| AC-16 | PASS | existing owners retained; zero fork-written contribution set; no #585 submission |
| AC-17 | PARTIAL | D census retains owned projections; H retirement awaits disposition |
| AC-18 | PARTIAL | D record/publication checks are recorded; final post-disposition gate remains due |
| AC-19 | SKIP | Stage G and final H deliberately not dispatched yet |
| AC-20 | SKIP | root acceptance/integration and final source headers remain future work |

## Renovation face

### Q1 Modernization

The immutable comparison shows changed kernel pins/configs and patch sets. RK3566/RK3576/S922X source7.2.11 is distinct from upstream's7.2.6 patch selector; RK3399 moves to6.18.54. Vendor RK3588 source and mali-bifrost module remain distinct. Existing #563/#559 integration owns uptake and polldev relocation. No source replacement is proposed from a filename or absent counterpart.

### Q2 Standards and provenance

Every row binds literal mode, Git blob, header claims, targets, source recipe and full selected pin.116 regular patches have no leading header; distribution-history backpointers cover all432 paths, but do not establish original authors. Preserve upstream credits and header uncertainty. Executable patch modes are recorded and never executed. Symlink identity is separate from referent content. No recipe edit means no package lint claim.

### Q3 Bugs

All779 complete normal calls returned0. This establishes application only, including offsets/fuzz. No newly confirmed product defect follows. Existing #1408 is specifically preserved despite successful applications, with source-byte equality to T41; #1410 is inherited T42 context. Unknown source, custom unpack/hook preimages and missing checksum inputs are open, not failed product behavior. No compiler, guest or installed artifact was inspected.

### Q4 Currency

The comparison is fixed local Git history, not a current web release check. Every table row records base equality and fixed-upstream identity;31 recipe contexts retain conditional pin assignments at both source and fixed upstream. Component release/absorption claims remain unverified.39 changed paths and59 absent paths require existing integration/recipe-owner review; none is silently deleted or called obsolete.

### Q5 Efficiency

Source cost is328,516 logical lines and10,690,267 literal bytes; the largest RK3588 Mali patch is125,129 lines. PipeWire buffer and kernel RAID6 source choices suggest possible runtime costs, but none was measured. No boot, memory or player-latency PASS. Both interface→first-frame and exit→next-first-frame are explicitly unmeasured. The audit changes neither quantity.

### Q6 Reachability

The432 keys are fixed inventory unshipped path rows.28 consumer combinations overlap across21 configurations. Static114 recipe/consumer plans preserve selected stack order and configuration precedence; they do not create a new build graph or a shipped-support decision. The shipped SM8550 MangoHud link reaches a T43 referent while staying owned by T42. #1101 owns unpack-edge limitations. Class removal remains #1048/#346, with no removal proposal.

### Q7 Clarity and structure

One native key remains one provenance and one coverage row; no deduplication loses an owned link or alias. Exact receipts and source history distinguish unknown origin, source-only configuration, successful application and unresolved input. PL-001 asks for explicit outcome custody for93 native input gaps, preserving owners and exact next evidence. No blanket source reformat or invented author attribution is requested.

## Code-quality assessment and spec fidelity

The source mechanisms are intentionally not modified. The audit-local tools fail on membership/kind/link/header drift, isolate source candidates, record failed-prefix behavior and protect all non-owned paths. Three initial limitations were made explicit: the slow static-selector producer was replaced after interruption, overlay inputs were qualified in a separate bounded pass, and the partial-failure check was strengthened before source use to share actual promotion logic. Original evidence is retained. The headerless-file lead was narrowed after history review; it is not a punch item.

## Cornerstone conformance and interactions

See03 for individually scoped doctrine, blindspot and interaction rows. Runtime/storage preservation is a boundary, not a newly proved device result. No external reviewer, council, provider or other-agent permission action occurred. The newer coordinator rules control over generic next-refresh prose.

## Risk assessment

| Risk | Severity | Mitigation |
| --- | --- | --- |
| Open source inputs promoted to application claims | Low evidence gap | PL-001 plus93 exact owner/action rows; no positive result without receipts |
| Fuzz/normal application mistaken for correctness | Evidence limitation | explicit105 total /71 native fuzz calls and40 native paths; no semantic or runtime verdict |
| Existing MSM uninitialized pointer | High, inherited #1408 | existing #563/#559 integration; no duplicate bug or source repair here |
| Shared shipped referent mistaken for unshipped-only bytes | Ownership limitation | two native links plus T42 consumer explicitly bound |

## Coverage boundary

Exhaustive mechanical facts:432 native keys/modes/hashes/line counts/header-target extraction,31 recipe contexts,114 selected plans and fixed-base/upstream identities. Primary reading covers grouped header/target evidence, static selector/recipe mechanisms, config writers, prior context and suspicious-origin/application limits. No vendor whole-body review, compilation, current release web check, generated config, benchmark, runtime correctness, physical fact or cloud state proof. Source projections live only under owned /workspace/tmp/m6-t43 roots; cache is read only. Stage-D custody retains them until authorized H retirement.

## Finding verification and self-refutation

PL-001 survives as an evidence gap because the actual cache directory/candidate checksum/hook records name missing inputs per plan.20 initially open overlay plans were qualified and removed from the final gap population, showing the gap test is not merely blanket absence. Six shared patches have mixed results, not contradictory path counts. Header absence does not survive as a product defect: known distribution history and explicit unknown original authorship suffice for this table. No Critical/High new finding remains to escalate; inherited #1408 stays High.

## Second opinion

Local under D-WORKFLOW-184 and plan section6c. Actual primary Codex / GPT-6-Astra / xhigh, OpenAI, identity from own visible Herdr footer. One perspective, reviewers[], zero external calls. stage-a/local-lint-capability.json proves accepted Local metadata and rejected reviewer-count mismatch. Stage-C source-bound negative inputs and own refutation are the checks; no independent-review claim.

## Missing artifacts and quality self-check

| Requirement | Status |
| --- | --- |
| 20-criterion scorecard and final-stage limits | Present |
| Source/coverage/config/recipe/link tables | Present with exact populations |
| Q1–Q7 and both unmeasured time-to-play quantities | Present |
| Conformance / interactions / refutation | Present in03 and this report |
| Critical/High new finding verification | None; inherited High remains cited |
| Local depth and actual identity | Present; no external review |
| Exact four negative inputs and source-path refusal | Present |
| Instruction recommendations | Existing rules suffice; no shared edit authorized |
| Tier-B visual artifacts | Not applicable: no interface change |
| Phase7 / final retro / H acceptance | Deliberately pending coordinator disposition |

Audit tracker: [#1412](https://github.com/pixelelated/distribution/issues/1412), M6 child of #690. Stage-D PL-001 remains Open.

Publication custody qualification: the one known public filename is escaped for storage in19 artifacts; see README.md and stage-d/transport-manifest.json for distinct raw/stored identities. All432 decoded keys,779 call records and original programs are preserved. New tampered/missing-payload refusals and positive restoration pass; the original hook refusal is retained. Coordinator clarification6589917275 permits records-only publication and grants no D acceptance or PL-001 disposition.

## 2026-11-02T23:02:10.852000+00:00 — S1 current outcome

PL-001 is **Resolved for outcome custody only**, S1 commit d4a25244a80c6459b22e044f6ae6d1e5dc946886. The exact93-key matrix and seven new refusals then positive are in stage-e/owner-outcomes.json and owner-outcome-controls.json. All93 source-input gaps remain open:87 wholly open/6 mixed, with188 open and36 retained positive consumer records and unchanged existing owners. No new source qualification, application or correctness is claimed. See [forward-audit outcome addendum](stage-e/02-outcome-addendum.md) alongside unchanged02. Authority is #690 comments6590563116 and6590591845; audit closure/marker and20criteria await root final acceptance. No new maintainer preference is required. Final F/G/H checks and retirement remain separate work.

## 2026-11-02T23:25:22.735364+00:00 — H actual result

Committed plan fb97dd53bd8e936ff7402888c70fb6bc25f7180d preceded mutation. Actual H retirement completed:881retired,8retained,0partial. Four empty prefixes were freshly rechecked and removed by nonrecursive rmdir; their historical ownership was not upgraded. The8retained roots hit the non-symlink guard and were not deleted. Retired-root absence, retained-root presence and durable publication roots were read back.21cache metadata records match before/after; no fresh cache content hash is claimed. Original process/serialization/citation failures remain alongside corrected results. All93source-input gaps remain open; PL-001 is custody-only Resolved. Final publication receipts and exact posted retro will bind the actual tip externally; root owns acceptance/marker/closure.

## Final agent-side readiness (root acceptance pending)

AC01–17 and19 have their required evidence within the recorded limits, including the preserved02/addendum, custody-only resolution, F gates and guarded881retired/8retained H census. The written final retro is committed; posting/readback is bound to the eventual actual published tip externally. AC18 has current normal gates; its final commit/push/remote/status/scan receipts must be observed outside that commit. AC20 source headers will bind seed/final on publication; root integration/acceptance and completion marker are not lane claims. All20 live criteria remain unchecked for root. The D scorecard above remains dated history, not a current claim that E–H was undispatched.
