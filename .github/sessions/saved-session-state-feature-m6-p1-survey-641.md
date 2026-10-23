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

**Checkpoint 2026-10-23, at the pass-7 gate, third version (the executor,
Opus 5.5, session `dbac446e-3b41-4b28-966d-0a6efe07ea2b`).** The second
version (47 slices) was posted on #641. The maintainer answered the first
question through the coordinator (`m6-renovation-plan-346-d9`):
D-WORKFLOW-185 (H700 and SM8550 ship, GENERIC_X64 is the test image) and
D-WORKFLOW-186 (the build process and its tooling before any device). The P0
tip `5923dd29a4` was merged (`be3ddf13c5`); the inventory gained a `test`
reach value; the order was re-sequenced to a third version of 46 slices
(build cluster T5 to T15, `device-rockchip-shipped` dissolved), every ledger
regenerated (`p1-tracking.md` § Pass 7), and the third version posted on
#641 with the commit sent to the coordinator. **Waiting for:** question 2
(`backuptool` T17 and the system services T22 under the `0.1` gate), then
question 3 (the 13 Extended slices), then the yes on the third version, all
relayed by the coordinator. #644 (ROCKNIX's build docs) is the coordinator's;
its findings are an input to T5 and T9, not a change to their paths.

**On the yes** (a yes that moves a slice renumbers `T<k>` in `slices.json`
first, then `--order`):
1. the register row, the next free ID above the P0 tip's highest
   (**D-WORKFLOW-187** today; re-derive with the brief § 6 greps first and
   check the other lanes), citing D-WORKFLOW-185 and D-WORKFLOW-186;
2. the 46 slice issues: generate the titles and bodies with
   `tools/renovation-inventory --slice-issues <dir> --order-row D-WORKFLOW-<that ID>` (writes `T<k>.title` and
   `T<k>.md`, touches no tracker), then for each: `gh issue create
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
register ID for the order is the next free above 186 (182 is the stacked-start
decision, 183 the lane structure, 184 to 186 the coordinator's relays; the M7
lane holds 171 to 180 unmerged).
The P0 branch is merged into this one when it moves, as the stack's base
(done twice: `bff1ccec2a`, `be3ddf13c5`). Nothing here builds,
touches a device, a cloud or the M7 build worktrees.
