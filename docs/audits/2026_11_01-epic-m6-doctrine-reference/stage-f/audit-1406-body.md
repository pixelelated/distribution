## Stage-F scoped outcomes — 2026-11-02T19:02:55Z

**15 Resolved, 22 Deferred, 9 Withdrawn.** Resolution means committed and source-verified in T39; integration and coordinator acceptance remain pending. Historical Stage-D statements below retain their date. Audit #1406 and reactive bugs #1400–#1405 remain open. No guest, build, physical/cloud action, host allocation or upstream submission occurred.

Artifact: `docs/audits/2026_11_01-epic-m6-doctrine-reference/stage-f/outcomes.json`. Five immutable source-stream commits passed candidate and committed harnesses; final source `de11515859d231a82a511c3867e12211190041a2` passes normal and withheld-findings runs, each 13/13. Exact source scope is 48 paths; 31 binaries/18 art files match the reviewed baseline. Owner dispositions D-WORKFLOW-223/-224 and later #1407 work remain separate.

---

# T39 Stage-D audit filing

**46 findings: 0 Critical, 0 High, 6 Medium, 40 Low.** Parent #686; area #807; milestone M6: Codebase renovation. Local depth under D-WORKFLOW-184; no reviewer or provider call.

## Executive summary

The accepted audit covers 254 paths: 223 text and 31 binary. Its generated coverage dispositions are 34 fix, 20 inherited, 50 ledger, 145 none, 2 #528 and 3 #585 (total 254); 18 art text rows are separately protected. These are path dispositions, not finding counts. PL-01–PL-46 retain the brief's L-01–L-46 numbering and accepted grades.

Six Medium statements misdirect readers: the unpublished release instructions, a settled decision called open, retired migration described as current, the flashing runbook's OS identity, unshipped backup menu labels, and an incomplete read mask. Historical statuses that still appear current are the common failure. Low findings include dated-document corrections and items routed to the coordinator or other owners. Conditional/unverified findings keep their status; no source fix or finding re-grade occurs at Stage D.

[Accepted artifact tree](https://github.com/pixelelated/distribution/blob/c61bcdcb5f2de47dfa35ac25776965e77f962914/docs/audits/2026_11_01-epic-m6-doctrine-reference) at `c61bcdcb5f2de47dfa35ac25776965e77f962914`; reviewed source `86ebb6dffc`; [Stage-C acceptance](https://github.com/pixelelated/distribution/issues/686#issuecomment-6582545265). A–C receipts are historical evidence, not new test results or resolution acceptance. All 46 items remain open until their eventual Phase-7 outcomes.

**Can this be done on the VM?** No -- the tree, the tool or the register shows it. Stage D files accepted evidence and validates records; no guest, build, physical/cloud action or runtime allocation.

## Acceptance-criteria scorecard for #686 at Stage D

| Criterion | Status / evidence boundary |
| --- | --- |
| 1 | Partial; 00–07 and stages A–D at this checkpoint; stage E is future work. |
| 2 | Accepted pre-issue lint at C; validate updated D records; resolution lint remains F. |
| 3 | Accepted Local plan and one-file second-opinions directory; append D identity only. |
| 4 | 46 open items; Stage-D issue checks precede checkpoint; outcomes remain F. |
| 5 | Final reviewed-at/fixed-at and removal proof remain H. |
| 6–8 | Accepted A membership, carve/order and Local proof receipts retained. |
| 9–10 | Accepted 254 coverage rows and 46 leads retained. |
| 11–13 | Accepted binary/art baseline and unchanged-source evidence retained; final comparisons remain F/H. |
| 14 | Accepted C checker receipts retained; no replay. |
| 15–17 | Accepted baseline and failure/refusal receipts retained; corrected-source results await E. |
| 18 | Accepted Q4/Q5/Q6 tables retained; both time-to-play numbers untouched. |
| 19 | Two Stage-D question comments with IDs/readback; historical draft retained with a dated update. |
| 20 | Pending E: fixes, commits and before/after receipts. |
| 21 | Inherited routing retained in 02; no posts to other owners' issues. |
| 22 | Six bug traces and 46 punch items; Stage-D issue receipts provide the new filing evidence. |
| 23 | Accepted 12 proof cells / 12 PROOF lines retained. D record checks use their own log, without rewriting these proofs. |
| 24 | No lane host-file write or runtime allocation; final hand-back census remains H. |
| 25–27 | Retro, final/simulated-merge checks and hand-back remain G/H. |

## Punch list

The checklist below retains each accepted item and its ownership/ladder. Its evidence is the matching lead in 02, finding verification in 04, and the retained A–C receipts. Corrected-source proof waits for the coordinator's stream brief and Stage E. The six bugs have independent reactive issues; they are neither milestone items nor sub-issues.

### PL-02: the front page sends a player to instructions attached to a release that does not exist

- [x] PL-02: The committed README describes the actual publication state and points only to existing instructions. The fix receipt includes the corrected sentence, its destination artifact or a contemporaneous release listing, and L-02's before/after check output.
  **Resolved** — README no longer promises attached instructions for an existing release; #344 remains the release-status authority. Commit `de40e931a469f6aa6889f08ec9d4d31266f4c6d4`; `stage-e/S1/focused-checks.out; stage-e/S1/result.json; stage-f/withheld-findings/harness.out`.
- **Severity:** Medium
- **Category:** Bug
- **Question:** Q3
- **Source Finding:** L-02 (`02` § The table)
- **Where:** `README.md:9`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix (ruling (c)); bug
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)'s `leads` step
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** The repository front page contains the misleading release pointer. This establishes exposure to readers, not a count of affected people.
- **Tracked:** #1400 (reactive bug); this audit

### PL-03: the device-testing policy calls D-QA-016 open

- [x] PL-03: The committed policy cites the settled register rows and no longer calls D-QA-016 open. The receipt includes the corrected sentence, the decided rows and the L-03 check output; existing per-action permission requirements remain intact.
  **Resolved** — D-QA-016 is described as decided on 2026-09-13. Existing per-action boundaries remain. Deferred rule counterpart: coordinator #346 must reconcile vm-first.md. Commit `de40e931a469f6aa6889f08ec9d4d31266f4c6d4`; `stage-e/S1/focused-checks.out; stage-e/S1/result.json; stage-f/withheld-findings/harness.out`.
- **Severity:** Medium
- **Category:** Bug
- **Question:** Q3
- **Source Finding:** L-03 (`02` § The table)
- **Where:** `docs/device-testing-policy.md:5`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix (ruling (l)); bug; `vm-first.md`'s sentence inherit:coordinator
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9) with a decided-row-called-open check
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** The misleading status is in the policy that AGENTS.md, CLAUDE.md and the relevant rule files direct testers to read.
- **Tracked:** #1401 (reactive bug); this audit

### PL-04: the retired cloud-folder migration script described as current

- [x] PL-04: Both committed documents state the retirement and cite D-CLOUD-175 without promising automatic migration. The receipt names the corrected passages and the retained-name classifications, with L-04 before/after output and the applicable retired-name check.
  **Resolved** — Both old migration documents carry historical/retired notices, D-CLOUD-175 and current selected-folder policy; original record text preserved. Commit `424eea28ecbfaa8fbbe49cdee6c99750becd13cf`; `stage-e/S2/focused-checks.out; stage-e/S2/result.json; stage-f/withheld-findings/harness.out`.
- **Severity:** Medium
- **Category:** Bug
- **Question:** Q3
- **Source Finding:** L-04 (`02` § The table)
- **Where:** `docs/rasteratops/cloud-layout.md:16`, `docs/releases/pr/08-saves.md:5`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix (ruling (l)); bug
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)'s `retired` step (it fails at the tip today)
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** The cloud-layout reference and the 08-saves PR description already carry the current-tense claim.
- **Tracked:** #1402 (reactive bug); this audit

### PL-05: the flashing runbook names the OS ROCKNIX throughout

- [x] PL-05: The fix receipt classifies all 21 original ROCKNIX lines against NAMING.md. Current fork OS references use pixelelated; retained paths, stored interfaces, upstream credits and historical names each have a reason. The committed runbook and L-05/identity check output establish the correction without a device operation.
  **Resolved** — All 21 original ROCKNIX lines classified; current OS prose corrected and all fenced command bytes unchanged. Commit `de40e931a469f6aa6889f08ec9d4d31266f4c6d4`; `stage-e/S1/focused-checks.out; stage-e/S1/result.json; stage-f/withheld-findings/harness.out`.
- **Severity:** Medium
- **Category:** Bug
- **Question:** Q3
- **Source Finding:** L-05 (`02` § The table)
- **Where:** `docs/device-flashing-runbook.md` (21 lines), at the dispatch tip `86ebb6dffc`
- **Disposition:** fix where NAMING.md decides the word; the rest classed
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)'s `identity` step with a ROCKNIX-as-the-OS class
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** The flashing runbook and the three entrypoint references already direct readers through the outdated identity.
- **Tracked:** #1403 (reactive bug); this audit

### PL-07: labels the pin does not ship, in banned words, in the public docs' stated source

- [x] PL-07: The committed reference uses labels and content tiers derived from the pinned ES source, with source path/line citations for each replacement. The receipt includes the obsolete-label before/after output and literal-to-source mapping; the three obsolete labels are absent from current instructions.
  **Resolved** — Four labels mapped to exact ES source at 16dbac5211eea7e70db7394372033be2be7df829; backup semantics/stored archive names retained. Commit `424eea28ecbfaa8fbbe49cdee6c99750becd13cf`; `stage-e/S2/focused-checks.out; stage-e/S2/result.json; stage-f/withheld-findings/harness.out`.
- **Severity:** Medium
- **Category:** Bug
- **Question:** Q3
- **Source Finding:** L-07 (`02` § The table)
- **Where:** `docs/backup-contents.md:3-4`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix (labels re-derived from the pin); bug
- **Ladder:** written; next rung: a label check against the ES pin (`es-menu-map-check`'s reach widened)
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** The repository backup reference and drafts sourced from it carry these labels. This audit does not establish that a public page was deployed with them.
- **Tracked:** #1404 (reactive bug); this audit

### PL-16: the read mask's long form lacks the flag form

- [x] PL-16: The committed policy mask includes the canonical rule's command-line flag coverage as well as assignment coverage. The fix receipt cites both expressions and the L-16 before/after check. Any later synthetic verification builds placeholders at runtime and records only redacted output; no real credential is read.
  **Resolved** — Canonical literal mask hides 24 synthetic values; assignment-only control leaks eight space-separated flags; benign text preserved. Commit `de40e931a469f6aa6889f08ec9d4d31266f4c6d4`; `stage-e/S1/focused-checks.out; stage-e/S1/result.json; stage-f/withheld-findings/harness.out; stage-e/S1/mask-fixture.out`.
- **Severity:** Medium
- **Category:** Bug
- **Question:** Q3
- **Source Finding:** L-16 (`02` § The table)
- **Where:** `docs/device-testing-policy.md:94`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix; bug
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)'s `leads` step
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** The incomplete mask is already written in the device-testing policy for readers to copy.
- **Tracked:** #1405 (reactive bug); this audit

### PL-01: the renovation's README and plan name P1's files and tools

- [x] PL-01: **Withdrawn** under the coordinator's v2 disposition: recorded design; accepted 15-name dispatch evidence Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** L-01 (`02` § The table)
- **Where:** `docs/reviews/README.md:10-12`, `plan-for-the-plan.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** ledger: resolved at dispatch (ruling (p)); the 15-name loop prints no MISSING
- **Ladder:** written; next rung: no tool can (a merge order)
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing: resolved before any reader acted
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-06: an M7 order of closed issues

- [x] PL-06: L-06's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Resolved** — The old order is dated 2026-10-08; the live M7 milestone supplies current order. Commit `895b90abcf44e62d3aa7339eba043cfe01e9b98e`; `stage-e/S3/focused-checks.out; stage-e/S3/result.json; stage-f/withheld-findings/harness.out`.
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q4
- **Source Finding:** L-06 (`02` § The table)
- **Where:** `docs/cloud-save-integrity.md:4`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9) with an issue-state check (Q4 (c))
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing traced
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-08: the map's journal calls closed #570 work pending

- [x] PL-08: L-08's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Resolved** — Journal remains in place, three status headings corrected, historical anchor aliases retained; canonical menu prefix unchanged. Commit `895b90abcf44e62d3aa7339eba043cfe01e9b98e`; `stage-e/S3/focused-checks.out; stage-e/S3/result.json; stage-f/withheld-findings/harness.out`.
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q4
- **Source Finding:** L-08 (`02` § The table)
- **Where:** `docs/es-menu-map.md:758`, `:806`, `:817`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix: the headings only (ruling (b)); the journal's home is § 4 question 1
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9) with an issue-state check
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** agents placing a row read it
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-09: a superseded baseline build named as the baseline

- [x] PL-09: L-09's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Resolved** — The exact 20261011 build remains the baseline of the dated October reconciliation. Commit `895b90abcf44e62d3aa7339eba043cfe01e9b98e`; `stage-e/S3/focused-checks.out; stage-e/S3/result.json; stage-f/withheld-findings/harness.out`.
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q4
- **Source Finding:** L-09 (`02` § The table)
- **Where:** `docs/releases/next-candidate-work.md:4`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix
- **Ladder:** written; next rung: no tool can (a baseline is a judgement)
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing traced
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-10: the player's cloud-folder guide ends in internal release status

- [x] PL-10: L-10's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Resolved** — Guide ends with player guidance; removed internal publication note retained in S2 audit evidence. Commit `424eea28ecbfaa8fbbe49cdee6c99750becd13cf`; `stage-e/S2/focused-checks.out; stage-e/S2/result.json; stage-f/withheld-findings/harness.out`.
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q7
- **Source Finding:** L-10 (`02` § The table)
- **Where:** `docs/pixelelated/cloud-folders.md:32-35`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** `README.md:22` sends players here
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-11: words and numbers run together

- [x] PL-11: L-11's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Resolved** — 223 bounded hits classified, 189 ordinary prose hits corrected, identifiers retained; only whitespace plus old-heading aliases changed. Deferred upstream README prose: #585; rc-accept.txt remains a historical ledger. Commit `a2d4a33d4aa310d78c1b5c23b5bcdcd93f8ffe89`; `stage-e/S4/focused-checks.out; stage-e/S4/result.json; stage-f/withheld-findings/harness.out`.
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q7
- **Source Finding:** L-11 (`02` § The table)
- **Where:** ten files (`02` § The table), at the dispatch tip `86ebb6dffc`
- **Disposition:** fix in the edit scope; `docs/upstream/README.md`'s share inherit:#585; `rc-accept.txt`'s ledger
- **Ladder:** written; next rung: no tool can (a heuristic, not a check)
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing traced
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-12: a counter note for a seat outside every run profile, no banner

- [x] PL-12: L-12's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Resolved** — Historical/retired-seat notice cites scaffold#915; original counter description and verified:false limits retained. Commit `895b90abcf44e62d3aa7339eba043cfe01e9b98e`; `stage-e/S3/focused-checks.out; stage-e/S3/result.json; stage-f/withheld-findings/harness.out`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q5
- **Source Finding:** L-12 (`02` § The table)
- **Where:** `docs/council-mistral-counter.md:3`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix: a banner; `council-limits.md` is § 4 question 2
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)'s `leads` step
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing traced
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-13: rocknix.org drafts naming pages without their repository

- [x] PL-13: L-13's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Resolved** — External repository named in three paths; the fourth already names it and was unchanged in S4. Commit `a2d4a33d4aa310d78c1b5c23b5bcdcd93f8ffe89`; `stage-e/S4/focused-checks.out; stage-e/S4/result.json; stage-f/withheld-findings/harness.out`.
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q6
- **Source Finding:** L-13 (`02` § The table)
- **Where:** four files (`02` § The table), at the dispatch tip `86ebb6dffc`
- **Disposition:** fix: the repository named beside each page
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)'s `paths` step (`external` class)
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing traced
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-14: the splash repository's wordmark tool, named with its repository

- [x] PL-14: **Withdrawn** under the coordinator's v2 disposition: splash repository already named; accepted X02 Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** L-14 (`02` § The table)
- **Where:** `docs/pixelelated/art/README.md:20-21`, at the dispatch tip `86ebb6dffc`
- **Disposition:** withdrawn as a defect: a Coverage `none` (X02)
- **Ladder:** written; next rung: held by the `paths`/`tools` steps' `external` class
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-15: the device facts point to a catalog with none of their cuts

- [x] PL-15: L-15's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Resolved** — Catalog generated scope stated; exact row Evidence links remain; S3 fact-table bytes unchanged, S4 spacing separately recorded. Deferred catalog/tool work: #964/#270; no catalog regeneration here. Commit `895b90abcf44e62d3aa7339eba043cfe01e9b98e`; `stage-e/S3/focused-checks.out; stage-e/S3/result.json; stage-f/withheld-findings/harness.out`.
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q4
- **Source Finding:** L-15 (`02` § The table)
- **Where:** `docs/releases/device-facts.md:7`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix the pointer without moving a cited row; inherit:#270 (the tool); inherit:coordinator (the catalog's regeneration, #964)
- **Ladder:** written; next rung: #270's device-facts check
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** #1100, #1126 and #1094 cite its rows
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-17: the wizard's IA against its decided rows

- [ ] PL-17: L-17's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #23 interface owners: unverified/conditional IA claim Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q4
- **Source Finding:** L-17 (`02` § The table)
- **Where:** `docs/conflict-wizard-ia.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix where a sentence contradicts a decided row and no screen change owns it; else inherit:the interface lanes ([unverified]: the reading is owed)
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** #23 still says rev 5
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-18: low-inbound reference documents presenting themselves as current

- [x] PL-18: L-18's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Resolved** — Exactly 33/2770 accepted rows tabled: 29 additive notices, three S2 notices reused, one ledger-plan unchanged. #1407 owns later review. Later compact index, nested monthly storage and individual purpose/replacement review: #1407. Commit `de11515859d231a82a511c3867e12211190041a2`; `stage-e/S5/focused-checks.out; stage-e/S5/result.json; stage-f/withheld-findings/harness.out; stage-e/S5/dispositions.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q5
- **Source Finding:** L-18 (`02` § The table)
- **Where:** the Q5 table's LOW-INBOUND set, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix: a dated first line where a record presents itself as current; retirement is § 4 question 2
- **Ladder:** written; next rung: the Q5 generator's inbound columns, promoted with the checker
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** search results that look current
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-19: the splash repository's tool in a historical artifact's README

- [x] PL-19: **Withdrawn** under the coordinator's v2 disposition: recorded design: dated historical evidence; no current instructions claim Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** L-19 (`02` § The table)
- **Where:** `docs/rasteratops/art/README.md:8`, at the dispatch tip `86ebb6dffc`
- **Disposition:** ledger (a historical artifact; X02)
- **Ladder:** written; next rung: held by the `external` class
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-20: `packages/rocknix` in dated P0 records

- [x] PL-20: **Withdrawn** under the coordinator's v2 disposition: recorded design: dated historical evidence; no current instructions claim Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** L-20 (`02` § The table)
- **Where:** `docs/rasteratops/p0-read.md:11`, `p0-sweep.md:39`, at the dispatch tip `86ebb6dffc`
- **Disposition:** ledger (a dated record)
- **Ladder:** written; next rung: held by the `paths` step's `historical` class
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-21: Rasteratops as the OS's identity in dated records

- [x] PL-21: **Withdrawn** under the coordinator's v2 disposition: recorded design: dated historical evidence; no current instructions claim Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** L-21 (`02` § The table)
- **Where:** `docs/rasteratops/raofflineproxy-refresh.md:180,188`, `cloud-folder-state-table.md:38`, at the dispatch tip `86ebb6dffc`
- **Disposition:** ledger (records of their date)
- **Ladder:** written; next rung: held by the `identity` step's `historical` class
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-22: a current plan says the site remotes still name the retired owner

- [ ] PL-22: L-22's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #511 current remote/checkout fact remains unestablished Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q4
- **Source Finding:** L-22 (`02` § The table)
- **Where:** `docs/pixelelated/site-plan.md:72`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix where it misstates the present; else inherit:#511
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)'s `identity` step
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing traced
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-23: `maxengel/rocknix` links resolving only by redirect

- [x] PL-23: **Withdrawn** under the coordinator's v2 disposition: recorded design: dated historical evidence; no current instructions claim Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** L-23 (`02` § The table)
- **Where:** `docs/cloud-sync-changelog.md:706-735`, at the dispatch tip `86ebb6dffc`
- **Disposition:** ledger (dated changelog entries)
- **Ladder:** written; next rung: held by the `identity` step
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-24: the one plan, superseded and unmarked

- [x] PL-24: **Withdrawn** under the coordinator's v2 disposition: historical ledger-plan; table-only; later review #1407 Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q1
- **Source Finding:** L-24 (`02` § The table)
- **Where:** `plans/conflict-resolution/vita-style-conflict-resolution.md:8-9`, at the dispatch tip `86ebb6dffc`
- **Disposition:** ledger: one historical-plan row naming the superseding row (ruling (d))
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-25: 0.0.1 called the first Rasteratops release in the RC ledger

- [ ] PL-25: L-25's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #346 coordinator: preserve exact inherited action in 02 Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** L-25 (`02` § The table)
- **Where:** `docs/releases/rc-accept.txt:13`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator (ruling (l))
- **Ladder:** written; next rung: held by the `identity` step's allow-inherited entry
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-26: two stale acceptances kept as the record

- [x] PL-26: **Withdrawn** under the coordinator's v2 disposition: recorded design: dated historical evidence; no current instructions claim Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-26 (`02` § The table)
- **Where:** `docs/releases/rc-accept.txt`, at the dispatch tip `86ebb6dffc`
- **Disposition:** ledger
- **Ladder:** written; next rung: `tools/rc-preflight`
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-27: the upstream-series map names two deleted paths

- [ ] PL-27: L-27's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #346 coordinator: preserve exact inherited action in 02 Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** L-27 (`02` § The table)
- **Where:** `docs/pr-series/map.txt:112`, `:174`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator (ruling (e))
- **Ladder:** written; next rung: `tools/pr-stack-check` failing on an absent path
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-28: the plan says it exists on next; next has no docs/reviews/

- [ ] PL-28: L-28's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #346 coordinator: preserve exact inherited action in 02 Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-28 (`02` § The table)
- **Where:** `docs/reviews/plan-for-the-plan.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator (ruling (a))
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-29: a preliminary slice number in the order

- [ ] PL-29: L-29's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #346 coordinator: preserve exact inherited action in 02 Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** L-29 (`02` § The table)
- **Where:** `docs/reviews/order.md:792`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-30: current release records under the retired name's folder

- [ ] PL-30: L-30's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #509 reviewed rename batch Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** L-30 (`02` § The table)
- **Where:** `docs/rasteratops/release-readiness.md`, `support-matrix.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:#509 (a reviewed rename batch)
- **Ladder:** written; next rung: #509's batch
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-31: the fork's GENERIC_X64 emulator table has drifted and has no generator

- [ ] PL-31: L-31's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #346 coordinator: preserve exact inherited action in 02 Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** L-31 (`02` § The table)
- **Where:** `documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator: a Backlog candidate, generate or drop (ruling (j))
- **Ladder:** written; next rung: a generator from the image's systems list
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-32: the most-cited map, cited by line by open issues

- [ ] PL-32: L-32's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #1216 interface owners; return line mapping Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-32 (`02` § The table)
- **Where:** `docs/es-menu-map.md:134`, `:405`, `:595`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:the interface lanes (ruling (b)); #1216's quoted label differs at `:405`
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-33: two open issues cite a document the tree lacks

- [ ] PL-33: L-33's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #346 coordinator: preserve exact inherited action in 02 Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** L-33 (`02` § The table)
- **Where:** #576 `:7`, #620 `:16`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-34: register rows describe a series D-WORKFLOW-084 ended

- [ ] PL-34: L-34's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #346 coordinator: preserve exact inherited action in 02 Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-34 (`02` § The table)
- **Where:** `docs/decision-register.md` rows; `documentation-accuracy.md:48-52`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator (rows and a rule)
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-35: a docs/** glob loads a device rule for any record

- [ ] PL-35: L-35's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #346 coordinator: preserve exact inherited action in 02 Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q5
- **Source Finding:** L-35 (`02` § The table)
- **Where:** `.claude/rules/handheld-evidence.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator (T4's file)
- **Ladder:** written; next rung: `tools/rules-check` reporting glob reach
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-36: two documents or three that load nowhere

- [ ] PL-36: L-36's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #346 coordinator: preserve exact inherited action in 02 Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** L-36 (`02` § The table)
- **Where:** `CLAUDE.md:34`, `AGENTS.md:31`, `instruction-files.md:122`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator
- **Ladder:** written; next rung: `tools/rules-check`'s twin-fact check
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-37: an area sentence untrue of this slice

- [x] PL-37: **Withdrawn** under the coordinator's v2 disposition: erratum already present at dispatch; accepted case-insensitive readback Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-37 (`02` § The table)
- **Where:** #807 `:15`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator: the erratum is present (06:43 UTC)
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-38: citations no tool checks

- [ ] PL-38: L-38's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #947 citation-check coverage Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-38 (`02` § The table)
- **Where:** the reference files outside `register-check`'s LIVE, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:#947
- **Ladder:** written; next rung: `register-check`'s LIVE widened (#947)
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-39: an open criterion on the versioning document

- [ ] PL-39: L-39's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #1013 versioning criterion Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-39 (`02` § The table)
- **Where:** `docs/releases/versioning.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:#1013
- **Ladder:** written; next rung: #1013's criterion
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-40: a path word the machine retired

- [ ] PL-40: L-40's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #346 coordinator: preserve exact inherited action in 02 Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** L-40 (`02` § The table)
- **Where:** `worktrees.md`, `CLAUDE.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator (T4's rules)
- **Ladder:** written; next rung: no tool can until the coordinator rules
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-41: upstream's generated tables, behind upstream

- [ ] PL-41: L-41's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #563/#559 next upstream base merge Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-41 (`02` § The table)
- **Where:** 13 of the 15 upstream-carried `documentation/` tables, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:the next upstream base merge
- **Ladder:** written; next rung: the upstream base merge
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-42: an open checkbox against the licence file

- [ ] PL-42: L-42's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #346 coordinator: preserve exact inherited action in 02 Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-42 (`02` § The table)
- **Where:** #335 `:19`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator (a tracker edit)
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-43: the licence statements disagree

- [ ] PL-43: L-43's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #528 licensing/source publication; no legal interpretation or byte edit Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** L-43 (`02` § The table)
- **Where:** `TRADEMARK.md:5-6`; `LICENSE.md:3,13,18`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:#528 (a legal reading)
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-44: a licence upstream dropped for a licensing concern

- [ ] PL-44: L-44's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #528 licensing/source publication; no legal interpretation or byte edit Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q1
- **Source Finding:** L-44 (`02` § The table)
- **Where:** `licenses/AETHERSX2.pdf`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:#528
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-45: a qualified candidate's recorded licence bytes

- [ ] PL-45: L-45's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #528 licensing/source publication; no legal interpretation or byte edit Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-45 (`02` § The table)
- **Where:** #359 `:9`, `:13`, `:14`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:#528; the tree's hashes equal #359's
- **Ladder:** written; next rung: `tools/rasteratops-identity-check`
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

### PL-46: the contribution queue's drafts, read-only

- [ ] PL-46: L-46's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
  **Deferred** — #585 contribution queue; drafts never sent Owner dispatch [6585180759](https://github.com/pixelelated/distribution/issues/686#issuecomment-6585180759); retained accepted evidence and `stage-f/outcomes.json`.
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-46 (`02` § The table)
- **Where:** `docs/upstream/**`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:#585 (lines owed, never sent)
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Tracked:** this audit; inherited owner/disposition above retained

## Pause

Two decision comments on #686 will be linked from the Stage-D checkpoint and `07-questions-for-the-maintainer.md`. The next owner action is the coordinator's `docs/reviews/briefs/t39-streams.md`. No Stage E begins before that brief. This issue stays open.

Stage-D filing identity: Codex / GPT-6-Astra / xhigh; session 01a19d12-0c07-7ba3-88b8-ab9d609f4d67; Herdr T1 wN:p4.
