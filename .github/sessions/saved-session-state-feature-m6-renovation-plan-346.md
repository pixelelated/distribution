# Session pointer: the renovation lane (M6)

> **Saved:** 2026-10-22 (see the commit)
> **Branch:** `feature/m6-renovation-plan-346` (a pointer; D-WORKFLOW-133)
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346`
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (the fresh clone of 2026-10-22, D-INFRA-025; the legacy `/workspace/repos/rocknix` serves M7 until #640)
> **Repository:** `pixelelated/distribution`; integration branch `next`

## Start here

1. Read `next:AGENTS.md`, the every-session rules under `.claude/rules/`, and
   check this worktree's rules are `next`'s:
   `git diff --quiet next -- .claude CLAUDE.md AGENTS.md || echo STALE`.
2. Read [the canonical next checkpoint](saved-session-state-next.md) for the
   M7 lane's state. **This lane does not edit it** while M7 owns it (the open
   question on #346); this pointer is the lane's state.
3. Read `docs/reviews/plan-for-the-plan.md` (the plan for the plan, #346), the
   live [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #339 (the epic) and #640 (the checkout move).
4. Register rows this lane wrote: D-WORKFLOW-181, D-INFRA-025. The M7 lane
   holds D-WORKFLOW-171 to 180 and D-INFRA-024 unmerged on
   `feature/m7-audit-integration-603`; do not cite them on this branch until
   they reach `next` (`tools/register-check` refuses a citation of an absent
   row).

## Current focus

**2026-10-24, afternoon (13:5x UTC).** P0 and every accepted slice branch
wait for the M7 lane's post-candidate merge to clear the push guard's W42
gate before anything merges to `next` (never `--no-verify`); the order is in
§ Merge notes and § State at 2026-10-24. **Accepted:** P1 (#641), T1 (#648),
T2 (#649), T3 (#650), T5 (#652), T6 (#653), T7 (#654, `db6597356b`), T30
(#677, `a020b3d375`), **T24 (#671, complete at `26e4a34edf`: #900 closed, the completion marker written, the full lint PASS)**.
**T8 (#655, Independent) accepted at `13394550d6` (14:48 UTC)** from the T5 session (`m6-t5-build-engine`): four streams from `t8-streams.md` (`89e71c23fa`) -- S1 #852 `43f6a81070`, S2 #893 `4db09f6e2e` and `1904e29d54`, S3 #894 `467f19fc14` with #899 `0602f598e9` and `412be96c77`, S4 #901 `b58489297c` -- proved on an export and on the GENERIC_X64 guest; audit #895 closed (its nineteen checkboxes ticked by the coordinator after a closed-with-open slip, erratum on #655); **complete at `f50a031158`** (the completion marker, the full lint PASS, the guest payloads retired under D-INFRA-022, 15.8 GB, each with its hash in the `vm-qa-log`). **T9 (#656, `tooling-build-supervision`, Independent) dispatched 15:43 UTC** to the T5 session from brief v2 `8826d2968d` (the stranger's proof: 4 wrong, 6 partial, corrected; its U-1 answered: three qa-logs controls fail at the hash for want of `build-admission` in their fixtures), lane `feature/m6-tooling-build-supervision-656` at `cdc45513b0` (merge `2a24aa2063`, the chain stopping on four conflicts first; eight rule paths differ from `next`); the tooling area's epic is **#903** with its futro. **The T5 session was free from 14:53 UTC; the next slice in the order for it is T9 (`tooling-build-supervision`), whose area epic, futro and brief the coordinator writes next.** **T24** ran 13:4x to 14:20 in the T3 session (`m6-t3-emulators`) from brief
v2 `c25d772b21` on lane `feature/m6-emulators-dead-ends-671` (the merge
`8fd13c3133` carried the index's conflict markers for one commit;
`81331b499e` fixed it; blindspot 76) and is accepted. **Packets** reviewed and waiting for the merge: #877 `cf3a8d8e62` and #890 `566b01448f` (before T5's branch); #887 `c60cdddf8b` and #889 `828472eb59` (after T30's); **#905 `9e12014623`** (`ceremony-check` reads every friction entry; beside the checksum packets; T4's S8 and T10 depend on it). The T1 session is idle. **T4 (#651, the doctrine, Local) accepted at `cceac27d6a` (15:47 UTC)** after eight streams (S1 to S8, `0faea874de` to `b3c1d0d7c3`; the #905 packet `9e12014623` reviewed; audit #912 closed, 16 resolved, 8 deferred, 1 withdrawn; `register-check` and `rules-check` pass on the simulated merge); complete at `6ec78bbf8c` (the marker written, the full lint PASS); the T3 session is free since 15:49 UTC and T10 (#657, the guards, Extended) is being briefed for it; T4 had been dispatched 14:34 UTC** to the T3 session, freed by T24: brief v2 `0921782112`, lane `feature/m6-doctrine-rules-651` at `00e75ab135` (the merge `e3897db16d`: four ledger conflicts united by the recipe, the chain stopping on them first; the worktree differs from `next` on eleven doctrine paths, the first lead). The third-lane question on #346 is withdrawn as moot. **Waiting on the maintainer (#346):** #825's disclosure timing, `LOCAL_SSH_KEYS_FILE`, D-SYS-014, D-WORKFLOW-191. **At integration (the coordinator dispatches):** the #857/#873 packet
after T3's merge; the Backlogs #839, #878, #885, #896, #897; the
`fix-pending-image` rows; T8's conflict list (11 rows) read under
D-WORKFLOW-198/199. **Filed today by this lane:** #807 to #811, #838, #839,
#842 to #844, #847 to #852, #873 to #879, #885, #888, #890, #896 to #898, #901, #903; the lanes filed #880 to #884, #886, #887, #889, #891 to #895, #899, #900, #902, #904 to #912. **Guard added
today:** `.githooks/pre-commit` refuses a conflict marker (#696).

**T10 (#657) dispatched at 16:26 UTC (2026-10-24)** to the T3 session (`m6-t3-emulators`, pane `wN:p6`) from brief v2 `2a4be1006b` after the tooling futro's T10 addendum and a stranger's proof (6 wrong, 2 partial, corrected); lane `feature/m6-tooling-guards-657` at `a82d784216`; its stage-D pause and `t10-streams.md` are the coordinator's next after T9's. The host is M6's again since M7's 16:00 return (census qemu 0, compilers 0). Two lanes run: T9 (T5 session, stage C) and T10 (T3 session, stage A).

**T9 (#656) stage E dispatched at 16:48 UTC (2026-10-24)** from `docs/reviews/briefs/t9-streams.md` (`4c842e2485`): eight streams S1 to S8, three contract rows D-INFRA-028/029/030 (put to the maintainer on #346 for veto before the merge), leads filed #925 (PL-08's rows), #926 (PL-21), #927 (PL-13, the owner's), PL-20 on #528, two rows on #657. Accept with `AUDIT_ISSUE=924 $S/t9-accept.sh <tip> <coordinator tip>`. M7 holds a second VM window (16:50 to 18:30 UTC, extendable); M6 starts no guest until its return line.

**T10 (#657) stage E dispatched at 18:01 UTC (2026-10-24)** from `docs/reviews/briefs/t10-streams.md` (`9e0718eeb5`): ten streams S1 to S10 over 29 bugs (#929 to #957), audit #958; three contract rows D-WORKFLOW-200/201/202 (put to the maintainer on #346 for veto before the merge); leads #959 (PL-16), #960 (PL-30); #928 (pkgcheck, under #800). Accept with `AUDIT_ISSUE=958 $S/t10-accept.sh <tip> <coordinator tip>` (to be written in the shape of `t9-accept.sh`, with `hooks-test` on the tip and on the simulated merge). Two lanes run: T9 (S7, S8 next) and T10 (S1).

**T9 (#656) accepted (2026-10-24 18:3x UTC)** at `bf4445a13c`, #924 closed; the lane writes its completion marker next. T10 (#657) is at S5 of ten; its hand-back is accepted with `AUDIT_ISSUE=958 $S/t10-accept.sh <tip> <coordinator tip>` after the coordinator's branch is merged into it (criterion 17). Findings carried today: #961 (ES fork's guard-lib), #962 (ten credential-shaped tree lines; redaction packet after the maintainer's word on #312), the history counts on #312.

**T12 (#659) dispatched at 19:04 UTC (2026-10-24)** to the T5 session from brief v2 `74de5c1610` (the VM harness, cost against value; one bounded guest cycle authorized); lane `facb2ae523`. The register's twelve SHAPE rows are clerical at `d59b7a11eb` (D-WORKFLOW-203) so T10's merge keeps the push gate green. Two lanes run: T10 (S9/S10, then hand-back) and T12 (stage A). Accept T10 with `AUDIT_ISSUE=958 $S/t10-accept.sh <tip> <coordinator tip>` after merging this branch into it; T12's acceptance script is still to write (in `t9-accept.sh`'s shape, with the three no-guest controls).

**T10 (#657) accepted (2026-10-24 19:48 UTC)** at `afdce9a65b`, #958 closed; the lane writes its completion marker next. **Accepted today: T7, T30, T24, T8, T4, T9, T10.** Running: T12 (T5 session; stage C's seat, then stage D). Next for the coordinator: T12's stage-D pause and `t12-streams.md`; then the next slice for the freed T3 session from the order (the tooling epic's T14 #661, or the next unblocked).

**T14 (#661) dispatched at 20:16 UTC (2026-10-24)** to the T3 session from brief v2 `27d8942071` (the state tests, brittleness; one guest cycle authorized if needed; T15's file read, never edited); lane `30da4853bb`. T10 complete at `7182f743ea`. Two lanes run: T12 (T5 session, stage C's seat then D) and T14 (T3 session, stage A). Next for the coordinator: T12's stage-D pause and `t12-streams.md`; then T14's; `t14-accept.sh` is still to write in `t12-accept.sh`'s shape (the five bare-run tests, `build-identity-test --output`, the two stubs).

**T12 (#659) stage E dispatched at 20:57 UTC (2026-10-24)** from `docs/reviews/briefs/t12-streams.md` (`6d9898a493`): thirteen streams (S1 to S3 the runner, S4 before S5 the disk safety then the host state, S6 to S13), one new control `tools/vm-harness-test`, three contract rows D-QA-061 (vm-qa exits 3 over a SKIP), D-QA-062 (time-to-play judges every cell that ran), D-INFRA-031 (the host state belongs to the checkout) put to the maintainer on #346 for veto; Backlogs #986 (PL-19, `ra-candidate-games`'s retirement proposed), #987 (PL-20), #988 (PL-22, rule edits at integration). The lane's stage-D pause was `7774e86cfa` (audit #984, bugs #966 to #983, two High: #969, #970). Its one stage-E cycle is the pair, after S5, held behind the M7 lane's return line: **M7 holds a granted host window (20:44, bounded 22:15 UTC; START 20:57)**; no M6 guest before the RETURN line. T14 (#661) is at stage B (`f3cc73c6a4`). Acceptance: `AUDIT_ISSUE=984 $S/t12-accept.sh <tip> 6d9898a493`.

**T14 (#661) stage E dispatched at 21:30 UTC (2026-10-24)** from `docs/reviews/briefs/t14-streams.md` (`13242d182a`): twelve streams, S2 (the shared rclone sandbox and the connections fixture, the one High #992/#999) first, then S1, S3 to S5, S6 to S10, S11 (the guest pair's kill-after-refused-start: a Bug the lane files, then fixes), S12 (one lint fail fixture per violation; `run.sh`'s lines are the coordinator's at #945's merge). No register row; no guest in stage E. The stage-D pause was `7aa8eac253` (audit #1006, bugs #989 to #1005). Dispositions: the guest pair and the two stubs kept as refusing markers, the removal bundle (six tools with T12's two walk scripts) put to the maintainer on #346 at 21:30; PL-11's ten added to #986; #1007 filed (the state tests' rules and index). Acceptance: `AUDIT_ISSUE=1006 $S/t14-accept.sh <tip> 13242d182a`. T12 is at S4 of 13 (`ec0e4bcfcf`). **The 2026-W42 weekly summary is missing and refuses a push of `next`** (`ceremony-check`): offered to M7 at 07:13 with no answer; a read-only agent is drafting it from the week's logs for the coordinator to commit under #254 and hand to M7 for correction before its candidate merge.

**M7's host window closed at 22:09 UTC (2026-10-24)** with its FINAL RETURN (both notice components accepted, VM03 five cases PASS, four layouts reviewed; census 0 live/0 all, 0 compilers; receipt `/tmp/pix766-final-host-return-20261024-01.json`). **M6 holds the host.** T12's two stage-E cycles ran and returned (22:14-22:48 the pair; 22:56-22:59 `--only time-to-play`), census 0 after each; M7's corrected installer VM02 holds the host from 22:59 (bounded 23:24); T14 needs no guest. Two census slips today (a defunct QEMU counted at 20:57; a defaulted `compilers 0` at 22:10, both corrected on the file within the minute) became Backlog #1008 (a fail-closed `tools/host-census`); the live count is read with `pgrep -x qemu-system-x86 -r R,S,D,T | wc -l` until then. The 2026-W42 weekly summary is on this branch alone at `48fe62e202` for M7 to cherry-pick before its merge; the retro gate blocks in two active days (M7 told, 21:37).

**T14 (#661) accepted (2026-10-24 23:33 UTC)** at the hand-back `7c1d729b57`, the coordinator's branch merged in at `e8d866507d` (two ledger conflicts united; register-check 679); #1006 closed (ticked=23 open=0 by name); 17 of 18 criteria ticked, the before-its-merge checker line open for the merge packet. The lane writes `audit-completion.json`, the full lint and the idle pointer next. At T14's merge (after T12's, before T4's): T15's two `--busybox` calls gain `--busybox-from`/`--unverified-busybox` (`last-good-scripts-test:14224`, `:14231`); `run.sh`'s two lines for the split lint fixtures (#945's file); the `docs/releases/` receipts since `d9f428e1a0` re-read against the fixed state check and store. **Accepted today: T7, T30, T24, T8, T4, T9, T10, T14.** Running: T12 (stage F, then G and the hand-back; `t12-accept.sh` ready).

**T12 (#659) accepted (2026-10-24 23:39 UTC)** at the hand-back `d9991735d8` (`fixed-at 159ed33562`), the coordinator's branch merged in at `a1bdd18355`; #984 closed (ticked=23 open=0 by name); 17 of 18 criteria ticked. The lane writes `audit-completion.json`, the full lint, `cloud-test-backend down` and the idle pointer next. **Accepted today: T7, T30, T24, T8, T4, T9, T10, T14, T12.** Running: nothing dispatched; next in the order: T15 (#662, `last-good-scripts-test`, with #1015 and the `image_tool_source` fallback as its first findings) and T45 (#692), briefs to be written. At T12's merge: the catalog re-read for `vm-qa` PASSes over a SKIP; the device-action log's redaction (S7). Acceptance exports: `accept-t12` (retire after this record), `t12-proof` (43M, retire).

**T15 (#662) dispatched at 00:21 UTC (2026-10-25)** to the T3 session from brief v2 `269a552a0b` (the last-good scripts test, 14,238 lines, brittleness; no guest; two stage-A runs under the image's and the host's busybox, the twelve `--old` recipes); lane `60d7f6a5b2` (worktree `m6-tooling-last-good-test-662`, stacked on `2174265e9c`, the coordinator's tips merged at `1d1a33785e` and `5b91668d8c`). The coordinator's own two runs at the hash: 1,303/10/0 (image busybox, 514 s) and 984/329/0 (host, 671 s), 319 flipping, ten vacuous-fixture FAILs in `x`/`y`; `/workspace/tmp/m6-coordinator/t15-hash/run-{image,host}.out` hold them. Acceptance script to write: `t15-accept.sh` (the inventory block, the file at the hash, the diff over the dispatch tip, `--help`/`--nosuch`, the two call sites' flags, one image-busybox run and one no-root run of the fixed suite, the checkers on the simulated merge). Next brief: T45 (#692, the council toolchain, package currency). The M7 lane holds a single-guest window granted 00:09.

**The coordinator's session died 00:45-02:20 UTC (2026-10-25)** on an API usage-credit error; monitors re-armed, M7's 01:39 request granted at 02:24 (window to 04:30; its VM ran 02:26-02:30 and returned), T15's 01:11 question answered at 02:24; Backlog #1017 (a heartbeat on the host file). **T15 (#662) stage E dispatched at 02:36 UTC** from `docs/reviews/briefs/t15-streams.md` (`d717bac312`): six serial streams on one file, S1 the two Highs (#1018 the silent fallback, #1019 the writer-test calls); the stage-D pause was `2eface0727` (audit #1040, bugs #1018 to #1039; T15's brief corrected: the tree's figure under the image's busybox is 1,313/0/0, the coordinator's ten were a history-less export). Backlog #1041 (the split by subject); #1007 gained PL-23's two rows. **T45 (#692):** brief v1 `dc81388432`, worktree `m6-tooling-council-692` at `337bf46ede` (merge 1), pointer/dispatch templates in the scratchpad; the stranger's proof is running (its first run died with the session). Acceptance: `AUDIT_ISSUE=1040 $S/t15-accept.sh <tip> <coordinator tip>` -- amend it to export from a clone, not `git archive`, and to add the `--host-diagnostic` run.

**T45 (#692) dispatched at 02:54 UTC (2026-10-25)** to the T5 session (`m6-t5-build-engine`) from brief v2 `fe43e15058` (Local depth, no seat; the council toolchain's provenance and currency table). The decision in it: the coordinator's branch carries `0ceb2994c5` and `033eb7ed23` (#636/#638, the local Facilitator `1.14.1-pixelelated.2`; ten members, 30 pins) that `next` lacks, so the read stays at `8ebaf8daad`, the delta is tabled, the stop and the empty-diff checkbox are scoped to the other 42, the checks run on both trees, every `tools/council/run` call carries `COUNCIL_ENV_FILE=/nonexistent`, `efforts --refresh` is never passed. Lane worktree `m6-tooling-council-692` at `32a34393dd` (merges `337bf46ede`, `e2fdca688b`, `e787bc6939`; the pointer seeded). At hand-back: merge the coordinator's branch in, re-run the brief's § 10 list on a clone of the tip (both trees), tick #692 from the artifacts, close its audit issue, prompt the close-out; its merge into `next` comes after T15's, before T4's. **The lead for the maintainer (#346, 02:5x):** no register row names the local Facilitator fork; proposed as the next D-WORKFLOW row when they answer. **D-QA-063** (02:42): the exit lattice every fork suite shares (1 over 3 over 0); T15's `--host-diagnostic` exits 1 on a failing case, the stream brief corrected at `d54b754da3`.

**#1043 (2026-10-25 03:03-03:07 UTC):** T45 found two council seal keys committed under `research/council-runs/*/verification/seal-key.local` on public `next` since September (contents never read). Filed #1043; removed on this branch at `0fa5a20c5f`; M7 told on the host file (it may carry the two-file `git rm` if it pushes `next` first); the maintainer asked on #346 whether history is rewritten (theirs) or the two runs' records declare the seals void (proposed). Open on #1043: the guard pattern for the shape with its constructed positive (`.githooks/secret-patterns`, `.githooks/hooks-test`), the two runs' records, the blindspot entry, the register row from the maintainer's answer. T45's stage-A question (criterion 9's lint target) answered 03:03: the four `research/council-runs/*` directories; the brief and the body corrected at `2672582a01`.

## Next commands

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346
git fetch origin && git merge --no-edit next          # only when next moved; never another lane's feature branch
tools/register-check && tools/work-log-index --check && tools/ceremony-check
```

Then: **at every gate, re-read § The seed brief below and D-WORKFLOW-181 against
what is about to be accepted, and say on #641 what was checked** (maintainer,
2026-10-23, giving the yes on the order: *"It's incredibly important that we
remain aligned."*). Read #641's latest comments for P1's state. At its pass-7 gate, read
the proposed order against plan § 5 and § 6a and record the yes or the
changes on #641. After the M7 candidate's merge lands on `next`, merge this
branch to `next` first (`git switch next && git merge --no-ff
feature/m6-renovation-plan-346` in the primary checkout, the push guard's
checks green), then P1's branch when it hands back. Address every git
command to a worktree with `git -C <absolute path>` and every file by its
absolute path: a `cd` at the head of a call did not hold on 2026-10-22 and a
commit meant for this branch landed on P1's.

## Herdr lane map (2026-10-22, the planning session's record)

Workspace `wN` "pixelelated · Codebase renovation" (session `default`),
after the maintainer's Herdr layout: first tabs coordinate, each later tab is
one lane, one session per worktree (D-WORKFLOW-183).

| Tab | Label | Pane | Worktree | Agent name | Model | Role |
| --- | --- | --- | --- | --- | --- | --- |
| `wN:t1` | P0 planning (#346) | `wN:p1` | none (`/workspace/repos/pixelelated`) | (unnamed, Claude Fable 5.1) | Fable 5.1 | the session that planned P0 and started the lanes; closes once the coordinator has resumed |
| `wN:t2` | Coordinator (M6, #346) | `wN:p2` | this worktree | `m6-coordinator` | Fable 5.1 | plans, writes briefs, accepts at gates, integrates; keeper of the primary checkout |
| `wN:t3` | P1 Survey (#641) | `wN:p3` | `distribution.worktrees/m6-p1-survey-641` | `m6-p1-survey` | Opus 5.5 | executes `docs/reviews/briefs/p1-survey.md` |

Session ids are read fresh from `herdr agent list` (`agent_session.value`)
and recorded on #346 and #641 at each start; never from this table. Other
workspaces on this host (`w4` the M7 lane, `wG` the website, `w7` another
project) are never read, prompted, moved or closed from here. Questions only
the maintainer can answer go up through the coordinator, one at a time, and
the answer is recorded verbatim, marked RELAYED, where the question lives.

## Merge notes

This branch and the M7 lane both append to `docs/decision-register.md`, both
create `docs/work-logs/2026_10-work_logs/2026_10_22-work_log.md`, and both
regenerate `docs/work-logs/INDEX.md`. At merge: keep both appends in order,
keep both day-file entries, regenerate the index with
`tools/work-log-index --write`. Nothing here builds, touches a device, a
cloud or the M7 build worktrees.

- **This branch carries three of M7's commits as cherry-picks** (`-x`, 2026-10-23
  16:30 UTC): `033eb7ed23`, `0ceb2994c5`, `6874394d49` from `fac2129787`,
  `1c7d283ad5`, `a7a3bdda4e` on `feature/m7-audit-integration-603` (the
  Argon reviewer route and its pins, #636/#638). When the M7 candidate merges
  to `next` first, the merge of this branch sees them as duplicate patches;
  expect a clean or trivially identical resolution in `scripts/council-invoke.ts`,
  `tools/lint-audit-artifacts`, `verifier-pins.json`, `council-seat-efforts.json`
  and the two `docs/qa-logs/2026-10-22-*-638/` folders, and check for markers.
- **T2 accepted 2026-10-24 00:3x UTC** (#649: distribution `f16cf7fc28`, ES
  `55158d2a64`, 35 commits on the pin `16dbac5211`; `reviewed-at: f4e0f0a196`).
  Its `slices.json` row (`reviewed_at`, `fixed_at`, `es`) is written when this
  branch takes the P1 branch at integration. **The ES integration order:** the
  M7 lane's EmulationStation fixes of 2026-10-23 (#697/#698) reach
  `test/qa-integration` first, then T2's branch is merged there and the pin
  bumped in `package.mk` on this branch; both wait for D-WORKFLOW-191 (which
  build carries the renovation's pin bump). #649 stays open as `remediating`
  until that image proves the 21 walks; then it and the 24 `bug` issues close.
## State at 2026-10-23 (the coordinator's own update)

P0 is done on this branch; its merge waits on the M7 lane's post-candidate
merge (never `--no-verify`). P1's pass-7 gate: question 1 settled
(D-WORKFLOW-185/186), question 2 withdrawn (D-WORKFLOW-187: the renovation
gates no release), question 3 settled by D-WORKFLOW-184; the maintainer's yes
on the order's fourth version (`eb4763e3cc`, ledgers `00ca350666`) was given
on 2026-10-23 and relayed; P1 wrote the order's register row on its branch
(the next ID above 187). The question who authors the slice issues was
answered 2026-10-23 with a general rule, D-WORKFLOW-189: planning, the
division of work, the definition of work items and roadmap changes are this
lane's; a work lane executes. So the 46 slice issues are this lane's to file,
from P1's renderer (`tools/renovation-inventory --slice-issues DIR`, run
read-only against P1's tree into this lane's scratchpad). #644 and #645 are
the build-path read and its PR-process findings. The 46 are filed: #648 (T1) to #693
(T46), sub-issues of #339 on milestone M6, `tools/box-check` 0 fail over all
open issues (work log 05:40 UTC). P1 was accepted at hand-back and #641
closed completed on 2026-10-23 (P1's branch at `2174265e9c`; it merges to
`next` after this branch, after the M7 candidate). T1 is dispatched (2026-10-23): the area
epic #695 with its futro; the brief `docs/reviews/briefs/os-launch-control-state.md`
at version 2 (`968ba95993`); the lane `feature/m6-os-launch-control-state-648`
at `4228561fd2`, worktree `distribution.worktrees/m6-os-launch-control-state-648`,
an Opus 5.5 session at high effort in Herdr pane `wN:p4`, agent
`m6-t1-os-launch` (started from this pane: `herdr tab create --workspace wN
--cwd <worktree> --label ... --no-focus`, then `herdr agent start <name>
--kind claude --pane <id> -- --model claude-opus-5-5 --effort high`, then
`herdr agent prompt <name> "<seed>"`; the seed is kept in this session's
scratchpad and quoted in the 07:50 work-log entry). This lane's rules from
the futro: no merge of `next` into a slice branch between stage A and stage
D; every drift report read at every slice close and the re-open named;
`tools/box-check` on every issue a lane files, at the pause. Next: **T1 accepted at hand-back 2026-10-24 01:24** (`ba22eea867`; `reviewed-at efadfea08a`, `fixed-at 0f7558cff7`; 13 of 15 criteria ticked; one `Already written:` line owed on Q6's `installtointernal` row, asked of the lane; the simulated merge of this tip into the lane's conflicts only in the four ledgers; #796 and #797 filed from its stage F and retro). Both lanes are idle; the host is M7's from 2026-10-24 01:33 (H700 then SM8550 builds) until its return line, acknowledged with a census at 01:27, both lanes holding. **T3 is dispatched (2026-10-24 02:37):** the brief at version 2 (`f650d65522`, after the epic #798's futro `179093ffd6` and a stranger's proof), the lane `feature/m6-emulators-libretro-650` at `af35d54f87` in `distribution.worktrees/m6-emulators-libretro-650` (P1 `2174265e9c` + this tip merged at `16778b5f61`), Opus 5.5 at high effort in pane `wN:p6`, agent `m6-t3-emulators`; the dispatch comment is #650 issuecomment-6378830351. The host returned to M6 at 02:22 (acknowledged in the file at 02:23). **T5 is dispatched (2026-10-24 03:51) beside T3:** the brief at version 2 (`01ff4c0bcd`, after the epic #800's futro `fd46029257` with errata and a stranger's proof), the lane `feature/m6-build-engine-652` at `30b1bb38c0` in `distribution.worktrees/m6-build-engine-652` (P1 `2174265e9c` + this tip merged at `dcd70698f1`), Opus 5.5 at high effort in pane `wN:p7`, agent `m6-t5-build-engine`; the dispatch comment is #652 issuecomment-6379501933. **The host is M7's from 03:47** (handoff confirmed in the file; both lanes hold runtime until the return is relayed on #650 and #652). Read #650 and #652 at every turn; each lane's stage-D pause comes with its punch list, then its stream briefs are this lane's to write. Bugs filed today by this lane: #801 (the identity test's release-plan half, T14's), #802 (the default PlayStation core not where the launcher loads it: the base merge takes `c9820d0e89` adapted to `${DISTRONAME}`). **The research behind the brief (#650, `emulators-libretro`, Extended, currency; the 01:00 to 01:45 reads of this session: 344 paths, 31,961 lines, 10,185 read, RetroArch at `bdba046fa6` v1.22.2, 151 core recipes with 144 full-hash pins, one pin differing from `upstream/next`, 14 upstream commits on the paths since `c445081a59`, upstream's `retroarch-0100-ffmpeg9-lavc63.patch` absent here, `mk_es_systems` defined in T5's `distributions/ROCKNIX/config/functions:99` and called at `virtual/emulators/package.mk:1726`, `Install Steam.sh` 2,755 lines fork-own by M7's October commits).** At integration, T1's acceptance leaves (brief § 10: re-run the harness under
`QA_SYSTEM_ROOT` and `pkgcheck` once; the `fix-pending-image` rows stay open);
T2 accepted 2026-10-24 (above), its ES merge and pin bump held for the M7 ES
fixes and D-WORKFLOW-191; the merge order to `next` after
the M7 candidate (P0, P1, T1, T2, T3, T5, then T4 last so the doctrine's edits land once, each rule-file conflict resolved in this lane's favour and the slice's edit re-applied by the paragraph its stream brief names; **at the integration commit, after T3's S2 and T5's E4 are both on `next`: flip `add_es_system`'s zero-default `elif` in `distributions/ROCKNIX/config/functions` from the WARNING to `return 1` (E4 left it a warning because GENERIC_X64's `psx` default is S2's line) and regenerate the five tables once more, the diff being S2's and E4's intended lines only;** the ledgers united by whole entries; the change log for T1's player-visible lines the day it lands; `audit-completion.json` for T1 after #701 closes; the drift re-open over M7's `runemu.sh` hunks; the image proof of T1's nine fix-pending-image rows and T2's 21 walks, then #648/#649 and their bugs close, the three device-fact bugs as open items to test). **At the next base merge of `upstream/next`:** take upstream's `c9820d0e89` (the 32-bit PlayStation core installed where the launcher loads it, #802) and `yabadabadoo-lr`, and **rewrite their `build.${DISTRO}-${DEVICE}.arm` to `build.${DISTRONAME}-`** (the fork's roots since `43d0bc3bf4`; `DISTRO` is still `ROCKNIX`), with `git grep -F 'build.${DISTRO}-' -- projects packages` printing nothing on the merged tree as the check (T3's F-09); take upstream's `aethersx2-sa` deletion (`c4d353449e`, licensing; T3's F-07) rather than keep the recipe, as #644's finding 16 routes the retired overrides; the two calls open with the maintainer on
#346 (D-SYS-014, D-WORKFLOW-191); the host handoff file is read before any
runtime. **State at 2026-10-24 04:3x UTC:** T3 (#650) has stage C prepared and
waits for M7's return line for its Phase 4.6 (ten `bug` drafts at `00f535942a`;
context at 1 %, a compaction is expected); T5 (#652) is at stage B
(`da3e6559cc`, the 242-row coverage table); **T4 (#651) is briefed** at
version 1 (`docs/reviews/briefs/doctrine-rules.md`, `8a056c4a60`, Local),
the doctrine area epic **#807** filed (T4, T38 #685, T39 #686 retitled
`E807/T<k>`) with its futro (`docs/futros/2026-10-24-m6-doctrine.md`,
`12d163dd2c`, nine adjustments A1 to A9 for version 2), the stranger's proof
running, **the dispatch held for the maintainer's answer on #346 about a third
lane**; #808 (`bug`: `CLAUDE.md`'s rule table names 29 of 30) and #809
(Backlog: the inventory's three read-count renderings) filed from the
brief's re-derivation. **Two fix-packet streams for the M7 candidate**
(`docs/reviews/briefs/fix-packets-802-806.md`, `3f04de3342`, at the M7 lane's
request of about 04:30): #802 to T3 (`fix/m6-802-pcsx-rearmed32`, upstream
`c9820d0e89` with `${DISTRONAME}`), #806 to the T1 lane
(`fix/m6-806-grep-pcre2`); **both handed back and reviewed 04:3x**:
`a0defbd527` and `ea0af11d07`, one commit each on `8ebaf8daad`, told to M7
on the host file; M7 applies to its candidate tree and its images prove the
criteria; the two fix worktrees (`m6-802-pcsx-rearmed32`,
`m6-806-grep-pcre2`) are removed with `tools/fork-worktree remove` once M7
has consumed the packets. **M7 returned the host at 05:42** (relayed on #650 and #652); **both
lanes are at stage E** on their stream briefs (`docs/reviews/briefs/t3-streams.md`
S0 to S6 after audit issue #826 and bugs #813 to #825 -- #825 the security
defect in RetroArch patch 0012, the maintainer notified, M7 told, #585
given the row; `t5-streams.md` E1 to E8 after audit issue #837 and bugs
#827 to #836; D-WORKFLOW-193 written for E6). #838 and #839 filed for T3's
routed items. **S0 reviewed 06:3x**: `fix/m6-825-cheevos-hook-no-shell` at
`fac139dd43` (merged into the slice branch as `faac89ffc0`), the hook half
proven on the guest, the RetroArch half `fix-pending-image`; M7 told the
hash; the fix worktree stays until M7 consumes it. **T3 accepted at hand-back 07:1x** (`d9003d819f`; `reviewed-at d606301784`,
`fixed-at 3c47325fb2`; #826 closed completed; 14 of 15 ticked, the
`renovation-status` clause at the merge; its `slices.json` row written when
this branch takes P1's at integration; #823 and #841 close at the merge; the
eleven `fix-pending-image` items at the first image). **T5 accepted at hand-back 07:2x** (`52e6794ba7`; `reviewed-at 46f6c7d428`,
`fixed-at 877775e61e`; #837 closed completed; 15 of 16 ticked; the
coordinator's rows on #652: the container pin at the first M6 build, the three
base-merge files, the ccache measurement, `areas.json` at the P1 merge). Both
work lanes idle. **T6 accepted at hand-back 08:5x** (`ec5f7cf3fd`; `reviewed-at b96e1ca761`,
`fixed-at 820e413179`; #846 closed; 15 of 16 ticked; S1 #845's exit 2, S2 the
late-binding list widened; the sweep's leads on #654, #655, #657; the merge
after T5's, before T4's). **T6 dispatched 08:0x** (brief version 2 `3d60062ce5`; lane
`feature/m6-build-engine-upstream-tools-653` at `b96e1ca761` in
`m6-build-engine-upstream-tools-653`, the T5 session `m6-t5-build-engine`;
Local, no calls). **A merge recipe stops on the union script's failure and on a
non-empty marker grep before `git add`** (the first T6 push carried markers;
replaced within minutes; #696). **T30 dispatched 08:2x** (brief version 2 `b81fc193a1`; lane
`feature/m6-emulators-standalone-677` at `c7e3dfcc87` in `m6-emulators-standalone-677`,
the T3 session `m6-t3-emulators`; Extended, the two calls authorized; VNC 24,
SSH 10037). **Earlier:** T30 (`docs/reviews/briefs/emulators-standalone.md`, Extended, for the T3
session in `m6-emulators-standalone-677`), both at version 1 with futro
addenda, their stranger's proofs running at 07:3x; version 2, the issues'
sixteen criteria, the worktrees stacked on P1 + this tip, the seeds, then the
dispatch comments. **Tree exports go under `/workspace/tmp/m6-coordinator/`,
never the scratchpad on `/tmp`** (the tmpfs ran out of inodes at 07:13 under
two lanes' exports). **Rule edits by this lane
since `8ebaf8daad`** (the ledger the doctrine futro's A7 asks for; posted on
#651 once T4 is at stage A, and listed here as they happen):
`8c9b1d4721` `generic-x64-vm-testing.md` +7, lines 1225 to 1231 (`time-to-play`'s
reboot drops bind mounts, #797); `ab8f750784` `engineering-practices.md`
+7, a bullet under § A name is not a behaviour (a count or a line number is
a claim about one tree; blindspot 75's guard). **Accepted lanes' rule
edits, the coordinator's by acceptance, reaching `next` in the merge order:**
T2 `f16cf7fc28` `es-native-ui.md` +5/-1 (#699's `--root` paragraph). The
registers' and the friction log's appends are not rule edits. **T4's brief is
at version 2** (`0921782112`); #810 (the lint refuses Local at epic tier) is fixed on
`fix/m6-810-lint-local-epic` (`fa6bcdafa8`, T1's lane) and merged here at
`18747fbc52`; T4's dispatch now waits only on the maintainer's answer on #346. A
`fix/*` branch stays one commit; its work-log entry is this lane's. Both lanes report on their issues; nothing wakes this lane on a
post, so read #648 and #649 at every turn. **And nothing wakes a lane on a
comment:** a lane's turn ends when it posts a question, so every answer the
coordinator gives on an issue is also sent as `herdr agent prompt <lane>`,
the same minute (T1 sat idle 78 minutes on 2026-10-23 after an answer that
was only a comment). Before calling a lane idle, read its worktree's branch
and status, not the origin. **A seed ends with "do not end a turn on a post that asks nothing; post checkpoints and continue"** (T5 stopped after stage A on 2026-10-24 because its seed's list ended there), and the agent-state watch (`herdr agent get`, every 30 s, idle named at ten minutes) is armed for every working lane. A prompt that does not flip a lane to `working`
within a minute went nowhere: `herdr agent read <lane>` shows why (a settings or
usage dialog eats typed text; `herdr agent send-keys <lane> esc`, then the
prompt, then `send-keys enter`).

## State at 2026-10-24 (the coordinator's own update, midday)

The day's work log (`docs/work-logs/2026_10-work_logs/2026_10_24-work_log.md`)
is the narrative; this is the index of what a resuming agent must know.

- **Host.** M7 returned the host at 05:42 (its last block on
  `/tmp/m7-m6-host-coordination-20261023.txt`); M6 holds it. T30's guest
  cycles run under that hold with census lines; every M6 block on the file
  is an `== M6 coordinator -- HH:MM UTC:` ack with the census
  (`pgrep -c -x qemu-system-x86`, M6 pidfiles, compilers). Read the file
  before any runtime. `upstream/next` moved from `e0f9deb899` to `481c9d0d75`
  at 13:4x (heroic 2.22.4, one recipe): every slice's (a) read stays a fact
  about `e0f9deb899`, and the base merge at integration is against the
  `upstream/next` of that day, with `tools/renovation-drift` run first. `/tmp` is a tmpfs that ran out of inodes at 07:13:
  tree exports and simulated merges go under `/workspace/tmp/m6-coordinator/`
  after `df -i`.
- **Lanes and sessions.** `m6-t3-emulators` (pane `wN:p6`) ran T3 and T30 and runs T24 in
  `distribution.worktrees/m6-emulators-dead-ends-671`; `m6-t5-build-engine`
  (pane `wN:p7`) ran T5, T6 and T7 and runs T8 in
  `distribution.worktrees/m6-image-packages-655`; the T1 session ran the
  #802/#806/#825/#810 fix packets and cut the #877, #887, #889 and #890 packets. A lane's worktree is
  read with `git -C`, never written. The agent-state watch (`herdr agent
  get` every 30 s, idle named at ten minutes) is re-armed for every working
  lane; before calling a lane idle, read its worktree and the host's
  processes (a Facilitator call in flight is a wait, not idleness).
- **Register and blindspots.** Decided rows end at D-WORKFLOW-196 on this
  branch (193: an archive without `PKG_SHA256` fails the fetch; 194: five
  archive versions in four recipes; 195: a seat cut by its output ceiling
  re-runs on a trimmed packet, same model and effort; 196: an empty
  `PKG_SHA256=""` is a missing checksum, `libfmt` the sixth); the next free
  ID was 197 at midday; **since: 197 (seven archive versions, `simple-http-server`), 198 (glslang's modify/delete keeps the fork's copy), 199 (the spirv triple); the next free ID is 200** and a lane may take it. Blindspot entries run to 76 (75: a corpus read on the wrong tree, guard `engineering-practices.md` bullet `ab8f750784`; 76: a merge chain that does not stop on its own check, guard `.githooks/pre-commit`'s marker refusal, #696); 29 is used
  twice (#811).
- **Briefs and streams on this branch:** `docs/reviews/briefs/` holds the
  slice briefs (p1-survey, os-launch-control-state, es-launch-path,
  emulators-libretro, emulators-standalone, build-engine,
  build-engine-upstream-tools, doctrine-rules, generic-packages-reached v2, image-packages v2,
  emulators-dead-ends v2), the stream briefs (`t1-` to `t8-streams.md`,
  `t30-streams.md`, `fix-packets-802-806.md`, `fix-packet-libfmt.md`,
  `fix-packet-simple-http-server.md`, `fix-packet-887-melonds-toml.md`,
  `fix-packet-889-scan-toml.md`, `lint-local-epic-tier.md`); `docs/futros/2026-10-24-m6-*.md` the area
  futros (doctrine, build-engine, emulators-and-cores, generic-packages).
- **Issues filed by this lane today:** #807, #808, #809, #810 (fixed, merged
  here at `18747fbc52`), #811, #838, #839, #842, #843, #844, #847, #848, #849,
  #850, #851, #852, #873 to #879, #885, #888, #890, #896, #897, #898, #901, #903. The lanes
  filed #813 to #837, #841, #845, #846, #880 to #884, #886, #887, #889, #891 to #895,
  #899, #900, #902, #904 to #912.
- **Open with the maintainer on #346:** (the third lane for T4 is moot: T4 runs in the T3 session since 14:34); the #825
  disclosure timing; `LOCAL_SSH_KEYS_FILE` in Docker builds; D-SYS-014;
  D-WORKFLOW-191 (the `portaudio` question was withdrawn: the mirror serves it; #849 corrected).
- **Integration (after the M7 candidate):** P0, P1, T1, T2, T3, T30, **`fix/m6-877-libfmt-sha256` (`cf3a8d8e62`) and `fix/m6-890-shs-sha256` (`566b01448f`), the two checksums T5's fetch would refuse**, T5, T6,
  T7 (`db6597356b`), T24 (`26e4a34edf`) after T30's, T8 (`f50a031158`), T9 (`feature/m6-tooling-build-supervision-656`, **accepted at `bf4445a13c`**, #924 closed; at its merge and T10's, the `fork-newdrive` index row and list entry leave with T10's deletions over T9's "retired" row), T14 (`feature/m6-tooling-state-tests-661`, dispatched 20:16 UTC from brief v2 `27d8942071`, lane `30da4853bb`) at its hand-back after T12's, T12 (`feature/m6-tooling-vm-harness-659`, dispatched 19:04 UTC from brief v2 `74de5c1610`, lane `facb2ae523`) at its hand-back after T10's, T10 (`feature/m6-tooling-guards-657`, **accepted at `afdce9a65b`, complete at `7182f743ea`**, #958 closed; at its merge: its deletions of the two `fork-newdrive` rule entries over T9's "retired" row, and the `fix-pending-ci` read of #944 at the first `next` run after T9's and T10's merges; dispatched 16:26 UTC from brief v2 `2a4be1006b`, lane `a82d784216`) at its hand-back after T9's, a packet for #902 cut over `next` once T3's and T30's branches are in (five of its seven files are T30's, one T3's; the T1 session cuts it; its guest proof then), T4 (`6ec78bbf8c`, complete) last; #887 (`c60cdddf8b`) and #889 (`828472eb59`) after T30's branch; T8's conflict list (11 rows) read under
  D-WORKFLOW-198/199 with the `spirv-headers` override kept; at integration flip `add_es_system`'s zero-default WARNING to
  `return 1` after T3's S2 and regenerate the five tables; the #802/#806/#825
  adaptations; close #823, #841, #845 and the other fixed bugs at the merge;
  the `fix-pending-image` rows are proved on the first image.

## The seed brief (2026-10-22, the planning session's handoff, verbatim)

The first message this lane received, pasted by the maintainer from the P0
planning session; kept here because the maintainer asked that the lane consult
it at each step (*"You should have a copy of the original seed I provided for
this exercise"*). The intent it serves is D-WORKFLOW-181's, in the maintainer's
words there.

> Started by the P0 planning session (Claude Fable 5.1, Herdr pane wN:p1, tab "P0 planning (#346)") on the maintainer's direction of 2026-10-22. You are the M6 coordinator lane (D-WORKFLOW-183): the renovation program's planner, brief-writer, gate-acceptor and integrator, running on Fable; the work lanes run on Opus 5.5. Your worktree is /workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346 on feature/m6-renovation-plan-346; the primary checkout /workspace/repos/pixelelated/distribution stays on next with no resident session, and you are its keeper. Read first, in this order: .github/sessions/saved-session-state-feature-m6-renovation-plan-346.md (your lane's pointer), docs/reviews/plan-for-the-plan.md, the live M6 milestone body, issues #346, #641 and #640 on pixelelated/distribution, then next:AGENTS.md and the every-session rules. The maintainer's direction, verbatim: "the coordinator will be Fable and the work will be Opus 5.5" and "we begin our work and ensure that everything is in the new work tree with the seeded session file to resume, and that there's a corresponding branch. We can then begin work there." Gates: nothing merges to next until the M7 lane's post-candidate merge clears the push guard, and never with --no-verify; the P1 lane (Herdr tab "P1 Survey (#641)", agent m6-p1-survey, worktree m6-p1-survey-641) pauses at its pass-7 gate on #641 for the maintainer's yes, which reaches it through you, one question at a time; you accept P1 at hand-back against brief section 10; one session per worktree, so never write in the P1 worktree. Report on #346 and #641. First action: read your pointer and the plan, confirm on #346 in one comment that you have resumed (your session id from herdr agent list, this pane, the time), then wait for P1's pass-7 post or the maintainer; do not start new work streams on your own.  Also: append this lane start to docs/work-logs/2026_10-work_logs/2026_10_22-work_log.md in your worktree (the planning session writes there no longer, one session per worktree), run tools/work-log-index --write, commit with Refs #346 and push; and note on #346 that Claude Code reports the 25 instruction files at 324.2k characters, over its 150k limit, so the rules load truncated in every lane, a finding for the doctrine slice.

