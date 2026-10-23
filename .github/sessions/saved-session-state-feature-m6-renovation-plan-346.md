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
What remains of P0: the merge to `next`, which waits for the M7 lane's
post-candidate merge to clear the push guard's W42 gate (D-INFRA-026,
D-WORKFLOW-182); never `--no-verify`. P1 started 2026-10-22 in its own
worktree `distribution.worktrees/m6-p1-survey-641` on
`feature/m6-p1-survey-641`, stacked on this branch; its state lives in its
own pointer. The pass-7 gate and the hand-back are passed (2026-10-23; #641 closed); this
lane's next act is T1's brief; see § State at 2026-10-23.

## Next commands

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346
git fetch origin && git merge --no-edit next          # only when next moved; never another lane's feature branch
tools/register-check && tools/work-log-index --check && tools/ceremony-check
```

Then: **at every gate, re-read § The seed brief below and D-WORKFLOW-181 against
what is about to be accepted, and say on #641 what was checked** (maintainer,
2026-10-23, giving the yes on the order: *"It's incredibly important that we
remain aligned."*). Read #641's latest comments for P1's state. At its pass-7 gate, read
the proposed order against plan § 5 and § 6a and record the yes or the
changes on #641. After the M7 candidate's merge lands on `next`, merge this
branch to `next` first (`git switch next && git merge --no-ff
feature/m6-renovation-plan-346` in the primary checkout, the push guard's
checks green), then P1's branch when it hands back. Address every git
command to a worktree with `git -C <absolute path>` and every file by its
absolute path: a `cd` at the head of a call did not hold on 2026-10-22 and a
commit meant for this branch landed on P1's.

## Herdr lane map (2026-10-22, the planning session's record)

Workspace `wN` "pixelelated · Codebase renovation" (session `default`),
after the maintainer's Herdr layout: first tabs coordinate, each later tab is
one lane, one session per worktree (D-WORKFLOW-183).

| Tab | Label | Pane | Worktree | Agent name | Model | Role |
| --- | --- | --- | --- | --- | --- | --- |
| `wN:t1` | P0 planning (#346) | `wN:p1` | none (`/workspace/repos/pixelelated`) | (unnamed, Claude Fable 5.1) | Fable 5.1 | the session that planned P0 and started the lanes; closes once the coordinator has resumed |
| `wN:t2` | Coordinator (M6, #346) | `wN:p2` | this worktree | `m6-coordinator` | Fable 5.1 | plans, writes briefs, accepts at gates, integrates; keeper of the primary checkout |
| `wN:t3` | P1 Survey (#641) | `wN:p3` | `distribution.worktrees/m6-p1-survey-641` | `m6-p1-survey` | Opus 5.5 | executes `docs/reviews/briefs/p1-survey.md` |

Session ids are read fresh from `herdr agent list` (`agent_session.value`)
and recorded on #346 and #641 at each start; never from this table. Other
workspaces on this host (`w4` the M7 lane, `wG` the website, `w7` another
project) are never read, prompted, moved or closed from here. Questions only
the maintainer can answer go up through the coordinator, one at a time, and
the answer is recorded verbatim, marked RELAYED, where the question lives.

## Merge notes

This branch and the M7 lane both append to `docs/decision-register.md`, both
create `docs/work-logs/2026_10-work_logs/2026_10_22-work_log.md`, and both
regenerate `docs/work-logs/INDEX.md`. At merge: keep both appends in order,
keep both day-file entries, regenerate the index with
`tools/work-log-index --write`. Nothing here builds, touches a device, a
cloud or the M7 build worktrees.

- **This branch carries three of M7's commits as cherry-picks** (`-x`, 2026-10-23
  16:30 UTC): `033eb7ed23`, `0ceb2994c5`, `6874394d49` from `fac2129787`,
  `1c7d283ad5`, `a7a3bdda4e` on `feature/m7-audit-integration-603` (the
  Argon reviewer route and its pins, #636/#638). When the M7 candidate merges
  to `next` first, the merge of this branch sees them as duplicate patches;
  expect a clean or trivially identical resolution in `scripts/council-invoke.ts`,
  `tools/lint-audit-artifacts`, `verifier-pins.json`, `council-seat-efforts.json`
  and the two `docs/qa-logs/2026-10-22-*-638/` folders, and check for markers.
## State at 2026-10-23 (the coordinator's own update)

P0 is done on this branch; its merge waits on the M7 lane's post-candidate
merge (never `--no-verify`). P1's pass-7 gate: question 1 settled
(D-WORKFLOW-185/186), question 2 withdrawn (D-WORKFLOW-187: the renovation
gates no release), question 3 settled by D-WORKFLOW-184; the maintainer's yes
on the order's fourth version (`eb4763e3cc`, ledgers `00ca350666`) was given
on 2026-10-23 and relayed; P1 wrote the order's register row on its branch
(the next ID above 187). The question who authors the slice issues was
answered 2026-10-23 with a general rule, D-WORKFLOW-189: planning, the
division of work, the definition of work items and roadmap changes are this
lane's; a work lane executes. So the 46 slice issues are this lane's to file,
from P1's renderer (`tools/renovation-inventory --slice-issues DIR`, run
read-only against P1's tree into this lane's scratchpad). #644 and #645 are
the build-path read and its PR-process findings. The 46 are filed: #648 (T1) to #693
(T46), sub-issues of #339 on milestone M6, `tools/box-check` 0 fail over all
open issues (work log 05:40 UTC). P1 was accepted at hand-back and #641
closed completed on 2026-10-23 (P1's branch at `2174265e9c`; it merges to
`next` after this branch, after the M7 candidate). T1 is dispatched (2026-10-23): the area
epic #695 with its futro; the brief `docs/reviews/briefs/os-launch-control-state.md`
at version 2 (`968ba95993`); the lane `feature/m6-os-launch-control-state-648`
at `4228561fd2`, worktree `distribution.worktrees/m6-os-launch-control-state-648`,
an Opus 5.5 session at high effort in Herdr pane `wN:p4`, agent
`m6-t1-os-launch` (started from this pane: `herdr tab create --workspace wN
--cwd <worktree> --label ... --no-focus`, then `herdr agent start <name>
--kind claude --pane <id> -- --model claude-opus-5-5 --effort high`, then
`herdr agent prompt <name> "<seed>"`; the seed is kept in this session's
scratchpad and quoted in the 07:50 work-log entry). This lane's rules from
the futro: no merge of `next` into a slice branch between stage A and stage
D; every drift report read at every slice close and the re-open named;
`tools/box-check` on every issue a lane files, at the pause. Next: T2's brief (`docs/reviews/briefs/es-launch-path.md`), proven like T1's,
then the interface area epic, the ES worktree for the lane at the pin, the
lane cut from P1's tip with this tip merged, and dispatch: the maintainer's
call of 2026-10-23 is that T2 runs beside T1 (D-WORKFLOW-190, work log 16:30
UTC). T1 is past its Phase 4.6 blocker: the Argon route is on this branch as
three cherry-picks (`033eb7ed23`, `0ceb2994c5`, `6874394d49`; M7's
`fac2129787`, `1c7d283ad5`, `a7a3bdda4e`), the lane merges `6874394d49` and
runs the Argon seat; then its stage-D pause (write the stream briefs; F-21,
F-45, F-49 are a merge of upstream commits, F-14 and F-03 wait for the M7
bytes, F-68 is D-SYS-014); T1's drift re-open when the M7 candidate lands.

## The seed brief (2026-10-22, the planning session's handoff, verbatim)

The first message this lane received, pasted by the maintainer from the P0
planning session; kept here because the maintainer asked that the lane consult
it at each step (*"You should have a copy of the original seed I provided for
this exercise"*). The intent it serves is D-WORKFLOW-181's, in the maintainer's
words there.

> Started by the P0 planning session (Claude Fable 5.1, Herdr pane wN:p1, tab "P0 planning (#346)") on the maintainer's direction of 2026-10-22. You are the M6 coordinator lane (D-WORKFLOW-183): the renovation program's planner, brief-writer, gate-acceptor and integrator, running on Fable; the work lanes run on Opus 5.5. Your worktree is /workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346 on feature/m6-renovation-plan-346; the primary checkout /workspace/repos/pixelelated/distribution stays on next with no resident session, and you are its keeper. Read first, in this order: .github/sessions/saved-session-state-feature-m6-renovation-plan-346.md (your lane's pointer), docs/reviews/plan-for-the-plan.md, the live M6 milestone body, issues #346, #641 and #640 on pixelelated/distribution, then next:AGENTS.md and the every-session rules. The maintainer's direction, verbatim: "the coordinator will be Fable and the work will be Opus 5.5" and "we begin our work and ensure that everything is in the new work tree with the seeded session file to resume, and that there's a corresponding branch. We can then begin work there." Gates: nothing merges to next until the M7 lane's post-candidate merge clears the push guard, and never with --no-verify; the P1 lane (Herdr tab "P1 Survey (#641)", agent m6-p1-survey, worktree m6-p1-survey-641) pauses at its pass-7 gate on #641 for the maintainer's yes, which reaches it through you, one question at a time; you accept P1 at hand-back against brief section 10; one session per worktree, so never write in the P1 worktree. Report on #346 and #641. First action: read your pointer and the plan, confirm on #346 in one comment that you have resumed (your session id from herdr agent list, this pane, the time), then wait for P1's pass-7 post or the maintainer; do not start new work streams on your own.  Also: append this lane start to docs/work-logs/2026_10-work_logs/2026_10_22-work_log.md in your worktree (the planning session writes there no longer, one session per worktree), run tools/work-log-index --write, commit with Refs #346 and push; and note on #346 that Claude Code reports the 25 instruction files at 324.2k characters, over its 150k limit, so the rules load truncated in every lane, a finding for the doctrine slice.

