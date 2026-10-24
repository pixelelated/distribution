# Session pointer: M6.P2 T30, the standalone emulators (#677)

> **Seeded:** 2026-10-24 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file at every checkpoint
> **Updated:** 2026-10-24 by the executor (the T3 session, `m6-t3-emulators`), at stage E (S0 done, S1 next)
> **Branch:** `feature/m6-emulators-standalone-677`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tip merged in at `f606d29bef`
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-standalone-677`; the T3 worktree `m6-emulators-libretro-650` beside it is this session's earlier slice, accepted and idle: read only until the merge (its audit folder's tools are copied from there by path)
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there (the three install trees the brief § 5 names are read with `ls`)
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T3 session, `m6-t3-emulators`), unless #677 says otherwise
> **Epic:** #798 (the emulators and cores); the renovation epic #339; the milestone M6; beside T6 (#653) in the other lane (D-WORKFLOW-190)
> **Depth:** Extended -- GPT-6 Astra at `max` and Gemini 4 Argon at `high` through the Facilitator, as T3's Phase 4.6 ran them; the dispatch comment authorizes the two calls
> **Guest:** the GENERIC_X64 image `069fc2704421` (the M7 root's, read only), VNC display 24, SSH 10037, pidfile `/workspace/tmp/m6-t30/qemu.pid`; only while M6 holds the host (the coordinator relays), census before, `tools/vm-stop` after

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   this worktree's rules are `next`'s except the seven paths the brief § 1
   names: `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`
   lists exactly those; anything else is STALE. Known stale facts in the
   rules are in the brief § 1 and § 3.
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/emulators-standalone.md` whole (version 2). The
   brief is the work; its § 7 is the contract, identical to the checklist
   on #677. A tree export never goes under `/tmp`.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #677 (with its comments), #798 (the epic, with its futro and the T30
   addendum), #650 (T3, accepted: its audit's tools, Q4 method and
   dispositions are this slice's starting point), #648 (T1: `runemu.sh`'s
   standalone arms and F-24), #825 (the shell-line class), #520 (the
   standalone save layout). The M7 lane's canonical checkpoint
   `.github/sessions/saved-session-state-next.md` is read for what runs on
   this host; this lane never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-emulators-standalone/00-running-log.md`
   and write stage A before reading a line of the slice.

## Current focus

**Stage E: the streams of `docs/reviews/briefs/t30-streams.md` at `bf8184e494`** (on `feature/m6-renovation-plan-346`; read with `git show`, never merged), S0 to S5 in order. **S0 is done** (`787daa65bd`..`6894bfd3cd`; PL-007 and PL-008 fix-guest, PL-018, PL-019 and PL-031 by fixture). **Next: S1**, the `link_storage_dir` helper (a new file under `projects/ROCKNIX/packages/rocknix/sources/scripts/`, authorised) and the nine link sites. Stages A to D are done. Audit folder: `docs/audits/2026_10_24-epic-m6-emulators-standalone/` (00-05, second-opinions, tools).
- Punch list: #872, 41 items (2 High, 16 Medium, 23 Low; PL-013 re-graded Low by the coordinator, the mirror fact).
- Bugs: #853 to #871.
- The lint: `PASS pre-issue artifacts`.
- Proofs: 21 (16 on the guest in three cycles, 5 on the host).
- Phase 4.6: both seats graded; Gemini's on a trimmed packet (D-WORKFLOW-195).

Each stream: the test first, seen to fail, then a commit per script with `Refs`; a guest cycle named on #677 before its boot; the Phase 7 rows at the stream's end; one hand-back comment on #677, then straight on. The retro draft is `docs/retros/2026-10-24-m6-emulators-standalone.md`. `reviewed-at` candidate `c7e3dfcc87`.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-standalone-677
cd "$D" && git status --short && git log --oneline -3
gh issue view 677 --repo pixelelated/distribution --comments | tail -40   # the stream briefs
A=docs/audits/2026_10_24-epic-m6-emulators-standalone
python3 -I $A/tools/set-outcome.py $A/tools/punch-items.py PL-NNN resolved - "<note with commit>"   # Phase 7 outcomes
```

## Merge notes

Merge order after the M7 candidate: P0, P1, T1, T2, T3, then this branch
(with T3's, the area's), T5, T6, T4; the ledgers united by whole entries.
When `next` moves, the **coordinator** merges `next` into this branch,
never between stage A and stage D. Never merge another lane's feature branch
here. The highest register ID on 2026-10-24 is D-WORKFLOW-194 in the Decided
table; T6 runs beside this lane and may take 195: check every pushed branch
before writing a row, at the end of `## Decided`. A commit names its paths;
`git status --short` is read before each commit as well as after. Nothing
here builds, touches a device, a cloud, or another lane's worktree; a
guest runs only as the brief § 5 says.
