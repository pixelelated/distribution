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

## Current focus (06:14 UTC update)

**Stage E: every bug's code is in (tip `5d1f67ca0b`); the evidence runs are going on M6's donor** (`QA_SYSTEM_ROOT=/workspace/artifacts/m6-donor/1a0266484423/image/system`; no M6 run names an M7 root).
- **S1:** `3037ce6b8c`, `7cb11eb379`, `4e5b6c6103`, `3da816ce24` (with #1030).
- **S2:** #1023 `5a155ed7fc`, #1022 `bea0374f3b`, #1021 `70af8e3771`, #1035 `1dbb668bb2`, #1024 `4bc40d7733`, #1039 `a286e5b49f`.
- **S3:** #1033 `5429e27e72`, #1037 `60066e21f8`, #1027 `65bdd1a717`, #1036 `32ba775765`, #1034 `e155cd4309`, #1032 `11952dfcf3` (and `5d1f67ca0b`), #1026 `812d09e3af`, #1031 `b729628ad6`.
- **S4:** #1025 `db08ed0953`. **S5:** #1028 `5d1b47deb7`.
- **Running: the second queue** `/workspace/tmp/m6-t15/s3/queue2.sh`, PID 1008748, harness task `btiiafr4w`, writing `/workspace/tmp/m6-t15/s2/queue.log`:
  1. root-final at `5d1f67ca0b`;
  2. #1026's fake-`bwrap` runs, unfixed and fixed;
  3. #1028's probe cuts, unfixed and fixed;
  4. the twelve `--old` recipes at `5d1f67ca0b`.
- **root-final at `5d1f67ca0b`: rc 3, 1,315 PASS / 0 FAIL / 0 SKIP / 2 CANNOT** in 516 s (1,312, plus #1033's self-check, plus #1027's split). Every strengthened check passes on the real scripts.
- **Queued after the second queue:** a waiter (harness task `bko8f22st`) on `QUEUE2 END`, then `docs/audits/2026_10_25-epic-m6-tooling-last-good-test/stage-e/run-positives.sh <worktree> 5d1f67ca0b`. That is S3's constructed positives: the `alter-*.sh` recipes on throwaway clones under `/workspace/tmp/m6-t15/s3/<bug>/`, the unfixed and fixed harness each, the clones removed after (the coordinator, 06:05).
- **It honours a `PAUSE T15` directive** at each boundary. If the session is gone, read `queue.log`; a START with no END means in flight or died, so check its PID.
- **Done and recorded:** root-tip at `a286e5b49f` (rc 3, 1,312 / 0 / 0 / 2 CANNOT); #1021's shallow-clone positives (`02`); #1023's `1d1503180d` and `34aca64afd`.
- **Answered (06:05):** altered throwaway copies yes, as committed recipes (`stage-e/`, `c388b07f78`); the twelve at the final tip only.
- **Then:** write each positive into `02`, the twelve-recipe table, and the S2-S5 checkpoint; then the close-out.
- **The register:** D-WORKFLOW-206 to 209 and D-INFRA-032 are the M7 lane's; a row here takes D-WORKFLOW-210+, D-QA-064 or D-INFRA-033+. None is planned.
- **Then S2 to S6, then the close-out** (the brief's last section): the Phase 7 table, `02` § The suites re-run, the lint, `fixed-at:`, the retro, the hand-back, then idle.
- **Stages A to D** are in `00` (A 00:23-01:10; B `c4a7e98509`; C `4851698b02`; D `2eface0727`: `05`, bugs #1018-#1039, audit issue #1040).

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
