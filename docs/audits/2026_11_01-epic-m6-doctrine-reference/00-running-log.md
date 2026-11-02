# T39 (#686) running log -- doctrine: the reference documents

**Executor:** session `m6-t1-os-launch` (ruling (f); freed from T36 #683). Model: the dispatch's and the pointer's label is "Opus 5.5 at high effort"; the session's own harness metadata reports the model id `claude-opus-4-8`. **L-38 settled by the coordinator on #686 (06:43 UTC):** `second-opinions/review-plan.json` records `primary.model` = `claude-opus-4-8` (the harness-reported id) with both the label and the id in `identity_source`, as T36 did. Written at stage C.
**Depth:** Local (a table; D-WORKFLOW-184). One worktree, no EmulationStation worktree, no guest, no compile.
**reviewed-at:** `86ebb6dffc` (the dispatch tip = the coordinator's branch merged into the lane's, `MERGE_HASH`), stacked on P1 `2174265e9c`, the coordinator's tip `86ebb6dffc` beside it (`COHASH` = `MERGE_HASH` here). Brief `89fd4e2610` (`V2HASH`, version 2, 2389 lines, sha256 `f2194b5326acdb57`).

## 2026-11-01 06:24-06:27 UTC -- stage A

Read order: the pointer's eleven keys first, then § 5's `# STAGE A` block whole and in order. `LC_ALL=C` throughout; counts by `/usr/bin/grep`; the split blocks run under `en_US.UTF-8` (X01). `df -i /workspace`: 28% inodes used.

### The pointer's eleven keys
All eleven are T39's; none names the predecessor T38 as a key (T38 appears only as correct context -- its branch `feature/m6-doctrine-skills-685` read by hash, its L-51). Branch `feature/m6-doctrine-reference-686`; session `m6-t1-os-launch`; brief `doctrine-reference.md`; ownership row `D-WORKFLOW-220` (not T38's -218/-219). The four hash words filled and the `Register:` line full: `grep -c -E '__[A-Z0-9_]+__'` = 0, `grep -c -w -E 'CO|MERGE_|TIP|V2 HASH'` = 0.

### The lint's Local proof (ruling (q)) -- before anything else
- T4's tip `6ec78bbf8cc2dc07...`; folder `docs/audits/2026_10_24-epic-m6-doctrine-rules`.
- T4's plan: `t4 plan: local D-WORKFLOW-184 0` (depth local, tier_exception, 0 reviewers).
- **`lint, a Local plan, rc=0`** (ends `PASS`) -- the Local-plan shape lints clean.
- **`lint, tier_exception removed, rc=1`** -- `FAIL  second-opinions/review-plan.json or its call evidence is invalid: local-only cannot satisfy Epic/Milestone`; `1 CONTRACT FAILURE(S)`. The PASS's FAIL-first (§ 5 rule 4).

### L-01's loop (ruling (p))
The fifteen-name loop (`README.md`, `areas.json`, `assessment.md`, `briefs/p1-survey.md`, `build-path-read.md`, `cross-reference.md`, `inventory.md`, `order.md`, `p1-tracking.md`, `plan-for-the-plan.md`, `slices.json`, `status.md`, `tools/renovation-{inventory,status,drift}`) printed **no `MISSING` line** -- the renovation's files and tools resolve at the dispatch tip because the branch is stacked on P1.

### The host file (protocol only; this slice writes no line there)
`/workspace/tmp/m7-m6-host-coordination.txt` read once, whole, 06:27:08Z: **712 lines**, **0 lines matching `T39|#686`** (criterion 24's baseline; the dispatch comment named this line count). The tail is T36 (#683)'s acceptance compile START/END pairs (03:50-05:19 UTC). No guest window and no compile are this slice's.

### #686 and #807
- #686: `M6.P2 E807/T39: doctrine: the reference documents`, OPEN, body 87 lines (27 before the coordinator's fill, R5 C16).
- #807 (ruling (i), L-37): `:15` reads *"its paths have no upstream (ROCKNIX carries none of them)"*. **L-37 settled by the coordinator on #686 (06:43 UTC): the ruling-(i) erratum IS present**, appended to the same long line 15 (*"(Erratum, 2026-11-01, at T39's dispatch: untrue of T39's 90 upstream-carried documents under ...)"*). My stage-A flag was a false alarm: `grep errat` was case-sensitive (the text is `Erratum`) and `cut -c1-160` truncated line 15 before the appended erratum. Corrected here (verify the artifact, not my own grep's report). No post on #807 (never list).

See `01-research-notes.md` § Scope for the membership blocks, the carve, the tip lines and the issue states.

## 2026-11-01 06:58 UTC -- stage B (the reader's pass and the leads)

Read the 254 in § 2's order (the reader's pass is `01` § The reader's pass,
group by group) and ran every lead's FAIL-first check at the lane's tip
`f60c2c08bf`. The leads are `02` § The table (46 rows); the probes are `02`
§ The identity words / § The retired names / § The runs; `02` § Coverage is
generated at stage C by `tools/t39-tables.py` from the inputs gathered here.
`LC_ALL=C` throughout; counts by `/usr/bin/grep`.

PROOF: 06:58 UTC the membership exports 254 files at the tip (`git archive HEAD`); proved: tree
PROOF: 06:58 UTC the carve classifier on `block-2.txt` prints edit-scope 68, edit-under-naming 1, total 254 (the v2 figures, brief `:1297`); proved: tool-run
PROOF: 06:58 UTC 0 dead relative Markdown links over 511 scanned, resolved against the worktree; proved: tree
PROOF: 06:58 UTC decision IDs: register 716, cited distinct 442, 0 unresolved (L-38; D-WORKFLOW-188 carried by the P1 merge); proved: tool-run
PROOF: 06:58 UTC Pixelelated/PIXELELATED capitalised 0 (D-WORKFLOW-144 holds); proved: tree
PROOF: 06:58 UTC each of the 46 leads prints its defect at the tip (see `02` § The table); proved: tree/tool-run/record
PROOF: 06:58 UTC the 31 binaries and 18 art text files carry their recorded sha256 at the tip (ruling (o)); proved: tree
PROOF: 06:58 UTC none of the 254 is modified; the removal check vs `86ebb6dffc` is empty (rulings (a),(k),(n),(o)); proved: tree

A first-scoping note was corrected the moment it was found (verify the artifact,
not my own probe's report): a dead-link scan resolved against the 254-only
export read 417 dead; resolved against the full worktree it reads 0, which is
the research's figure -- the 254 reference other paths of the tree that are not
themselves in the slice. And the brief's R3 C24 `cloud_migrate_layout`
product-tree figure includes `tools` and reads 0, while at the tip `tools/`
carries 127 (fork-only QA tooling) and the shipped OS carries 0; L-04 stands,
the parenthetical is a coordinator-owned brief-evidence erratum (flagged on
#686, `02` § The runs).

**Stage-B census (this session's last line):** `git status --short` shows only
the audit folder (`00`, `01` modified; `02` new) -- **no fix to any of the
254 while reading**. No build, no compiler, no guest, no fetch, no council or
keyed call, no held directory opened, no `--write` of a generated file. The
read tree is exported at `/workspace/tmp/m6-t39/export/` (254 files), retired
at stage H. No line written to the host-coordination file or to #807.

## 2026-11-02 00:10-05:21 UTC -- the model switch, and the stage-B completion

**The model switch.** The stage-B acceptance was posted at 00:12 UTC (#686,
issuecomment-6565981458), with its correction at 00:12:44
(issuecomment-6565986529). Before that, the owner moved this session from Claude
Code (session `33bed370-...`, which reported `claude-opus-4-8` for stages A and B)
to the **Antigravity CLI**, conversation `1364d92f-d934-4080-ac5b-5b7ee9ff8d0a`. That
harness's model setting reads **"Claude Opus 5.5 (High)"**, read from the harness
itself at 00:10 UTC 2026-11-02. The coordinator's ruling: `primary.model` stays
`anthropic/claude-opus-4-8`, because stages A and B are the reading the review rests
on, and `identity_source` names three things:
- the dispatch's label;
- the A-B id;
- the C-onward harness reading.

Commits from now end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
The session stopped on a usage quota at about 00:25 UTC with three stage-C paths
uncommitted (`tools/`, `second-opinions/`, `stage-c/`). It resumed at 05:15 UTC on the
owner's authorization.

**The stage-B completion** (the correction's three items, one commit):
- `03-retrospective.md`: § 3.1 to § 3.4; § 3.5's five seams (the rules, the three
  ledger-reading tools, the issue-cited lines, upstream's copies); the futro's
  predictions checked.
- `04-analysis.md`: Phase 4; the 4.5 verification of every fix candidate (6 Medium
  bugs, 11 Low); Q1 to Q7, with Q4 to Q6's tables marked as `t39-tables.py`'s at
  stage C; the two maintainer questions; § Second opinion *not applicable at Local
  depth*.
- `stage-a/`: the first commands' scripts and outputs, from
  `/workspace/tmp/m6-t39/tmp/` and `.qa-scratch/t39/`.
- `stage-b/`: the reading notes, which are lists and hashes, from
  `/workspace/tmp/m6-t39/stage-b/`. **`reader-digest.txt` is kept out**: it holds the
  head of each document, so it is text of the 254. Its sha256 is in `stage-b/README.md`.
- `02` § What the coordinator and the next slices inherit takes the R3 C24 lead at its
  six paths, owner the coordinator, as the acceptance asked.

Design-intent reads for 4.5 (`git log -S` per fix candidate, at `86ebb6dffc`) are
tabled in `03` § 3.3. One new observation, recorded in `03` § 3.5: #1216 quotes
`es-menu-map.md:405` as *"FINISH RESTORE PROCESS"*, and the line reads
`### FINISH RESTORE SETUP`. That is the interface lanes' (L-32).

PROOF: 05:16 UTC each fix candidate's sentence predates, or was left untouched by, the change that made it untrue (`git log -S` per lead, `03` § 3.3); proved: history

`git status --short` for the 254 is empty (no fix at this stage). No build, no
compiler, no guest, no fetch, no council or keyed call. No line was written to the
host file.
