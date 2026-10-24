# Session pointer: M6.P2 T6, upstream's helper tools and the other distributions (#653)

> **Seeded:** 2026-10-24 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file at every checkpoint
> **Branch:** `feature/m6-build-engine-upstream-tools-653`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tip merged in at `e84180386d`
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-upstream-tools-653`; the T5 worktree `m6-build-engine-652` beside it is this session's earlier slice, accepted and idle: read only until the merge
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T5 session, `m6-t5-build-engine`), unless #653 says otherwise
> **Epic:** #800 (the build engine); the renovation epic #339; the milestone M6; beside T30 (#677) in the other lane (D-WORKFLOW-190)
> **Depth:** Local -- no reviewer, no Facilitator call, no `npm install`; the review plan carries `tier_exception: D-WORKFLOW-184` (#810)

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   this worktree's rules are `next`'s except the seven paths the brief § 1
   names: `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`
   lists exactly those; anything else is STALE. Known stale facts in the
   rules are listed in the brief § 1 and § 3; this lane's layout is the
   brief's, not `worktrees.md`'s.
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/build-engine-upstream-tools.md` whole (version 2).
   The brief is the work; its § 7 is the contract, identical to the
   checklist on #653. Its first and second commands include the at-hash
   export under `.qa-scratch/t6/`; a tree export never goes under `/tmp`.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #653 (with its comments), #800 (the epic, with its futro and the T6
   addendum), #644 (finding 24), #652 (T5, accepted: the engine this slice's
   tools belong to; its audit folder is the nearest reading), #585 (where
   finding 24's proposal lands). The M7 lane's canonical checkpoint
   `.github/sessions/saved-session-state-next.md` is read for what runs on
   this host; this lane never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-build-engine-upstream-tools/00-running-log.md`
   and write stage A before reading a row of the slice.

## Current focus

**T6 complete; the lane is idle (2026-10-24 08:58 UTC).** Accepted on #653; #846 closed as completed.
- `reviewed-at` `b96e1ca761`, `fixed-at` `820e413179`. S1 `7fa8bafba4` (#845) and S2 `44f64842b6`.
- `audit-completion.json` was written from #846's closed readback, and the full lint prints PASS (posted on #653).
- #845 stays open until the branch merges to `next`.
- **Next:** nothing in this lane. The coordinator merges the branch in its turn (after T5's, before T4's); this worktree stays read-only until then.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-upstream-tools-653
cd "$D" && git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts    # the six files
sed -n '1,120p' docs/reviews/briefs/build-engine-upstream-tools.md
```

## Merge notes

Merge order after the M7 candidate: P0, P1, T1, T2, T3, T30 (with T3's),
T5, then this branch (after T5's, before T4's), the ledgers united by whole
entries. When `next` moves, the **coordinator** merges `next` into this
branch, never between stage A and stage D. Never merge another lane's
feature branch here. The highest register ID on 2026-10-24 is D-WORKFLOW-194
in the Decided table; T30 runs beside this lane and may take 195: check
every pushed branch before writing a row, at the end of `## Decided`. A
commit names its paths; `git status --short` is read before each commit as
well as after. Nothing here builds, touches a device, a cloud, or another
lane's worktree.
