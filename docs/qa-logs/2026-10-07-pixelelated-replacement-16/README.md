# Candidate16 — M7.P4 verification build

## Current execution — 2026-10-07 00:41 UTC

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

The real partial-copy/UI retry test is active in English/French at 640×480:
`/workspace/tmp/pixelelated-m7-p4-build16-partial-retry-640x480-01`, launcher128765,
watcher128767, run `20261007T004110Z-e8f0e007`. Direct frame review is still required.

Whole-image scan15 passed: 57,295 files, 8,606 classified branding contexts, zero
FIX/UNKNOWN or unclassified credential matches, and exact French/XML checks.
Inventory12 mapped 583 components; its 14 known P5 metadata gaps remain open.
The primary actively consumes watcher results; disconnected alerts remain #395.

The exact approved two-disk retirement is complete: 10,713,485,312 bytes recovered,
all other evidence and protected sources preserved. No broader cleanup or reserve
change was made or is authorized. The fixed swap helper passed before the build.

**Next:** actual interrupted-file UI retry /
next-backup preservation → English/French recovery/reason/interruption frames at
640×480 and 1280×800 → full clean/actual RC2-upgrade QA20 and the standing WebDAV/SFTP/S3 baseline →
#471/P4 closure → #461 device capacity review → H700 DDR4 RG35XX SP arm, then
aarch64 → named physical/P5 gates. #478/#479/#482 remain open until acceptance.
No new RA reset or Dropbox credential is needed. Ten #168 upstream drafts remain
unsubmitted. No release-candidate designation or device-readiness claim yet.

Evidence: `docs/qa-logs/2026-10-07-pixelelated-replacement-16/`; source and earlier
results: `docs/audits/2026_10_06-milestone-m7-p4-fixes-383/`.

The raw input inventory stays at the runtime path named by`freeze/manifest-custody.json`; its exact hash is recorded. `publication-failed-01` retains the normal guard failure before the duplicate was removed (#483).
