# Week 2026-W42 (October 12–18): Stable foundation, candidate audits and the private H700 handoff

Written October 24 by the M6 coordinator lane from the dated daily logs, the
work-log index and the friction log, as the ceremony asks; the week is the M7
lane's, which corrects anything here it knows better. This summarizes W42 only: six day files (October 12–17, 225
entries), 140 commits on `next`, 65 issues filed and 39 closed. No day file
exists for October 18; #618–#621 were filed that day. Refs #344, #493, #528, #603.

## Delivered during the week

#493 removed all 17 old build trees, recovering about 1.98 TB, and found the
promised pre-build retention enforcement missing from the build entrypoints;
mandatory state-bound build admission landed on October 13 with 27 admission
and 36 routing controls. #557 updated the RG SP and the Nova with the accepted
firmware under named consent. D-INFRA-023 defers hardware choices until the
next build's peaks are measured.

The foundation moved to ROCKNIX stable 20261001 (D-WORKFLOW-161, #563); #564
reproduced upstream's new Steam function deleting the working runtime before
any repair. Owner feedback became #565–#572 the day it was given, including the
browser pressure incident (#570: available RAM fell to 53 MiB with WebKit near
500 MiB before a forced reset) and the GStreamer packaging defect (#572). #566
took the shared JELOS ScreenScraper identity for now (D-WORKFLOW-166; #586).

#570 ran as a bounded investigation, not a cure: a nine-case low-memory VM
matrix, named RG35XX SP bench runs (D-QA-060), and a compiled EmulationStation
trim whose one-guest comparison saved 78.01 MiB of anonymous memory. The lazy
proxy import saved only 390 KiB installed, so it and GTK4 stayed diagnostic
(D-WORKFLOW-163). #570 closed on October 14 with an explicit recurrence watch;
the physical hang remains unexplained.

October 14–15 built and audited the candidate. An engineering image from
`d6a87f05c1` exposed four plugins missing `libgstnet-1.0.so.0` and was rebuilt
narrowly; the #590 audit (two Fable 5.1 calls, frozen score 80 PASS / 16
PARTIAL / 16 SKIP / 3 FAIL) found six findings, all resolved under #596. H700
was accepted at 06:47 UTC on October 15 and SM8550 followed after the upstream
ABL 1.2 checksum fix (#600) and a signed-ABL check (#602). Fifteen closures
crossed the twelve-closure cadence, so #603 audited the completed handoff: 67
criteria across 15 issues, 67 PASS after the #606 RetroArch proof, seven punch
items in #612 with five (#607–#611) left open.

The private handoff under the new rule followed on October 16: the RG35XX SP
received the `077197`/ES `16dbac` image with all 163 protected files preserved and automatic
cloud sync off, under D-WORKFLOW-168, which separates owner-only testing from
public release. The device's browser exit stayed inconclusive (#615) while its
VM controls passed (#614). #587 measured a 26.27 MiB median gain from stopping
the proxy and a 15 s timeout/SIGKILL counterexample during a busy flush, so no
stop policy was adopted (D-RA-048, D-WORKFLOW-169). October 17 compiled WebKit
2.54.1 GTK4/API6 for #576 and loaded the Google Drive and Dropbox sign-in forms
on the VM for #616, with no runtime claim (D-WORKFLOW-170; #617 holds Blink).

## Friction and changes to the process

The friction log took 143 lines, 45 of them on October 15. The recurring shape
was a fixture assuming what the runtime lacked: `hashlib.file_digest` in the
container's Python 3.10 three times in four days, absent PSI or `/proc` task
lists, a BusyBox applet losing its dispatch name. Each kept the original
failure, corrected only the fixture and reran under a fresh owner. Commits
without an issue citation were refused before publication on four of the six
days; the recorded lesson is to run the coverage check against the integrated
`next` history, not before the commit exists.

Sixteen register rows were written. Beyond those cited above, D-UI-126/127
record intended phone-status and Wi-Fi-picker behaviour, D-WORKFLOW-162 makes
an early upstream check standing practice (#573), D-WORKFLOW-164/165 keep the
contribution queue #585 with submissions held until the initial build,
D-WORKFLOW-167 puts release credits on the website (#605), and D-RA-047 files
the proxy-stop experiment as conditional future work. No blindspot entry was
added. One mini-retro closed the audit-to-device-builds phase on October 15 and
asked for no new rule; no futro was run.

Thirteen commits touched seven rule files: `engineering-practices.md` gained
the upstream-check and contribution sections; `device-builds.md` took build
admission (#493), the interim scraper identity (#566) and the producer-owned
results rule (#597); `release-candidates.md` carries D-WORKFLOW-168;
`worktrees.md` the cleanup parent-permission preflight (`81941a48b2`) and the
admission note; the VM-testing rule the BusyBox applet-path lesson and the
bind-mount identity lesson (#570); fork-workflow and instruction-files registered the
two `pixelelated-state-check` tools (#565).

## Position at the end of October 18

The accepted private image was on the RG35XX SP with its preservation verified;
#613 and #607–#610 preceded any next candidate or Nova qualification. Browser
work stood on three open spikes, #576, #616 and #617, with GTK4 compiled but
unrun. #528's source, notice and custody obligations and #605's website credits
remained the public release gates; no RC number or public artifact was
allocated. Of the 65 issues filed this week, 27 were still open on October 24.

Sources: [October 12](2026_10_12-work_log.md),
[October 13](2026_10_13-work_log.md), [October 14](2026_10_14-work_log.md),
[October 15](2026_10_15-work_log.md), [October 16](2026_10_16-work_log.md),
[October 17](2026_10_17-work_log.md); `docs/friction-log.md`;
`docs/retros/2026-10-15-m7-audit-to-device-builds.md`;
`docs/audits/2026_10_14-milestone-m7-next-candidate/` and
`docs/audits/2026_10_15-milestone-603-completed-handoff/`.
