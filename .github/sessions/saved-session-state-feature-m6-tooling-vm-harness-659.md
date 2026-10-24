# Session pointer: M6.P2 T12, the VM harness (#659)

> **Seeded:** 2026-10-24 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file at every checkpoint
> **Branch:** `feature/m6-tooling-vm-harness-659`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tip `74de5c1610` merged in at `32dc03c888`
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-vm-harness-659`; the T5, T6, T7, T8 and T9 worktrees beside it (`m6-build-engine-652`, `m6-build-engine-upstream-tools-653`, `m6-generic-packages-reached-654`, `m6-image-packages-655`, `m6-tooling-build-supervision-656`) are this session's earlier slices, accepted and idle: read only, until their merges
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T5 session, `m6-t5-build-engine`), unless #659 says otherwise
> **Epic:** #903 (the tooling and guards: T9 accepted, T10 running in the T3 session, this slice, then T14, T15, T45); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- one GPT-6 Astra seat at `max` through the Facilitator (a probe, then one refutation over one packet scanned before it is sent; D-WORKFLOW-184, 195; a failed seat is a hold); `npm install` only under `tools/council`
> **The lens:** cost against value -- Q5's cost table (minutes and host per suite) and Q6's value table (each suite's last recorded catch, or `nothing recorded`; its caller, or `nobody`) are what the slice is for; the lens is not a licence to delete, the coordinator decides a suite's fate with the maintainer
> **The host:** M6's; this slice runs no build, no handheld action, no QA account against anything real, and **one bounded GENERIC_X64 guest cycle** (the image named with its sha256 first; the host file line before and after; the pidfile under `/workspace/tmp/m6-t12/`; `tools/vm-stop` to end it; the disk retired after its record, D-INFRA-022); a second cycle needs a line on #659

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   this worktree's rules are `next`'s except the paths the dispatch comment
   on #659 lists: `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`
   prints exactly those; anything else is STALE. `generic-x64-vm-testing.md`
   is the owning rule; `vm-first.md` and `time-to-play.md` the principles.
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/tooling-vm-harness.md` whole (version 2). The brief is
   the work; its § 7 is the contract, identical to the checklist on #659.
   Its § 5 gives the one guest cycle its exact ritual; its § 8 names what is
   never run here.
3. Read the live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #659 (with its comments), #903 (the epic, with its futro comment and the
   T12 addendum: U-1 to U-6 and A1 to A7), #339, #346 (the maintainer's
   channel: what is open there is not this lane's to decide), #656 (T9,
   accepted: D-INFRA-028, the guest census and `vm-stop` as the stopping
   path), #655 (T8, accepted: its `02` records five guest cycles in the shape
   this slice uses), #135, #252, #133, #166, #228, #545, #454 (the harness's
   own record), #640 (the legacy paths). The M7 lane's canonical checkpoint
   `.github/sessions/saved-session-state-next.md` is read for what runs on
   this host; this lane never edits it.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-tooling-vm-harness/00-running-log.md`
   and write stage A -- the hash, the counts, the host file's last line and
   the census, the no-guest controls with their exits -- before reading a
   tool.

## Current focus

**Idle (23:40 UTC 2026-10-24): T12 accepted by the coordinator at 23:39 UTC on #659; #984 is closed as completed, with its 23 checkboxes ticked by name.**
- **The marker:** `docs/audits/2026_10_24-epic-m6-tooling-vm-harness/audit-completion.json`, written by `tools/write-completion.py` from #984's closed readback (completed 23:40:02 UTC). Beside it are `tracker-final-readback.json` and `tracker-completion.json`. `tools/ceremony-check`'s `completed_audit_marker()` accepts it, and `tools/lint-audit-artifacts` on the folder prints `PASS`.
- **Commits:** `reviewed-at` `facb2ae523`, `fixed-at` `159ed33562` (in #659's body); the hand-back tip `d9991735d8`.
- **Stopped:** the QA webdav backend this lane's cycle 1 started (pid 188175, 22:14:47) went down through `tools/cloud-test-backend down` (rc 0); the pid is gone and port 9010 is free.
- **Running for this lane:** nothing. No guest, no backend, no watcher.
- **What the lane waits for:** the merge to `next`, the coordinator's, after T10's and before T14's. `register-check` turns green with it (D-INFRA-031, D-QA-061, D-QA-062).
- **Open elsewhere, not this lane's:**
  - #1012, the g2g stamp;
  - #1013, the ES pin;
  - #1015, the scripts suite on this host, T15's;
  - the frame baseline, the maintainer's on #346;
  - #986, #987 and #988.

## Next commands

None. The lane is idle until the coordinator's merge, and nothing runs here until then.

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets (#877, #890; #887, #889; #905), T5, T6, T7, T8, T9, T10, **then
this branch**, then T4's last. When `next` moves, the **coordinator** merges
`next` into this branch, and never between stage A and stage D (the read
must stay a fact about one hash, plan § 8); the coordinator merges its own
branch into this one at hand-back, before criterion 17's checkers run (as
for T9 and T10), so a register row cited from the coordinator's branch
resolves. Never merge another lane's feature branch here. Every lane and the
M7 lane append to `docs/decision-register.md`, the day's work log and
`docs/work-logs/INDEX.md`: keep every append, regenerate the index, never
edit another lane's rows; a merge with conflicts is checked for leftover
markers before it is committed (#696), and a union of two ledgers is made by
whole entries. The highest Decided register IDs on 2026-10-24 at the dispatch
are D-WORKFLOW-202 and D-INFRA-030 (the coordinator's); T10 runs beside this
lane and may take 203: check both branches; a new row goes at the end of
`## Decided`, and a row is never edited. Nothing here builds, touches a
device, a cloud, a QA account, the host's swap, another lane's worktree, or
a guest the host file has not been told about.
