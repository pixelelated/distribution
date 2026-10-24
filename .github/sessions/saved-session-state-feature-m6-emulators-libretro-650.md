# Session pointer: M6.P2 T3, RetroArch and the libretro cores (#650)

> **Seeded:** 2026-10-24 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file at every checkpoint
> **Branch:** `feature/m6-emulators-libretro-650`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tip `f650d65522` merged in at `16778b5f61` (the brief at version 2, the epic's futro, the Argon route, T1's and T2's briefs)
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-libretro-650` -- the only worktree of this lane; no EmulationStation path is in the slice
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (the fresh clone, D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only (an image, a build root, a diff). The T1 and T2 worktrees beside this one (`m6-os-launch-control-state-648`, `m6-es-launch-path-649`) and T2's EmulationStation worktree are other lanes': read with `git -C`, never write
> **Repository:** `pixelelated/distribution` (integration branch `next`; every `gh` call carries `--repo pixelelated/distribution`)
> **Executor:** Opus 5.5 at high effort unless #650 says otherwise
> **Epic:** #798 (the emulators and cores: T3, T30, T24); the renovation epic #339; the milestone M6. T1 (#648) and T2 (#649) are accepted and idle; no other M6 lane runs beside this one at dispatch

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
   `docs/reviews/briefs/emulators-libretro.md` whole (version 2). The brief
   is the work; its § 7 is the contract, identical to the checklist on #650.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #650 (with its comments), #798 (the area epic, with its futro and the
   futro's erratum as comments), #339, #346, and the two accepted lanes'
   hand-backs on #648 and #649 (their audits are the other sides of this
   slice's table; the brief § 2 and § 3 say where). The M7 lane's canonical
   checkpoint `.github/sessions/saved-session-state-next.md` is read for
   what runs on this host, not for a work queue; this lane never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-emulators-libretro/00-running-log.md`
   and write stage A (the hashes, the counts, the upstream ref, the host
   file's state) before reading a line of the slice.

## Current focus

Not started. The first commit on this branch is the running log's header,
`01-research-notes.md` § Scope, this pointer updated, and the day's
work-log entry headed `#650`. **The host:** the M7 lane returned it at
02:22 UTC on 2026-10-24 (last block when this pointer was seeded:
`== M6 coordinator — 02:23 UTC: resource return read (both H700 and SM8550 builds and their`); a later M7 window is requested five minutes ahead in
`/tmp/m7-m6-host-coordination-20261023.txt` and relayed on #650 by the
coordinator, and while one is open this lane runs no guest, no compiler and
no `npm install` (brief § 5).

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-libretro-650
cd "$D" && git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md          # exactly the four files above
git diff --quiet 8ebaf8daad HEAD -- projects/ROCKNIX/packages/emulators/libretro projects/ROCKNIX/packages/virtual/emulators && echo "slice bytes are next's"
ls "$(git config core.hooksPath)"                             # must list pre-push
tail -3 /tmp/m7-m6-host-coordination-20261023.txt            # the host's state
sed -n '1,140p' docs/reviews/briefs/emulators-libretro.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then the T1 and T2
branches, then this branch; the coordinator merges. When `next` moves, the
**coordinator** merges `next` into this branch, and never between stage A
and stage D (the read must stay a fact about one hash, plan § 8); after
stage D a merge re-baselines the slice over the diff, recorded on #650.
Never merge another lane's feature branch here. This branch, the P0, P1, T1
and T2 branches and the M7 lane all append to `docs/decision-register.md`,
the day's work log and `docs/work-logs/INDEX.md`: keep every append,
regenerate the index, never edit another lane's rows; a merge with conflicts
is checked for leftover markers before it is committed (#696), and a union
of two ledgers is made by whole entries, never by an unanchored pattern over
marker-shaped text (the coordinator's merge `16778b5f61` did exactly that
for the friction log and the 23rd's work log). The register on this branch
holds P1's D-WORKFLOW-188 and 189 and the coordinator's 190 to 192 (191 is
an open row), 660 IDs each once; the T1 and T2 branches carry 188 to 191;
**the next Decided row is 193**, checked on every branch at the time, and
goes at the end of `## Decided`. Nothing here builds, touches a device, a
cloud, or another lane's worktree or guest; a pin bump is never a fix on
this branch without a stream brief (brief § 5).
