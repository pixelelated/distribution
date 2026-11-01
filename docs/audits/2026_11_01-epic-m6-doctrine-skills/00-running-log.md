# Epic Audit Running Log — M6.P2 T38, the skills, agents and settings

**Auditor:** Code Auditor skill (the fork's adaptation, at the dispatch tip), with the renovation face of `docs/reviews/plan-for-the-plan.md` § 4
**Primary model:** Claude Opus 5.5 (`claude-opus-5-5`, lab Anthropic) at high effort, in Claude Code. Identity sources: the coordinator's dispatch on #685 (issuecomment-6552443399, 2026-11-01T02:40:26Z) and the session's own model line
**Session:** the T5 session, herdr agent `m6-t5-build-engine` (the dispatch's name for it), Claude Code session `c649553c-8086-4db7-ad9c-248c7e41ff95`. It started in T5's worktree (`.../m6-build-engine-652`), and every command of this lane runs after `cd /workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-skills-685`. Its context was summarized once before this dispatch, at T35's close-out; nothing of T35's is carried into this slice
**Started:** 2026-11-01 02:42 UTC (`date -u` 02:42:28 at the pointer's key check)
**Scope:** slice `doctrine-skills` (#685, `M6.P2 E807/T38`), area epic #807 (the doctrine), renovation epic #339, milestone M6. The membership is the inventory's 52 paths under `.claude/**` less `.claude/rules/**`: 44 under `.claude/skills`, 8 under `.claude/agents`
**Spec:** `docs/reviews/briefs/doctrine-skills.md` version 2 at `fa4a9a5b0d` (sha256 prefix `b6d30242978fa606` of the file at that hash), with `## Errata before dispatch` appended at the dispatch, the file's only change since (`1 file changed, 10 insertions(+)`; 2,031 lines at the dispatch tip). #685's body carries § 7's 22 criteria and wins where the two differ
**Depth:** Local (plan § 6c, *a doctrine read*; D-WORKFLOW-184). No reviewer, no Facilitator call, no `tools/council/run` call, no `npm install`, no keyed call
**Branch / worktree:** `feature/m6-doctrine-skills-685` at `/workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-skills-685`, stacked on `feature/m6-p1-survey-641` at `2174265e9c`, with the coordinator's `3a9b0aec81` merged at `87c2ab0fed`. The lane's HEAD at stage A is `11fa8f95b8`, the coordinator's seeded pointer on top of the merge
**reviewed-at:** `87c2ab0fed`, the dispatch tip (the brief's merge-commit placeholder, filled); its 52 are the bytes read. Beside it are the P1 tip `2174265e9c` and `next` `8ebaf8daad`, which hold the same bytes on the 52 (12,734 lines). The coordinator's branch moved three of the 52 after the inventory: `.claude/skills/code-auditor/references/templates.md` (331 -> 348 lines), `.claude/skills/council/IMPORTED-FROM.md` (102 -> 127) and `.claude/skills/mini-retro/references/scoped-audit.md` (709 -> 716); the lines at each hash are `stage-a/stage-a-extra.out`'s
**Proof tokens:** a line of this log that records a proof begins with the proof token followed by a colon. Criterion 18 counts those lines against the `proved:` cells of `02-forward-audit.md`. Each carries an ID `A-nn` that its `02` row cites, its class, the command, the line it printed and what result would have been a FAIL (§ 5 rule 4: nobody else asks it at Local depth). This header names the token without starting a line with it

---

## Log Entries

### [Stage A] 02:40-02:43 — the dispatch, the brief, the pointer's eleven keys

- The dispatch comment (6552443399, 02:40:26Z) was read first, then the brief whole at the dispatch tip: version 2's 2,021 lines and the errata's 10.
- **The pointer's eleven keys, against § 10's table (`date -u` 02:42:28):**
  - Each key appears once: `Branch (distribution):`, `Worktree (distribution):`, `Worktree (EmulationStation):`, `Executor:`, `Epic:`, `Depth:`, `The lens:`, `The rule:`, `The host:`, `Register:`, `The brief:`.
  - Each reads § 10's *Must read* value, and no key line carries a T37 value: `0` matches over the eleven key lines of `feature/m6-es-recipe-684`, `m6-es-recipe-684`, `m6-t3-emulators`, `#700`, `packages/ui`, `15 + 5`, `qa-integration`, `es-recipe.md`, `pkgcheck`, `T36 in flight`, `trimmed packet` or `GPT-6 Astra at`.
  - The pointer's only lines that name T37's values are `:22-24`, its *Current focus* paragraph describing this check.
- **The widened placeholder check:** `__[A-Z0-9_]+__|\b(CO|MERGE_|TIP|V2)HASH\b`, written in pieces as the pointer writes it, printed `0` on the pointer (rc 1).
- **Branch:** `feature/m6-doctrine-skills-685`, HEAD `11fa8f95b8`; `stacked-on-P1`; `coordinator-tip-merged`; the merge `87c2ab0fed`'s parents are `2174265e9c` and `3a9b0aec81`.

### [Stage A] 02:43 — the lint's Local proof (ruling (m)), the first check

The `# STAGE A` block of the brief's § 5 is `stage-a/stage-a-block.sh`: lines `:1069-1106` of the brief, with its coordinator's-tip placeholder filled in two lines. The `CO=` line reads `CO=3a9b0aec81`, the pointer's value, and chunk 4's comment names the coordinator's tip in place of the placeholder; the comment was filled after the run, and a comment does not execute. `diff` against the brief's lines prints those two lines. It ran in one shell through `stage-a/chunk-run.sh`, which splits the block at its column-0 comments and prints each chunk's start, end, wall seconds and the exit of its last command. The block's own `rc=` lines are the per-command record. Its second chunk is the lint proof (`stage-a/stage-a-block.out`; the lint's whole output is `stage-a/lint-local-pass.out` and `stage-a/lint-local-fail.out`):

<!-- include: stage-a/stage-a-block.out from ^== chunk-02 to ^== chunk-02.sh ends -->
```text
== chunk-02.sh begins 02:43:34: # the lint's PASS on a Local plan, before anything else (ruling (m)): T4's finished Local folder, ex
6ec78bbf8cc2dc07a3a46dd30c63132fbc7bbfc8
t4 plan: local D-WORKFLOW-184 0
lint, a Local plan, rc=0
  ok    PL-25 answers Q4

PASS
lint, tier_exception removed, rc=1
12:  FAIL  second-opinions/review-plan.json or its call evidence is invalid: local-only cannot satisfy Epic/Milestone
91:1 CONTRACT FAILURE(S)
== chunk-02.sh ends 02:43:35, last command rc=0, wall 1s
```

PROOF: A-01 (tool-run) -- the dispatch tip's `tools/lint-audit-artifacts` accepts a Local plan in an `-epic-` folder and refuses it without its `tier_exception`. T4's finished folder was exported from `6ec78bbf8c` (`origin/feature/m6-doctrine-rules-651` resolved to `6ec78bbf8cc2dc07a3a46dd30c63132fbc7bbfc8`; its plan read `t4 plan: local D-WORKFLOW-184 0`). The lint printed `lint, a Local plan, rc=0` and ended `PASS`; the copy with `tier_exception` removed printed `lint, tier_exception removed, rc=1`, with `FAIL  second-opinions/review-plan.json or its call evidence is invalid: local-only cannot satisfy Epic/Milestone` and `1 CONTRACT FAILURE(S)`. A FAIL would have been an rc other than 0 on the first, or rc 0 on the second (a lint that accepts any Local plan, so its PASS on this slice's folder would prove nothing).

### [Stage A] 02:43-02:44 — the rest of the `# STAGE A` block

<!-- include: stage-a/stage-a-block.out match ^== chunk -->
```text
== chunk-01.sh begins 02:43:34: D=/workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-skills-685
== chunk-01.sh ends 02:43:34, last command rc=0, wall 0s
== chunk-02.sh begins 02:43:34: # the lint's PASS on a Local plan, before anything else (ruling (m)): T4's finished Local folder, ex
== chunk-02.sh ends 02:43:35, last command rc=0, wall 1s
== chunk-03.sh begins 02:43:35: # the three moved files, against the P1 tip and against next (ruling (a), L-01): ` 3 files changed, 
== chunk-03.sh ends 02:43:35, last command rc=0, wall 0s
== chunk-04.sh begins 02:43:35: # other lanes' refs (proof correction 1, § 1): each ref's 52 read from its merge base with the coor
== chunk-04.sh ends 02:43:35, last command rc=0, wall 0s
== chunk-05.sh begins 02:43:35: # the checkers' baseline at the dispatch tip (R3 C6, C24; their lines may move with the dispatch's o
== chunk-05.sh ends 02:43:45, last command rc=0, wall 10s
```

- **Chunk 1** (02:43:34): `df -i` showed `/workspace` at 27% of its inodes before any scratch was written. Then the branch `feature/m6-doctrine-skills-685`; `git status --short` `0`; `stacked-on-p1`; `next-is-here`; the membership inputs' sha256 prefixes `49bc2745664e52f4` (`slices.json`) and `d17b9cac4b2c2245` (`inventory.json`), as § 2 names them; `clone-here`.
- **Chunks 3 and 4** (the drift and the refs) are A-03 and A-04 below.
- **Chunk 5, the checkers' baseline at the dispatch tip:**
  - `rules-check rc=0`, `rules-check: 30 rule files, every one front-mattered and indexed`. This is **no evidence for the 52**: the tool reads no skill or agent (§ 3 item 5).
  - `register-check rc=0`, `register-check: 714 IDs, each once; every citation in the live documents names a row`. That is 712 at `2f42ff5ddf`, 713 at `3a9b0aec81` (D-WORKFLOW-218 added) and 714 at HEAD (the P1 branch's D-WORKFLOW-188), by `stage-a/stage-a-extra.out`'s row counts.
  - `ceremony-check rc=0`, `nothing overdue.`; its full output (`stage-a/ceremony-check.out`) carries two `DUE` lines that are not this lane's: the retro (5 active days since 2026-10-26, blocks at 7) and the 2026-10 monthly summary (due by the 3rd). Both are noted on #685.
  - #685's title, `OPEN`, and its body at `77` lines after the coordinator's fill.
  - The host file's last six lines at 02:43:45 (below, § The host file).

### [Stage A] 02:44 — § 2's membership block

`stage-a/membership.sh` is the brief's `:390-507`, extracted by `sed` between its fences (`:389`, `:508`) and never retyped: `118` lines, sha256 prefix `7fa0430cf613e867` (the same command over the extract). It ran from the worktree at 02:44:16 (`membership block rc=0 wall 3s`). Its output, `stage-a/membership.out`, was diffed against the brief's expected lines `:516-536`: no line, `diff rc=0`.

PROOF: A-02 (tool-run) -- § 2's block, byte for byte, reaches exactly the inventory's 52 and prints the brief's expected lines. The output carries `mine: 52 paths.txt: 52 equal: True`, `only-mine: []`, `only-paths.txt: []`, `ls-tree at the inventory's head = paths.txt` and `paths.txt = ls-tree at 2174265e9c`, and `diff` against the brief's `:516-536` printed nothing, rc 0. `stage-a/membership-block-2.txt`'s CLAIMS holds `52` rows reading `in-T38 non-rest [('doctrine-skills', 38)]`. A FAIL would have been `equal: False`, a line in either `only-` list, or any `diff` line: a glob that reaches a path the inventory does not give T38, or misses one.

### [Stage A] 02:44 — both totals, the drift and the settings paths

`stage-a/dispatch-tip.sh` is § 2's dispatch-tip lines (`:558-568`); it ran at 02:44:38. Its output, `stage-a/dispatch-tip.out`:

<!-- include: stage-a/dispatch-tip.out -->
```text
dispatch tip: paths 52 lines 12783
 3 files changed, 50 insertions(+), 1 deletion(-)
 3 files changed, 50 insertions(+), 1 deletion(-)
18	1	.claude/skills/code-auditor/references/templates.md
25	0	.claude/skills/council/IMPORTED-FROM.md
7	0	.claude/skills/mini-retro/references/scoped-audit.md
0
0
```

The script's `rc=1` is its last command, `grep -c ''` printing `0`.

PROOF: A-03 (tool-run) -- the lane carries the dispatch tip's tree: `dispatch tip: paths 52 lines 12783`, beside the block's `lines: 12734` at the P1 hash. The difference is the coordinator's three files alone: ` 3 files changed, 50 insertions(+), 1 deletion(-)` against `2174265e9c` and again against `8ebaf8daad`, with numstat `18 1`, `25 0` and `7 0`. The `# STAGE A` block's chunk 3 printed the same shortstat twice. A FAIL would have been any fourth file in the numstat, or a total that is not 12,734 plus the numstat's 50 less its 1: something else in the 52 moved.

PROOF: A-05 (tool-run) -- "settings" names no tracked path (ruling (g)). `git ls-tree -r --name-only HEAD -- .claude/ | grep -c -i settings` printed `0`, and `git log --all --oneline -- '.claude/settings*' | grep -c ''` printed `0`. A FAIL would have been a non-zero count: a tracked settings file this slice would have to read.

### [Stage A] 02:43 — other lanes' refs

The block's chunk 4 printed `refs scanned: 83` and no `own change to the 52:` line. The proof's run at `2f42ff5ddf` scanned 82; this lane's own branch did not exist then (the brief's § 1: absent before dispatch).

PROOF: A-04 (tool-run) -- no `feature/m6-*` ref, local or `origin/`, carries a change of its own to the 52. Each of the 83 was compared from its merge base with the coordinator's tip (`git diff --quiet "3a9b0aec81...$r" -- .claude/agents .claude/skills`), and none printed. The comparison can fire: the P1 tip as the base and the coordinator's tip as the ref printed `the loop's positive, the P1 tip as base and the coordinator's tip as the ref: rc=1`. A FAIL would have been an `own change` line (another lane moved the 52, to be named on #685 before stage B), or a positive at rc 0 or 128 (a comparison that cannot fire, or an unfilled coordinator's-tip placeholder).

### [Stage A] 02:44:49-02:44:52 — § 5's runs

`stage-a/runs.sh` is the brief's `:1129-1218`, the runs block up to its `# STAGE C` line: 22 chunks, with `stage-a/runs.out` as the output. Its stage-C line is not run here, because the checker does not exist yet. Its stage-A removal check is `stage-a/removal.sh` (`:1221-1222`, the lane's-tip placeholder filled with `87c2ab0fed`). The chunks:

<!-- include: stage-a/runs.out match ^== chunk -->
```text
== chunk-01.sh begins 02:44:49: export LC_ALL=C; G=/usr/bin/grep; T=/workspace/tmp/m6-t38; X=':(exclude).claude/rules/'
== chunk-01.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-02.sh begins 02:44:49: # the read tree, once (expect 52 -- R1 C05; R2 C1; R3 C1)
== chunk-02.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-03.sh begins 02:44:49: # L-01: the moved files' commits and the scoped-audit hunk (expect the five commits of § 2 -- R1 C0
== chunk-03.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-04.sh begins 02:44:49: # front matter (expect `FRONT-MATTER 18 NONE 34` -- R3 C17: the 10 SKILL.md and the 8 agents carry i
== chunk-04.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-05.sh begins 02:44:49: # L-02: the evidence floor (expect 157 the heading, 159 `Three hard rules`, then 161, 166, 179, 186 
== chunk-05.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-06.sh begins 02:44:49: # L-03, L-04 (expect `420:` and `711:` -- R4 C24, C26)
== chunk-06.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-07.sh begins 02:44:49: # L-05: durations used as estimates, by the widened pattern (`~N min`, `~N hr`, `~N–N hr`, `~1 day
== chunk-07.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-08.sh begins 02:44:49: # L-06, L-07, L-08, L-20: what the skills do not name (expect no line from either, the second's rc 1
== chunk-08.sh ends 02:44:49, last command rc=1, wall 0s
== chunk-09.sh begins 02:44:49: # L-09 (expect 5 lines in 2 files by `state-main` -- R3 C21)
== chunk-09.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-10.sh begins 02:44:49: # L-10, L-11, L-13: the blocks and sentences a reader would act on (expect the stash and vitest line
== chunk-10.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-11.sh begins 02:44:49: # L-23: the two texts, quoted whole into 02 (expect release-candidates.md:74-76 and review-levels.md
== chunk-11.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-12.sh begins 02:44:49: # the brief's grep (expect `80` -- R1 C19)
== chunk-12.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-13.sh begins 02:44:49: # L-22 (expect `19`, `1`, and no line -- R1 C13, C19)
== chunk-13.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-14.sh begins 02:44:49: # L-30, L-31, L-47: the council family's absences (expect no line; a non-zero rc; `0` -- R2 L-01, L-
== chunk-14.sh ends 02:44:49, last command rc=1, wall 0s
== chunk-15.sh begins 02:44:49: # #1044's loop over the slice, its criterion's pattern (R4 item 33): every MISSING line recorded -- 
== chunk-15.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-16.sh begins 02:44:49: # L-34: the bundle's sums against the tree (expect `BUNDLE match=52 diff=39 absent=3` -- R3 C15; R1 
== chunk-16.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-17.sh begins 02:44:49: # the pins, recomputed offline, never by running scripts/verify-pins.ts (expect eight MATCH lines an
== chunk-17.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-18.sh begins 02:44:49: # the stale names (R3 C21's terms, case-insensitive; expect its table: rubber[- ]duck 0/0, copilot 4
== chunk-18.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-19.sh begins 02:44:49: # the IDs the 52 cite (expect 16, each resolving -- R2 C24; R2's loop is not printed, so the lane's 
== chunk-19.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-20.sh begins 02:44:49: # the roster's rows in the rule (expect the Claude and GPT rows of adversarial-council.md:77-78 -- R
== chunk-20.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-21.sh begins 02:44:49: # the contract read: the lint's constants against the templates (R3 § 2.6), parsed from the lint at
== chunk-21.sh ends 02:44:49, last command rc=0, wall 0s
== chunk-22.sh begins 02:44:49: # the text checks over the 52, in the hooks' own form (expect the compile rc at most 1, the planted 
== chunk-22.sh ends 02:44:52, last command rc=0, wall 3s
```

Every chunk printed the line its comment expects. Each run's figure, exit and *a FAIL would mean* go into `02` § The runs at stage B. The open items this settles:
- **Open item 4:** L-30's three `scripts/__tests__/` files are `MISSING`, while the two the pattern also reaches are `PRESENT`.
- **Open item 7:** `tools/ceremony-check`, `.githooks/hooks-test` and `tools/box-check` at the dispatch tip, the lines above.

PROOF: A-07 (tool-run) -- the eight agent files' bytes match their pins, recomputed offline as `pins[path].sha` with no Node and no `scripts/verify-pins.ts`: eight `MATCH` lines and `pins MATCH 8 of 8`. A FAIL would have been a `DIFF` line: an agent edited after its pin, or a pin naming bytes the tree does not hold.

PROOF: A-09 (tool-run) -- no line of the 52 is credential-shaped in the hooks' own form. `.githooks/secret-patterns` was sourced for its one regex and never `guard_load`. The compile printed `secret regex compile rc=1`, a private-key header assembled at run time matched `1`, and the scan over the export printed `0` files. A FAIL would have been a non-zero file count, or a compile rc above 1 or a `0` on the positive (a scan that cannot match anything).

PROOF: A-10 (tool-run) -- no line of the 52 carries a listed word. `forbidden-terms-check: 0 hits on stdin` over the 52 concatenated, with `forbidden-terms over the 52 rc=0`; it also gives `rc=0` over empty input, so that 0 alone is not evidence. A planted line through `FORBIDDEN_PATTERNS`, which the tool reads instead of the list, printed `forbidden-terms-check: 1 line(s) on stdin carry a listed word` and `forbidden-terms, a planted positive, rc=1`. The list itself was never read, listed or quoted. A FAIL would have been an rc of 1 over the 52, or rc 0 on the planted line.

- `hooks-test rc=0`, `PASS`; `box-check rc=0`, `box-check: 300 issue(s), 633 open checkbox(es), 0 fail, 13 issue(s) with rows to re-derive against`. The 13 notes name other lanes' issues and #1373, which D-WORKFLOW-218 cites; none is this lane's to re-derive at stage A.

### [Stage A] 02:45-02:50 — the reads the brief leaves to the lane

`stage-a/stage-a-extra.sh` is written here and its output is `stage-a/stage-a-extra.out` (re-run at 02:50:01 after the moved files' line counts were added). It holds:
- the removal check;
- each ID the 52 cite looked up in the decided and the open table at `3a9b0aec81`;
- the highest decided row per area;
- the register's rows at three hashes;
- the three moved files' lines at the P1 tip, `next` and HEAD;
- the rules this session loaded against the coordinator's tip.

<!-- include: stage-a/stage-a-extra.out -->
```text
02:50:01
removal check: the lines above are its output (none expected); its rc is tail's
open decisions heading at :780
D-WORKFLOW-003 dec:1 open:0
D-WORKFLOW-009 dec:1 open:0
D-WORKFLOW-068 dec:1 open:0
D-WORKFLOW-074 dec:1 open:0
D-WORKFLOW-078 dec:1 open:0
D-WORKFLOW-079 dec:1 open:0
D-WORKFLOW-088 dec:1 open:0
D-WORKFLOW-089 dec:1 open:0
D-WORKFLOW-090 dec:1 open:0
D-WORKFLOW-102 dec:1 open:0
D-WORKFLOW-109 dec:1 open:0
D-WORKFLOW-133 dec:1 open:0
D-WORKFLOW-135 dec:1 open:0
D-WORKFLOW-137 dec:1 open:0
D-WORKFLOW-149 dec:1 open:0
D-WORKFLOW-184 dec:1 open:0
-- highest decided per area above :780 at 3a9b0aec81:
D-CLOUD-193 D-INFRA-031 D-LAUNCH-007 D-NET-017 D-QA-063 D-RA-052 D-SYS-013 D-UI-137 D-WORKFLOW-218 
register rows at 2f42ff5ddf: 712
register rows at 3a9b0aec81: 713
register rows at HEAD: 714
+| D-WORKFLOW-188 | 2026-10-23 | **The r
-- the three moved files, lines at the P1 tip, at next and at HEAD (grep -c ''):
.claude/skills/code-auditor/references/templates.md 331 331 348
.claude/skills/council/IMPORTED-FROM.md 102 102 127
.claude/skills/mini-retro/references/scoped-audit.md 709 709 716
-- the rules this session loaded (52e6794ba7) against the coordinator's tip:
 .claude/rules/device-builds.md          | 12 +++++++
 .claude/rules/engineering-practices.md  | 58 +++++++++++++++++++++++++++++++--
 .claude/rules/es-code-traps.md          | 44 +++++++++++++++++++------
 .claude/rules/es-native-ui.md           | 16 ++++++---
 .claude/rules/es-player-text.md         | 10 ++++--
 .claude/rules/es-ui-style-guide.md      |  2 +-
 .claude/rules/fork-workflow.md          |  2 +-
 .claude/rules/generic-x64-vm-testing.md | 53 ++++++++++++++++++++++++++++++
 .claude/rules/instruction-files.md      |  5 +--
 9 files changed, 175 insertions(+), 27 deletions(-)
-- this lane's ref:
feature/m6-doctrine-skills-685 11fa8f95b8
```

PROOF: A-06 (tree) -- nothing outside the 52 and nothing in the council family has moved on the lane's branch since the dispatch tip: `git diff --stat 87c2ab0fed HEAD -- .claude/rules CLAUDE.md AGENTS.md NAMING.md verifier-pins.json scripts tools .claude/skills/council .claude/skills/council-research .claude/agents | tail -n 1` printed no line, run as `stage-a/removal.sh` and inside `stage-a-extra.sh`. A FAIL would have been any line: an edit this slice may never make, which is a stop. The check is re-run before every commit of the lane.

PROOF: A-08 (tool-run) -- every decision ID the 52 cite resolves in the decided table at `3a9b0aec81`. The runs printed `16`, and the lane's look-up printed sixteen lines, each `dec:1 open:0` (D-WORKFLOW-003, -009, -068, -074, -078, -079, -088, -089, -090, -102, -109, -133, -135, -137, -149, -184). A FAIL would have been `dec:0` (a citation naming no row) or `open:1` (a decided-sounding citation of an open question).

- **Which commit touched which moved file:** `stage-a/moved-commits.sh`, run at 02:53:15 with rc 0. `161effca8f` touched `scoped-audit.md`, `fa6bcdafa8` (merged at `18747fbc52`) `templates.md`, and `0ceb2994c5` and `033eb7ed23` `IMPORTED-FROM.md`. Its output is included in `01` § Scope.
- **The register line:** `D-CLOUD-193 D-INFRA-031 D-LAUNCH-007 D-NET-017 D-QA-063 D-RA-052 D-SYS-013 D-UI-137 D-WORKFLOW-218`, read from the table above `:780` at `3a9b0aec81`. This is the pointer's `Register:` line, row for row.
- **The rules this session loaded:** they came from T5's worktree (`52e6794ba7`) and differ from the coordinator's tip in 9 files, `9 files changed, 175 insertions(+), 27 deletions(-)`. The four that bind how this lane works -- `engineering-practices.md`, `instruction-files.md`, `fork-workflow.md` and `device-builds.md` -- were read in their changes at `3a9b0aec81` at 02:46. Every rule § 3 item 1 names is read at `3a9b0aec81` by `git show` at stage B, never from the session's loaded copy (`01` § Pre-flight).

### [Stage A] 02:44 — the host file, for its protocol alone

- **The first read, at 02:43:45 (`date -u`):** the block's `tail -n 6`, at its chunk 5. These are other lanes' lines, T36's compile START, END and START with the coordinator's acknowledgements:

<!-- include: stage-a/stage-a-block.out from ^02:43:45$ to ^== chunk-05.sh ends -->
```text
02:43:45
2026-11-01T02:29:47Z T36 (#683) lane: stage E compiles START (S9 tip: #1367 against the fixed TextureData.cpp; host-only, no guest).
== M6 coordinator — 02:29 UTC (2026-11-01): acknowledged T36 (#683) lane: stage E compiles START (2026-11-01T02:29:47Z; host-only compile, no guest, no image build) -- automatic acknowledgement by k
2026-11-01T02:30:05Z T36 (#683) lane: stage E compiles END (S9 tip: #1367 loadFromPdf=true for a loaded page, control false, rc 0; PASS-at-tip).
== M6 coordinator — 02:30 UTC (2026-11-01): acknowledged T36 (#683) lane: stage E compiles END (2026-11-01T02:30:05Z; host-only compile, no guest, no image build) -- automatic acknowledgement by kit
2026-11-01T02:41:42Z T36 (#683) lane: stage E compiles START (S10 pin: G-6/G-7, G-14, G-10 ASan harnesses against pre-S10 copies; host-only, no guest).
== M6 coordinator — 02:41 UTC (2026-11-01): acknowledged T36 (#683) lane: stage E compiles START (2026-11-01T02:41:42Z; host-only compile, no guest, no image build) -- automatic acknowledgement by k
== chunk-05.sh ends 02:43:45, last command rc=0, wall 10s
```

- **The second read, at 02:44:07Z:** `host file lines: 689`, `lines matching T38|#685: 0`. The dispatch recorded 687 lines at 02:40, none matching. Criterion 19 subtracts these figures from the count at the hand-back.
- **The protocol (lines 1-3):** M7 writes timestamped lines; M6 writes `== M6 coordinator — HH:MM UTC (date): ...` blocks; every START, RETURN or request line is acknowledged within the minute with a census.
- **This lane writes no line there and posts no START:** a prose slice compiles nothing.
- **Census at 02:44** (`pgrep -c -x`): `qemu-system-x86` 0, `cc1` 0, `cc1plus` 0, `ninja` 0, `make` 0. The guest's binary name is longer than the 15 characters `-x` matches, so its 15-character process name was used. None of these processes is this lane's at any time.

### [Stage A] 02:46-02:48 — the issues, re-read

`stage-a/issues.sh` re-read the 32 issues § 3 item 9 lists, and #685's comments. Output `stage-a/issues.txt`, re-run at 02:48:53:

<!-- include: stage-a/issues.txt -->
```text
2026-11-01T02:48:53Z
#685 OPEN  comments=4 M6.P2 E807/T38: doctrine: the skills, agents and settings
#807 OPEN  comments=1 M6.P2 E339: Area epic: the doctrine (T4, T38, T39)
#651 OPEN  comments=20 M6.P2 E807/T4: doctrine: the binding doctrine: rules, CLAUDE.md, AGENTS.md, the registers
#686 OPEN  comments=1 M6.P2 E807/T39: doctrine: the reference documents
#911 OPEN  comments=0 Bug: council-substrate-integrity.md names ten defences this tree does not have
#810 OPEN  comments=4 Bug: lint-audit-artifacts refuses depth local in an epic-tier folder, against D-WORKFLOW-1
#342 OPEN  comments=0 Time is not a planning factor: the instruction files re-examined for time-free estimates
#640 OPEN  comments=5 Ops: Move the primary checkout to /workspace/repos/pixelelated/distribution and retire the
#1044 OPEN  comments=1 Backlog: council toolchain, fork side -- the wrapper's env guard and test runner, the tool
#1045 OPEN  comments=0 Backlog: council toolchain -- the next export refresh: a written procedure, pristine bytes
#343 OPEN  comments=0 Council toolchain: a Setup PONG probe with zero reasoning tokens halts the whole run (effo
#850 OPEN  comments=1 Backlog: council-invoke's --help names the old 360000/1800000 ms timeouts; the code enforc
#314 OPEN  comments=1 Retro on the adversarial review round: the meta-learnings, through the recursive learning 
#287 OPEN  comments=1 Council and code-audit calls go through the Facilitator on OpenRouter; the native harness'
#260 OPEN  comments=2 code-auditor: an adversarial second-model phase by default (the GPT seat, max effort), and
#378 OPEN  comments=3 Use a second lab for two-model code audits; keep five-seat council separate
#261 OPEN  comments=2 Roadmap: carry the adversarial code-audit learnings into the upstreamed CI/CD, project-man
#333 OPEN  comments=2 Upstream PRs: no AI attribution anywhere upstream-bound, descriptions in the maintainer's 
#326 OPEN  comments=0 The 2026-09-29 review's decisions: the series' shared files, #325 now, the appendix's home
#341 OPEN  comments=0 After the migration: relax the policies that existed for upstream (attribution, one commit
#645 OPEN  comments=1 M6.P2: Upstream refuses PRs touching packages/ and its PR process has rules the fork's do 
#953 OPEN  comments=0 Bug: prose-check's sign-off pattern cannot match a sign-off at a line's end, and its repea
#955 OPEN  comments=0 Bug: pr-stack-check's header claims a stack whose last head equals next; its EXIT trap for
#268 OPEN  comments=2 Agent-first acceptance criteria: every checkbox is agent-verifiable and names its artifact
#235 OPEN  comments=0 Epic: offer the fork's VM QA, quality tooling and agent practices to the ROCKNIX project
#943 OPEN  comments=0 Bug: ceremony-check reads --limit 200 of 331 closed issues, does not count a gh failure in
#254 OPEN  comments=1 Operationalise the ceremonies: tools/ceremony-check in the push guard and the fork CI, the
#809 OPEN  comments=0 Backlog: renovation-inventory renders a prose slice's read count three ways (0 read vs N o
#540 CLOSED COMPLETED comments=1 M7.P5: Resolve network/cloud audit — 7 findings (3 high)
#1308 OPEN  comments=1 Backlog: lint-audit-artifacts accepts a held second-opinion reply bound by its receipt's s
#585 OPEN  comments=29 Standing: Queue upstream contributions after the initial build
#1373 OPEN  comments=0 Backlog: tools/skills-check -- front matter, cross-references, stale names, the seats' ros
-- #685's comments:
2026-10-23T06:56:32Z blitterbot **Lead for this slice, from T1's brief proof (2026-10-23, coordinator):** `.claude/skills/code-auditor/SKILL.m
2026-10-24T04:54:57Z blitterbot **Coordinator, a lead for T38 from T4's stranger's proof (2026-10-24):** `.claude/skills/code-auditor/SKILL.md
2026-10-24T15:21:20Z blitterbot **Lead from T4 (coordinator, 2026-10-24; #651/#912 PL-17, bug #911), deferred to this slice:** `.claude/rules/
2026-11-01T02:40:26Z blitterbot **Dispatch (coordinator, 02:40 UTC 2026-11-01) to the T5 session (`m6-t5-build-engine`, free since T35's close
```

`#540` is `CLOSED COMPLETED`; the other 31 are `OPEN`. #685 carries its three lead comments and the dispatch.

### [Stage A] census

- **What did not happen:** no build, no compiler, no guest, no fetch (no `git fetch`, `git ls-remote` or `gh api` of another repository), no council run, no Facilitator call, no `tools/council/run`, no `npm install`, no keyed call, no skill invoked against a provider. No held directory was opened, no line was written in the host file, and nothing was edited under `.claude/`.
- **Scratch:** `/workspace/tmp/m6-t38/`, made after `df -i`. It holds:
  - the export `/workspace/tmp/m6-t38/export/` (52 files, 771,266 bytes by `du -sb`);
  - the lint proof `/workspace/tmp/m6-t38/lint-proof/` (672,359 bytes);
  - `stage-a/`, `tmp/` and `inc-test/`.

  All are retired at stage H, their paths and sizes recorded here then. `.qa-scratch/t38/` (gitignored) holds the membership block's files.
- **The placeholder check before the commit:** the widened pattern of the errata, `__[A-Z0-9_]+__` with the four hash words, written in pieces, prints `0` on the pointer, on this log, on `01` and on every file under this folder.
  - The brief's extracts carry their placeholders filled. In `stage-a/stage-a-block.sh` that is the `CO=` line and chunk 4's comment; in `stage-a/removal.sh`, the command and its comment. Each comment was filled after the run (a comment does not execute), and `stage-a/runs.sh` and `stage-a/membership.sh` equal the brief's `:1129-1218` and `:390-507`.
  - The day's work log's `:39`, in the coordinator's 02:16 entry, names the coordinator's-tip placeholder as a word. That line is the coordinator's; this lane's appended entry carries no match.

### [Stage B] 03:00-03:30 — the reader's pass, then the auditor's read in ruling (j)'s order

- **The coordinator's acceptance of stage A** (issuecomment-6552603604, 02:58 UTC) was read first: start stage B in the named order, a no-context reader per skill before the lane's own read, no edits.
- **The reader's pass, 03:00:** eleven Explore-type subagents launched at once, each given one directory of the export and nothing else. Each report is saved verbatim as `stage-b/reader-*.md` (`01` § The reader's pass). Two readers say they ran one listing (`ls`, `find`) and nothing else; none ran a command that writes or calls out.
- **The rules, 03:00-03:02:** read at `3a9b0aec81`. The four the lane's commands depend on were read in their changes at stage A. `council-substrate-integrity.md`, never loaded this session, was read by `git show` (`01` § Read order). The lint's own contract was read from its source at the tip; its `ANALYSIS_SECTIONS` comparison is `sec.lower() in analysis.lower()`, which settles open item 2.
- **The auditor's read, 03:03-03:20,** each skill after its reader. The notes are `stage-b/notes-*.md`; each check a note called for is a script under `stage-b/` with its output, first line the `date -u` of the run:
  - `checks-code-auditor` 03:06:18;
  - `checks-mini-retro` 03:08:18;
  - `checks-futro` 03:10:12;
  - `checks-sessions` 03:11:25;
  - `checks-writing-pair` 03:13:15;
  - `checks-council` 03:16:59;
  - `floor-reads` 03:18:53;
  - `blocks` 03:25:23.

  Each exited 0, except `blocks.sh`, whose last command is a `grep -c` printing `0`.
- **The tables, 03:21-03:24:** `tools/t38-tables.py` (`coverage`, `q4`, `q5`, `q6`, `q7`), with outputs under `stage-b/tables/`.
  - Each subcommand exited 0 on the export and 1 on its constructed drift (`tools/t38-tables-drift.sh`, `stage-b/tables/drift.out`, run at 03:24:02 and again after the `q6` fix).
  - Two generator defects were met and fixed before any table was trusted: `q4`'s pattern for a phrase that wraps a line, and `q6`'s profiles, which omitted `definitive`.
  - The drift script's first run printed a harness error (its scratch did not exist); fixed, and re-run whole.
- **Corrected in the record before commit:**
  - `notes-futro.md` had said #1556 and #1558 name other issues on this tracker; they are above 1385, and the note says so;
  - `04`'s summary had typed two figures; both are now the computed `7,234` lines, ten descriptions, and `50` leads owned by the T38 stream (`stage-b/summary-figures.sh` and `.out`).

PROOF: B-01 (tree) -- L-02: `code-auditor/SKILL.md`'s floor says three rules and numbers five 1, 2, 3, 4, 3 (`stage-a/runs.out` chunk 5); the import `437ebd09af` had three (`116:3.`), and `9a09b76dd9` inserted two without renumbering (`stage-b/checks-mini-retro.out`). A FAIL would have been a numbering of 1 to 5, or the count matching it.
PROOF: B-02 (tree) -- L-11: `tools/fork-publish-release:6-7` at the tip says `No upload, tag creation, asset replacement or publication occurs.` (`stage-b/checks-writing-pair.out`). A FAIL would have been an upload path in the tool's source, making the skill's *uploads the files* true.
PROOF: B-03 (tree) -- L-56: `phases.md:439`, `:486-491`, `SKILL.md:247`, `:508` and `review-levels.md:9` fail Phase 4.6 closed at epic tier, while `templates.md:129-146` and the lint accept Local there (A-01); #810's checkbox names `templates.md` alone (`stage-b/checks-code-auditor.out`). A FAIL would have been any of the five naming D-WORKFLOW-184's exception.
PROOF: B-04 (tool-run) -- L-52: `git grep -c -E 'pre-issue|--phase'` over `code-auditor` printed nothing, rc 1. A FAIL would have been a line: the skill naming the pre-issue phase.
PROOF: B-05 (tree) -- L-60: the lint compares `sec.lower() in analysis.lower()`, so `## Acceptance Criteria Scorecard` misses `Acceptance-criteria scorecard` and the other two headings pass by case. A FAIL would have been a normalising comparison, making all three pass.
PROOF: B-06 (tool-run) -- L-10: the work logs, the friction log, the retros, the futros and the audit folders name `git stash pop` or `npx vitest` nowhere but this slice's stage-A output (`stage-b/checks-mini-retro.out`). A FAIL would have been a session's record of the block run: an `Already written:` to migrate.
PROOF: B-07 (tool-run) -- L-13: `gh repo set-default --view` printed `No default remote repository has been set`, with `upstream` pointing at ROCKNIX (`stage-b/checks-futro.out`). A FAIL would have been a default of `pixelelated/distribution`, filling `{owner}/{repo}` correctly here.
PROOF: B-08 (tool-run) -- L-66: `origin/main rc=1`, `main rc=1`. A FAIL would have been either at rc 0.
PROOF: B-09 (tool-run) -- L-58: #2299, #2634, #2382, #2952, #3059, #2510, #2674, #2302, #2289, #2387, #1556, #1558, #2373, #2545, #2647 and #2648 resolve to nothing (the tracker's highest is 1385), and `#203` resolves to `Launching a game while saves sync ...`. A FAIL would have been an issue of this tracker that is the citation's.
PROOF: B-10 (tree) -- L-30: `.githooks/` holds `0` council hooks and `0` files naming the council-research lints. A FAIL would have been the two hooks `council-research/SKILL.md:407-411` says exist.
PROOF: B-11 (tree) -- L-32 withdrawn: `council-research/references/phase-4-council-deliberation.md` is present and `council/references/phase-4-council-deliberation.md` absent, and the sentence at `council/SKILL.md:188-190` names council-research as its subject. A FAIL would have been the path under council, or the sentence naming council.
PROOF: B-12 (tree) -- L-35 narrowed: each agent's relative `references/member-roster.md` is named *"the council skill's"* in its sentence, and three write the repo-rooted path. A FAIL would have been a bare relative path.
PROOF: B-13 (history) -- L-19 corrected: `session-stash/SKILL.md:32` reads `prove it by giving an agent with no context only the repository and asking it to resume`, from `d8df0877a4`. A FAIL would have been no such sentence.
PROOF: B-14 (tree) -- L-08's delta: `docs/retrospective` is present at HEAD, the P1 tip, `next` and the coordinator's tip, holding one file, `carry-forward.md`. A FAIL would have been absent, as the brief records.
PROOF: B-15 (tool-run) -- the counts a skill states, recomputed by `tools/t38-tables.py q4` (c): eight `no`, two `yes`. A FAIL would have been a stated count equal to its recomputation.
PROOF: B-16 (tool-run) -- the duplicates by `tools/t38-tables.py q7`: *pixelelated continuation* `identical, 10 lines` twice, the criterion entry `9 line(s) differ`. A FAIL would have been a difference in the first, or none in the second.
PROOF: B-17 (tree) -- L-69's Already written: the canonical stash on `next` opens `8:## Start here`. A FAIL would have been no *Start here*: a stash already written by the template's gap.
PROOF: B-18 (tool-run) -- L-37: `0` register rows name #636 or #638. A FAIL would have been a row.
PROOF: B-19 (tool-run) -- every table generator printed rc 0 on the export and rc 1 on its constructed drift, ten lines each at its wanted exit (`stage-b/tables/drift.out`). A FAIL would have been a drift a generator printed without failing.
PROOF: B-20 (tool-run) -- L-53: Phase 0's `diff -q` over `SKILL.md` printed `rc=0` while the same diff over `templates.md` printed `rc=1` (`stage-b/blocks.out`). A FAIL would have been the check reading the references too.
PROOF: B-21 (tool-run) -- the roster agrees across `adversarial-council.md:77-78`, `member-roster.md` and the five active agents, five `yes` (`tools/t38-tables.py q4` (e)). A FAIL would have been a `no`, which the generator exits 1 on.
PROOF: B-22 (history) -- L-67: *"Apply four techniques"* came with `437ebd09af`, and the fifth bullet with `3624e2e329` (`stage-b/checks-futro.out`). A FAIL would have been the count moved with the bullet.
PROOF: B-23 (tool-run) -- L-18: `0` files under `tools/` or `.githooks/` name `saved-session-state` or `sessions/archived`. A FAIL would have been a tool that archives or refuses.
PROOF: B-24 (history) -- L-11's dates: the skill's sentence `9404f23c55` (2026-09-29), the tool's *no upload* `f10eec1306` (2026-10-09) (`stage-b/checks-writing-pair-2.out`). A FAIL would have been the tool's change before the skill's sentence: false from the day it was written.

### [Stage B] census

No build, no compiler, no guest, no fetch, no council run, no Facilitator call, no `tools/council/run`, no `npm install`, no keyed call, no skill invoked against a provider, no held directory opened, no line in the host file. The only writes are under this folder, `/workspace/tmp/m6-t38/` (the drift copies at `/workspace/tmp/m6-t38/drift/`, retired at stage H), and `.qa-scratch/t38/`. Nothing under `.claude/` was edited.
- **The last line of stage B (`date -u` 03:33:20):** `git status --short -- .claude/agents .claude/skills` printed 0 lines.

### [Stage C] 03:37-03:52 — the plan, the checker FAIL-first, the punch list, the pre-issue lint

- **03:37:44 `second-opinions/review-plan.json`:**
  - `depth` is `local`, `reviewers` is `[]`, and `tier_exception` is `D-WORKFLOW-184`, the reason plan § 6c.
  - It was written before any call; this slice makes none.
  - The model is `anthropic/claude-opus-5-5`, not the template's slug (L-51).
- **The checker, `tools/t38-checks.sh` and `tools/t38-checks.py`:**
  - **What it reads:**
    - the read tree, `git archive HEAD .claude/agents .claude/skills` under `/workspace/tmp/m6-t38/export/`, never a checkout;
    - the rule's rows, `verifier-pins.json` and the lint's constants, read by `git show HEAD:`. HEAD is `168bbba783`, whose `.claude` and `tools` equal the dispatch tip's (A-06).
  - **The steps:** inventory, front, refs, stale, roster, pins and contract, then the allowlists themselves, with the bundle reported as information only.
  - **The three allowlists:** 13 legit, 26 inherited and 19 findings. It writes only under `--out`.
  - **Its refusals** exit 2 and check nothing.
- **03:43:44-03:44:12, runs 1 to 3.** Each FAIL-first case puts a planted positive into the tip's unfixed text on a copy under `/workspace/tmp/m6-t38/mut/`. The text's own run 1 passes, so each FAIL belongs to the probe.
  - **Run 2a** printed `rc=0` for three cases: roster, pins and contract.
    - The inherited `path:*` entries excused the agents' integrity failures.
    - The contract key `templates.md:0` collided with the legit entry for `01-research-notes.md`.
  - **The fix:** `ALLOWABLE` admits only the text steps, and a contract item is keyed by its name and never matched by `*`. Runs 1, 2 and 3 were then made again.
  - **This is Check 7 (harness self-coverage):** the guard's own FAIL-first found a guard that could not fail.
- **03:45:53-03:48:33, `05-punch-list.md`.**
  - It is written by `tools/t38-punch.py` from one list: 57 items, every one Open.
  - The proposals are 5 bugs for stage D, 41 punch items, 6 questions for the pause, and 5 inherited, owned by #911, the coordinator or #1373.
  - The generator refuses when a lead of `02` is neither cited nor listed. The first pass found three, L-01, L-25 and L-26, now listed with where each lives. The refusal was then proved by planting a gap.
  - The pre-issue lint passes it.
- **Stage C's corrections to the notes:**
  - `02` § The names and the references: the provenance terms are left out of the `stale` step's terms, not allowlisted.
  - `stage-b/notes-council-family.md`: the agents' `../../.github/instructions/` link resolves to the root's absent `.github/instructions/`; it does not climb out of the repository.
  - `04`'s scorecard is re-verdicted at stage C, with its pass rate computed.

PROOF: C-01 (tool-run) -- the Local plan: the pre-issue lint printed `ok    review-plan: local at epic tier under D-WORKFLOW-184 (...)` and `0 verified external calls` (`stage-c/run-4-lint-pre-issue.out`). A FAIL would have been a reviewer named, or a plan the lint refuses.
PROOF: C-02 (tool-run) -- run 1, the tip with every allowlist: `rc=0`, `TOTAL: 947 of 947 assertions`, `allowlists 58 of 58 passed` (`stage-c/run-1-baseline.out`). A FAIL would have been an assertion no entry excuses, or an entry that excuses nothing.
PROOF: C-03 (tool-run) -- run 2: nine planted positives, one per probe, each `want 1 rc=1` with its FAIL line; the bundle's `want 0 rc=0` with `BUNDLE match=51 diff=40` (`stage-c/run-2-firstfail.out`). A FAIL would have been a probe at `rc=0` on its positive.
PROOF: C-04 (tool-run) -- run 2's seven refusals, each `want 2 rc=2` and `refused: ...; nothing checked`: no `--tree`, a checkout, no python3, the lint unreadable, an entry without its reason, a finding with `*`, an allowlist missing. A FAIL would have been a refusal case that checked something.
PROOF: C-05 (tool-run) -- run 2a against run 2: `roster-gpt-slug`, `pins-one-byte` and `contract-05-removed` at `want 1 rc=0` before the fix, `rc=1` after (`stage-c/run-2a-firstfail-before-the-fix.out`). A FAIL would have been a case still at `rc=0` after the fix.
PROOF: C-06 (tool-run) -- run 3, `--withhold findings`: `rc=1`, `TOTAL: 902 of 928 assertions`, 26 FAIL lines over 19 keys, equal to the 19 entries of `allow-findings.txt` (`stage-c/run-3-tip-findings-withheld.out`). A FAIL would have been a key with no entry, or an entry with no failing key.
PROOF: C-07 (tool-run) -- `tools/lint-audit-artifacts --phase pre-issue`: `rc=0`, `PASS pre-issue artifacts (does not certify resolution)`, `57 punch item(s)`, and no FAIL line (`stage-c/run-4-lint-pre-issue.out`). A FAIL would have been an item without its Phase 7 row, its index entry or its `question:`.
PROOF: C-08 (tool-run) -- `tools/t38-punch.py`: 85 leads in `02`, 82 cited by an item and 3 listed. The planted gap was refused: `t38-punch: refused: leads 85, uncited [25], unknown [99], both []` (`stage-c/punch-refusal-planted.err`). A FAIL would have been a `05` written with a lead unaccounted.

### [Stage C] census

No build, no compiler, no guest, no fetch, no council run, no Facilitator call, no `tools/council/run`, no `npm install`, no keyed call, no skill invoked against a provider, no held directory opened, no line in the host file. The writes are under this folder and `/workspace/tmp/m6-t38/`, where the checker's outputs are `checks-*` and the FAIL-first copies are `mut/`; both are retired at stage H. Nothing under `.claude/` was edited.
- **The last line of stage C (`date -u` 03:52:02):** `git status --short -- .claude/agents .claude/skills` printed 0 lines.

### [Stage D] 03:57-04:04 — the five bugs, the audit issue, the two questions

- **03:57 accepted.** The coordinator accepted stage C (#685, 03:56) and said the five bugs go on as proposed. It posted the `council-research` question on #807 as comment `6553118160` (two options, the coordinator's reading B).
- **The reads behind the `Already written:` lines** (`stage-d/checks-bugs.sh`, `.out`) and **the sibling hunt** (`stage-d/siblings.out`). Both are read-only. Two claims in the drafts were corrected against them before filing: the shared-stash rule now cites the brief's never-run list, not `CLAUDE.md`, and the completion markers are described without a claim about how each was written.
- **04:00:23, the five bugs**, label `bug`, no milestone, not sub-issues. Each carries its code trace, its `Already written:` line and the VM line in § 6's shape. The bodies are in `stage-d/bug-PL-0N.md` and the numbers in `stage-d/bugs.tsv`:
  - #1389 PL-01 (L-56);
  - #1390 PL-02 (L-10);
  - #1391 PL-03 (L-11);
  - #1392 PL-04 (L-52);
  - #1393 PL-05 (L-13).
- **The punch list's generator** now reads `stage-d/bugs.tsv` and `stage-d/audit-issue.txt`. It refuses a bug list that differs from the items proposed as bugs, and the refusal was proved by planting a gap. PL-01's acceptance said *five files*; it is four, corrected in the generator.
- **04:01:25, the audit issue #1394.**
  - Title: `Audit: M6 T38 the skills, agents and settings -- 57 findings (0 critical, 0 high)`.
  - Labels `audit` and `punch-list`, milestone M6.
  - Attached as a sub-issue of #685 by its REST id, and read back.
  - Its body is written from `05` by `stage-d/audit-issue-body.py`: one checkbox per item, in #837's shape.
- **04:02:22, § 4's second question,** `begin-exploration`'s, on #685 as comment `6553169705`, in `04` Q5's shape with what a session sees. Both comments are read back by id, and `02`'s rows cite them (the inherit table, L-22's and L-47's lead rows).
- `04`'s scorecard is re-verdicted at stage D (12 of 22), with its pass rate computed.

PROOF: D-01 (tool-run) -- the five bugs: `1389` to `1393` each `OPEN labels=bug milestone=none`, and #685's sub-issues list `1394` alone (`stage-d/issues-readback.out`, `stage-d/sub-issues-685.out`). A FAIL would have been a bug with a milestone, another label, or attached under #685.
PROOF: D-02 (tool-run) -- `tools/box-check --issue N` on each bug printed `0 fail`, over 3, 3, 2, 3 and 2 open checkboxes (`stage-d/box-check-bugs.out`). A FAIL would have been a checkbox naming a person or a device without its fact.
PROOF: D-03 (tool-run) -- #1394 reads `OPEN labels=audit,punch-list milestone=M6: Codebase renovation`, and `1394 open` under #685's sub-issues. A FAIL would have been a label or the milestone missing, or no parent.
PROOF: D-04 (tool-run) -- `tools/box-check --issue 1394`: `1 issue(s), 57 open checkbox(es), 0 fail` (`stage-d/box-check-1394.out`). A FAIL would have been any checkbox the checker refuses.
PROOF: D-05 (tool-run) -- `tools/lint-audit-artifacts --phase pre-issue --issue 1394`: `rc=0`, `issue #1394 carries a task list (57 items)`, a `references PL-NN` line for each item, `PASS pre-issue artifacts (does not certify resolution)` (`stage-d/lint-pre-issue-1394.out`). A FAIL would have been an item in `05` the issue does not carry.
PROOF: D-06 (tool-run) -- `gh api repos/pixelelated/distribution/issues/comments/<id>` read `6553169705` on #685 and `6553118160` on #807, each with its first line (`stage-d/question-readback.out`). A FAIL would have been an id that does not resolve, or one on the wrong issue.
PROOF: D-07 (tree) -- the `Already written:` reads (`stage-d/checks-bugs.out`): the lint opens no file for writing (`grep rc=1`); `0` records name the stash block; `0` futros, retros or work logs cite another repository's issue comments; the newest release is `rc1-20260929`; the eight earlier Local epic-tier folders each have `pending-lines=0`. A FAIL would have been a record the old sentence left that the fix must migrate.
PROOF: D-08 (tool-run) -- `tools/t38-punch.py` on a copy whose `bugs.tsv` lacks PL-05: `t38-punch: refused: bugs.tsv names ['PL-01', 'PL-02', 'PL-03', 'PL-04'], the items proposed as bugs are [...]`; the real list `rc=0` (`stage-d/punch-refusal-bugs-planted.err`). A FAIL would have been a `05` written with a bug item and no issue.

### [Stage D] census

No build, no compiler, no guest, no fetch, no council run, no Facilitator call, no `tools/council/run`, no `npm install`, no keyed call, no skill invoked against a provider, no held directory opened, and no line in the host file. Nothing was posted on #807, #911, #585 or #346. The tracker writes are the five bugs, #1394 with its sub-issue link, and two comments on #685: the `begin-exploration` question and, after this commit, the pause post. The tree writes are under this folder and `/workspace/tmp/m6-t38/`. Nothing under `.claude/` was edited.
- **The last line of stage D (`date -u` 04:04:03):** `git status --short -- .claude/agents .claude/skills` printed 0 lines.

### [Stage E] 04:49-04:55 — S0 opening: the stream brief read, the dispositions, the helper

- **Stage E was dispatched on #685** as comment `6553579374` (04:49:37 UTC). The stream brief `docs/reviews/briefs/t38-streams.md` at `95052eaf78` (331 lines, sha256 prefix `12962b56d9737c8c`) is read by `git show` into `/workspace/tmp/m6-t38/stage-e/`.
  - The rulings are D-WORKFLOW-219, and the rule lines are swept in `b344408e46` (`2026-11-01T04:29:44Z`).
  - The Backlogs #1395 and #1396 are open, read back by `gh issue view`.
  - The start is the lane's tip `e93c13457e`, with no merge before the hand-back.
- **S0's opening dispositions in `02`:**
  - § The streams: the brief, the pause's inputs, and *Recorded, no stream* for PL-48 and PL-53 to PL-57.
  - § What ... inherit: the swept rule errata name `b344408e46`, with two rows added (`learning-capture.md:67`, the pidfile sentence). L-23, D-QA-040 and L-50 are *open, the coordinator's*. The Backlog row names #1395 and #1396. The questions row carries `begin-exploration`'s answer.
- **The stage-E helper** carries § The rules every stream keeps as a procedure (`learning-capture.md` § 3): `tools/t38-fix.sh` and `tools/t38-rekey.py`.
  - The parent and the staged tree are exported by `git archive`, never a checkout.
  - The allowlists' exact-line entries are re-keyed by their text.
  - The item's check is run on both exports, followed by the checker, `tools/rules-check --quiet` and the wordlist over the added lines.
  - A commit is made only when every expectation holds. Its tree is checked against the tree that was checked, and the record is written to `stage-e/<SN>-<PL>.txt`.
  - Its two refusals were seen first (`stage-e/S0-opening.txt`): no skill file staged gave `rc=2`; a planted line whose parent's count does not match gave `rc=1`, with nothing committed and the allowlists equal to HEAD.
- **Before the first fix:** `git status --short -- .claude/agents .claude/skills` printed `0` lines, and HEAD is `e93c13457e`. The export `/workspace/tmp/m6-t38/e/e93c13457e` was made at 04:54:06 (`stage-e/exports.log`).
- **Census:** no guest, no compile, no keyed call, no council call, no host-file line.
