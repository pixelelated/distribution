# Session pointer: M6.P2 T14, the last-good, settings and state tests (#661)

> **Seeded:** 2026-10-24 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file at every checkpoint
> **Branch:** `feature/m6-tooling-state-tests-661`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tip `27d8942071` merged in at `59704abf8f`
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-state-tests-661`; the T3, T30, T24, T4 and T10 worktrees beside it (`m6-emulators-libretro-650`, `m6-emulators-standalone-677`, `m6-emulators-dead-ends-671`, `m6-doctrine-rules-651`, `m6-tooling-guards-657`) are this session's earlier slices, accepted and idle: read only, until their merges
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T3 session, `m6-t3-emulators`), unless #661 says otherwise
> **Epic:** #903 (the tooling and guards: T9 and T10 accepted, T12 running in the T5 session, this slice, then T15, T45); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- one GPT-6 Astra seat at `max` through the Facilitator (a probe, then one refutation over one packet scanned before it is sent; D-WORKFLOW-184, 195; a failed seat is a hold); `npm install` only under `tools/council`
> **The lens:** brittleness -- Q6's table (what each test depends on that is not the thing it proves, and what happens when that is absent; its last recorded catch; its caller; its positive) and Q3's hunt for a test that passes without proving are what the slice is for; the lens is not a licence to delete, the coordinator decides a test's fate with the maintainer
> **The host:** M6's; this slice runs no build, no handheld action, no cloud test against a real provider or account, no `fork-publish-release` without `--prepare`, and at most **one bounded GENERIC_X64 guest cycle** for the two guest tests, under T12's ritual (the `069fc2704421` image copied under `/workspace/tmp/m6-t14/` and checked against its `.img.gz.sha256`; the host file line before and after; the pidfile; `tools/vm-stop`; the disk retired, D-INFRA-022); a second cycle needs a line on #661
> **T15's file is not this slice's:** `tools/last-good-scripts-test` calls four of these tools and is read, never edited

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   this worktree's rules are `next`'s except the paths the dispatch comment
   on #661 lists: `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`
   prints exactly those; anything else is STALE. `engineering-practices.md`
   § Guards must fail closed and `upgrade-and-install.md` § Verify on a
   device, not on the host are the two rules these tests live by.
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/tooling-state-tests.md` whole (version 2). The brief
   is the work; its § 7 is the contract, identical to the checklist on #661;
   its § 5 says which tests run on the host and how the two guest tests are
   benched; its § 8 names what is never run here.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #661 (with its comments), #903 (the epic, with its futro comment and the
   T14 addendum: U-1 to U-6 and A1 to A7), #339, #346 (the maintainer's
   channel: what is open there is not this lane's to decide), #657 (T10,
   accepted: its retro's five fail-open shapes are the first checklist), #656
   (T9: the model of a control with constructed positives), #659 (T12: the
   guest cycle's record), #662 (T15, not yet dispatched: the caller of four
   of these tools), #365, #421, #526, #531, #532, #565 (the tests' own
   record), #640 (the legacy paths). The M7 lane's canonical checkpoint
   `.github/sessions/saved-session-state-next.md` is read for what runs on
   this host; this lane never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-tooling-state-tests/00-running-log.md`
   and write stage A -- the two hashes, the counts, the host file's last line
   and the census, whether a build root exists for the busybox applets, the
   host-side runs with their exits and wall times -- before reading a tool.

## Current focus (21:19 UTC update)

**The stage-D pause.**
- `05` holds 23 items (1 High, 15 Medium, 7 Low). There are 17 bugs (#989 to #1005), and the audit issue is #1006, a sub-issue of #661.
- `lint --phase pre-issue` passes. The seat came back clean and is graded 42 of 42.
- No guest; no tool edited.
- Waiting for the coordinator's stage-E stream briefs, and its answer on whether PL-09 (the guest pair) is a bug or a disposition.

## Earlier focus

Not started. The first commit on this branch is the running log's header,
`01-research-notes.md` § Scope, this pointer updated, and the day's
work-log entry headed `#661` (prose through a quoted heredoc or the Write
tool). The host-side tests run in this worktree with their own temp roots
(`TMPDIR` under `/workspace/tmp/m6-t14/`, never `/tmp`); the real-rclone
four are read for their backend binding before any of them runs; the guest
cycle, if a claim needs it, follows § 5's ritual and is recorded in `00`,
`02` § The guest cycle and `docs/vm-qa-log.md`. `.qa-scratch/` is gitignored
and `git status --short` is read before every `git add -A`. The seat's two
calls and the read-only tracker reads are the only network.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-state-tests-661
cd "$D" && git fetch origin && git fetch upstream --no-tags
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the dispatch's paths
test -f docs/reviews/inventory.json && echo inventory
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -c -x qemu-system-x86
ls -d /workspace/repos/pixelelated/distribution.worktrees/*/build.* 2>/dev/null | head -3   # a build root for the busybox applets, if any
sed -n '1,170p' docs/reviews/briefs/tooling-state-tests.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets (#877, #890; #887, #889; #905), T5, T6, T7, T8, T9, T10, T12,
**then this branch**, then T4's last. When `next` moves, the **coordinator**
merges `next` into this branch, and never between stage A and stage D (the
read must stay a fact about one hash, plan § 8); the coordinator merges its
own branch into this one at hand-back, before criterion 17's checkers run
(as for T9, T10 and T12), so a register row cited from the coordinator's
branch resolves. Never merge another lane's feature branch here. Every lane
and the M7 lane append to `docs/decision-register.md`, the day's work log
and `docs/work-logs/INDEX.md`: keep every append, regenerate the index,
never edit another lane's rows; a merge with conflicts is checked for
leftover markers before it is committed (#696), and a union of two ledgers
is made by whole entries. The highest Decided register IDs on 2026-10-24 at
the dispatch are D-WORKFLOW-205 and D-INFRA-030 (the coordinator's); T12 runs
beside this lane and may take 206: check both branches; a new row goes at
the end of `## Decided`, and a row is never edited. T10's #945 changes
`tools/test-fixtures/lint-audit-artifacts/` on its branch (a `run.sh` and a
third fixture), which merges before this one: read as a delta, not a member.
Nothing here builds, touches a device, a cloud account, a real `rclone.conf`,
the host's swap, another lane's worktree, T15's file, or a guest the host
file has not been told about.
