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

The first later batch is the two standalone QA files under D-INFRA-019. No worktree registration was removed. Its six input seals, four zero results, observed9.98GiB recovery,53 unchanged evidence hashes and15 protected identities are retained. The general report planner and rejection controls remain open.
