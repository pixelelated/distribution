---
slice: T39
id: doctrine-reference
issue: "#686"
epic: "#807"
area: doctrine
kind: table
lens: cost against value
depth: Local
version: 2
written: 2026-11-01
author: the M6 coordinator lane (D-WORKFLOW-189)
read_refs:
  distribution: 8ebaf8daad
  p1: 2174265e9c
  coordinator: e3fb3dfe00
  inventory_head: eb4763e3cc
  merge_base: c445081a59
  upstream: 651150fc88
---

# Review brief: M6.P2 T39, the reference documents: README, TRADEMARK, LICENSE and `licenses/`, `documentation/`, `plans/`, and the reference documents under `docs/`, tabled for what misleads a reader today (#686)

**Version 2, 2026-11-01, after the stranger's proof of version 1**
(D-WORKFLOW-189; `docs/reviews/plan-for-the-plan.md` § 6b, § 6c, § 7).
Version 1 was written from five read-only research files -- R1 membership
and provenance, R2 the documents read, R3 checks and harness, R4 the inherited
items, R5 the model and the ceremony
(`/workspace/tmp/m6-coordinator/kit/t39-research/`, in no tree) -- and nothing
else: **every figure here is one of their quoted tool lines**, cited as
`R1 C<nn>` (R1's commands C01 to C20) or `R1 § <n>`; `R2 C<n>` (R2's "command
<n>", 1 to 27), `R2 § <n>` or `R2 L-<nn>` (R2's leads L-01 to L-20, never this
brief's numbering); `R3 C<n>` (C1 to C24) or `R3 § <n>`; `R4 item <n>` (1 to
68), `R4 § <n>` or `R4 C<n>` (R4's "command <n>", 1 to 28); `R5 C<n>` (C1 to
C24), `R5 § <letter>` or `R5 § B item <n>`. **Version 2** applies the
stranger's proof of version 1 (`/workspace/tmp/m6-coordinator/kit/t39-proof.md`,
in no tree, 443 lines; its totals `checks 125; PASS 107; MISMATCH 13; SETTLED
3; NOTE 2; corrections 12`, read at `a0fb117b8b`, version 1's commit on the
coordinator's branch), cited `proof K<nn>` (its checks K01 to K125), `proof
X<nn>` (its corrections X01 to X12) or `proof C<n>` (its commands C1 to C17),
and the coordinator's rulings on it (D-WORKFLOW-189); a figure version 2's
drafting read re-ran is cited `v2 read` with its command, run by hash at
`2174265e9c` or `a0fb117b8b`. **`[unverified]` marks what no tool line
settles, with what would settle it**;
`## Version 1: what the drafting read did not settle` lists every one with its
state after the proof, then every place where the research files disagree and
how this brief takes each, then the checks on version 1; the last section,
`## Version 2: corrections from the proof`, lists each correction at its line,
the open items' states and the checks on this file. Counts by
`/usr/bin/grep`, never the shell's function (#1138; R5 § B item 12).

**The structure is T38's brief** (`docs/reviews/briefs/doctrine-skills.md` at
`3a9b0aec81`, its dispatch with `## Errata before dispatch`; 2,031 lines, R5
C5), the newest Local model, with R5 § A's verdicts applied
(`copy 13, rewrite 26, drop 5, of 44 rows`, R5 C24): every part R5 marks
*copy* is copied with this slice's names, every part marked *rewrite* is
rewritten for a table, and the skill-, agent-, pin- and bundle-specific parts
are dropped. **The table's shapes of § 5 and § 7 are T40's**
(`docs/reviews/briefs/patches-dead.md` at the same commit, 454 lines, 16
checkboxes, accepted with its `## Errata, 2026-10-25`; R5 § A, C14, C15): rows
a tool generates, one per member, the session's judgement in one column, the
count equal to a command's. **R5 § 0's premise correction is written in**: the
daily ledgers -- the work logs, futros, retros, audit folders, qa-logs and
session pointers -- are area `records` (T46's), and the friction log and the
decision and blindspot registers are T4's, with `NAMING.md`; what the 254
carry that no lane edits is a different set, ruling (a)'s (R5 § 0; R1 § 4,
C06). R5 § B's recurring errata are written out of it: the register line from
the decided table only (§ 9); the placeholder check in its widened form (§ 9;
T38's errata before dispatch); every other lane's ref recorded as whichever
line prints (§ 3 item 8); a checker whose rc 0 covers nothing in the slice
named as such (§ 3 item 5); every figure as its tool prints it, the
inventory's 38,598 beside the newline counts, each with its population (ruling
(h)); § 10 copying § 1's, § 5's and § 9's figures from one place; a reading
that would call a provider listed in the never-run list (§ 10); a row read
before it is cited (§ 9); the locale stated beside each count (§ 5); one
ownership row, D-WORKFLOW-220, cited everywhere (§ 9); and every count by
`/usr/bin/grep`. The rule, register and futro lines are the coordinator
worktree's at **`e3fb3dfe00`** (R1's, R2's, R3's, R4's and R5's headers); the
lane re-reads them at `COHASH`.

## 1. Identity

- **Issue:** #686 `M6.P2 E807/T39: doctrine: the reference documents` (OPEN,
  milestone `M6: Codebase renovation`, no labels, 1 comment, already retitled;
  parent #807 by the API; REST id `5992346342`; R5 § A, C16). The pre-dispatch
  body is 27 lines with 5 generated checkboxes (sha256 prefix
  `a4005afbd8130c72` by
  `gh api repos/pixelelated/distribution/issues/686 --jq .body | sha256sum`,
  R5 C16; `gh issue view --json body --jq .body` hashes the same body to
  `f4e17688f4350982`, proof K31; last updated `2026-10-24T15:21:21Z`). The
  provenance and depth lines carry bold markup in the body
  (`**Provenance tiers:** ...`, `**Review depth:** ...`), which the quotations
  below drop, so a `grep -F` of their words prints 0 (proof K30). **Its sentences are cited here by content,
  never by line number**, because the kit rewrites the body from § 7 at
  dispatch and every line moves (ruling (i)): the why, *"tabled for what
  misleads a reader today"*; the paths sentence *"254 paths, 38,598 lines; 190
  lines read, 190 of them fork-own (inventory at `eb4763e3cc`)"* (R4 § 0; R5
  C16); the provenance line *"Provenance tiers: fork-own 164, upstream-carried
  90"* (R4 § 0); the depth line *"Review depth: Local -- a table"* (R4 item
  23); the `reviewed-at:` and `fixed-at:` header lines, blank (R4 item 23);
  the generated VM line *"No test is proposed: a table slice is host analysis
  of the tree; a removal it proposes is proven on the GENERIC_X64 guest before
  it is a punch item."* (R4 item 23; R5 § D); the criteria sentence *"are
  added here by the coordinator with its brief"* (R4 item 23); and the
  audit-folder line `docs/audits/<date>-epic-m6-doctrine-reference/` (R4 item
  23). **The body fill at dispatch is the coordinator's** (ruling (i)).
- **The order's row.** Slice `doctrine-reference` (`k: 39`) in
  `docs/reviews/slices.json`, area `doctrine`, kind `table`, lens
  `cost against value`, selector `{"rest": true}` (no glob of its own), read
  before none, depth `Local`, `depth_reason` *"a table"* (R1 C01).
  `docs/reviews/order.md` § T39 opens at `:673` (*"### T39. doctrine: the
  reference documents"*), its why *"the rest of the doctrine area: README,
  TRADEMARK, LICENSE and `licenses/`, `documentation/`, `plans/`, and the
  reference docs under `docs/` (upstream, releases, the rename, the menu map):
  tabled for what misleads a reader today"*, its paths line *"254 paths,
  38,598 lines, -- read, of which -- fork-own; 0 patch and config lines; reach
  n/a 254"*, its interacting subsystems *"every area (25 to 29 rules govern
  each, cross-reference.md)"*, its closing evidence *"audit folder
  `docs/audits/<date>-epic-m6-doctrine-reference/` with `00-running-log.md`
  and `01-research-notes.md` to `05-punch-list.md`,
  `tools/lint-audit-artifacts` PASS with the renovation face, the punch-list
  issue resolved through Phase 7, `reviewed-at` and `fixed-at` set"* (`:681`);
  `:156` puts T38 and T39 after the rules; `:188` is the renumbering table's
  row for this slice (`| T39 | T39 |`, naming `doctrine-reference`); and
  `:792`'s *"split in three (T4, T33, T39)"* uses the preliminary review's T33
  for today's T38 (R1 C01, § 1; L-29). `order.md`, `slices.json`, `areas.json`
  and `inventory.json` are the P1 branch's at `2174265e9c`, which the lane's
  worktree is stacked on (ruling (g)).
- **What each figure counts** (R1 § 1, § 2). **254 paths and 38,598 lines**
  are the inventory's `lines` column summed at its head `eb4763e3cc` (R1 C16:
  `lines: 38598 reach: {'n/a': 254} tier: {'fork-own': 164, 'upstream-carried': 90}`).
  **"190 read, 190 fork-own"** is the tool's *Read* rule -- a path's lines
  count only when its language is in the `CODE` set -- and two rows qualify,
  `docs/pixelelated/art/source/generate.py` (python, 180) and
  `docs/pixelelated/art/source/wordmark.css` (css, 10), both fork-own (R1 C16:
  `read lines: 190 of which fork-own: 190`); for a table slice the order
  prints `--` in those columns (`tools/renovation-inventory:1343-1344`, R1
  C02), so the order's `--` and the tool's `190` are the same row. **31 rows
  are binary** (`lines` is `None`): `binary rows: 31 (gz 1, pdf 2, png 28)`
  (R1 C19), so a newline count runs over the **223 text rows** (ruling (h)).
  Reach is `n/a` for all 254; the languages are
  `{'markdown': 113, 'text': 78, 'image': 39, 'json': 8, 'python': 1, 'css': 1, 'none': 1, 'other': 3, 'patch': 10}`
  (R1 C16), the ten `patch` rows being the `fix.patch` drafts under
  `docs/upstream/raofflineproxy/*/`, fork-own and so not the inventory's
  vendor-carried "patch and config lines" (R1 § 2).
- **Provenance.** `fork-own 164`, `upstream-carried 90` (R1 C16), the 90 being
  **`licenses/` 75 and `documentation/` 15** (R1 C06's GROUPS; R5 C21). 92 of
  the 254 exist at the merge base `c445081a59`: the 90 and `README.md` and
  `LICENSE.md`, upstream files the fork rewrote (R1 C11, C16:
  `present at the merge base: 92`). **All 90 upstream-carried rows are
  byte-identical to the merge base; 76 are byte-identical to today's
  `upstream/next` `651150fc88`** -- the 74 licence texts and two
  `documentation/` tables, AMD64 and SDM845 -- while 13 tables differ and
  `licenses/AETHERSX2.pdf` is absent upstream (R1 C12: `vs MB identical 90`,
  `vs UP identical 76`, `vs UP differs 15`, `vs UP absent 163`). Upstream
  since the merge base: `documentation/` 4 commits (three
  `documentation: SUPPORTED_EMULATORS_AND_CORES` regenerations on 2026-10-02,
  10-18 and 10-22, and `S922X: docs` on 10-01), `licenses/` 1 (`c4d353449e`
  2026-10-18 *aethersx2: drop package due to licensing concern*, which deleted
  `licenses/AETHERSX2.pdf`: 75 at the base, 74 at `651150fc88`), `README.md`
  and `LICENSE.md` 0 (R1 C11). Upstream holds no `TRADEMARK.md`, no `plans/`
  and no `docs/` (R1 C11). The one non-merge fork commit on an
  upstream-carried row is `1476fe68a5` 2026-08-27 *RK3566: regenerate the
  supported-emulators table*, whose file is again blob-identical to the base
  (R1 C18, C12). The fork's commits on the 254 since the merge base: 663, 651
  of them non-merges (R1 C11); 144 of the 254 have one commit in their whole
  history (`one-commit paths: 144`, every commit at the P1 tip, by
  `while IFS= read -r p; do git -C "$W" rev-list --count 2174265e9c -- "$p"; done < .qa-scratch/t39/paths.txt | awk '{c[$1]++} END {print "one-commit paths: " c[1]+0}'`
  -- proof C3 and `v2 read`; R1 C09's non-merge rule, over the commits
  reachable from `e3fb3dfe00`, prints 145 one-commit and 8 zero-commit paths,
  proof C12; X09), and the most edited are `docs/vm-qa-log.md` 184,
  `docs/cloud-sync-changelog.md` 137, `docs/rasteratops/release-readiness.md`
  128, `docs/es-menu-map.md` 79, `docs/releases/next-candidate-work.md` 58 and
  `docs/releases/catalog.md` 51 (R1 C09).
- **The coordinator's rulings, stated once; § 2's take-up table and § 3's
  leads point here** (D-WORKFLOW-189):
  (a) **The carve-out.** T39's edit scope is the reference documents proper:
  the 254 less the 90 upstream-carried, less the ledger rows below and less
  the read-only rows of rulings (j), (k) and (n) -- R1's
  `REFERENCE 239 paths 29057 lines` (R1 C16) counts the 90 among its 239, so
  the class sizes are the stage-A `CARVE` lines (§ 5), never a figure typed
  here: the proof printed version 1's at `a0fb117b8b` (K26, `CARVE total 254`;
  open item 1 settled) and version 2's read re-ran them with
  `p0-sweep-hits.txt` in the ledger -- `CARVE art-bytes 18`, `edit-scope 68`,
  `edit-under-naming 1`, `ledger-binary 31`, `ledger-named 6`, `ledger-plan 1`,
  `ledger-reviews 12`, `read-only-528 1`, `read-only-585 27`,
  `read-only-upstream 88`, `tabled-generic-x64 1`, `CARVE total 254` (`v2
  read`; version 1's lines read `edit-scope 69` and `ledger-named 5`); the
  ruling's own wording is the Version 1 section's disagreement 2. **The ledger
  rows** -- tabled in `02` as *"a ledger, not a
  reference"*, never edited here -- are: the coordinator's 12 files under
  `docs/reviews/**` (the program's own documents under D-WORKFLOW-189; R1's L1
  class, `CLASS L1-renovation-records 12 paths 5487 lines`, C16);
  `docs/releases/catalog.md` (generated by `tools/release-catalog` from the
  artifacts' `RECORD.txt`, its header *"do not edit by hand"*, never
  hand-edited; R3 § 1, C21); `docs/pr-series/map.txt` (read by
  `tools/pr-stack-check`, `fork-workflow.md`'s; R5 § 0, C20);
  `docs/releases/rc-accept.txt` (read by `tools/rc-preflight`, the RC round's;
  R5 § 0); `docs/vm-qa-log.md` (the VM cycles' ledger) and
  `docs/cloud-sync-changelog.md` (the running change log under
  `change-log.md`; R1 § 4); `docs/rasteratops/p0-sweep-hits.txt` (the P0
  sweep's generated classification baseline, which `NAMING.md:30` names so:
  2,419 lines, of which 20 carry `maxengel/rocknix` -- the sweep's hits as it
  found them, not references to correct; `v2 read`:
  `git -C "$W" show 2174265e9c:docs/rasteratops/p0-sweep-hits.txt | /usr/bin/grep -c ''`
  prints `2419` and `| /usr/bin/grep -c 'maxengel/rocknix'` `20`; read-only,
  findings to the coordinator; open item 25, ruled at version 2); `plans/` as
  one historical-plan row (ruling (d)); and the 31 binary files by name, size
  and sha256 (ruling (o), which at version 2 also tables the 18 art text
  files). **The 90
  upstream-carried are read-only**: a finding goes to #528 (the licences, and
  `licenses/AETHERSX2.pdf`, which upstream deleted for a licensing concern;
  L-44) or to upstream as a #585 line, never sent (D-WORKFLOW-164, -165).
  **`LICENSE.md` and `TRADEMARK.md` are fork-own but legal and identity**:
  findings to #528, edits only where `NAMING.md` already decides the word
  (D-WORKFLOW-136, -144).
  (b) **The menu map's stale rows are the E700 interface lanes'** under
  D-UI-039 (`decision-register.md:190`, R5 § B item 8). T39 fixes only defects
  no screen change owns: the dated journal's "Pending" headings for closed
  issues (#570, `CLOSED 2026-10-14`, R2 C14) are corrected to say closed, with
  no restructuring (L-08); the journal's home is a question for § 4.
  (c) **`README.md` has no build commands** (23 lines, no `make ` or `docker`
  line, R3 § 2.6, C16; R5 C21): the question of build commands against the
  admission gate is moot. Its `:7-10` *"use the instructions attached to the
  [release]"* with no pixelelated release on the releases page (R2 L-14; R4
  item 16) is a lead with a contained fix that tells a reader the fork's true
  state (L-02).
  (d) **`plans/` is one historical-plan ledger row**; no plan is edited; a
  plan a decided row supersedes is named with that row's ID (L-24).
  (e) **`docs/pr-series/map.txt`'s two paths deleted on 2026-10-08** (R2 L-04)
  are the coordinator's (`fork-workflow.md`'s map): inherited, not fixed here
  (L-27).
  (f) **The session** is whichever of `m6-t1-os-launch` (T36) or
  `m6-t3-emulators` (T37) frees first; the dispatch comment names it (R5 § G
  (f), C18: both `working` at the research's read).
  (g) **The lane reads the tree it carries** at the dispatch tip: the P1 tip
  `2174265e9c` with the coordinator's branch merged. § 2's block runs from the
  worktree's `docs/reviews/{slices,inventory,areas}.json` and
  `tools/renovation-inventory`, which are there; `next` (`8ebaf8daad`, 242 of
  the 254, the twelve `docs/reviews/` paths absent, R1 C07) is not a read tree
  for this slice.
  (h) **Two line figures, side by side**: the inventory's **38,598** (its tool
  line, R1 C16) and the newline count of the **223 text files** at the P1
  hash, **`grep -c` 38,675 and `wc -l` 38,674** (R1 C16; one file, upstream's
  `licenses/XFree86-1.1.txt`, lacks its trailing newline, R1 C17), with the
  **31 binaries named as uncounted** (R1 C19).
  (i) **#686's body is rewritten at dispatch by the kit from § 7**: the
  generated VM line replaced by § 5's answer, § 7's criteria in place of the
  five generated ones, no `-es` header pair. **#807 `:15`'s *"its paths have
  no upstream (ROCKNIX carries none of them)"*** (R5 C23) is wrong for T39's
  90 upstream-carried paths -- an erratum the coordinator writes on the epic's
  body at dispatch (R5 § B item 16; L-37).
  (j) **The fork-own GENERIC_X64 table in `documentation/`**
  (`documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md`,
  128 lines, no generator in the tree; R2 L-17) is tabled with a Backlog
  candidate -- generate it or drop it -- and not edited (L-31).
  (k) **`LICENSE.md`**: findings go to #528; no edit.
  (l) **The retired-name and identity hits are fixes where a reader would act
  wrongly:** `cloud_migrate_layout` described in the present tense
  (`docs/rasteratops/cloud-layout.md:16`, `docs/releases/pr/08-saves.md:5`;
  D-CLOUD-175 retired it, `decision-register.md:642`, R4 item 13) takes a
  sentence saying so, with the row's ID (L-04); `maxengel/rocknix` links that
  resolve only by redirect become `pixelelated/distribution` where the fork's
  own repository is meant (L-23); `rc-accept.txt:13`'s *"the first Rasteratops
  release"* is the RC ledger's (ruling (a)), inherited to the coordinator
  (L-25); `device-testing-policy.md`'s *"D-QA-016 open"* (decided 2026-09-13,
  #131 closed) is fixed (L-03); the flashing runbook's 21 `ROCKNIX` against 0
  `pixelelated` (R2 C20) is fixed only where `NAMING.md` decides the word, the
  rest recorded (L-05); a hit that exposes a rule erratum is inherited to the
  coordinator.
  (m) **The futro addendum** goes in the doctrine futro after T38's (§ 10).
  (n) **`docs/upstream/`** (the contribution queue's prepared patches; 28
  paths, R1 C06) is #585's: read-only, findings to #585 (L-46).
  (o) **The 31 binary files and the 18 art text files** --
  `docs/pixelelated/art/**`'s SVG, JSON, CSS, `generate.py` and the two
  `Tiny5-OFL.txt`, and `docs/rasteratops/art/*.svg`: the stage-A
  `CARVE art-bytes 18` class (proof K26; `v2 read`) -- are tabled by name, size
  and sha256 and never edited by T39; the two art READMEs
  (`docs/pixelelated/art/README.md`, `docs/rasteratops/art/README.md`) are that
  area's reference documents; a finding in an art source is routed to the
  splash repository (external), a licence text's to #528. (Widened at version
  2 from the binaries alone: open item 21, the coordinator's ruling.)
  (p) **R2's L-01 is the coordinator's and is resolved at dispatch:**
  `docs/reviews/README.md` and `plan-for-the-plan.md` name P1's files and
  tools that live on `feature/m6-p1-survey-641` and not on the coordinator's
  branch (seven `MISSING` at `e3fb3dfe00`, R2 C6, C10, C12); the coordinator
  merges the P1 branch into the coordinator's branch before T39's dispatch,
  and the lane verifies at stage A that every named file resolves in its
  worktree (it did already, the worktree being P1 plus the coordinator). The
  lead is recorded as resolved at dispatch with its verification command
  (L-01; § 5's `# STAGE A`).
  (q) **Depth Local, no guest, no compile, no keyed or council call, no
  `config/options`:** `second-opinions/review-plan.json` records `local` with
  no reviewer, `tier_exception` `D-WORKFLOW-184` (`decision-register.md:719`,
  R5 § B item 8; R3 § 3); the lint's Local-plan proof runs first at stage A
  (ruling (m) of T38's brief, the same shape); **a compile START written by
  this lane is a stop**; the guest plan is "none" with `vm-first.md`'s
  sentence, the one exception a document that claims a guest behaviour,
  recorded `[unverified]` (§ 5).
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does not
  re-cut the slice, change a criterion, write a brief, move the M6 body, edit
  `slices.json`, `areas.json`, `order.md`, the plan or any other
  `docs/reviews/` file, file a Backlog issue, post on #346, #528, #585, #807
  or #509, or decide a question of scope: those are the coordinator's, reached
  through #686, one question at a time. What it does file: its own audit
  punch-list issue (stage D) and a `bug` issue for each statement it proves a
  reader acts on wrongly (§ 4 Q3), with its trace and `Already written:` line
  (D-WORKFLOW-187). **A fix lands only under a stream brief the coordinator
  writes at the stage-D pause, on the slice branch, inside the edit scope of
  ruling (a).** A finding in a ledger row, an upstream-carried file,
  `LICENSE.md`, `docs/upstream/` or a binary is an inherited item with its
  owner (rulings (a), (k), (n), (o)); a finding in a rule, `CLAUDE.md`,
  `AGENTS.md`, `NAMING.md` or a register is the coordinator's (T4's read,
  #651); a stale menu-map row is the interface lanes' (ruling (b)).
- **One worktree, one session, and four placeholders.** The distribution's
  **`feature/m6-doctrine-reference-686`** at
  **`/workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-reference-686`**
  (both absent before dispatch, R5 C17), created by the coordinator, **stacked
  on `feature/m6-p1-survey-641` at `2174265e9c`** (the P1 tip, or the one the
  dispatch comment names) with the coordinator's branch merged in and the
  lane's pointer seeded. **There is no EmulationStation worktree**: the only
  EmulationStation read is L-07's label check,
  `git -C <the ES checkout> grep <pin>` at the shipped pin, read-only (R2 C20;
  R3 C12 names the checkout `~/Development/emulationstation-next`). **Four
  placeholders stand in this brief for hashes that do not exist until
  dispatch:** `COHASH` (the coordinator's tip merged into the lane's branch),
  `MERGE_HASH` (that merge commit, the lane's dispatch tip), `TIPHASH` (the
  lane's own tip as it moves; at stage A it is `MERGE_HASH`) and `V2HASH`
  (this brief's commit on the coordinator's branch at dispatch, after the
  stranger's proof makes version 2; version 1 has no dispatch hash). The
  dispatch comment on #686 and the seeded pointer carry their values; the lane
  reads them there, never guesses them, and § 9's placeholder check runs on
  every artifact. **No other lane's slice is these paths**: every one of the
  254 is claimed by T39 alone, by the area's `rest` (R1 C06:
  `254 paths 38598 lines ('distribution', ('doctrine-reference',), 'rest')`).
  Until the dispatch comment exists the pointer is not seeded and nothing
  starts.
- **Review depth: Local** (plan § 6c: *"a dead-end table, a provenance table,
  a doctrine read | Local: the executor alone; the lint and the counts are the
  check"*, R1 C13). **No external reviewer, no `npm install`, no Facilitator
  call, no `tools/council/run`.** `second-opinions/review-plan.json` is still
  written, in **T4's plan's shape** (read at stage A from T4's tip
  `6ec78bbf8c`, R4 § 4): depth `local`, the primary as that plan writes it,
  lab `anthropic`, reviewers `[]`, `tier_exception` `D-WORKFLOW-184` and a
  `reason` naming plan § 6c's row. No Local plan exists under the
  coordinator's tip's audit folders (R3 C21: `0 of 8`), which is why the
  lint's PASS on one is proven at stage A first (ruling (q)). The code-auditor
  skill's Phase 4.6 is recorded as *not applicable at Local depth*, with plan
  § 6c's row cited; Phase 4.5 (the executor's own finding verification) is
  done in full, and § 5's rule 4 -- what result would have produced a FAIL --
  is asked of every PASS, because nobody else asks it here.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at stage A
  (R5 § G (f)). **The session is ruling (f)'s**; its `cwd` is its first
  worktree (R5 C18), so the dispatch names the new worktree and the lane `cd`s
  there.
- **The first commands** are § 5's `# STAGE A` block, whole and in order,
  after the pointer's eleven keys (§ 10) and before the membership block (§
  2). It carries no `git fetch` line: a by-hash read needs none, and the
  never-run list forbids it (§ 10; T40's errata at acceptance, R5 § A, C15:
  *"A brief's first commands never carry a fetch where its evidence floor says
  no network"*).

## 2. Scope

**The membership, by the block that defines it** (run from the lane's
distribution worktree, stacked on the P1 branch, which holds
`docs/reviews/{slices,inventory,areas}.json` at `2174265e9c` -- sha256
prefixes `49bc2745664e52f4` (`slices.json`), `d17b9cac4b2c2245`
(`inventory.json`) and `985f742cfd4a2138` (`areas.json`), R1 C05, the first
two the same as T38's; § 5's `# STAGE A` checks all three before the block
runs; ruling (g)). The script is T38's `membership.py` rewritten for the
area's `rest` (R1 § 6): rows of `tree == "distribution"`, the slice id
`doctrine-reference`, the labels `in-T39` / `not-in-T39`. **A `rest` slice has
no glob of its own**, so the tree-side proof is `TREE-SIDE`: the doctrine area
by `areas.json`'s globs, less every non-rest selector naming the area (T4's
and T38's globs), derived from `ls-tree -r` at the inventory head and at the
P1 hash; the run therefore needs `areas.json` beside the two JSONs; it prints
`GROUPS`, the read rows, the binary rows, the tier lines and
`last_upstream_commit`; its `CLAIMS` names the neighbours (the registers,
`NAMING.md`, `inventory.json`, the plan, the order, the menu map, the VM
ledger, the catalog, the work-log index, the doctrine futro, the resume file,
a skill); `DOCS TREE BY SLICE` shows every `docs/` row by subdirectory and
owning slice; and the line counts run over the **223 text rows** only (R1 §
6). **`W` is the P1 research clone
`/workspace/tmp/m6-coordinator/t11-research/tree`, read by `git -C` only, and
`P1=2174265e9c`; `MB` is the distribution merge base `c445081a59`.** Keyword
arguments are spaced `key = lambda`. The heredoc is saved once and run twice
-- first against `/dev/null` to make the paths file from its own TSV, then
against that file to prove equality. **The text below is R1's `block.sh` byte
for byte** (130 lines, sha256 prefix `e81453b6732cdea8`, R1 C16); R1
re-extracted it from its own text, re-ran it from a fresh scratch and diffed
the output against the expected lines, which printed *"re-run of the block =
R1's Expected, byte for byte"* (R1 C20). The lane extracts it from this brief
at `V2HASH` by its markers, never retypes it, and checks the prefix (§ 5's
`# STAGE A`):

<!-- t39 block.sh begin -->
```bash
mkdir -p .qa-scratch/t39
cat > .qa-scratch/t39/membership.py <<'PYEOF'
import json, re, sys, collections
CODE = {"shell","python","recipe","c","c++","c-header","c++-header","javascript","typescript","make","cmake","systemd","udev","script","perl","lua","rust","go","assembly","shader","docker","kconfig","html","css"}
SID = "doctrine-reference"
def gre(g):
    out=""; i=0
    while i<len(g):
        if g.startswith("**/",i): out+="(?:.*/)?"; i+=3
        elif g.startswith("**",i): out+=".*"; i+=2
        elif g[i]=="*": out+="[^/]*"; i+=1
        elif g[i]=="?": out+="[^/]"; i+=1
        elif g[i]=="{":
            j=g.index("}",i); out+="(?:"+"|".join(gre(x) for x in g[i+1:j].split(","))+")"; i=j+1
        else: out+=re.escape(g[i]); i+=1
    return out
def compile_globs(globs):
    inc=collections.defaultdict(list); exc=collections.defaultdict(list)
    for g in globs:
        neg=g.startswith("!"); g=g[1:] if neg else g
        tree="es" if g.startswith("es:") else "distribution"
        g=g[3:] if tree=="es" else g
        (exc if neg else inc)[tree].append(re.compile(gre(g)+r"\Z"))
    return inc,exc
def gm(comp,p,t="distribution"):
    inc,exc=comp
    return any(r.match(p) for r in inc.get(t,())) and not any(r.match(p) for r in exc.get(t,()))
doc=json.load(open("docs/reviews/slices.json"))
sl=[]
for s in doc["slices"]:
    sels=s.get("select",{}); sels=sels if isinstance(sels,list) else [sels]
    comp=[]
    for sel in sels:
        comp.append((set(sel.get("areas",[s["area"]])), compile_globs(sel["globs"]) if sel.get("globs") else None,
                     set(sel["reach"]) if sel.get("reach") else None, bool(sel.get("rest")), set(sel["tier"]) if sel.get("tier") else None))
    sl.append((s,comp))
ar=json.load(open("docs/reviews/areas.json")); ar=ar["areas"] if isinstance(ar,dict) else ar
DOCA=compile_globs([a for a in ar if a["area"]=="doctrine"][0]["globs"])
inv=json.load(open("docs/reviews/inventory.json"))
hd=inv["header"]["distribution"]
print("distribution head:",hd["head"]); print("distribution merge_base:",hd["merge_base"]); print("distribution upstream:",hd["upstream"],hd["upstream_head"])
cols=inv["columns"]; print("columns:",cols)
rows=[dict(zip(cols,r)) for r in inv["rows"]]
def match(row,areas,comp,reach,tier):
    if row["area"] not in areas: return False
    if reach and row["reach"] not in reach: return False
    if tier and row["tier"] not in tier: return False
    if comp is None: return True
    return gm(comp,row["path"],row["tree"])
def hits(row):
    non=[s["id"] for s,c in sl if any(not rest and match(row,a,cm,r,t) for a,cm,r,rest,t in c)]
    if non: return non,"non-rest"
    return [s["id"] for s,c in sl if any(rest and match(row,a,cm,r,t) for a,cm,r,rest,t in c)],"rest"
def nonrest_doctrine(p):
    return [s["id"] for s,c in sl if any(not rest and "doctrine" in a and cm is not None and gm(cm,p) for a,cm,r,rest,t in c)]
kof={s["id"]:s["k"] for s,_ in sl}
mine=sorted((r for r in rows if r["tree"]=="distribution" and hits(r)[0]==[SID]), key = lambda r:r["path"])
want=[l.strip() for l in open(sys.argv[1]) if l.strip()]
got=[r["path"] for r in mine]
print("mine:",len(got),"paths.txt:",len(want),"equal:",got==want)
print("only-mine:",sorted(set(got)-set(want))); print("only-paths.txt:",sorted(set(want)-set(got)))
c=collections.Counter
print("lines:",sum(r["lines"] or 0 for r in mine),"reach:",dict(c(r["reach"] for r in mine)),"tier:",dict(c(r["tier"] for r in mine)))
print("lang:",dict(c(r["language"] for r in mine)))
print("fork-own lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="fork-own"),"upstream-carried lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="upstream-carried"))
rd=[r for r in mine if r["language"] in CODE and r["tier"]!="vendor-carried" and r["reach"]!="unreached"]
print("read lines:",sum((r["lines"] or 0) for r in rd),"of which fork-own:",sum((r["lines"] or 0) for r in rd if r["tier"]=="fork-own"),"read rows:",[(r["path"],r["language"],r["lines"]) for r in rd])
print("overlap:",sum(1 for r in mine if r["overlap"]),"last_upstream_commit set:",sum(1 for r in mine if r["last_upstream_commit"]),"binary (lines None):",[r["path"] for r in mine if r["lines"] is None])
def grp(p):
    q=p.split("/")
    if len(q)==1: return p
    if q[0]=="docs":
        if len(q)==2: return "docs/*"
        if q[1]=="reviews" and len(q)>3: return "docs/reviews/"+q[2]+"/"
        return "docs/"+q[1]+"/"
    return q[0]+"/"
print("GROUPS (group: paths lines | fork-own paths lines | upstream-carried paths lines)")
g=collections.defaultdict(lambda:[0,0,0,0,0,0])
for r in mine:
    x=g[grp(r["path"])]; n=r["lines"] or 0; x[0]+=1; x[1]+=n
    if r["tier"]=="fork-own": x[2]+=1; x[3]+=n
    else: x[4]+=1; x[5]+=n
for k in sorted(g): print("  %-26s %4d %6d | %4d %6d | %4d %6d" % ((k,)+tuple(g[k])))
print("GROUPS TOTAL", len(mine), sum(v[1] for v in g.values()), "groups", len(g))
print("TSV"); print("\t".join(cols))
for r in mine: print("\t".join(str(r.get(k)) for k in cols))
print("TREE-SIDE (doctrine area by areas.json, less the doctrine non-rest slices' globs)")
for tf in sys.argv[2:]:
    ps=[l.strip() for l in open(tf) if l.strip()]
    der=sorted(p for p in ps if gm(DOCA,p) and not nonrest_doctrine(p))
    print(tf,"derived:",len(der),"equal to mine:",der==got,"only-derived:",sorted(set(der)-set(got)),"only-mine:",sorted(set(got)-set(der)))
print("CLAIMS")
byp={r["path"]:r for r in rows if r["tree"]=="distribution"}
named=["README.md","NAMING.md","CLAUDE.md","AGENTS.md","docs/decision-register.md","docs/blindspot-register.md","docs/friction-log.md","docs/reviews/inventory.json","docs/reviews/order.md","docs/reviews/plan-for-the-plan.md","docs/es-menu-map.md","docs/vm-qa-log.md","docs/releases/catalog.md","docs/work-logs/INDEX.md","docs/futros/2026-10-24-m6-doctrine.md",".github/sessions/saved-session-state-next.md",".claude/skills/futro/SKILL.md"]
for p in named:
    r=byp.get(p)
    if not r: print(p,"NOT IN INVENTORY"); continue
    h,kind=hits(r); print(p,"in-T39" if p in got else "not-in-T39",kind,[(x,kof[x]) for x in h],"tier",r["tier"],"lines",r["lines"],"lang",r["language"],"area",r["area"])
print("DOCS TREE BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["tree"]=="distribution" and r["path"].startswith("docs/"):
        h,kind=hits(r); q=r["path"].split("/")
        k=("docs/*" if len(q)==2 else "docs/"+q[1]+"/",tuple(h),r["area"])
        cnt[k]+=1; ln[k]+=(r["lines"] or 0)
for k,v in sorted(cnt.items()): print(v,"paths",ln[k],"lines",k)
print("DOCTRINE BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["area"]=="doctrine":
        h,kind=hits(r); k=(r["tree"],tuple(h),kind); cnt[k]+=1; ln[k]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:-kv[1]): print(v,"paths",ln[k],"lines",k)
PYEOF
W=/workspace/tmp/m6-coordinator/t11-research/tree; P1=2174265e9c; MB=c445081a59
IH=$(python3 -I -c 'import json; print(json.load(open("docs/reviews/inventory.json"))["header"]["distribution"]["head"])')
git -C "$W" ls-tree -r --name-only "$IH" > .qa-scratch/t39/tree-ih.txt
git -C "$W" ls-tree -r --name-only "$P1" > .qa-scratch/t39/tree-p1.txt
python3 -I .qa-scratch/t39/membership.py /dev/null > .qa-scratch/t39/block-1.txt
awk -F'\t' '/^TSV$/{p=1;next} /^TREE-SIDE/{p=0} p && $1=="distribution" {print $2}' .qa-scratch/t39/block-1.txt > .qa-scratch/t39/paths.txt
python3 -I .qa-scratch/t39/membership.py .qa-scratch/t39/paths.txt .qa-scratch/t39/tree-ih.txt .qa-scratch/t39/tree-p1.txt > .qa-scratch/t39/block-2.txt
awk -F'\t' '/^TSV$/{p=1;getline;for(i=1;i<=NF;i++)ix[$i]=i;next} /^TREE-SIDE/{p=0} p && $1=="distribution" && $ix["lines"]!="None" {print $ix["path"]}' .qa-scratch/t39/block-2.txt > .qa-scratch/t39/text.txt
wc -l .qa-scratch/t39/paths.txt .qa-scratch/t39/text.txt
/usr/bin/grep -E '^(distribution |mine:|only-|lines:|lang:|fork-own lines:|read lines:|overlap:|GROUPS TOTAL|\.qa-scratch/t39/tree-)' .qa-scratch/t39/block-2.txt | cut -c1-200
while IFS= read -r p; do git -C "$W" show "$P1:$p" | wc -l; done < .qa-scratch/t39/text.txt | awk '{s+=$1} END {print "wc -l, the text rows at the P1 hash:", s}'
while IFS= read -r p; do git -C "$W" show "$P1:$p" | /usr/bin/grep -c ''; done < .qa-scratch/t39/text.txt | awk '{s+=$1} END {print "grep -c, the text rows at the P1 hash:", s}'
while IFS= read -r p; do git -C "$W" show "$IH:$p" | /usr/bin/grep -c ''; done < .qa-scratch/t39/text.txt | awk '{s+=$1} END {print "grep -c, the text rows at the inventory head:", s}'
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t39/paths.txt | wc -l | sed 's/^/present at the merge base: /'
xargs -d '\n' -a .qa-scratch/t39/paths.txt git -C "$W" diff --shortstat "$MB" "$P1" -- | sed 's/^/MB..P1:/'
xargs -d '\n' -a .qa-scratch/t39/paths.txt git -C "$W" diff --shortstat "$IH" "$P1" -- | sed 's/^/IH..P1:/'
echo "(end)"
```
<!-- t39 block.sh end -->

Expected (the first pass, with no paths file, writes
`mine: 254 paths.txt: 0 equal: False` into `block-1.txt`; the block prints
these lines, R1 C16's, byte for byte; the `overlap:` line is cut at 200
characters by the block itself):

<!-- t39 block expected begin -->
```
  254 .qa-scratch/t39/paths.txt
  223 .qa-scratch/t39/text.txt
  477 total
distribution head: eb4763e3cc9bcd729830cd85f1719bbd4f28db10
distribution merge_base: c445081a59518f37d9776e5412dd7b14910696f7
distribution upstream: upstream/next c1f1746828ca47dfc751ffe44bb47b6b259883d7
mine: 254 paths.txt: 254 equal: True
only-mine: []
only-paths.txt: []
lines: 38598 reach: {'n/a': 254} tier: {'fork-own': 164, 'upstream-carried': 90}
lang: {'markdown': 113, 'text': 78, 'image': 39, 'json': 8, 'python': 1, 'css': 1, 'none': 1, 'other': 3, 'patch': 10}
fork-own lines: 28749 upstream-carried lines: 9849
read lines: 190 of which fork-own: 190 read rows: [('docs/pixelelated/art/source/generate.py', 'python', 180), ('docs/pixelelated/art/source/wordmark.css', 'css', 10)]
overlap: 0 last_upstream_commit set: 92 binary (lines None): ['docs/pixelelated/art/proofs/backgrounds.png', 'docs/pixelelated/art/proofs/boot-shutdown-640x480.png', 'docs/pixelelated/art/proofs/small
GROUPS TOTAL 254 38598 groups 15
.qa-scratch/t39/tree-ih.txt derived: 254 equal to mine: True only-derived: [] only-mine: []
.qa-scratch/t39/tree-p1.txt derived: 254 equal to mine: True only-derived: [] only-mine: []
wc -l, the text rows at the P1 hash: 38674
grep -c, the text rows at the P1 hash: 38675
grep -c, the text rows at the inventory head: 38598
present at the merge base: 92
MB..P1: 164 files changed, 28807 insertions(+), 75 deletions(-)
IH..P1: 9 files changed, 197 insertions(+), 120 deletions(-)
(end)
```
<!-- t39 block expected end -->

**The tree-side derivation reaches exactly the inventory's 254** at the
inventory head and at the P1 hash (the two `TREE-SIDE` lines); `92` are
present at the merge base; the merge base to the P1 hash is
` 164 files changed, 28807 insertions(+), 75 deletions(-)` over the 254, and
the inventory head to the P1 hash
` 9 files changed, 197 insertions(+), 120 deletions(-)`, all under
`docs/reviews/` (R1 § 2, § 5). `block-2.txt` also holds the TSV, `TREE-SIDE`,
`CLAIMS`, `DOCS TREE BY SLICE` and `DOCTRINE BY SLICE`, read with
`sed -n '/^CLAIMS$/,$p' .qa-scratch/t39/block-2.txt` (R1 C06):

```
CLAIMS
README.md in-T39 rest [('doctrine-reference', 39)] tier fork-own lines 23 lang markdown area doctrine
NAMING.md not-in-T39 non-rest [('doctrine-rules', 4)] tier fork-own lines 60 lang markdown area doctrine
CLAUDE.md not-in-T39 non-rest [('doctrine-rules', 4)] tier fork-own lines 202 lang markdown area doctrine
AGENTS.md not-in-T39 non-rest [('doctrine-rules', 4)] tier fork-own lines 351 lang markdown area doctrine
docs/decision-register.md not-in-T39 non-rest [('doctrine-rules', 4)] tier fork-own lines 738 lang markdown area doctrine
docs/blindspot-register.md not-in-T39 non-rest [('doctrine-rules', 4)] tier fork-own lines 1198 lang markdown area doctrine
docs/friction-log.md not-in-T39 non-rest [('doctrine-rules', 4)] tier fork-own lines 863 lang markdown area doctrine
docs/reviews/inventory.json not-in-T39 non-rest [('records', 46)] tier fork-own lines 134637 lang json area records
docs/reviews/order.md in-T39 rest [('doctrine-reference', 39)] tier fork-own lines 806 lang markdown area doctrine
docs/reviews/plan-for-the-plan.md in-T39 rest [('doctrine-reference', 39)] tier fork-own lines 499 lang markdown area doctrine
docs/es-menu-map.md in-T39 rest [('doctrine-reference', 39)] tier fork-own lines 989 lang markdown area doctrine
docs/vm-qa-log.md in-T39 rest [('doctrine-reference', 39)] tier fork-own lines 361 lang markdown area doctrine
docs/releases/catalog.md in-T39 rest [('doctrine-reference', 39)] tier fork-own lines 112 lang markdown area doctrine
docs/work-logs/INDEX.md not-in-T39 non-rest [('records', 46)] tier fork-own lines 1664 lang markdown area records
docs/futros/2026-10-24-m6-doctrine.md NOT IN INVENTORY
.github/sessions/saved-session-state-next.md not-in-T39 non-rest [('records', 46)] tier fork-own lines 355 lang markdown area records
.claude/skills/futro/SKILL.md not-in-T39 non-rest [('doctrine-skills', 38)] tier fork-own lines 483 lang markdown area doctrine
DOCS TREE BY SLICE
27 paths 9222 lines ('docs/*', ('doctrine-reference',), 'doctrine')
3 paths 2799 lines ('docs/*', ('doctrine-rules',), 'doctrine')
59688 paths 16262198 lines ('docs/audits/', ('records',), 'records')
6 paths 520 lines ('docs/futros/', ('records',), 'records')
50 paths 3551 lines ('docs/pixelelated/', ('doctrine-reference',), 'doctrine')
2 paths 323 lines ('docs/pr-series/', ('doctrine-reference',), 'doctrine')
970 paths 5625 lines ('docs/qa-frames/', ('records',), 'records')
64327 paths 6195761 lines ('docs/qa-logs/', ('records',), 'records')
2 paths 649 lines ('docs/ra-offline/', ('doctrine-reference',), 'doctrine')
15 paths 4906 lines ('docs/rasteratops/', ('doctrine-reference',), 'doctrine')
23 paths 1858 lines ('docs/releases/', ('doctrine-reference',), 'doctrine')
5 paths 415 lines ('docs/retros/', ('records',), 'records')
1 paths 17 lines ('docs/retrospective/', ('records',), 'records')
12 paths 5487 lines ('docs/reviews/', ('doctrine-reference',), 'doctrine')
1 paths 134637 lines ('docs/reviews/', ('records',), 'records')
28 paths 2323 lines ('docs/upstream/', ('doctrine-reference',), 'doctrine')
81 paths 27812 lines ('docs/work-logs/', ('records',), 'records')
DOCTRINE BY SLICE
254 paths 38598 lines ('distribution', ('doctrine-reference',), 'rest')
52 paths 12734 lines ('distribution', ('doctrine-skills',), 'non-rest')
36 paths 11414 lines ('distribution', ('doctrine-rules',), 'non-rest')
```

(`docs/futros/2026-10-24-m6-doctrine.md` is not in the inventory because it
was added by `12d163dd2c` on 2026-10-24, after the inventory head's
2026-10-23; by the records glob it would be T46's, R1 C18.) The lane's copy of
the block's output in `01-research-notes.md` § Scope is quoted from
`block-2.txt`, never retyped.

**The second block, the ledger/reference split** (`split.sh`, 46 lines, sha256
prefix `afb1909c5cdc6c88`, R1 C16; re-run byte for byte by R1 C20), run after
`block.sh` from the same directory: it reads `block-2.txt`, classes every row
by R1's rule (L1 every path under `docs/reviews/`; L2 the three files a
procedure appends to or generates; R the rest, by tier and language), sums
inventory lines and `grep -c ''` at the P1 hash per class and per group,
compares each row's blob at a tip `TIP` (default the P1 hash) in the
repository `G` (default the primary checkout), then derives the selector's
reach at the tip (R1 § 4, § 6). **R1's classes are R1's, not ruling (a)'s**:
R1's L2 holds three files where ruling (a)'s ledger rows add
`docs/pr-series/map.txt`, `docs/releases/rc-accept.txt`, `plans/` and the 31
binaries, and R1's `R-fork-assets` (41, by language `image`, `other` or
`none`) is not the binary set (31, by `lines` `None`); ruling (a)'s classes
are printed by § 5's `CARVE` lines. The text below is R1's `split.sh` byte for
byte:

<!-- t39 split.sh begin -->
```bash
W=/workspace/tmp/m6-coordinator/t11-research/tree; P1=2174265e9c; G=${G:-/workspace/repos/pixelelated/distribution}; TIP=${TIP:-2174265e9c}
cat > .qa-scratch/t39/split.py <<'PYEOF'
import collections
rows=[]; ix=None; p=False
for l in open(".qa-scratch/t39/block-2.txt"):
    l=l.rstrip("\n")
    if l=="TSV": p=True; continue
    if l.startswith("TREE-SIDE"): break
    if p and ix is None: ix={k:i for i,k in enumerate(l.split("\t"))}; continue
    if p: f=l.split("\t"); rows.append({k:f[i] for k,i in ix.items()})
L2={"docs/vm-qa-log.md","docs/cloud-sync-changelog.md","docs/releases/catalog.md"}
ASSET={"image","other","none"}
def cls(r):
    p=r["path"]
    if p.startswith("docs/reviews/"): return "L1-renovation-records"
    if p in L2: return "L2-running-records"
    if r["tier"]=="upstream-carried": return "R-upstream-carried"
    if r["language"] in ASSET: return "R-fork-assets"
    return "R-fork-reference"
def grp(p):
    q=p.split("/")
    if len(q)==1: return p
    if q[0]=="docs": return "docs/*" if len(q)==2 else "docs/"+q[1]+"/"
    return q[0]+"/"
c=collections.Counter(); n=collections.Counter()
with open(".qa-scratch/t39/classes.tsv","w") as out:
    for r in rows:
        k=cls(r); ln=0 if r["lines"]=="None" else int(r["lines"]); c[k]+=1; n[k]+=ln
        out.write("%s\t%s\t%s\t%s\n" % (k,grp(r["path"]),r["lines"],r["path"]))
for k in sorted(c): print("CLASS %-22s %4d paths %6d lines" % (k,c[k],n[k]))
print("LEDGER", sum(c[k] for k in c if k.startswith("L")), "paths", sum(n[k] for k in n if k.startswith("L")), "lines; REFERENCE", sum(c[k] for k in c if k.startswith("R")), "paths", sum(n[k] for k in n if k.startswith("R")), "lines")
for r in rows:
    if cls(r).startswith("L"): print("  ", cls(r), r["lines"], r["path"])
PYEOF
python3 -I .qa-scratch/t39/split.py
while IFS=$'\t' read -r k g l p; do [ "$l" = None ] && continue; printf '%s\t%s\t%s\n' "$k" "$g" "$(git -C "$W" show "$P1:$p" | /usr/bin/grep -c '')"; done < .qa-scratch/t39/classes.tsv | awk -F'\t' '{a[$1]+=$3; b[substr($1,1,1)" "$2]+=$3; t+=$3} END {for (k in a) printf "P1 grep -c class %s %d\n", k, a[k]; for (k in b) printf "P1 grep -c group %s %d\n", k, b[k]; print "P1 grep -c total", t}' | sort
echo "tip: $TIP"
while IFS=$'\t' read -r k g l p; do if git -C "$G" cat-file -e "$TIP:$p" 2>/dev/null; then if [ "$(git -C "$G" rev-parse "$TIP:$p")" = "$(git -C "$G" rev-parse "$P1:$p")" ]; then s=same; else s=changed; fi; else s=absent; fi; printf '%s %s\n' "$k" "$s"; done < .qa-scratch/t39/classes.tsv | sort | uniq -c
git -C "$G" ls-tree -r --name-only "$TIP" > .qa-scratch/t39/tree-tip.txt
python3 -I .qa-scratch/t39/membership.py .qa-scratch/t39/paths.txt .qa-scratch/t39/tree-tip.txt | /usr/bin/grep '^\.qa-scratch/t39/tree-tip\.txt' | python3 -I -c 'import sys, ast
l=sys.stdin.read(); a=ast.literal_eval(l.split(" only-derived: ")[1].split(" only-mine: ")[0]); b=ast.literal_eval(l.split(" only-mine: ")[1].strip())
print("at the tip the selector reaches:", l.split(" derived: ")[1].split()[0], "paths; added since P1:", len(a), "; of the 254 absent:", len(b))
print("  added under docs/reviews/briefs/:", sum(1 for x in a if x.startswith("docs/reviews/briefs/")))
for x in a:
    if not x.startswith("docs/reviews/briefs/"): print("  added", x)'
echo "(end split)"
```
<!-- t39 split.sh end -->

Expected with the defaults, **under `LC_ALL=en_US.UTF-8`**
(`LC_ALL=en_US.UTF-8 bash .qa-scratch/t39/split.sh`, R1 C16): the lines are
that locale's, because `split.sh`'s `| sort` under `LC_ALL=C` puts the three
upper-case `P1 grep -c group R` lines -- `LICENSE.md`, `README.md`,
`TRADEMARK.md` -- before the lower-case groups (proof C2, C3; X01; `v2 read`:
`diff` of this block against the run under `C` prints `29a30,32`, `38d40` and
`41,42d42`, against the run under `en_US.UTF-8` nothing), so stage A runs the
split under `en_US.UTF-8` while its `export LC_ALL=C` stays for the greps and
the counts; `block.sh` prints the same under both (K04):

<!-- t39 split expected p1 begin -->
```
CLASS L1-renovation-records    12 paths   5487 lines
CLASS L2-running-records        3 paths   4054 lines
CLASS R-fork-assets            41 paths   1765 lines
CLASS R-fork-reference        108 paths  17443 lines
CLASS R-upstream-carried       90 paths   9849 lines
LEDGER 15 paths 9541 lines; REFERENCE 239 paths 29057 lines
   L2-running-records 3581 docs/cloud-sync-changelog.md
   L2-running-records 112 docs/releases/catalog.md
   L1-renovation-records 165 docs/reviews/README.md
   L1-renovation-records 124 docs/reviews/areas.json
   L1-renovation-records 108 docs/reviews/assessment.md
   L1-renovation-records 386 docs/reviews/briefs/p1-survey.md
   L1-renovation-records 216 docs/reviews/build-path-read.md
   L1-renovation-records 113 docs/reviews/cross-reference.md
   L1-renovation-records 1515 docs/reviews/inventory.md
   L1-renovation-records 806 docs/reviews/order.md
   L1-renovation-records 449 docs/reviews/p1-tracking.md
   L1-renovation-records 499 docs/reviews/plan-for-the-plan.md
   L1-renovation-records 1048 docs/reviews/slices.json
   L1-renovation-records 58 docs/reviews/status.md
   L2-running-records 361 docs/vm-qa-log.md
P1 grep -c class L1-renovation-records 5564
P1 grep -c class L2-running-records 4054
P1 grep -c class R-fork-assets 1765
P1 grep -c class R-fork-reference 17443
P1 grep -c class R-upstream-carried 9849
P1 grep -c group L docs/* 3942
P1 grep -c group L docs/releases/ 112
P1 grep -c group L docs/reviews/ 5564
P1 grep -c group R docs/* 5280
P1 grep -c group R docs/pixelelated/ 3551
P1 grep -c group R docs/pr-series/ 323
P1 grep -c group R docs/ra-offline/ 649
P1 grep -c group R docs/rasteratops/ 4906
P1 grep -c group R docs/releases/ 1746
P1 grep -c group R docs/upstream/ 2323
P1 grep -c group R documentation/ 2160
P1 grep -c group R LICENSE.md 18
P1 grep -c group R licenses/ 7817
P1 grep -c group R plans/ 223
P1 grep -c group R README.md 23
P1 grep -c group R TRADEMARK.md 38
P1 grep -c total 38675
tip: 2174265e9c
     12 L1-renovation-records same
      3 L2-running-records same
     41 R-fork-assets same
    108 R-fork-reference same
     90 R-upstream-carried same
at the tip the selector reaches: 254 paths; added since P1: 0 ; of the 254 absent: 0
  added under docs/reviews/briefs/: 0
(end split)
```
<!-- t39 split expected p1 end -->

Expected with `TIP=e3fb3dfe00` (R1 C16): the same lines to `P1 grep -c total`,
then:

<!-- t39 split expected e3fb begin -->
```
tip: e3fb3dfe00
      8 L1-renovation-records absent
      3 L1-renovation-records changed
      1 L1-renovation-records same
      3 L2-running-records same
     41 R-fork-assets same
    108 R-fork-reference same
     90 R-upstream-carried same
at the tip the selector reaches: 328 paths; added since P1: 82 ; of the 254 absent: 8
  added under docs/reviews/briefs/: 82
(end split)
```
<!-- t39 split expected e3fb end -->

**At the lane's dispatch tip** the lane runs
`LC_ALL=en_US.UTF-8 G="$PWD" TIP=<MERGE_HASH's value> bash .qa-scratch/t39/split.sh`:
every line before `tip:` is the P1 tree's and must match the defaults' (R1 §
6; both runs under `en_US.UTF-8`, X01); the
`tip:` lines differ by whatever the coordinator's branch has moved. **By
ruling (p) no line reads `absent` there** -- the P1 branch is merged, so the
twelve `docs/reviews/` rows resolve -- and the selector's reach is the 254
plus every brief added under `docs/reviews/briefs/` since P1 (82 at
`e3fb3dfe00`, R1 C07; 83 at `a0fb117b8b`, this brief among them --
`selector reaches: 329 paths; added since P1: 83`, proof K19 -- so the
dispatch tip prints at least 83); the exact lines are `[unverified]` until
stage A prints them, and the lines that print are the record.

**The tool's own row, from the worktree** (ruling (g); R1 C02 ran the same
command from the clone):
`./tools/renovation-inventory --order --no-write --distribution "$W"` exits 0
with `50` lines, among them `slices: 46`, `rows: 134634 (inventory: 134634)`,
`unassigned: 0`, `ambiguous: 0` and the row
`39 doctrine-reference doctrine 254 paths 38,598 lines 190 read 190 fork-own 0 patch table`
(R1 C02, its spacing the tool's). Whether the worktree's copy prints the same
as the clone's is `[unverified]` (R1 ran it with the clone as its working
directory; the proof's run from the clone reproduced R1 C02's lines with the
status unchanged, K20); the lane records what prints and whether
`git status --short --ignored` moved (R1 C02: the clone's two ignored lines
before and after).

**Both line figures** (ruling (h)): **38,598** is the inventory's column over
the 254 (`GROUPS TOTAL 254 38598 groups 15`, R1 C16) and **38,675** the
`grep -c ''` of the 223 text rows at the P1 hash (`P1 grep -c total 38675`;
`wc -l` `38674`, the one unterminated file being upstream's
`licenses/XFree86-1.1.txt`: `wc -l 15 grep -c 16`, R1 C16, C17). They differ
because 9 of the 254 changed between the inventory head and the P1 hash, all
under `docs/reviews/`
(` 9 files changed, 197 insertions(+), 120 deletions(-)`, R1 C16), and the
inventory head's own `grep -c` over the same 223 is `38598` (R1 C16). **The 31
binaries are named and not counted**: `binary rows: 31 (gz 1, pdf 2, png 28)`
(R1 C19) -- the PNG proofs and rasters under `docs/pixelelated/art/`, the
interim icon under `docs/rasteratops/art/`,
`docs/upstream/2026-10-15-queue-reconciliation/originals.tar.gz`, and
`licenses/AETHERSX2.pdf` and `licenses/DRASTIC.pdf` (R1 § 2's list). A newline
count that includes them is not a line count (R1 C05's first version summed
them: superseded by C16).

**The bases** (R1 C01, § 0). The P1 tip `2174265e9c` is `next` plus 64
commits; the coordinator's branch at `e3fb3dfe00` is `next` plus 537 and does
not contain `2174265e9c` (it lacks 47 of the P1 branch's commits; merge base
`f5bea1696a`), so the lane's tree is their merge (ruling (g)). `next` is
`8ebaf8daad` (2026-10-17, *browser: record provider pages and GTK4 compilation
(#616)*). **The 242 paths outside `docs/reviews/` are byte-identical at
`2174265e9c`, `next` and `e3fb3dfe00`** (R1 C10: `3 L2-running-records same`,
`41 R-fork-assets same`, `108 R-fork-reference same`,
`90 R-upstream-carried same` at `e3fb3dfe00`); `next` has no `docs/reviews/`
(`12 files changed, 5564 deletions(-)` from the P1 tip), and at `e3fb3dfe00` 8
of the 12 are absent, 3 changed (`README.md`, `briefs/p1-survey.md`,
`plan-for-the-plan.md`) and 1 unchanged (`build-path-read.md`) (R1 C10).
Upstream is the local ref `upstream/next` `651150fc88` (2026-10-24, *Merge
pull request #3547*, R2 C16; not fetched, R3 § 2.5) and the merge base
`c445081a59`, ROCKNIX stable20261001 by `rc-accept.txt:7` (R2 § 1). This
paragraph is the one statement of the bases; § 1's rulings, § 5's expectations
and § 7's checkboxes cite it.

**The groups, by R1's `GROUPS` lines** (R1 C06: inventory lines; fork-own and
upstream-carried as paths and lines), with ruling (a)'s carve and **the read
order** `[proposed]` -- R5 § C stage B's order (the top-level files, the
reference groups, then the read-only and ledger rows), which no ruling names;
the dispatch comment may move it:

| Order | Group | Paths | Lines | Fork-own / upstream-carried | Ruling (a)'s carve | Read as |
| ---: | --- | ---: | ---: | --- | --- | --- |
| 1 | `README.md` | 1 | 23 | 1 / 0 | edit scope (ruling (c)) | the front page a player opens first |
| 2 | `TRADEMARK.md` | 1 | 38 | 1 / 0 | edit only where `NAMING.md` decides the word; findings #528 | legal and identity |
| 3 | `LICENSE.md` | 1 | 18 | 1 / 0 | read-only; findings #528 (ruling (k)) | legal |
| 4 | `docs/*` | 27 | 9,222 | 27 / 0 | edit scope less `docs/vm-qa-log.md` and `docs/cloud-sync-changelog.md` (ledger rows) | five families (R1 C17): `council-*` 9 / 1,463; `save-*`/`savestate-*` 7 / 1,129; `cloud-*` 3 / 3,921; `device-*` 2 / 656; other 6 / 2,053 (`es-menu-map` 989, `vm-qa-log` 361) |
| 5 | `docs/pixelelated/` | 50 | 3,551 | 50 / 0 | edit scope for the prose (the two art READMEs and `wordmark-system.md`); the 18 art text files and the binaries not (ruling (o), widened at version 2) | the rename plan, the cloud-folder guide and review, the site plans, the art tree |
| 6 | `docs/rasteratops/` | 15 | 4,906 | 15 / 0 | edit scope under `NAMING.md`'s historical clause (`docs/rasteratops/` keeps its name), less `p0-sweep-hits.txt` (a ledger row, open item 25) and the wordmark SVG and `Tiny5-OFL.txt` (ruling (o)); the icon binary not | current release records (L-30), the P0 sweep's evidence, pre-D-CLOUD-175 cloud work |
| 7 | `docs/releases/` | 23 | 1,858 | 23 / 0 | edit scope less `catalog.md` and `rc-accept.txt` (ledger rows) | versioning, device facts, candidate records, release notes, the PR stubs |
| 8 | `docs/ra-offline/` | 2 | 649 | 2 / 0 | edit scope | a dated design note, a rocknix.org draft |
| 9 | `docs/pr-series/` | 2 | 323 | 2 / 0 | `map.txt` a ledger row (ruling (e)); `es-review-guide.md` edit scope | the closed upstream series |
| 10 | `plans/` | 1 | 223 | 1 / 0 | ledger: one historical-plan row (ruling (d)) | the July conflict-wizard plan |
| 11 | `docs/upstream/` | 28 | 2,323 | 28 / 0 | read-only; findings #585 (ruling (n)) | the contribution queue, ten proxy patch drafts, a receipt packet with a `.tar.gz` |
| 12 | `documentation/` | 16 | 2,160 | 1 / 15 | read-only; the fork-own GENERIC_X64 table tabled, not edited (ruling (j)) | upstream's per-device emulator tables |
| 13 | `licenses/` | 75 | 7,817 | 0 / 75 | read-only; findings #528 | upstream's licence texts, two of them PDFs |
| 14 | `docs/reviews/` | 11 | 5,101 | 11 / 0 | ledger rows (ruling (a)) | the renovation's own documents |
| 15 | `docs/reviews/briefs/` | 1 | 386 | 1 / 0 | ledger row (ruling (a)) | P1's brief, `p1-survey.md` |

`GROUPS TOTAL 254 38598 groups 15` (R1 C06). **Living reference documents** --
edited often, still reference, each under its own rule -- stay in the edit
scope where ruling (a) puts them: `docs/es-menu-map.md` (79 commits;
D-UI-039), `docs/rasteratops/release-readiness.md` (128),
`docs/releases/next-candidate-work.md` (58), `docs/releases/device-facts.md`
(30) and `docs/releases/next-candidate-scope.md` (19) (R1 C09, § 4).

**Drift since the P1 tip and the briefs the selector would reach** (R1 § 5; R2
§ 0). At `e3fb3dfe00` the `rest` selector reaches **328** paths: 246 of the
254 plus **82** new briefs under `docs/reviews/briefs/`
(`added at e3fb3dfe00: 82 paths 45125 lines`, R1 C07). An inventory re-run on
that tree would put them into T39; **the membership stays the inventory's
254** at `eb4763e3cc` (the order and #686 say so), and the briefs are listed
in `01` as information, not as rows -- the coordinator's ledger under ruling
(a) in any case.

**The neighbours, and whose they are** (R1 C06's `CLAIMS`): `NAMING.md`,
`CLAUDE.md`, `AGENTS.md` and the three registers are **T4 `doctrine-rules`**'s
(k 4); `docs/reviews/inventory.json`, `docs/work-logs/INDEX.md` and
`.github/sessions/saved-session-state-next.md` are **T46 `records`**'s (k 46);
the skills are **T38 `doctrine-skills`**'s (k 38). Outside the inventory's
slices the owners are: the interface lanes (epic #700) for a stale menu-map
row (ruling (b)); #528 for licence and notice text; #585 for `docs/upstream/`
(ruling (n)); and the tools that read three ledger rows --
`tools/pr-stack-check` (`map.txt`), `tools/rc-preflight` (`rc-accept.txt`),
`tools/release-catalog` (`catalog.md`) -- whose inputs are the coordinator's
to change (ruling (a), (e)).

**Already found; do not re-find; take up.** Each is cited at its lines in `02`
with a disposition; the states are as R4 read them on 2026-11-01, re-read at
stage A. **Asks**: *read* (state the finding or the contract in `02`), *fix*
(an edit in the edit scope, under a stream brief at the stage-D pause),
*inherit* (the coordinator's or another owner's; § 8), *none* (recorded so the
lane does not re-find it):

| Found by | Lines at the tip | Take up as |
| --- | --- | --- |
| T38's brief `doctrine-skills.md:1465-1467` (R1 C15; R4 item 53): *"`docs/reviews/plan-for-the-plan.md` is its file ... any lead the read finds in the plan's description of the skills (§ 6b's stage lines, § 6c's reviewer row) is named for T39, not edited here"* | `docs/reviews/plan-for-the-plan.md` | **inherit**: a ledger row (ruling (a)); every plan lead T38's hand-back names is a `02` row with `inherited:coordinator`, never an edit (L-28) |
| T38's brief `:670-674` (R1 C15; R4 item 53): `docs/council-*.md` are T39's, the area's `rest` | the nine `docs/council-*.md`, 1,463 lines (R1 C17) | **read**: Q5's rows; L-12 |
| T4's streams brief `t4-streams.md:244-246`, T4 `05-punch-list.md:575` PL-24 *"Withdrawn ... the `docs/**` glob is a T39 (#686) lead"* (R1 C15; R4 item 50) | `.claude/rules/handheld-evidence.md`'s `docs/**` glob | **read** which reference documents the glob reaches; **inherit** the narrowing (L-35) |
| T4's boundary `doctrine-rules.md:262-265` (R1 C15; R4 item 49) | `docs/reviews/**` named apart from T39 | **inherit**: settled by ruling (a) (L-28) |
| T4 F-09 `02-forward-audit.md:128-131` (R4 item 51) | `CLAUDE.md:34`, `AGENTS.md:31`, `es-native-ui.md:37`, `instruction-files.md:122` | **inherit**: the rules' wording; T39's half is whether the policy document carries interface law (L-36) |
| T4's citation table `04-analysis.md:705-912` (R4 item 52) | every reference document with the rule and register lines citing it, at T4's hash; `device-builds.md` cites versioning at `:589` and the runbook at `:616` at `e3fb3dfe00`, not `:577`/`:604` (R4 C20) | **read**: Q4 starts from the table, re-read at the lane's ref with `git -C <worktree> show 6ec78bbf8c:<path>` |
| T37 L-17 and L-18 (R4 item 54) | `device-builds.md`'s EmulationStation fork lines; `CLAUDE.md`'s per-device patches (`1f9327d496`) | **none**: rules, swept by the coordinator |
| the doctrine futro's T39 lines `:7`, `:9-10`, `:52-53` (R1 C15; R5 C16) | -- | **read**: the kickoff addendum (§ 10) |
| #809 (R4 item 25) | the read count rendered three ways | **read**: § 1's figure, the inventory's rule |
| #810 (R4 item 26) | the lint's Local depth at epic tier | **read**: the lane's lint is the dispatch tip's |
| #42 (R4 item 27): `documentation-accuracy.md:48-52`'s *"blocks it"* | the rocknix.org page, outside the tree | **inherit**: L-34 |

## 3. The floor: read first, then the leads

**Read first**, in this order, each in this session, and
`01-research-notes.md` says which were read (`working-principles.md` §
Pre-flight). For this slice the reading **is** the slice's material: each
reference document is read once as a reader before it is read again as an
auditor (T4's and T38's shape), in § 2's order. The line numbers are the
coordinator worktree's at `e3fb3dfe00` as the research printed them; the lane
re-reads each with `grep -n` at `COHASH`:

1. **The rules**, each at the section named; the section's own sentence is not
   repeated here -- open it. **They are read, never edited** (D-WORKFLOW-189;
   T4's read, #651):

   | Rule | Line or section | Serves |
   | --- | --- | --- |
   | `NAMING.md` (T4's file, 60 lines, R3 C15) | `:3` (pixelelated lowercase); `:10-13` (pixelelated the OS name; ROCKNIX kept for retained labels, paths and upstream credit); `:14-18` (active Rasteratops folder names retired in reviewed batches, #509); `:19` (the character and the handle keep their names); `:30` (`p0-sweep-hits.txt` the baseline classification); `:31-32` (ROCKNIX assessed by consumer, not by grep); `:35` (the artifact-sweep allowlist); `:47-51` (the OS and the release are pixelelated; historical docs keep names and paths) (R2 L-06, L-11, L-19, § 0, § Identity; R3 § 2.2; R5 § A, § C, C21) | Q2, L-02, L-05, L-19 to L-23, L-25, L-30 |
   | `documentation-accuracy.md` | `:20-22` (the site is `ROCKNIX/rocknix.org`); `:48-52` (#42 *"the docs half of the upstream PR and blocks it"*) (R4 items 27, 55) | L-13, L-34 |
   | `es-native-ui.md`, `es-ui-style-guide.md` | D-UI-039 and the map's ownership lines (`es-native-ui.md:46-47`, `:49-56`); `es-ui-style-guide.md:59` (*"`es-menu-map-check` detects missing screen titles, not stale copy or screenshot coverage"*), `:66` (the visual-evidence section is the entrypoint) (R4 items 57, 58; the two lines by proof K96, X05) | L-08, L-32 |
   | `es-player-text.md` | § Conventions: the tiers and the banned words *configurations* and *everything* (D-UI-022) (R2 L-08) | L-07 |
   | `upgrade-and-install.md` | § Current cloud setup policy (D-CLOUD-175: no automatic cloud-folder migration) (R2's header) | L-04, L-10 |
   | `fork-workflow.md` | `docs/` and `plans/` are personal paths (`:17`, `:32`); the by-content recipe; `tools/pr-stack-check` builds from `docs/pr-series/map.txt` (`instruction-files.md:194`) (R4 item 61) | L-27, L-34 |
   | `release-candidates.md` | step 0 and step 6 (*"the catalog and the device facts current"*); `:38-40` (*"An acceptance is a line in `docs/releases/rc-accept.txt` citing a decided row. The device facts have no tool yet (#270)"*); `:92-93` (rocknix.org's documentation last, #42) (R2 L-03; R4 item 59) | L-15, L-26 |
   | `device-builds.md` | `:589` (*"New build identities follow `docs/releases/versioning.md`"*), `:616` (*"For a fresh card, follow `docs/device-flashing-runbook.md`"*) at `e3fb3dfe00` (R4 item 60, C20) | L-05, L-39 |
   | `engineering-practices.md` | § Verify design intent; § A name is not a behaviour (a total is the tool's line); § Guards must fail closed; `rc=$?` on its own line; § Nothing runs on a person's device (the masks; `:721` names `docs/device-testing-policy.md` § "Reading a device's output" the long form); `:66-69` (the queue *"reached from `docs/upstream/README.md`"*) (R4 item 62) | § 5, L-16, L-46 |
   | `issue-tracking.md`, `vm-first.md` | a device checkbox points at its row in `docs/releases/device-facts.md` (`issue-tracking.md:143`, `vm-first.md:36`, R4 item 63); `--repo pixelelated/distribution` always; *checkbox*, not *box* (D-QA-045) | L-15, every bug |
   | `instruction-files.md` | `:122-126` (*"Three documents"* load nowhere); `:181`, `:192` (`es-menu-map-check`; `release-catalog` writes `catalog.md` from `RECORD.txt`) (R4 items 56, 64) | L-36, L-15 |
   | `milestone-phase-naming.md` | the milestone body owns order (R2's header) | L-06, L-09 |
   | `adversarial-council.md` | the Mistral seat outside every run profile since scaffold#915 (R2 L-20) | L-12 |
   | `learning-capture.md`, `change-log.md`, `generic-x64-vm-testing.md` | § 3 (a procedure becomes a tool); the rules of the two running ledgers, `docs/cloud-sync-changelog.md` and `docs/vm-qa-log.md` (by the loaded index; R5 § 0 `[not read by a command]`) | the ledger rows |
   | `decision-register.md`, `bugs-are-agent-first.md`, `time-to-play.md`, `working-principles.md` | whole | § 9, every bug, the retro, every punch item's ladder stage |

2. **The register** -- § 9.
3. **The blindspots** (`docs/blindspot-register.md`, 1,250 lines, 5 matching;
   R4 C22): `:684-685` (*"drifts from the first comment on; a session that
   reads the copy and not the record inherits the drift"* -- the shape of the
   line-number citations of L-15 and L-32), `:1151` (*"a second copy
   drifts"*), `:938` (the `--allow-unchecked device-facts` FAIL) (R4 item 67).
4. **The friction log** (`docs/friction-log.md`, 891 lines, 11 matching; R4
   C22): `:137` (2026-10-03, a site screenshot push refused on
   `maxengel/rocknix.org`; guard *"explicit remote delivery/readback before
   claiming docs published"*), `:194` (an exact-image sweep *"inspect each
   context against consumed source/NAMING.md"*), `:384` and `:417` (stale
   packet READMEs; the session-stash fresh-reader review), `:558` (*"an
   unnamed canonical completion screen"*), `:800` (#528 notice03) (R4 item
   66). `:137` is the precedent for L-22; `:417` for every dated document that
   claims to be current (L-18).
5. **The checks that exist, and what each reads of the 254** (R3 § 1). **No
   check the fork runs reads a reference document for whether it misleads**
   (R3's answer):

   | Check | Reads the 254? | Its line at `e3fb3dfe00` | What its rc means here |
   | --- | --- | --- | --- |
   | `tools/rules-check` | **no**: the rules, the index, `CLAUDE.md`, `AGENTS.md`, the tool inventories | `rules-check: 30 rule files, every one front-mattered and indexed`, rc 0 (R3 C13) | **no evidence for the 254** (R5 § B item 4): it proves the lane broke nothing outside the slice |
   | `tools/register-check` | **4 of them**: its `LIVE` list names `docs/cloud-sync-changelog.md`, `docs/es-menu-map.md`, `docs/device-testing-policy.md` and `docs/device-flashing-runbook.md` among the 254 (R3 C12) | `register-check: 713 IDs, each once; every citation in the live documents names a row`, rc 0 (R3 C13) | a decision ID that names no row, in those 4 only; the rest is L-38 |
   | `tools/es-menu-map-check` | `docs/es-menu-map.md`, against the EmulationStation source at the shipped pin, by `git ls-tree`/`show` only (R2 C15; R3 C12) | `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing`, rc 0 (R3 C13; R2 C16) | screen titles only -- not rows, copy, order, French or frames (R3 § 2.4); not in fork CI (R3 C14); `CANNOT` without an ES checkout (exit 2) |
   | `tools/release-catalog --check` | `docs/releases/catalog.md` against `/workspace/artifacts/rocknix-images/*/RECORD.txt` (R3 C11) | `release-catalog: current (99 cuts)`, rc 0 (R3 C13) | a hand edit or a stale page, on this host only; `--write` is the only writer and **the lane never runs it** (ruling (a)) |
   | `tools/work-log-index --check` | not one of the 254 (`docs/work-logs/INDEX.md`) | `work-log index: current` (R3 C13) | the lane's own log entries |
   | `tools/rasteratops-identity-check` | `LICENSE.md`, `TRADEMARK.md` for non-empty text; the wordmark SVG's sha256 against the ES and theme copies (R3 C12) | not run: it requires `--es` and writes a temporary work directory (R3 § 1, C11, C13) | **an edit to `docs/pixelelated/art/pixelelated-wordmark.svg` fails it**: the art bytes are not edited here (ruling (o), widened at version 2; § 5) |
   | `tools/prose-check` | a page it is given; strict under `docs/releases/` | `self-test: PASS`; over the three release-note drafts rc 0 each, the 0.0.1 draft `PASS (0 fail, 1 warn)` (R3 C13, C21) | the site's voice in a draft; run by nothing automatically (R3 C14) |
   | `tools/lint-audit-artifacts` | **no**: the lane's folder | `usage: lint-audit-artifacts [-h] [--issue ISSUE] [--repo REPO] [--phase {pre-issue,resolution}]`; Local plans under the tip's audit folders `0 of 8` (R3 C13, C21) | the slice's folder; the Local PASS shape is proven at stage A (ruling (q)) |
   | `tools/forbidden-terms-check --stdin` | yes | over the 215 text paths at the tip `forbidden-terms-check: 0 hits on stdin`, rc 0; empty input rc 0; a planted `FORBIDDEN_PATTERNS` token `1 line(s) on stdin carry a listed word`, rc 1 (R3 C20) | **rc 0 is evidence only beside its positive**: the tool honours `FORBIDDEN_PATTERNS` before reading the private list (R3 C12) |
   | `.githooks/pre-commit`, `commit-msg`, `pre-push` (`guard-lib`) | added lines | not run; `guard-lib:31-32` loads `secret-patterns` (R3 C20); `docs/` and `plans/` are personal paths refused only on `pr/*` (R3 C14) | a credential-shaped or listed word added to a document |
   | `.github/workflows/fork-checks.yml`, `fork-wordlist.yml` | through `register-check` (4 documents); the wordlist over the tree (R3 C14) | -- | **no CI step runs `es-menu-map-check`, `release-catalog`, `prose-check`, `rasteratops-identity-check` or any link or path check** (R3 § 1) |
   | `tools/box-check`, `tools/ceremony-check`, `.githooks/hooks-test` | no | not run by any research file `[unverified]` | the lines that print at stage A are the record |

   **There is no `tools/docs-check`**: R3 § 2.9 proposes one in
   `tools/rules-check`'s style. This lane writes **`tools/t39-checks.sh`**
   FAIL-first under its audit folder (§ 5), and promoting it to a fork tool is
   a Backlog the hand-back names, with the two fork-only tool lists and the
   tool index beside it (R5 § A; R3 § 2.9); whose slice writes the fork tool
   -- T10 `tooling-guards` or a later one -- is the coordinator's call (R3 §
   2.9).
6. **T4's audit**, on its branch, read with
   `git -C <worktree> show 6ec78bbf8c:<path>` (T4's tip, R4 § 4;
   `origin/feature/m6-doctrine-rules-651` recorded at stage A as whichever
   line prints, R5 § B item 3): its `04-analysis.md:705-912` (every reference
   document with the rule and register lines citing it, R4 item 52),
   `02-forward-audit.md:128-131` (F-09, R4 item 51), `05-punch-list.md:575`
   (PL-24, R4 item 50) and its `second-opinions/review-plan.json`, the Local
   plan § 5's `# STAGE A` lints.
7. **T38's lane**: `feature/m6-doctrine-skills-685` (`98019cea9f` locally and
   on `origin`, R5 C17), its stage-A checkpoint accepted (R5 C18); the plan
   leads its hand-back names for T39 (R4 item 53) are read when it reports,
   and each becomes a `02` row (§ 2's take-up table).
8. **Other lanes' refs**: each is read at stage A and recorded as whichever
   line prints (a hash or `fatal:`), never copied from here, and none is a
   stop (R5 § B item 3).
9. **The issues**: #686's own body and comment; #807, #651, #685; #528, #585,
   #509, #511, #344, #42; #359, #360, #335, #334, #338, #947; #270, #964,
   #1094, #1100, #1126; #1013, #963, #273; #576, #620; #965, #682, #1216,
   #667, #570; #131, #507, #508, #515, #533; #11, #23, #134; #333, #256, #645
   (R2 C12, C14, C20, C23; R4 § 3). The lane re-reads each with
   `gh --repo pixelelated/distribution issue view` at stage A and records the
   states it saw; a sentence it quotes from an issue goes through § 5's mask.
10. **Time to play: untouched.** No path of the 254 reaches an image, so
    neither number moves (R5 § C stage G, proposed); the retro says so in
    those words.
11. **The walks, the French catalog, the ES tests**: none reaches the 254; a
    document claim only a frame could settle is the interface lanes' evidence
    route (R3 § 6; ruling (b)).

**The leads, one line each, in the brief's own numbering** -- `R2 L-<nn>` is
R2's numbering, never this table's; R3's four dead-path candidates (one real
absent in-tree path, `packages/rocknix`, and three names ruled external, X02),
R3's
retired-procedure hits, R4's three documents most likely to change and R4's
contradictions are folded in where they fall. Nothing here was tested by this
lane; a lead is a fact of the lines until the lane's proof says more.
**`proved`** is the research's column: `tree` (read at the hash), `tool-run`
(a command's output shows it), `record` (an issue's or a row's state),
`row vs doc` (two texts disagree). **Every lead is FAIL-first**: its check
line prints the defect at the tip and must print nothing, or the corrected
line, after its disposition lands -- for a `fix` after the stream's commit,
for any other disposition after the owner acts (the lane records the line at
the tip only). Each gets its `git log -S` (or `git log -L` over its lines)
before it is called a defect (`engineering-practices.md` § Verify design
intent). **Every check is a `git show`, `git grep`, `git ls-tree`,
`git cat-file` or `git diff` at a hash, a `gh --repo pixelelated/distribution`
read, a `t39-checks.sh` step, or a read -- never a fetch, a guest, a build or
a keyed call** (ruling (q)). `HEAD` in a check line is the lane's worktree at
the stage named; `W` is § 2's clone; a `\|` inside a table cell is Markdown's
escape for `|`, and the lane types `|`. **The disposition column is the closed
set of § 6: `fix`, `inherited:<owner>`, `ledger`, `#528`, `#585`.**

| Lead | Lines at the tip | Shape | proved | Check (FAIL-first) | Q | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| **L-01** | `docs/reviews/README.md:10-12`, `plan-for-the-plan.md:15,223,224,234,245,258,259`, `briefs/p1-survey.md:60-61,306-337,380-381`, `build-path-read.md:147` (R2 L-01) | **the renovation's own README and plan name files and tools absent at `e3fb3dfe00`**: `order.md`, `inventory.json`, `status.md`, `slices.json`, `tools/renovation-inventory`, `-status`, `-drift`; present only at `2174265e9c`, which `e3fb3dfe00` does not contain (R2 C6, C10, C12) | tree | `for p in docs/reviews/{README.md,areas.json,assessment.md,briefs/p1-survey.md,build-path-read.md,cross-reference.md,inventory.md,order.md,p1-tracking.md,plan-for-the-plan.md,slices.json,status.md} tools/renovation-{inventory,status,drift}; do git cat-file -e "HEAD:$p" 2>/dev/null \|\| echo "MISSING $p"; done` -- R2's seven-name form printed seven `MISSING` at `e3fb3dfe00`; **at the dispatch tip it prints no line** (ruling (p)) | Q6 | **ledger**: the coordinator's, resolved at dispatch (ruling (p)); the line printed at stage A is the record |
| **L-02** | `README.md:7-10` (R2 L-14; R4 item 16) | **the front page sends a player to a release with no pixelelated release**: *"Updates for this release are manual; use the instructions attached to the [release]"*, while `gh release list` printed `rc1-20260929`, `dev-20260827`, `dev-rk3326-20260819` (R2 C25) and the page carries seven ROCKNIX-era releases, the newest *ROCKNIX RC1 (2026-09-29)* (R4 C25); #344 OPEN (R2 C12) | tool-run, record | `git show HEAD:README.md \| $G -c 'instructions attached'` prints `1` at the tip and `0` after; the corrected sentence names the true state (no 0.0.1 release published yet; #344) beside `gh release list --repo pixelelated/distribution --limit 3`'s line at the fix's date | Q4, Q7 | **fix** (ruling (c)) |
| **L-03** | `docs/device-testing-policy.md:5` (R2 L-05) | **a decided row called open**: *"**Open:** D-QA-016 (a dedicated QA handheld and accounts, #131)."*; D-QA-016 decided at `decision-register.md:249` (2026-09-13) and D-QA-027 at `:327` (2026-09-17: the RG35XX SP is the dedicated QA handheld); #131 `CLOSED 2026-09-20` (R2 C23, C26) | row vs doc | `git show HEAD:docs/device-testing-policy.md \| $G -c -E 'Open:.*D-QA-016'` prints `1` at the tip and `0` after | Q4 | **fix** (ruling (l)); `vm-first.md`'s sentence on D-QA-016 is T4's: **inherited:coordinator** |
| **L-04** | `docs/rasteratops/cloud-layout.md:16`, `docs/releases/pr/08-saves.md:5` (R3 § 2.3, § 7 item 4) | **a retired script in the present tense**: *"`cloud_migrate_layout` derives the destination from the shipped defaults."*; *"... saves root, layout migration and log scrub scripts"*; the product tree has none (`product-tree hits for cloud_migrate_layout (projects packages scripts tools): 0`, R3 C24); D-CLOUD-175 retired it (`decision-register.md:642`, R4 item 13) | tree, row vs doc | `git grep -n -E 'cloud_migrate_layout\|layout migration' HEAD -- docs/rasteratops/cloud-layout.md docs/releases/pr/08-saves.md` prints the two lines; after the fix each file also carries a sentence naming the retirement: `git grep -c 'D-CLOUD-175' HEAD -- <the two files>` prints a count of at least 1 for each, where it printed `0` and `0` at `a0fb117b8b` (proof K45; open item 7's first half settled). The other reference-class hits -- `docs/cloud-vocabulary-audit.md:189`, `docs/rasteratops/cloud-folder-state-table.md:46,61` (line-cited reads of the script), `docs/rasteratops/release-readiness.md:874`, and `docs/pixelelated/cloud-folder-flow-review.md:272`, a hit of R3's looser heuristic (*folder migration*: *"without scheduling a folder migration"*), consistent with the retirement and not of L-04's check words (proof K46, X11) -- and R3's join/follow heuristic's 10 reference lines are read and classed (R3 C18, C19; the 10 unread `[unverified]`) | Q1, Q3 | **fix** (ruling (l)) |
| **L-05** | `docs/device-flashing-runbook.md:3`, `:5` and the rest of its 21 `ROCKNIX` lines (R2 L-06) | **the OS named ROCKNIX throughout**: `ROCKNIX` 21 lines, `pixelelated` 0 (R2 C20); last commit 2026-09-20, before D-WORKFLOW-144; *"Use this for every fresh ROCKNIX card"*, *"For devices already running ROCKNIX"*; `CLAUDE.md` names the runbook for physical flashing | tool-run, row vs doc | `git show HEAD:docs/device-flashing-runbook.md \| $G -c ROCKNIX` prints `21` and `\| $G -c pixelelated` prints `0` at the tip; after the fix the second is non-zero and every remaining `ROCKNIX` line is classed in `02` as a retained label, path or the upstream project (`NAMING.md:3,10-13`); D-INFRA-008 (`:94`, bench documentation) and #1100's SM8550 gap are cited, not fixed (R4 item 5) | Q2, Q4 | **fix** where `NAMING.md` decides the word; the rest recorded (ruling (l)) |
| **L-06** | `docs/cloud-save-integrity.md:4` (R2 L-07) | **an M7 order of closed issues**: *"M7 order remains #515 -> #508 -> #507 -> assembled firmware..."*; each `CLOSED 2026-10-08` (R2 C12, C20); the milestone body owns order (`milestone-phase-naming.md`) | record | `git show HEAD:docs/cloud-save-integrity.md \| $G -c 'M7 order remains'` prints `1` at the tip and `0` after | Q4 | **fix** |
| **L-07** | `docs/backup-contents.md:3-5` (R2 L-08) | **labels the pin does not ship, in banned words**, in a file that calls itself the *"source of truth for the user-facing docs on rocknix.org"*: **BACKUP CONFIGURATIONS**, **RESTORE FROM BACKUP**, **BACK UP / RESTORE EVERYTHING**, each `0` at the pin `16dbac5211` with the `_("` prefix (R2 C13, C20) | tool-run | `for s in 'BACKUP CONFIGURATIONS' 'RESTORE FROM BACKUP' 'RESTORE EVERYTHING' 'BACK UP / RESTORE'; do printf '%s %s\n' "$s" "$(git -C ~/Development/emulationstation-next grep -F -c "$s" 16dbac5211 -- es-app es-core \| awk -F: '{s+=$NF} END {print s+0}')"; done` -- the bare strings, which R2 did not grep (R2 L-08 asks for them before a label is called gone); after the fix every label the file names prints a non-zero count at the pin and *configurations* and *everything* are gone from it | Q2, Q4 | **fix** (labels re-derived from the pin) |
| **L-08** | `docs/es-menu-map.md:758`, `:806`, `:817` (R2 L-09) | **a dated journal that says "pending" for closed work**: `### Pending nonvisual allocator candidate (#570)`, `## Pending allocator candidate: constrained handoff proof (#570)`, `### M7 setup candidate under qualification — October 13` (R2 C13); #570 `CLOSED 2026-10-14` (R2 C14); from `:711` to the end `MAP-TAIL-711-END lines=279` under `MAP-TAIL-headings=16` (R2 C26) | record | `git show HEAD:docs/es-menu-map.md \| $G -n -E '^#+ .*(Pending\|under qualification)'` prints the three lines at the tip; after the fix the two #570 headings say closed and the third's issue state is read and said; `tools/es-menu-map-check` still prints `0 missing` | Q4, Q7 | **fix**: the headings only, no restructuring (ruling (b)); the journal's home is § 4 question 1 |
| **L-09** | `docs/releases/next-candidate-work.md:4` (R2 L-12) | **a superseded baseline**: *"the last tested device build, `0.0.1-dev+20261011T222153Z.gbc9dfe8141d9`"*, while `device-facts.md` records a 2026-10-16 transfer to `077197` and `support-matrix.md` says the three images *"share distribution source `077197e6cd`"* (R2 C14, C19, C26) | row vs doc | `git show HEAD:docs/releases/next-candidate-work.md \| $G -n 'baseline is'` prints `:4` at the tip; after the fix the line names the current baseline or the file is headed as the dated reconciliation it is | Q4 | **fix** |
| **L-10** | `docs/pixelelated/cloud-folders.md:32-35` (R2 L-13; R4 item 13) | **the player's guide ends in internal release status**: *"Publish it with the qualified build ... The accepted H700 and SM8550 artifacts from earlier on 2026-10-07 still contain the previous migration flow"*; #508 `CLOSED 2026-10-08`; `site-plan.md:3-5` says the guides are published; `README.md:22` sends players here (R2 C23, C26) | tree, record | `git show HEAD:docs/pixelelated/cloud-folders.md \| $G -c 'prepared release documentation'` prints `1` at the tip and `0` after | Q7 | **fix** |
| **L-11** | `docs/rasteratops/release-readiness.md` 122, `docs/releases/next-candidate-work.md` 46, `next-candidate-scope.md` 22, `docs/es-menu-map.md` 12, `cloud-folder-flow-review.md` 9, `support-matrix.md` 8, `docs/upstream/README.md` 8, `device-facts.md` 2, `versioning.md` 1, `0.0.1-release-preparation.md` 1 (R2 L-16) | **words and numbers run together** (*"approved8b511→bc9dfe"*, *"Candidate ESf7b71db0a"*, *"all18"*, *"October14"*): a heuristic, not a check (R2 C22) | tool-run | `$G -o -E '\b(approved\|completed\|verified\|primary\|about\|at\|on\|in\|of\|for\|and\|all\|with\|by\|from\|October\|Oct\|replacement\|glslang)[0-9]'` per file over `HEAD`'s text: the counts above at the tip; after the fix each hit in the edit scope is read and either spaced or kept as an identifier (`replacement02` in `rename-plan.md:16` is a name) with its class in `02` | Q7 | **fix** in the edit scope; `docs/upstream/README.md`'s 8 **#585**; `rc-accept.txt:17`'s `glslang16.6.0` **ledger** (L-26) |
| **L-12** | `docs/council-limits.md` (54 lines), `docs/council-mistral-counter.md:3` (R2 L-20) | **council notes about a retired seat and with no reader**: `council-limits.md` has `0/0/0/0` inbound (R2 C21); the counter note documents `scripts/council-count-mistral.mjs` (`PRESENT`, R2 C26) for the Mistral seat, outside every run profile since scaffold#915 | tree | `git show HEAD:docs/council-mistral-counter.md \| $G -c -i -E 'sealed\|retired\|scaffold#915'` prints `0` at the tip (proof K54; open item 8 settled) and at least `1` after the banner | Q5, Q6 | **fix**: a banner on the counter note; retiring `council-limits.md` is § 4 question 2 |
| **L-13** | `docs/technical-appendix-cloud-sync-and-offline-achievements.md` (3 lines), `docs/pixelelated/site-plan.md:70`, `docs/releases/rocknix-org-pr-cloud-sync-wifi-achievements.md:5`, `docs/ra-offline/rocknix-org-offline-achievements.md:3` (R2 L-18; R3 § 2.1, § 7 item 2) | **rocknix.org drafts naming pages this tree cannot check**: seven rocknix.org pages (R3 § 2.1's external class) and `docs/cloud-saves-native-wizard`, a branch of the site checkout (`site-plan.md:69-70` *"clean on `docs/cloud-saves-native-wizard`"*; the appendix `:3` *"on the site checkout's `docs/cloud-saves-native-wizard` branch"*): an `allow-legit` `external` entry, not a dead path (proof K55, X02; disagreement 11 settles for R2) | tree | `git cat-file -e HEAD:docs/cloud-saves-native-wizard 2>/dev/null \|\| echo ABSENT` prints `ABSENT` (R3 C17; the name is the site repository's branch, `external`); whether the pages exist in `ROCKNIX/rocknix.org` is `[unverified]` (outside the tree; a read of a local checkout, if one is present, by `git -C <it> ls-tree` at its default branch and never a fetch, settles it); after the fix each named page carries its repository and branch | Q6 | **fix**: the repository named beside each page; retiring the stubs (`rocknix-org-pr-...md` has `0/0/0/0` inbound, R2 C21) is § 4 question 2 |
| **L-14** | `docs/pixelelated/art/README.md:20-21` (R3 § 2.1 candidate 1, § 7 item 1) | **another repository's generator tool, named as such**: *"`pixelelated-wordmark.svg` is generated by `pixelelated/splash` `tools/pixelelated-wordmark` from the unmodified Tiny5 Duo LCD 2.007 font"* -- the splash repository's tool, not this tree's (proof K56, X02); the generator among the 254 is `docs/pixelelated/art/source/generate.py` (R3 C10, C17) | tree | `git cat-file -e HEAD:tools/pixelelated-wordmark 2>/dev/null \|\| echo ABSENT` prints `ABSENT`, and `git show HEAD:docs/pixelelated/art/README.md \| sed -n '20,21p'` prints the sentence naming `pixelelated/splash`; the `paths` step carries it as an `allow-legit` `external` entry | Q6 | **record**: a § Coverage row reading `none` -- the README already says where the tool lives (X02) |
| **L-15** | `docs/releases/device-facts.md:7` and its rows (R2 L-03; R4 items 9, 38, 39) | **the device facts point to a catalog with none of their cuts, and their rows are cited by number**: *"The cuts themselves are [catalog.md]"*; `catalog-has-<hash>: 0` for `bc9dfe8141`, `077197`, `8b511`, `a0f60255ab` (R2 C15); the catalog's newest row `x64-all-20261002-b2378d9c33` (`catalog.md:11`), last regenerated `3d7c075f63` 2026-10-02, while `release-catalog: current (99 cuts)` (R3 C13) is current against the `RECORD.txt` files present (#964: *"395 kept folders ... without a `RECORD.txt`"*, R4 item 39); rows cited by number by #1100 (`L17-L19`) and #1126 (*"line 31"*), a row #1094 says is missing; **D-WORKFLOW-046** (`:390`, *"a tool says when they are not"*) against `release-candidates.md:38-40` (*"no tool yet (#270)"*) | tool-run, row vs doc | `for h in bc9dfe8141 077197 8b511 a0f60255ab; do git show HEAD:docs/releases/catalog.md \| $G -c "$h"; done` prints `0` four times; `git show HEAD:docs/releases/device-facts.md \| sed -n '7p;17,19p;31p'` recorded before and after any edit, so no line an issue cites by number moves | Q4, Q6 | **fix**: `device-facts.md:7`'s pointer says where the cuts after 2026-10-02 are recorded, written without moving a cited row; **inherited:#270** (the tool and the row-against-rule); **inherited:coordinator** (the catalog's regeneration and #964; the lane never runs `--write`) |
| **L-16** | `docs/device-testing-policy.md:94` `## Reading a device's output` (R4 item 6, C21) | **a mask a reader copies, short of the flag form**: the policy's long form lacks `engineering-practices.md`'s widened mask -- the flag form added 2026-10-30 is absent at `a0fb117b8b` (`--(token` count `0`, proof K58; R4 item 6) -- so a reader masking a command line by the policy prints a credential | tool-run | `git show HEAD:docs/device-testing-policy.md \| $G -c -F -e '--(token'` prints `0` at the tip (K58) and at least `1` after the fix | Q3 | **fix** (the check printed `0`, K58; open item 10 settled) |
| **L-17** | `docs/conflict-wizard-ia.md` (323 lines) (R4 item 4) | **the wizard's IA against its decided rows**: D-CLOUD-024 (`:62`), -027 (`:67`), -032 (`:84`), -041 (`:98`, *"the cloud is the left column, so KEEP LEFT keeps the cloud copy"*) and #23's *"to be revised to rev 5 as listed in #134"*; the IA is at **Rev 6 (2026-09-12)** (`:19`), past #23's rev 5 (`:29`; #23 still says `rev 5`), proof K59; its words are `KEEP BOTH` 5, `KEEP LEFT` 2, `KEEP RIGHT` 2, no `MERGE` (R2 C22; K59); the text against the four rows is unread `[unverified]` | tree | `git show HEAD:docs/conflict-wizard-ia.md \| $G -n -i -E 'rev(ision)? ?[0-9]'` prints `19:> **Rev 6 (2026-09-12).**` and `29:> **Rev 5 (2026-09-06).**` (K59), read against #134's list | Q4 | **fix** where a sentence contradicts a decided row and no screen change owns it; otherwise **inherited:the interface lanes** |
| **L-18** | the 17 low-inbound reference documents (R2 § 3) | **the lens's sharpest rows**: `LOW-INBOUND-SUM files=17 lines=2135` (R2 C26) -- the plan (223), `backup-contents` (100), `save-manifest-alignment-review` (98), three save-history pieces (92/40/111), `savestate-compat-test` (117), `rules-sweep` (277), the technical appendix (3), `council-limits` (54), the rc1 note (38), `rocknix-org-pr-...` (13), `es-review-guide` (124), `candidate-source-plan` (80), the proxy design note (590, 15 backticked paths of another tree, R3 § 7 item 9), `rocknix-org-offline-achievements` (59), `cloud-layout` (116) | tool-run | the generator's `R/O/D/W` inbound columns re-derive R2 C21's counts at `HEAD`, and its line prints the number of documents with no inbound name and at most one `docs/` reference outside the ledgers (R2 C26's `files=17`); after the fixes every one of them that is a dated record says so in its first line | Q5, Q7 | **fix**: a dated first line where a record presents itself as current (R5 § A: *"a dated record misleads only where it presents itself as current"*); retirement is § 4 question 2 |
| **L-19** | `docs/rasteratops/art/README.md:8` (R3 § 2.1 candidate 2) | **another repository's tool in a historical artifact's README, named as such**: *"generated from Tiny5 Duo by `rasteratops/splash`'s `tools/rasteratops-wordmark`"* (proof K56, X02); `NAMING.md`: historical docs and artifacts keep their names and paths | tree | `git cat-file -e HEAD:tools/rasteratops-wordmark 2>/dev/null \|\| echo ABSENT` prints `ABSENT`, and `git show HEAD:docs/rasteratops/art/README.md \| sed -n 8p` prints the line naming `rasteratops/splash`; the `paths` step carries it as an `allow-legit` `external` entry | Q6 | **ledger** (a historical artifact, kept; the tool is the splash repository's, X02) |
| **L-20** | `docs/rasteratops/p0-read.md`, `p0-sweep.md` (R3 § 2.1 candidate 4) | **a short path in dated P0 records**: `packages/rocknix` (R3 C17); `NAMING.md:30` names `p0-sweep-hits.txt` the baseline classification (R2 § 0) | tree | `git cat-file -e HEAD:packages/rocknix 2>/dev/null \|\| echo ABSENT` prints `ABSENT` | Q6 | **ledger** (a dated record) unless it presents itself as current |
| **L-21** | `docs/rasteratops/raofflineproxy-refresh.md:180,188`, `docs/rasteratops/cloud-folder-state-table.md:38` (R3 § 2.2, § 7 item 5) | **Rasteratops as the OS's identity**: *"Rasteratops, so automatic account discovery could not find system.cfg"*, *"Rasteratops identity above"*; *"`N` is `/Rasteratops/Saves`"* (R3 C18, C19) | tree | `git show HEAD:docs/rasteratops/raofflineproxy-refresh.md \| sed -n '180p;188p'` and `git show HEAD:docs/rasteratops/cloud-folder-state-table.md \| sed -n 38p` print the lines | Q2 | **ledger** (a record of its date) unless its tense presents the identity as current: then **fix** (a sentence naming D-WORKFLOW-144) |
| **L-22** | `docs/pixelelated/site-plan.md:72` and its `Development/rocknix` line (R2 § Identity; R3 § 2.2, § 7 item 3) | **a current plan naming a retired owner and path**: *"Remotes still name `maxengel/rocknix.org`"*; currency not settled (R2); #511 OPEN (R2 C20); the friction log's `:137` | tree, record | `git show HEAD:docs/pixelelated/site-plan.md \| $G -n -E 'maxengel\|Development/rocknix'` prints the two lines; #511's last comment read for the remote's state | Q4 | **fix** where the sentence misstates the present; otherwise **inherited:#511** |
| **L-23** | `docs/cloud-sync-changelog.md:706-735` (R2 § 2 Not leads; R3 § 2.2) | **`maxengel/rocknix` links that resolve only by redirect** (`gh api repos/maxengel/rocknix` -> `pixelelated/distribution`, R2 C22): the four sit in the changelog's dated entries, a ledger row; `github.com/(rasteratops\|maxengel)` is `0/0` in R3's reference class and `4/1` in its ledger class (R3 C18) | tool-run | `xargs -d '\n' -a .qa-scratch/t39/paths.txt git grep -c -E 'github\.com/(rasteratops\|maxengel)' HEAD --` prints `HEAD:docs/cloud-sync-changelog.md:4` alone (proof K64 over the 223 at P1: `2174265e9c:docs/cloud-sync-changelog.md:4`; open item 12 settled); the bare string `maxengel/rocknix` is on 27 lines in 5 files (K64: the changelog `:4`, `docs/pixelelated/site-plan.md` 1, `docs/rules-sweep-2026-09-12.md` 1, `docs/upstream/raofflineproxy/image-completeness/fix.patch` 1, and 20 in `docs/rasteratops/p0-sweep-hits.txt` -- the sweep's hits as it found them, a ledger row by open item 25) | Q2 | **ledger**; ruling (l)'s fix applies to any instance the identity step finds in the edit scope; `rename-plan.md:24` (the account, allowed), `rules-sweep-2026-09-12.md:113` (dated) and `docs/upstream/raofflineproxy/image-completeness/fix.patch:64` (**#585**, kept; the full path by X12) are recorded (R2 § Identity) |
| **L-24** | `plans/conflict-resolution/vita-style-conflict-resolution.md:8-9`, `:13` (R2 L-10) | **the one plan, superseded and unmarked**: *"Choices: KEEP CLOUD / KEEP DEVICE / MERGE"*, *"Merge = re-slot"*, captured 2026-07-26; the IA's words have no `MERGE` (R2 C22); `_("KEEP CLOUD` and `_("KEEP DEVICE` `0` at the pin (R2 C20); no rule, root document, register line, map or IA names the plan (R2 C19); the superseding row is not settled (R2 C20) | tree, tool-run | `git show HEAD:docs/conflict-wizard-ia.md \| $G -o -E 'KEEP [A-Z]+\|MERGE' \| sort \| uniq -c` prints `KEEP BOTH`, `KEEP LEFT`, `KEEP RIGHT` and no `MERGE`; `tools/archaeology --no-gh 'KEEP CLOUD'` names the deciding row `[unverified]` (D-CLOUD-041, `:98`, is the candidate, R4 item 4) | Q1, Q5 | **ledger**: one historical-plan row naming the superseding row's ID (ruling (d)) |
| **L-25** | `docs/releases/rc-accept.txt:13`, `:15` (R2 L-11) | **0.0.1 called *"the first Rasteratops release"*** in the RC ledger; `:15` sends the reader to `docs/rasteratops/release-readiness.md` (R2 C8); `NAMING.md:47-50` | tree | `git show HEAD:docs/releases/rc-accept.txt \| $G -n Rasteratops` prints `13:` | Q2 | **ledger**: **inherited:coordinator** (ruling (l)) |
| **L-26** | `docs/releases/rc-accept.txt` (R4 items 41, 59) | **two stale acceptances kept as the record**: `zip` and `spirv-headers` (#963 `:10`; `:16` *"the acceptances in `rc-accept.txt` stay as the record"*); `rc-accept zip/spirv lines: 2  total non-comment: 9` (R4 C25); `release-candidates.md:38-40`: each acceptance cites a decided row | tool-run | `git show HEAD:docs/releases/rc-accept.txt \| $G -v '^#' \| $G -c .` prints `9` (proof K68, this command; open item 14 settled); each non-comment line's cited ID looked up in the decided table, the look-up's line recorded | Q4 | **ledger** |
| **L-27** | `docs/pr-series/map.txt:112`, `:174` (R2 L-04) | **the upstream-series map names two deleted paths**: `.../rclone/sources/post-update`, `.../rclone/sources/cloud_migrate_layout`; the latest deletion over the pair `e6645cb5ea 2026-10-08` (R2 C11); `tools/pr-stack-check`'s failure on them inferred from its code, not observed (R2 L-04) | tree | `for p in projects/ROCKNIX/packages/network/rclone/sources/post-update projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout; do git cat-file -e "HEAD:$p" 2>/dev/null \|\| echo "GONE $p"; done` prints two `GONE` (R2 C10) | Q6 | **ledger**: **inherited:coordinator** (ruling (e)); never run `pr-stack-check` here (it makes a worktree) |
| **L-28** | `docs/reviews/plan-for-the-plan.md:528` at `e3fb3dfe00`; `doctrine-rules.md:262-265` (R1 § 8 item 5; R3 § 7 item 7) | **the renovation's records listed apart, and a criterion true of no tree**: T4's brief keeps `docs/reviews/**` as *"P0's and P1's, the plan and the order"* while `areas.json` puts it in the doctrine and the `rest` gives T39 its 12 rows; the plan reads *"This file exists on `next` at `docs/reviews/plan-for-the-plan.md`"* while `next` has no `docs/reviews/` (R1 C10) | tree | `git ls-tree --name-only 8ebaf8daad docs/reviews/ \| $G -c ''` prints `0`; `git show HEAD:docs/reviews/plan-for-the-plan.md \| $G -n 'This file exists on'` prints the line | Q4 | **ledger**: **inherited:coordinator** (ruling (a) settles the ownership; every plan lead T38's hand-back names is a row here) |
| **L-29** | `docs/reviews/order.md:792` at `2174265e9c` (R1 § 1, § 8 item 9) | **a preliminary number in the order**: *"split in three (T4, T33, T39)"*, T33 being today's T38 by the renumbering table (`:188`, R1 C01) | tree | `git -C "$W" show 2174265e9c:docs/reviews/order.md \| sed -n 792p` prints the line | Q7 | **ledger**: **inherited:coordinator** |
| **L-30** | `docs/rasteratops/release-readiness.md` (990 lines, *"# pixelelated 0.0.1 release readiness"*), `support-matrix.md` (162) (R2 L-19) | **current release records under the retired name's folder**: changed 2026-10-16; the first is named by `rc-accept.txt:15`, and they are named by four and six `docs/` files outside the ledgers (R2 C19, C21); `NAMING.md:14-18` and `rename-plan.md:60` retire active folder names in reviewed batches; #509 OPEN (R2 C12) | tree, record | `git show HEAD:docs/rasteratops/release-readiness.md \| sed -n 1p` prints the title; `git grep -l -F 'docs/rasteratops/release-readiness.md' HEAD -- docs \| $G -c ''` prints its inbound count | Q2, Q7 | **inherited:#509** (a move is a reviewed rename batch, and it would change a ledger row's text) |
| **L-31** | `documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md` (R2 L-17; ruling (j)) | **the fork's emulator table has drifted and has no generator**: against AMD64's `57 insertions(+), 66 deletions(-)` (R2 C18); fork-own, added by `a6b28a469f` and last changed by `a19831ebf6`, both 2026-08-21, not updated since (proof K36, X08; `v2 read`: `git log --format='%h %cs' 2174265e9c -- <the file>` prints 2 commits); only `tools/fork-worktree` names the file among `scripts/ tools/ config/ Makefile` (R2 C22); whether the differences are real is not settled | tool-run | `git diff --stat HEAD:documentation/PER_DEVICE_DOCUMENTATION/AMD64/SUPPORTED_EMULATORS_AND_CORES.md HEAD:documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md \| tail -n 1` prints the stat | Q5, Q6 | **inherited:coordinator**: a Backlog candidate -- generate it from the image's systems list, or drop it (ruling (j)) |
| **L-32** | `docs/es-menu-map.md:134`, `:405`, `:595` (R4 item 37, § 8 item 2) | **the most-cited reference document, cited by line**: 26 open issues name the map (R4 C8); #682 `:42` (`:134`, the configure-a-controller flow), #1216 `:16` (`:405`, *"reading FINISH RESTORE PROCESS"*), #667 `:41` (`:595`, the scan page's entries); #965's 22 settings pages; a check that proves titles only (R4 items 2, 58) | record | `git show HEAD:docs/es-menu-map.md \| sed -n '134p;405p;595p'` printed beside each issue's quoted sentence; `tools/es-menu-map-check`'s line quoted | Q4 | **inherited:the interface lanes** (E700, ruling (b)): `02` records which lines still say what the issues cite |
| **L-33** | #576 `:7`, #620 `:16` (R4 item 45) | **two open issues cite a document the tree lacks**: *"governed by `docs/graphics-memory-testing.md`"*, *"implemented and checked on October18: docs/graphics-memory-testing.md"*; `MISSING` at `e3fb3dfe00` and at `next`; added by `b5aad48cbe` 2026-10-18 on `remotes/legacy/m7-audit-integration-603` only (R4 C25 to C27) | tree, record | `git cat-file -e HEAD:docs/graphics-memory-testing.md 2>/dev/null \|\| echo MISSING` prints `MISSING` | Q6 | **inherited:coordinator** (the file is in no tree here, so in no slice) |
| **L-34** | `docs/decision-register.md:239`, `:250`, `:368`, `:486`, `:490`, `:497`, `:502` against `:514`; `:797`; `documentation-accuracy.md:48-52` (R4 items 7, 21, 27) | **row against row**: D-WORKFLOW-011, -014 (*"The rocknix.org documentation (#42) is the last step before the upstream PR"*), -034, -064, -068, -071, -076 describe a series that **D-WORKFLOW-084** ended (*"nothing more is submitted to ROCKNIX beyond the small generic fixes"*; #333 `:1`: every PR of the series closed); D-WORKFLOW-080 open (*"How does the interface work go upstream in pieces a person can review?"*); `map.txt` still a live map; the rule's *"blocks it"* names that series | row vs doc | `git show HEAD:docs/decision-register.md \| sed -n '250p;514p;797p' \| cut -c1-160` prints the three rows | Q4 | **inherited:coordinator** (rows and a rule); `map.txt` is tabled as the record of a closed series (L-27) |
| **L-35** | `.claude/rules/handheld-evidence.md`'s glob (R1 § 8 item 3; R4 item 50) | **a rule that loads for any record**: the `docs/**` glob loading `handheld-evidence.md` (`t4-streams.md:244-246`; T4 PL-24 withdrawn as this lead) | tree | `git show HEAD:.claude/rules/handheld-evidence.md \| sed -n '1,12p' \| $G -n 'docs/'` prints the glob line | Q5 | **inherited:coordinator** (T4's file); `02` lists which reference documents the glob reaches |
| **L-36** | `CLAUDE.md:34`, `AGENTS.md:31`, `es-native-ui.md:37`, `instruction-files.md:122` (R4 items 51, 56) | **two documents or three**: `CLAUDE.md:34` says *"Two more documents"* and `AGENTS.md:31` *"Two documents"* load nowhere (proof K76, X10); `instruction-files.md` says three, adding `docs/device-testing-policy.md` (T4 F-09) | row vs doc | `git show HEAD:.claude/rules/instruction-files.md \| sed -n 122p` and `git show HEAD:CLAUDE.md \| sed -n 34p` print the two | Q7 | **inherited:coordinator**; T39's half, whether the policy carries interface law, is a `02` § Coverage note |
| **L-37** | #807's body `:15` (R5 C23; ruling (i)) | **an area sentence untrue of this slice**: *"its paths have no upstream (ROCKNIX carries none of them)"* against `upstream-carried 90` (R1 C16); #807's own T39 row `:11` carries the right tiers (R5 C23) | record | `gh --repo pixelelated/distribution issue view 807 --json body --jq .body \| $G -c 'no upstream'` read at stage A, after the coordinator's erratum | Q4 | **inherited:coordinator**: written at dispatch (ruling (i)); the lane reads it back |
| **L-38** | the 53 reference files outside `register-check`'s `LIVE` (R3 § 2.7; R4 item 34) | **citations no tool checks**: `D-ID citations unread-by-register-check named=864 unresolved=0` in 53 files; inside `LIVE` `named=326 unresolved=0` (R3 C23); #947 `:9`: *"`LIVE` omits documents that cite IDs: `docs/conflict-wizard-ia.md`, `NAMING.md`, `docs/releases/device-facts.md` and four more"* | tool-run | § 5's `cites` step prints the unresolved IDs: over the 223 at P1 against the register at `a0fb117b8b` it prints `UNRESOLVED D-WORKFLOW-188` (`docs/reviews/p1-tracking.md:56`, `:500`; the row lives on P1's branch alone, proof C8, C12, X03); ruling (p)'s merge of `feature/m6-p1-survey-641` (`2174265e9c`) into the coordinator's branch before dispatch carries the row into the register -- the coordinator runs `tools/register-check` after the merge and records it -- so at the dispatch tip the step expects no line, and an `UNRESOLVED D-WORKFLOW-188` there is the coordinator's finding at dispatch, never the lane's | Q4 | **inherited:#947** (the guard); clean today, unguarded tomorrow |
| **L-39** | `docs/releases/versioning.md` (138 lines) (R4 item 40) | **an open criterion on a reference document**: #1013 `:11`: *"`docs/releases/versioning.md` names the field (`git grep -c emulationstation next -- docs/releases/versioning.md` is 1 or more"* | tool-run | `git grep -c emulationstation HEAD -- docs/releases/versioning.md` prints nothing at `a0fb117b8b` (proof K80; open item 16 settled), re-run at the lane's ref | Q4 | **inherited:#1013** (the check printed nothing, K80) |
| **L-40** | `worktrees.md`, `CLAUDE.md` against the machine (R3 § 7 item 8) | **a path word the machine retired**: the rules prescribe `../rocknix.worktrees/` and `/workspace/repos/rocknix`; the primary checkout is `/workspace/repos/pixelelated/distribution` and the worktrees sit under `distribution.worktrees/` (R3 C16); `rocknix.worktrees` in the reference class is `docs/rules-sweep-2026-09-12.md` alone, a dated record (R3 C18) | tool-run | `git worktree list \| $G -c 'distribution.worktrees'` beside `git show HEAD:.claude/rules/worktrees.md \| $G -c 'rocknix.worktrees'` | Q2 | **inherited:coordinator** (T4's rules); the identity step does not retire `rocknix.worktrees` until the coordinator rules (R3 § 2.2) |
| **L-41** | `documentation/PER_DEVICE_DOCUMENTATION/*/SUPPORTED_EMULATORS_AND_CORES.md`, 13 of the 15 upstream-carried (R1 § 8 item 6; R3 § 2.5, § 7 item 6; R4 item 17) | **upstream's generated tables, behind upstream**: three regenerations since the merge base (R1 C11); 13 differ from `upstream/next` (R1 C12); the H700 Saturn row lacks upstream's `**retroarch:** yabadabadoo` (R3 C19); D-WORKFLOW-185 (`:720`): an unshipped device is a row in the unshipped tables | tool-run | `git diff --stat 651150fc88 HEAD -- documentation/ \| tail -n 1` prints the stat (R2 C16 printed ` 14 files changed, 152 insertions(+), 24 deletions(-)` from `651150fc88` to `2174265e9c`, the fourteenth the fork's GENERIC_X64 file; the same at the dispatch tip unless the dispatch moved `documentation/`) | Q1, Q4 | **inherited:the next upstream base merge** (`release-candidates.md` step 0, read-only by ruling (a)); not a #585 line, since upstream carries the regeneration already (R1 C11) |
| **L-42** | #335 `:19` (R4 item 33) | **an open checkbox against the licence file and its row**: *"the CC BY-NC-SA attribution of the branding, per `LICENSE.md`"*, while `LICENSE.md` carries `BY-NC: 0` (R4 C24) and D-WORKFLOW-131 (`:572`) removed ROCKNIX's CC BY-NC-SA branding from this project | row vs doc | `git show HEAD:LICENSE.md \| $G -c 'BY-NC'` prints `0`; #335's body read through the mask | Q4 | **inherited:coordinator** (a stale checkbox: a tracker edit) |
| **L-43** | `TRADEMARK.md:5-6`; `LICENSE.md:3`, `:13`, `:18` (R2 L-15) | **the licence statements disagree**: *"The code is free software under the GNU GPL version 2 (`LICENSE.md`)"* against *"This distribution includes components licensed for non-commercial use only"*; *"Copyright 2024 ROCKNIX"*; *"Modifications ... by the ROCKNIX team"*; nothing states the terms of the fork's own changes and tools; the wordmark's font licence sits in `docs/pixelelated/art/Tiny5-OFL.txt`, not `licenses/` (R2 C5, C18) | tree | `git show HEAD:TRADEMARK.md \| sed -n '5,6p'` and `git show HEAD:LICENSE.md \| sed -n '3p;13p;18p'` print the lines | Q2 | **#528** (a legal reading; never a fix here) |
| **L-44** | `licenses/AETHERSX2.pdf` (R2 L-02; R1 § 8 item 7) | **a licence upstream dropped for a licensing concern**: `c4d353449e 2026-10-18 aethersx2: drop package due to licensing concern`; the fork carries the PDF and `21` paths matching `aethersx2` at `2174265e9c` and `e3fb3dfe00`, `0` at `upstream/next` (R1 C18; R2 C17, C18) | tree | `git log -1 --diff-filter=D --format='%h %cs %s' 651150fc88 -- licenses/AETHERSX2.pdf` prints the deletion; `git ls-tree -r --name-only HEAD \| $G -c -i aethersx2` prints `21` | Q1 | **#528** (the PDF row); the package is another slice's question |
| **L-45** | #359 `:9`, `:13`, `:14` (R4 item 31) | **a qualified candidate's recorded licence bytes**: `LICENSE.md` `1a277de267611abc4242e6a1e08ac2abac54316e7abcbf8ae7afd0a1dc98ec6c` and `TRADEMARK.md` `d46db25cb845b021cd7f1c13dabcd98d04e77d89a45968527e58abc9e3788761` in candidate16's `/usr/share/licenses/pixelelated/`; the tree's hashes equal them at `a0fb117b8b` (proof K85) | tool-run | `for f in LICENSE.md TRADEMARK.md; do git show "HEAD:$f" \| sha256sum; done` printed beside #359's two: equal (K85; open item 17 settled), re-run at the lane's ref | Q4 | **#528**; an edit to `TRADEMARK.md` under ruling (a) is preceded by this line and names it |
| **L-46** | `docs/upstream/**` (28 paths) (ruling (n); R4 items 15, 29, 42) | **the contribution queue's drafts, read-only**: `docs/upstream/README.md` names #585 and D-WORKFLOW-165 (`:8`, `:45`, R2 § 1) and carries 8 run-together hits (R2 C22); `raofflineproxy/pixelelated-identity/README.md:15,23` describe the rejected identity; `docs/upstream/raofflineproxy/image-completeness/fix.patch:64` carries `maxengel` (keep; the full path, X12) (R2 § Identity); #585 `:60`, `:73`, `:79`; #645 `:22` (*"... `docs/upstream` on `next` matches nothing"*, R4 item 42) | tree, record | `git show HEAD:docs/upstream/README.md \| $G -n -E '#585\|D-WORKFLOW-165'` prints lines among them `8:` and `45:` (`#585` 4 times, R4 C21) | Q4 | **#585** |

**Not leads (checked, pass).** No reference document describes the retired
`git rebase --onto` recipe as current, `rclonectl`, `.github/instructions/`,
Copilot, or the retired `pixelelated-cloud-folder{,-vm}-test`: `total: 0` each
(R2 C9; `rebase --onto` and `rubber-duck` occur only in the dated
`docs/rules-sweep-2026-09-12.md`, R3 § 2.3). `0` dead relative Markdown links
(R2 C10: `FILES-SCANNED 185 DEAD-LINKS 0`; R3 C17:
`link-named=337 link-ok=337`; R5 C22: `LINKS-relative 511 DEAD-LINKS 0`).
`Pixelelated` or `PIXELELATED` capitalised `0` (R2 C8; D-WORKFLOW-144 holds).
`README.md`'s four links resolve (R3 § 2.6). The menu map passes its checker
(R2 § 1) and `CHANGE CLOUD FOLDER` (`:286`) exists at the pin (`2` matches, R2
C20). **Not a contradiction** on R4's read (R4 § 8): D-WORKFLOW-131's
*"Rasterabot"* against `TRADEMARK.md:3` (the later rows -136 and -144 rule
it); D-CLOUD-174's *"migration destination"* against `rename-plan.md:32-33`
(D-CLOUD-175 rules it); D-WORKFLOW-073 and the three-line appendix pointer;
D-WORKFLOW-145 and `README.md:21` (`:20` is blank; proof K33, X06).

## 4. The questions

All seven apply (plan § 4); none is struck. They are T4's and T38's frame
turned on reference documents (R5 § A): **per statement** -- what it claims,
the artifact it names, whether a reader acting on it today acts wrongly, who
owns the fix; **per document** -- who reads it, what keeping it costs (R5 §
A's rewrite of § 4). Each is answered in `04-analysis.md` § Renovation face
with the evidence at its lines; the leads are § 3's, cited by number. A defect
proved is a `bug` only when a reader acting on the statement would act wrongly
(Q3); it falls in one of five families -- **a statement that names what is not
there**, **a statement true once and not now**, **two texts that disagree**,
**a record presenting itself as current**, **a cost no reader repays** -- with
the lens, **cost against value**, asked of every reference document: who opens
it, for what, and what a wrong sentence in it costs that reader.

| # | Question, for this slice | Evidence |
| --- | --- | --- |
| Q1 Modernize | A document written against a mechanism the tree retired: the cloud-folder migration (L-04, L-10; D-CLOUD-175), the closed upstream series (L-27, L-34; D-WORKFLOW-084), the Rasteratops name as the OS's (L-21, L-25, L-30; D-WORKFLOW-144, -151), the SSH `rclone config` workflow the rocknix.org page still teaches (#42, `documentation-accuracy.md:48-52`, R4 item 27), a package upstream dropped for a licensing concern (L-44), upstream's tables three regenerations behind (L-41), a plan its own wizard superseded (L-24) | the row or commit that retired it, cited; `tools/archaeology --reversal <old words>` for the sweep's list (`decision-register.md` § A reversal sweeps its old words) |
| Q2 Standards | The doctrine's standards applied to the documents: `NAMING.md`'s allowances (lowercase pixelelated; ROCKNIX for labels, paths and credit; the character and the handle; historical documents keep their names) (L-05, L-19 to L-23, L-25, L-40, L-43); `es-player-text.md`'s vocabulary in a document that names player labels (L-07); D-UI-039 for the map (L-08, L-32); a dated record's first line saying what it is (L-18); the identity of the fork's own repository in links (L-23) | `NAMING.md` at `COHASH`, its lines quoted; the identity step's lines (§ 5) |
| Q3 Bugs | **A statement a reader acts on wrongly**: runs a retired tool or flag; follows a retired procedure (a cloud-folder migration, D-CLOUD-175); flashes or stages by a wrong instruction (L-05); trusts a licence or trademark statement the tree contradicts (L-43, L-44, L-42); copies a mask that prints a credential (L-16); follows a release instruction to a release that does not exist (L-02); trusts a policy that calls a decided row open (L-03) (R5 § C stage D). Each is a `bug` with its trace and its `Already written:` line -- what the statement has already caused: a brief, a release note, a rocknix.org draft or an issue that copied it. Everything else is a punch item resolved by an edit, an inherited item, or a ledger row | the statement quoted at its `path:line`; the artifact it misdescribes; the artifact the corrected statement must match |
| Q4 Currency | Against the fork's own record and code: **(a) every decision ID a document cites** with its row's state (`named=864 unresolved=0` outside `LIVE`, `named=326 unresolved=0` inside, R3 C23; L-38); **(b) every tool named**, its existence (L-14, L-19, L-27); **(c) every issue cited as open, pending or ordered**, against its state (L-03, L-06, L-08, L-33, L-37, L-42); **(d) every path named**, resolved, in the classes of § 5's `paths` step (L-13, L-20, L-28, L-33); **(e) every baseline, catalog row or count** a document states, against the artifact (L-09, L-15, L-26, L-41); **(f) every line number an issue cites** in a reference document, against the line (L-15, L-32) | tables written by `tools/t39-tables.py` committed beside them (§ 6), each with its command and count |
| Q5 Efficiency -- **the lens** | **What each reference document costs a reader and what it earns.** The cost: its lines, its last commit, whether a session must open it (`CLAUDE.md`, `AGENTS.md` or a rule names it) and whether a wrong sentence in it sends a reader somewhere wrong. The value: its inbound names from `.claude/`, the root documents, `docs/` outside the ledgers and the October work logs (R2 C21's `R/O/D/W` columns), its role (the procedure an agent runs, a player's guide, a redistributor's notice, a dated record). The sharpest rows: the 17 documents with no inbound name and at most one `docs/` reference (`LOW-INBOUND-SUM files=17 lines=2135`, R2 C26; L-18), the council notes (L-12), and at the heavy end the four that carry most of the reference lines -- the changelog (3,581, a ledger row), the map (989, a fifth of it the journal of L-08), `release-readiness.md` (990, L-11's 122 hits, L-30) and `next-candidate-work.md` (963, L-09) (R2 § 3). `licenses/` (7,817) and `documentation/` (2,160) are upstream's and cost nothing to read wrongly except through L-41, L-43 and L-44 (R2 § 3) | the Q5 table: one row per reference document proper (§ 6) |
| Q6 Dead ends | Everything the documents point at that the tree lacks: R3's four dead-path candidates -- one real absent in-tree path, `packages/rocknix` (L-20), and three names ruled external: the splash repositories' `tools/pixelelated-wordmark` and `tools/rasteratops-wordmark` (L-14, L-19) and the site checkout's branch `docs/cloud-saves-native-wizard` (L-13) (R3 § 2.1; X02), the two deleted map paths (L-27), the document two open issues cite (L-33), the GENERIC_X64 table with no generator (L-31), the 17 documents nobody names (L-18) | § 5's `paths` and `tools` steps; the inbound columns |
| Q7 Clarity | Can a reader new to it tell what each document is for, and whether it is current, in one pass: a dated journal inside a reference (L-08); a player's guide ending in internal status (L-10); words and numbers run together (L-11); a record with no date in its first line (L-18); two counts of the documents that load nowhere (L-36); a preliminary slice number in the order (L-29) | the reader's pass (§ 5 rule 5) |

**The ladder, applied to every finding** (`working-principles.md` §
Enforcement depth). Each punch item says which stage the statement sits at --
written, routed, evidenced, audited, self-examining -- and the tool that would
hold it at the next stage (`tools/t39-checks.sh` promoted to a fork tool for
Q2, Q4 and Q6; `tools/register-check`'s `LIVE` widened for L-38, #947; #270's
device-facts check for L-15), or the words *no tool can*. A statement found
wrong twice in the record is proposed for the tool, not only the rewrite.

**The questions for the maintainer, framed here and put by the coordinator**
(the lane raises each on #686 at the stage-D pause with its evidence; it does
not ask the maintainer itself). Put in terms of what a reader would see
(`player-language.md` § How to apply: *"A decision is put in terms of what
they would see"*):

1. **The menu map's dated journal: keep it in the map, marked historical, or
   move it into the qa-logs it already links?** (ruling (b), L-08) Today an
   agent placing a row reads `279` lines under `16` headings of dated
   candidate narrative after `## Not mapped` (R2 C26), two of whose headings
   call closed work pending. T39 corrects those headings either way; moving
   the journal is a restructuring this slice does not do.
2. **The reference documents nobody reads: keep each with a dated first line,
   or retire it?** (L-12, L-13, L-18) Today 17 documents, 2,135 lines (R2
   C26), carry no inbound name from the rules, the root documents or the
   October work logs and at most one from `docs/`; among them the council
   limits note, two rocknix.org stubs and a 590-line design note whose paths
   are another repository's. Keeping them costs a reader a search result that
   looks current; retiring them is a removal, the maintainer's, never stage
   E's.

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict, as its `SKILL.md` §
Evidence floor lists them, restated for a table as T40's § 5 did (R5 § A):

1. *Tracker state is never sole evidence.* Every cell cites a command's output
   -- the inventory's row, a `git show` at a hash, a tool's run, a register
   row, an issue's state read by `gh` -- or a `file:line`.
2. *Mechanical evidence outranks reading.* **A document's sentence is its own
   claim about the tree, recorded as such; the artifact it names is the
   evidence** (R5 § A, from T40's rule 2): a path is `git cat-file -e` at the
   hash, a tool its existence and its `--help`, an issue its state, a count a
   command's line, a label the pin's string.
3. *The bench is the host; no guest, no build, no plan, no network beyond
   `gh --repo pixelelated/distribution` reads* (ruling (q)). **Can this be
   done on the VM? No, for nearly all of it** -- the slice is a table of what
   the reference documents claim about the tree, the tools and the record, and
   reading a file at a hash is not a test, a proof or a measurement
   (`vm-first.md`; #807 `:19`'s answer for the area, R5 § D, C23). **The one
   exception** is a document that claims a guest behaviour -- a VM recipe, a
   tool's guest option, a frame a check reads, what a walk shows -- whose
   truth only a guest would show: it is checked first against the tool's
   options and source and `docs/vm-qa-log.md`, and **recorded as
   `[unverified]` in `02` with the proof a later slice could make**; this lane
   brings nothing to a guest (ruling (q)). A document that claims a handheld
   fact is read against `docs/releases/device-facts.md`, never tested on a
   handheld (R5 § D). Which of the 254 carry a guest claim was not read
   `[unverified]` (R5 § D; R3 § 6 found none in the paths and names it read);
   stage B's table finds them, each a `02` row. **This paragraph is the VM
   line #686's body takes in place of its generated one** (ruling (i); R5 §
   D).
4. *An assertion that cannot fail is not evidence.* Before recording a PASS,
   ask what result would have produced a FAIL -- at Local depth nobody else
   asks it; `tools/forbidden-terms-check` exiting 0 on empty input is the
   shape (§ 3 item 5).
5. *Subagent output is a LEAD, never EVIDENCE.* Fan-out inside this lane is
   read-only research subagents only (D-WORKFLOW-183), and for this slice
   **one no-context read-only reader per group of § 2's table** is the right
   one, given that group's files at the hash and asked what it would have done
   on the strength of each document; its answers are Q7's and Q3's leads,
   re-read by the lane before any becomes a row (R5 § C stage B).

- **The reads at the tip.** The 254 are read at the dispatch tip's bytes
  (ruling (g)) -- `git show HEAD:<path>`, or the read tree exported once under
  `/workspace/tmp/m6-t39/export/` by `git archive` (a tree export goes under
  `/workspace/tmp/<lane>/`, never the session's scratch on `/tmp`) -- with the
  twelve `docs/reviews/` rows also read at `2174265e9c` where the
  coordinator's branch changed them (§ 2's split lines).
- **A read is free and goes through the filter.** No reference document is a
  config file, but the issues, the device-testing policy and the cloud
  documents name sign-in keys and variables: any line read from an issue body
  or a command over a config goes through the mask `M` below, and a variable
  is named, never its value. **The wordlist**
  (`~/.config/rocknix/forbidden-terms`) is never read, listed or quoted
  (D-WORKFLOW-061): `tools/forbidden-terms-check` is its only reader, and
  `.githooks/guard-lib`'s `guard_load` sources it, so the secret scan below
  sources `.githooks/secret-patterns` alone and never calls `guard_load`.
- **The EmulationStation checkout** is read for L-07's labels only, by
  `git -C ~/Development/emulationstation-next grep <pin>` at the recipe's pin
  (`16dbac5211`, R2 C13), never checked out, built or written (R2's header; R3
  C12).

**`# STAGE A` -- the first commands, before anything else** (in the lane's
worktree, under bash, after the pointer's eleven keys, § 10). `rc=$?` sits on
its own line after each command; the expected lines are research lines cited
in their comments, or marked `[unverified]`:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-reference-686
cd "$D"
cat .github/sessions/saved-session-state-feature-m6-doctrine-reference-686.md   # the pointer: the dispatch's hashes; § 10 names the eleven keys to check
export LC_ALL=C; G=/usr/bin/grep; T=/workspace/tmp/m6-t39; W=/workspace/tmp/m6-coordinator/t11-research/tree; mkdir -p "$T/tmp"; df -i /workspace | tail -n 1
date -u +%Y-%m-%dT%H:%M:%SZ
git branch --show-current                                                    # feature/m6-doctrine-reference-686
git status --short | $G -c ''                                                # 0
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-p1           # stacked-on-p1 (ruling (g))
git merge-base --is-ancestor 8ebaf8daad HEAD && echo next-is-here            # next-is-here
sha256sum docs/reviews/slices.json docs/reviews/inventory.json docs/reviews/areas.json | cut -c1-16   # 49bc2745664e52f4, d17b9cac4b2c2245, 985f742cfd4a2138 (R1 C05): the block's inputs, present because the branch is stacked on P1
test -d "$W" && echo clone-here                                              # clone-here: the block's W, read by git -C only (R1 C20 re-ran the block against it)
# the lint's PASS on a Local plan, before anything else (ruling (q)): T4's finished Local folder, exported from T4's tip and linted by this tip's lint; then a copy with its tier_exception removed, which must FAIL
git rev-parse --verify origin/feature/m6-doctrine-rules-651 2>&1             # recorded whole as it prints, a hash or `fatal:` (R5 § B item 3); T4's tip is 6ec78bbf8c (R4 § 4)
F=$(git ls-tree -d --name-only 6ec78bbf8c docs/audits/ | $G -E -e '-epic-m6-doctrine-rules$'); echo "T4 folder: $F"
L=$T/lint-proof; mkdir -p "$L/pass" "$L/fail"
git archive 6ec78bbf8c "$F" | tar -x -C "$L/pass"; git archive 6ec78bbf8c "$F" | tar -x -C "$L/fail"
python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); print("t4 plan:", d.get("depth"), d.get("tier_exception"), len(d.get("reviewers") or []))' "$L/pass/$F/second-opinions/review-plan.json"   # `t4 plan: local D-WORKFLOW-184 0` (proof K111, on T4's folder exported from 6ec78bbf8c; open item 6 settled)
python3 -I -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d.pop("tier_exception",None); json.dump(d,open(p,"w"),indent=2)' "$L/fail/$F/second-opinions/review-plan.json"
tools/lint-audit-artifacts "$L/pass/$F" > "$T/tmp/lint-local-pass.out" 2>&1; rc=$?
echo "lint, a Local plan, rc=$rc"; tail -n 3 "$T/tmp/lint-local-pass.out"   # rc=0 and a line ending `PASS` (proof K111: `lint, a Local plan, rc=0`): this line is the proof ruling (q) asks for
tools/lint-audit-artifacts "$L/fail/$F" > "$T/tmp/lint-local-fail.out" 2>&1; rc=$?
echo "lint, tier_exception removed, rc=$rc"; $G -n 'FAIL' "$T/tmp/lint-local-fail.out"   # rc=1 with `FAIL  second-opinions/review-plan.json or its call evidence is invalid: local-only cannot satisfy Epic/Milestone` and `1 CONTRACT FAILURE(S)` (proof K111) -- the PASS's FAIL-first
# L-01, ruling (p): every file the renovation's README and plan name resolves in this worktree (R2's seven-name form printed seven MISSING at e3fb3dfe00, R2 C6, C10, C12; expect no line here: this fifteen-name loop printed `MISSING=0` at 2174265e9c, 11 at a0fb117b8b and e3fb3dfe00, 15 at 8ebaf8daad, proof K39)
for p in docs/reviews/{README.md,areas.json,assessment.md,briefs/p1-survey.md,build-path-read.md,cross-reference.md,inventory.md,order.md,p1-tracking.md,plan-for-the-plan.md,slices.json,status.md} tools/renovation-{inventory,status,drift}; do git cat-file -e "HEAD:$p" 2>/dev/null || echo "MISSING $p"; done
# the brief's own two blocks, extracted by their markers at V2HASH and checked, never retyped (§ 2)
BR=V2HASH   # the pointer's value, never the literal word (§ 1's placeholders): unfilled, the show fails and nothing below runs
git show "$BR:docs/reviews/briefs/doctrine-reference.md" > "$T/tmp/brief.md"; rc=$?
echo "brief read rc=$rc"
mkdir -p .qa-scratch/t39
python3 -I -c 'import sys,re
t=open(sys.argv[1]).read()
for name in ("block.sh","split.sh"):
    seg=t[t.index("<!-- t39 %s begin -->" % name):t.index("<!-- t39 %s end -->" % name)]
    body=re.search(r"\n```bash\n(.*?)\n```\n", seg, re.S).group(1)+"\n"
    open(".qa-scratch/t39/"+name,"w").write(body)' "$T/tmp/brief.md"
sha256sum .qa-scratch/t39/block.sh .qa-scratch/t39/split.sh | cut -c1-16; $G -c '' .qa-scratch/t39/block.sh .qa-scratch/t39/split.sh   # e81453b6732cdea8 and afb1909c5cdc6c88; 130 and 46 lines (R1 C16, C20)
# the membership (§ 2): expect § 2's lines byte for byte
bash .qa-scratch/t39/block.sh > "$T/tmp/block.out" 2>&1; rc=$?
echo "block rc=$rc"; cat "$T/tmp/block.out"
LC_ALL=en_US.UTF-8 bash .qa-scratch/t39/split.sh > "$T/tmp/split-p1.out" 2>&1; rc=$?   # under en_US.UTF-8: § 2's expected lines are that locale's (X01); the C locale exported above stays for every other count
echo "split (defaults) rc=$rc"; cat "$T/tmp/split-p1.out"
TIP=MERGE_HASH   # the pointer's value, never the literal word: unfilled, every row prints `absent`
LC_ALL=en_US.UTF-8 G="$PWD" TIP="$TIP" bash .qa-scratch/t39/split.sh > "$T/tmp/split-tip.out" 2>&1; rc=$?   # the same locale, so the diff below compares like with like (X01)
echo "split (dispatch tip) rc=$rc"; sed -n '/^tip:/,$p' "$T/tmp/split-tip.out"   # no `absent` line (ruling (p)); the rest as it prints [unverified] (§ 2; at a0fb117b8b: 8 absent, 3 changed, 1 same, 329 reached, 83 added, proof K11, K19)
diff <(sed -n '1,/^P1 grep -c total/p' "$T/tmp/split-p1.out") <(sed -n '1,/^P1 grep -c total/p' "$T/tmp/split-tip.out") && echo "the lines before tip: agree"
./tools/renovation-inventory --order --no-write --distribution "$W" > "$T/tmp/order.out" 2>&1; rc=$?
echo "renovation-inventory --order rc=$rc lines=$($G -c '' "$T/tmp/order.out")"; $G -E '^(slices|rows|unassigned|ambiguous):|^ *39 doctrine-reference ' "$T/tmp/order.out"   # rc=0 lines=50; slices: 46; rows: 134634 (inventory: 134634); unassigned: 0; ambiguous: 0; the T39 row (R1 C02)
# ruling (a)'s carve-out, from block-2.txt's TSV: the classes and their counts, printed by this command and quoted, never typed (proof K26 printed version 1's; open item 1 settled; the expected lines follow the command)
python3 -I -c 'import collections
rows=[]; ix=None; p=False
for l in open(".qa-scratch/t39/block-2.txt"):
    l=l.rstrip("\n")
    if l=="TSV": p=True; continue
    if l.startswith("TREE-SIDE"): break
    if p and ix is None: ix={k:i for i,k in enumerate(l.split("\t"))}; continue
    if p: f=l.split("\t"); rows.append({k:f[i] for k,i in ix.items()})
NAMED={"docs/releases/catalog.md","docs/pr-series/map.txt","docs/releases/rc-accept.txt","docs/vm-qa-log.md","docs/cloud-sync-changelog.md","docs/rasteratops/p0-sweep-hits.txt"}
def carve(r):
    p=r["path"]
    if r["lines"]=="None": return "ledger-binary"
    if r["tier"]=="upstream-carried": return "read-only-upstream"
    if p.startswith("docs/reviews/"): return "ledger-reviews"
    if p in NAMED: return "ledger-named"
    if p.startswith("plans/"): return "ledger-plan"
    if p.startswith("docs/upstream/"): return "read-only-585"
    if p=="LICENSE.md": return "read-only-528"
    if p.startswith("documentation/"): return "tabled-generic-x64"
    if "/art/" in p and not p.endswith(".md"): return "art-bytes"
    if p=="TRADEMARK.md": return "edit-under-naming"
    return "edit-scope"
c=collections.Counter(carve(r) for r in rows)
for k in sorted(c): print("CARVE", k, c[k])
print("CARVE total", sum(c.values()))'
# expect (v2 read at 2174265e9c, with p0-sweep-hits.txt in NAMED; the proof's K26 lines at a0fb117b8b read edit-scope 69 and ledger-named 5): CARVE art-bytes 18; edit-scope 68; edit-under-naming 1; ledger-binary 31; ledger-named 6; ledger-plan 1; ledger-reviews 12; read-only-528 1; read-only-585 27; read-only-upstream 88; tabled-generic-x64 1; CARVE total 254
# the checkers' baseline at the dispatch tip (R3 C13; their lines may move with the dispatch's own commits, so each line that prints is recorded beside the research's)
tools/rules-check > "$T/tmp/rules-check.out" 2>&1; rc=$?
echo "rules-check rc=$rc"; tail -n 1 "$T/tmp/rules-check.out"               # rc=0, `rules-check: 30 rule files, every one front-mattered and indexed` (R3 C13) -- no evidence for the 254 (§ 3 item 5)
tools/register-check > "$T/tmp/register-check.out" 2>&1; rc=$?
echo "register-check rc=$rc"; tail -n 1 "$T/tmp/register-check.out"         # rc=0, `register-check: 713 IDs, each once; ...` at e3fb3dfe00 (R3 C13); the dispatch's own row D-WORKFLOW-220, T38's dispositions row D-WORKFLOW-219 and P1's D-WORKFLOW-188 (carried in by ruling (p)'s merge, X03) move the count, so the line that prints is recorded
tools/es-menu-map-check > "$T/tmp/menumap.out" 2>&1; rc=$?
echo "es-menu-map-check rc=$rc"; tail -n 1 "$T/tmp/menumap.out"             # rc=0, `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` (R3 C13); exit 2 is CANNOT, never a pass
tools/release-catalog --check > "$T/tmp/catalog.out" 2>&1; rc=$?
echo "release-catalog --check rc=$rc"; tail -n 1 "$T/tmp/catalog.out"       # rc=0, `release-catalog: current (99 cuts)` (R3 C13); --write is never run here
tools/work-log-index --check > "$T/tmp/index.out" 2>&1; rc=$?
echo "work-log-index rc=$rc"; tail -n 1 "$T/tmp/index.out"                  # `work-log index: current` (R3 C13)
tools/prose-check --self-test > "$T/tmp/prose.out" 2>&1; rc=$?
echo "prose-check rc=$rc"; tail -n 1 "$T/tmp/prose.out"                     # `self-test: PASS` (R3 C13)
tools/ceremony-check > "$T/tmp/ceremony-check.out" 2>&1; rc=$?
echo "ceremony-check rc=$rc"; tail -n 1 "$T/tmp/ceremony-check.out"         # [unverified]: no research file for this brief ran it; what another lane owes is noted on #686, never paid here
gh --repo pixelelated/distribution issue view 686 --json title,state,body --jq '.title, .state, (.body | split("\n") | length)'   # the title, OPEN, and the body's line count after the coordinator's fill (27 before it, R5 C16)
gh --repo pixelelated/distribution issue view 807 --json body --jq .body | $G -n -i -E 'no upstream|errat' | cut -c1-160   # L-37: the sentence and the coordinator's erratum beside it (ruling (i)); the sentence prints and `errat` 0 before the dispatch (proof K78: `#807 errat lines: 0`); the erratum is written at dispatch, and the lines that print are recorded
H=/workspace/tmp/m7-m6-host-coordination.txt   # named by T38's brief (:1106, :1674); 710 lines at the proof's read (C10); the dispatch comment confirms the path and records its line count (open item 23)
date -u +%H:%M:%S; wc -l < "$H"; tail -n 6 "$H" | cut -c1-200   # read for the protocol only, with the time of the read and its line count beside the dispatch comment's; this slice writes no line there (§ 10)
```

Then the runs below. **If the lint's Local PASS does not print**, the lane
records the lint's lines in `00`, names it on #686 as one question before
stage C (its own folder cannot pass § 7's second criterion until the shape is
known), and goes on with stage B's reading, which does not depend on it (T38's
contingency, the same shape).

**The runs** (every one in `02` § The runs with exit, wall time, the figure
and *a FAIL would mean ...*; **the block below captures exit only where it
says `rc=$?`; the lane wraps each run in its own `rc=$?` line and a `date +%s`
pair, or records that it did not**; a run that cannot be made is `CANNOT` with
its reason). From the lane's worktree after the membership block, under bash
with `LC_ALL=C` (a non-ASCII count depends on the locale, R5 § B item 9; R5
C22 ran under `LC_ALL=C.UTF-8`); counts by `/usr/bin/grep`; `rc=$?` on its own
line, never after a pipe; no `cut` on an expected error line; **every line
read from an issue body goes through the mask `M`**:

```bash
export LC_ALL=C; G=/usr/bin/grep; T=/workspace/tmp/m6-t39
M='s/((token|key|pass(w[a-z]*)?|psk|user|login|apikey) *[=:] *)[^ "]*/\1***/Ig; s/(--(token|key|pass(w[a-z]*)?|psk|user)[= ]+)[^ ]+/\1***/Ig'   # the read mask, engineering-practices.md's two substitutions, widened as T38's was
# the read tree, once: the 254 at the dispatch tip (246 present at e3fb3dfe00, R2 C6, R3 C20; at P1 every one of the 254 is present, `of the 254 absent: 0`, proof C11; 254 here by ruling (p) [unverified])
mkdir -p "$T/export" && xargs -d '\n' -a .qa-scratch/t39/paths.txt git archive HEAD -- | tar -x -C "$T/export"; find "$T/export" -type f | $G -c ''
# the binaries, by name, size and sha256 (ruling (o)): expect 31 (R1 C19: gz 1, pdf 2, png 28)
awk -F'\t' '/^TSV$/{p=1;getline;for(i=1;i<=NF;i++)ix[$i]=i;next} /^TREE-SIDE/{p=0} p && $1=="distribution" && $ix["lines"]=="None" {print $ix["path"]}' .qa-scratch/t39/block-2.txt > .qa-scratch/t39/binary.txt; $G -c '' .qa-scratch/t39/binary.txt
while IFS= read -r p; do printf '%s\t%s\t%s\n' "$p" "$(git cat-file -s "HEAD:$p")" "$(git show "HEAD:$p" | sha256sum | cut -c1-64)"; done < .qa-scratch/t39/binary.txt > "$T/binaries-dispatch.tsv"; $G -c '' "$T/binaries-dispatch.tsv"
# the 18 art text files, the same way (ruling (o), widened at version 2; the CARVE art-bytes class, 18 by proof K26 and v2 read)
awk -F'\t' '/^TSV$/{p=1;getline;for(i=1;i<=NF;i++)ix[$i]=i;next} /^TREE-SIDE/{p=0} p && $1=="distribution" && $ix["lines"]!="None" && $ix["path"] ~ /\/art\// && $ix["path"] !~ /\.md$/ {print $ix["path"]}' .qa-scratch/t39/block-2.txt > .qa-scratch/t39/art-text.txt; $G -c '' .qa-scratch/t39/art-text.txt
while IFS= read -r p; do printf '%s\t%s\t%s\n' "$p" "$(git cat-file -s "HEAD:$p")" "$(git show "HEAD:$p" | sha256sum | cut -c1-64)"; done < .qa-scratch/t39/art-text.txt > "$T/art-text-dispatch.tsv"; $G -c '' "$T/art-text-dispatch.tsv"
# byte identity against the merge base and upstream (expect R1 C12: vs MB absent 162, differs 2, identical 90; vs UP absent 163, differs 15, identical 76 -- the docs/reviews rows are absent from both, so the dispatch moves nothing here unless it moved one of the 242)
for B in c445081a59 651150fc88; do while IFS= read -r p; do if git cat-file -e "$B:$p" 2>/dev/null; then [ "$(git rev-parse "$B:$p")" = "$(git rev-parse "HEAD:$p")" ] && echo "vs $B identical" || echo "vs $B differs"; else echo "vs $B absent"; fi; done < .qa-scratch/t39/paths.txt | sort | uniq -c; done
# the identity words over the text rows, case-sensitive, lines and files (R2 C8 over the 215 text files at e3fb3dfe00: Rasteratops 27, rasteratops 27, RASTERATOPS 4, ROCKNIX 5238, rocknix 1250, maxengel 28, JELOS 7, pixelelated 247, Pixelelated/PIXELELATED 0 -- R2's are occurrences, proof K104: all nine equal the occurrence column over the 215 at e3fb3dfe00, open item 20 settled; this loop prints lines and files, over the 223 at P1: Rasteratops 27 / 11, rasteratops 31 / 20, ROCKNIX 3297 / 57, maxengel 28 / 6, pixelelated 243 / 51, rocknix.worktrees 4 / 3 (K103), so its ROCKNIX line is not R2's 5238; the dispatch tip's 223 text rows add the eight docs/reviews files)
for w in Rasteratops rasteratops RASTERATOPS ROCKNIX rocknix maxengel JELOS pixelelated Pixelelated PIXELELATED; do printf '%s lines %s files %s\n' "$w" "$(cd "$T/export" && xargs -d '\n' -a "$OLDPWD/.qa-scratch/t39/text.txt" $G -h -c -e "$w" | awk '{s+=$1} END {print s+0}')" "$(cd "$T/export" && xargs -d '\n' -a "$OLDPWD/.qa-scratch/t39/text.txt" $G -l -e "$w" | $G -c '')"; done
# the flashing runbook (L-05; R2 C20: ROCKNIX=21 pixelelated=0)
git show HEAD:docs/device-flashing-runbook.md | $G -c ROCKNIX; git show HEAD:docs/device-flashing-runbook.md | $G -c pixelelated
# the retired names over the text rows, case-insensitive (R3 C18 by class; R5 C22 at P1: cloud_migrate_layout 21 in 7, maxengel 28 in 6, rocknix.worktrees 4 in 3, rubber-duck 1 in 1, rclonectl 0, .github/instructions 0)
for w in 'cloud_migrate_layout' 'migrate.?layout' 'rebase --onto' 'rclonectl' '\.github/instructions' 'copilot' 'rubber[- ]duck' '\brclone config\b' 'rocknix\.worktrees'; do printf '%s lines %s\n' "$w" "$(cd "$T/export" && xargs -d '\n' -a "$OLDPWD/.qa-scratch/t39/text.txt" $G -h -c -i -E -e "$w" | awk '{s+=$1} END {print s+0}')"; done
# the decision IDs the text rows cite, against the register's rows (R3 C23: register IDs 713; named=864 unresolved=0 outside LIVE, named=326 unresolved=0 inside; a -0+ placeholder skipped): expect no unresolved line at the dispatch tip -- over the 223 at P1 against the register at a0fb117b8b the line is `UNRESOLVED D-WORKFLOW-188` (p1-tracking.md:56, :500; a row on P1's branch alone, proof C8, C12), which ruling (p)'s merge of 2174265e9c carries into the register before dispatch, the coordinator running tools/register-check after the merge and recording it; a line here at dispatch is the coordinator's finding, never the lane's (X03)
git show HEAD:docs/decision-register.md | $G -o -E '^[|] D-[A-Z]+-[0-9]+' | sed 's/^[|] //' | sort -u > "$T/tmp/ids.txt"; $G -c '' "$T/tmp/ids.txt"
(cd "$T/export" && xargs -d '\n' -a "$OLDPWD/.qa-scratch/t39/text.txt" $G -h -o -E 'D-[A-Z]+-[0-9]+') | $G -v -E -e '-0+$' | sort -u | comm -23 - "$T/tmp/ids.txt" | sed 's/^/UNRESOLVED /'
# the text checks over the 223, in the hooks' own form (R3 C20: `secret regex loaded (338 chars)`, `SECRET-PATTERN FILES: 0 LINES: 0`, the runtime-built positive matching 1; `NON-ASCII FILES: 78 LINES: 1359` over the 215, and `86` files over the 223 at P1, proof K113; forbidden-terms rc 0, empty input rc 0, the planted positive rc 1)
( P=$(mktemp "$T/tmp/sp.XXXXXX"); git show HEAD:.githooks/secret-patterns > "$P"; SECRET_PATTERNS=''; . "$P"; rm -f "${P:?}"
  printf '' | $G -E -e "$SECRET_PATTERNS" >/dev/null 2>&1; rc=$?
  echo "secret regex compile rc=$rc"
  printf -- '-----BEGIN %s-----\n' "$(printf '%s' 'OPENSSH PRIVATE KEY')" | $G -c -E -e "$SECRET_PATTERNS"
  cd "$T/export" && xargs -d '\n' -a "$OLDPWD/.qa-scratch/t39/text.txt" $G -c -E -e "$SECRET_PATTERNS" | $G -v -c ':0$' )
(cd "$T/export" && xargs -d '\n' -a "$OLDPWD/.qa-scratch/t39/text.txt" $G -c -P '[^\x00-\x7F]') | $G -v -c ':0$'
(cd "$T/export" && xargs -d '\n' -a "$OLDPWD/.qa-scratch/t39/text.txt" cat) > "$T/tmp/text223.txt"
tools/forbidden-terms-check --stdin < "$T/tmp/text223.txt"; rc=$?
echo "forbidden-terms over the 223 rc=$rc"
tools/forbidden-terms-check --stdin < /dev/null; rc=$?
echo "forbidden-terms over empty input rc=$rc"   # rc=0 too (R3 C20): not evidence until the positive below fires
printf 'a zzqplantedzz line\n' > "$T/tmp/planted.txt"
FORBIDDEN_PATTERNS='zzqplantedzz' tools/forbidden-terms-check --stdin < "$T/tmp/planted.txt"; rc=$?
echo "forbidden-terms, a planted positive, rc=$rc"   # rc=1 and `forbidden-terms-check: 1 line(s) on stdin carry a listed word` (R3 C20's form): with FORBIDDEN_PATTERNS set the tool never reads the list
# the licence files against #359's recorded bytes (L-45; R4 item 31): equal at a0fb117b8b (proof K85)
for f in LICENSE.md TRADEMARK.md; do printf '%s %s\n' "$f" "$(git show "HEAD:$f" | sha256sum | cut -c1-64)"; done
# the releases a reader of README.md:7-10 finds (L-02; R2 C25: rc1-20260929, dev-20260827, dev-rk3326-20260819)
gh release list --repo pixelelated/distribution --limit 3
# the menu map's pending headings (L-08; R2 C13: :758, :806, :817) and the checker again after any map edit
git show HEAD:docs/es-menu-map.md | $G -n -E '^#+ .*(Pending|under qualification)'
.githooks/hooks-test > "$T/tmp/hooks-test.out" 2>&1; rc=$?
echo "hooks-test rc=$rc"; tail -n 1 "$T/tmp/hooks-test.out"   # [unverified]: no research file for this brief ran it
tools/box-check > "$T/tmp/box-check.out" 2>&1; rc=$?
echo "box-check rc=$rc"; tail -n 1 "$T/tmp/box-check.out"     # once here, once at hand-back, and --issue N once per issue this lane files [unverified]
# STAGE C -- the lane's checker, which does not exist at stage A (expect its FAIL-first runs' exits, then at the tip exit 1 naming each stage-B finding, with its own `TOTAL:` line)
A=$(ls -d docs/audits/*-epic-m6-doctrine-reference); bash "$A/tools/t39-checks.sh" --tree "$T/export" --repo "$PWD" --commit HEAD --since MERGE_HASH --paths .qa-scratch/t39/paths.txt --allow "$A/tools" --out "$T/checks" 2>&1 | tail -n 30
# STAGE A and at every stage -- the removal check: nothing outside the edit scope moves (rulings (a), (k), (n), (o)); TIPHASH is the lane's own tip the pointer names (MERGE_HASH at stage A); the literal word fails with `fatal: bad revision`; expect no line at any stage
git diff --stat MERGE_HASH TIPHASH -- docs/reviews docs/releases/catalog.md docs/pr-series/map.txt docs/releases/rc-accept.txt docs/vm-qa-log.md docs/cloud-sync-changelog.md docs/rasteratops/p0-sweep-hits.txt plans licenses documentation LICENSE.md docs/upstream .claude CLAUDE.md AGENTS.md NAMING.md tools scripts packages projects | tail -n 1
# the registers and the friction log take the procedure's appends only: expect 0 removed lines
git diff MERGE_HASH TIPHASH -- docs/decision-register.md docs/blindspot-register.md docs/friction-log.md | $G -c -E '^-([^-]|$)'
```

Every expectation above is a research file's printed line, cited in its
comment, or marked `[unverified]`. **The lane re-runs every one as its own
line; a line that differs is recorded beside the expectation, not argued
with.** The removal check names the ledger, read-only and other lanes' paths
of rulings (a), (k), (n) and (o) and the doctrine owners' files, and the
registers' line takes the appends the ceremonies owe (a removed line there is
a rewrite of a decided row); the binaries are checked by hash in
`t39-checks.sh`'s `binaries` step, and the stage-E streams' own commits are
the only ones under the edit scope. `docs/reviews/briefs/` is in the removal
check's `docs/reviews` because the briefs are the coordinator's (ruling (a));
the coordinator's own merges into the lane's branch are named in the dispatch
comment and excluded by reading `git log --no-merges` over the same paths
alongside.

**The lane's checker, `tools/t39-checks.sh`** (stage C; R3 § 2.9's
`tools/docs-check` design, scaled to the slice; R5 § C stage C). Written under
the audit folder's `tools/`, never under the repository's `tools/` (a new fork
tool changes `fork-workflow.md`'s list, `.githooks/pre-push`'s
`PERSONAL_PATTERNS` and `instruction-files.md`'s tool table in the same
change, R3 § 2.9). Bash with `python3 -I` for the parsing; it reads `--tree`
(the export, never a checkout), `--paths` (§ 2's `paths.txt`) and, for the
register, the history and the generated header,
`git -C <--repo> show|log|diff <--commit>`; it writes only under `--out`. Its
steps, one `ok` / `FAIL` line each:

1. **`inventory`** -- the paths of `--paths` (expect `254`), each present at
   `--commit`, split text and binary (`223` and `31`, R1 C16, C19), printed by
   the script.
2. **`scope`** -- each path's class by ruling (a)'s carve (the stage-A `CARVE`
   rule, one definition), the class sizes printed by the script.
3. **`links`** -- every relative Markdown link in the text rows resolves at
   `--commit`, prefixed and bare, with `http:`, `https:` and `mailto:`
   excluded properly (R3 § 2.9: R3 C17's bare pattern stopped at the colon of
   `https://`); the baseline is `0` dead (R2 C10, R3 C17, R5 C22).
4. **`paths`** -- every backticked repository path resolves after a `:N` or
   `:N-M` suffix is stripped (R5 § B item 21) and placeholders (`<`, `>`, `{`,
   `}`, `*`, `$`, `[`, `]`, ASCII `...` and U+2026) are skipped (R3 § 2.1), or
   sits on `allow-legit.txt` in a class -- `external` (the seven rocknix.org
   pages, the fifteen presumed RAOfflineProxy paths, the two splash
   repositories' wordmark tools of L-14 and L-19 and the site checkout's
   branch of L-13, X02), `pattern`, `historical` -- with its reason; R3 C17's
   baseline is `path-dead=40` (30 distinct) in its reference class; of its
   four candidates three are ruled `external` and one is a real absent
   in-tree path, `packages/rocknix` (L-20), which FAILs until ruled or
   allowlisted `historical` with its reason, so the step's baseline is the
   external classes plus that one candidate (the proof's own probe over the
   edit scope: `backticked repo paths 363 dead 39 distinct 29`, over the 223
   `2432 dead 41 distinct 31`, K102 -- its population, not R3's).
5. **`tools`** -- every `tools/<name>` a text row names exists at `--commit`
   (L-14, L-19).
6. **`identity`** -- no `Pixelelated` or `PIXELELATED` anywhere; no
   Rasteratops as the OS's or the release's name, no `maxengel/rocknix` link
   where the fork's own repository is meant and no `/Rasteratops` folder as
   current, outside `allow-legit.txt`'s classes `character` (the character and
   the handle), `historical` (a dated record; `docs/rasteratops/**` per
   `NAMING.md`), `provenance` and `interim-name` (`rasteratops-*` tools and
   `RASTERATOPS_*` variables, #509) (R3 § 2.2, § 2.9); `rocknix.worktrees` is
   not on the list until the coordinator rules L-40.
7. **`retired`** -- no term of the runs block's retired list outside an
   allowlisted `historical` line (R3 § 2.3, § 2.9); a present-tense
   `cloud_migrate_layout` line is a FAIL until L-04's sentence lands.
8. **`cites`** -- every `D-<AREA>-<n>` in the text rows names a register row
   at `--commit`, a `-0+` placeholder skipped (R3 § 2.9; the half
   `register-check` does not read, L-38).
9. **`untouched`** -- with `--since`, no non-merge commit between `--since`
   and `--commit` touches a path outside the `edit-scope` and
   `edit-under-naming` classes, the lane's audit folder, its retro and its
   pointer and work-log appends (rulings (a), (k), (n), (o)).
10. **`generated`** -- `docs/releases/catalog.md` begins with its
    `Generated by` header (R3 C21) and is unchanged between `--since` and
    `--commit`.
11. **`binaries`** -- the 31 binaries' and the 18 art text files' sha256 at
    `--commit` equal those at `--since` (ruling (o), widened at version 2).

**Three allowlists, committed beside it**, every entry
`<path>:<line> <class> <reason>`: `allow-legit.txt` (what is not a defect:
another repository's path, an elided pattern, a historical name in a dated
record, the character, provenance, an interim name); `allow-inherited.txt`
(each finding owned elsewhere, naming its lead and its owner: the coordinator,
#528, #585, #509, #270, #947, #1013, the interface lanes); and
`allow-findings.txt` (this slice's own stage-B findings in the edit scope,
each naming its lead, emptied as stage E fixes them). **An entry with no class
or no reason is a refusal.**

**FAIL-first, in this order, each run's exit and `TOTAL:` line recorded:** (i)
**the baseline** -- the export at the dispatch tip with all three allowlists:
exit 0; (ii) **one mutation per step**, each on its own scratch copy of the
export under `/workspace/tmp/m6-t39/` (never a checkout): a planted
`[x](docs/no-such.md)` in `README.md`; a planted
`` `tools/no-such-tool` `` in `docs/releases/versioning.md`; a planted `` `docs/no-such-dir/` `` path; a planted `Pixelelated` heading and a planted *"Rasteratops OS 0.0.1"* line in `README.md`; a planted `git
rebase --onto upstream/next next
pr/x` line and a planted *"cloud_migrate_layout runs at startup"* line in `docs/pixelelated/cloud-folders.md`; a planted `D-CLOUD-9999`; a scratch commit editing `docs/reviews/order.md`, one editing a `licenses/` file and one appending a row to `docs/releases/catalog.md` by hand (in a throwaway clone under `/workspace/tmp/m6-t39/`, never the worktree); one byte appended to a PNG -- **each exit 1 naming its own step**, the stub checked against the unfixed text first (`engineering-practices.md` § Guards must fail closed: T21's S11 stub is the lesson); (iii) **the tip with `allow-findings.txt` withheld**: exit 1 naming each of the slice's own findings -- the record's FAIL at the tip; (iv) **after stage E**, the same withheld: exit 0, every remaining entry either fixed or moved to `allow-legit.txt` or `allow-inherited.txt` with its reason. **Refusals exit 2**, "nothing checked": no `--tree`; a `--tree` with a `.git` in it (a checkout); `--paths` absent or not 254 lines; `python3` missing; the register unreadable at `--commit`; an allowlist entry without its class or reason. Each command's `rc=$?` on its own line; **the last line `TOTAL:
<passed> of <checks>
steps`, printed by the script and quoted, never summed by hand**. A planted credential-shaped value, if a mutation ever needs one, is assembled at run time, never a literal (`.githooks/pre-commit`
refuses the literal).

**The art bytes are not edited** (ruling (o), widened at version 2 to the 18
art text files of the `CARVE art-bytes` class -- open item 21, settled by the
coordinator; R3 § 1 is the reason):
`tools/rasteratops-identity-check` binds
`docs/pixelelated/art/pixelelated-wordmark.svg`'s sha256 to the
EmulationStation and theme copies (R3 C12), so an edit to the SVGs, the
generator `docs/pixelelated/art/source/**`, the proofs or the font licence is
outside any stream brief; a finding in an art source is routed to the splash
repository (external), a licence text's (`Tiny5-OFL.txt`) to #528; the two art
READMEs and `wordmark-system.md` are prose, in the edit scope.

**A fix lands only under a stream brief** at the stage-D pause, on the slice
branch, inside the edit scope (ruling (a)) -- proven where it can be: its
lead's check line (§ 3) FAILing on the tip's text and PASSing on the fix's,
both recorded, with `t39-checks.sh` exit 0 at the fix's commit,
`tools/rules-check --quiet` rc 0 (nothing outside the slice moved) and, for a
map edit, `tools/es-menu-map-check` still `0 missing`. Every fix's
`Already written:` line says what the old sentence has already caused -- a
brief, a release note, a rocknix.org draft, an issue body that copied it --
read both, migrated, or nothing inherited, argued (`upgrade-and-install.md`;
D-WORKFLOW-050). **An edit to a document an issue cites by line** (L-15, L-32)
records the cited lines before and after, so the issue's citation is known to
hold or is corrected on that issue by the coordinator.

## 6. Outputs

As T40's § 6 and T38's, scaled for a table slice at Local depth: no packet, no
seat, no guest, no compile (R5 § A); § 7 is this section as checkboxes. All in
the worktree, committed on its branch with messages that cite `#686`
(`Refs #686` while any criterion is open, never a closing keyword). The folder
**`docs/audits/<yyyy_mm_dd>-epic-m6-doctrine-reference/`** (#686's
audit-folder line; T4's date form, `2026_10_24-...`). **The two dispositions
sets, fixed here:** a § Coverage row takes one of `fix`, `inherited:<owner>`,
`ledger`, `#528`, `#585`, `none`; a § The table row -- a misleading statement,
so never `none` -- takes one of `fix`, `inherited:<owner>`, `ledger`, `#528`,
`#585`, where `<owner>` is `coordinator`, `#509`, `#511`, `#270`, `#947`,
`#1013`, `the interface lanes` or `the next upstream base merge`.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `.../00-running-log.md` | opened first: the model and effort that ran, the session, `reviewed-at` (the dispatch tip) with `2174265e9c` and `e3fb3dfe00` beside it, every command with its exit status and time; **every check that stands as a proof announced on a line that begins `PROOF:`** with its time and command; **each stage-B session's last line records `git status --short` empty for the 254** (no fix while reading); its closing census says no build, no compiler, no guest, no fetch, no council or keyed call, no held directory, no `--write` of a generated file, and names the export's path and its retirement at stage H | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: § 2's two blocks with their sha256 prefixes checked and their output, both line figures, the 31 binaries named, the split's lines at the dispatch tip, the `CARVE` lines, the tool's row, the 82 briefs as information; **§ Read order** (§ 2's table, and any move the dispatch comment made); § The reader's pass: what a stranger would have done on each document's strength, group by group, before any auditing (§ 5 rule 5) | A, B |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #686's checklist, in this order: **§ Coverage** (254 rows: the path in backticks as the first cell, its group, tier, inventory lines, text or binary, ruling (a)'s class, the probes' hits -- dead links, unresolved paths, identity words, retired names, decision IDs with their rows' state, tools named and their existence -- Q1 to Q7 each answered or `n/a` with the reason, and its disposition from § 6's set); **§ The table** (one row per misleading statement: `path:line`, the sentence quoted, the artifact it names, what a reader acting on it would do, the owner, the lead number, the disposition); **§ Binaries** (31 rows: path, size, sha256 at the dispatch tip and at `fixed-at`) and **§ Art bytes** (18 rows, the same columns; ruling (o)); **§ The ledgers** (one row each, *"a ledger, not a reference"*, its misleading sentence if any and where it went); **§ The identity words** and **§ The retired names** (per term and per class, at the tip and after stage E, with the allowlists; generated, asserted); **§ The runs** (every § 5 run with exit, wall time, its figure and *a FAIL would mean ...*); **§ Proofs** with `proved:` cells; **§ The streams** (each fix with its check lines); **§ What the coordinator and the next slices inherit** | B to F |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5's interaction audit for the seams § 2 names: the documents x the rules that cite them; the documents x the tools that read three of them (`pr-stack-check`, `rc-preflight`, `release-catalog`); the documents x the issues that cite their lines; the reference set x upstream's copies; and the doctrine futro's predictions checked | B |
| Analysis | `.../04-analysis.md` | Phase 4, then § Finding Verification (4.5, in full: Local depth has no other reviewer), then **§ Renovation face** with one subsection per question Q1 to Q7 (the lint requires all seven): Q4's tables written by `tools/t39-tables.py`; **Q5's cost-against-value table, one row per reference document proper** (lines, last commit, the `R/O/D/W` inbound counts, its role, who reads it, and the verdict -- keep, date its first line, or § 4 question 2); Q6's dead-ends table; § Second opinions reads *not applicable at Local depth (plan § 6c)* | B, C |
| Second opinions | `.../second-opinions/review-plan.json` | depth `local`, the primary in the form T4's plan writes it, lab `anthropic`, reviewers `[]`, `tier_exception` `D-WORKFLOW-184`, `reason` plan § 6c's row (ruling (q)); **no provenance file, no packet manifest, no held sidecar** | C |
| Tools | `.../tools/` | `t39-checks.sh`, its three allowlists, and `t39-tables.py` (writes § Coverage, § Binaries and the Q4, Q5 and Q6 tables from `block-2.txt`, the probes and the export, and asserts their counts -- 254 coverage rows, 31 binaries, 18 art text rows, the dispositions summing to the table's row count by its own line -- so a missing row fails there rather than printing an empty cell, as T40's generator did); each seen to exit 1 on a constructed drift before its table is trusted | C |
| Stages | `.../stage-a/` to `.../stage-e/` | the first commands and § 5's runs under `stage-a/`; the reader's pass notes under `stage-b/`; the checker's FAIL-first and tip runs under `stage-c/`; the streams' runs under `stage-e/`; **no `guest-cycle/`** | A to E |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | prints `PASS pre-issue artifacts (does not certify resolution)`; recorded in `00` | C to D |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category (`Renovation` where it is not a defect), where (`file:line` at the dispatch tip), acceptance, **the ladder stage and the tool that would hold it at the next, or the words *no tool can***; the YAML `punch_index`; an inherited item marked with its owner (`inherit:coordinator`, `inherit:#528`, `inherit:#585`, ...) | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #686 | `Audit: M6 T39 the reference documents -- N findings (X critical, Y high)`; one checkbox per item, each agent-verifiable (D-QA-044); `tools/box-check --issue N` run on it and its line recorded | D |
| Bug issues | GitHub, label `bug`, title `Bug: ...`, milestone-less and not sub-issues (`milestone-phase-naming.md` § Reactive) | one per statement a reader acts on wrongly (§ 4 Q3; D-WORKFLOW-187, D-QA-051): the code-trace shape with *the statement* as the defect's source and *the artifact it misdescribes* as the evidence; *"Can this be done on the VM? No -- the tree, the tool or the register shows it"*; a criterion naming the artifact the corrected statement must match; `Already written:` | D |
| **The stage-D pause** | #686 | the punch list posted with the audit issue's and the bugs' numbers and § 4's two questions; **the lane waits** while the coordinator writes the stream brief `docs/reviews/briefs/t39-streams.md` (D-WORKFLOW-189; plan § 6b stage E: the verdict's lines, the fix as a specification, the test first, the `Already written:` line, the files owned, the commit shape; R5 § C) | D to E |
| Verification | `02` appended; `.../audit-completion.json` | every claim proven where the tree, a tool or the register can show it; every proof's `proved:` cell one of `tree`, `history`, `tool-run`, `fixture`, `design` (T40's five, R5 § C stage F); the Phase 7 gate in `05` | F |
| Retro | `docs/retros/<yyyy-mm-dd>-m6-doctrine-reference.md`, and the same text as a comment on #686 | the mini-retro skill's four answers with its scoped audit, in Instruction-Recommendations mode (plan § 6b G), its *adjustments* written as proposals for the coordinator; **what the slice did to the two time-to-play numbers: nothing, said in those words** | G |
| Hand-back | #686 | `reviewed-at:` and `fixed-at:` written into #686's body by the executor; one comment naming **the one tip** and each artifact by path, the checkers' exit codes, and per fix its `proved:` class | H |
| Lane pointer | `.github/sessions/saved-session-state-feature-m6-doctrine-reference-686.md` | seeded by the coordinator; the executor updates it at every checkpoint | every checkpoint |
| Work log | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session, headed `#686` and the thing decided or learned | every session |

Neither `tools/renovation-status`, `tools/renovation-drift` nor
`tools/renovation-inventory` is run to write a ledger or edited here, and
`tools/release-catalog --write` is never run; a defect in one is a lead on
#686.

## 7. Acceptance

The checklist on #686 becomes this section at dispatch, written there by the
coordinator in place of the five generated ones (ruling (i)). Its first five
items are plan § 6b's contract for every slice, adapted as T38's and T40's
were; the rest are this slice's (D-WORKFLOW-189). Every checkbox names the
artifact that ticks it (D-QA-044); the coordinator ticks at acceptance, from
the artifacts, never from the hand-back's words; where this section and #686
differ, #686 wins and the coordinator corrects the brief.

- [ ] `docs/audits/<date>-epic-m6-doctrine-reference/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `second-opinions/`, `stage-a/` to `stage-e/` and `tools/`, and no `guest-cycle/` (`ls` of the folder in the hand-back).
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-doctrine-reference/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`), and the same with `--issue <audit issue>` prints `PASS`; Q1 to Q7 are answered in `04-analysis.md` and every punch item carries `question:` in the index.
- [ ] `second-opinions/review-plan.json` records `depth: local`, the primary in the form T4's plan at `6ec78bbf8c` writes it, lab `anthropic`, reviewers `[]`, `tier_exception: D-WORKFLOW-184` and plan § 6c's row as the reason (plan § 6c, D-WORKFLOW-137, D-WORKFLOW-184); `ls second-opinions/` lists that file alone; `00`'s closing census shows no `tools/council/run`, no Facilitator, no `npm install` and no keyed call.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, #528, #585, #509, #511, #270, #947, #1013, or a Backlog the coordinator files), withdrawn, or recorded as a ledger row with its reason; `tools/box-check --issue <audit issue>` prints 0 fail; the issue is closed by the coordinator at acceptance.
- [ ] `reviewed-at:` and `fixed-at:` in #686's header carry the lane's commits, and no `-es` pair (nothing in the 254 is EmulationStation's); § 5's removal check with `MERGE_HASH` and `fixed-at` prints no line, the registers' line prints `0`, and `git log --no-merges --format=%h <merge hash>..<fixed-at>` lists only the lane's own commits.
- [ ] `01-research-notes.md` § Scope records § 2's membership block, its sha256 prefix `e81453b6732cdea8` checked, with its exact output lines (`mine: 254 paths.txt: 254 equal: True`; `lines: 38598 reach: {'n/a': 254} tier: {'fork-own': 164, 'upstream-carried': 90}`; `fork-own lines: 28749 upstream-carried lines: 9849`; `read lines: 190 of which fork-own: 190` with its two rows; the two `TREE-SIDE` lines with `equal to mine: True`; `wc -l, the text rows at the P1 hash: 38674`; `grep -c, the text rows at the P1 hash: 38675`; `grep -c, the text rows at the inventory head: 38598`; `present at the merge base: 92`; the `MB..P1:` and `IH..P1:` shortstats -- or the deltas beside them) and both line figures of ruling (h) with the 31 binaries named.
- [ ] `01` § Scope records § 2's split block, its sha256 prefix `afb1909c5cdc6c88` checked, with the defaults' lines, run under `LC_ALL=en_US.UTF-8` (X01), through `P1 grep -c total 38675` and the dispatch tip's `tip:` lines with no `absent` line; the stage-A `CARVE` lines and their `CARVE total 254`; and the `renovation-inventory --order` row for `39 doctrine-reference` (or the lines that printed beside R1 C02's).
- [ ] `00` records, at stage A and before any other check, the lint's `PASS` on a Local plan (T4's exported folder, `rc=0`) and its FAIL on the same plan with `tier_exception` removed (`rc=1`, the FAIL line quoted) -- ruling (q) -- and L-01's loop printing no `MISSING` line (ruling (p)); or, for either, the lines that printed and the question raised on #686 before stage C.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `254`; each row names its ruling-(a) class and a disposition from § 6's Coverage set, and `t39-tables.py`'s own line prints the dispositions' counts and their total `254`.
- [ ] `02` § The table carries one row per misleading statement with its `path:line`, the sentence quoted, the artifact it names, what a reader acting on it would do, its owner and a disposition from § 6's table set; every lead of § 3 appears in it or as a § Coverage `none` with its reason: ``/usr/bin/grep -o -w -E 'L-[0-9]{2}' 02-forward-audit.md | sort -u | /usr/bin/grep -c ''`` prints `46` (`-w`, X04: without it the `711` of L-08's `MAP-TAIL-711-END` is read as a lead id); `t39-tables.py`'s line prints the counts by disposition and their total, equal to the section's row count.
- [ ] `02` § Binaries carries exactly 31 rows (``awk '/^## Binaries/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `31`), each with its size and its sha256 at the dispatch tip and at `fixed-at`, the two equal; `t39-checks.sh`'s `binaries` step prints `ok` at `fixed-at` (ruling (o)); and `02` § Art bytes carries exactly 18 rows (the same `awk` with `## Art bytes` prints `18`), each with its size and its sha256 at the dispatch tip and at `fixed-at`, the two equal, and `git diff --stat <merge hash> <fixed-at> -- docs/pixelelated/art docs/rasteratops/art` names only `.md` files (ruling (o) as widened at version 2, open item 21).
- [ ] The ledger rows are untouched: `git log --no-merges --format=%h <merge hash>..<fixed-at> -- docs/reviews docs/releases/catalog.md docs/pr-series/map.txt docs/releases/rc-accept.txt docs/vm-qa-log.md docs/cloud-sync-changelog.md docs/rasteratops/p0-sweep-hits.txt plans` prints no line, and each of them has a `02` § The ledgers row reading *"a ledger, not a reference"* with its routed finding, if any (ruling (a)).
- [ ] The read-only paths are untouched: `git log --no-merges --format=%h <merge hash>..<fixed-at> -- licenses documentation LICENSE.md docs/upstream` prints no line; every finding in them is a `#528`, `#585` or `inherited:<owner>` row in `02` (rulings (a), (j), (k), (n)).
- [ ] `02` § The runs records, each as a command's own output line with its exit: `tools/rules-check` (with the words *no evidence for the 254*), `tools/register-check`, `tools/release-catalog --check`, `tools/work-log-index --check`, `tools/prose-check --self-test`, `tools/ceremony-check`, `.githooks/hooks-test`, `tools/box-check`; the byte-identity lines against `c445081a59` and `651150fc88`; the identity and retired-name counts; the decision IDs with no `UNRESOLVED` line (D-WORKFLOW-188 carried into the register by ruling (p)'s merge, X03; a line naming it is the coordinator's finding at dispatch, recorded as such); the secret scan in the hooks' form (compile rc at most 1, the runtime-built positive `1`, then `0` files); the non-ASCII count; `tools/forbidden-terms-check` over the 223 and over empty input (`rc=0` both) and over the planted line through `FORBIDDEN_PATTERNS` (`rc=1`, its line quoted); #359's two hashes beside the tree's; `gh release list`'s three lines -- a check without its positive is recorded as such.
- [ ] `tools/es-menu-map-check`'s line is quoted in `02` at the dispatch tip and at `fixed-at`, each `<N> screen(s) at <pin>, <M> in the map, <K> declared unmapped, 0 missing` with `rc=0` (at `e3fb3dfe00`: `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing`, R3 C13), or `CANNOT` with exit 2 named; at `fixed-at` the map's #570 headings say closed: `git show <fixed-at>:docs/es-menu-map.md | /usr/bin/grep -c -E '^#+ Pending.*#570'` prints `0` (ruling (b)).
- [ ] `tools/t39-checks.sh` exists under the audit folder's `tools/`; `02` § The runs quotes its four runs -- the baseline's exit 0, each mutation's exit 1 naming its own step (the stub checked against the unfixed text first), the tip's exit 1 with `allow-findings.txt` withheld naming each finding, and exit 0 after stage E with it withheld -- each with its `TOTAL:` line quoted from the script's own output; its refusals exit 2.
- [ ] `02` § The identity words and § The retired names carry, per term, the count at the tip and after stage E, each a line of `t39-checks.sh` or a generator's; every allowlisted line sits in `tools/allow-legit.txt`, `tools/allow-inherited.txt` or `tools/allow-findings.txt` with its class and reason; `tools/allow-findings.txt` is empty at `fixed-at`, or each remaining line names its stream's disposition.
- [ ] `04-analysis.md` § Renovation face Q4 carries the currency tables written by `t39-tables.py` (the decision IDs with their rows' state, the tools named with their existence, the issues cited with their states, the paths named with their class, the counts and baselines stated with their artifact, the line numbers issues cite with the line); Q5 carries one row per reference document proper with its cost and value columns and the low-inbound count re-derived by the generator's own line; Q6 the dead-ends table; and the two time-to-play numbers named as untouched.
- [ ] § 4's two questions are written in `04` in the shape § 4 gives and posted as comments on #686 at the stage-D pause, and `02`'s row for each cites its comment's id, which `gh api repos/pixelelated/distribution/issues/comments/<id> --jq .body` reads back.
- [ ] Every fix has, recorded in `02` § The streams beside its commit, its lead's check line FAILing on the tip's text and PASSing on the fix's (both lines quoted), `t39-checks.sh`'s exit 0 at the fix's commit and `tools/rules-check --quiet` rc 0; a fix to a document an issue cites by line records the cited lines before and after (L-15, L-32).
- [ ] `02` § What the coordinator and the next slices inherit lists every inherited lead of § 3 with its owner issue -- the coordinator (L-01, L-03's rule half, L-25, L-27 to L-29, L-31, L-33 to L-37, L-40, L-42, the catalog's regeneration, the `t39-checks.sh` Backlog), #528 (L-43 to L-45), #585 (L-46), #509 (L-30), #511 (L-22 where it is not fixed), #270 (L-15's tool half), #947 (L-38), #1013 (L-39), the interface lanes (L-32, and L-17 where a screen change owns it), the next upstream base merge (L-41) -- each at its `file:line`, and the #585 lines owed, never sent.
- [ ] Every bug states its trace, its `Already written:` line and its VM line and passes `tools/box-check --issue N`; every punch item carries the ladder stage and the tool that would hold it at the next, or *no tool can*; every row of § 2's take-up table has a disposition at its lines; the § 1 rulings (a) to (q) each have their `02` row.
- [ ] Every proof in `02` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture` or `design`; ``/usr/bin/grep -c 'proved:' 02-forward-audit.md`` equals ``/usr/bin/grep -c '^PROOF:' 00-running-log.md``.
- [ ] **The host file carries no line of this lane's**: `/usr/bin/grep -c -E 'T39|#686'` over the lines the host file gained between the dispatch comment's recorded line count and the hand-back prints `0` -- no START, no RETURN and no compile START (a table slice compiles nothing; a compile START here is a stop, § 10).
- [ ] The retro exists at `docs/retros/<date>-m6-doctrine-reference.md`, is posted on #686 with its heading's time from `date -u` in the posting command, and says what the slice did to the two time-to-play numbers (nothing, in those words).
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the slice branch before the hand-back merge, and again on the coordinator's simulated merge; `tools/lint-audit-artifacts` prints `PASS` on the folder; the six exit codes pasted on #686.
- [ ] The hand-back is one comment on #686 naming **one tip** and each artifact by path, with `reviewed-at:` and `fixed-at:` only in #686's header; every inherited item is a row of `02` naming its owner issue; and `tools/box-check --issue 686` prints 0 fail.

## 8. What the coordinator and the next slices inherit

Written, not done here; `02` § What the coordinator and the next slices
inherit carries each item as a row with its lines and its owner issue, and the
hand-back names them (§ 7). No pin, no image and no other lane's branch is
moved by this slice, so the list holds no integration step; T39's branch
merges in the coordinator's turn, its exact place named by the coordinator at
acceptance (open item 22, the coordinator's: the order before dispatch is
ruling (p)'s, and T39's place after acceptance is named then).

1. **The coordinator's ledgers and tracker** -- L-01, resolved at dispatch
   (ruling (p)); `rc-accept.txt:13`'s identity (L-25); `map.txt`'s two deleted
   paths (L-27, ruling (e)); the renovation's records -- `docs/reviews/**`,
   the plan's `:528` criterion, T4's boundary sentence and every plan lead
   T38's hand-back names (L-28); the order's preliminary number (L-29); #807
   `:15`, at dispatch (L-37, ruling (i)); #335's stale checkbox (L-42); the
   two issues citing `docs/graphics-memory-testing.md` (L-33); the catalog's
   regeneration and #964's folders without a `RECORD.txt` (L-15) --
   **`tools/release-catalog --write` is the coordinator's, never the lane's**.
2. **The rule and register errata a document read turned up, the
   coordinator's** (D-WORKFLOW-189; T4's rules): `vm-first.md`'s D-QA-016
   sentence (L-03's rule half); the upstream-series rows against
   D-WORKFLOW-084 and `documentation-accuracy.md:48-52`'s *"blocks it"*
   (L-34); `handheld-evidence.md`'s `docs/**` glob (L-35); the two counts of
   the documents that load nowhere (L-36); the rules' worktree path words
   (L-40). **None is edited on this branch.**
3. **Backlog candidates the hand-back names for the coordinator to file**: the
   GENERIC_X64 emulator table -- generate it or drop it (L-31, ruling (j));
   **`tools/t39-checks.sh` promoted to a fork tool** (`tools/docs-check`, R3 §
   2.9), its steps, its three allowlists' classes and its FAIL-first fixtures
   as the input, wired into `ceremony-check --gate` or `fork-checks.yml` only
   after each check has been seen to FAIL once on its constructed case, and
   changing `.githooks/pre-push`'s `PERSONAL_PATTERNS`, `fork-workflow.md`'s
   list and `instruction-files.md`'s tool table in the same change (R3 § 2.9).
4. **#528** (licences and notices): the licence statements that disagree
   (L-43); `licenses/AETHERSX2.pdf` (L-44; the package is another slice's);
   the tree's `LICENSE.md` and `TRADEMARK.md` against #359's recorded hashes
   (L-45). **No clearance sentence is T39's to write** (#528 `:3`, R4 item
   28).
5. **#585** (the contribution queue): `docs/upstream/**`'s findings (L-46),
   L-11's eight hits in `docs/upstream/README.md`, and
   `docs/upstream/raofflineproxy/image-completeness/fix.patch:64`'s line (L-23;
   the full path, X12) -- each a #585 line in the
   shape the lane writes, **never sent** (D-WORKFLOW-164, -165).
6. **The interface lanes (epic #700)**: the map's rows the issues cite by line
   (L-32) and any IA sentence a screen change owns (L-17), each with the
   screen named (ruling (b)).
7. **#509** (the reviewed rename batches): the current release records under
   `docs/rasteratops/` (L-30). **#511** (the website): `site-plan.md:72`'s
   remote, where it is not fixed (L-22). **#270** (the device-facts check):
   the tool D-WORKFLOW-046 promises and `release-candidates.md:38-40` says
   does not exist (L-15). **#947** (`register-check`'s `LIVE`): L-38.
   **#1013**: L-39.
8. **The next upstream base merge** (`release-candidates.md` step 0):
   `documentation/`'s thirteen tables behind upstream (L-41).
9. **The maintainer's two answers** (§ 4): the menu map's journal kept or
   moved; the low-inbound documents kept with a dated first line or retired.
   The coordinator puts both, and a stream brief carries whatever the answers
   make an edit.

## 9. The register and the ceremonies

**The register** (`docs/decision-register.md` at `e3fb3dfe00`: 797 lines,
`## Decided` from `:15`, `## Open decisions` at `:780`, 13 open rows; R4 § 1,
§ 2, C3, C6; R5 C20; the same at `a0fb117b8b`, proof K87; at the coordinator's
tip `b344408e46`, version 2's read, 798 lines, D-WORKFLOW-219 at `:779` and
`## Open decisions` at `:781`, `v2 read`). Each row is read before it is cited
(R5 § B item 8):

| Row | Line | What it binds here |
| --- | ---: | --- |
| **D-UI-039**; D-UI-076 | `:190`; `:332` | *"`docs/es-menu-map.md` is updated in the same change as every row added, moved or renamed"*; the map checked by `tools/es-menu-map-check` -- ruling (b), L-08, L-32 (R4 items 1, 2) |
| D-WORKFLOW-155, -156 | `:658`, `:660` | the canonical flows and their screenshots with every interface change (R4 item 3) -- the map's evidence section is the interface lanes' |
| D-CLOUD-024, -027, -032, -041 | `:62`, `:67`, `:84`, `:98` | the conflict wizard's rows, citing `docs/conflict-wizard-ia.md` -- L-17, L-24 (R4 item 4) |
| D-INFRA-008 | `:94` | *"The device-flashing documentation targets the maintainer's own bench ... not a public installation guide."* -- L-05 (R4 item 5) |
| D-QA-021; D-QA-060 | `:227`; `:692` | the read filter wider than *password*; the browser bench -- L-16 (R4 item 6) |
| D-QA-016, D-QA-027 | `:249`, `:327` | the dedicated QA handheld, decided -- L-03 (R2 L-05) |
| D-WORKFLOW-011, -014, -034, -064, -068, -071, -076; **D-WORKFLOW-084**; D-WORKFLOW-080 (open) | `:239`, `:250`, `:368`, `:486`, `:490`, `:497`, `:502`; `:514`; `:797` | the upstream series and its end -- L-27, L-34 (R4 items 7, 21) |
| D-WORKFLOW-073 | `:499` | the technical appendix lives on rocknix.org, the fork keeps a pointer -- agrees (R4 item 8) |
| D-WORKFLOW-044, **-046** | `:382`, `:390` | the catalog generated, the device facts kept by hand, *"a tool says when they are not"* -- L-15 (R4 item 9) |
| D-WORKFLOW-121, -131, -136, **-144** | `:562`, `:572`, `:587`, `:604` | the component inventory; the marks under `TRADEMARK.md`; Blitterbot; pixelelated -- L-25, L-42, L-43 (R4 item 10) |
| D-CLOUD-174, D-WORKFLOW-151 | `:606`, `:644` | the `/pixelelated` folders; active Rasteratops remnants retired in reviewed batches -- L-30 (R4 item 11) |
| D-WORKFLOW-145 | `:608` | Tiny5 Duo LCD; `README.md:21` agrees (R4 item 12; `:21` by proof K33, X06) |
| **D-CLOUD-175**; D-CLOUD-176 to -179, -181, -182 | `:642`; `:646`, `:648`, `:650`, `:662`, `:666`, `:668` | the cloud-folder migration engine retired -- ruling (l), L-04, L-10 (R4 item 13) |
| D-WORKFLOW-157 to -160 | `:670`, `:672`, `:676` (D-WORKFLOW-159), `:674` (D-WORKFLOW-160) | the build identity; `docs/releases/versioning.md` -- L-39 (R4 item 14; -159 and -160 by proof K92, X07) |
| D-WORKFLOW-164, -165 | `:698`, `:700` | contributions considered and queued, never sent before the initial build -- ruling (n), L-46 (R4 item 15) |
| D-WORKFLOW-167, -168 | `:706`, `:708` | credits and licence disclosures on the website; private owner testing apart from public release -- L-02 (R4 item 16) |
| D-WORKFLOW-185 | `:720` | the shipped-device set; every other target a row in the unshipped tables -- L-41 (R4 item 17) |
| D-WORKFLOW-088 | `:518` | the council toolchain is scaffold's export -- the `docs/council-*` notes describe it (R5 § B item 8) |
| D-WORKFLOW-183, **-184**, **-189** | `:718`, `:719`, `:723` | fan-out is read-only research subagents; **Local for a dead-end table, a provenance table or a doctrine read**; planning and work items the coordinator's (R4 item 19) |
| D-WORKFLOW-217; D-WORKFLOW-218; **D-WORKFLOW-219** | `:777`; `:778`; `:779` (at `b344408e46`) | T37's and T38's ownership rows, the last two decided rows at `e3fb3dfe00` (R5 § F); T38's stage-D pause dispositions (#685, #1394; 2026-11-01), the last decided row before T39's (`v2 read`) |
| D-WORKFLOW-050, -187, -215 | read at `COHASH` | every bug's `Already written:` line; the renovation's bug shape; the hold test (below) |
| D-UI-120 | `:796` (open) | sentence case for explanatory prose; touches a rule, not a reference document (R4 item 22) |

**The highest decided IDs per area**, read from the table above
`## Open decisions` only (R5 § F's `awk` at `e3fb3dfe00`): **D-CLOUD-193,
D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-137,
D-WORKFLOW-218** (R5 C20); `| D-WORKFLOW-219 |` printed no line there (R5
C20) and none at `a0fb117b8b` (proof K89). **Since then D-WORKFLOW-219 is
T38's stage-D pause dispositions row** (#685, #1394; 2026-11-01), so the same
`awk` at the coordinator's tip `b344408e46` prints `D-WORKFLOW-219` as its
WORKFLOW line (`v2 read`); `tools/register-check` printed *"713 IDs, each
once; every citation in the live documents names a row"* (R3 C13; K94 at
`a0fb117b8b`). **This slice's ownership row is D-WORKFLOW-220**, written by
the coordinator at dispatch before `## Open decisions`, its `<date>` checked
on the appended line alone; if another WORKFLOW row lands between (as
D-WORKFLOW-219 did between version 1 and version 2), it is the next free
WORKFLOW ID, and the row, the body fill and the pointer follow it (R5 § B
item 1, § F). **The row, from R5 § F's draft with the coordinator's rulings
applied** (the ledger list of ruling (a), the line figures of ruling (h), the
art text files of ruling (o) and `p0-sweep-hits.txt` of open item 25):

> | D-WORKFLOW-220 | `<date>` | **T39 (#686) owns the reference documents proper among the 254 paths of `doctrine-reference` -- the inventory's area `doctrine` at `2174265e9c` less T4's 36 and T38's 52 (38,598 lines by the inventory's column; 38,675 by `grep -c` over its 223 text rows at the P1 tip, the 31 binaries uncounted) -- and tables the rest without editing it.** The coordinator's twelve documents under `docs/reviews/`, the generated `docs/releases/catalog.md`, the tool inputs `docs/pr-series/map.txt` and `docs/releases/rc-accept.txt`, the running ledgers `docs/vm-qa-log.md` and `docs/cloud-sync-changelog.md`, the P0 sweep's generated baseline `docs/rasteratops/p0-sweep-hits.txt`, the one plan under `plans/`, the 31 binary files and the 18 art text files under `docs/pixelelated/art/` and `docs/rasteratops/art/` (by name, size and sha256; the two art READMEs stay reference documents) are tabled as *a ledger, not a reference*, one row each, their findings routed to their owners; the work logs, futros, retros, audit folders and qa-logs are area `records` and outside the slice. `licenses/` and `documentation/` (the 90 upstream-carried) and `LICENSE.md` are read-only, their findings for #528 or the next upstream base merge; `docs/upstream/` is #585's, read-only; the fork's GENERIC_X64 emulator table is tabled with a Backlog candidate. `README.md` and `TRADEMARK.md` change only where `NAMING.md` decides the word. The rules, `CLAUDE.md`, `AGENTS.md`, `NAMING.md` and the registers are the coordinator's (D-WORKFLOW-189; T4's read, #651): a rule erratum a document read turns up is an inherited item, never a fix on this branch; a menu-map row an interface change made stale is the interface lanes' (D-UI-039). Local depth, `tier_exception` D-WORKFLOW-184, no reviewer, no guest and no keyed call. | #686; #807; #651; #685; #528; #585; D-WORKFLOW-184; D-WORKFLOW-189; D-UI-039 |

The pointer's `Register:` line is filled from the same `awk` at `COHASH`,
never from here (§ 10).

**Rows the pause may need, all put to the coordinator as questions, never
decided by the lane:** the menu map's journal (§ 4 question 1); the
low-inbound documents (§ 4 question 2); the device-facts pointer's wording against the rows issues cite by
number (L-15); the GENERIC_X64 table's Backlog (L-31); `t39-checks.sh`'s
promotion (§ 8 item 3). (Version 1 also asked whether ruling (o)'s *never
edited* reaches the art text files; the coordinator widened the ruling at
version 2, open item 21.) A row this slice forces takes an ID the coordinator
assigns on #686.

**The ceremonies** every lane owes are the rules that load every session --
`learning-capture.md` (the work-log entry per session headed `#686`, its time
from `date -u` in the same command, `tools/work-log-index --write` after it),
`ceremonies.md` (a friction line the moment something slows, `issue: #686` or
the guard; `tools/ceremony-check --gate` before every push, never
`--no-verify`), `decision-register.md` (a row the same session for any
decision), `vm-first.md` (the VM question before any proof: § 5 answers it),
the mini-retro at stage G posted on #686 in Instruction-Recommendations mode
with its *adjustments* as proposals for the coordinator -- and are not
restated here. What is this slice's:

- **What a hold is**: a finding is held off the public tracker only under
  D-WORKFLOW-215's test; holding is the coordinator's, and the lane never
  opens a held directory (`/workspace/tmp/m6-t34/held/` and
  `/workspace/tmp/m6-t36/held/` included). None is expected in a table of
  reference documents; a finding the lane thinks that row's test may cover is
  raised with the coordinator on #686 before anything about it is posted.
- **The same-commit rules, stated once:** a map edit's commit records
  `tools/es-menu-map-check`'s line after it (D-UI-039 is the interface lanes',
  so the commit says no screen changed); a document edit's commit records its
  lead's check line before and after and `t39-checks.sh`'s exit at the commit;
  an edit to a line-cited document records the cited lines; no commit touches
  a ledger row, an upstream-carried file, `LICENSE.md`, `docs/upstream/` or a
  binary (ruling (a)).
- **Every count is a tool's line** (`engineering-practices.md` § A name is not
  a behaviour): a figure in `02`, a post or the hand-back is the command's own
  output, quoted; a sum, a difference or a rate is computed by the command
  that prints it; **`rc=$?` on its own line after the command, never after a
  `$(...)` in the same word or a pipeline's last stage**; **no `cut` on an
  expected error line**; **a heading's time from `date -u`, never typed**.
- **Prose goes into a running log or a note through a quoted heredoc
  (`<<'EOF'`) or the Write tool, never an unquoted one** (plan § 6b: an
  unquoted heredoc runs every backticked name in the prose, and the 254 are
  full of them).
- A merge with conflicts is checked for markers; the ledgers united by whole
  entries; **a commit names its paths**; anything temporary under
  `/workspace/tmp/m6-t39/` after `df -i`, never `/tmp`; the export and the
  lint proof under `/workspace/tmp/m6-t39/` retired at stage H, their paths
  and retirement in `00`'s census (D-INFRA-022); **`rm -rf` only as
  `"${VAR:?}"/...` or a literal path, in its own short command, never inside a
  `bash -c` script**.
- A fixture rewrites no path outside scratch; **a credential-shaped value
  assembled at run time, never a literal** -- `.githooks/pre-commit` refuses
  the literal; a generator seen to exit 1 on a constructed drift before its
  table is trusted.
- **Every edited file checked for an unfilled placeholder before its commit**:
  `/usr/bin/grep -c -E '__[A-Z0-9_]+__'` is 0 on the pointer, the running log
  and every artifact (the widened pattern of T38's errata before dispatch: the
  narrower one missed a placeholder with a digit and one with an underscore),
  and none of § 1's four hash words appears unfilled in a filled artifact
  (`/usr/bin/grep -c -w -E 'COHASH|MERGE_HASH|TIPHASH|V2HASH'` is 0 there).
  This brief carries the four names as its own words, so it is never copied
  into an artifact unfilled.
- Commit messages `docs: ...` on the slice branch for the audit folder, with
  `Refs #686`; a reference-document fix in the history's form
  (`docs: <document>: ...`), `Refs #686, #<bug>`; no closing keyword before an
  issue number while a criterion is open (`issue-tracking.md`).

## 10. Hand-back, the pointer, the host, the stops and what never runs

**The hand-back.** The coordinator accepts by reading, in this order, without
re-reviewing: #686's checkboxes against their artifacts; the lint's `PASS`
line on the default phase and with `--issue`; `review-plan.json` (Local, no
reviewer, `tier_exception` D-WORKFLOW-184, read directly) and
`ls second-opinions/` showing it alone; `00`'s stage-A lint proof and L-01's
loop (rulings (q), (p)); the audit issue's checkboxes all at an outcome; the
coverage table's row count (254), the binaries' (31) and the table's
dispositions with their generator's line; every bug with its three lines;
**re-running on a clone of the slice branch at its tip under
`/workspace/tmp/m6-coordinator/`: § 2's two blocks and their dispatch-tip
lines, the `CARVE` lines, every § 5 run in full, and `tools/t39-checks.sh`
with its four runs**, through the coordinator's acceptance script
**`kit/t39-accept.sh`**, written by
**`kit/selftest/accept-t39/derive-t39.py`** from `kit/t36-accept.sh` the way
`derive-t38.py` wrote T38's (R5 § E; R3 § 4), naming the dispatched brief's
lines and sha256 from the start (R5 § B item 19) and its FAIL fixtures in a
named directory beside it (R5 § B item 20), its section list read by grep
before a header is copied (R5 § B item 18); its usage as T38's,
`AUDIT_ISSUE=<n> BUGS="<numbers>" DISPATCH_TIP=<MERGE_HASH's value> bash t39-accept.sh <lane tip> <coordinator tip>`
(R5 § E, C19), no ES tip. Its conventions are T38's: one
`VERDICT PASS|FAIL|CANNOT|ABSENT|RAN <section> -- <reason>` line per section,
`SUMMARY: pass N, fail N, cannot N, absent N, ran N`, `ACCEPT-RC` 0 when every
section is PASS or RAN, 1 on any FAIL, 2 on no FAIL but a CANNOT or ABSENT;
`rc=$?` on its own line; counts by `/usr/bin/grep`; every awk regex through
`ENVIRON`, never `awk -v`; the whole output through the credential mask;
writes only under `ACCEPT_DIR` and `OUT` (R3 § 4; R5 § E, C19). **Kept and
re-pointed** (R3 § 4; R5 § E): `pointer` (T39's keys), `folder`
(`*-epic-m6-doctrine-reference`), `dist-tip`, `product-paths` (inverted: the
lane's commits touch only the edit scope, its audit folder, its retro, its
pointer and its log entries), `membership` (254 by § 2's block, its inputs at
`2174265e9c`; T38's section goes ABSENT where `inventory.json` is not at the
tip, R3 § 4), `tree-counts` (both figures of ruling (h)), `issue-body`
(`reviewed-at:`/`fixed-at:`, the `-es` pair absent), `bug-bodies`, `lint`,
`review-plan-local`, `lint-proof`, `punch-list`, `ladder`, `audit-boxes`,
`bug-boxes`, `scope-record`, `read-order`, `tables` (coverage `254`),
`generated` (`02`'s sections marked generated, asserted -- **a different thing
from `docs-generated-untouched` below; the names are kept apart**, R3 § 4),
`analysis-face`, `checker-run`, `checker-record`, `fixes-record`,
`inherited-record` (the owners of § 8), `proof-lines`, `lane-boxes`, `proved`
(T40's five words), `rulings` ((a) to (q)), `analysis`, `last-comments` (#686,
#807), `streams`, `record-lines` (the #585 lines owed), `generators`,
`runs-record`, `running-log`, `no-compile`, `handback`, `retro`, `checkers`,
`merge`, `runs`, `scratch`; `question-comments` (the two § 4 questions are
posted as comments). **Dropped** (each reads skills, agents, pins or the
bundle): `skills-frontmatter`, `skills-xref`, `skills-stale-names`,
`agents-roster`, `agent-pins`, `bundle` (R3 § 4; R5 § E). **Added**, each with
a FAIL fixture seen to fail before the section is trusted (R3 § 4; R5 § E):

| Section | PASS when | FAIL fixture |
| --- | --- | --- |
| `docs-links` | every relative Markdown link in the text rows resolves at the lane's tip, prefixed and bare, `https:` and `mailto:` excluded; the line quoted | a scratch tree with `[x](docs/no-such.md)` added to `README.md` |
| `docs-paths` | every backticked repository path resolves after its `:N[-M]` suffix is stripped, or sits on an allowlist with its class and reason; the four candidates of L-13, L-14, L-19, L-20 each fixed or ruled | a planted `` `tools/no-such-tool` `` line |
| `docs-identity` | no `Pixelelated`/`PIXELELATED`; no Rasteratops as the OS's or the release's name outside `NAMING.md`'s allowances and the allowlist's classes | a planted `Pixelelated` heading; a planted *"Rasteratops is the OS name"* line in a copy of `README.md` |
| `docs-retired` | every retired-name hit classed current or historical in `02`, and no current-tense hit surviving the fixes | a planted *"run cloud_migrate_layout to move your library"* line in a copy of `docs/pixelelated/cloud-folders.md` |
| `docs-cites` | every decision ID in the text rows names a register row (`-0+` skipped) | a planted `D-CLOUD-9999` |
| `docs-generated-untouched` | the lane's non-merge commits leave `docs/releases/catalog.md` unchanged; `tools/release-catalog --check` passes on the coordinator's host (`release-catalog: current (<n> cuts)`) | a fixture commit appending a row to `catalog.md` by hand |
| `ledgers-untouched` | the lane's non-merge commits touch no ledger row of ruling (a), no records path other than its own audit folder, retro, pointer and work-log appends, and no T4 or T38 path; the registers take appends only | a fixture commit touching `docs/reviews/order.md`; a `-` line in a decided register row |
| `upstream-carried-untouched` | the same over `licenses/`, `documentation/`, `LICENSE.md` and `docs/upstream/` (rulings (a), (j), (k), (n)) | a fixture commit editing one `SUPPORTED_EMULATORS_AND_CORES.md` row |
| `binaries-untouched` | the 31 binaries' sha256 at the lane's tip equal those at the dispatch tip (ruling (o)) | one byte appended to a PNG |
| `art-bytes-untouched` | the diff over `docs/pixelelated/art/` and `docs/rasteratops/art/` touches only their `.md` files | one byte appended to `pixelelated-wordmark.svg` |
| `menu-map-check` | `tools/es-menu-map-check` passes on the lane's tip with `0 missing`, or its `CANNOT` names the missing ES checkout; `02`'s row for the map carries the line | a copy of the map with one `## Not mapped` declaration removed |
| `table-record` | `02` § Coverage has 254 rows and § The table one row per statement, each disposition from § 6's sets, each `fix` naming its stream's commit and each inherited row its owner's issue | a copy of `02` with one coverage row deleted and one disposition misspelt |
| `forbidden` | the slice's text rows concatenated through `tools/forbidden-terms-check --stdin`, rc 0 **after** the planted `FORBIDDEN_PATTERNS` positive exits 1 | the positive itself |
| `secret` | `.githooks/secret-patterns` sourced in a subshell, one `grep -E -e` per file, counts only: 0 files after the runtime-built positive counts 1 | the positive itself |
| `nonascii` | RAN (informational: `NON-ASCII FILES: 78 LINES: 1359` over the 215 at `e3fb3dfe00`, R3 C20) | -- |

Then `register-check` on a simulated merge with the coordinator's tip; the
retro's answers; the checkers' exit codes; the inherited items' rows and their
owner issues with `tools/box-check --issue 686`'s line (§ 7's last checkbox);
**the § 1 rulings' rows in `02`**. The lane posts one hand-back comment naming
**its one tip** and each artifact by path, writes `reviewed-at:` and
`fixed-at:` into #686's body, then says it is idle. **The hand-back's hashes
are § 1's placeholders, filled**: `reviewed-at:` is the commit the read was
made at (`MERGE_HASH`, the dispatch tip), `fixed-at:` the lane's `TIPHASH`
when the fixes are complete, § 7's `<merge hash>` is `MERGE_HASH` and its
`<fixed-at>` that `TIPHASH`, § 5's removal check runs with the pointer's
values, the register's line is read at `COHASH`, and the brief is cited at
`V2HASH`; none of the four words appears unfilled in the comment (§ 9's
placeholder check). After acceptance the coordinator closes the audit issue,
prompts the lane for `audit-completion.json` and the lint against **the audit
issue**, merges the slice branch in its turn (§ 8), regenerates the ledgers
and the catalog itself, files the Backlogs the hand-back names, writes the
rule errata into a sweep of its own, carries § 8's #528 and #585 items to
their issues, and closes #686 when every row is proven; the doctrine epic #807
closes when T4, T38 and T39 have.

**The pointer the lane checks at stage A, line by line.** The seeded pointer
`.github/sessions/saved-session-state-feature-m6-doctrine-reference-686.md` is
written by the coordinator from T38's. So before the first command after `cat`
the lane reads these eleven keys -- the keys verbatim from T38's pointer, the
values T39's (R5 § A) -- each against the one value that would be the seeding
error, **T38's**, and reports any that names the predecessor on #686 before
going on. **The four hash words and the register IDs are the seeding's to
fill**; a pointer line still carrying one of them unfilled is a seeding error
too. Every figure in the *Must read* column is § 1's, § 5's or § 9's, copied
from that one place (R5 § B item 6):

| Key | Must read | The seeding error reads |
| --- | --- | --- |
| `Branch (distribution):` | `feature/m6-doctrine-reference-686` stacked on `feature/m6-p1-survey-641` at the P1 tip the dispatch comment names (`2174265e9c` today), the coordinator's branch merged | `feature/m6-doctrine-skills-685` |
| `Worktree (distribution):` | `/workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-reference-686` | `m6-doctrine-skills-685` |
| `Worktree (EmulationStation):` | **none**: nothing in the 254 is EmulationStation's; the ES checkout is read by `git -C ... grep <pin>` for L-07's labels only | any ES branch or worktree named for #686 |
| `Executor:` | Opus 5.5 at high effort, in the session the dispatch comment names (ruling (f): `m6-t1-os-launch` or `m6-t3-emulators`, whichever freed first) | T38's session, `m6-t5-build-engine` |
| `Epic:` | #807; T4 (#651) at its tip `6ec78bbf8c` (R4 § 4); T38 (#685) in its stages or accepted, as the dispatch comment says (R5 C18: its stage-A checkpoint accepted at the research's read) | "T39 (#686) after", or T38's predecessor line |
| `Depth:` | **Local -- a table**: the executor alone; `review-plan.json` with reviewers `[]` and `tier_exception` D-WORKFLOW-184; no seat, no packet, no keyed call | *"Local -- a doctrine read"* |
| `The lens:` | cost against value over the 254 of `doctrine-reference` -- the area's `rest`: `README.md`, `TRADEMARK.md`, `LICENSE.md`, `licenses/`, `documentation/`, `plans/` and the reference documents under `docs/` -- 38,598 lines by the inventory, 38,675 by `grep -c` over the 223 text rows at the P1 hash, 31 binaries uncounted | cost against value over the 52 of `.claude/**` less `.claude/rules/**` |
| `The rule:` | the lane changes only the reference documents proper of ruling (a), only at stage E under a stream brief; **never** a ledger row, `licenses/`, `documentation/`, `LICENSE.md`, `docs/upstream/`, a binary, the art bytes, `.claude/**`, `CLAUDE.md`, `AGENTS.md`, `NAMING.md`, a register (beyond the appends the procedure owns), `tools/`, `scripts/`, `packages/` or `projects/`; no council, Facilitator or keyed call; no `--write` of a generated file (rulings (a), (k), (n), (o), (q)) | "the lane changes only the fork-adapted skills among the 52" |
| `The host:` | **none**: no guest window and no compile; the host file read once at stage A for its protocol and its line count; no START, RETURN or compile line of this lane's in it at any stage | a line naming T38 or #685 |
| `Register:` | the highest decided row per area read from the table at `COHASH` (at `e3fb3dfe00`: D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-137, D-WORKFLOW-218; at `b344408e46` D-WORKFLOW-219, T38's dispositions row, is the WORKFLOW line), plus **this slice's ownership row, D-WORKFLOW-220, which the coordinator writes at dispatch** | D-WORKFLOW-218 or D-WORKFLOW-219 named as this slice's own row |
| `The brief:` | `docs/reviews/briefs/doctrine-reference.md` at `V2HASH` (filled by the dispatch comment; version 1 has no dispatch hash, and no `docs/reviews/briefs/doctrine-reference.md` exists at `e3fb3dfe00`, R1 C18) | `doctrine-skills.md`, or the literal word `V2HASH` |

**The host.** No guest window and no compile, so this slice holds no slot in
the host file's queue: the file the dispatch comment names
(`/workspace/tmp/m7-m6-host-coordination.txt`, named by T38's brief `:1106`
and `:1674`; it exists and held 710 lines at the proof's read, C10; open item
23, confirmed by the dispatch comment with its line count) is read once at
stage A, whole enough for its
protocol and with the time of the read and its line count, which the dispatch
comment also records; the lane writes no line in it and posts no
`START HH:MM:SS UTC` on #686; **a START or a compile line of this lane's, in
the file or on #686, is a stop** (a table slice compiles nothing; ruling (q)).
The guarded swap reclamation is not this slice's. No build on the host at any
time.

**The readings before dispatch** (plan § 3, principle 3): the doctrine futro,
`docs/futros/2026-10-24-m6-doctrine.md` (486 lines; its T39 lines `:7` and
`:9-10`, the latter *"It does not cover T38's or T39's briefs (their own
readings at their dispatch)"*; R5 C16), takes a **T39 kickoff addendum**
written by the coordinator at dispatch, **after T38's addendum**
(`## T38 kickoff addendum (written with the brief's version 2, 2026-11-01)` at
`:472`, R5 C16, C23), at its level and in its shape (ruling (m); R5 § C): a
heading `## T39 kickoff addendum (written with the brief's version 2, <date>)`
and six bold-led paragraphs -- **The plan, in the order's words**
(`order.md:673-681`, with the 38,598 against 38,675 fact and the 31 binaries);
**Assumptions the plan leans on and does not state** (that the slice holds the
daily ledgers -- R5 § 0 refutes it; that the 254 are all the fork's to edit --
90 are upstream's, and ruling (a)'s ledgers are not; that `tools/rules-check`
or `tools/register-check` reads the reference documents -- one reads none, the
other 4; that `docs/rasteratops/` is all historical -- two current records
live there, L-30; that a `rest` slice's membership is fixed by a glob -- the
82 briefs show it moves with the tree); **Known unknowns** (the futro's `:7`
and `:9-10` as their spine, and this brief's open items); **Patterns** (the
friction log's `:137` and `:417`; a record presenting itself as current; a
count true once; a checker whose rc 0 covers nothing in the slice); **What we
could be missing (the simulation)** -- an Opus lane with only the brief: edits
`licenses/` text it finds stale; rewrites a `docs/reviews/` page because it is
among the 254; regenerates the catalog with `--write`; "fixes" every
Rasteratops hit including the historical ones `NAMING.md` keeps; deletes
`plans/` as stale; treats a crude probe's 145 dead paths as 145 findings (R5
C22); corrects `docs/pr-series/map.txt` and so changes what `pr-stack-check`
builds; restructures the menu map's journal; edits an art SVG and breaks the
identity check (R5 § C; R3 § 1); **Adjustments before execution**; then the
version-2 line. The stranger's proof of version 1 makes version 2; this
brief's hash at dispatch is `V2HASH`.

**Stop only on:** every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); the stage-D pause (the punch list, the audit issue,
the bugs and § 4's two questions posted on #686; the lane waits for the
coordinator's stream brief and does no remediation before it, drafting
meanwhile the retro's four answers and the Q5 table's verdict column, and
editing none of the 254); an explicit maintainer pause on #686; a blocker
named on #686 -- two commands that disagree, a block whose output differs from
§ 2's beyond the deltas it records, a path of the 254 at the lane's tip
differing from the dispatch tip before stage E, a pointer line that names T38,
**a keyed call, a `tools/council/run` call or a Facilitator run found in
`00`**, **a START or a compile line of this lane's on the host file or on
#686**, a write to a ledger row, a read-only path, a binary or a doctrine
owner's file; or an execution limit, stated as such with the running log
current. **Not** a stop: the absence of a reviewer (Local depth);
`tools/rules-check`'s rc 0 over files it does not read (§ 3 item 5); a
`CANNOT` from `tools/es-menu-map-check` without an ES checkout; a rule erratum
or a finding in a read-only file (each is inherited); 38,598 against 38,675
(two measures, ruling (h)); the 82 briefs the selector would reach
(information, § 2); the lint's Local PASS not printing at stage A (a question,
§ 5); `next` moving under the slice. A checkpoint is not a stop
(D-WORKFLOW-149). An idle session says it is idle on #686, **and does not end
a turn on a post that asks nothing**: a turn ends on a post or a commit, never
on "next is ...".

**What never runs in this slice:** an image build, a package build or any
compiler; `config/options` sourced anywhere; a guest; a fetch -- no
`git fetch`, no `git ls-remote`, no `gh api` of another repository's contents
(the one `gh` read of another name is R2's redirect check,
`gh api repos/maxengel/rocknix`, which this lane need not repeat); a council
run, a Facilitator call, any `tools/council/run` call keyed or keyless, any
`scripts/council-*`, `scripts/verify-*` or `node` script, `npm install`;
`tools/release-catalog --write`, `tools/renovation-status` or
`tools/renovation-drift` writing a ledger, or any generator that writes a
ledger (`tools/work-log-index --write` after the lane's own log entry
excepted); `tools/pr-stack-check` (it makes a worktree);
`tools/rasteratops-identity-check` unless an edit reached `LICENSE.md`,
`TRADEMARK.md` or the wordmark, with its temporary directory under
`/workspace/tmp/m6-t39/`; a handheld; the owner's accounts or any hosted
account; M7's roots, worktrees or prep directories; a held directory
(D-WORKFLOW-215; `/workspace/tmp/m6-t34/held/`,
`/workspace/tmp/m6-t36/held/`); `~/.config/council/env`, anything under
`~/.ROCKNIX/` or `~/.rocknix/`, the wordlist
`~/.config/rocknix/forbidden-terms` (its tool alone reads it), the user-level
`~/.claude/`; a print of a credential-shaped line or of a variable's value (a
variable is named, never printed); `guard_load` (it sources the wordlist); an
edit to any ledger row, `licenses/`, `documentation/`, `LICENSE.md`,
`docs/upstream/`, a binary or the art bytes (rulings (a), (j), (k), (n), (o));
an edit to any `.claude/**` file, `CLAUDE.md`, `AGENTS.md`, `NAMING.md`, a
register (other than the appends the procedure owns), `tools/`, `scripts/`,
`packages/` or `projects/`; an edit at stage B; a new file under the
repository's `tools/` (the fork tool is a Backlog, § 8 item 3); an edit to
`.github/sessions/saved-session-state-next.md` (T46's); the coordinator's
files (`order.md`, `slices.json`, `areas.json`, the plan, this brief, #686's
criteria, the M6 body, the futro); a post on #807, #528, #585, #509 or #346;
bare `git stash`; `--no-verify`; `git worktree remove --force` or `rm -rf` of
any worktree; a write in another lane's worktree; and a credential-shaped
literal in a fixture.

## Version 1: what the drafting read did not settle

Every open mark of version 1, with the read that settles it; then the places
where the research files disagree, and how this brief takes each; then the
checks on this file. The stranger's proof of version 1 reads this list first,
and version 2 records each item's state after it (T38's shape: **Settled**,
with where the body carries the fact and its command, or **Open**).

**The open marks** (each is a mark in the body, cited by its section):

1. **Ruling (a)'s class sizes** (§ 1 (a), § 5's `CARVE` command, § 7) -- the
   edit scope, the ledger, read-only, binary, art and naming-restricted
   classes counted. Settles: the stage-A `CARVE` lines, quoted in `01`.
   **Settled**: proof K26's `CARVE` lines at `a0fb117b8b` (`CARVE total 254`),
   re-run for version 2 with `p0-sweep-hits.txt` in the ledger (§ 1 (a); the
   expected lines beside § 5's command).
2. **Which of the 254 claim a guest behaviour** (§ 1 (q), § 5 rule 3) -- R5 §
   D and R3 § 6 did not read every sentence. Settles: stage B's table, each
   such sentence a `02` row with the proof a later slice could make. **Open**:
   the lane's stage B (§ 5 keeps its mark).
3. **The dispatch tip's split lines and the selector's reach there** (§ 2,
   § 5) -- ruling (p) says no `absent` line; the counts of `changed` and of
   briefs added depend on the dispatch. Settles:
   `G="$PWD" TIP=<MERGE_HASH's value> bash .qa-scratch/t39/split.sh` at
   stage A. **Open**: no dispatch tip exists; at `a0fb117b8b` `8 ... absent`,
   `3 ... changed`, `1 ... same` and `selector reaches: 329 paths; added since
   P1: 83` (proof K11, K19; § 2); since version 2 the run is under
   `LC_ALL=en_US.UTF-8` (X01).
4. **Whether the worktree's `tools/renovation-inventory --order` prints R1
   C02's lines** (§ 2, § 5) -- R1 ran it from the clone's directory. Settles:
   the stage-A run, with `git status --short --ignored` before and after.
   **Open** for the worktree; the proof's run from the clone reproduced R1 C02
   with the status unchanged (K20; § 2).
5. **`tools/box-check`, `tools/ceremony-check` and `.githooks/hooks-test` at
   the dispatch tip** (§ 3 item 5, § 5) -- no research file for this brief ran
   them. Settles: their stage-A lines. **Open**: not run by the proof either;
   `box-check`'s predicate over § 7 printed `brief s7 boxes 27 fail 0` (K118).
6. **The lint's Local proof** (§ 5's `# STAGE A`): T4's plan's three fields
   (`t4 plan: local D-WORKFLOW-184 0` expected), the PASS line and the FAIL
   line with `tier_exception` removed -- no research file for this brief ran
   the lint on a Local plan; R3 § 3 says T38's ruling (m) did. Settles: the
   stage-A lines. **Settled**: `t4 plan: local D-WORKFLOW-184 0`, `rc=0`
   ending `PASS`, `rc=1` with its FAIL line (proof K111; § 5's `# STAGE A`).
7. **L-04**: whether the two files cite D-CLOUD-175 at the tip, and R3's
   join/follow heuristic's 10 unread reference lines (R3 C18). Settles: L-04's
   check line and stage B's read. **Settled** for D-CLOUD-175: `0` and `0`
   (proof K45; L-04); the ten join/follow lines stay **Open** (stage B).
8. **L-12**: the counter note's banner words at the tip. Settles: L-12's check
   line. **Settled**: `0` (proof K54; L-12).
9. **L-13**: whether the seven rocknix.org pages exist in
   `ROCKNIX/rocknix.org` (outside the tree; not fetched). Settles: a
   `git -C <a local checkout> ls-tree` at its default branch where one is
   present, never a fetch; otherwise recorded as not settled. **Open** (outside
   the tree); the name itself is the site checkout's branch, an `external`
   entry (X02; L-13).
10. **L-16**: whether the policy's mask carries the flag form (R4 item 6).
    Settles: L-16's check line. **Settled**: `0`, so **fix** (proof K58; L-16).
11. **L-17**: the IA's text against D-CLOUD-024, -027, -032, -041 and #134's
    rev 5 (R4 item 4). Settles: stage B's read with the revision line.
    **Settled in part**: the IA is at rev 6 (`:19`), past #23's rev 5 (proof
    K59; L-17); the text against the four rows stays **Open** (stage B).
12. **L-23**: the `maxengel/rocknix` links over the 254's paths rather than
    R3's classes. Settles: L-23's `git grep -c` line. **Settled**: the changelog
    alone (proof K64; L-23).
13. **L-24**: which decided row superseded the plan's choices (R2 C20 found
    none; D-CLOUD-041 is the candidate). Settles:
    `tools/archaeology --no-gh 'KEEP CLOUD'` and the rows it names, read.
    **Open**: `tools/archaeology` not run by the proof; the lane's stage B.
14. **L-26**: whether this brief's non-comment count reproduces R4 C25's
    `total non-comment: 9` (R4 does not print its command). Settles: L-26's
    check line. **Settled**: `9` (proof K68; L-26).
15. **L-38**: the decision IDs over the 254's text rows (R3 C23 read its own
    population). Settles: § 5's `cites` command, no `UNRESOLVED` line
    expected. **Settled with a finding**: `UNRESOLVED D-WORKFLOW-188` over the
    223 at P1 against the register at `a0fb117b8b`; ruling (p)'s merge carries
    the row, and a line at dispatch is the coordinator's (X03; L-38, § 5).
16. **L-39**: #1013's criterion at the lane's ref. Settles: L-39's check line.
    **Settled**: nothing printed, so **inherited:#1013** (proof K80; L-39).
17. **L-45**: the tree's `LICENSE.md` and `TRADEMARK.md` sha256 against #359's
    (R4 § 8). Settles: § 5's hash loop. **Settled**: equal to #359's (proof K85;
    L-45, § 5).
18. **L-37**: #807's sentence and the coordinator's erratum beside it (ruling
    (i)). Settles: the stage-A `gh` read. **Settled in part**: the sentence
    present and `errat` 0 (proof K78; L-37); the erratum is written at dispatch.
19. **The export's file count at the dispatch tip** (§ 5's runs): `254` by
    ruling (p), against `246` at `e3fb3dfe00` (R2 C6; R3 C20). Settles: the
    runs block's `find | grep -c` line. **Open**: at P1 every one of the 254 is
    present (`of the 254 absent: 0`, proof C11); the dispatch tip's line is the
    lane's.
20. **R2 C8's identity counts**: whether they count lines or occurrences (R2
    does not print its command). Settles: nothing here -- the lane's loop
    prints lines and files, recorded as its own figures beside R2's.
    **Settled**: occurrences (proof K104); § 5's runs carry K103's line figures.
21. **The art bytes as a ruling** (§ 5, § 9): the drafter extends ruling (o)'s
    *never edited* to the SVGs, the generator, the proofs and the font
    licence, because `tools/rasteratops-identity-check` binds the wordmark SVG
    (R3 C12). Settles: the coordinator's dispatch comment. **Settled** by the
    coordinator at version 2: ruling (o) widened to the 18 art text files, the
    two art READMEs the area's reference documents (§ 1 (o), § 5, § 7).
22. **T39's merge order** (§ 8). Settles: the coordinator at acceptance.
    **Settled** as the item says: the coordinator's, at acceptance; the order
    before dispatch is ruling (p)'s (§ 8).
23. **The host file's path** (§ 5, § 10): T38's brief names one; no research
    file for this brief read it (R5 § D). Settles: the dispatch comment, with
    the file's line count. **Settled**: `/workspace/tmp/m7-m6-host-coordination.txt`
    (T38's brief `:1106`, `:1674`; 710 lines at the proof's read, C10); the
    dispatch comment records its line count (§ 5, § 10).
24. **The read order** (§ 2's table) is R5 § C stage B's proposal, which no
    ruling names. Settles: the dispatch comment, which may move it. **Settled**
    at dispatch: the dispatch comment names the read order; § 2's table stands
    unless it moves a row.
25. **`docs/rasteratops/p0-sweep-hits.txt`** (2,419 lines, R1 § 2's list): R3
    C17 classes it a ledger and `NAMING.md:30` names it the baseline
    classification (R2 § 0), while ruling (a) does not list it, so it sits in
    the edit scope under `NAMING.md`'s historical clause. Settles: the
    coordinator's dispatch comment -- a ledger row, or an edit-scope row
    expected to read `none`. **Settled** by the coordinator at version 2: a
    ledger row -- a generated classification baseline (`NAMING.md:30`), 2,419
    lines, its 20 `maxengel/rocknix` lines the sweep's hits as it found them;
    read-only, findings to the coordinator (§ 1 (a), § 5's `CARVE`, § 7).

**Where the research files disagree, and how this brief takes each** (the
proof confirmed 1, 5, 6, 8, 9, 10, 12, 13, 14, 16 and 17 as this brief takes
them, K115, and settled 2, 3, 4, 7, 11 and 15, K116 and K117, each noted
below):

1. **The line figures are several measures, not one disagreement** (ruling
   (h)). R1 C16: the inventory's `38598`; over the 223 text rows at the P1
   hash `grep -c` `38675` and `wc -l` `38674`; at the inventory head `38598`.
   R5 C10: `46327` at `eb4763e3cc` and `46404` at `2174265e9c`, newline counts
   over all 254 binaries included, with
   `NUL-files 31 mismatch 34 sum-inv 1334 sum-nl 9140` (R5 C11); R1 C05's
   superseded first version, `46374` by `wc -l` and `98785` by `grep -c`, also
   counted the binaries. At `e3fb3dfe00`: `34296` over the 215 text rows
   present (R2 C24; R3 C20) and `42026` over the 246 present (R5 C10). **This
   brief states the inventory's 38,598 and the text rows' 38,675 (with
   `wc -l`'s 38,674) and names the 31 binaries uncounted**; the counts with
   binaries are not used.
2. **Ruling (a)'s *"the 239 non-upstream-carried paths"*** against R1 C16:
   `REFERENCE 239 paths 29057 lines` counts the 90 upstream-carried among its
   239, and the non-upstream-carried are `fork-own 164` (R1 C16's tier line).
   **This brief writes the ruling's rule** -- the reference documents proper
   are the 254 less the 90 upstream-carried and less the ledger rows -- **and
   leaves the count to the `CARVE` lines** (open mark 1). **Settled** (proof
   K116): `REFERENCE 239` is the 254 less R1's `LEDGER 15` and holds the 90;
   the reference documents proper are the `edit-scope` and `edit-under-naming`
   lines of the `CARVE` (68 and 1 at version 2, `v2 read`).
3. **`licenses/AETHERSX2.pdf`'s direction.** R3 § 2.5 calls it *"the fork's
   addition"* and R4 § 0 *"one added file ... (`Bin 0 -> 1005740 bytes`)"*,
   both reading a diff from `upstream/next` to the fork; R1 C11 and C12 show
   it byte-identical at the merge base and absent upstream, and R2 L-02 names
   upstream's deletion `c4d353449e` 2026-10-18. **This brief takes R1's and
   R2's: upstream deleted a file the fork still carries** (L-44). **Settled**
   (proof K37): `c4d353449e` deleted the PDF upstream; the fork has not taken
   the deletion.
4. **Dead backticked paths, three extractors.** R2 C10
   `MISSING-BACKTICK-PATHS 88`; R3 C17 `path-dead=40` (30 distinct) in its
   reference class and `path-dead=87` in its total; R5 C22 `DEAD-PATHS 145` at
   the P1 tree, line suffixes unstripped (R5 § B item 21). The populations,
   the trees and the stripping differ. **This brief takes R3's classed list
   for the leads (its four candidates) and `t39-checks.sh`'s `paths` step for
   the baseline the lane records.** The three agree on dead relative links:
   `0` (R2 C10, R3 C17, R5 C22). **Settled** (proof K102, X02): the probe's
   own lines are the baseline; three of the four candidates are ruled external.
5. **The membership's inputs**: R3 C10 read `inventory.json` and `slices.json`
   at `00ca350666`, a lane-branch commit; R1, R2 and R5 at `2174265e9c`. Both
   print the same 254 and 38,598. **This brief follows ruling (g)**: the
   worktree's files, their sha256 prefixes checked against R1 C05's.
6. **`docs/council-*.md`: ten or nine.** R5 § B item 13 says ten; R1 C17
   (`council-*` 9 paths), R2 § 0 (9 files) and R4 C2 (`council docs: 9`) say
   nine. **This brief takes nine.**
7. **The identity counts**: R2 C8 over the 215 text files at `e3fb3dfe00`
   (`Rasteratops 27`, `rasteratops 27`, `RASTERATOPS 4`, `ROCKNIX 5238`, ...),
   R3 C18 by its classes in lines and files, R5 C22 at the P1 tree
   (`Rasteratops hits 61 files 27`, its case rule unread) -- different
   populations, trees and case rules. `maxengel` is `28` in R2 C8 and in R5
   C22 (`28 in 6`). **This brief quotes each with its population and has the
   lane print its own** (open mark 20). **Settled** (proof K103, K104): R2 C8
   counts occurrences.
8. **What is a ledger.** R1 C16 classes 15 (L1 the 12 under `docs/reviews/`,
   L2 `vm-qa-log.md`, `cloud-sync-changelog.md`, `catalog.md`); R2 § 0's kinds
   put the queue-reconciliation packet beside `docs/reviews/`, the VM log and
   the catalog, and the changelog among the references; R3 C17's `ledger 13`
   adds `p0-sweep-hits.txt` and the queue packet, with the catalog
   `generated`; R5 § 0 adds `map.txt` and `rc-accept.txt` as tool inputs.
   **Ruling (a) decides**: the twelve, the catalog, `map.txt`,
   `rc-accept.txt`, the two running logs, `plans/` and the 31 binaries;
   `docs/upstream/` is read-only by ruling (n); `p0-sweep-hits.txt` was open
   mark 25, **settled** at version 2 as a ledger row.
9. **What is a reference document.** R2 § 0's `49` reference documents proper
   (13,372 lines), R1 C16's `R-fork-reference 108 paths 17443 lines` and R3
   C17's `reference 81` are three classifications of different kinds. **This
   brief uses ruling (a)'s carve** and lets the `CARVE` lines count it.
10. **The briefs the selector would reach**: R1 C07's `82 paths 45125 lines`
    added at `e3fb3dfe00` and R2 C24's `83` briefs, `45512` lines, are the
    same set with and without `p1-survey.md`, a member. Not a disagreement.
11. **`docs/cloud-saves-native-wizard`**: a candidate dead path in this tree
    for R3 (C17), another repository's path for R2 (L-18). **L-13 takes
    both**: absent here, its existence there open (open mark 9). **Settled** for
    R2 (X02): a branch of the site checkout, an `external` entry.
12. **What R4 left open and R1 settles**: whether another `docs/reviews/**`
    path is among the 254 (R4 § 0) -- twelve are (R1 C06); and #686's *"190
    lines read"* (R4 § 0) -- the two `CODE` rows, `generate.py` and
    `wordmark.css` (R1 C16).
13. **`tools/es-menu-map-check`'s exit code**: R2 C16 printed `tail`'s status,
    not the checker's; R3 C13 printed `rc 0`. **This brief takes R3's.**
14. **The catalog, current and stale at once**: R3 C13's
    `release-catalog: current (99 cuts)` and R2 L-03's newest row of
    2026-10-02 are both true -- the check compares the page with the
    `RECORD.txt` files present, and #964 counts kept folders without one (R4
    item 39). Not a disagreement; L-15 carries both.
15. **Rulings (a) and (l) on the `maxengel/rocknix` links**: ruling (l) asks
    for the fix where the fork's own repository is meant, and the only four
    instances R2 and R3 found sit in `docs/cloud-sync-changelog.md`, a ledger
    row under ruling (a). **This brief applies (a) to the changelog and (l) to
    any instance the identity step finds in the edit scope** (L-23; none in R3
    C18's reference class). **Settled** (proof K64): the links sit in the
    changelog alone.
16. **`README.md`'s release sentence**: `:9-10` for R2 (L-14), `:7-10` for R4
    (item 16). The same sentence; L-02's grep settles the line.
17. **The binaries**: R1 C19's `31` by the inventory's `lines` `None` and R5
    C11's `NUL-files 31` by content agree on the count by two methods.

**Checks on this file, version 1** (run from the coordinator's worktree on the
file as written to the kit, each command's own line):

- `/usr/bin/grep -c ''` prints `2111`.
- The leads, in § 3's row shape
  (`/usr/bin/grep -c -E '^\| (\*\*)?L-[0-9]+(\*\*)? \|'`): `46` rows
  and `46` distinct IDs.
- § 7's checkboxes (`/usr/bin/grep -c '^- \[ \]'`): `27`;
  `tools/box-check`'s own predicate, its `PERSON`, `DEVICE` and `FACT`
  patterns read from its source at `HEAD` and applied as it applies them, over
  § 7's lines here (the tracker is not read): `boxes 27 fail 0`, after a planted two-checkbox file printed `boxes 2 fail 1`.
- The open marks outside this section
  (`sed '/^## Version 1: what the drafting/,$d'` then `/usr/bin/grep -o` of
  the mark, counted by `/usr/bin/grep -c ''`): `37` occurrences on `36` lines
  (proof C12: `[unverified] lines 36 occurrences 37`), the header's and § 5's
  two sentences explaining the mark among them; the open items listed
  above (`/usr/bin/grep -c -E '^[0-9]+\. \*\*'` between this section's heading
  and its second bold paragraph): `25`.
- Unfilled placeholders (`/usr/bin/grep -c -E '__[A-Z0-9_]+__'`):
  `0`.
- The hooks' credential regex, built as `.githooks/guard-lib` builds it --
  `SECRET_PATTERNS=''`, then `.githooks/secret-patterns` sourced from
  `git show HEAD:` into a scratch file, then `grep -E -e "$SECRET_PATTERNS"`,
  never `-f` -- `compile rc=1, the runtime-built positive matched 1, the file matched 0`.
- `tools/forbidden-terms-check --stdin < <this file>` from the coordinator's
  worktree: `rc=0 (forbidden-terms-check: 0 hits on stdin), the planted positive through FORBIDDEN_PATTERNS rc=1 (forbidden-terms-check: 1 line(s) on stdin carry a listed word)`.
- § 2's two blocks, extracted from between their markers: `block.sh 130 lines, sha256 e81453b6732cdea8; split.sh 46 lines, sha256 afb1909c5cdc6c88`,
  byte-identical to R1's; `bash -n` over the file's `bash` blocks:
  `4 blocks, rc 0 0 0 0`.

Version 1, 2026-11-01 03:48:37 UTC, written from the five research files for the
coordinator's dispatch; the stranger's proof of it makes version 2

## Version 2: corrections from the proof

The stranger's proof of version 1 (`/workspace/tmp/m6-coordinator/kit/t39-proof.md`,
in no tree, 443 lines) read the brief at `a0fb117b8b` by hash and closed on
its own totals line `checks 125; PASS 107; MISMATCH 13; SETTLED 3; NOTE 2;
corrections 12` (its C16; `K ids distinct 125, X ids distinct 12`). Each
correction is applied in the body at the line the proof names, under the
coordinator's rulings (D-WORKFLOW-189): the line is version 1's at
`a0fb117b8b`, the words are the old and the new, and the command is the
proof's.

| X | Version 1 line(s) | Old words | New words | The proof's command |
| --- | --- | --- | --- | --- |
| **X01** | `:649`, `:728-729`, `:1206`, `:1209`, `:1497` | *"Expected with the defaults (`bash .qa-scratch/t39/split.sh`, R1 C16)"*; the two stage-A `split.sh` runs under `export LC_ALL=C` | the expected lines are `en_US.UTF-8`'s: both stage-A `split.sh` runs are prefixed `LC_ALL=en_US.UTF-8` (the ruling names `:1206`; the dispatch-tip run at `:1209` follows so the `diff` after them compares like with like), `export LC_ALL=C` stays for the greps and counts, § 2 says in one sentence why (`split.sh`'s `sort` under `C` puts the three upper-case `P1 grep -c group R` lines first), and § 7's criterion names the locale; `block.sh` unchanged (equal under both, K04) | C2: `split.sh` with the defaults under `LC_ALL=C`, its `diff` against `:653-704` printing `29a30,32`, `38d40`, `41,42d42`; C3: `LANG=en_US.UTF-8`, `SPLIT(defaults, default locale) = expected` (K06, K121); `v2 read`: the same diff and the same equality |
| **X02** | `:960`, `:994`, `:995`, `:1000`, `:1067`, `:1369-1370`, `:1747` | *"R3's four real dead paths"*; L-14 *"a generator tool that is not in the tree"*, disposition **fix**; L-19 *"an absent tool in a historical artifact's README"*; Q6 *"the four dead backticked paths"*; *"the four candidates of L-13, L-14, L-19 and L-20 FAIL until fixed or ruled"* | one real absent in-tree path (`packages/rocknix`, L-20) and three names ruled external: L-14 and L-19 are `allow-legit` `external` entries (the splash repositories' wordmark tools, named on their own lines as another repository's), L-14's disposition **record** (a § Coverage `none`: the README already says where the tool lives), L-13's `docs/cloud-saves-native-wizard` `external` (a branch of the site checkout); disagreement 11 settles for R2; the `paths` step's baseline is the external classes plus the one real candidate | C7, C8: `docs/pixelelated/art/README.md:20-21` (*"generated by `pixelelated/splash` `tools/pixelelated-wordmark`"*), `docs/rasteratops/art/README.md:8` (*"by `rasteratops/splash`'s `tools/rasteratops-wordmark`"*), `docs/pixelelated/site-plan.md:69-70` and the appendix `:3` (K55, K56) |
| **X03** | `:1019`, `:1244`, `:1293`, `:1504` | L-38 *"none at the tip by R3 C23"*; `cites` *"expect no unresolved line"*; the `713 IDs` comment *"the dispatch's own row moves the count"*; § 7 *"the decision IDs with no `UNRESOLVED` line"* | D-WORKFLOW-188 named in all four: the 223 at P1 cite it (`docs/reviews/p1-tracking.md:56`, `:500`) and its row lives on P1's branch alone; ruling (p)'s merge of `feature/m6-p1-survey-641` (`2174265e9c`) into the coordinator's branch before dispatch carries the row into the register, the coordinator runs `tools/register-check` after the merge and records it, so at the dispatch tip the `cites` step expects no line; an `UNRESOLVED D-WORKFLOW-188` at dispatch is the coordinator's finding, never the lane's | C8: `D-IDs named (distinct) 438 occurrences 1280 unresolved ['D-WORKFLOW-188']`; C10: the two citing lines; C12: `P1 register rows D-WORKFLOW-188: 1; a0fb rows: 0` (K79, K122) |
| **X04** | `:1500` | ``/usr/bin/grep -o -E 'L-[0-9]{2}' 02-forward-audit.md`` prints `46` | ``/usr/bin/grep -o -w -E 'L-[0-9]{2}'`` (without `-w` the `711` of L-08's `MAP-TAIL-711-END` reads as a lead id) | C12, C13: `L-NN distinct anywhere 47` on the brief (K120) |
| **X05** | `:875` | `es-ui-style-guide.md:21` (the checker sentence), `:59` (the entrypoint) | `es-ui-style-guide.md:59` and `:66` | C6, C10: `:21` the companion line, `:59` *"`es-menu-map-check` detects missing screen titles, not stale copy or screenshot"*, `:66` *"The menu map's visual-evidence section is the entrypoint."* (K96) |
| **X06** | `:1043`, `:1596` | `README.md:20` | `README.md:21` (`:20` is blank) | C7, C8: `21:The next candidate uses the lowercase pixelelated wordmark in Tiny5 Duo LCD.` (K33) |
| **X07** | `:1598` | D-WORKFLOW-157 to -160 at `:670`, `:672`, `:674`, `:676` | `:670`, `:672`, `:676` (D-WORKFLOW-159), `:674` (D-WORKFLOW-160) | C5: `D-WORKFLOW-159 676 676; D-WORKFLOW-160 674 674` (K92) |
| **X08** | `:1012` | *"fork-own from `a19831ebf6` 2026-08-21, never updated"* | *"added by `a6b28a469f` and last changed by `a19831ebf6`, both 2026-08-21, not updated since"* | C3, C4: `--diff-filter=A` prints `a6b28a469f 2026-08-21 GENERIC_X64 - syslinux: install ldlinux.c32 (BIOS boot for syslinux 6.x)`; `a19831ebf6` changed it (`4 ++--`); 2 commits (K36); `v2 read`: `git log --format='%h %cs' 2174265e9c -- <the file>` prints 2 lines |
| **X09** | `:149` | *"143 of the 254 have one commit in their whole history"* | *"144 of the 254 have one commit in their whole history (`one-commit paths: 144`, every commit at the P1 tip, ...)"*, the loop named in place; R1 C09's non-merge rule, over the commits reachable from `e3fb3dfe00`, prints 145 one-commit and 8 zero-commit paths | C3: `one-commit paths: 144`; C13: `non-merge one-commit paths at 2174265e9c: 144`; C12: `one-commit 145; zero 8` (K25); `v2 read`: the named loop prints `one-commit paths: 144` |
| **X10** | `:1017` | *"two say "Two more documents" load nowhere"* | *"`CLAUDE.md:34` says "Two more documents" and `AGENTS.md:31` "Two documents" load nowhere"* | C6, C10: `CLAUDE.md:34` *"Two more documents carry interface law and load *nowhere*"*; `AGENTS.md:31` *"Two documents carry interface law and are loaded by no rule"* (K76) |
| **X11** | `:985` | `docs/pixelelated/cloud-folder-flow-review.md:272` listed among the other reference-class hits as *"(consistent with the retirement)"* | a hit of R3's looser heuristic (*folder migration*), consistent with the retirement, not of L-04's check words | C7, C8: `cloud_migrate_layout at:` prints nothing for the file; `:272` reads *"... return to the caller without scheduling a folder migration."* (K46) |
| **X12** | `:1004`, `:1559` (and `:1027`, L-46's same short form) | `image-completeness/fix.patch:64` | `docs/upstream/raofflineproxy/image-completeness/fix.patch:64` | C7, C8: `docs/upstream/image-completeness/fix.patch` does not exist; the file is under `raofflineproxy/`, its `:64` *"+    F-RA-12). Written for ROCKNIX (fork maxengel/rocknix#213)."* (K65) |

Beside the twelve, **the register moved under the brief**: D-WORKFLOW-219,
which version 1 reserved for this slice's ownership row, is T38's stage-D
pause dispositions row (#685, #1394; written 2026-11-01), so every
`D-WORKFLOW-219` that meant T39's row -- `:65`, `:1611-1614`, the draft row at
`:1622`, the pointer's `Register:` key at `:1804` -- now reads
**D-WORKFLOW-220**, and the places that list the highest decided IDs (§ 9, the
pointer's `Register:` key, the register-check comment of § 5) name
D-WORKFLOW-219 as T38's dispositions row. `v2 read` at the coordinator's tip
`b344408e46`:
`awk '/^## Open decisions/{exit} /^\| D-[A-Z]+-[0-9]+ /{print $2}' docs/decision-register.md | awk -F- '{n=$3+0; if(n>m[$2]) m[$2]=n} END{for(a in m) printf "D-%s-%03d\n", a, m[a]}' | sort`
prints `D-CLOUD-193`, `D-INFRA-031`, `D-LAUNCH-007`, `D-NET-017`, `D-QA-063`,
`D-RA-052`, `D-SYS-013`, `D-UI-137`, **`D-WORKFLOW-219`**, one per line; the
register there is 798 lines, the row at `:779`, `## Open decisions` at `:781`.
Two NOTEs of the proof for the coordinator at dispatch, not corrections: K39,
`docs/reviews/README.md:10` differs between P1 (*"any reading-order
prerequisite (the renovation gates no release, D-WORKFLOW-187)"*) and the
coordinator's branch (*"the release it gates"*), so ruling (p)'s merge meets
two versions of that row; and K19, the `rest` selector reaches `329` paths at
`a0fb117b8b` (`83` briefs added), so the dispatch tip's split prints at least
83.

**The coordinator's two rulings on the open items that were theirs:**

- **Open item 21, the art bytes** (ruling (o) in § 1; § 5's art paragraph and
  runs block; `t39-checks.sh`'s `binaries` step; § 6's `02` row; § 7's
  binaries criterion; § 9's row draft): the ruling is widened -- the 31
  binaries **and** the 18 art text files (`docs/pixelelated/art/**`'s SVG,
  JSON, CSS, `generate.py` and the two `Tiny5-OFL.txt`, and
  `docs/rasteratops/art/*.svg`; the stage-A `CARVE art-bytes 18` class, proof
  K26 and `v2 read`) are tabled by name, size and sha256 and never edited by
  T39; the two art READMEs are that area's reference documents; a finding in
  an art source is routed to the splash repository (external), a licence
  text's to #528. The runs block tables the 18 beside the 31 (its `awk` over
  the block's TSV prints `18`, `v2 read`), the `binaries` step covers both, and
  `02` gains § Art bytes with 18 rows.
- **Open item 25, `docs/rasteratops/p0-sweep-hits.txt`** (ruling (a)'s ledger
  list; § 2's groups table; § 5's `CARVE` and removal check; § 7's ledger
  criterion; § 9's row draft; L-23): moved from the edit scope to the ledger
  class -- a generated classification baseline (`NAMING.md:30` names it so),
  2,419 lines, whose 20 `maxengel/rocknix` lines are the sweep's hits as it
  found them, not references to correct; tabled as a ledger, read-only,
  findings to the coordinator. The carve's `NAMED` set gains the path and the
  class sizes were re-derived by the command, never adjusted by hand (`v2
  read` at `2174265e9c`, from the block's `block-2.txt`): `CARVE art-bytes 18`,
  `edit-scope 68`, `edit-under-naming 1`, `ledger-binary 31`, `ledger-named 6`,
  `ledger-plan 1`, `ledger-reviews 12`, `read-only-528 1`, `read-only-585 27`,
  `read-only-upstream 88`, `tabled-generic-x64 1`, `CARVE total 254` --
  version 1's lines, the proof's K26, read `edit-scope 69` and `ledger-named 5`.
  `v2 read`: `git -C "$W" show 2174265e9c:docs/rasteratops/p0-sweep-hits.txt | /usr/bin/grep -c ''`
  prints `2419` and `| /usr/bin/grep -c 'maxengel/rocknix'` prints `20`.

**The 25 open items of version 1, their state after the proof and the
rulings** (each is also annotated in place in the Version 1 section; the
proof's partial settlements -- items 7, 11, 18, 23 -- are in the state column):

| # | Item | State |
| ---: | --- | --- |
| 1 | ruling (a)'s class sizes | **Settled**: K26's `CARVE` lines (`CARVE total 254`); re-derived for version 2 with `p0-sweep-hits.txt` in the ledger (§ 1 (a), § 5) |
| 2 | which of the 254 claim a guest behaviour | **Open**: the lane's stage B (§ 5 keeps its mark) |
| 3 | the dispatch tip's split lines | **Open**: the lane's stage A, under `LC_ALL=en_US.UTF-8` (X01); at `a0fb117b8b` `8 absent`, `3 changed`, `1 same`, `329` reached, `83` added (K11, K19) |
| 4 | the worktree's `renovation-inventory` | **Open**: the lane's stage A; the clone run reproduced R1 C02 with the status unchanged (K20) |
| 5 | `box-check`, `ceremony-check`, `hooks-test` | **Open**: the lane's stage A; `box-check`'s predicate over § 7 printed `brief s7 boxes 27 fail 0` (K118) |
| 6 | the lint's Local proof | **Settled**: K111's three lines, now § 5's `# STAGE A` expectations |
| 7 | L-04 | **Settled** for D-CLOUD-175 (`0` and `0`, K45); the ten join/follow lines stay open, the lane's stage B |
| 8 | L-12 | **Settled**: `0` (K54) |
| 9 | L-13 | **Open** (outside the tree): the lane's stage B reads a local checkout where one is present, never a fetch; the name itself is `external` (X02) |
| 10 | L-16 | **Settled**: `0`, so **fix** (K58) |
| 11 | L-17 | **Settled in part**: the IA is at rev 6, past #23's rev 5 (K59); the text against the four rows is the lane's stage B |
| 12 | L-23 | **Settled**: the changelog alone (K64) |
| 13 | L-24 | **Open**: the lane's stage B (`tools/archaeology --no-gh 'KEEP CLOUD'`) |
| 14 | L-26 | **Settled**: `9` (K68) |
| 15 | L-38 | **Settled** with a finding: X03 |
| 16 | L-39 | **Settled**: nothing printed, so **inherited:#1013** (K80) |
| 17 | L-45 | **Settled**: equal to #359's two (K85) |
| 18 | L-37 | **Settled in part**: the sentence present and `errat` 0 (K78); the erratum is written at dispatch and read back at stage A |
| 19 | the export's count at the dispatch tip | **Open**: the lane's stage A; at P1 `of the 254 absent: 0` (C11) |
| 20 | R2 C8 lines or occurrences | **Settled**: occurrences (K104); the lane's loop prints lines and files beside them |
| 21 | the art bytes as a ruling | **Settled**: ruling (o) widened to the 18 art text files (above) |
| 22 | T39's merge order | **Settled** at dispatch, as § 8 says: ruling (p)'s order before dispatch, the coordinator's at acceptance after |
| 23 | the host file's path | **Settled**: `/workspace/tmp/m7-m6-host-coordination.txt` (T38's brief `:1106`, `:1674`; 710 lines at C10's read); the dispatch comment names it and records its line count |
| 24 | the read order | **Settled** at dispatch: the dispatch comment names it; § 2's table stands unless it moves a row |
| 25 | `docs/rasteratops/p0-sweep-hits.txt` | **Settled**: a ledger row (above) |

By `/usr/bin/grep -c` over the rows above: `18` begin **Settled**
(two of them, 11 and 18, in part; 7 for its first half), `7` begin
**Open**. The disagreements' states are annotated in the Version 1 section:
the proof confirmed 1, 5, 6, 8, 9, 10, 12, 13, 14, 16 and 17 as this brief
takes them (K115) and settled 2, 3, 4, 7, 11 and 15 (K116, K117).

**Not checked by the proof, kept as the research printed them and not
marked** (its own list): L-07's labels and `CHANGE CLOUD FOLDER` at the pin
`16dbac5211` (no EmulationStation checkout among its sources); L-13's seven
pages in `ROCKNIX/rocknix.org`; L-24's deciding row (`tools/archaeology`);
L-18's `R/O/D/W` inbound columns and `files=17` (the 17's line sum `2135`
reproduces, K60; the proof's own pattern caught an eighteenth candidate,
`save-history-consensus-amendment.md`, 116 lines -- the generator's inbound
columns decide); `tools/box-check`, `tools/ceremony-check`,
`.githooks/hooks-test` and `tools/prose-check --self-test` as runs; every
dispatch-tip expectation; L-09's 2026-10-16 transfer to `077197`; L-33's
`b5aad48cbe` on `remotes/legacy/m7-audit-integration-603`; T38's session name
`m6-t5-build-engine`; T4's PL-24 row past 165 characters; R5's newline counts
`46327` and `46404`; R3 C17's own `40` (`30` distinct) and R3 C18's class
counts; the guest-behaviour sentences (open item 2).

**Checks on this file, version 2**, each the command's own output, run from
the coordinator's worktree on the file as written (`LC_ALL=C`, counts by
`/usr/bin/grep`):

- `/usr/bin/grep -c ''` prints `2389`.
- The leads, in § 3's row shape (`/usr/bin/grep -c -E '^\| (\*\*)?L-[0-9]+(\*\*)? \|'`): `46` rows; `/usr/bin/grep -o -w -E 'L-[0-9]{2}' | sort -u | /usr/bin/grep -c ''`: `46` distinct IDs (without `-w`: `47`, X04's own case, the `711` of `MAP-TAIL-711-END`).
- § 7's checkboxes (`awk '/^## 7\. /{p=1;next} /^## /{p=0} p' | /usr/bin/grep -c '^- \[ \]'`): `27`; `tools/box-check`'s own predicate, its `PERSON`, `DEVICE`, `FACT` and `BOX` patterns read from its source at `b344408e46` (`:44-47`) and applied as its `:92-93` apply them over § 7's lines here (the tracker is not read): `boxes 27 fail 0`, after a planted two-checkbox list printed `boxes 2 fail 1`.
- The open marks (`/usr/bin/grep -c '\[unverified\]'`): `19` lines on this file, `18` of them outside the Version 1 section (version 1 had `36` lines, `37` occurrences): the two sentences that define the mark (the header, § 5 rule 3), the two *"or marked"* sentences (§ 5's `# STAGE A` intro and the runs' closing paragraph), and the open items' own marks -- ruling (q)'s guest sentence, § 2's dispatch-tip lines and the tool's row, § 3 item 5's three unrun checks, L-04's ten join/follow lines, L-13's pages, L-17's text, L-24's deciding row, § 5's guest claims, the split's `tip:` lines, `ceremony-check`, the export's count, `hooks-test` and `box-check`; inside the Version 1 section the one occurrence is the proof's quoted count line.
- Unfilled placeholders (`/usr/bin/grep -c -E '__[A-Z0-9_]+__'`): `0`.
- `D-WORKFLOW-220` on `7` lines (§ 1's header paragraph, § 5's register-check comment, § 9's text and row draft, the pointer's `Register:` key); `D-WORKFLOW-219` on `13` lines, each naming T38's dispositions row or the register's state, none this slice's.
- § 2's two blocks, extracted from between their markers: `block.sh` 130 lines, sha256 prefix `e81453b6732cdea8`; `split.sh` 46 lines, `afb1909c5cdc6c88` -- byte-identical to version 1's and R1's; the three expected blocks byte-identical to version 1's (sha256 prefixes of the marked segments `9fdc39dffd7e429e`, `fd5c6b775ab8209d`, `a3956e5a2a2216d3`); `bash -n` over the file's `4` `bash` blocks: rc `0` each.
- The `CARVE` python extracted from § 5's `# STAGE A` block and run in scratch against the block's `block-2.txt` prints the twelve expected lines written beside it, `CARVE total 254` last; `split.sh` extracted from § 2 and run with the defaults prints § 2's expected block under `LC_ALL=en_US.UTF-8` (`diff` empty) and three moved lines under `LC_ALL=C` (`29a30,32`, `38d40`, `41,42d42`); `block.sh` prints the same under both.
- The hooks' credential regex, built as `.githooks/guard-lib` builds it -- `SECRET_PATTERNS=''`, then `.githooks/secret-patterns` sourced from `git show HEAD:` into a scratch file, then `grep -E -e "$SECRET_PATTERNS"`, never `-f`, never `guard_load` -- compile rc `1`, a private-key header line assembled at run time matched `1`, the file matched `0`.
- `tools/forbidden-terms-check --stdin < <this file>` from the coordinator's worktree: `forbidden-terms-check: 0 hits on stdin`, rc `0`; the planted positive through `FORBIDDEN_PATTERNS`: `forbidden-terms-check: 1 line(s) on stdin carry a listed word`, rc `1` (the list itself never read).
- `tools/register-check` from the coordinator's worktree: rc `0`, its line `register-check: 714 IDs, each once; every citation in the live documents names a row`.

Version 2, 2026-11-01 04:48:47 UTC, after the stranger's proof of version 1
