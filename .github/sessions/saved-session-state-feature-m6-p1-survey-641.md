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

**Checkpoint 2026-10-22, passes 1 to 5 complete and pass 6's reconciliation
done (the executor, Opus 5.5, session `dbac446e-3b41-4b28-966d-0a6efe07ea2b`).**
The generated ledgers: `docs/reviews/inventory.{json,md}` (at `17dee5ba42`),
`assessment.md` (`--assess`), `cross-reference.md` (`--cross`), and the
proposed order: `slices.json` (43 slices) rendered into `order.md` by
`--order` (every one of 134,591 rows in exactly one slice). The tracking file
records each pass with its commands. **Next: the preliminary review of the
order** (brief § 1): `npm install --prefix tools/council`, record the `tsx`
version, write the contract to
`research/preliminary-reviews/2026-10-22-m6-p1-order/review-contract.json`,
build the source manifest (`order.md`, `inventory.md`, `areas.json`,
`plan-for-the-plan.md` with sha256 and witness commit), invoke claude, gemini
and gpt one at a time through `tools/council/run invoke --provider openrouter`,
verifying each served model before the next. Then answer objections in
`order.md`, and post the pass-7 gate on #641 and **wait for the maintainer's
yes** (via the coordinator) before filing any slice issue or the register row
D-WORKFLOW-184. Meanwhile build `tools/renovation-status`,
`tools/renovation-drift` and the lint's renovation face. The ES detached
worktree is at `/home/max/Development/emulationstation-next.worktrees/m6-p1-survey`
(remove with `git -C /home/max/Development/emulationstation-next worktree
remove` at the end).

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
