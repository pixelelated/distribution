# Session pointer: M6.P1, the survey (#641)

> **Seeded:** 2026-10-22 by the planner (Fable 5.1); the executor updates this file at every checkpoint
> **Branch:** `feature/m6-p1-survey-641`, stacked on `feature/m6-renovation-plan-346` (D-WORKFLOW-182)
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-p1-survey-641`
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (the fresh clone, D-INFRA-025); the legacy `/workspace/repos/rocknix` is the M7 lane's until its cutover at the next release candidate (D-INFRA-026)
> **Repository:** `pixelelated/distribution`; integration branch `next`
> **Executor:** Opus 5.5 at high effort unless #641 says otherwise
> **Herdr:** workspace `wN` "pixelelated · Codebase renovation", tab `wN:t3` "P1 Survey (#641)", pane `wN:p3`, agent name `m6-p1-survey`; the coordinator is tab `wN:t2` "Coordinator (M6, #346)", agent `m6-coordinator` (Fable). Your session id is read from `herdr agent list` and recorded on #641 at start. Never write outside this worktree; never type into another pane; questions for the maintainer go up through the coordinator.

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   confirm this worktree's rules are `next`'s:
   `git diff --quiet next -- .claude CLAUDE.md AGENTS.md || echo STALE`.
   Known stale facts in those rules are listed in the brief § 3; this lane's
   layout is the brief's, not `worktrees.md`'s.
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/p1-survey.md` whole. The brief is the work; its § 7 is
   the contract, identical to the checklist on #641.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #641 (with its comments), #339 and #346. The M7 lane's canonical
   checkpoint `saved-session-state-next.md` is read for what runs on this
   host, not for a work queue; this lane never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/reviews/p1-tracking.md` and write the futro before pass 1.

## Current focus

**Checkpoint 2026-10-22 19:20 UTC (the executor, Opus 5.5, session
`dbac446e-3b41-4b28-966d-0a6efe07ea2b`).** The P0 tip `fac868f2fb` merged
into this stack (`bff1ccec2a`); the stacking check passes. The order's
register ID is now **D-WORKFLOW-184** (183 is the lane structure). Counts
re-derived equal (tracking file). Done: the futro
(`docs/futros/2026-10-22-m6-p1-survey.md`, also on #641), the tracking
file's header (`docs/reviews/p1-tracking.md`), the work-log entry and a
friction line. The ES detached worktree exists at
`/home/max/Development/emulationstation-next.worktrees/m6-p1-survey` (remove
with `git -C /home/max/Development/emulationstation-next worktree remove` at
the end). **Next: pass 1**, `docs/reviews/areas.json` and
`tools/renovation-inventory`, under the futro's rules: `BUILD_DIR` in a temp
directory, `ambiguous:` beside `unassigned:`, the `n/a` reachability value,
sourced generic recipes reached, the `patches/<DEVICE>/` refinement, compact
rows with the size measured.

## Next commands

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-p1-survey-641
git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor origin/feature/m6-renovation-plan-346 HEAD && echo stacked-on-P0
git diff --quiet next -- .claude CLAUDE.md AGENTS.md || echo STALE
sed -n '/## Progress/,/## Read first/p' docs/reviews/p1-tracking.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` to
`next`, then this branch. When `next` moves, merge `next` into this branch
(never another lane's feature branch). This branch, the P0 branch and the M7
lane all append to `docs/decision-register.md`, today's work log and
`docs/work-logs/INDEX.md`: keep every append, regenerate the index. The
register ID for the order is D-WORKFLOW-184 (182 is the stacked-start
decision, 183 the lane structure; the M7 lane holds 171 to 180 unmerged).
The P0 branch is merged into this one when it moves, as the stack's base
(done once, `bff1ccec2a`). Nothing here builds,
touches a device, a cloud or the M7 build worktrees.
