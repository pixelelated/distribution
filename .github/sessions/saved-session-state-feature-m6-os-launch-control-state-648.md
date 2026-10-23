# Session pointer: M6.P2 T1, the OS scripts: launch, control and state (#648)

> **Seeded:** 2026-10-23 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file at every checkpoint
> **Branch:** `feature/m6-os-launch-control-state-648`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tip merged in at `86d3a49f6c`
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-os-launch-control-state-648`
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (the fresh clone, D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only
> **Repository:** `pixelelated/distribution`; integration branch `next`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort unless #648 says otherwise
> **Epic:** #695 (the OS scripts and launch path); the renovation epic #339; the milestone M6

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   this worktree's rules are `next`'s except two files P1 extended
   (`fork-workflow.md` and `instruction-files.md`, the three renovation
   tools added to the fork-tool lists): `git diff --stat next -- .claude
   CLAUDE.md AGENTS.md` lists exactly those two; anything else is STALE.
   Known stale facts in the rules are listed in the brief § 1 and § 3; this
   lane's layout is the brief's, not `worktrees.md`'s.
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/os-launch-control-state.md` whole. The brief is the
   work; its § 7 is the contract, identical to the checklist on #648.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #648 (with its comments), #695 (the area epic, with its futro comment),
   #339 and #346. The M7 lane's canonical checkpoint
   `.github/sessions/saved-session-state-next.md` is read for what runs on
   this host, not for a work queue; this lane never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-os-launch-control-state/00-running-log.md`
   and write stage A (the hashes, the counts, the image's BUILD_ID) before
   reading a line of the slice.

## Current focus

**Stage A done (2026-10-23, executor `m6-t1-os-launch`, session
`33bed370`, pane `wN:p4`).** Audit folder
`docs/audits/2026_10_23-epic-m6-os-launch-control-state/`: `00-running-log.md`
(the resume point: read its last entry first), `01-research-notes.md` § Scope.
Counts equal the brief's (83, 13,327, 29/54); `upstream/next` is `8b70f693b8`;
the guest's BUILD_ID is `069fc270442134fe771258418adf4e666e0473fb`; the
image's `/bin/sh` is **bash**, not dash (reported on #648). Next: stage B,
Phase 1 (the open issues, the prior punch lists as provenance, git history),
then Phase 2's coverage table, group 1 first.

**The lane's guest** (up while the slice needs it): QEMU pid in
`/workspace/artifacts/m6-t1-20261023/qemu.pid`, serial
`$A/serial.sock`, monitor `$A/monitor.sock`, SSH `-p 10032 -i $A/qa-key`,
VNC :19, disk `$A/t1.qcow2`. Stop it by its pidfile only
(`tools/vm-stop` or `kill "$(cat $A/qemu.pid)"`); never by pattern.
shellcheck v0.11.0 at `.qa-scratch/shellcheck-v0.11.0/shellcheck-v0.11.0/shellcheck`.

**Stage B, Phase 2 in progress (checkpoint `26a676d12c`, 07:46 UTC).** Done:
Phase 1 (`01-research-notes.md` § 1.1-1.6); in `02-forward-audit.md` the image
vs tree sweep (78 same; `runemu.sh`, `system.cfg`, `motd` differ), the
mechanical checks (all 0 except `time-to-play`'s expected no-cloud 1;
`vocabulary-check` reads none of this slice), shellcheck's 16 errors as
leads, **group 1 read whole** (F-01 to F-27) and its guest proofs (nine
findings proven). Next: group 2 (state: `chksysconfig`, `post-update`,
`factoryreset`, `installtointernal`, `automount`, `system.cfg`, the
autostart fragments 001/003/007, `setrootpass`, three units), then group 3,
then the 83-row coverage table, the Q5/Q6/Q4 work, Phase 3 and 4.
**A proof script restores explicitly, never from an EXIT trap** (`wait_lock`
replaces it: F-22), and checks a file bind in `/proc/self/mountinfo`.

**Stage B through Phase 4.5 done; Phase 4.6 in progress (08:27 UTC).**
68 findings (0 Critical, 0 High, 19 Medium, 49 Low) in `02`/`04`; the
coverage table (83 rows), Q4 (43 commits), Q5 (0.64 s / 1.01 s;
`setsettings.sh` 127 ms), Q6 (47 rows) done; `03` written. The Astra
refutation pass runs under `tools/watch-build --record-only`
(`.build-runs/20261023T082647Z-e7167ae6/`), output
`second-opinions/gpt-audit.md` + `.provenance.json`. **Then the Phase 4.6
blocker:** the Gemini 4 Argon route is absent (`grep -c gemini-argon
scripts/council-invoke.ts tools/lint-audit-artifacts` = 0, 0); grade the
Astra items into `04` § Second opinion, record Argon pending, post the
blocker on #648 and stop -- no Phase 5, no issues, until the coordinator
brings `1c7d283ad5` + `a7a3bdda4e` or the M7 merge lands. Open on #648:
the rehearsal question (issuecomment-6360655911).

**Stopped at the Phase 4.6 blocker (08:43 UTC).** The Astra pass is done and
graded in `04-analysis.md` § Second opinion: provisional **75 (0 Critical, 2 High
F-14/F-67, 22 Medium, 51 Low)**, G-01 to G-07 new. The Argon seat is `pending` in
`review-plan.json`. Resume only when the coordinator brings `1c7d283ad5` +
`a7a3bdda4e` (or the M7 merge lands): then run the Argon probe and refutation
from the same brief (`second-opinions/gpt-brief.md`'s packet plus the Astra
grades), grade them, and go to Phase 5 (punch list with `punch_index` and
`question:` rows, F-10/F-43 split, the audit issue, bug issues, `box-check`),
then the stage-D pause. The guest stays up.

**Paused at stage D (16:50 UTC, `date -u`; the running log's last entry).** Phase 4.6 is complete: Astra and Argon both ran, verified, and are graded in `04` § Second opinion. Final: **81 findings (0 Critical, 2 High F-14/F-67, 22 Medium, 57 Low)**; `05-punch-list.md` has 84 items (F-10, F-43 and A-11 split). Audit issue **#701** (sub-issue of #648); bug issues **#702 to #761**, one per defect, all `box-check` 0 fail. **The guest is down** (stopped 16:37:49 for M7's host handoff, `t1.qcow2` kept): start no runtime until the coordinator posts `resource return` on #648. Next: wait for the coordinator's stream briefs (stage E); each stream works its items test-first on this branch unless its brief says otherwise; Phase 7 outcomes go in `05`'s gate and on #701.

## Next commands

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-os-launch-control-state-648
git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md          # exactly fork-workflow.md and instruction-files.md
git diff --quiet next HEAD -- projects/ROCKNIX/packages/rocknix/ && echo "slice paths equal next's"
sed -n '1,120p' docs/reviews/briefs/os-launch-control-state.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then this branch. When
`next` moves, the **coordinator** merges `next` into this branch, and never
between stage A and stage D (the read must stay a fact about one hash,
plan § 8); after stage D a merge re-baselines the slice over the diff,
recorded on #648. Never merge another lane's feature branch here. This
branch, the P0 and P1 branches and the M7 lane all append to
`docs/decision-register.md`, the day's work log and `docs/work-logs/INDEX.md`:
keep every append, regenerate the index, never edit another lane's rows;
a merge with conflicts is checked for leftover markers before it is
committed (#696). The highest register ID on 2026-10-23 is D-WORKFLOW-189
(the M7 lane holds 171 to 180 unmerged); a new row goes at the end of
`## Decided`. The M7 candidate's `runemu.sh` change (`next..069fc2704421`
in the legacy checkout) is expected drift: when it lands on `next`, the
coordinator reads `tools/renovation-drift`'s report and re-opens this slice
over the diff at its depth. Nothing here builds, touches a device, a cloud,
or another lane's worktree.
