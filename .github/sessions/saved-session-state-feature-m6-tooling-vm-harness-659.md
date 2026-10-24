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

**Stage E complete (S1 to S13); both guest cycles returned; stage F in progress** (updated 2026-10-24, 23:15 UTC).
- **`reviewed-at`:** `facb2ae523`. **The code tip:** `6e2d204987`. Everything up to it is pushed except this file's commit.
- **The streams:** S1 to S13 are all landed, one commit per bug or tool; each commit's tree was gated on its controls. Every control in full at `930ea05d70`: `vm-harness-test` 77 PASS, and `vm-pair-test`, `vm-stop-test` and `vm-upgrade-readiness-test` rc 0 (`streams/all-controls-final.txt`).
- **Cycle 1** (22:14 to 22:48): `vm-qa <069fc2704421 image>` with no override.
  - The report is in `cycle-e/vm-qa-report.md`: BUILD_ID matches the image; `tear-down: vm-pair down rc 0`; walks 16/16 hold the frames their steps name.
  - S7 and S8 ran on guest b (a recorded deviation).
  - scripts, wrapper and time-to-play FAILED; the six ES rows SKIP (02 § Why the six ES rows stayed SKIP).
- **Cycle 2** (22:56 to 22:59): `--only time-to-play`, in `cycle-e2/`. The kill fix held. The g2g row has no stamp because the product ran no exit sync: **product #1012**.
- **Both cycles are returned** on the host file, census 0, disks retired. No guest is up, and no further cycle is planned.
- **`proved:` 33 = `PROOF:` 33; coverage rows 60** (`grep -c -E '^\| `tools/'`).
- **Open items, none of them this lane's to decide:**
  - **#1012**, the g2g exit sync stopped before it starts, has no stamp (the cloud lane's bug). The g2g row fails on this image until the product stamps it.
  - **#1013** (Backlog, under #800): the ES pin in `.identity.json`.
  - **The frame-diff baseline**, the maintainer's on #346: with the 348 `#578` proposals inert, the fixed compare over cycle 1's walks shows 65 unclaimed boxes (`cycle-e/frame-diff-fixed.md`).
  - **#986, #987, #988:** PL-19, PL-20 and PL-22's Backlog issues.
- **In flight:** the scripts-suite TMPDIR runs, which settle cycle 1's 326-check scripts FAIL (the coordinator: if the worktree TMPDIR is the cause, the fix is S5's).
  - Run 1 (TMPDIR under the worktree) is done: **rc 1, 326 failed**, the same as the cycle.
  - Run 2 (`TMPDIR=/workspace/tmp/m6-t12/scripts-probe-ws`) started about 23:11. Its pids: the outer shell 834647, `timeout` 1360740 and `last-good-scripts-test` 1360741. It is the harness's background task `b0ekxo82h`.
  - The results land in `/workspace/tmp/m6-t12/scripts-tmpdir/{wt,ws}/{scripts.log,rc}`, with `finished` written when both are done.
  - **The reading so far:** the harness unsets TMPDIR before its bwrap runs, and backuptool's mktemp uses the sandbox's private /tmp. If run 2 also fails 326, the cause is not the location; look at the host's uutils coreutils (`/usr/bin/mktemp` is uutils, bound into the sandbox from /usr).
- **Uncommitted, beside this file:** `02` (#1012 and #1013 recorded) and `tools/punch-items.py` (the Phase 7 outcomes in `P7`; PL-06's evidence ends in a `SCRIPTS_RESULT` placeholder to replace).

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-vm-harness-659; A=$D/docs/audits/2026_10_24-epic-m6-tooling-vm-harness
cd "$D" && git status --short && git log --oneline -1
# 1. The scripts result (wait for task b0ekxo82h, or read the files once `finished` exists):
L=/workspace/tmp/m6-t12/scripts-tmpdir; cat $L/finished $L/wt/rc $L/ws/rc; tail -n 1 $L/wt/scripts.log $L/ws/scripts.log
#    Copy both logs and rcs into $A/streams/ (scripts-tmpdir-wt.txt, scripts-tmpdir-ws.txt), write a 00 entry and a PROOF line,
#    and put the answer in punch-items.py's PL-06 (replace SCRIPTS_RESULT). If ws passes and wt fails, the fix is S5's
#    (vm-qa's exported TMPDIR), with a vm-harness-test case; then rerun the scripts suite under vm-qa's TMPDIR, with no guest.
# 2. Regenerate 05 and lint the folder:
python3 -I $A/tools/punch-items.py > $A/05-punch-list.md && tools/lint-audit-artifacts $A | tail -3   # want PASS (the default phase)
grep -c 'proved:' $A/02-forward-audit.md; grep -c 'PROOF:' $A/00-running-log.md; grep -c -E '^\| `tools/' $A/02-forward-audit.md   # equal; 60
# 3. 02 § The suites re-run: vm-harness-test, vm-pair-test, vm-stop-test, the seven S12 tools' controls, and the cycles' reports.
#    No guest; the ports must be free (port-held-refused binds 10022).
# 4. fixed-at: <tip> in #659's body (gh issue edit 659 --repo pixelelated/distribution --body-file ...; read it back).
# 5. Stage G: the retro at docs/retros/2026-10-24-m6-tooling-vm-harness.md, posted on #659. It covers what the slice did to the
#    two time-to-play numbers (nothing to the numbers; the cells now fail when unmeasured) and what each stream did to a refusal.
# 6. The checkers: tools/register-check (red here until the coordinator's hand-back merge; D-QA-061 and D-INFRA-031 live on
#    feature/m6-renovation-plan-346), tools/rules-check --quiet, tools/work-log-index --check, the lint.
#    Then a work-log entry, this pointer, and the hand-back comment on #659 naming the tip and each artifact by path.
```

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
