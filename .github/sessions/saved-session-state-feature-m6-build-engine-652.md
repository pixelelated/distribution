# Session pointer: M6.P2 T5, the build engine (#652)

> **Seeded:** 2026-10-24 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file at every checkpoint
> **Branch:** `feature/m6-build-engine-652`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tip `01ff4c0bcd` merged in at `dcd70698f1` (the brief at version 2, the epic's futro, the Argon route, T1's, T2's and T3's briefs)
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-652` -- the only worktree of this lane; no EmulationStation path is in the slice
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (the fresh clone, D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only (a build root's install tree, a `.build-runs/<id>/` record, a diff; never a write, never a process started there). The T1, T2 and T3 worktrees beside this one (`m6-os-launch-control-state-648`, `m6-es-launch-path-649`, `m6-emulators-libretro-650`) and T2's EmulationStation worktree are other lanes': read with `git -C`, never write
> **Repository:** `pixelelated/distribution` (integration branch `next`; every `gh` call carries `--repo pixelelated/distribution`)
> **Executor:** Opus 5.5 at high effort unless #652 says otherwise
> **Epic:** #800 (the build engine: T5, T6); the renovation epic #339; the milestone M6. T3 (#650) runs beside this lane in its own worktree (D-WORKFLOW-190); T1 and T2 are accepted and idle

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   this worktree's rules are `next`'s except four files (P1's
   `fork-workflow.md` and `instruction-files.md`; the coordinator's
   `generic-x64-vm-testing.md` paragraph on `time-to-play`'s reboot; M7's
   `.claude/skills/council/IMPORTED-FROM.md`, which came with the Argon
   route): `git diff --stat next -- .claude CLAUDE.md AGENTS.md` lists
   exactly those four; anything else is STALE. Known stale facts in the
   rules are listed in the brief § 1 and § 3; this lane's layout is the
   brief's, not `worktrees.md`'s.
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/build-engine.md` whole (version 2). The brief is
   the work; its § 7 is the contract, identical to the checklist on #652.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #652 (with the dispatch comment), #800 (the area epic, with its futro
   and the futro's errata in the file), #339, #346, #644 and its
   `docs/reviews/build-path-read.md` (nine of its findings are this
   slice's), #801 and #802 (two bugs the coordinator filed on 2026-10-24
   that touch this slice's neighbourhood), the hand-backs on #648 and #649,
   and T3's comments on #650 (its F-06 is this slice's function). The M7
   lane's canonical checkpoint `.github/sessions/saved-session-state-next.md`
   is read for what runs on this host, not for a work queue; this lane
   never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-build-engine/00-running-log.md` and
   write stage A (the hashes, the counts with the tool's code-class set,
   the upstream ref, the host file's state) before reading a line of the
   slice.

## Current focus

**Idle (2026-10-24 07:20 UTC): T5 accepted by the coordinator on #652; the audit closed.**
- **Status:** #837 closed as completed. `docs/audits/2026_10_24-epic-m6-build-engine/audit-completion.json` was written from its closed readback (completed 07:20:05 UTC) and is accepted by `tools/ceremony-check`'s validator. `tools/lint-audit-artifacts` on the folder prints `PASS`.
- **Commits:** `reviewed-at` `46f6c7d428`, `fixed-at` `877775e61e` (in #652's body).
- **Work done:** streams E1 to E8 and E5b, each accepted on #652. The ten `bug` issues #827 to #836 stay open for the coordinator, who closes them after the integration's first image proves the `fix-pending-image` halves.
- **What the lane waits for:** nothing. The merge to `next` (the engine's fixes last), the launch table's regeneration after T3's S2, and the zero-default case made fatal are the coordinator's. Nothing runs in this lane: no guest, no compiler, no watched run, no waiter.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-652
cd "$D" && git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md          # exactly the four files above
grep -c 'Renovation face' tools/lint-audit-artifacts; grep -c gemini-argon tools/lint-audit-artifacts   # 4 and 4
ls "$(git config core.hooksPath)"                             # must list pre-push
tail -3 /tmp/m7-m6-host-coordination-20261023.txt            # the host's state
sed -n '1,160p' docs/reviews/briefs/build-engine.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then the T1, T2 and T3
branches, then this branch **last** (the engine's fixes after the slices
whose proofs the first build carries, so a failing build is attributable);
the coordinator merges. When `next` moves, the **coordinator** merges `next`
into this branch, and never between stage A and stage D (the read must
stay a fact about one hash, plan § 8); after stage D a merge re-baselines
the slice over the diff, recorded on #652. Never merge another lane's
feature branch here. This branch, the P0, P1, T1, T2 and T3 branches and
the M7 lane all append to `docs/decision-register.md`, the day's work log
and `docs/work-logs/INDEX.md`: keep every append, regenerate the index,
never edit another lane's rows; a merge with conflicts is checked for
leftover markers before it is committed (#696), and a union of two ledgers
is made by whole entries, never by an unanchored pattern over marker-shaped
text (the coordinator's merge `dcd70698f1` did exactly that for the
friction log and the 23rd's work log). The register on this branch holds
P1's D-WORKFLOW-188 and 189 and the coordinator's 190 to 192 (191 is an
open row), 660 IDs each once; T3's branch carries the same set and may add
193 beside this lane; **the next Decided row is 193**, checked on every
branch at the time, and goes at the end of `## Decided`. Nothing here
builds, touches a device, a cloud, or another lane's worktree or guest; a
change that alters what a build does waits for a stream brief that names
the build proving it (brief § 5); the container pin, the admission and the
watcher are the coordinator's, T9's and T10's.
