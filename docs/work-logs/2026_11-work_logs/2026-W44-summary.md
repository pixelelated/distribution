# Week 2026-W44 (October 26 – November 1): Sixteen slices, the host shared by ledger, and four stops

Routing copy added 2026-11-04 for the ceremony path keyed to the week-ending month.
The [original November 2 summary](../2026_10-work_logs/2026-W44-summary.md) remains
unchanged (SHA256 f0af2995d7036bdc1b6ad7c7185d485b708690680d0e1eaa05fe317573ab1e6a). Its dated findings
and limits are retained below; only relative links are adjusted for this directory.
No historical ceremony, source review or test was replayed.

Written November 2 by the M6 coordinator lane from the dated daily logs, the
work-log index, the friction log and the decision register, as the ceremony
asks. The week is mostly M6's; the M7 lane appears through the tracker and the
shared host ledger, and corrects anything here it knows better. Six day files
exist on this branch (October 26, 27, 29, 30, 31 and November 1; none for
October 28, the day of the host reboot), 155 entries in all; 272 commits on
the coordinator branch and none on `next`; 282 issues filed (#1118–#1399, 214
of them labelled `bug`) and 18 closed. Refs #346, #339.

## Delivered during the week

**Sixteen slices were accepted.** October 26 took five: T29 (#676, the
devices-adjacent OS quirks), T17 (#664, the cloud setup scripts, with
D-CLOUD-185's rclone option allowlist), T18 (#665, the cloud pages in
EmulationStation, the first ES slice since T2), T19 (#666, the offline
achievements proxy, D-RA-049 to 051 and D-WORKFLOW-210/211) and T20 (#667,
D-RA-052). T20's research found #1154: EmulationStation's HTTP client never
verifies the TLS peer; the owner's direction and M7's proof windows followed
on October 30. October 27 took four, each dispatched, run, accepted and
closed out inside the day: T21 (#668; D-WORKFLOW-212, D-NET-017,
D-CLOUD-186), T26 (#673), T31 (#678; D-UI-128/129) and T32 (#679). October 30
took T15 (#662) and T33 (#680; D-CLOUD-187); October 31 T34 (#681; D-UI-130
to 133, 25 bugs, one held High) and T16 (#663, the cloud harness; D-CLOUD-188
to 191 and 193); November 1 T35 (#682; D-WORKFLOW-214), T36 (#683;
D-WORKFLOW-216) and T37 (#684). The October summary counts 36 of the 46
slices accepted or complete by October 31; with T35, T36 and T37, 39 by the
week's end. T38 (#685) was in its acceptance runs, T39 (#686) dispatched at
06:22 on November 1 (D-WORKFLOW-220) and T41 (#688) briefed at version 1.

**The acceptance recipe settled into tools.** Every slice from T16 on was
accepted by a per-slice script derived from one shared script
(`kit/t36-accept.sh`) with an exact-substitution derivation that refuses when
the shared text moves, and ticked by a tick script that reads the live issue
body, PATCHes it and reads it back. Each audit issue closes from its folder's
Phase 7 gate. The derivations refused twice on November 1 when the shared
script moved under them (T37's and T38's); widening the derivation and
re-deriving was the rule both times, never an edit of the derived script.

**The host became a ledger.** After the reboot of October 28 removed
`/tmp`, the shared coordination file moved to
`/workspace/tmp/m7-m6-host-coordination.txt` (October 29). M7 writes
timestamped START and RETURN lines; the coordinator grants each window with
its CPUs, memory, bound and start-by, re-reading the file in the same command.
`kit/compile-ack.sh` acknowledges M7's lines within seconds; on November 1 it
missed three new M7 wordings in turn (`M7 root RETURN`, `M7 root: standing
functional RETURN`, `M7 SM8550 packaged readback START/END`) and was rebuilt on
one shared classifier, `kit/m7-kind.awk`, tested against every ledger line.
M7's GENERIC, H700 and SM8550 engineering builds ran under those grants on
November 1 (H700 and SM8550 images built and read back; GENERIC qualified
clean and retained by 19:29).

**Rules and records.** Seventeen commits touched the rules: six to
`engineering-practices.md` (the `rc=$?` line, the total from the tool, the
hash copied by command, the pidfile), three each to `es-code-traps.md` and
`device-builds.md`, two each to `es-native-ui.md` and `es-player-text.md`, one
each to `learning-capture.md`, `worktrees.md` and the per-device patches
sentence in `CLAUDE.md`, `AGENTS.md` and `packaging-and-patches.md` (T37's
L-18). The October monthly summary was written on November 1.

## Friction and changes to the process

**Four stops cost the coordinator most of a day.** A monthly limit from
October 27 about 20:35 to the resume on October 29 at 18:00, with the host
reboot between (00:37 on October 28) emptying the session scratchpad -- every
dispatch kit, research file and mirror template of the week went with it, and
the kit now lives under `/workspace/tmp/m6-coordinator/kit/` (Backlog #1386
gives it a tree home). Then three five-hour cuts on October 30 and 31, and a
credit stop on November 1 about 07:01 that moved the session to another model
and, the next day, another harness. Each resume was recovered from files
alone; the cost was the waiting lanes.

**The friction log took 15 lines.** The shapes: a watch that said nothing --
the guest-window mirror matched one post shape (October 26), two tail pipelines
on the acceptance runs delivered no event (November 1), and the acknowledger
missed new M7 wordings twice; a lane left idle -- T21 18 minutes on a question
asked only on its screen, T26 28 minutes after a turn ended on "next is S7";
a fill that went out wrong -- T31's dispatch entry pushed with placeholders
unfilled, T39's kit with a delimiter-alternating paste and an unquoted value;
a census that missed a credential form -- the mask covered `user=` and `pass=`
but not `--user X --pass Y` (October 30; the mask now covers both); an
acceptance re-run that compiled 50 s inside another lane's guest window
(October 31); and a close-out that checked the distribution tip and not that
T36's EmulationStation tip was on the remote (November 1; it was not, and the
force-push it needs is the owner's).

**Thirty-five decided rows were written**: D-CLOUD-185 to 193, D-RA-049 to
052, D-NET-017, D-UI-128 to 137 and D-WORKFLOW-210 to 220. The last four are
T37's ownership row D-WORKFLOW-217, T38's ownership row D-WORKFLOW-218, T38's
pause dispositions in D-WORKFLOW-219 (`begin-exploration` swept, not written),
and T39's ownership row D-WORKFLOW-220.

**Ceremonies.** The coordinator's mini-retro of October 26 (three silent
watches, three claims from memory, the brief practice written down) and its
phase retro of November 1 (the acceptance-script discipline, the host
protocol, the kit's home; Backlogs #1386 and #1387); the offline-achievements
futro of October 26; a futro or addendum for every slice dispatched; a retro
for every slice accepted. `tools/ceremony-check --gate` returned 0 at each
commit.

## Position at the end of November 1

Thirty-nine of the 46 slices accepted or complete; T38 (#685) at its last
acceptance FAIL, T39 (#686) at its stage-B checkpoint, T41 (#688) briefed and
under proof. Nothing had merged to `next`, still at `8ebaf8daad` from
October 17; every slice issue stays open until its branch reaches it. 912
issues open on the fork, 530 of them labelled `bug`. Waiting on the owner:
T36's EmulationStation force-push, the two pause decisions on #346,
`council-research` kept or retired (#807), and the merge subjects of T36's
two merges.

Sources: [October 26](../2026_10-work_logs/2026_10_26-work_log.md), [October 27](../2026_10-work_logs/2026_10_27-work_log.md),
[October 29](../2026_10-work_logs/2026_10_29-work_log.md), [October 30](../2026_10-work_logs/2026_10_30-work_log.md),
[October 31](../2026_10-work_logs/2026_10_31-work_log.md), [November 1](2026_11_01-work_log.md);
`docs/friction-log.md`; `docs/decision-register.md`; `docs/retros/` and
`docs/futros/`; the October summary [SUMMARY.md](../2026_10-work_logs/SUMMARY.md); the host ledger.

<details><summary>Evidence</summary>

All commands run on 2026-11-02 between 05:28 and 05:30 UTC from the worktree
on `feature/m6-renovation-plan-346`.

1. Day files and entries (`/usr/bin/grep -c '^## '`): 2026_10_26 60 entries,
   1,604 lines; 2026_10_27 22, 319; 2026_10_28 MISSING; 2026_10_29 1, 7;
   2026_10_30 10, 72; 2026_10_31 24, 148; 2026_11_01 38, 213.
2. `git log --since=2026-10-26T00:00:00Z --until=2026-11-02T00:00:00Z --oneline | wc -l`:
   272 on this branch; 0 on `next`.
3. `gh api -X GET search/issues -f q='repo:pixelelated/distribution is:issue created:2026-10-26..2026-11-01'`:
   `total_count` 282, first #1118, last #1399; with `label:bug` 214;
   `closed:2026-10-26..2026-11-01` 18. Open now: 912; open with `label:bug`: 530.
4. Decided rows dated in the week (`grep -E '^\| D-[A-Z]+-[0-9]+ \| 2026-1(0-2[6-9]|0-3[01]|1-01) '`):
   D-CLOUD-185 to 193, D-RA-049 to 052, D-NET-017, D-UI-128 to 137,
   D-WORKFLOW-210 to 220 -- 35 IDs.
5. Friction lines dated in the week (`grep -c -E '^- 2026-1(0-2[6-9]|0-3[01]|1-01)'`): 15.
6. Acceptances from the day files' headings
   (`grep -o -E '(T[0-9]+ \(#[0-9]+\)|#[0-9]+: T[0-9]+|T[0-9]+) (accepted|complete)'`):
   10-26 T29, T17, T18, T19, T20; 10-27 T21, T26 (T31's and T32's headings
   read "stage E, hand-back and acceptance"); 10-30 T15, T33; 10-31 T34 (T16's
   acceptance at `ce3242e14f` is in the 10:56 entry's body, as the October
   summary notes); 11-01 T35, T36, T37. The October summary's line 88: "36 of
   46 accepted or complete by October 31".
7. Rule commits in the week (`git log ... -- .claude/rules CLAUDE.md AGENTS.md`): 17;
   files by count: engineering-practices.md 6, es-code-traps.md 3,
   device-builds.md 3, es-player-text.md 2, es-native-ui.md 2, CLAUDE.md 1,
   AGENTS.md 1, worktrees.md 1, packaging-and-patches.md 1, learning-capture.md 1.
8. Retros and futros dated in the week (`ls docs/retros docs/futros`):
   2026-10-26-m6-coordinator.md, 2026-11-01-m6-coordinator.md,
   2026-10-26-m6-offline-achievements.md.

Not read: the M7 lane's branches and day files; the lane branches' own
retros and futros (each is cited from the coordinator's day entries);
`docs/blindspot-register.md`.

</details>
