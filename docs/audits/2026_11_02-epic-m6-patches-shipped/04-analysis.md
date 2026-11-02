# T42 analysis — patches shipped outside the kernel table

Primary reader: Codex / GPT-6-Astra / xhigh, OpenAI. Reviewed-at `9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1`; Local D-WORKFLOW-184/225. Stage D is a review packet, not final slice acceptance.

## Executive summary

One confirmed Medium defect: PPSSPP's selected 007 patch adds a nested patch file instead of changing SDLJoystick.cpp (F-T42-01 / PL-01). No Critical or High finding is established. No product change is made. The native provenance and coverage tables each have exactly 384 keys; the separate inherited table has 50 keys / 26 overrides. All twelve fork-written patches / 498 lines were read in full.

| Native application classification | Paths |
| --- | --- |
| applies | 151 |
| offset | 38 |
| fuzz | 22 |
| open-item | 173 |
| **Total** | **384** |

These counts take each path's worst per-plan result, not the number of tool invocations. The 542 package/plan groups include context siblings; they are not the coverage denominator. A source projection applying is not a code-correctness or runtime PASS.

| Inherited conclusion | Keys |
| --- | --- |
| already-carried, with the exact current-pin intent stated | 21 |
| not-applicable-with-reason | 7 |
| unresolved-with-specific-evidence-needed | 22 |
| **Total** | **50** |

## Acceptance-criteria scorecard

Numbers match brief v2 and #689's twenty final criteria. No final issue checkbox is ticked by this packet. Stage D records, issue readbacks and checks complete the named D portions; E–H and coordinator integration are deliberately pending.

| Criterion | Stage D evidence / limit |
| --- | --- |
| 1 | 00–07, A–D receipts, audit-local tools and one-file Local plan; no build/guest artifact. |
| 2 | stage-a source/seed summaries, comparison.out and identity hashes: 384 / 71,387 logical lines. |
| 3 | 02 native Provenance/Coverage and tables.json; exact-key/field/receipt assertions. |
| 4 | 02 Fork-written reading, full 1–N ranges for twelve / 498, including Dolphin. |
| 5 | Four mode/literal/referent bindings; T43 referent only context; other slice ownership explicit. |
| 6 | 50 frozen keys / 26 overrides; 24 exclusions retained, not recounted. |
| 7 | Individual inherited decisions and source/pair/hunk evidence; 22 specific unresolved inputs with owner actions. |
| 8 | Fixed upstream/base patch identities plus recipe-currency.json literal pin assignments/includes; no live-ref or external-URL claim. |
| 9 | Application/group/archive receipts, projection hashes, rendering, stdout/stderr, normal rc; explicit gaps and fail/non-promotion fixture. |
| 10 | Four fail-first assertions then positive table validation; independent population sums. |
| 11 | This Q1–Q7 face, 03 conformance/interactions/refutation, classified proofs in running log. |
| 12 | Actual primary, OpenAI, reviewers [], D-WORKFLOW-184; no external review. |
| 13 | Pre-issue lint belongs to C/D; Phase-7 disposition and final resolution lint remain E/F. |
| 14 | One reactive bug with source trace, Already written, VM rationale and observable acceptance; issue readback/checks in D. Bug remains open. |
| 15 | Protected-path tree/commit guards and planted source-edit failure; no product/rule/ledger change. |
| 16 | Per-row owner/action; #585 drafts only; class removal #1048/#346. |
| 17 | Per-group source-only process census; scratch retained; no allocation or build/config/fetch action. |
| 18 | Final D check receipts and normal commit/push records; check outputs are written only after process exit. |
| 19 | Final retro and final accepted hand-back remain G/H; D summary is not a substitute. |
| 20 | Immutable reviewed-at preserved; source-preserving D tip published for disposition. Final fixed-at/integration acceptance remains coordinator-owned. |

## Risk assessment

F-T42-01 is a silent intended-change failure: the outer patch can succeed while the intended guide-button source change never occurs. Severity Medium reflects incorrect intended input behavior without a demonstrated data-loss/security impact. The current input mapping and any runtime symptom have not been measured here. Unknown application inputs are coverage limits, not invented product bugs. Fuzz/offset results warrant owner review before later pin changes; they are not runtime failures.

## Coverage boundary

384 native paths / 71,387 logical Git-blob lines; 71,378 newline bytes; 380 regular files and four symlinks; 379 shipped/five test. Resolving each selected link yields a different 71,477-line quantity. Full line reading is claimed only for twelve fork-written members / 498 lines. Native dispositions: 199 keep, 172 open-item, four #585 drafts, seven upstream-changed, one upstream-moved, one bug. Fixed upstream path identity: 307 same, 24 changed, 52 absent, one identical blob elsewhere; fixed base: 372 same, eleven absent, one changed. Whole path absence does not prove feature removal.

Application copies contain only required target members from a validated cached archive, plus patch-created files. Whole-component correctness, configured compiler behavior, binary integration, image upgrades, runtime efficiency, real controller behavior, provider or device facts are outside this source-only packet. Unknown dynamic/conditional pins remain explicit even when raw pin assignments are retained. No shell configuration/recipe, package build, external web/provider review or fetch was executed.

## Renovation face

### Q1 — Modernization

02 records target interfaces, current recipe pins and why the recorded intent is still carried. Modern compiler/header fixes, cross-compilation paths, lifecycle cleanup and device policies are distinct purposes. woff2 adds explicit cstdint includes; FEX excludes rebased system headers from guest thunks; shaderc avoids clobbering the prepared dependency tree. Newer pins are not sufficient proof of supersession. The inherited source/hunk/pair comparisons retain the exact version-specific question, including libsndfile's still-two-dot CMake range and changed FFmpeg request API series.

### Q2 — Standards and attribution

Literal mail headers and last path commits are preserved separately from source identity. 235 native identities have no From header; a missing mail header is not itself an attribution violation or a legal verdict. Existing upstream credits remain unchanged. Header dates, authors and URLs are recorded claims; no external integration verification or legal opinion is offered. The fabricated-attribution negative control checks literal header identity, not trust in the claimed author.

### Q3 — Defects

F-T42-01 follows outer patch lines 11–16, nested SDL payload 17–29, recipe hook source and unpack 191–196 to a created inert patch. The constructed fixture reproduces normal success with unchanged sentinel source. Fixed upstream has a direct source diff with a different desired key code; it supplies a comparison, not authorization to replace the seed. PL-01 is the single new reactive defect. No “missing counterpart” bug is invented for an unresolved inherited row.

### Q4 — Currency

All 384 native paths compare to fixed 651150fc88 and fixed base c445081a59518f37d9776e5412dd7b14910696f7. Recipe assignments/includes at all three refs are retained in recipe-currency.json; static resolved per-plan inputs stay in selection.json. Busybox/util-linux upstream additions resolve through their symlinks to exact generic changed-line counterparts; util-linux gettext remains its separate I45 question. Systemd's three intent comparisons stay separate and #1104 owns their design collision. External component-upstream claims are unverified. No “latest release” claim is made.

### Q5 — Efficiency

Source-visible cost changes include SDL display-mode frees, Mesa executable-heap and empty virgl-cache teardown, and Dolphin achievement-manager lifecycle. Qualified SDL/Mesa source context supports their stated cleanup paths; cached Dolphin ScopeGuard::Exit clears the finalizer, so explicit Exit does not invoke shutdown again at destruction. Historical launch-memory and image-delta evidence retains its original pins and limits. **No new boot, memory, player-step, runtime-efficiency or either time-to-play measurement exists.** Runtime owners must qualify any such claim in their own allocated scope.

### Q6 — Dead ends and reach

Native membership uses the residual P1 selector after explicit owners. Reach is a survey fact, not an executed plan. Four symlinks retain both path and referent identity; MangoHud's SM8750 source remains T43. No source is removed. #1048/#346 own class removal, and existing #1056/#1071/#1072 own adjacent selection/provenance work. The PPSSPP nested target is reachable by patch application but inert as source transformation; the sibling scan distinguishes the one product hit from 23 historical patch-record hits.

### Q7 — Clarity and structure

The separate tables expose literal provenance, exact recipe/context, application limits and remaining owner actions. Generic filenames or a single Subject in an aggregate patch cannot substitute for source reading. Inherited glibc, FFmpeg, BlueZ and systemd questions remain individual rows. Draft contribution text retains ownership and requires focused upstream qualification before submission. A future nested-target guard should examine product patch targets and explicit intentional exceptions, not reject audit product-diff files.

## Second opinion

Local, one actual reader: Codex / GPT-6-Astra / xhigh (OpenAI), own wN:p7 footer, session 01a19d12-3d7a-7642-9108-ae06a719cdd7. reviewers: []. D-WORKFLOW-184 permits Local at this epic tier. The sole second-opinions/review-plan.json and A's real validator controls record that contract. No council, provider call, external reviewer or independent second perspective is claimed. Earlier T38 identity/results remain historical.

## Quality self-check

First observations preceded prior-verdict reading. Counts are machine-asserted against frozen keys, while conclusions name their evidence and limitations. The four corrupted-data controls each fail their named assertion before the positive dataset passes. The separate protected-path guard must reject both working-tree and committed fixture edits before accepting this branch. Receipt validation checks recorded output hashes and equivalent diagnostic input projections. Assertions do not prove a complete semantic audit of vendor code. The brief's final resolution/integration requirements remain pending at D, and the one product bug remains open.
