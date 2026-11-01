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

**Checkpoint 2026-10-23 05:45 UTC, the hand-back (the executor, Opus 5.5,
session `dbac446e-3b41-4b28-966d-0a6efe07ea2b`).** All seven passes are
complete. The order's fourth version has the maintainer's yes (#641 comment
6356453637) and its row, D-WORKFLOW-188, which sits between 187 and 189
after the P0 tip `f5bea1696a` was merged (`1e5d151b2b`).

**D-WORKFLOW-189:** planning, the division of work, the definition of work
items and roadmap changes are the coordinator lane's; a work lane executes.
So the 46 slice issues, their criteria, the M6 body's NEXT and #339's links
are the coordinator's. **Never file, edit or write criteria for a slice
issue from this lane.** P1's part is the renderer,
`tools/renovation-inventory --slice-issues DIR`, which printed `wrote 46
slice issue bodies` at the merge (brief version 3.2, criterion 7).

Hand-back posted on #641:
- the inventory and its four counts;
- the order;
- the three tools and the lint face (fixtures rc 0 and rc 1);
- `status.md`, regenerated with 24 of 46 linked while the coordinator was
  filing;
- the five checkers, all exit 0;
- the tracking file's § Pass 7 hand-back paragraph;
- the retro, `docs/retros/2026-10-23-m6-p1-survey.md`.

The ES worktree of the survey is removed. `ceremony-check --gate` refuses a
push of `next` on the M7 lane's W42 summary only.

**Waiting for:** the coordinator's acceptance under brief § 10. Questions
about scope or order go to the coordinator; this lane decides none of them.

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
order's row is D-WORKFLOW-188, between 187 and 189 in the Decided table (189
is the coordinator's lane rule); the M7 lane holds 171 to 180 unmerged.
The P0 branch is merged into this one when it moves, as the stack's base
(done five times: `bff1ccec2a`, `be3ddf13c5`, `87f447f930`, `b56943963c`, `1e5d151b2b`). Nothing here builds,
touches a device, a cloud or the M7 build worktrees.
