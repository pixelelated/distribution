# Session pointer: M6.P2 T4, the binding doctrine (#651)

> **Seeded:** 2026-10-24 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file at every checkpoint
> **Branch:** `feature/m6-doctrine-rules-651`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tip `c35acd3732` merged in at `e3897db16d` (four ledger conflicts united by whole entries, the index regenerated, P1's brief kept; the marker grep empty before the commit)
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-rules-651`; the T3, T30 and T24 worktrees beside it (`m6-emulators-libretro-650`, `m6-emulators-standalone-677`, `m6-emulators-dead-ends-671`) are this session's earlier slices, accepted and idle: read only, until their merges
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T3 session, `m6-t3-emulators`, freed by T24's completion at 14:27 UTC; no third lane runs), unless #651 says otherwise
> **Epic:** #807 (the doctrine: T4, T38 #685, T39 #686); the renovation epic #339; the milestone M6; beside T8 (#655) in the other lane (D-WORKFLOW-190)
> **Depth:** Local -- a doctrine read; no reviewer, no Facilitator call, no `npm install`; the review plan carries `tier_exception: D-WORKFLOW-184` (#810, fixed and merged here at `18747fbc52`)
> **Budget:** the GitHub API (5,000 calls an hour, shared with the coordinator's monitors); `gh api rate_limit` before any loop over issues

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   **this slice reads the rules at `next`'s hash `8ebaf8daad` as its bytes**
   (brief § 2). This worktree differs from `next` on the eleven paths the
   dispatch comment on #651 lists (the coordinator's and P1's unmerged
   edits since the hash, the first lead): `git diff --stat next -- .claude
   CLAUDE.md AGENTS.md NAMING.md docs/decision-register.md
   docs/blindspot-register.md docs/friction-log.md tools/lint-audit-artifacts`
   prints exactly those; anything else is STALE. Known stale facts in the
   rules (the legacy layout, #640's) are the slice's own findings, recorded
   with #640 named and not changed here.
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/doctrine-rules.md` whole (version 2, `0921782112`).
   The brief is the work; its § 7 is the contract, identical to the sixteen
   checkboxes on #651. The brief's § 1 says *five files* differ from `next`
   and names a third lane as the maintainer's call: both are superseded by
   the dispatch comment (eleven paths; this session, no third lane); the
   brief is otherwise current.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #651 (with its comments), #807 (the epic, with its futro comment),
   #339, #346 (the maintainer's channel: what is open there is not this
   lane's to decide), #644 (four of its findings are this slice's, brief
   § 3), #640 (the legacy host paths: the drift is recorded here, changed
   only when #640 says so), #810 (fixed), T1 #648 and T2 #649 (accepted;
   their rule leads). The M7 lane's canonical checkpoint
   `.github/sessions/saved-session-state-next.md` is read for what runs on
   this host; this lane never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-doctrine-rules/00-running-log.md`
   and write stage A before reading a rule.

## Current focus

**Accepted; the lane idle (2026-10-24 15:48 UTC).**
- The coordinator accepted T4 at `cceac27d6a` (#651, 15:47 UTC) and closed #912 as completed.
- `audit-completion.json` is written from #912's closed readback, and the full `lint-audit-artifacts` prints `PASS`.
- `reviewed-at: 00e75ab135`, `fixed-at: b3c1d0d7c3`.
- Nothing is owed. The branch merges last in the order, after the M7 candidate: the coordinator's merge, then `renovation-status`.
- #904 and #906 to #910 stay open, ticked, until that merge. #905 closes with its packet; #911 is T38's.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-doctrine-rules-651
cd "$D" && git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md NAMING.md docs/decision-register.md docs/blindspot-register.md docs/friction-log.md tools/lint-audit-artifacts   # exactly the eleven paths
ls docs/reviews/inventory.json docs/reviews/slices.json docs/reviews/cross-reference.md
sed -n '1,160p' docs/reviews/briefs/doctrine-rules.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24
(`26e4a34edf`), the two checksum packets (#877, #890), T5, T6, T7, T8, **then
this branch last**, so the doctrine's edits land once: each rule-file
conflict is resolved in the coordinator's favour and this slice's edit
re-applied by the paragraph its stream brief names. When `next` moves, the
**coordinator** merges `next` into this branch, and never between stage A
and stage D (the read must stay a fact about one hash, plan § 8); after
stage D a merge re-baselines the slice over the diff, recorded on #651.
Never merge another lane's feature branch here. Every lane and the M7 lane
append to `docs/decision-register.md`, the day's work log and
`docs/work-logs/INDEX.md`: keep every append, regenerate the index, never
edit another lane's rows; a merge with conflicts is checked for leftover
markers before it is committed (#696; the pre-commit hook on the
coordinator's branch refuses them, not yet on `next`), and a union of two
ledgers is made by whole entries. The highest Decided register ID on
2026-10-24 at 14:3x is D-WORKFLOW-199 (the coordinator's); T8 runs beside
this lane and may take 200: check both branches; a new row goes at the end
of `## Decided`, and a row is never edited. Nothing here builds, touches a
device, a cloud, a guest, or another lane's worktree.
