# Session pointer: M6.P2 T24, emulator recipes and files no shipped image builds (#671)

> **Seeded:** 2026-10-24 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file at every checkpoint
> **Branch:** `feature/m6-emulators-dead-ends-671`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tip `c25d772b21` merged in at `8fd13c3133` (whose work-log index carried conflict markers until the next commit; nothing else in it was touched)
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-dead-ends-671`; the T3 and T30 worktrees beside it (`m6-emulators-libretro-650`, `m6-emulators-standalone-677`) are this session's earlier slices, accepted and idle until their merges: nothing is written there
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, `ls` of their `build/` directories is the one read this slice makes
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T3 session, `m6-t3-emulators`), unless #671 says otherwise
> **Epic:** #798 (the emulators and cores); the renovation epic #339; the milestone M6; beside T8 (#655) in the other lane (D-WORKFLOW-190)
> **Depth:** Local -- no reviewer, no Facilitator call, no `npm install`; the review plan carries `tier_exception: D-WORKFLOW-184` (#810); nothing here changes a file (a dead-end table)
> **Budget:** the GitHub API (5,000 calls an hour, shared with the coordinator's monitors); the brief's loops read `gh api rate_limit` before and after and start only above 1,500 remaining

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   this worktree's rules are `next`'s except the seven paths the brief § 1
   names: `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`
   lists exactly those; anything else is STALE. Known stale facts in the
   rules are listed in the brief § 1 and § 3; this lane's layout is the
   brief's, not `worktrees.md`'s.
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/emulators-dead-ends.md` whole (version 2).
   The brief is the work; its § 7 is the contract, identical to the
   checklist on #671. Its first commands include the at-hash export under
   `.qa-scratch/t24/`; a tree export never goes under `/tmp`.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #671 (with its comments), #798 (the epic, with its futro comment and
   the T24 addendum), #650 (T3, accepted: its `04` § Q6 names this slice's
   five ROCKNIX recipes with their `Already written:`), #677 (T30,
   accepted: #857 and #873 are the launch table's side of the same
   emulators), #585 (where the proposal about the 83 LibreELEC files
   lands), #644 (finding 24's class). The M7 lane's canonical checkpoint
   `.github/sessions/saved-session-state-next.md` is read for what runs on
   this host; this lane never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-emulators-dead-ends/00-running-log.md`
   and write stage A before reading a row of the slice.

## Current focus

**Stage A done (2026-10-24 13:41 UTC; the executor; `b7ac3b087b`).** The
audit folder is `docs/audits/2026_10_24-epic-m6-emulators-dead-ends/`:
`00-running-log.md` (Phase 0 and Stage A) and `01-research-notes.md`
§ Scope.
- The membership matches the brief exactly: 86 paths, 2,399 lines, 84
  `unreached` and 2 `unshipped`, 85 recipes and 1 cmake file.
- The fork changed none of them. 81 are identical to `upstream/next` and
  5 differ by `af70bd435b`.
- The branch differs from `8ebaf8daad` on none of the 86, so
  `reviewed-at: 81331b499e`.
- `upstream/next` moved during the stage-A fetch, from `e0f9deb899` to
  `481c9d0d75` (heroic only). The (a) loop records both heads.

**Next is stage B**: brief § 5's host-side checks, in this order:
1. the (a) loop;
2. the (b) LibreELEC master loop: 80 serial reads, the budget read
   before and after, `libretro-snes9x` as the control;
3. the three `viewplan` reads, with `snes9x-lr` as the control;
4. the metapackage and `git grep` reads;
5. the record by name prefix over the five M7 roots, and the `.info`
   trace;
6. the two `pkgcheck` runs;
7. the weight.

After that come `02` to `04`, then the lint (`--phase pre-issue`), then
the stage-D punch list and the pause. No runtime of any kind; the host is
M6's, and this slice does not touch it.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-dead-ends-671
cd "$D" && git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the seven paths
test -f docs/reviews/inventory.json && echo inventory
gh api rate_limit --jq '.resources.core.remaining'
sed -n '1,140p' docs/reviews/briefs/emulators-dead-ends.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, then this branch, the two checksum packets
(#877, #890), T5, T6, T7, T8, then T4's. When `next` moves, the **coordinator**
merges `next` into this branch, and never between stage A and stage D (the
read must stay a fact about one hash, plan § 8); after stage D a merge
re-baselines the slice over the diff, recorded on #671. Never merge another
lane's feature branch here. This branch, the P0, P1 and the other lanes'
branches and the M7 lane all append to `docs/decision-register.md`, the
day's work log and `docs/work-logs/INDEX.md`: keep every append, regenerate
the index, never edit another lane's rows; a merge with conflicts is checked
for leftover markers before it is committed (#696), and a union of two
ledgers is made by whole entries, never by an unanchored pattern over
marker-shaped text. The highest Decided register ID on 2026-10-24 is
D-WORKFLOW-198 (the coordinator's); T8 runs beside this lane and may take
199: check both branches; a new row goes at the end of `## Decided`.
Nothing here builds, touches a device, a cloud, a guest, the shared source
cache (read only), or another lane's worktree.
