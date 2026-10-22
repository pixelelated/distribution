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

**Checkpoint 2026-10-22, at the pass-7 gate (the executor, Opus 5.5, session
`dbac446e-3b41-4b28-966d-0a6efe07ea2b`). Waiting for the maintainer's yes on
#641, relayed by the coordinator (`m6-coordinator`).** Passes 1 to 6 are
complete: the ledgers at `f814d1a75c` (`inventory`, `assessment`,
`cross-reference`), the revised order (47 slices, `slices.json` rendered into
`order.md`), the preliminary review (`research/preliminary-reviews/2026-10-22-m6-p1-order/`,
three seats verified, all "ready with named changes", answered by name in
`order.md`), `status.md` (`order: reviewed`, 47 unreviewed). The three tools
and the lint face are built and proven. The five checkers passed before the
post. Three questions are put to the maintainer in the post: the shipped
devices, `backuptool` and the system services under the `0.1` gate, and the
cost of 13 Extended slices.

**On the yes** (a yes that moves a slice renumbers `T<k>` in `slices.json`
first, then `--order`):
1. the register row **D-WORKFLOW-184** (re-derive the ID with the brief § 6
   greps first; check the other lanes);
2. the 47 slice issues: generate the bodies with
   `python3 -I <scratch>/slice_issues.py <dir>` (its text is quoted in the
   tracking file if the scratch copy is gone), then for each: `gh issue create
   --repo pixelelated/distribution --milestone "M6: Codebase renovation"
   --title "$(cat T<k>.title)" --body-file T<k>.md`, the REST id with `gh api
   repos/pixelelated/distribution/issues/<n> --jq .id`, and `gh api -X POST
   repos/pixelelated/distribution/issues/339/sub_issues -F sub_issue_id=<id>`;
   `tools/box-check --issue <n>` on each, pasted on #641;
3. `docs/reviews/status.md` regenerated (`tools/renovation-status --write`),
   #339's body linking `docs/reviews/order.md`, the M6 body's NEXT set to T1
   and read back;
4. the mini-retro on #641, the ES worktree removed
   (`git -C /home/max/Development/emulationstation-next worktree remove
   /home/max/Development/emulationstation-next.worktrees/m6-p1-survey`), the
   five checkers re-run and pasted, the branch pushed.

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
