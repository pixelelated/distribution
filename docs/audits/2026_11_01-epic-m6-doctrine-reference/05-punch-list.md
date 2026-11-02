# Punch list -- M6.P2 T39, the reference documents (#686)

**Local depth** (plan § 6c, D-WORKFLOW-184): no reviewer; Phase 4.5 is in `04`. **46 items, one per lead** (PL-NN is L-NN, brief § 3):
- **6 Medium**, each a `bug` filed at stage D: PL-02, PL-03, PL-04, PL-05, PL-07, PL-16.
- **40 Low**: the remaining fix candidates, and the ledger, inherited, #528 and #585 items, each with its owner.

Each item gives the rung of `working-principles.md`'s ladder its statement sits at (*written*: the sentence exists) and the tool that would hold it at the next rung, or *no tool can*. **Nothing in the 254 is changed here.** Every edit waits for the stage-D pause's stream brief (`docs/reviews/briefs/t39-streams.md`, the coordinator's). The audit issue (a sub-issue of #686) and the bugs are filed at stage D; until then each item's `Tracked:` reads *stage D*. Drafted at stage C so the pre-issue lint reads the shape.

---

## PL-01: the renovation's README and plan name P1's files and tools
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** L-01 (`02` § The table)
- **Where:** `docs/reviews/README.md:10-12`, `plan-for-the-plan.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** ledger: resolved at dispatch (ruling (p)); the 15-name loop prints no MISSING
- **Ladder:** written; next rung: no tool can (a merge order)
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing: resolved before any reader acted
- **Acceptance:** L-01's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-02: the front page sends a player to instructions attached to a release that does not exist
- **Severity:** Medium
- **Category:** Bug
- **Question:** Q3
- **Source Finding:** L-02 (`02` § The table)
- **Where:** `README.md:9`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix (ruling (c)); bug
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)'s `leads` step
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** every session that opens the front page; #344 is open
- **Acceptance:** L-02's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-03: the device-testing policy calls D-QA-016 open
- **Severity:** Medium
- **Category:** Bug
- **Question:** Q3
- **Source Finding:** L-03 (`02` § The table)
- **Where:** `docs/device-testing-policy.md:5`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix (ruling (l)); bug; `vm-first.md`'s sentence inherit:coordinator
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9) with a decided-row-called-open check
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** the five rule files that send testers to the policy
- **Acceptance:** L-03's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-04: the retired cloud-folder migration script described as current
- **Severity:** Medium
- **Category:** Bug
- **Question:** Q3
- **Source Finding:** L-04 (`02` § The table)
- **Where:** `docs/rasteratops/cloud-layout.md:16`, `docs/releases/pr/08-saves.md:5`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix (ruling (l)); bug
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)'s `retired` step (it fails at the tip today)
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** the 08-saves PR description; the cloud-layout record
- **Acceptance:** L-04's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-05: the flashing runbook names the OS ROCKNIX throughout
- **Severity:** Medium
- **Category:** Bug
- **Question:** Q3
- **Source Finding:** L-05 (`02` § The table)
- **Where:** `docs/device-flashing-runbook.md` (21 lines), at the dispatch tip `86ebb6dffc`
- **Disposition:** fix where NAMING.md decides the word; the rest classed
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)'s `identity` step with a ROCKNIX-as-the-OS class
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** `CLAUDE.md`, `AGENTS.md` and `device-builds.md:616` send every fresh-card flasher here
- **Acceptance:** L-05's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-06: an M7 order of closed issues
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q4
- **Source Finding:** L-06 (`02` § The table)
- **Where:** `docs/cloud-save-integrity.md:4`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9) with an issue-state check (Q4 (c))
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing traced
- **Acceptance:** L-06's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-07: labels the pin does not ship, in banned words, in the public docs' stated source
- **Severity:** Medium
- **Category:** Bug
- **Question:** Q3
- **Source Finding:** L-07 (`02` § The table)
- **Where:** `docs/backup-contents.md:3-4`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix (labels re-derived from the pin); bug
- **Ladder:** written; next rung: a label check against the ES pin (`es-menu-map-check`'s reach widened)
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** the rocknix.org backup page drafts that copy it
- **Acceptance:** L-07's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-08: the map's journal calls closed #570 work pending
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q4
- **Source Finding:** L-08 (`02` § The table)
- **Where:** `docs/es-menu-map.md:758`, `:806`, `:817`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix: the headings only (ruling (b)); the journal's home is § 4 question 1
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9) with an issue-state check
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** agents placing a row read it
- **Acceptance:** L-08's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-09: a superseded baseline build named as the baseline
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q4
- **Source Finding:** L-09 (`02` § The table)
- **Where:** `docs/releases/next-candidate-work.md:4`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix
- **Ladder:** written; next rung: no tool can (a baseline is a judgement)
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing traced
- **Acceptance:** L-09's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-10: the player's cloud-folder guide ends in internal release status
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q7
- **Source Finding:** L-10 (`02` § The table)
- **Where:** `docs/pixelelated/cloud-folders.md:32-35`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** `README.md:22` sends players here
- **Acceptance:** L-10's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-11: words and numbers run together
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q7
- **Source Finding:** L-11 (`02` § The table)
- **Where:** ten files (`02` § The table), at the dispatch tip `86ebb6dffc`
- **Disposition:** fix in the edit scope; `docs/upstream/README.md`'s share inherit:#585; `rc-accept.txt`'s ledger
- **Ladder:** written; next rung: no tool can (a heuristic, not a check)
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing traced
- **Acceptance:** L-11's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-12: a counter note for a seat outside every run profile, no banner
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q5
- **Source Finding:** L-12 (`02` § The table)
- **Where:** `docs/council-mistral-counter.md:3`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix: a banner; `council-limits.md` is § 4 question 2
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)'s `leads` step
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing traced
- **Acceptance:** L-12's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-13: rocknix.org drafts naming pages without their repository
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q6
- **Source Finding:** L-13 (`02` § The table)
- **Where:** four files (`02` § The table), at the dispatch tip `86ebb6dffc`
- **Disposition:** fix: the repository named beside each page
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)'s `paths` step (`external` class)
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing traced
- **Acceptance:** L-13's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-14: the splash repository's wordmark tool, named with its repository
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** L-14 (`02` § The table)
- **Where:** `docs/pixelelated/art/README.md:20-21`, at the dispatch tip `86ebb6dffc`
- **Disposition:** withdrawn as a defect: a Coverage `none` (X02)
- **Ladder:** written; next rung: held by the `paths`/`tools` steps' `external` class
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-14's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-15: the device facts point to a catalog with none of their cuts
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q4
- **Source Finding:** L-15 (`02` § The table)
- **Where:** `docs/releases/device-facts.md:7`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix the pointer without moving a cited row; inherit:#270 (the tool); inherit:coordinator (the catalog's regeneration, #964)
- **Ladder:** written; next rung: #270's device-facts check
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** #1100, #1126 and #1094 cite its rows
- **Acceptance:** L-15's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-16: the read mask's long form lacks the flag form
- **Severity:** Medium
- **Category:** Bug
- **Question:** Q3
- **Source Finding:** L-16 (`02` § The table)
- **Where:** `docs/device-testing-policy.md:94`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix; bug
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)'s `leads` step
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** readers who copy the policy's mask
- **Acceptance:** L-16's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-17: the wizard's IA against its decided rows
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q4
- **Source Finding:** L-17 (`02` § The table)
- **Where:** `docs/conflict-wizard-ia.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix where a sentence contradicts a decided row and no screen change owns it; else inherit:the interface lanes ([unverified]: the reading is owed)
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** #23 still says rev 5
- **Acceptance:** L-17's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-18: low-inbound reference documents presenting themselves as current
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q5
- **Source Finding:** L-18 (`02` § The table)
- **Where:** the Q5 table's LOW-INBOUND set, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix: a dated first line where a record presents itself as current; retirement is § 4 question 2
- **Ladder:** written; next rung: the Q5 generator's inbound columns, promoted with the checker
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** search results that look current
- **Acceptance:** L-18's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-19: the splash repository's tool in a historical artifact's README
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** L-19 (`02` § The table)
- **Where:** `docs/rasteratops/art/README.md:8`, at the dispatch tip `86ebb6dffc`
- **Disposition:** ledger (a historical artifact; X02)
- **Ladder:** written; next rung: held by the `external` class
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-19's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-20: `packages/rocknix` in dated P0 records
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** L-20 (`02` § The table)
- **Where:** `docs/rasteratops/p0-read.md:11`, `p0-sweep.md:39`, at the dispatch tip `86ebb6dffc`
- **Disposition:** ledger (a dated record)
- **Ladder:** written; next rung: held by the `paths` step's `historical` class
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-20's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-21: Rasteratops as the OS's identity in dated records
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** L-21 (`02` § The table)
- **Where:** `docs/rasteratops/raofflineproxy-refresh.md:180,188`, `cloud-folder-state-table.md:38`, at the dispatch tip `86ebb6dffc`
- **Disposition:** ledger (records of their date)
- **Ladder:** written; next rung: held by the `identity` step's `historical` class
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-21's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-22: a current plan says the site remotes still name the retired owner
- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q4
- **Source Finding:** L-22 (`02` § The table)
- **Where:** `docs/pixelelated/site-plan.md:72`, at the dispatch tip `86ebb6dffc`
- **Disposition:** fix where it misstates the present; else inherit:#511
- **Ladder:** written; next rung: t39-checks.sh promoted to a fork tool (`tools/docs-check`, R3 § 2.9)'s `identity` step
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** nothing traced
- **Acceptance:** L-22's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-23: `maxengel/rocknix` links resolving only by redirect
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** L-23 (`02` § The table)
- **Where:** `docs/cloud-sync-changelog.md:706-735`, at the dispatch tip `86ebb6dffc`
- **Disposition:** ledger (dated changelog entries)
- **Ladder:** written; next rung: held by the `identity` step
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-23's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-24: the one plan, superseded and unmarked
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q1
- **Source Finding:** L-24 (`02` § The table)
- **Where:** `plans/conflict-resolution/vita-style-conflict-resolution.md:8-9`, at the dispatch tip `86ebb6dffc`
- **Disposition:** ledger: one historical-plan row naming the superseding row (ruling (d))
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-24's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-25: 0.0.1 called the first Rasteratops release in the RC ledger
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** L-25 (`02` § The table)
- **Where:** `docs/releases/rc-accept.txt:13`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator (ruling (l))
- **Ladder:** written; next rung: held by the `identity` step's allow-inherited entry
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-25's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-26: two stale acceptances kept as the record
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-26 (`02` § The table)
- **Where:** `docs/releases/rc-accept.txt`, at the dispatch tip `86ebb6dffc`
- **Disposition:** ledger
- **Ladder:** written; next rung: `tools/rc-preflight`
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-26's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-27: the upstream-series map names two deleted paths
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** L-27 (`02` § The table)
- **Where:** `docs/pr-series/map.txt:112`, `:174`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator (ruling (e))
- **Ladder:** written; next rung: `tools/pr-stack-check` failing on an absent path
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-27's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-28: the plan says it exists on next; next has no docs/reviews/
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-28 (`02` § The table)
- **Where:** `docs/reviews/plan-for-the-plan.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator (ruling (a))
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-28's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-29: a preliminary slice number in the order
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** L-29 (`02` § The table)
- **Where:** `docs/reviews/order.md:792`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-29's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-30: current release records under the retired name's folder
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** L-30 (`02` § The table)
- **Where:** `docs/rasteratops/release-readiness.md`, `support-matrix.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:#509 (a reviewed rename batch)
- **Ladder:** written; next rung: #509's batch
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-30's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-31: the fork's GENERIC_X64 emulator table has drifted and has no generator
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** L-31 (`02` § The table)
- **Where:** `documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator: a Backlog candidate, generate or drop (ruling (j))
- **Ladder:** written; next rung: a generator from the image's systems list
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-31's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-32: the most-cited map, cited by line by open issues
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-32 (`02` § The table)
- **Where:** `docs/es-menu-map.md:134`, `:405`, `:595`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:the interface lanes (ruling (b)); #1216's quoted label differs at `:405`
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-32's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-33: two open issues cite a document the tree lacks
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** L-33 (`02` § The table)
- **Where:** #576 `:7`, #620 `:16`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-33's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-34: register rows describe a series D-WORKFLOW-084 ended
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-34 (`02` § The table)
- **Where:** `docs/decision-register.md` rows; `documentation-accuracy.md:48-52`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator (rows and a rule)
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-34's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-35: a docs/** glob loads a device rule for any record
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q5
- **Source Finding:** L-35 (`02` § The table)
- **Where:** `.claude/rules/handheld-evidence.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator (T4's file)
- **Ladder:** written; next rung: `tools/rules-check` reporting glob reach
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-35's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-36: two documents or three that load nowhere
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** L-36 (`02` § The table)
- **Where:** `CLAUDE.md:34`, `AGENTS.md:31`, `instruction-files.md:122`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator
- **Ladder:** written; next rung: `tools/rules-check`'s twin-fact check
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-36's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-37: an area sentence untrue of this slice
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-37 (`02` § The table)
- **Where:** #807 `:15`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator: the erratum is present (06:43 UTC)
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-37's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-38: citations no tool checks
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-38 (`02` § The table)
- **Where:** the reference files outside `register-check`'s LIVE, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:#947
- **Ladder:** written; next rung: `register-check`'s LIVE widened (#947)
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-38's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-39: an open criterion on the versioning document
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-39 (`02` § The table)
- **Where:** `docs/releases/versioning.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:#1013
- **Ladder:** written; next rung: #1013's criterion
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-39's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-40: a path word the machine retired
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** L-40 (`02` § The table)
- **Where:** `worktrees.md`, `CLAUDE.md`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator (T4's rules)
- **Ladder:** written; next rung: no tool can until the coordinator rules
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-40's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-41: upstream's generated tables, behind upstream
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-41 (`02` § The table)
- **Where:** 13 of the 15 upstream-carried `documentation/` tables, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:the next upstream base merge
- **Ladder:** written; next rung: the upstream base merge
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-41's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-42: an open checkbox against the licence file
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-42 (`02` § The table)
- **Where:** #335 `:19`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:coordinator (a tracker edit)
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-42's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-43: the licence statements disagree
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q2
- **Source Finding:** L-43 (`02` § The table)
- **Where:** `TRADEMARK.md:5-6`; `LICENSE.md:3,13,18`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:#528 (a legal reading)
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-43's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-44: a licence upstream dropped for a licensing concern
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q1
- **Source Finding:** L-44 (`02` § The table)
- **Where:** `licenses/AETHERSX2.pdf`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:#528
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-44's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-45: a qualified candidate's recorded licence bytes
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-45 (`02` § The table)
- **Where:** #359 `:9`, `:13`, `:14`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:#528; the tree's hashes equal #359's
- **Ladder:** written; next rung: `tools/rasteratops-identity-check`
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-45's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## PL-46: the contribution queue's drafts, read-only
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** L-46 (`02` § The table)
- **Where:** `docs/upstream/**`, at the dispatch tip `86ebb6dffc`
- **Disposition:** inherit:#585 (lines owed, never sent)
- **Ladder:** written; next rung: no tool can
- **Can this be done on the VM?** No -- the tree, the tool or the register shows it (brief § 5)
- **Already written:** --
- **Acceptance:** L-46's check line (brief § 3) prints the corrected line or nothing after its disposition lands, or the owner's issue carries it
- **Tracked:** stage D

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "L-01"
  disposition: "ledger: resolved at dispatch"
  tracked: "stage D"
  outcome: "open"
- id: PL-02
  severity: Medium
  category: Bug
  question: Q3
  source_finding: "L-02"
  disposition: "fix"
  tracked: "stage D"
  outcome: "open"
- id: PL-03
  severity: Medium
  category: Bug
  question: Q3
  source_finding: "L-03"
  disposition: "fix"
  tracked: "stage D"
  outcome: "open"
- id: PL-04
  severity: Medium
  category: Bug
  question: Q3
  source_finding: "L-04"
  disposition: "fix"
  tracked: "stage D"
  outcome: "open"
- id: PL-05
  severity: Medium
  category: Bug
  question: Q3
  source_finding: "L-05"
  disposition: "fix where NAMING.md decides the word"
  tracked: "stage D"
  outcome: "open"
- id: PL-06
  severity: Low
  category: Code Quality
  question: Q4
  source_finding: "L-06"
  disposition: "fix"
  tracked: "stage D"
  outcome: "open"
- id: PL-07
  severity: Medium
  category: Bug
  question: Q3
  source_finding: "L-07"
  disposition: "fix"
  tracked: "stage D"
  outcome: "open"
- id: PL-08
  severity: Low
  category: Code Quality
  question: Q4
  source_finding: "L-08"
  disposition: "fix: the headings only"
  tracked: "stage D"
  outcome: "open"
- id: PL-09
  severity: Low
  category: Code Quality
  question: Q4
  source_finding: "L-09"
  disposition: "fix"
  tracked: "stage D"
  outcome: "open"
- id: PL-10
  severity: Low
  category: Code Quality
  question: Q7
  source_finding: "L-10"
  disposition: "fix"
  tracked: "stage D"
  outcome: "open"
- id: PL-11
  severity: Low
  category: Code Quality
  question: Q7
  source_finding: "L-11"
  disposition: "fix in the edit scope"
  tracked: "stage D"
  outcome: "open"
- id: PL-12
  severity: Low
  category: Renovation
  question: Q5
  source_finding: "L-12"
  disposition: "fix: a banner"
  tracked: "stage D"
  outcome: "open"
- id: PL-13
  severity: Low
  category: Code Quality
  question: Q6
  source_finding: "L-13"
  disposition: "fix: the repository named beside each page"
  tracked: "stage D"
  outcome: "open"
- id: PL-14
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "L-14"
  disposition: "withdrawn as a defect: a Coverage `none`"
  tracked: "stage D"
  outcome: "open"
- id: PL-15
  severity: Low
  category: Code Quality
  question: Q4
  source_finding: "L-15"
  disposition: "fix the pointer without moving a cited row"
  tracked: "stage D"
  outcome: "open"
- id: PL-16
  severity: Medium
  category: Bug
  question: Q3
  source_finding: "L-16"
  disposition: "fix"
  tracked: "stage D"
  outcome: "open"
- id: PL-17
  severity: Low
  category: Code Quality
  question: Q4
  source_finding: "L-17"
  disposition: "fix where a sentence contradicts a decided row and no screen change owns it"
  tracked: "stage D"
  outcome: "open"
- id: PL-18
  severity: Low
  category: Renovation
  question: Q5
  source_finding: "L-18"
  disposition: "fix: a dated first line where a record presents itself as current"
  tracked: "stage D"
  outcome: "open"
- id: PL-19
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "L-19"
  disposition: "ledger"
  tracked: "stage D"
  outcome: "open"
- id: PL-20
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "L-20"
  disposition: "ledger"
  tracked: "stage D"
  outcome: "open"
- id: PL-21
  severity: Low
  category: Renovation
  question: Q2
  source_finding: "L-21"
  disposition: "ledger"
  tracked: "stage D"
  outcome: "open"
- id: PL-22
  severity: Low
  category: Code Quality
  question: Q4
  source_finding: "L-22"
  disposition: "fix where it misstates the present"
  tracked: "stage D"
  outcome: "open"
- id: PL-23
  severity: Low
  category: Renovation
  question: Q2
  source_finding: "L-23"
  disposition: "ledger"
  tracked: "stage D"
  outcome: "open"
- id: PL-24
  severity: Low
  category: Renovation
  question: Q1
  source_finding: "L-24"
  disposition: "ledger: one historical-plan row naming the superseding row"
  tracked: "stage D"
  outcome: "open"
- id: PL-25
  severity: Low
  category: Renovation
  question: Q2
  source_finding: "L-25"
  disposition: "inherit:coordinator"
  tracked: "stage D"
  outcome: "open"
- id: PL-26
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "L-26"
  disposition: "ledger"
  tracked: "stage D"
  outcome: "open"
- id: PL-27
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "L-27"
  disposition: "inherit:coordinator"
  tracked: "stage D"
  outcome: "open"
- id: PL-28
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "L-28"
  disposition: "inherit:coordinator"
  tracked: "stage D"
  outcome: "open"
- id: PL-29
  severity: Low
  category: Renovation
  question: Q7
  source_finding: "L-29"
  disposition: "inherit:coordinator"
  tracked: "stage D"
  outcome: "open"
- id: PL-30
  severity: Low
  category: Renovation
  question: Q2
  source_finding: "L-30"
  disposition: "inherit:#509"
  tracked: "stage D"
  outcome: "open"
- id: PL-31
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "L-31"
  disposition: "inherit:coordinator: a Backlog candidate, generate or drop"
  tracked: "stage D"
  outcome: "open"
- id: PL-32
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "L-32"
  disposition: "inherit:the interface lanes"
  tracked: "stage D"
  outcome: "open"
- id: PL-33
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "L-33"
  disposition: "inherit:coordinator"
  tracked: "stage D"
  outcome: "open"
- id: PL-34
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "L-34"
  disposition: "inherit:coordinator"
  tracked: "stage D"
  outcome: "open"
- id: PL-35
  severity: Low
  category: Renovation
  question: Q5
  source_finding: "L-35"
  disposition: "inherit:coordinator"
  tracked: "stage D"
  outcome: "open"
- id: PL-36
  severity: Low
  category: Renovation
  question: Q7
  source_finding: "L-36"
  disposition: "inherit:coordinator"
  tracked: "stage D"
  outcome: "open"
- id: PL-37
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "L-37"
  disposition: "inherit:coordinator: the erratum is present"
  tracked: "stage D"
  outcome: "open"
- id: PL-38
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "L-38"
  disposition: "inherit:#947"
  tracked: "stage D"
  outcome: "open"
- id: PL-39
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "L-39"
  disposition: "inherit:#1013"
  tracked: "stage D"
  outcome: "open"
- id: PL-40
  severity: Low
  category: Renovation
  question: Q2
  source_finding: "L-40"
  disposition: "inherit:coordinator"
  tracked: "stage D"
  outcome: "open"
- id: PL-41
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "L-41"
  disposition: "inherit:the next upstream base merge"
  tracked: "stage D"
  outcome: "open"
- id: PL-42
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "L-42"
  disposition: "inherit:coordinator"
  tracked: "stage D"
  outcome: "open"
- id: PL-43
  severity: Low
  category: Renovation
  question: Q2
  source_finding: "L-43"
  disposition: "inherit:#528"
  tracked: "stage D"
  outcome: "open"
- id: PL-44
  severity: Low
  category: Renovation
  question: Q1
  source_finding: "L-44"
  disposition: "inherit:#528"
  tracked: "stage D"
  outcome: "open"
- id: PL-45
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "L-45"
  disposition: "inherit:#528"
  tracked: "stage D"
  outcome: "open"
- id: PL-46
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "L-46"
  disposition: "inherit:#585"
  tracked: "stage D"
  outcome: "open"
```

## Phase 7 resolution gate

Every item is **Open** at the pre-issue lint; the outcomes are written at stage F from the streams' commits and the owners' issues.

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Open | stage D/E |
| PL-02 | Open | stage D/E |
| PL-03 | Open | stage D/E |
| PL-04 | Open | stage D/E |
| PL-05 | Open | stage D/E |
| PL-06 | Open | stage D/E |
| PL-07 | Open | stage D/E |
| PL-08 | Open | stage D/E |
| PL-09 | Open | stage D/E |
| PL-10 | Open | stage D/E |
| PL-11 | Open | stage D/E |
| PL-12 | Open | stage D/E |
| PL-13 | Open | stage D/E |
| PL-14 | Open | stage D/E |
| PL-15 | Open | stage D/E |
| PL-16 | Open | stage D/E |
| PL-17 | Open | stage D/E |
| PL-18 | Open | stage D/E |
| PL-19 | Open | stage D/E |
| PL-20 | Open | stage D/E |
| PL-21 | Open | stage D/E |
| PL-22 | Open | stage D/E |
| PL-23 | Open | stage D/E |
| PL-24 | Open | stage D/E |
| PL-25 | Open | stage D/E |
| PL-26 | Open | stage D/E |
| PL-27 | Open | stage D/E |
| PL-28 | Open | stage D/E |
| PL-29 | Open | stage D/E |
| PL-30 | Open | stage D/E |
| PL-31 | Open | stage D/E |
| PL-32 | Open | stage D/E |
| PL-33 | Open | stage D/E |
| PL-34 | Open | stage D/E |
| PL-35 | Open | stage D/E |
| PL-36 | Open | stage D/E |
| PL-37 | Open | stage D/E |
| PL-38 | Open | stage D/E |
| PL-39 | Open | stage D/E |
| PL-40 | Open | stage D/E |
| PL-41 | Open | stage D/E |
| PL-42 | Open | stage D/E |
| PL-43 | Open | stage D/E |
| PL-44 | Open | stage D/E |
| PL-45 | Open | stage D/E |
| PL-46 | Open | stage D/E |
