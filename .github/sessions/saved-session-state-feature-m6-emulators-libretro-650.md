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

**Updated 2026-10-24 ~03:45 UTC by the executor (Opus 5.5, session `a6d65411`, pane `wN:p6`).**

**Stage B, Phase 2, mid-read.** `reviewed-at: d606301784` (the slice's bytes equal `8ebaf8daad`). The audit folder is `docs/audits/2026_10_24-epic-m6-emulators-libretro/`.

Written so far:

- `00` (the running log) and `01` (§ Scope, Phase 1).
- `02` with the mechanical checks done:
  - wrapper test, plain and `--gated`, with both constructed failures;
  - `pkgcheck` 152 runs;
  - shellcheck over 30 files;
  - the table parse, and the host regeneration (`tools/regen-es-systems.sh`), byte-identical to the GENERIC_X64, H700 and SM8550 images;
  - the rotation generators, byte-identical;
  - the `FetchContent` grep.
- Q4 (b) `tools/q4-pins.py` (151 rows) and Q4 (c) `tools/q4c-patches.sh`, at the pin and at master. Q4 (a) is partly done: the `merge-tree` preview, five conflicts, F-09.
- Guest proofs P1, P2, P3, P3b, P4 (criterion 12: `proved:` 5 = `GUEST-PROOF:` 5). The guest is down.
- Findings F-01 to F-15.

Bugs: #799 (the wrapper test's roots, fixed `d606301784`) and #802 (filed by the coordinator: the default PSX core, F-08/F-09).

The coordinator's rulings, read on #650:

- F-07 (aethersx2): `to merge`, class 1, with the base merge.
- F-06: routed to T5 (#652).
- #802: references only; the fix comes with the base merge.

**The host:** an M7 window opened at 03:47 UTC (#650 comment 6379424513). No guest, no compiler, no `npm install` until the coordinator relays the return on #650. Reading, `gh api`, `pkgcheck`, shellcheck and the host sandbox continue.

## Next commands

The rest of stage B, in order:

1. **Group 3:** the fork's own core recipes, each `git log -p` and the delta against `upstream/next`; `easyrpg-lr`'s three sub-recipes; the two rotation-table generators read whole.
2. **Group 2:** `virtual/emulators/package.mk`'s GENERIC_X64 arms and the `X64_SKIP_CORES` comment (#16 is closed); `Install Steam.sh` read structurally, every finding `deferred:M7-merge`; the 24 `sources/*.sh` against `PKG_EMUS`.
3. **The remaining widget patches:** 0014, 0016, 0019.
4. **Q4 (a):** the 14 dispositions.
5. **The Q6 tables:** 131 recipes, 142 systems (from `.qa-scratch/t3-regen/<DEVICE>`), 24 scripts, 15 source sets, 21 patches.
6. **The `02` coverage table** (344 rows: ``grep -c '^| `projects/ROCKNIX/packages/' 02`` must print 344).
7. **The fifteen criterion entries.**
8. **`03`, then `04`** with the renovation face.

Then Phase 4.6, after the return line: `npm install --prefix tools/council`, `tools/council/run verify-pins`, `tools/council/run test`, a probe per seat, Astra (`--member gpt`, max) and Argon (`--member gemini-argon`, high). Then `05`, the lint with `--phase pre-issue`, the audit issue, and the stage-D pause.

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
