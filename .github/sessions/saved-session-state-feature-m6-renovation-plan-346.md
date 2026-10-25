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

**03:12-03:19 UTC (2026-10-25):** M7's build window granted from 03:12 with no start expiry (GENERIC_X64 then H700 builds, the GENERIC smoke, SM8550 after; M6 runs no guest, compiler or build during it). M7's selective-integration request for #825/#887/#889 answered on the host file at 03:15 (`fac139dd43`, `c60cdddf8b`, `828472eb59`, each one commit on `8ebaf8daad` on its pushed `fix/m6-*` branch). **Register: D-WORKFLOW-206 and 207 are M7's; M6 uses 208 and up** (lanes told). T45 stage B done at `474c434fa4` with fifteen leads and no bug; Backlogs #1044 (fork side) and #1045 (the export refresh) filed for them; the lane is at stage D. T15 at S1 done (#1018 `3037ce6b8c`), #1020 in progress with shape (a).

**T45 (#692) accepted at 03:33 UTC (2026-10-25)** at the hand-back `bbb5f28824`, the coordinator's branch merged in at `cd08f82d07`; #1046 closed (ticked=15 open=0); #692 at 15 of 16 (the pre-merge checker line open until the merge into `next`); Backlogs #1044 and #1045 hold its leads, #1043 the seal keys. The lane's close-out (`audit-completion.json`, the lint with `--issue 1046`, the pointer idle, its scratch removed) was prompted; its merge into `next` comes after T15's, before T4's. `$S/t45-accept.sh` corrected to archive `projects/` for the simulated-merge check. T15 at stage E: #1018 and #1020 committed (`7cb11eb379`), #1029/#1038 then S2 next, the `--old` shape ruled at 03:34 (per-tool provenance under `--old` only).

**03:40-03:57 UTC (2026-10-25):** T23 (#670) briefed for the freed T5 session: brief v1 `16dee83d38` (a reachability table at Local depth; D-WORKFLOW-209: the lane removes nothing; the `PKG_DEPENDS_UNPACK` gap in `tools/renovation-inventory` is the brief's first finding); **dispatched 04:11** to `m6-t5-build-engine` from v2 `74b71ab443` (the proof's three wrongs fixed: 5 dead pairs not 32; the tier's meaning; the checks against the dispatch tip); lane tip `27b015c901` (merges `f532c23876`, `36cb455e3c`); `$S/t23-accept.sh` ready (usage `AUDIT_ISSUE=<n> t23-accept.sh <tip> <coordinator tip>`, `DISPATCH_TIP=27b015c901`); stage A (`6208f69e78`) and B (`96ab1ab210`) done -- 731 dispositions, five units reached after all, three bugs to file at stage D; the brief corrected at `0a5676ea5d` (plan generation reads one checksum; the pkgcheck sweep form); **#1048** is the decision issue for the four deferrals. **T23 accepted 04:40** at `12374c733d` (merged `44fc2fe436`); #1052 closed; #670 at 15 of 16; the class decision on #346 (04:40) awaits the maintainer's word (then a D-WORKFLOW-210+ row and the two removal packets); the lane's close-out prompted; the merge after T8's, before T9's. **T13 (#660) dispatched 04:58** to `m6-t1-os-launch` from v2 `6aa2fbaadb` (the proof's six wrongs fixed; #909's fix is on T4's branch); lane tip `e1d51b3a04` (merge `ef56509d36`); `$S/t13-accept.sh` ready (usage `AUDIT_ISSUE=<n> DISPATCH_TIP=e1d51b3a04 t13-accept.sh <tip> <coordinator tip>`); **its guest cycle is held behind M7's FINAL RETURN and granted on #660 by the coordinator** (the lane asks at the end of stage A); its seat is the one `run invoke`; merge order after T12's, before T14's. **D-INFRA-032 is M7's; M6's next infrastructure row is 033+.** The T5 session is idle after T23: **T40 (#687) briefed** at `aa21e2f52c` under the new patches area epic **#1054** (T40 to T43; the futro written); the stranger's proof running (`$S/t40-proof.md`); then v2, the worktree `m6-patches-dead-687` from `2174265e9c`, the pointer from `$S/t40-pointer.md` (V1HASH/MERGE1_HASH, V2HASH/MERGE2_HASH), `rewrite-body.py 687 ... t40-vm.txt`, an accept script derived from `$S/t23-accept.sh` (no plans, no curl shim; the header count, the get_pkg_directory answers, the Makefile count), the dispatch to `m6-t5-build-engine`. Merge order: after T8's, before T9's. **#1012** retitled to the runner's defect on M7's review and dispatched as a fix packet (`66f3b6eae5`) to the T1 session (`m6-t1-os-launch`) in `m6-1012-ttp-runner` on `fix/m6-1012-ttp-runner` (from T12's `f77dc6325e`); **accepted 04:01** at `af16f3391c` (four criteria ticked; the open item to test stays); the fix branch `fix/m6-1012-ttp-runner` merges into `next` after T12's `feature/m6-tooling-vm-harness-659` in the integration order. **#775**: the gate stated on the issue (ES `23e8dccfa`, T2's; image-proven nowhere; M7's call under D-WORKFLOW-191). **M7's 03:43 window** open (helper compile done 03:45; two guests pending); D-WORKFLOW-206 to 208 are M7's; M6 uses 209 and up (209 written).

**04:11-04:19 UTC (2026-10-25):** T23 dispatched (above). **#1047** filed: the cloud sync and saves area epic (T13 #660, T16 #663, T17 #664; the three re-parented and retitled `E1047/T<k>`); T13 is the next slice for the idle T1 session: the futro `docs/futros/2026-10-25-m6-cloud-sync-and-saves.md` and the brief `docs/reviews/briefs/cloud-harness.md` are to be written from the research notes `$S/t13-research.md` (a read-only subagent, running), then the stranger's proof, the worktree `m6-cloud-harness-660` from `2174265e9c`, the dispatch to `m6-t1-os-launch`. M7's swap question (its guest's qemu-img conversion stopped by its own guard on SwapFree 0) answered 04:18 from the host's numbers: no M6 reclaim or pressure; the documented file-copy refill; serialization agreed. M7's #775 packet (`23e8dccfa` + #779) is its own under D-WORKFLOW-191.

**04:58-05:41 UTC (2026-10-25):** T13 (#660) dispatched 04:58 to the T1 session from brief v2 `6aa2fbaadb` (corrected `42db7308c6`; worktree `m6-cloud-harness-660`, dispatch tip `e1d51b3a04`; its guest window asked of M7 and HELD behind the M7 lane's full `bcc866f1` build window, granted 05:22, until that FINAL RETURN); stage B done at `779b39db8c`, stages C/D running. The patches area epic #1054 filed and its futro posted; T40 (#687) briefed v1 `aa21e2f52c` and, from the stranger's proof, v2 `92f2f35c16`; **T40 dispatched 05:26 to the T5 session**: worktree `m6-patches-dead-687` on `feature/m6-patches-dead-687` (from `2174265e9c`, the coordinator's tip merged once at `26875c972d`), lane tip `b8cde6f305` (= the dispatch tip), stage A; accept with `$S/t40-accept.sh`, to derive from `t23-accept.sh` (no plans, no curl shim; `DISPATCH_TIP=b8cde6f305`). At 05:25 the M7 lane found T15's five S2 shells holding `QA_SYSTEM_ROOT` on the `069fc2704421` root it needed to move; T15 stopped them at 05:30 (#662), the M7 lane renamed that root to `m7-signin-generic-build-20261025-01` (gone for good, rebuilt from `bcc866f1`), and M6 retained its own donor at `/workspace/artifacts/m6-donor/1a0266484423/image/system` (busybox, 146 links, rclone v1.75.2, os-release; byte-equal from `m7-pixelelated-replacement20`'s root; RECORD.txt and SHA256SUMS beside it; owning issue #662): every T15 run from here and `t15-accept.sh`'s run A use it, no M6 run names an M7 root again, and T15's serial runs resume beside M7's build (a `PAUSE T15` line on the host file stops them at a run boundary). The brief's § Root change and #662's VM line and final-run criterion carry it; the host file carries M6's disposition block.

**05:4x-06:02 UTC (2026-10-25):** T40 ran stages A to H in 25 minutes and is **accepted** at `e863379cec` (its `29b3f478e5` with the coordinator's `737a726224` merged at hand-back; `$S/t40-accept.sh` on a clone, report `/workspace/tmp/m6-coordinator/accept-t40.out`), closed out at `bf3409ea18`; #1074 closed; bugs #1071 (vitaquake2-lr, area #798), #1072 (ES cpugov, area #700), #1056 (the inventory's symlink gap) open; the 50 leads on #689; the class decision's second half on #346 (keep recommended; a yes becomes D-WORKFLOW-210+ and closes #1048). The T5 session is idle: its next slice (T11 or T22 by the order) needs a research pass, a futro/brief and a stranger's proof before dispatch. T13 reached its stage-D pause at `2454d3e123` (14 bugs #1057-#1070, audit #1073, the seat's one rule break recorded), the rulings applied at `8a2518fa44` (#1081 the census bug; the six Backlogs #1075-#1080 filed by the coordinator), and **stage E runs under `docs/reviews/briefs/t13-streams.md`** (three streams by tool; the guest cycle, still held behind M7's FINAL RETURN, carries the six guest-bound positives under a 45-minute bound; the lane posts the cycle's plan before the grant). T15 runs its serial S2 suite on the retained donor beside M7's build.

**06:0x-06:44 UTC (2026-10-25):** The devices area epic **#1082** filed (T11 #658, T25 #672, T27 #674, T28 #675 re-parented and retitled `E1082`), its futro `docs/futros/2026-10-25-m6-devices.md`, and T11's brief `docs/reviews/briefs/device-generic-x64-and-kernel.md` v1 `9ba389c9ce`, v2 `5bb8828b71` from a stranger's proof (`$S/t11-proof.md`; the research digest `$S/t11-research.md` with `t11-paths.txt`/`t11-rows.json`). **T11 dispatched 06:43 to the T5 session**: worktree `m6-device-generic-x64-658` on `feature/m6-device-generic-x64-658` (from `2174265e9c`, the coordinator's tip merged at `d72afeff0a`), lane tip `2103f0271d` (= the dispatch tip), stage A; accept with `$S/t11-accept.sh` (`AUDIT_ISSUE=<n> BUGS=... DISPATCH_TIP=2103f0271d`). T13's stage E is done (`eb31ea0e9a`, `fixed-at` `cee4bf481d`; the lane idle at `d8ab360340` until the guest grant; its cycle plan is on #660, about 32 minutes with the same-guest #1057 run as step 5b; grant it on #660 as its own comment at M7's FINAL RETURN, then stages F to H, then `t13-accept.sh` extended with the streams' host positives). T15's second queue runs on the retained donor (about six hours; root-final passed). M7 asked for and got the H700 caches released (no M6 consumer; the five references historical). Next briefs: T22 (#669, Extended) for the T1 session after T13; T27 (#674) for the next freed session.

**06:5x-07:36 UTC (2026-10-25):** Two briefs written ahead of their sessions from read-only research passes and stranger's proofs: **T27** (`docs/reviews/briefs/device-h700.md`, v2 `d292110962`; `$S/t27-research.md`, `t27-proof.md`, `t27-pointer.md`, `t27-accept.sh`; the H700 configuration has a base, upstream's own copy, 12 / 13; nothing runs on a unit) for the T5 session when T11 closes out, and **T22** (`docs/reviews/briefs/os-system-services.md`, v2 `41875841af`; `$S/t22-research.md`, `t22-proof.md`; Extended with two seats as T1's -- the gemini-argon route and the lint's acceptance are on this branch, not at the P1 tip; two selection mechanisms; 29 root units; one guest cycle after T13's) for the T1 session after T13's close-out (its pointer template and accept script still to derive; #669 retitled `E695/T22` at dispatch). **T11** reached stage C at `b501bdad67` (the seat ran; two of its items refuted by fixture, one with `mtools` copied from an M7 toolchain -- an M7-root read, recorded; its M7-root reads of the built `.config` accepted as evidence with provenance) and its fourteen punch items were dispositioned at 07:34 (#658): five bugs the lane files (PL-08 the inventory's third gap, PL-11's modeswitch half, PL-12 `dtb_overlay`, PL-13 the launcher's pidfile, PL-14 `install`/`release` masking failures beside #827), three Backlogs filed (#1083 the guest's firmware list after T5's E6, #1084 the configuration's regeneration, #1085 the UTM README), PL-06's four dead branches of the fork-own `install` removed in the stream (the coordinator's decision), PL-03/PL-10 resolved there, PL-02/05/09 recorded (PL-09 into the merge notes: **a merge of `next` must keep GENERIC_X64 in the override's version case**). The stage-E brief (S1 `install`+`release`, S2 the launcher, S3 the udev rule and `options`, S4 `dtb_overlay`) follows T11's stage-D post. T13's stream positives reproduced from the branch (`accept-t13e.out`); its retention answer given; its drivers on the branch at `537361499b`.

**07:3x-08:08 UTC (2026-10-25):** **T11 accepted** at `47672fe4a0` (its `871c5a6bc0` with the coordinator's `cc8b6cf2a3`; stage-E streams S1-S4 under `docs/reviews/briefs/t11-streams.md` `46df9643d3`; `$S/t11-accept.sh` on the stage-D tip `499628a049` and on the merged tip, then `stage-e/run-all.sh` 47/0/0; reports `accept-t11.out`, `accept-t11-final.out`); #1091 closed; #1087-#1090 ticked and open until `next`; #1086 is T10's; Backlogs #1083 #1084 #1085; the close-out awaited, then **T27 dispatched to the T5 session** (prepared: #674 body from brief v3 `cc8b6cf2a3`, worktree `m6-device-h700-674`, merge `d48302d739`, lane tip `ed7fd0ea50`, `$S/t27-dispatch.md` drafted with `__TS__`/`__Q__`/`__C__` placeholders; accept with `$S/t27-accept.sh`, `DISPATCH_TIP=ed7fd0ea50`). **Merge note from T11's F-09: a merge of `next` must keep GENERIC_X64 in the override's version case (`projects/ROCKNIX/packages/linux/package.mk`), or the build has no `PKG_VERSION`.** T13's guest cycle started 07:52:28 under M6 ownership after M7's FINAL RETURN (07:4x; H700 and SM8550 built; caches renamed to `m7-signin-{h700,sm8550}-build-20261025-01`); RETURN due by 08:37, a harness waiter on #660; then its retention step, stages F-H, hand-back, `t13-accept.sh` + the guest ticks, and T22 (brief v3 `41875841af`→ its version-3 commit `cc8b6cf2a3`; `$S/t22-accept.sh`, `t22-pointer.md`) to the T1 session with #669 retitled `E695/T22`. T15's queue restarts at `e430d61cfa` for the rest of the twelve.

**08:0x-08:16 UTC (2026-10-25):** T11 closed out at `ed8c48f3cd`; **T27 dispatched 08:09** to the T5 session (lane tip `ed7fd0ea50`; stage A at 08:12 reproduced every figure; the bare `--since` erratum ruled). **T13's cycle RETURNED 08:10** (17 minutes; record `a5522b8eb8`): #1062, #1064, #1065 (fixed in-window `a70b4889a3`), #1069, #1070 met; #1057 refused by the #91 guard (needs two guests); **#1067's `rclone serve sftp` endpoint fails the content tier over SFTP (7 checks, rclone exit 5; host server 1.60.1-DEV vs client 1.75.2)** -- ruled (a) fix forward on the host with the donor's 1.75.2 rclone as the client, `CLOUD_QA_RCLONE` if the server's generation is the cause, bound **09:15 UTC** else revert `94c050ed5a`; **a second window granted**: a guest pair, 25 minutes, the SFTP suite then A5/RETENTION with two guests; KILL1's 124 branch and A15's needle are stage-F fixes; the retention step waits for the second RETURN; then stages F-H, hand-back, `t13-accept.sh` + `t13-accept-e.sh` + the guest ticks. **T22 prepared**: #669 retitled `E695/T22` under #695, body from brief v3 `cc8b6cf2a3`, worktree `m6-os-system-services-669` (merge `3d56c56380`), lane tip `cf78d8fd62`, `$S/t22-dispatch.md` drafted (`__TS__`/`__Q__`/`__C__` placeholders) -- posted after T13's close-out, with its guest cycle granted after T13's second window. T15 runs the rest of the twelve at `e430d61cfa`.

**08:3x-08:4x UTC (2026-10-25):** T13's third window returned at 08:42 (#1092 and #1093 ticked from guest a; mirrored on the host file); T13 is in stages F to H. T27's stage-D dispositions are on #674 (08:40): bug #1095 (PL-12) with its fix as the one stream in `docs/reviews/briefs/t27-streams.md` (`64e56a3136`), audit issue #1096, Backlog #1094 (PL-03), the serial debug-shell policy question on #346 (PL-13), pointers on #672, #44 and #669; the lane's hand-back of A to D is at `70df17982c` and S1 is running. Next for the coordinator: T13's hand-back and acceptance, then T22's dispatch (`$S/t22-dispatch.md`, placeholders `__TS__`, `__Q__`, `__C__`); T27's acceptance after H via `$S/t27-accept.sh` with `AUDIT_ISSUE=1096 BUGS=1095 DISPATCH_TIP=ed7fd0ea50`, the audit issue ticked from the Phase 7 table, then the close-out.

**08:4x-08:5x UTC (2026-10-25):** **T27 accepted** at `78579255e4` (the lane's `0459859b84` with the coordinator's `161effca8f`; report `/workspace/tmp/m6-coordinator/accept-t27.out`; #674 16 of 17 ticked, #1096 closed 14 of 14, #1095 open until `next`; brief errata `db6c8f55cc`; the M6 body updated 08:54); its close-out is prompted to the T5 session (audit-completion.json, the lint with `--issue 1096`, the pointer idle, `/workspace/tmp/m6-t27/` removed, the tip posted on #674). T13's retro proposals housed: Backlog #1097, T22's dispatch line, scoped-audit step 5 at `161effca8f`, the #909 comment. Waiting on T13's stage H (then the hand-back merge, `AUDIT_ISSUE=1073 DISPATCH_TIP=e1d51b3a04 $S/t13-accept.sh <tip> <co tip>` and `$S/t13-accept-e.sh <tip>`, the ticks, `$S/t13-retro-dispositions.md` posted with the acceptance, the close-out), then T22's dispatch.

**08:5x-09:0x UTC (2026-10-25):** **T27 closed out** at `0ac98afe43` (the T5 session idle; the gitignored leftovers stay until retirement). **T13 accepted** at `a7a5bb94aa` (reports `accept-t13-final.out`, `accept-t13e-final.out`; #660 15 of 16, #1073 closed 26 of 26, the 17 bugs open until `next`; Backlog #1098 for the puts' exits); its close-out prompted to the T1 session at 09:01. T25's research digest is being written by a read-only subagent into `$S/t25-research.md` (the brief follows, then the stranger's proof). Next: T13's close-out tip → T22's dispatch (`$S/t22-dispatch.md`: `__TS__` at post time; `__Q__` and `__C__` on its line 7).

**09:0x UTC (2026-10-25):** **T13 closed out** at `0b72904621` (the T1 session free). **T22 (#669) dispatched 09:05** to the T1 session: worktree `/workspace/repos/pixelelated/distribution.worktrees/m6-os-system-services-669`, branch `feature/m6-os-system-services-669`, dispatch tip `4a48d388c4` (the coordinator's `1b752289e0` merged at `311c1f7972` after the seed's `3d56c56380`), brief v3 `cc8b6cf2a3`; its guest cycle is granted on #669 on request; acceptance via `$S/t22-accept.sh` with `DISPATCH_TIP=4a48d388c4`. The M6 body carries T13 accepted/closed out and the next action (T22 running; T25's brief, then T28's). The T5 session idles for T25 (#672): research digest in `$S/t25-research.md` (read-only subagent), then the brief `docs/reviews/briefs/devices-unshipped.md`, the stranger's proof from the scratch clone, the worktree cut from `2174265e9c` with the coordinator tip merged, the pointer seed, the dispatch.

**09:1x-09:3x UTC (2026-10-25):** T22's guest window ran 09:13-09:16 (START/RETURN mirrored on the host file); T22 is in stage C (two seats). **T25 (#672) dispatched 09:39** to the T5 session: worktree `/workspace/repos/pixelelated/distribution.worktrees/m6-devices-unshipped-672`, branch `feature/m6-devices-unshipped-672`, lane tip `b27889bce2` (P1's `2174265e9c` with the coordinator's `55e414441d` merged at `7d61fe0f96`), brief v2 `55e414441d` (Local; no seat, no guest); acceptance via a `$S/t25-accept.sh` to be written from `t27-accept.sh`'s shape (the block from the brief's second fence, every § 5 check, the tables' row counts 397 / 25 / 12 / 9 / 53 / 10, the Local plan file, the lint, the simulated merge, the audit issue's checkboxes). Next: T28's brief (#675, SM8550) from a research digest for the next idle session; T22's stage-C checkpoint and its stage-D dispositions; T15's queue.

**09:4x-10:1x UTC (2026-10-25):** T25 is in stage C (stage B at `304a17ebda`, the tables generated; errata kept in `$S/t25-errata.md`; Backlog #1101 for the inventory's unpack edges). T22 is in stage C (the seats' second round running). **T28's brief v1** at `4620b18497` (`docs/reviews/briefs/device-sm8550.md`; Backlogs #1099 boot change at the merge, #1100 runbook section); the stranger's proof is running into `$S/t28-proof.md`; version 2 follows it; then the worktree `m6-device-sm8550-675` cut from `2174265e9c` with the coordinator's tip merged, `$S/t28-pointer.md` and `$S/t28-dispatch.md` seeded (placeholders), #675's body rewritten (17 criteria, the VM line Yes on the host), and the dispatch to the first of T1 (after T22) and T3 (after T15's queue) to go idle. Acceptance scripts: `$S/t25-accept.sh` written; `$S/t28-accept.sh` to write from `t27-accept.sh`.

**10:1x UTC (2026-10-25):** both lanes at their stage-D pauses, ruled: **T25** (#672, audit #1102, no bug, no stream; PL-01 → #1101, PL-02 posted on #346 as the devices half of the class decision; F to H next, then `$S/t25-accept.sh` with `AUDIT_ISSUE=1102 DISPATCH_TIP=b27889bce2`); **T22** (#669, audit #1103, 28 items; bugs PL-02, PL-03, PL-05, PL-28 and PL-01 if the mount is unsafe; the Lows to #585 as the lane's block; PL-08 and the root-surfaces list to #346; PL-16/17 → #1104; PL-20 the coordinator's rule edit at acceptance). T22's second window (15 min, four cases) granted 10:13, mirror armed; **the stream brief `docs/reviews/briefs/t22-streams.md` is written after its RETURN** (S1 `scripts/init`'s update writes and the rejected-update mount; S2 `input_sense`; S3 `095-cloud-ssh`; S4 `udevil.conf` if PL-01 mounts unsafe), with host fixtures as T27's S1. T28's proof pending; then version 2, the worktree, the body, the dispatch to the first idle session.

**10:2x UTC (2026-10-25):** **T25 accepted** at `68dc79793f` (report `accept-t25.out`; #672 13 of 14, #1102 closed 5 of 5; errata `418203399c`; close-out prompted to the T5 session, then idle for T28). T22's second window running since 10:14 (mirror armed); on its RETURN: the ruling on PL-01, the stream brief `t22-streams.md` (`7c64407e62`) posted, the lane's bugs, stage E. T28's proof pending → version 2 → worktree `m6-device-sm8550-675` (cut from `2174265e9c`, merge, pointer `$S/t28-pointer.md`), body (17 criteria), dispatch (`$S/t28-dispatch.md`) to the first idle session (T5 after T25's close-out is the likely one now).

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

