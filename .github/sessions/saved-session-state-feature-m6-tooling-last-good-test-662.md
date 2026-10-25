# Session pointer: M6.P2 T15, the last-good scripts test (#662)

> **Seeded:** 2026-10-24 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014: two lanes' pointers lagged a dozen streams on 2026-10-24)
> **Branch:** `feature/m6-tooling-last-good-test-662`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tips merged in (`b14c7ba207` at `1d1a33785e`, then `269a552a0b` at `5b91668d8c`)
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-last-good-test-662`; the T3, T30, T24, T4, T10 and T14 worktrees beside it (`m6-emulators-libretro-650`, `m6-emulators-standalone-677`, `m6-emulators-dead-ends-671`, `m6-doctrine-rules-651`, `m6-tooling-guards-657`, `m6-tooling-state-tests-661`) are this session's earlier slices, accepted and idle: read only, until their merges -- T14's four fixed tools are read with `git show 7c1d729b57:tools/<name>`, never run from its worktree
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there -- this slice reads one file there, a GENERIC_X64 build root's `image/system/usr/bin/busybox`, through `QA_SYSTEM_ROOT`, which the suite copies into its own run
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T3 session, `m6-t3-emulators`), unless #662 says otherwise
> **Epic:** #903 (the tooling and guards: T9, T10, T12 and T14 accepted; this slice; then T45); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- one GPT-6 Astra seat at `max` through the Facilitator (a probe, then one refutation over one packet of excerpts, scanned before it is sent; D-WORKFLOW-184, 195; a failed seat is a hold); `npm install` only under `tools/council`
> **The lens:** brittleness -- Q6's table (34 sections: what each depends on that is not the thing it proves, what its absence does, the last catch, the caller, the positive), Q3's hunt (the busybox split from two runs at the hash, the five `--old` controls, the `check $?` and `|| true` sites), and the file's split as a Q7 lead; the lens is not a licence to delete
> **The host:** M6's; this slice runs **no guest**, no build, no handheld action, no cloud test against anything real; its suite runs start in the foreground or with `setsid -w`, with `TMPDIR` under `/workspace/tmp/m6-t15/`, never `/tmp` and never a path under the worktree
> **Not this slice's to edit:** the scripts the file proves (a `bug` for their lane), T14's four tools (`7c1d729b57`), `tools/vm-qa` (T12's), any rule or decided register row

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   this worktree's rules are `next`'s except the paths the dispatch comment
   on #662 lists: `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`
   prints exactly those; anything else is STALE. `engineering-practices.md`
   § Guards must fail closed and `upgrade-and-install.md` § Verify on a
   device, not on the host (blindspot 34) are the two rules this file serves.
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/tooling-last-good-test.md` whole (version 2). The brief
   is the work; its § 7 is the contract, identical to the checklist on #662;
   its § 5 gives the two stage-A runs and the five `--old` recipes; its § 8
   names what is never run here.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #662 (with its comments), #903 (the epic, with its futro comment and the
   T15 addendum: U-1 to U-6 and A1 to A7), #339, #346 (the maintainer's
   channel: what is open there is not this lane's to decide), #1015 (T12's
   bug: the 319 FAILs and the busybox lead), #997 and #999 (T14's contract
   for the two writer tests and the fixture's `--config`), #661 and #659
   (the two accepted slices whose runs of this file are the record), #657
   (T10's retro: the five fail-open shapes), #640 (the legacy paths), #962
   (the fixture literal at `:8004`). The M7 lane's canonical checkpoint
   `.github/sessions/saved-session-state-next.md` is read for what runs on
   this host; this lane never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-tooling-last-good-test/00-running-log.md`
   and write stage A -- the hash, the counts, the host file's last line and
   the live census, the two runs (image and host busybox) with their
   banners, exits, wall times and counts, the five `--old` recipes' exits --
   before reading a section.

## Current focus (01:59 UTC update)

**Stage B done (03, 04: F-01 to F-21, Q6's 34 rows + 15 groups). Next: stage C, the seat.** Dispatched on #662 at 00:21 UTC; the first commands passed (stacked on P1, the rules differ from `next` in exactly the dispatch's eight paths, the file at the hash with 14238 lines and 1167697 bytes, census 0).
- **Running:** `docs/audits/2026_10_25-epic-m6-tooling-last-good-test/tools/t15-stage-a.sh`, one sequential background job started at 00:23:16 UTC. It runs the image's busybox (`QA_SYSTEM_ROOT` on the `069fc2704421` root), then the host's, then the twelve `--old` recipes. Each run starts through `vm-qa:158`'s launcher (`SIGINT ignored=0` on the first). The outputs go to `.qa-scratch/t15/run-*.out` and `old-*.out`, and the summary to `/workspace/tmp/m6-t15/stage-a.txt`. Its exit is delivered by the harness to the session; if the session is gone, read the summary file, and the `runner rc` line is the job's end.
- **Written:** `00-running-log.md` (header and stage A so far), `01-research-notes.md` § Scope (the inventory row, 408 commits, the 34 sections), and the day's work-log entry.
- **The coordinator's 00:27 ruling (#662):** keep 34 section rows for Coverage and Q6, plus a sub-group table under Q6. The lane found eight capitalised groups, not five (`x`: F1, C, D; `y`: A, F1r, CF; `z`: S315, S3F) and asked whether `x`'s three join the table (00:3x post). All eight are drafted until the coordinator answers.
- **Run 1 (the image's busybox):** rc 0, 517 s, 1313/0/0. The coordinator's ten image-run FAILs were sorted as the fixture's git-history dependency (an export without `.git`), and put to the coordinator as bug or design (the post at the time above). The sub-group table covers twelve groups (00:33 ruling).
- **Runs back:** run 2 (host) rc 1, 677 s, 994/319/0: 319 flips, `flock` (150 "applet not found") and the host's rclone 1.60.1-DEV. The twelve `--old` recipes all exit 2: two dead refs (`0f7785e6ed`, `d79281066c`), and ten stopped by `src_of` at `s` or `x`. `70b6c70ca7`'s `t` fires on patch failures, not its `012` checks. Put to the coordinator: three bugs, or (2) design.
- **Attribution:** `bbhost` 994/319 and `rchost` 1313/0, so all 319 flips are the busybox's and rclone 1.60.1 changes no verdict. Q5: `y` 248 s, `x` 82, `n` 42, `af` 34, `t` 34 of 515. Nothing is running.
- **Stage B (`c4a7e98509`):** three read-only agents' leads were re-derived where marked. Open with the coordinator: the `--old` question (three bugs, or the exit 2 as design).
- **Next:** each run's exit, wall time and counts into `00` and `02` § The runs, then the image/host diff, then the sections read for Q6 and Q3.

Not started before 00:22 UTC. The first commit on this branch is the running log's header,
`01-research-notes.md` § Scope, this pointer updated, and the day's
work-log entry headed `#662` (prose through a quoted heredoc or the Write
tool). `.qa-scratch/` is gitignored and `git status --short` is read before
every `git add -A`. The seat's two calls and the read-only tracker reads are
the only network.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-last-good-test-662
cd "$D" && git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the dispatch's paths
test -f docs/reviews/inventory.json && echo inventory
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
ls /workspace/repos/rocknix.worktrees/*/build.*GENERIC_X64*/image/system/usr/bin/busybox   # the read-only roots for QA_SYSTEM_ROOT
sed -n '1,120p' docs/reviews/briefs/tooling-last-good-test.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets (#877, #890; #887, #889; #905), T5, T6, T7, T8, T9, T10, T12,
T14, **then this branch**, then T4's last. When `next` moves, the
**coordinator** merges `next` into this branch, and never between stage A
and stage D (the read must stay a fact about one hash, plan § 8); the
coordinator merges its own branch into this one at hand-back, before the
last criterion's checkers run (as for T9, T10, T12 and T14). Never merge
another lane's feature branch here. Every lane and the M7 lane append to
`docs/decision-register.md`, the day's work log and `docs/work-logs/INDEX.md`:
keep every append, regenerate the index, never edit another lane's rows; a
merge with conflicts is checked for leftover markers before it is committed
(#696), and a union of two ledgers is made by whole entries. The highest
Decided register IDs on 2026-10-24 at the dispatch are D-WORKFLOW-205,
D-QA-062 and D-INFRA-031 (the coordinator's); a new row goes at the end of
`## Decided`, and a row is never edited. T14's fixes to the four tools this
file calls merge before this branch: until then read them from
`7c1d729b57`. Nothing here builds, touches a device, a cloud account, a real
`rclone.conf`, the host's swap, another lane's worktree, or a guest.
