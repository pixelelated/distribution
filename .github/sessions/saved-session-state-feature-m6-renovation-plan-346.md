# Session pointer: the renovation lane (M6)

> **Saved:** 2026-10-22 (see the commit)
> **Branch:** `feature/m6-renovation-plan-346` (a pointer; D-WORKFLOW-133)
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346`
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (the fresh clone of 2026-10-22, D-INFRA-025; the legacy `/workspace/repos/rocknix` serves M7 until #640)
> **Repository:** `pixelelated/distribution`; integration branch `next`

## Start here

1. Read `next:AGENTS.md`, the every-session rules under `.claude/rules/`, and
   check this worktree's rules are `next`'s:
   `git diff --quiet next -- .claude CLAUDE.md AGENTS.md || echo STALE`.
2. Read [the canonical next checkpoint](saved-session-state-next.md) for the
   M7 lane's state. **This lane does not edit it** while M7 owns it (the open
   question on #346); this pointer is the lane's state.
3. Read `docs/reviews/plan-for-the-plan.md` (the plan for the plan, #346), the
   live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #339 (the epic) and #640 (the checkout move).
4. Register rows this lane wrote: D-WORKFLOW-181, D-INFRA-025. The M7 lane
   holds D-WORKFLOW-171 to 180 and D-INFRA-024 unmerged on
   `feature/m7-audit-integration-603`; do not cite them on this branch until
   they reach `next` (`tools/register-check` refuses a citation of an absent
   row).

## Current focus

P0, the plan for the plan: the document is on the branch (`0bfd387f7b` and
the correction after the first proof); the milestone and issue edits are made;
#641 is M6.P1 with the brief `docs/reviews/briefs/p1-survey.md` (version 2,
after the first stranger's proof found sixteen gaps, all answered in the text).
What remains of P0: the second proof's result recorded on #346, the P0
checkboxes ticked with their evidence, then the merge to `next`.

## Next commands

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346
git fetch origin && git merge --no-edit next          # only when next moved; never another lane's feature branch
tools/register-check && tools/work-log-index --check && tools/ceremony-check
```

Then: read #346's last comment for the proof's state; if the second proof
passed, tick P0's checkboxes on #346 with the evidence and merge this branch
to `next` (`git switch next && git merge --no-ff feature/m6-renovation-plan-346`
in the primary checkout, the push guard's checks first); if not, correct the
brief and run the proof again (a fresh session, the repository and the brief,
read-only, its first ten commands and its questions).

## Merge notes

This branch and the M7 lane both append to `docs/decision-register.md`, both
create `docs/work-logs/2026_10-work_logs/2026_10_22-work_log.md`, and both
regenerate `docs/work-logs/INDEX.md`. At merge: keep both appends in order,
keep both day-file entries, regenerate the index with
`tools/work-log-index --write`. Nothing here builds, touches a device, a
cloud or the M7 build worktrees.
