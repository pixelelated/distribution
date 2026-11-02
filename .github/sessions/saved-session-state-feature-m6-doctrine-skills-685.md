# Session pointer: M6.P2 T38, the skills, agents and settings: the ten skills the per-slice procedure and the sessions run, the council export and its eight agent definitions, and what each costs against what it is used for (#685)

> **Seeded:** 2026-11-01 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch (distribution):** `feature/m6-doctrine-skills-685`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's branch merged in -- its tip `3a9b0aec81` at the merge commit `87c2ab0fed`, one merge, carrying the brief's versions 1 and 2, the doctrine futro's T38 kickoff addendum, the register rows the brief cites with this slice's ownership row, and the day's logs; the lane's own tip at stage A is `87c2ab0fed` (the merge commit; each checkpoint line below records it as it moves). These are the brief's four placeholders in its § 1 order -- the coordinator's tip, the merge commit, the lane's tip, and the brief's commit under *The brief* below -- filled here at seeding, so none is the lane's to guess
> **Worktree (distribution):** `/workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-skills-685` -- the audit artifacts, the work log, this pointer, every ceremony and every fix (stage E, inside the fork-adapted skills only) live here; the read tree is exported once to `/workspace/tmp/m6-t38/export/` (`git archive HEAD .claude/agents .claude/skills`, the brief's § 5) and retired at stage H
> **Worktree (EmulationStation):** **none**: nothing in the 52 is EmulationStation's, and no ES checkout is read (the brief's § 1)
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run; no ES checkout under `~/Development/emulationstation-next.worktrees/` is read by this slice; T4's audit is read from its branch by hash (`git show 6ec78bbf8c:<path>` in this worktree), T45's records at `ae08d48392` the same way; M7's October work is cited by issue number
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #685 names (`m6-t5-build-engine`; the brief's § 1: the T5 session, `m6-t5-build-engine`, free since T35's close-out, its cwd an earlier lane's worktree -- the lane `cd`s here first)
> **Epic:** #807 (`M6.P2 E339: Area epic: the doctrine (T4, T38, T39)`): T4 #651 complete and idle at `6ec78bbf8c`, awaiting the area's merge, its folder `docs/audits/2026_10_24-epic-m6-doctrine-rules/` read by hash; this slice; T39 #686 after; the renovation epic #339; the milestone M6 (D-WORKFLOW-190); this lane posts nothing on #807 (the coordinator posts the `council-research` question there at the stage-D pause, the brief's § 4 and ruling (n))
> **Depth:** **Local** -- the executor alone (plan § 6c: *"a dead-end table, a provenance table, a doctrine read | Local: the executor alone; the lint and the counts are the check"*); `second-opinions/review-plan.json` in T4's plan's shape -- depth `local`, primary `anthropic/claude-opus-5-5` (T4's form at `6ec78bbf8c`; the template's `templates.md:136` writes `anthropic/claude-opus-5.5`, which is L-51), lab `anthropic`, reviewers `[]`, `tier_exception` `D-WORKFLOW-184`, the reason plan § 6c's row -- and `ls second-opinions/` listing it alone: **no seat, no packet, no provenance file, no held sidecar, no keyed call, no `tools/council/run` call keyed or keyless, no Facilitator, no `npm install`**; the lint's PASS on a Local plan proved at stage A before anything else, with its FAIL-first (ruling (m)); Phase 4.6 recorded *not applicable at Local depth*, Phase 4.5 in full, and § 5's rule 4 -- what result would have produced a FAIL -- asked of every PASS
> **The lens:** cost against value over the 52 of `.claude/**` less `.claude/rules/**` -- the ten skills and the eight agent definitions -- **12,734 lines at the P1 hash `2174265e9c`** (and at the inventory's head `eb4763e3cc` and at `next` `8ebaf8daad`) and **12,783 at the dispatch tip**, the coordinator's branch having moved three of the 52 after the inventory (` 3 files changed, 50 insertions(+), 1 deletion(-)`: `code-auditor/references/templates.md` 331 -> 348, `council/IMPORTED-FROM.md` 102 -> 127, `mini-retro/references/scoped-audit.md` 709 -> 716; L-01); 10 `SKILL.md` (3,797 lines), 31 `references/*.md` (8,373), 8 agent definitions (334), 2 other markdown files in the council skill (136) and 1 checksum list (94) at the P1 hash; 51 `markdown` and 1 `other`, all tier fork-own; by origin the export (`council` 15 files, `council-research` 12, the 8 agents), imported and adapted (`begin-delivery`, `code-auditor`, `futro`, `mini-retro`, `session-resume`, `session-stash`) and synthesized here (`developer-relations`, `release-notes`); seven questions in the brief's § 4 (Modernize, Standards, Bugs, Currency, Efficiency -- the lens --, Dead ends, Clarity), with the leads L-01 to L-51 in its § 3 and the FAIL-first candidates (L-02 to L-11, L-51) first; the read order of ruling (j) -- cluster 2's six (`code-auditor`, `mini-retro`, `futro`, `session-resume`, `session-stash`, `begin-delivery`), then the writing pair (`developer-relations`, `release-notes`, between the clusters where § 2's table places them; the dispatch comment answers open item 1), then the council family (`council`, `council-research`, the agents), read and never edited; T38 is not split
> **The rule:** **the lane changes only the fork-adapted skills among the 52, only at stage E under a stream brief** (`docs/reviews/briefs/t38-streams.md`, the coordinator's at the stage-D pause); **never** `.claude/rules/**`, `CLAUDE.md`, `AGENTS.md`, `NAMING.md`, a register (beyond the appends the procedure owns), `verifier-pins.json`, `scripts/` or `tools/` (no new file there: `tools/skills-check` is Backlog #1373's, and the lane's checker is `tools/t38-checks.sh` under the audit folder), or anything under `council/`, `council-research/` or `.claude/agents/` -- the export, refreshed by copying (D-WORKFLOW-088), the agents pinned and the three inactive ones kept as written (rulings (d), (e), (l)); **no council, Facilitator or keyed call, and no skill invoked against a provider** (ruling (k)): a block of the 52 that would call a provider, write a stash, post on the tracker or open a `research/` run is checked for its tool's existence and options, never run; a sentence a reader acts on wrongly is a `bug` the lane files with its trace and its `Already written:` line, everything else a punch item (ruling (c)); a rule erratum a skill read turns up is the coordinator's, an inherited item (ruling (l)), and a council-family finding an inherited item for #911 (ruling (d)); no held directory is opened (`/workspace/tmp/m6-t34/held/` and `/workspace/tmp/m6-t36/held/` included)
> **The host:** **none**: no guest window and no compile; the shared log `/workspace/tmp/m7-m6-host-coordination.txt` is read once at stage A, whole, with the time of the read, for its protocol alone; **no START, RETURN or compile line of this lane's in it, or on #685, at any stage -- one is a stop** (the brief's § 10); criterion 19 counts the lines that file gains between the dispatch comment (which names its line count then) and the hand-back; the guarded swap reclamation is not this slice's; no build on the host at any time
> **Register:** the rows this brief cites are on the coordinator's branch, merged here; D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-137, D-WORKFLOW-218 are the highest decided rows of their areas, read from the decided table above `## Open decisions` at the coordinator's tip `3a9b0aec81` (at `926d1fbaee` the brief read D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-137, D-WORKFLOW-216, with T37's -217 since its dispatch, `:777` at `2f42ff5ddf`), the WORKFLOW one being **this slice's ownership row, D-WORKFLOW-218, written by the coordinator at dispatch** (the brief's § 1 (l) and § 9); the rows the pause may need (council-research kept or retired, `begin-exploration` written or swept, the bundle's sums, the October22 sections, the stash's tool, the time lines) are put to the coordinator there, never decided by the lane, and a row this slice forces takes an ID the coordinator assigns on #685
> **The brief:** `docs/reviews/briefs/doctrine-skills.md` at `fa4a9a5b0d` (version 2 of 2026-11-01, after the stranger's proof of version 1, which is committed under this name at `2f42ff5ddf` -- its eleven corrections under `## Version 2: corrections from the proof`, with the nine open items that remain); #685's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Stage E is done and handed back twice on #685.** The first hand-back was at 05:55 UTC; the second, at the amendment of the acceptance read's eight asks (06:45), carries the retro `docs/retros/2026-11-01-m6-doctrine-skills.md`. The lane is idle until the coordinator accepts. Stage F comes next:
- run 4 of the checker;
- `audit-completion.json`, once #1394 is closed.

Stage G, the retro, follows F.

What stage E produced, under the stream brief `docs/reviews/briefs/t38-streams.md` at `95052eaf78`:
- **51 items in 56 fix commits** (S1 to S7), each with its check FAIL at the parent's export and PASS at the fix's, `tools/t38-checks.sh` exit 0 and `tools/rules-check --quiet` rc=0. `fixed-at` is `420b845656`, `reviewed-at` `87c2ab0fed`. The records are `stage-e/<SN>-<PL>.txt`, and the helper is `tools/t38-fix.sh`.
- **`05`:** 51 Resolved and 6 Deferred. `tools/lint-audit-artifacts` passes on its default phase and with `--issue 1394`.
- **The bugs #1389 to #1393:** `fixed-at` and every checkbox ticked, `box-check` 0 fail. #1394's checkboxes are the coordinator's.
- **`allow-findings.txt`** is empty. The stale term `begin-exploration` is in the checker and counts 0 outside the export.
- **The merge:** the coordinator's `6a12ce2d73`, merged at `916c9f9952` by the recipe; the five checkers exit 0 before and after it.
- **The record:** 58 proofs and 58 `PROOF:` lines; `04` stands at 15 of 22.

What the stage-A paragraph below asked:

Before the first command after `cat`, the eleven keys of this
pointer are read against the brief's § 10 table, and any that names the
predecessor slice (T37's `feature/m6-es-recipe-684`, `m6-es-recipe-684`,
`m6-t3-emulators`, #700, the 15 of `projects/ROCKNIX/packages/ui/**`, a
15 + 5 minute window) is reported on #685 before going on; the placeholder
check below prints 0. The first check after the pointer is the lint's PASS
on a Local plan and its FAIL with `tier_exception` removed (ruling (m)),
recorded in `00` before anything else; then the rest of § 5's `# STAGE A`
block, whole and in order; then § 2's membership block and its dispatch-tip
lines. The first commit on the distribution branch is the running log's
header (the model, the effort, the session, `reviewed-at` the dispatch tip
with `2174265e9c` and `8ebaf8daad` beside it and the three moved files
listed, the lint's Local proof, the host file's last lines with the time of
the read), `01-research-notes.md` § Scope (§ 2's block with its output and
its sha256 prefix `7fa0430cf613e867` checked, both totals, the drift), this
pointer updated, and the day's work-log entry headed `#685` (prose through a
quoted heredoc or the Write tool). There is no ES worktree, no guest and no
compile. `.qa-scratch/` is gitignored and `git status --short` is read
before every `git add -A`; anything temporary goes under
`/workspace/tmp/m6-t38/`, never `/tmp`. No network is used beyond
`gh --repo pixelelated/distribution` reads and the lane's own posts and
issues.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-skills-685
cd "$D"   # no fetch of any kind: every hash the brief names is already in the repository
git branch --show-current                                                            # feature/m6-doctrine-skills-685
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git merge-base --is-ancestor 3a9b0aec81 HEAD && echo coordinator-tip-merged
X=':(exclude).claude/rules/'; git diff --shortstat 2174265e9c HEAD -- .claude/ "$X"     #  3 files changed, 50 insertions(+), 1 deletion(-)
git diff --stat 87c2ab0fed HEAD -- .claude/rules CLAUDE.md AGENTS.md NAMING.md verifier-pins.json scripts tools .claude/skills/council .claude/skills/council-research .claude/agents | tail -n 1   # empty at every stage (the brief's § 5 removal check)
test -f docs/reviews/inventory.json && echo inventory
/usr/bin/grep -c -E '__[A-Z0-9_]+__|\b(CO''HASH|MERGE_''HASH|TIP''HASH|V2''HASH)\b' .github/sessions/saved-session-state-feature-m6-doctrine-skills-685.md   # 0: the brief's § 9 check, its first half widened to catch a digit or an underscore; the quotes split each word so this line does not count itself
git show fa4a9a5b0d:docs/reviews/briefs/doctrine-skills.md | sha256sum | cut -c1-16   # b6d30242978fa606 (version 2, 2,021 lines)
date -u +%H:%M:%S; tail -n 6 /workspace/tmp/m7-m6-host-coordination.txt | cut -c1-200   # the protocol only; this slice writes no line there
sed -n '1,359p' docs/reviews/briefs/doctrine-skills.md                               # the opening and § 1; § 2 opens at :360
```

## Merge notes

The merge order is the coordinator's, named at acceptance (the brief's § 8
and its open item 9): the doctrine's edits land after the engine's (T4's
§ 10: *"the rules every later lane reads land last and once"*), with T4's
last. When `next` moves, the **coordinator** merges `next` into this branch,
and never between stage A and stage D; the coordinator merges its own branch
into this one at hand-back, before the last criterion's checkers run. Never
merge another lane's feature branch here. Every lane and the M7 lane append
to `docs/decision-register.md`, the day's work log and
`docs/work-logs/INDEX.md`: keep every append, regenerate the index, never
edit another lane's rows; a merge with conflicts is checked for leftover
markers before it is committed (#696), and a union of two ledgers is made by
whole entries. Nothing here builds an image or a package, sources
`config/options`, runs a guest, a council call or a skill against a
provider, touches a device, a cloud account, a key file, the host's swap,
another lane's worktree or an ES checkout, or edits a rule, `CLAUDE.md`,
`AGENTS.md`, `NAMING.md`, the pins or the council family.

## Checkpoints

- Stage A, 02:53 UTC 2026-11-01: committed on `11fa8f95b8` (the commit carrying this line; its hash is in #685's stage-A checkpoint post). The lint's Local proof PASS rc 0 and FAIL rc 1; the membership block equal to the brief's lines byte for byte; 12,734 at the P1 hash and 12,783 at the dispatch tip; the 32 issues re-read; nothing under `.claude/` edited; no line in the host file.
- Stage B, 03:33 UTC 2026-11-01: committed on `98019cea9f` (the commit carrying this line; its hash in #685's stage-B checkpoint post). The 52 read by a reader and the lane; `02`, `03`, `04` and `01` § Read order written; 34 proofs; nothing under `.claude/` edited.
- Stage C, 03:52 UTC 2026-11-01: committed on `168bbba783` (the commit carrying this line; its hash is in #685's stage-C checkpoint post). Run 1 of the checker 947 of 947; FAIL-first every probe at its wanted exit after run 2a's harness fix; the withheld tip 902 of 928 at the 19 keys; `05` with 57 Open items; the pre-issue lint PASS; 42 proofs; nothing under `.claude/` edited.
- Stage D, 04:04 UTC 2026-11-01: committed on `8c76ca62d3` (the commit carrying this line; its hash is in #685's pause post). The bugs #1389 to #1393; the audit issue #1394 under #685 with 57 checkboxes, `box-check` 0 fail, the lint `--phase pre-issue --issue 1394` PASS; the questions `6553169705` and `6553118160` read back; 50 proofs; nothing under `.claude/` edited.
- Stage E, 05:55 UTC 2026-11-01: committed on `916c9f9952` (the merge; the commit carrying this line is named in #685's stage-E hand-back). 51 items in 56 fix commits, `fixed-at` `420b845656`; the checker at fixed-at `TOTAL: 962 of 962 assertions`; the lint PASS on its default phase and with `--issue 1394`; the coordinator's `6a12ce2d73` merged; 58 proofs.
- Stage E amendment, 2026-11-01: committed on `44626257ef`. The acceptance read's eight asks: `05`'s Ladder lines; the generated, asserted lines; four sets of lines into `02` § The runs; the per-lead inherit rows with the #585 row; the retro. The commit carrying this line is named in the second hand-back.
- Acceptance, 00:21 UTC 2026-11-02: the coordinator ticked 21 of 22 (comment 6566095780); #1394 closed as completed at 00:19.
- Stage F, 00:23 UTC 2026-11-02: `audit-completion.json` written by `tools/t38-completion.py` from #1394's closed readback (`completed_at` `2026-11-02T00:23:01.200276+00:00`). `ceremony-check`'s validator rc=0, and rc=1 on a planted one-byte change to `04`. The lint `PASS` on its default phase, with `--issue 1394` and with `--phase resolution`. 59 proofs. The commit carrying this line is named in the stage-H post.
