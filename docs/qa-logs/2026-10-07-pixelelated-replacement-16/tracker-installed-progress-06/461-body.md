## Maintainer request

> Got it. That's fine because we're about to do more builds, but we should come up with a way we're going to eventually clean after a successful build is generated. We don't want to keep it this full all the time if we may need the space. We can proceed with what we need to get this release candidate ready.

## Current state and scope

#453 inventoried the build volume; #456 preserved required inputs; #459 removed five explicitly approved superseded build trees, recovering 539.34 GiB and leaving 576.45 GiB available at the final measurement. #460 corrected the standard worktree removal helper. This one-time cleanup is complete. There is no recurring post-qualification retention report or automatic cleanup policy yet.

Add a durable retention review after a build has an immutable image/update bundle and its required QA results. A successful compiler exit alone does not release predecessors. Keep the current candidate and useful rebuild tree, a qualified fallback per device/architecture, the ROCKNIX upgrade baseline, exact source/licence inputs and shared source cache, retained failure evidence, and all transitive dependencies (including qcow2 backing files and objects referenced from another preservation store). Retain compact evidence instead of entire superseded trees when independent copies are verified.

Before the next build, compare live available space with the intended build/copy/QA footprint and a measured margin; do not count filesystem reserve as available build capacity. The report should list protected objects, proposed removals, expected net recovery after preservation, and remaining headroom. Cleanup follows the existing guarded removal and watcher protocol, with a concrete reviewed scope and verified results. This request does not extend the completed five-tree deletion approval.

This is infrastructure follow-up, outside M7's RC acceptance gates. Adopt the rule now; implement/report the next cleanup batch after successful qualification or when measured capacity requires it. M7 keeps its existing P3 → P4 → H700 order.

Can this be done on the VM? No: build-volume allocation, host process references, container mounts and host worktree ownership are host facts. Test any new planner using isolated temporary fixtures; inspect production state read-only before proposing deletion.

## Acceptance criteria

- [x] Canonical worktree/build instructions describe the qualification trigger, protected set and capacity review; a decision row and M7 link make the follow-up findable.
- [ ] A repeatable read-only retention report binds proposed removals and retained dependencies to exact paths/identities and states whether the next scheduled build fits.
- [ ] Planner controls reject active, unreadable, unclassified or referenced candidates, including qcow2 backing chains and cross-store objects; logs retain each rejection.
- [x] The first later authorized batch records preservation checks, watcher completion, actual path/registration removal, measured recovery and unchanged protected inputs. Until then, no automatic deletion is claimed.

## Policy delivery

Published on next `202a40cf9d4fb0115fca7e08a8619e2256475d43`: [canonical rule](https://github.com/pixelelated/distribution/tree/202a40cf9d4fb0115fca7e08a8619e2256475d43/.claude/rules/worktrees.md), D-INFRA-018 and [M7 priority link](https://github.com/pixelelated/distribution/milestone/7). The report tool and next concrete cleanup batch remain open; automatic deletion is not implemented.

## Current execution — 2026-10-07 01:12 UTC

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

Legacy-root/reasons640 PASSED all10 English/French cases and44 directly reviewed
frames. Actual selection shows supported Game Boy content. Future/malformed
layout, unreadable settings and record refusals preserve cloud/pointers and
show complete, distinct reasons. The previously clipped French settings reason
now fits completely. Primary01:12:01 verified allfour0/9seals and actual guest/
backend/port cleanup; evidence isQ16/root-reasons-640x480-acceptance.

The matching1280x800 proof is active with virgl:
`/workspace/tmp/pixelelated-m7-p4-build16-root-reasons-1280x800-01`, launcher361138,
watcher361140, run`20261007T011212Z-1322e2dc`. Both-resolution recovery,
full clean/actual RC2-upgrade QA20 and local protocols follow serially.
#482/#486 are CLOSED completed with published evidence and exact body/state
readbacks in Q16/interruption-issue-resolution. #478/#479 and four original
audit findings await their complete remaining acceptance.

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

The first later batch is the two standalone QA files under D-INFRA-019. No worktree registration was removed. Its six input seals, four zero results, observed9.98GiB recovery,53 unchanged evidence hashes and15 protected identities are retained. The general report planner and rejection controls remain open.
