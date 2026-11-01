# Week 2026-W43 (October 19–25): The renovation's plan, its survey and its first twenty-three slices

Written October 26 by the M6 coordinator lane from the dated daily logs, the
work-log index and the friction log, as the ceremony asks. The week is mostly
M6's: no day file for October 19–21 exists on this branch, on `next` or on any
of the 33 M6 lane branches, so the M7 lane appears only through the tracker and
the shared-host windows; it corrects anything here it knows better. Four day
files (October 22–25, 164 entries), 296 commits on the coordinator branch and
none on `next`, 496 issues filed (#622–#1117) and 29 closed. Refs #346, #339.

## Delivered during the week

#346 opened the program on October 22: the maintainer widened the
whole-codebase review into a renovation under M6 -- modernize, standards, bugs,
package currency, efficiency, dead ends, clarity -- in slices beside feature
work, Fable planning and Opus 5.5 executing from briefs (D-WORKFLOW-181). One
coordinator lane and one session per worktree, `next` the roll-up
(D-WORKFLOW-183), working from a fresh clone (D-INFRA-025; #640 moves the M7
checkout after its candidate, D-INFRA-026/027). P1 started without waiting
for a candidate (D-WORKFLOW-182), at the standing review depths (D-WORKFLOW-184).

#641, the survey, inventoried 133,520 distribution paths and 1,114
EmulationStation paths with none unassigned, into 46 slices, 13 at Extended
depth, with three new tools (`renovation-inventory`, `-drift`, `-status`). Its
questions settled the shipped set as H700 and SM8550 with GENERIC_X64 the test
image (D-WORKFLOW-185), the build process weighed before any chip
(D-WORKFLOW-186), and a renovation that gates no release (D-WORKFLOW-187).
Planning stays with the coordinator (D-WORKFLOW-189), which filed the slice
issues #648–#693 under #339; #641 closed on October 23. #644 read ROCKNIX's
build documentation against the fork's build path: 26 findings and #645.

#648 and #649 ran side by side (D-WORKFLOW-190). T1's audit #701 found 81
issues, two High (the netplay host reaching `runemu.sh`'s root `eval`;
`updateabl` writing both bootloader slots unchecked), with 60 bug issues at
its stage-D pause (#702–#761) and 61 by its retro. T2's #790 filed 23 bugs
(#767–#789); the netplay seam between them became D-WORKFLOW-192. Both were
accepted at hand-back early on October 24.

October 24 accepted fourteen slices -- T1, T2, T3, T5, T6, T7, T30, T24, T8,
T4, T9, T10, T14 and T12 -- under five new area epics (#798, #800, #807, #848,
#903), each opened with a futro. #825: RetroArch patch 0012 hands an
achievement's title to `system()` as root on every unlock, as upstream ROCKNIX
does; reproduced on the guest, the hook's half proven fixed. #802: the default
PlayStation core `pcsx_rearmed32` is installed where the launcher does not
load it, fixed upstream on 2026-10-04 (`c9820d0e89`) but not on `next`; it and
#806, a build-order race, went to the M7 candidate as fix packets.

The build engine now fails an archive fetch without `PKG_SHA256` and verifies
TLS (D-WORKFLOW-193), its count of unchecked versions refined from five to six
to seven (D-WORKFLOW-194/196/197). The guards slice filed 29 bugs from 44
findings (#929–#957; D-WORKFLOW-200/201/202/205), the preflight now reports
rather than stops guests (D-INFRA-028/029/030), and `vm-qa` and `time-to-play`
cannot pass over a skip or an empty cell (D-QA-061/062, D-INFRA-031). #659
moved neither number: first frame 0.69 and 0.76 s against 0.603 s recorded,
the exit sync 1.33 and 1.32 s (budget 3 s), game to game 1.01 s against 1.017 s.

October 25 accepted nine more -- T45, T23, T40, T11, T27, T13, T25, T22 and
T28 -- under #1047, #1054 and #1082. T45 found two council HMAC seal keys
committed on `next` since September (#1043), removed on the M6 branch with the
history put to the maintainer. Every fork suite now shares one exit lattice
(D-QA-063); a dead-end table removes nothing (D-WORKFLOW-209). T13 fixed
#1067 on the host (rclone serve's directory cache) and proved #1057 across two
guests. The M7 lane, whose #622–#643 carried sign-in refinements and two delta
audits (#633, #639), returned the host at 07:53 UTC (`bcc866f1`): GENERIC_X64
qualified, H700 and SM8550 built and read back.

## Friction and changes to the process

The friction log took 23 lines: one on October 22, ten each on the 23rd and
24th, two on the 25th. The main shape was a shell chain that ran past its own
failed step: merges pushed with conflict markers once on October 23 and twice
on the 24th, a refused commit followed by a comment naming the old tip
(blindspot 76; #696 asks pre-commit to refuse markers). The second was a lane
left idle: T1 seven hours at a known blocker and 78 minutes after an answer
posted only as a comment; a comment wakes nobody. The coordinator's own slips:
#895 closed with 19 checkboxes open until the lane's writer refused, clock-ahead
timestamps (#843), a census default (#1008), stale pointers (#1014), and a
credit error that ended the session for about 95 minutes on October 25 with
27 background monitors (#1017).

Thirty-four decided rows were written (seven, six, nineteen and two by day)
and two questions parked: D-WORKFLOW-191 (which build carries the renovation's
EmulationStation pins) and D-SYS-014 (Bluetooth keys under `/storage/roms`).
Beyond those above, D-WORKFLOW-195 reruns a seat cut by its output ceiling on
a trimmed packet, D-WORKFLOW-198/199 settle base-merge modify/delete conflicts,
D-WORKFLOW-203 is clerical and D-WORKFLOW-204 gives `renovation-status` its
states. Ten decided rows had sat under Open decisions; `register-check` now
refuses that (#646). Blindspots 74 (a fixture that silently did not engage),
75 (a corpus read on the wrong tree) and 76 were added on October 24.

Every slice ran its ceremonies: 11 futros and 24 mini-retros on the lane
branches, one retro for P1 and one per accepted slice. On the coordinator
branch 8 commits touched three rule files: `generic-x64-vm-testing.md` four
times (#669's guest lessons, T1's retro), `engineering-practices.md` three
(the `rc=$?` rule, blindspot 75's guard, hashes as tree claims) and
`device-builds.md` once (every field read per plan). The W42 summary was
written on October 24 (#254).

## Position at the end of October 25

Twenty-three of the 46 slices were accepted at hand-back and 21 of their audit
issues closed; #701 and #790 stay open on fixes only an image can show. T15
(#662), T16 (#663) and T29 (#676) were in their lanes and T17's research
(#664) had launched by 11:56 UTC, where this branch's record ends. Nothing had
merged to `next`, still at `8ebaf8daad` from October 17; P0 and P1 merge first,
after the M7 candidate, and every slice issue stays open until its merge. Of
the 496 issues filed, 467 were open, 311 labelled `bug`. Waiting on the
maintainer: #1043's history, #1048's class decision, D-WORKFLOW-191, D-SYS-014.

Sources: [October 22](2026_10_22-work_log.md), [October 23](2026_10_23-work_log.md),
[October 24](2026_10_24-work_log.md), [October 25](2026_10_25-work_log.md);
`docs/friction-log.md`; the decision and blindspot registers; `docs/futros/`;
the lane branches' `docs/retros/` (P1, T1, T12 and T45 read).

<details><summary>Evidence</summary>

All commands run on 2026-10-26 from the worktree on `feature/m6-renovation-plan-346`.

1. Day-log headings and counts (`/usr/bin/grep -c '^## '` per file):
   2026_10_19, _20, _21: MISSING. 2026_10_22: 211 lines, 10 entries;
   2026_10_23: 823 lines, 17; 2026_10_24: 1,224 lines, 84; 2026_10_25: 379
   lines, 53 (10+17+84+53 = 164). INDEX.md line 71: "Week 2026-W43, Oct 22 to
   Oct 25 (164 entries over 4 days)". Last heading of October 25 on this
   branch: 11:56 UTC (T29 stage A, T16 stage B, T17 research launched).
2. Lane refs (`git for-each-ref 'refs/remotes/origin/feature/m6-*'`): 33 refs.
   `next` and `origin/next` at `8ebaf8daad` 2026-10-17T06:02:46Z. No ref
   carries a 2026_10_19/20/21 day file (output truncated at 150 lines; the
   unique-file count in command 3 covers all 33 refs). Newest ref
   `origin/feature/m6-cloud-setup-content-664` also has 53 entries on Oct 25.
3. Retros and futros dated 10-19..10-25 across the 33 refs (`sort | uniq -c`):
   futros 11 distinct (2026-10-22 p1-survey; 10-23 interface, os-scripts-and-launch;
   10-24 build-engine, doctrine, emulators-and-cores, generic-packages,
   tooling-and-guards; 10-25 cloud-sync-and-saves, devices, patches-and-configs).
   Retros 24 distinct: 10-23 es-launch-path, p1-survey; 10-24 build-engine,
   build-engine-upstream-tools, doctrine-rules, emulators-dead-ends,
   emulators-libretro, emulators-standalone, generic-packages-reached,
   image-packages, os-launch-control-state, tooling-build-supervision,
   tooling-guards, tooling-state-tests, tooling-vm-harness; 10-25
   cloud-harness, device-generic-x64-and-kernel, device-h700, device-sm8550,
   devices-unshipped, generic-packages-dead-ends, os-system-services,
   patches-dead, tooling-council. This branch: the 10 futros from 10-23 on, no
   retro dated in the week.
   Friction: `grep -c -E '2026-10-(19|2[0-5])' docs/friction-log.md` = 23;
   by date 10-22: 1 (18:24), 10-23: 10 (02:15, 03:19, 06:40, 16:30 x2, 17:10,
   17:40, 17:30, 21:15, 21:50), 10-24: 10 (03:09, 03:57, 07:21, 08:05, 10:14,
   13:45, 14:51, 15:42, 22:12, 23:16), 10-25: 2 (00:37, 02:25).
   First register grep (`^\| ?2026-10-...`) returned 0: the date is column 2.
4. Register (`^\|.*2026-10-(19|2[0-5])`): 36 lines = 34 decided rows + 2 open
   rows that mention 2026-10-23 in text (D-WORKFLOW-191, D-SYS-014).
   10-22 (7): D-WORKFLOW-181, D-INFRA-025, 026, 027, D-WORKFLOW-182, 183, 184.
   10-23 (6): D-WORKFLOW-185, 186, 187, 189, 190, 192.
   10-24 (19): D-WORKFLOW-193, 194, 195, 196, 197, 198, 199, D-INFRA-028, 029,
   030, D-WORKFLOW-200, 201, 202, 203, 204, 205, D-QA-061, D-QA-062, D-INFRA-031.
   10-25 (2): D-QA-063, D-WORKFLOW-209.
   Not on this branch's register: D-WORKFLOW-188 (P1's order row, named in the
   P1 retro), 206/207 (reserved for M7 per the 03:20 entry), 208.
   Blindspots: `## 74.` / `## 75.` / `## 76.`, each "(2026-10-24)": a fixture or
   a stub that silently did not engage; a corpus read on the wrong tree; a merge
   chain that does not stop on its own check. Highest earlier: 73 (2026-10-03).
5. First `gh issue list ... created:2026-10-19..2026-10-25 --limit 400`:
   returned exactly 400, lowest #718 -- truncated; discarded, rerun in 6.
6. `gh issue list --limit 1000` created and closed, 2026-10-19..2026-10-25:
   CREATED total=496, #622 to #1117 (1117-622+1 = 496, contiguous); open=467
   closed=29; label bug=311; title "Bug:"=303; label epic=10; label audit=26;
   title "Backlog:"=68; title "M7"=33; title "M6"=59; "Ops:"=9.
   By creation day: 10-19 0, 10-20 12, 10-21 2, 10-22 8, 10-23 150,
   10-24 223, 10-25 101.
   Created 10-20..10-22: #622-#626 M7.P5 sign-in; #627 C not planned; #628 C;
   #629 bug (ZIP hashing); #630, #632 Backlog; #631; #633 C audit (7 findings,
   0 critical/high); #634 Ops swap 32 GiB; #635 Ops memory admission; #636 Ops;
   #637; #638 C Ops Gemini 4 Argon route; #639 C audit (5 findings, 0
   critical/high); #640 Ops checkout move; #641 C M6.P1; #642 C; #643.
   Epics created (c=): #695 10-23, #700 10-23, #798, #800, #807, #848,
   #903 all 10-24; #1047, #1054, #1082 all 10-25.
   CLOSED total=29: completed=28, not planned=1 (#627); all 29 created in the
   week; label audit=23; bug=0. By close day: 10-20 1, 10-22 4, 10-23 3,
   10-24 12, 10-25 9. Closed, not audit-labelled: #627, #628, #638, #641, #642,
   #646. Closed audits: #633, #639 (M7) and 21 M6 slice audits: #826 T3 (34
   findings), #837 T5 (25), #846 T6 (6), #872 T30 (41), #884 T7 (15), #895 T8
   (17), #900 T24 (3), #912 T4 (25), #924 T9 (21), #958 T10 (44), #984 T12
   (23), #1006 T14 (23), #1046 T45 (15), #1052 T23 (9), #1073 T13 (24), #1074
   T40 (6), #1091 T11, #1096 T27 (14), #1102 T25, #1103 T22 (28), #1108 T28 (9).
   Open audits: #701 T1 (81 findings), #790 T2 (title: 36 findings), #1040 T15
   (24 findings).
7. Slice issues #648-#693: all 46 open ("slice issues open=46"). M6 milestone
   (`gh api .../milestones/6`, read 2026-10-26): open=242 closed=28, updated
   2026-10-26T20:49:53Z. Body: #644 done at `67bcd70dc3`,
   `docs/reviews/build-path-read.md`, "26 findings each with its carrier";
   #645 filed; the P0 merge "waits for the M7 lane's post-candidate merge to
   clear the push guard's W42 gate".
8. `git log --since=2026-10-19T00:00:00Z --until=2026-10-26T00:00:00Z HEAD`:
   296 commits (295 non-merge); by day 10-19 0, 10-20 0, 10-21 0, 10-22 11,
   10-23 31, 10-24 150, 10-25 104. Merge base with `next` `8ebaf8daad`; 393
   commits ahead of `next`. Rule-file commits (8): `49e6691b69`, `e97a5fafe9`,
   `9927413bb2` (generic-x64-vm-testing, #669), `575be34d8c` (rc=$?,
   engineering-practices), `764d30ed2e` (device-builds, #655), `e09b57d16c`
   (tree-claim covers hashes, #654), `ab8f750784` (blindspot 75's guard, #651),
   `8c9b1d4721` (T1's retro, #648). Files: generic-x64-vm-testing.md 4,
   engineering-practices.md 3, device-builds.md 1. New top-level tools on
   this branch in the week: none.
9. Entries read, 10-22 and 10-23: 16:16 (D-WORKFLOW-181, Fable plans, Opus 5.5
   executes); 18:58 (D-WORKFLOW-183); 19:02 (Herdr workspace); 00:45
   (D-WORKFLOW-185/186); 05:40 (46 issues #648-#693 under #339); 06:05 (P1
   accepted, #641 closed); 17:20 (T1: 81 findings, 0 Critical, 2 High -- F-14
   netplay host into `runemu.sh`'s root `eval`, F-67 `updateabl` both slots
   unchecked -- 84 punch items, 60 bug issues #702-#761); 20:25 (T2: 1 High
   SS-1 save-state path into the shell unquoted, 23 bugs #767-#789, audit
   #790); 23:59 (D-WORKFLOW-192, fix-pending-image rows). Headings: 16:30
   (D-WORKFLOW-190, T2 beside T1).
10. Entries read, 10-24 and 10-25: 01:25 (T1 accepted); 01:58 (blindspot 74);
    03:20 (#802, upstream fix 2026-10-04 `c9820d0e89`, not on `next`); 05:02
    (blindspot 75); 06:17 (#825, patch 0012, `system()` as root, upstream
    carries the identical patch); 07:21 (T5 accepted; tmpfs inodes); 10:14
    (D-WORKFLOW-195); 14:51 (#895 closed with 19 open checkboxes;
    `write-completion.py` refused); 23:40 ("Accepted today: T7, T30, T24, T8,
    T4, T9, T10, T14, T12"); 02:25 (session ended about 00:45, resumed
    02:20, 95 minutes; 27 monitors per the friction line; #1017); 03:07
    (#1043, two seal keys, removed at `0fa5a20c5f`); 07:53 (M7 FINAL RETURN
    `bcc866f1`); 11:56 (T29, T16, T17). Heading-only: 04:36 (#802/#806 fix
    packets; build-order race); 06:27 (#825 injection reproduced, hook's half
    proven); 07:00 (D-WORKFLOW-194, five not eight); 08:25 (#1067 fixed
    forward, rclone serve's directory cache; #1057 two guests); 21:36 (W42
    summary, #254).
    Acceptances counted from headings -- 10-24 (14): T2 00:35, T1 01:25, T3
    07:11, T5 07:21, T6 08:58, T7 11:19, T30 12:32, T24 14:25, T8 14:48, T4
    15:47, T9 18:32, T10 19:48, T14 23:34, T12 23:40. 10-25 (9): T45 03:35,
    T23 04:42, T40 06:02, T11 08:08, T27 08:54, T13 09:02, T25 10:21, T22
    10:51, T28 11:25. Total 23 = 21 closed slice audits + #701 + #790.
    T10 (18:01 heading): 44 findings, 29 bugs #929-#957, audit #958.
    T11 (07:44 heading): five bugs #1086-#1090, audit #1091.
11. Retros read: P1 survey (133,520 distribution paths, 1,114 ES paths,
    unassigned 0, 46 slices, 13 Extended, three tools); T1 (84 items from 81
    findings, 61 bug issues #702-#762); T45 (no stage E; #1043, #1044, #1045);
    T12 (time-to-play: interface to first frame 0.603 s record, 0.69 s and
    0.76 s; exit sync 1.33 s record, 1.33 s and 1.32 s, budget 3 s; game to
    game 1.017 s record, 1.01 s and 1.01 s; "The slice changed neither number").
12. This file written with a quoted heredoc; `wc -l` in the same command.

Not read: any M7 lane branch or day file for October 19-21 (none on the
branches listed); `tools/ceremony-check` was not run; the M6 milestone body
past its first 6,000 characters.

13. Added after the trim (figures in the prose, from outputs above): D-WORKFLOW-194
"five, in four recipes"; D-WORKFLOW-196 "becomes six"; D-WORKFLOW-197 "are
seven". Friction 10-23 16:30 "sat idle seven hours"; 10-23 21:15 "sat idle 78
minutes". Heading 10-23 03:19 "Ten decided rows sat under 'Open decisions'".
The 10-24 epic count (five) is #798, #800, #807, #848, #903, each c=10-24 in
command 6's output; #1047, #1054, #1082 each c=10-25. The summary prose was
then trimmed with the Edit tool (no new figures); `wc -l` in a final command.

</details>
