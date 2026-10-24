# Brief: M6.P2 T4, the binding doctrine (#651)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #651 differ, #651 wins and the
coordinator corrects the brief in the same session. **Version 1
(2026-10-24):** written after T1's, T2's, T3's and T5's briefs had each been
through a futro and a stranger's proof (plan § 3, principle 3), so the
shapes those found wrong -- a count the executor cannot reproduce, a tool
absent from the host, a line number quoted from memory, a command whose
variables do not survive a Bash call, a path that belongs to another slice's
area, a seam described as agreement where the files disagree -- are
answered from the start; it goes through the same two readings before
dispatch, and version 2 records what they found. (The coordinator's own
re-derivation at `8ebaf8daad`, before the futro, corrected ten counts and
four line numbers that version 1's first draft had read from the branch
or from memory; every figure below is now the hash's unless it says
*branch*.) **This slice reads the
rules every other slice obeys**, so its own first act is the pre-flight
every rule asks for, done on the rules themselves. **Each command block
below sets its own variables** (`D`): a Bash call in this harness starts a
fresh shell, only the working directory persists, and the fork's tools are
run by absolute path from `$D`.

## 1. Identity

- **Issue:** #651 `M6.P2 E339/T4: doctrine: the binding doctrine: rules,
  CLAUDE.md, AGENTS.md, the registers`, slice `doctrine-rules` (`k: 4`) in
  `docs/reviews/slices.json`, fourth in `docs/reviews/order.md` (its sizing
  row: `| 4 | the binding doctrine: ... | doctrine | prose | cost against
  value | 36 | 11,414 | 11,414 of prose | 0 | Local |`) (the
  order's argument 4, *How the order was argued*: *"Doctrine and guards too
  late (gemini, claude): Accepted. The binding doctrine is T4 and the guards
  T5"*; the slice's own `why`: *"every session obeys it, and a rule that lies
  is the most expensive cruft (plan § 5); #640's hardcoded host paths live
  here. Early, so the rules every later slice reads are current"*; the
  order's row is on the P1 branch). **Epic:** the area epic for **the
  doctrine** (`doctrine` in `docs/reviews/areas.json`: T4, T38
  `doctrine-skills` #685, T39 `doctrine-reference` #686), filed by the
  coordinator at this slice's dispatch with its futro, under the renovation
  epic #339; the three are re-parented to it and retitled `E<epic>/T<k>`
  (`milestone-phase-naming.md`). **Milestone:** M6; its body holds the live
  order; read it first. **Predecessors:** #346 (the plan), #641 (the survey),
  #644 (the build-path read: four of its 26 findings are this slice's, § 3),
  T1 #648 and T2 #649 (accepted 2026-10-24), T3 #650 and T5 #652 (running).
  **Beside it:** T3 and T5 run in their own lanes (D-WORKFLOW-190); **every
  lane reads the files this slice reads**, and none of them edits a rule
  (D-WORKFLOW-189: a rule change is the coordinator's or, under this slice's
  stream briefs, this lane's). **The coordinator edits rules too** -- a
  paragraph of `generic-x64-vm-testing.md` on 2026-10-24, a blindspot entry,
  friction lines daily -- so § 2's last paragraph sets how the two meet.
  **The dispatch** is the coordinator's comment on #651 that names this
  brief's commit, the model and effort, and says whether a third lane runs
  beside T3 and T5 (the maintainer's call, put on #346 on 2026-10-24); the
  lane's first comment answers it.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, re-order anything, change a criterion, write a
  brief, move the M6 body, edit `slices.json`, `areas.json`, `order.md` or
  the plan, or decide a question of scope: those are the coordinator's,
  reached through #651, one question at a time. **A rule is edited here only
  under a stream brief** (stage E), never at stage B as a reading's
  side-effect, and never a decided register row (append-only,
  `decision-register.md`; a correction is a new row, D-WORKFLOW-013 for a
  clerical one). What this lane does file: its own audit punch-list issue
  (stage D, the code-auditor skill's Phase 6) and a `bug` issue for every
  defect it finds (a rule that lies is a defect, D-WORKFLOW-187; its
  VM-verifiable criterion is the artifact the rule describes, § 5). Nothing
  else.
- **One worktree, one session.** The slice's paths are all in the
  distribution, so the lane holds one worktree: branch
  `feature/m6-doctrine-rules-651` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-rules-651`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** (which carries the P0 branch), with the coordinator's tip
  merged in and the lane's pointer seeded (the two hashes are in the
  dispatch comment on #651). From the dispatch on, one session per worktree
  (D-WORKFLOW-183) and the coordinator writes nothing there. **The rules in
  this worktree are `next`'s except four files** (P1's `fork-workflow.md`
  and `instruction-files.md`; the coordinator's `generic-x64-vm-testing.md`
  paragraph of `8c9b1d4721`; M7's `.claude/skills/council/IMPORTED-FROM.md`,
  not a rule) -- **and this slice reads the rules at `next`'s hash
  `8ebaf8daad` as its bytes** (§ 2), with the four differences recorded as
  the coordinator's unmerged edits, the first of the leads. The primary
  checkout is `/workspace/repos/pixelelated/distribution` on `next`
  (D-INFRA-025). `worktrees.md`, `device-builds.md`, `CLAUDE.md` and
  `AGENTS.md` still name the legacy layout (`/workspace/repos/rocknix`,
  `rocknix.worktrees/`); **#640 owns that drift and this slice is where
  its text lives**: eight files name the legacy paths (§ 2), and what to
  write there is #640's call (the cutover follows the M7 candidate,
  D-INFRA-026), so the finding is recorded with #640 named and the text is
  changed only when #640 says the paths have moved. The legacy checkout and
  every worktree beside it are the M7 lane's: read only. The T1, T2, T3 and
  T5 worktrees beside this one are other lanes': read with `git -C`, never
  write.
- **Model and effort:** Opus 5.5 at high effort (the maintainer, 2026-10-22:
  *"the work will be Opus 5.5"*), unless the dispatch says otherwise.
  Record what actually ran in `00-running-log.md`'s header.
- **Review depth: Local** (plan § 6c: *"a dead-end table, a provenance
  table, a doctrine read -- Local: the executor alone; the lint and the
  counts are the check"*). **No external reviewer, no `npm install`, no
  Facilitator call.** `second-opinions/review-plan.json` is still written
  (`templates.md`: depth `local`, primary `anthropic/claude-opus-5-5`,
  lab `anthropic`, reviewers none, the reason the plan's row), so the lint
  and the hand-back read one shape for every slice. The code-auditor
  skill's Phase 4.6 is recorded as not applicable at Local depth, with the
  plan's row cited; Phase 4.5 (the executor's own finding verification) is
  done in full, and § 5's rule 4 -- what result would have produced a FAIL
  -- is asked of every PASS, because nobody else asks it here.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-rules-651
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-doctrine-rules-651
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md NAMING.md docs/decision-register.md docs/blindspot-register.md docs/friction-log.md   # the files the dispatch names: the coordinator's unmerged doctrine edits since 8ebaf8daad, recorded as the first lead (§ 2); nothing else
git diff --quiet 8ebaf8daad 2174265e9c -- .claude/rules CLAUDE.md AGENTS.md NAMING.md && echo "P1 changed no rule file" || git diff --stat 8ebaf8daad 2174265e9c -- .claude/rules CLAUDE.md AGENTS.md NAMING.md   # P1's two rule edits (fork-workflow.md, instruction-files.md): recorded
ls tools/renovation-inventory tools/renovation-status tools/renovation-drift docs/reviews/inventory.json docs/reviews/slices.json docs/reviews/cross-reference.md   # P1's, present because the branch is stacked on P1
"$D/tools/rules-check"; echo "rc=$?"                                 # every line ok today: the baseline a changed rule is held to
"$D/tools/register-check"; echo "rc=$?"                              # 660 IDs each once on this branch; every citation names a row
"$D/tools/ceremony-check"; echo "rc=$?"                              # what the record owes today (the W42 summary and one checkbox were overdue on 2026-10-24; neither is this lane's)
git push -u origin feature/m6-doctrine-rules-651                     # the lane's own branch
test -f docs/reviews/briefs/doctrine-rules.md || { echo "the brief is not in this tree: stop"; exit 1; }
test -f docs/futros/2026-10-24-m6-doctrine.md || echo "the epic's futro is not in this tree: ask the coordinator before the first audit commit"
cat .github/sessions/saved-session-state-feature-m6-doctrine-rules-651.md   # the lane's seeded pointer
tail -3 /tmp/m7-m6-host-coordination-20261023.txt                   # the host's state: this slice needs no runtime, but the protocol is read
```

The order of the first session: § 3's reading first -- which for this slice
**is** the slice's material, read once as a reader before it is read again
as an auditor -- then stage A.

## 2. Scope

**36 paths, 11,414 lines (numstat; 11,394 by `wc -l`), every one fork-own
prose, every line read.** The
membership is the inventory's, with the slice's one rule of `slices.json`
(`k: 4`): the rows of the `doctrine` area under the globs `.claude/rules/**`,
`CLAUDE.md`, `AGENTS.md`, `NAMING.md`,
`docs/{decision-register,blindspot-register,friction-log}.md`. #651 says the
same set as `--order`'s membership; the filter below is the re-derivation,
because `--order` writes files (and `--slice-issues <dir>` writes
forty-six issue bodies into that directory: never run either in a worktree
you keep). **The tool renders this slice's read count three ways**: the
sizing table in `order.md` says `11,414 of prose`; the same file's § T4
section and #651's body (both from `--order`'s per-slice writer) say
`0 read, of which 0 fork-own` -- the `CODE` language set at
`tools/renovation-inventory` lines 674 to 676 has no `markdown`, so the
per-slice writer counts code lines over prose while the table's writer
knows a prose slice. Here the read set is all 11,414 lines, because a rule
is read whole or not at all; the disagreement is a lead on the tool for
#651's running log (§ 6: a defect in a renovation tool is a lead, not a
fix here).

**The hash.** The slice's bytes are `next`'s at **`8ebaf8daad`** (the hash
every M6 slice has read at; `next` has not moved since the survey).
**`reviewed-at:` is the branch's `HEAD` at stage A**, recorded in
`00-running-log.md` and `01-research-notes.md` § Scope -- and because the
branch carries P1's two rule edits and the coordinator's two
(`fork-workflow.md`, `instruction-files.md`; `generic-x64-vm-testing.md`'s
paragraph, a blindspot entry, friction lines, the registers' new rows), the
read is made **on `8ebaf8daad`'s bytes** (`git show 8ebaf8daad:<path>` for
each of the 36, or a detached read tree the lane makes under
`.qa-scratch/`) and the branch's own differences from that hash are the
first lead, listed hunk by hunk in `01-research-notes.md` § Scope. On
2026-10-24 the coordinator's branch differed from the hash on four of the
36: `generic-x64-vm-testing.md` (+7 at line 1222), `docs/blindspot-register.md`
(+6, entry 74), `docs/friction-log.md` (+13 lines) and
`docs/decision-register.md` (+13 decided rows D-WORKFLOW-181 to 192 and
D-INFRA-025 to 027, +2 open rows D-WORKFLOW-191 and D-SYS-014, and one
existing row, D-QA-040, differing by an `**Open:**` prefix -- the lane finds
whose commit, and whether `decision-register.md`'s append-only contract
allows it); P1's tip differs on two more (`fork-workflow.md` +1/-1,
`instruction-files.md` +4/-1). The lane's branch carries all six. The
stop (§ 8) is a branch whose rule files differ from `8ebaf8daad` in a hunk
the dispatch comment did not name: then something merged under the read
and the coordinator re-baselines.

**The counts, recorded by the survey at `eb4763e3cc` and re-derived here.**
A count that differs is a delta beside the recorded one, not a stop; the
stop is a count that cannot be produced, or two commands for one quantity
that disagree:

```bash
python3 -I - <<'PY'
import json, re, collections
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
globs = [".claude/rules/**", "CLAUDE.md", "AGENTS.md", "NAMING.md", "docs/decision-register.md", "docs/blindspot-register.md", "docs/friction-log.md"]
def gm(p, g): return re.fullmatch(re.escape(g).replace(r"\*\*/", "(?:.*/)?").replace(r"\*\*", ".*").replace(r"\*", "[^/]*"), p) is not None
t4 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "doctrine" and any(gm(r["path"], g) for g in globs)]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t4), "lines", L(t4), dict(collections.Counter(r["tier"] for r in t4)), dict(collections.Counter(r["language"] for r in t4)))
for r in sorted(t4, key=lambda r: -(r["lines"] or 0)): print(r["lines"], r["reach"], r["path"])
PY
git ls-files .claude/rules CLAUDE.md AGENTS.md NAMING.md docs/decision-register.md docs/blindspot-register.md docs/friction-log.md | wc -l                                       # 36 at 8ebaf8daad
git diff --numstat "$(git hash-object -t tree /dev/null)" 8ebaf8daad -- .claude/rules CLAUDE.md AGENTS.md NAMING.md docs/decision-register.md docs/blindspot-register.md docs/friction-log.md | awk '{s+=$1} END {print s}'   # 11414
```

Recorded (the coordinator's reads of 2026-10-24, at `8ebaf8daad`): **36
paths, 11,414 lines by numstat (11,394 by `wc -l`), all fork-own, all
`markdown`, all `reach: n/a`.** Thirty rules (`generic-x64-vm-testing.md`
1,398 lines at the hash, 1,405 on this branch; `rclone-cloud-sync.md` 895,
`engineering-practices.md` 836, `device-builds.md` 695, `es-native-ui.md`
423, down to `least-surprise.md` 40), `AGENTS.md` 351, `CLAUDE.md` 202,
`NAMING.md` 60, and the three registers (`docs/blindspot-register.md` 1,198
lines with 73 entries at the hash -- 1,204 and 74 on this branch, entry 74
the coordinator's of 2026-10-24; `docs/decision-register.md` 728 lines with
644 rows at the hash, 633 decided and 11 open -- 659 on this branch, 660 on
a lane branch with P1's D-WORKFLOW-188, which is what `tools/register-check`
counts; `docs/friction-log.md` 856 lines at the hash, 869 on this branch).
**What loads every session:** 7 rules carry no `paths:` (606 lines) and 17
carry `paths: "**"` (4,573 lines), so **24 of 30 rules, 5,179 lines, load
at every session's start**, plus `CLAUDE.md`'s 202; the six scoped ones
(`change-log.md`, `council-substrate-integrity.md`,
`generic-x64-vm-testing.md`, `handheld-evidence.md`, `packaging-and-patches.md`,
`rclone-cloud-sync.md`; `instruction-files.md` explains the ES four's `**`
and the no-`paths:` seven) load on a matching path; Crush loads all 30
(`instruction-files.md`). That figure is the slice's Q5, and the command
that produced it is § 5's glob listing: read each rule's `paths:` block
whole (a `grep -A3` cut the longer blocks short and mis-classed four `**`
rules as scoped on the first try). **Not in the membership, read only where a rule
points at them:** `.claude/skills/**`, `.claude/agents/**` and the settings
(T38's); `README.md`, `TRADEMARK.md`, `LICENSE.md`, `licenses/**`,
`documentation/**`, `plans/**`, the reference docs under `docs/` (T39's);
`docs/reviews/**` (P0's and P1's, the plan and the order);
`.github/sessions/**` (the `records` area); the tools a rule names
(`tools/**`, T9's, T10's, T14's: a rule's claim about a tool is checked
against the tool, the tool is not read as a finding).

**Where the doctrine runs.** A rule is loaded by Claude Code at session
start (no `paths:`) or when a matching path enters context (`paths:`), and
by Crush whole; it is read by every lane of this program as its pre-flight
(`working-principles.md` § Pre-flight), quoted in every brief's § 3, and
audited by four tools: `tools/rules-check` (front matter, the index in
`instruction-files.md`, the counts in `CLAUDE.md` and `AGENTS.md`,
`AGENTS.md` within Codex's budget and naming every rule; D-WORKFLOW-045),
`tools/register-check` (every ID once, every citation a row),
`tools/ceremony-check` (the friction, retro, weekly, monthly, index,
checkbox and blindspot-guard states, D-WORKFLOW-028) and
`tools/forbidden-terms-check` (the wordlist). The registers are the
records those rules point at: a decision cited by ID, a blindspot named by
number, a friction line that owes an issue within three days. **The
doctrine's consumers are the slices**: the cross-reference's table (P1's
`docs/reviews/cross-reference.md` § Doctrine to area) says 25 to 29 rules
govern each area, so a sentence here is read by every lane that touches
that area, and a wrong one costs each of them the hour the briefs' "known
stale facts" lists were written to save.

**Five groups, read in this order** (a reader before an auditor; the
reader's pass is § 3, the auditor's is stage B). Line numbers are
`8ebaf8daad`'s; each is a lead to re-read, not a verdict:

1. **The entry files**: `CLAUDE.md` (202; the rule table at 25 to 32 under
   *"All 30 of them"* at 22 -- the table names 29: `milestone-phase-naming`
   is absent from it, which `tools/rules-check` did not catch on 2026-10-24,
   the first lead on the counts it keeps; the build commands; the
   architecture; the gotchas -- the fork's "known stale facts": the legacy
   layout at 158, `mkimage` *"needs OS_VERSION/BUILD_DATE exported"* at 88
   (#644's finding 14: only `BUILD_DATE` is honoured and the fork defaults
   it), the ES source's path), `AGENTS.md`
   (351; the Codex-facing twin: rules-check holds it within Codex's budget
   and naming every rule; where it and `CLAUDE.md` say the same thing in
   different words, Q7), `NAMING.md` (60; D-WORKFLOW-144's lowercase
   `pixelelated`, the retired Rasteratops names, #509).
2. **The index and the standard**: `instruction-files.md` (221; the
   front-matter standard, D-WORKFLOW-009; the index of 30 rows; the fork's
   tools table, 72 rows, each tool's rule named -- every row's first tool
   checked against `tools/`, none dangling on 2026-10-24; the ES rules' `**` and
   no-`paths:` reasoning), `working-principles.md` (106; the twelve
   principles as an index, the pre-flight, the enforcement ladder: *"when a
   rule is broken twice, do not rewrite it -- move it up a stage"*, which is
   this slice's own test for every finding), `learning-capture.md` (91),
   `decision-register.md` (99), `ceremonies.md` (116), `issue-tracking.md`
   (208), `milestone-phase-naming.md` (127), `adversarial-council.md`
   (124), `bugs-are-agent-first.md` (91), `vm-first.md` (82),
   `least-surprise.md` (40), `player-language.md` (68), `time-to-play.md`
   (55; **T2's lead**: lines 32 to 42 describe D-CLOUD-076 as what ships and
   D-CLOUD-109 as its replacement, where the code ships D-CLOUD-130 -- the
   rule says both are *"true of different builds"*; the lane reads the
   register's three rows and the code's row and says which build the rule
   describes), `documentation-accuracy.md` (61), `change-log.md` (47).
3. **The engineering rules**: `engineering-practices.md` (836; the fork's
   lanes, D-UI-079; upstream checks; the artifact rules; the watch
   paragraphs; guards fail closed; the device rules; the shell-tool rule --
   one file, how many responsibilities, Q7), `upgrade-and-install.md` (225),
   `fork-workflow.md` (191; P1 added the three renovation tools to its
   personal-paths list; #644's finding 18: it states nothing of upstream's
   freeze period, merge queue, template or artifact links -- T4 writes the
   facts #645 establishes), `worktrees.md` (254; seven legacy-path mentions,
   #640; the layout *"superseded"* per every brief's § 1),
   `device-builds.md` (695; seven legacy-path mentions; the build inventory;
   § Build credentials where #644's finding 3 wants a sentence, T5's),
   `release-candidates.md` (154), `packaging-and-patches.md` (113).
4. **The subsystem rules**: `generic-x64-vm-testing.md` (1,398 at the hash,
   1,405 on the branch: the coordinator's 2026-10-24 paragraph at 1222 is on
   the branch, not at the hash;
   one legacy path; the largest rule by far, Q7's first question),
   `rclone-cloud-sync.md` (895; two mentions of the retired
   `cloud_migrate_layout`, D-CLOUD-175: retired-and-said-so is correct,
   described-as-current is a finding), `handheld-evidence.md` (114; its
   `paths:` globs checked against the tree), `council-substrate-integrity.md`
   (253; adopted verbatim from another estate, refreshed by re-review,
   `instruction-files.md` says: a finding here is a re-review request, not
   an edit), the ES four (`es-native-ui.md` 423, `es-player-text.md` 343,
   `es-ui-style-guide.md` 315, `es-code-traps.md` 254; load every session
   for a repository the globs cannot name; one legacy path in
   `es-code-traps.md`).
5. **The registers**: `docs/decision-register.md` (728 lines, 644 rows at
   the hash, 633 decided and 11 open; append-only; the `Open decisions` table; a reversal is a new
   row; the Q4 question is whether each row a rule cites is the latest on
   its subject), `docs/blindspot-register.md` (1,198; entries 1 to 28 as
   table rows and 29 to 73 as `## N.` headings at the hash, 74 on the
   branch; from 52 on each names a guard that exists, `tools/ceremony-check`
   audits it), `docs/friction-log.md` (856
   lines at the hash; one line per slowdown with `issue: #N` or a guard within three
   days; `tools/ceremony-check` audits that; Q6 and Q7 are its length and
   whether anything reads it but the check).

**Upstream's side of Q4.** The doctrine has no upstream: every path is
fork-own and ROCKNIX carries none of them. Q4 here is **currency against
the fork's own code and register** (§ 4): a rule that names a tool, a
path, a command, a count or a decision is current when the tool exists
with those options, the path exists, the command runs as written, the
count is true today and the decision is the latest row on its subject.
**The closed `bug` issues** that name a rule file are Phase 1's: `gh issue
list --repo pixelelated/distribution --label bug --state closed --limit 500
--json number,title,body`, grepped for `.claude/rules/` and each rule's
name (the count depends on the pattern, so record the pattern with the
count).

**The branch scan**, by one predicate: a branch is *ahead* of `next` on the
membership when `git log --oneline next..<branch> -- <the 36 paths>` prints a
line. **Every M6 lane branch is**, because every lane appends to the
registers and the friction log and the coordinator's branch edits rules;
list them with their rule-file hunks (the registers' appends are theirs by
design and are not findings; a rule edit on a lane branch other than the
coordinator's is a finding, D-WORKFLOW-189). The M7 lane's branches too
(`legacy/` and `origin/feature/m7-*`: its register rows 171 to 180 and its
rule edits, if any, are listed and left alone).

**The coordinator's rule edits during this slice.** The coordinator's
branch is where rules change between slices (a paragraph from a lane's
retro, a blindspot entry, a correction). **From this slice's stage A to its
stage D the coordinator posts every rule edit on #651 the day it is made**,
with its hash, and makes none that this slice's punch list would make
differently without asking here first; the lane records each as a delta
beside its read at `8ebaf8daad` and re-baselines its findings over them at
stage D (plan § 8's shape). A lane's register row or friction line is not a
rule edit and is not posted. At the merge, this branch's rule edits land
after the coordinator's (the merge order, § 10), so a conflict is resolved
in the coordinator's favour and the slice's edit re-applied over it.

**Drift.** `next` is `8ebaf8daad` and has not moved since the survey; the
M7 candidate's merge will move it, and it carries doctrine edits of its own
(the M7 lane's register rows 171 to 180; any rule it changed). When `next`
moves, the coordinator merges `next` into this branch -- never between
stage A and stage D -- and after stage D re-baselines the slice over the
diff, recorded on #651. `tools/renovation-drift` is the coordinator's at
every slice close; this lane runs it to read, never to write.

## 3. Read first

For this slice the reading list **is the material**, read first as any
lane reads it (the pre-flight, `working-principles.md`) and then again as
the auditor. So:

- `.github/sessions/saved-session-state-next.md` (the M7 lane's canonical
  checkpoint; read for what runs on this host, not for a work queue) and
  this lane's own pointer.
- **The 36 files, in the order of § 2's five groups**, at `8ebaf8daad`,
  once through, before any note is taken. The reader's pass records only
  what a stranger stumbled on (a sentence read twice, a command not
  understood, a path looked for); the auditor's pass is stage B.
- The code-auditor skill whole: `.claude/skills/code-auditor/SKILL.md` and
  its `references/phases.md`, `review-levels.md` (Local: *"the executor
  alone"*), `templates.md`, `anti-patterns.md`. The slice runs under its
  lifecycle with the renovation face added (plan § 6b); stage B's Phase 2
  criteria are #651's checklist, and Phase 3 carries § 4 below as its
  renovation face beside the skill's own faces.
- **`docs/reviews/build-path-read.md`** (#644): its findings **2** (the
  fork's build documentation is the accurate one: keep), **5** (`CLAUDE.md`
  and `device-builds.md` already say the entry points enter the watcher;
  T9 checks the refusal message), **14** (correct `CLAUDE.md`'s
  `OS_VERSION/BUILD_DATE` sentence: only `BUILD_DATE` is honoured and the
  fork defaults it) and **18** (write upstream's PR facts into
  `fork-workflow.md` -- the `bugfix` label in a month's last seven days, the
  merge queue, the template with its AI disclosure, the artifact links --
  once #645 has established them) are this slice's rows; the other
  twenty-two are named with their carriers so none is taken here.
- **The other slices' briefs** (`docs/reviews/briefs/*.md`) § 1 and § 3,
  for their *"known stale facts"* lists: each is a doctrine finding already
  made by a reader who paid for it -- the legacy paths (T1, T2, T3, T5),
  `tools/es-syntax-check`'s default root (#699), `tools/retroarch-wrapper-test`'s
  roots (#799), the dash-not-bash line (T1's brief, corrected), the ES
  pointers' paths. **T2's retro** (`docs/retros/2026-10-23-m6-es-launch-path.md`
  on the T2 branch at `7041b0d710`) names `time-to-play.md` as *"doctrine
  drift, not this lane's to fix"* and hands it to the coordinator: it is
  this slice's. **T1's retro** (`docs/retros/2026-10-24-m6-os-launch-control-state.md`
  at `d3aa6a19c5`) recommends two rule lines (the `time-to-play` reboot,
  now on the coordinator's branch; the harness refusing to run as a copy,
  #797) and names `001-functions`' `PATH` and `system.cfg`'s no-comment
  rule as facts a rule should carry.
- `docs/blindspot-register.md` whole, once (74 entries) -- it is the
  material, group 5 -- and then the entries that touch doctrine itself:
  **13** (assumed done), **30** (a resumed session built on its own
  summary), **46** (a name read as a behaviour), **51** (an open checkbox is
  a claim), **52** (four "pending decisions" put to the maintainer that the
  record had settled: `tools/archaeology` is its guard), **73** (a monitor
  of completion, not activity), **74** (a fixture that did not engage);
  and D-UI-039's lesson in `working-principles.md` § Enforcement depth (a
  rule that asked for the menu map to be updated lost 30 screens in a
  month until a tool checked it): **a finding here is graded by whether a
  tool could catch it**.
- Prior audits under `docs/audits/` as provenance only: which rule files
  were touched by a punch item, when (`grep -c -E '\.claude/rules/|CLAUDE\.md|AGENTS\.md|decision-register|blindspot-register|friction-log' 05-punch-list.md`
  per folder, the count recorded with the command); read after stage B's
  own Phase 2, never transcribed (plan § 7 item 3).
- Decisions by ID, cited and never re-argued -- **the ones about the
  doctrine itself**: D-WORKFLOW-007 and D-WORKFLOW-008 (the style guide a
  rule; the native-UI split), D-WORKFLOW-009 (the front-matter standard),
  D-WORKFLOW-010 (one rule corpus; the ES pointers), D-WORKFLOW-013 (a
  clerical register fix), D-WORKFLOW-028 (the ceremony state machine),
  D-WORKFLOW-045 (`tools/rules-check`), D-WORKFLOW-050 (*Already
  written*), D-WORKFLOW-061 (the wordlist outside every tree), D-WORKFLOW-083,
  D-WORKFLOW-102, D-WORKFLOW-132 (no work without an issue), D-WORKFLOW-133
  (the stash), D-WORKFLOW-139 (the milestone body), D-WORKFLOW-144
  (`pixelelated` lowercase), D-QA-012 (out-of-band requests become issues),
  D-QA-044 and D-QA-045 (agent-first criteria; *checkbox*, not *box*),
  D-QA-051 (bugs are agent-first), D-UI-039 (the menu map in the same
  change), D-UI-042 and D-UI-045 (least surprise; player language),
  D-INFRA-025 and D-INFRA-026 (the fresh clone; the cutover's timing),
  D-CLOUD-175 (the migration flows retired), D-CLOUD-076, D-CLOUD-109 and
  D-CLOUD-130 (the launch-over-sync question's three rows, T2's lead). The
  program: D-WORKFLOW-181, 183, 184, 185, 186, 187, 188 (on the P1 branch),
  189, 190, 192; D-WORKFLOW-137 (depth), D-WORKFLOW-162, 164, 165. **Every
  ID cited in the 36 files** is the Q4 table (§ 4), so the list above is
  the reading's start, not its extent.
- Issues whose bodies name these files, read for the planned changes and
  the known leads, not as a work queue. **Open:** #640 (the legacy paths:
  the cutover after the M7 candidate; this slice records, #640 edits),
  #644 and #645 (the build-path read; upstream's PR rules for
  `fork-workflow.md`), #696 (a pre-commit check for conflict markers,
  Backlog: the rule `worktrees.md` states by hand), #699, #799, #801 (three
  fork tools whose defaults or runners decayed: the shape a rule about
  tools should carry), #797 (the harness says when a fixture did not
  engage; a rule line may follow), #796, #585 (the upstream contribution
  queue), #509 (the remaining Rasteratops names, `NAMING.md`'s), #346,
  #339, #648, #649, #650, #652 (the lanes: their briefs' stale-facts lists).
  **Closed, read for their history on these files:** #147 (the 2026-09-12
  sweep that split the ES rules and found two `docs/` documents nobody
  loaded), #367 and #368 (the stale-worktree rules; the stranger's
  briefing), #646 (a register row appended under the wrong heading),
  #312's history (the wordlist). Every `gh` call carries `--repo
  pixelelated/distribution`.

## 4. The questions

All seven apply (plan § 4); none is struck, though Q4 and Q5 take the
shapes a prose corpus allows. Every path is fork-own, so every path gets
all seven in full. Per file, the evidence that answers each:

| # | Question, for this slice | Evidence |
| --- | --- | --- |
| Q1 Modernize | A rule written against a mechanism the tree has retired or replaced: the legacy layout (`/workspace/repos/rocknix`, `rocknix.worktrees/`; eight files, #640); the launch-over-sync behaviour (`time-to-play.md` on D-CLOUD-076/109 where D-CLOUD-130 ships); a cloud flow D-CLOUD-175 retired (`cloud_migrate_layout` and the join/follow flows) described as current anywhere; a tool invoked with options it no longer has or from a root it no longer has (`es-syntax-check`, #699); a count that was true when written (`"30 rule files"`, `"73 entries"`); a command sequence upstream's docs changed under (#644 finding 14) | the register row or commit that retired it, cited; the tool's `--help` or header beside the rule's sentence; the count recomputed |
| Q2 Standards | The doctrine's own standards, applied to the doctrine: the front-matter standard (D-WORKFLOW-009: `description` one line and first, `paths:` justified, a no-`paths:` rule says so in its first paragraph), the index complete (`instruction-files.md`), `AGENTS.md` within Codex's budget and naming every rule (D-WORKFLOW-045), the registers' contracts (append-only, one row per decision, IDs once, citations resolving; a blindspot from 52 on naming a guard that exists; a friction line owning an issue within three days), the vocabulary rules a rule itself must obey (`checkbox` not `box`, D-QA-045; `pixelelated` lowercase, D-WORKFLOW-144; *back up* / *backup*, the serial comma -- `tools/vocabulary-check` reads strings, not rules, so this is read); the heading shape `tools/archaeology` relies on (a work-log heading names the issue and the thing) | `tools/rules-check`, `tools/register-check`, `tools/ceremony-check` run and their lines recorded; the standard's section cited beside each miss |
| Q3 Bugs | **A rule that lies**: a path that does not exist, a command that does not run as written (its tool missing, its option gone, its default root retired, its variable unset in that block), a number that is wrong today, a cross-reference to a section that moved or never said that (T5's version 1 cited `es-code-traps.md` § The picture... for a thing it does not say: the shape), two rules that contradict each other, a rule and the code it describes disagreeing (`time-to-play.md`; `CLAUDE.md`'s `OS_VERSION`), a rule that promises a tool enforces something the tool does not check (`working-principles.md`'s ladder: *"an unenforceable rule that claims enforcement is worse than an honest one"*) | the artifact: `test -e` the path, run the command (where it runs on the host) or check the tool's options, recompute the number, read the section, read the code; every finding a `bug` with the artifact that proves the lie and the one that will prove the fix |
| Q4 Currency | Against the fork's own record and code, not an upstream: **(a) every decision ID cited in the 36 files** (`grep -oE 'D-[A-Z]+-[0-9]+' <the 36> \| sort -u`) with its row's state -- decided, open, or **superseded** by a later row on the same subject (the register's own *reversal cites the old ID* convention: `grep -n '<ID>' docs/decision-register.md` finds the citing rows; a rule citing a superseded row as current is a finding, `tools/archaeology --reversal` the sweep); **(b) every tool named** in the 36 files against `tools/` and `.githooks/` (exists; the options and defaults the rule states are the tool's today); **(c) every count** a rule states about the tree (rules, entries, tools, screens, packages) recomputed; **(d) every path** named (`test -e`, with the legacy ones named for #640 rather than failed) | one table per sub-question in `04`, with the commands; the counts of each class (cited IDs, superseded, tools named, missing, counts stated, wrong, paths named, absent) |
| Q5 Efficiency | What the doctrine costs a session and a lane: **5,179 lines of rules plus `CLAUDE.md`'s 202 load at every Claude Code session** (24 of 30 rules), all 11,394 under Crush; per rule, its lines against the number of areas its `paths:` reach (cross-reference § Doctrine to area: 25 to 29 rules per area) and the number of sessions that need it (an every-session rule read by a lane that never touches its subject is cost without value, plan § 5's lens); the registers' growth (659 rows, 869 friction lines) against what reads them (`tools/archaeology`, `tools/register-check`, the maintainer); the pre-flight's hour every brief budgets. **This slice does not touch time to play**: the retro says so in those words | the line counts and the glob reach per rule, in a table; a proposal to narrow a glob or split a rule is a Q5/Q7 `Renovation` item with its reader cost stated, decided by a stream brief, never applied at stage B |
| Q6 Dead ends | A rule whose `paths:` glob matches no tracked path (`git ls-files <glob>` empty: a rule that never loads); a section describing a flow, a tool or a device the tree no longer has (the retired migration flows, D-CLOUD-175; a tool table row with no tool -- none on 2026-10-24; `handheld-evidence.md`'s and `change-log.md`'s globs); a decision row cited by no document and reversed by none (not a defect: a record); a blindspot entry whose guard no longer exists (`tools/ceremony-check` audits from 52 on; 1 to 51 are read here); a friction line past three days with neither issue nor guard (`tools/ceremony-check` audits); a rule section that only restates another rule (`working-principles.md` is the deliberate index; a second copy elsewhere is the finding) | the reachability table in `04` Q6: one row per rule (30) with its `paths:` match count, one per tool table row (72) with `test -e`, one per retired-flow mention, one per blindspot guard (73 at the hash, 74 on the branch), one per friction line owing an issue (the check's output); every row marked unreached or dead carries an `Already written:` line -- for a rule, what the sessions that read it already did on its strength |
| Q7 Clarity | Can a reader new to it tell what each rule decides and when to open it in one pass: the `description` line against the body; one responsibility per file (`engineering-practices.md` at 836 lines and a dozen sections; `generic-x64-vm-testing.md` at 1,405; `device-builds.md` at 695); copies of the same instruction in `CLAUDE.md`, `AGENTS.md` and a rule, and whether each copy says the same thing (the counts, the paths, the build commands); the ES four's boundaries after the split (D-WORKFLOW-008); headings `tools/archaeology` can find; a sentence a stranger read twice (the reader's pass) | the specific sentence or section named with what a reader stumbled on; a duplicate named with its original and the diff of their words |

A finding is one question with its evidence; severity and category are the
code-auditor's, with `Renovation` as the category for Q1, Q5, Q6 and Q7
items that are not defects. **A Q3 finding -- a rule that lies -- is also a
`bug` issue** (D-WORKFLOW-187), because a lane will act on the lie: its
criterion names the artifact the corrected sentence describes
(`bugs-are-agent-first.md`: the VM is not the bench for prose; the tree,
the tool and the register are, and the criterion says which).

**The ladder, applied to every finding (`working-principles.md` § Enforcement
depth).** For each item the punch list says which stage the rule sits at --
written, routed, evidenced, audited, self-examining -- and whether a tool
could hold it at the next stage. A rule found wrong twice in the record (a
friction line, a brief's stale-facts list, a retro) is proposed for the
tool, not the rewrite; a rule nothing can check says so in its own words.
That is the slice's one design rule, and the stream briefs honour it.

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict, as its `SKILL.md`
§ Evidence floor lists them:

1. *Tracker state is never sole evidence.* Every PASS cites a primary
   artifact: the tree (`test -e`, `git ls-files`, `git show 8ebaf8daad:<path>`),
   a tool's run, a register row, a commit.
2. *Mechanical evidence outranks reading.* The four doctrine tools are run
   and their lines recorded; a claim a tool checks is proven by the tool,
   not by reading the tool.
3. *Run it on a device, not on the host.* **For prose, the target is the
   thing the sentence describes**: a tool (run its `--help` or the command
   as written where it runs on the host; a guest recipe is checked for its
   tool's existence and options, not run -- this slice brings up no guest
   unless a Q3 finding needs the guest's answer, and then T3's brief § 5
   gives the recipe with this lane's ports, SSH 10036 and VNC display 23,
   and the host window protocol applies), a path (`test -e`), a count
   (recomputed), a decision (the register), a behaviour of the code (the
   code's line, `git log -S`, or the other slices' audits that read it).
   Host reasoning about what a rule *means* is a lead; what the rule
   *names* is checkable.
4. *An assertion that cannot fail is not evidence.* Before recording a PASS,
   ask what result would have produced a FAIL -- at Local depth nobody else
   asks it.
5. *Subagent output is a LEAD, never EVIDENCE.* Fan-out inside this lane is
   read-only research subagents only (D-WORKFLOW-183), and for this slice
   a reader with no context is the right subagent: the stranger's pass
   over a rule (*"what would you have had to ask?"*) is this slice's own
   method, as every brief's stranger's proof was.

**What runs on the VM, and how.** Can this be done on the VM? **No, for
nearly all of it** -- the slice is prose about the tree, the tools and the
record, and its bench is the host's tree and tools. The exception is a
sentence about the guest (`generic-x64-vm-testing.md`'s recipes,
`vm-first.md`'s list of what the guest cannot have) whose truth a guest
would show: checked against the tools' options and the other slices' VM
cycles (`docs/vm-qa-log.md`) first, and brought to a guest only for a Q3
finding that nothing else can settle, under the host protocol. Nothing in
this slice touches a handheld, a person's cloud, a shared QA backend, or a
QA guest another lane owns.

- **The host handoff is a wait, not a stop.** The agreement in
  `/tmp/m7-m6-host-coordination-20261023.txt` holds for this lane as for
  every M6 lane; this slice expects to need none of the host's runtime, so
  a window costs it nothing and the first commands read the file for the
  protocol alone.
- **The reads at the hash.** The 36 files are read at `8ebaf8daad`
  (`git show 8ebaf8daad:<path>`, or a detached read tree under
  `.qa-scratch/t4/at-hash/` made with `git archive 8ebaf8daad <the 36>
  | tar -x -C ...`), so the branch's own edits (P1's, the coordinator's)
  do not colour the read; the deltas are the first lead.
- **The host-side checks**, each run and its command, exit status and
  summary line recorded in `02-forward-audit.md`; a check that cannot run
  is recorded as such, never as a pass (each block sets its variables; the
  tools are `$D`'s, by absolute path):
  ```bash
  D=/workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-rules-651
  cd "$D"; mkdir -p .qa-scratch/t4
  "$D/tools/rules-check" > .qa-scratch/t4/rules-check.out 2>&1; echo "rc=$?"; grep -c '^ *ok' .qa-scratch/t4/rules-check.out; grep -vc '^ *ok' .qa-scratch/t4/rules-check.out      # every check and its verdict; the counts of ok and not-ok
  "$D/tools/register-check" > .qa-scratch/t4/register-check.out 2>&1; echo "rc=$?"; tail -1 .qa-scratch/t4/register-check.out                                           # 660 IDs each once; every citation a row
  "$D/tools/ceremony-check" > .qa-scratch/t4/ceremony-check.out 2>&1; echo "rc=$?"; grep -E 'DUE|overdue|ok ' .qa-scratch/t4/ceremony-check.out | head -20             # what the record owes today, and whose
  "$D/tools/forbidden-terms-check" > .qa-scratch/t4/forbidden.out 2>&1; echo "rc=$?"; tail -1 .qa-scratch/t4/forbidden.out                                              # 0 hits; the wordlist itself is never read
  "$D/.githooks/hooks-test" > .qa-scratch/t4/hooks-test.out 2>&1; echo "rc=$?"; tail -1 .qa-scratch/t4/hooks-test.out                                                    # the guards' own proof
  "$D/tools/box-check" > .qa-scratch/t4/box-check.out 2>&1; echo "rc=$?"; tail -1 .qa-scratch/t4/box-check.out                                                           # D-QA-044 over every open issue (a GitHub read of every open issue; minutes, not seconds)
  git ls-files '.claude/rules/*.md' | while read f; do awk '/^---$/{c++; next} c==1' "$f" | awk '/^paths:/{p=1; next} p && /^ *- /' | grep -oE '"[^"]+"' | tr -d '"' | while read g; do printf '%s %s %s\n' "$(basename "$f")" "$g" "$(git ls-files "$g" | wc -l)"; done; done   # every paths: glob against the tree, the whole block (never grep -A: the long blocks run past it): a 0 is a rule that never loads; 7 rules print nothing (no paths: key), 17 print one `**` line
  grep -ohE 'D-[A-Z]+-[0-9]+' .claude/rules/*.md CLAUDE.md AGENTS.md NAMING.md | sort -u | wc -l                                                                           # the IDs the rules cite (Q4 a); each is then looked up in the register for its state
  grep -oE '^\| `[a-z0-9/_-]+`' .claude/rules/instruction-files.md | tr -d '|` ' | while read t; do [ -e "tools/$t" ] || echo "MISSING tools/$t"; done                   # the tool table's 72 rows against tools/, first tool of each row (the character class has no dot, so the rule-index rows do not match; a row naming several tools is checked by hand); none missing on 2026-10-24
  grep -c 'repos/rocknix\|rocknix\.worktrees' .claude/rules/*.md CLAUDE.md AGENTS.md | grep -v ':0$'                                                                       # the legacy paths, #640's (8 files on 2026-10-24: es-code-traps 1, device-builds 7, fork-workflow 3, CLAUDE.md 1, instruction-files 2, AGENTS.md 2, generic-x64-vm-testing 1, worktrees 7)
  ```
  - **every command block in the 36 files** is a Q3 case: run where it runs
    on the host without a build, a guest, a device or a cloud (a `git`
    command, a `tools/` invocation's `--help`, a `grep`), or checked for
    its tool's existence and options where it does not (a build, a guest
    recipe, a device command); the table in `02` lists each block with its
    file:line, what was done, and the verdict;
  - **`tools/archaeology --reversal '<old words>'`** for each reversal the
    register records since a rule's last edit (the rows that cite an
    earlier ID as reversed), its output the sweep list for Q4 (a);
  - **a reader with no context** (a read-only subagent, rule 5) given one
    rule at a time and asked what it would have had to ask: the questions
    are Q7's leads, re-read by the lane before any becomes a row;
  - of `tools/vm-qa`'s suites, none is this slice's; record that in `02`.
- **A read is free and goes through the filter.** Nothing in the 36 files
  carries a credential, and nothing this slice reads elsewhere is a config
  or a log; the filter (`grep -v -i -E 'key|pass|token|user|psk|login'`)
  applies if a Q3 check ever reads a tool's output over a config. **The
  wordlist** (`~/.config/rocknix/forbidden-terms`) is never read, listed or
  quoted (D-WORKFLOW-061): `tools/forbidden-terms-check` is its only reader.

**What never runs in this slice:** a build of an image or a package; a
guest, unless a Q3 finding needs it and the protocol allows; a command on a
handheld, a person's cloud or a shared QA backend; a model call outside
`tools/council/run` (and none is expected: Local depth); `npm install`
(not needed); an edit to any rule, `CLAUDE.md`, `AGENTS.md`, `NAMING.md` or
a register **at stage B** (a reading's finding is a row, the edit waits for
its stream brief); an edit to a decided register row ever (append-only; a
correction is a new row); a blindspot entry without a guard that exists;
`--no-verify` on any push; bare `git stash`; `git worktree remove --force`
or `rm -rf` of any worktree; a write under `/workspace/repos/rocknix` or
any `rocknix.worktrees/*`, or in another lane's worktree; an edit to
`.github/sessions/saved-session-state-next.md` (the M7 lane's); a change to
`docs/reviews/order.md`, `slices.json`, `areas.json`, the plan, the brief,
#651's criteria or the M6 body (the coordinator's, D-WORKFLOW-189); a text
change for the legacy paths before #640 says the paths have moved; a
GitHub issue other than the audit punch-list issue and `bug` issues (§ 1).

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#651`
(`Refs #651` while any criterion is open, never a closing keyword); the
stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-doctrine-rules/00-running-log.md` | the skill's append-only flight recorder, opened first: the model and effort that ran, `reviewed-at` (the branch `HEAD` at stage A) with `8ebaf8daad` beside it and the branch's doctrine deltas listed, every command with its exit status and time, each stage's entry; **every check that stands as a proof announced on a line that begins `PROOF:`** with its time and its command, the token criterion 12 counts | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 36 paths re-derived with the filter of § 2, the two counts, the always-loaded figure, the branch's deltas from `8ebaf8daad` hunk by hunk (P1's two, the coordinator's), the branch scan (every lane branch ahead on the registers by design; any rule edit outside the coordinator's named); § The reader's pass: what a stranger stumbled on, file by file, before any auditing; § Phase 1: the closed bugs grep with its pattern and count, the prior audits' counts per folder, the other briefs' stale-facts lists collected into one table with each fact's owner | A, B |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #651's checklist, plus a **coverage table with one row per path** (36 rows; the first cell the path in backticks, so ``grep -c -E '^\| `(\.claude/rules/|CLAUDE\.md|AGENTS\.md|NAMING\.md|docs/)' 02-forward-audit.md`` prints 36; then group, lines, loads-when, Q1 to Q7 each answered or `n/a` with the reason); § Mechanical checks (every check of § 5 with command, exit status, summary); § Command blocks (every block in the 36 files with its verdict); § The four #644 findings (2, 5, 14, 18 with their dispositions) and T2's lead; § Proofs (each with its `proved:` cell, below) | B onward |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5's interaction audit for the seams § 2 names (`CLAUDE.md` x `AGENTS.md` x the rules on the same facts; the ES four x `docs/es-menu-map.md` and `docs/conflict-wizard-ia.md`, which load nowhere; the registers x the tools that read them; `time-to-play.md` x the register's three rows x the code; the briefs' stale-facts lists x the rules they name) and the futro's predictions checked | B |
| Analysis | `.../04-analysis.md` | Phase 4, then § Finding Verification (4.5, in full: Local depth has no other reviewer), then **§ Renovation face** with one subsection per question Q1 to Q7 (the lint requires all seven), **Q4 carrying the four currency tables** (the cited IDs with their state; the tools named with their existence and options; the counts stated with the recomputation; the paths named with `test -e`), Q5 the load table, Q6 the reachability tables, Q7 the duplicates with their diffs; § Second opinions reads *not applicable at Local depth (plan § 6c)* | B, C |
| Second opinions | `.../second-opinions/review-plan.json` | depth `local`, primary `anthropic/claude-opus-5-5`, lab `anthropic`, reviewers `[]`, the plan's § 6c row as the reason; no call, no provenance file | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | prints `PASS pre-issue artifacts (does not certify resolution)`; recorded in the running log | C to D |
| Punch list | `.../05-punch-list.md` | Phase 5, every item with `question: Q1..Q7` (or `none` with a reason), severity, category (`Renovation` where it is not a defect), where (file:line at `8ebaf8daad`), acceptance, **and the ladder stage the rule sits at with the tool that would hold it at the next** (§ 4); the YAML `punch_index` (`templates.md`); an item that is #640's marked `deferred:#640`; an item that is a tool's (#699, #799, #801, #797) marked for that issue; a reversal sweep marked with its register row; a rewrite proposed where the ladder says a tool should hold it marked `Renovation` with the tool named | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #651 | `Audit: M6 T4 the binding doctrine -- N findings (X critical, Y high)`; one checkbox per item, each agent-verifiable (D-QA-044); `tools/box-check --issue N` run on it and its line recorded | D |
| Bug issues | GitHub, label `bug`, title `Bug: ...` (`milestone-phase-naming.md` § Reactive), milestone-less and not sub-issues | one per rule that lies (D-WORKFLOW-187, D-QA-051): the code trace shape (`release-candidates.md` step 0) with *the sentence* as the defect's source and *the artifact it misdescribes* as the evidence, the `Can this be done on the VM?` line answered honestly (*No -- the tree, the tool or the register shows it*), a criterion naming the artifact the corrected sentence must match, `Already written:` (what sessions already did on the sentence's strength) | D |
| **The stage-D pause** | #651 | the punch list posted on #651 with the audit issue's number and the `bug` issues' numbers; **the lane waits** while the coordinator writes one remediation brief per stream of related items (plan § 6b stage E: the D-WORKFLOW-056 shape, the files owned, the test first -- for a rule, the check that fails today and passes after -- the `Already written:` line, commits cut from intermediates only after `rules-check` and `register-check` pass; D-WORKFLOW-189) | D to E |
| Remediation | the branches the stream briefs name | each stream as its brief specifies: a rule edit with its failing check first where a tool checks it (`rules-check`, `register-check`, a `test -e`, a recount), the `description` still one line, the index and the counts kept true, the French of any player string untouched (none here); a new register row for a decision a stream forces, never an edit to a decided one; a blindspot entry only with its guard; a tool proposal filed as an issue, not built here | E |
| Verification | `02-forward-audit.md` appended; `.../audit-completion.json` | every claim proven where the tree, a tool or the register can show it; every proof's row carries a `proved:` cell with one of `tree` (a path, a count or a section read from the tree at the hash), `tool-run` (`rules-check`, `register-check`, `ceremony-check`, `archaeology`, `forbidden-terms-check`, `hooks-test`, `box-check`), `history` (`git log -S`, `git blame`, a register row), `fix-tree` (a rule edit proven by the check that failed before it and the artifact the sentence now matches), `fix-pending-session` (a rule whose only proof is a later session acting on it: the coordinator reads it at the next lane's stage A and says so on #651); the Phase 7 gate in `05` | F |
| Retro | `docs/retros/<yyyy-mm-dd>-m6-doctrine-rules.md`, and the same text as a comment on #651 | the mini-retro skill's four answers with its scoped audit, in Instruction-Recommendations mode (plan § 6b G); findings that recur become a rule edit, a tool, a blindspot entry; **what the slice did to the two time-to-play numbers** (nothing, said in those words) | G |
| Hand-back | #651 | `reviewed-at:` and `fixed-at:` written into #651's body by the executor; one comment naming the branch tip and each artifact by path, the six checker exit codes, and per fix its `proved:` class | H |
| Lane pointer | `.github/sessions/saved-session-state-feature-m6-doctrine-rules-651.md` | seeded by the coordinator; the executor updates it at every checkpoint | every checkpoint |
| Work log | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session, headed `#651` and the thing decided or learned | every session |

Neither `tools/renovation-status` nor `tools/renovation-drift` nor
`tools/renovation-inventory` is run to write ledgers or edited here; a
defect in one is a lead on #651.

## 7. Acceptance

The checklist on #651 is the contract. Its first five items are plan § 6b's
contract for every slice; the rest are this slice's, written by the
coordinator with this brief (D-WORKFLOW-189). Each names the artifact that
ticks it; the coordinator ticks them at hand-back from the artifacts, not
from this lane's word.

- [ ] `docs/audits/<date>-epic-m6-doctrine-rules/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-doctrine-rules/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included: Q1 to Q7 answered in `04-analysis.md`, and every punch item's `question:` in the index.
- [ ] `second-opinions/review-plan.json` records Local depth with no reviewer and the plan's § 6c row as the reason (plan § 6c, D-WORKFLOW-137).
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue, or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits the read and the fixes were made at (the read made on `8ebaf8daad`'s bytes with the branch's doctrine deltas listed; no EmulationStation path here, so no `fixed-at-es:`), and, after the coordinator closes this issue and the branch merges to `next`, `tools/renovation-status` lists this slice as `closed` (the coordinator's regeneration).
- [ ] `01-research-notes.md` § Scope records the read hash `8ebaf8daad`, the filter of brief § 2 with its output (36 paths, 11,414 lines, all fork-own markdown, or the deltas beside them), the always-loaded figure (24 of 30 rules, 5,179 lines plus `CLAUDE.md`'s 202, recomputed), the branch's doctrine deltas from the hash hunk by hunk with their owners, and § The reader's pass with at least one line per file.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path, the path in backticks as the first cell: ``grep -c -E '^\| `(\.claude/rules/|CLAUDE\.md|AGENTS\.md|NAMING\.md|docs/)' 02-forward-audit.md`` prints 36; each row's Q1 to Q7 cells answered or `n/a` with a reason.
- [ ] `02-forward-audit.md` records, with command, exit status and summary line, each of: `tools/rules-check`, `tools/register-check`, `tools/ceremony-check`, `tools/forbidden-terms-check`, `.githooks/hooks-test`, `tools/box-check`, the `paths:` glob match counts for all 30 rules, the cited-ID count, the tool-table existence check and the legacy-path count; and § Command blocks lists every command block in the 36 files with its file:line and a verdict (run and passed, run and failed, checked for its tool's existence and options, not runnable here with the reason) -- a check that could not run is recorded with the reason, never as a pass.
- [ ] `02-forward-audit.md` § The four #644 findings carries one row each for 2, 5, 14 and 18 with the disposition brief § 3 names and what the reading found, one row for T2's `time-to-play.md` lead with the register's three rows and the code's behaviour named, and names the other twenty-two #644 findings with their carriers so none is taken here.
- [ ] `04-analysis.md` § Renovation face Q4 carries the four currency tables: (a) every decision ID cited in the 36 files with its row's state (decided, open, superseded by a named later row); (b) every tool named with its existence and whether the options and defaults the rule states are the tool's today; (c) every count a rule states about the tree with the recomputation; (d) every path named with `test -e`, the legacy ones marked `#640` rather than failed; with the four class counts.
- [ ] `04-analysis.md` § Renovation face Q5 carries the load table (per rule: lines, `paths:`, loads every session or on a match, areas reached per the cross-reference) with the always-loaded total, and names the two time-to-play numbers as untouched by this slice.
- [ ] `04-analysis.md` § Renovation face Q6 carries the reachability tables of brief § 4 (30 rules with their glob match counts; the tool table's 72 rows; every retired-flow mention; the 73 blindspot guards at the hash and the branch's 74th; the friction lines the check names), each with its command and output; every row marked unreached or dead carries an `Already written:` line.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `tool-run`, `history`, `fix-tree` or `fix-pending-session` (§ 6, Verification); ``grep -c 'proved:' 02-forward-audit.md`` equals ``grep -c '^PROOF:' 00-running-log.md`` (the convention of § 6).
- [ ] Every punch item carries the ladder stage its rule sits at and the tool that would hold it at the next stage, or the words *no tool can*; every item whose `punch_index` entry carries a `tracked: "#N"` has that `bug` issue naming the sentence, the artifact it misdescribes and the artifact the corrected sentence must match; no rule, `CLAUDE.md`, `AGENTS.md`, `NAMING.md` or register line is changed on this branch before a stream brief (`git diff --stat 8ebaf8daad <fixed-at> -- <the 36>` shows only stage-E commits and the registers' appends); `tools/box-check --issue N` passes on the audit issue and on each `bug` issue this lane files.
- [ ] The retro exists at `docs/retros/<date>-m6-doctrine-rules.md`, is posted on #651, and answers what the slice did to the two time-to-play numbers.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge, and `tools/lint-audit-artifacts` prints `PASS` on the folder; the six exit codes pasted on #651.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back, § 10; criterion 5's `renovation-status` clause and
the merge are the coordinator's); **the stage-D pause** (the punch list and
the audit issue posted on #651; the lane waits for the coordinator's stream
briefs and does no remediation before them, D-WORKFLOW-189); an explicit
maintainer pause on #651; any other blocker, named on #651 with what is
needed (a count that cannot be produced or two commands that disagree; a
rule that forbids a step; a doctrine tool that will not run); **a hash
mismatch at stage A** (a rule file on the branch differing from
`8ebaf8daad` in a hunk the dispatch comment did not name: something merged
under the read, the coordinator re-baselines); or an execution limit,
stated as such with the running log current. There is no Phase 4.6
blocker at Local depth. **The host's window is not this slice's concern**
beyond the protocol: nothing here needs the host's runtime. A checkpoint is
not a stop (D-WORKFLOW-149): write it and take the next stage. A differing
count is a delta, not a stop. `next` moving under the slice is drift, not a
stop. An idle session says it is idle on #651, **and does not end a turn on
a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session, headed by `#651`; `tools/work-log-index
  --write` after it; the weekly summary if the lane's week falls due
  (`ceremonies.md`; W42's is the M7 lane's week, overdue on 2026-10-24).
- A friction line in `docs/friction-log.md` the moment something slows,
  with `issue: #651` or the guard -- **the friction log is in this slice's
  membership**: the lane appends to it as every lane does, and reads its
  own appends as Q6/Q7 material like anyone else's.
- The VM question written before every proof (§ 5 answers it for the slice:
  no, the tree and the tools are the bench); a row in `docs/vm-qa-log.md`
  only if a guest ran.
- The mini-retro skill at stage G, posted on #651, with its scoped audit, in
  Instruction-Recommendations mode -- and for this slice the retro's
  *"adjustments to remaining work"* are rule edits by nature, so each is
  written as a proposal with its ladder stage, for the coordinator's stream
  brief or the next slice, never applied in the retro's commit.
- A register row the same session for any decision the slice forces (a fork
  resolved, an assumption invalidated). The ID: one above the highest
  `D-WORKFLOW` on every pushed branch and in the M7 lane's worktree; on
  2026-10-24 the highest Decided row is D-WORKFLOW-192 (191 is an open row;
  T3 and T5 run beside this lane and may take 193), so **the next Decided
  row is checked on every branch at the time**, and goes at the end of the
  `## Decided` table, never after `## Open decisions` (`tools/register-check`
  refuses it there, #646). A row that reverses a rule's premise lists what
  it made stale (`decision-register.md` § A reversal... sweeps its old
  words; `tools/archaeology --reversal`).
- `tools/ceremony-check` before every push; what it reports as owed by this
  lane is paid first; what another lane owes is noted on #651. Never
  `--no-verify`. A merge with conflicts is checked for leftover markers
  before it is committed (#696), and a union of two ledgers is made by
  whole entries, never by an unanchored pattern over marker-shaped text --
  **this slice's own membership is three such ledgers**.
- Commit messages `docs: ...` (the rules and registers are docs) with
  `Refs #651` and the bug's number; a rule edit's subject names the rule
  (`docs: time-to-play.md says which build it describes (#651, #N)`).
- `change-log.md`'s running log is for player-visible changes; none here.

## 10. Hand-back

The coordinator accepts the slice by reading, in this order, without
re-reviewing it: #651's checkboxes against their artifacts (§ 7); the lint's
`PASS` line on the audit folder; `second-opinions/review-plan.json` (Local,
no reviewer, the reason); the audit issue's checkboxes all at an outcome;
the coverage table's row count; `02-forward-audit.md`'s check lines and the
`proved:` cell on each proof; **re-running `tools/rules-check`,
`tools/register-check` and the `paths:` glob counts once, and three of the
Q4 tables' rows re-queried**, rather than trusting the log alone; the
retro's four answers; the six checker exit codes on #651 (with
`register-check` run on a simulated merge with the coordinator tip, as
T1's acceptance did -- and here the simulation matters more than anywhere,
because both branches edit the same prose). The lane posts one hand-back
comment on #651 naming the branch tip and each of those artifacts by path,
writes `reviewed-at:` and `fixed-at:` into #651's body, then says it is
idle. After acceptance the coordinator writes the hashes into
`slices.json`, merges the branch in its turn after the M7 candidate (P0,
P1, T1, T2, T3, T5, T4: **the doctrine's edits after the engine's**, so the
rules every later lane reads land last and once), regenerates the ledgers,
and **closes #651 when every `fix-tree` row is proven and every
`fix-pending-session` row has been read by the next lane's stage A** (the
slice is `remediating` until then, plan § 6b stage H). A brief that needed
the coordinator's help mid-slice, beyond the stage-D pause and the
re-baseline over the coordinator's own rule edits this brief already names,
is a defect in this brief: log the friction, and the coordinator fixes the
template in plan § 7 before the next brief.

**The two readings before dispatch** (plan § 3, principle 3): the area
epic's futro (`docs/futros/2026-10-24-m6-doctrine.md`, posted on the epic)
and a stranger's proof of this brief by a reader with no context given this
tree and the brief. Version 2 records what each found and where it is
answered.
