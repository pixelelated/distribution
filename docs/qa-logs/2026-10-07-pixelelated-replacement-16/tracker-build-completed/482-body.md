Maintainer request:

> What's with the copy on that interrupt screen? It doesn't feel very aligned with our copywriting standards. Can you take a look at what's there against what we use and make sure it aligns with voice and tone?

Current installed candidate15 interruption says COULDN’T FINISH, SETTINGS BACKUPS - YOUR CLOUD STOPPED ANSWERING, and WHAT MOVED IS IN THE NEW FOLDER. TRY AGAIN TO FINISH. The reopened prompt says YOUR CLOUD FOLDER MOVE DIDN’T FINISH / TRY AGAIN? FILES ALREADY MOVED WILL BE KEPT. Exact failed05 frames and source are retained.

Against D-UI-045 (clear, brief, sized), D-UI-031 (everyday speech), D-UI-028/030 (canonical outcome) and D-UI-051 (English/French): keep the outcome and precise reason; replace the vague helper line with a direct next action, and put the retry question after its consequence. No global outcome-vocabulary change and no implication that a truncated copy completed.

Published English:
- Interruption guidance: TRY AGAIN TO MOVE THE REMAINING FILES.
- Reopened prompt: COULDN'T FINISH MOVING YOUR CLOUD FOLDER. / FILES ALREADY MOVED WILL BE KEPT. TRY AGAIN?

The published French follows the same meaning and established accented-capitals/typographic-apostrophe style; exact strings and source checks are retained in the interruption-copy review evidence.

Can this be done on the VM? Yes: owned WebDAV interruption/retry and English/French640x480/1280x800 frames on rebuilt16. No physical device or personal provider needed.

Acceptance criteria:
- [x] Record the exact old/new English/French text, canonical-rule comparison and source call sites; distinguish an interrupted transfer from a completed copy.
- [x] Actual image-compiler syntax, vocabulary and msgfmt checks pass for the changed source; pin the full integrated ES commit.
- [ ] Rebuilt candidate16 displays the complete interruption/retry text in English/French at640x480 and1280x800, with directly reviewed frames and unchanged recovery actions. The actual interrupted-file retry preserves original bytes and completes.

Refs #471, #468, #479; this owner-requested copy refinement joins P4 before the next build. Original audit baseline remains unchanged.

## Current execution — 2026-10-07 00:29 UTC

Both approved Fable audit calls and grading are complete. Phase 7 remains open:
PL-002/006/007/008 are resolved; PL-001/003/004/005 await candidate 16 installed
acceptance in #471. The interruption-copy refinement #482 is included at ES
`72494bc72e3d64d4dcfeb4e6478052bbdf166c5b`.

Candidate 16 built successfully: 642/642 tasks, all four result channels zero,
source/input seals verified, and its container and worker processes exited.
Distribution: `ee014909137e03706e0b3020b8396be589aaa705`.
Immutable bundle: `7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a`.
Disk-image and update SYSTEM payloads are byte-identical:
`5767ee7d72f3c538259ee927ad681c63533d661997b64e6beac9d83fdc70812c`.
Primary verification completed at 00:25:38 (build), 00:26:39 (store), and
00:28:45 (image extraction). These checks do not establish VM acceptance.

The 85-case installed matrix started at 00:28:54 under
`/workspace/tmp/pixelelated-m7-p4-build16-installed-matrix-01`, launcher 57723,
watcher 57725, run `20261007T002854Z-d1d7980f`. Two isolated QA guests are running.
The primary actively consumes the watcher result; disconnected alerts remain #395.

The exact approved two-disk retirement is complete: 10,713,485,312 bytes recovered,
all other evidence and protected sources preserved. No broader cleanup or reserve
change was made or is authorized. The fixed swap helper passed before the build.

**Next:** installed matrix → historical shelf and actual interrupted-file UI retry /
next-backup preservation → English/French recovery/reason/interruption frames at
640×480 and 1280×800 → full clean/actual RC2-upgrade QA20 and final artifact scans →
#471/P4 closure → #461 device capacity review → H700 DDR4 RG35XX SP arm, then
aarch64 → named physical/P5 gates. #478/#479/#482 remain open until acceptance.
No new RA reset or Dropbox credential is needed. Ten #168 upstream drafts remain
unsubmitted. No release-candidate designation or device-readiness claim yet.

Evidence: `docs/qa-logs/2026-10-07-pixelelated-replacement-16/`; source and earlier
results: `docs/audits/2026_10_06-milestone-m7-p4-fixes-383/`.
