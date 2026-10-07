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
- [x] Rebuilt candidate16 displays the complete interruption/retry text in English/French at640x480 and1280x800, with directly reviewed frames and unchanged recovery actions. The actual interrupted-file retry preserves original bytes and completes.

Refs #471, #468, #479; this owner-requested copy refinement joins P4 before the next build. Original audit baseline remains unchanged.

## Current execution — 2026-10-07 00:59 UTC

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

The installed matrix retained 84 PASS / 1 FAIL. The failed T23 observer expected
partial writes after a collision; fresh collision01 now passes two write-free
refusals and rejects the actual candidate15 script with the same unchanged-state
predicate. Primary00:39:10 verified all four results zero, 212 seals and guest/
backend/port cleanup. Coverage is 84 original cases plus the requalified T23;
the original failed run has not been relabeled.

All three historical discarded-save recovery cases passed: actual RC2-complete,
record-copy and record-delete states restore all four owned tiers, remove the
record and remain unchanged on repeated apply. Primary00:41:06 verified all four
results zero, 211 seals and actual guest/backend cleanup.

Actual interrupted-file retry is COMPLETE in English/French at640x480 and
1280x800. Each of the four real copies was killed at258,048 of8,391,392bytes;
original files/pointers and the recovery record survived. Actual UI retry moved
all4 originals; the next backup preserved the displaced save in current
Saves-replaced. Empty old-parent state and restart cloud hashes stayed unchanged.
All32 frames were directly reviewed: complete revised reasons, prompts and
controls fit both panels. Primary verification:640 at00:53:05 and1280 at00:58:48,
allfour0/10seals and actual guest/backend/port cleanup for each owner.
Failed640-01 remains a separate failed fixture run under#486.

The English/French640 legacy-root and truthful-reason proof is active:
`/workspace/tmp/pixelelated-m7-p4-build16-root-reasons-640x480-01`, launcher291441,
watcher291443, run `20261007T005857Z-46bc93fa`. Next are1280 root/reasons,
both-resolution recovery, full clean/actual RC2-upgrade QA20 and local protocols.
#482/#486 installed acceptance is published at 63ef4e0590a835e72e52a2ac0999ca497f6cf1aa.
#478/#479 and four original audit findings await their complete final criteria.

Whole-image scan15 passed: 57,295 files, 8,606 classified branding contexts, zero
FIX/UNKNOWN or unclassified credential matches, and exact French/XML checks.
Inventory12 mapped 583 components; its 14 known P5 metadata gaps remain open.
The primary actively consumes watcher results; disconnected alerts remain #395.

The exact approved two-disk retirement is complete: 10,713,485,312 bytes recovered,
all other evidence and protected sources preserved. No broader cleanup or reserve
change was made or is authorized. The fixed swap helper passed before the build.

**Next:** English/French legacy-root/reason/recovery frames at
640×480 and 1280×800 → full clean/actual RC2-upgrade QA20 and the standing WebDAV/SFTP/S3 baseline →
#471/P4 closure → #461 device capacity review → H700 DDR4 RG35XX SP arm, then
aarch64 → named physical/P5 gates. #478/#479/#482 remain open until acceptance.
No new RA reset or Dropbox credential is needed. Ten #168 upstream drafts remain
unsubmitted. No release-candidate designation or device-readiness claim yet.

Evidence: `docs/qa-logs/2026-10-07-pixelelated-replacement-16/`; source and earlier
results: `docs/audits/2026_10_06-milestone-m7-p4-fixes-383/`.

## Verified acceptance — 2026-10-07 01:02 UTC

Candidate16 distribution `ee014909137e03706e0b3020b8396be589aaa705`, ES `72494bc72e3d64d4dcfeb4e6478052bbdf166c5b`. Published evidence commit `63ef4e0590a835e72e52a2ac0999ca497f6cf1aa` has exact file/readback verification.

[640x480 acceptance](https://github.com/pixelelated/distribution/tree/63ef4e0590a835e72e52a2ac0999ca497f6cf1aa/docs/qa-logs/2026-10-07-pixelelated-replacement-16/partial640-02-acceptance/) and [1280x800 acceptance](https://github.com/pixelelated/distribution/tree/63ef4e0590a835e72e52a2ac0999ca497f6cf1aa/docs/qa-logs/2026-10-07-pixelelated-replacement-16/partial1280-02-acceptance/) cover all four English/French scenarios and32 directly reviewed screens. Each real copy was interrupted at258,048 of8,391,392bytes; original bytes/pointers and the recovery record survived; the actual UI retry completed all four files. The next conflicting backup preserved displaced save bytes under the current Saves-replaced path. Exact old-parent state stayed unchanged, and restarting ES changed no cloud bytes.

Independent completion verification recorded all four result channels0,10 input seals and actual guest/backend/port cleanup for each owner (64000:53:05;128000:58:48). The complete guidance, retry consequence/question and actions fit both panels in both languages.

This closes only the stated issue criteria. Four original audit findings, root/recovery UI and final clean/upgrade/protocol qualification remain separate M7/P4 gates.
