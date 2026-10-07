# Saved Session State

## Start here

Continue pixelelated M7 /0.0.1 from actual running jobs below. Read AGENTS.md and
canonical rules from next. Candidate16 qualification and the full P4 fixes audit
are complete; both approved Fable transfers have been accepted. Never replay
completed audits/VM tests or re-ask generic build/cleanup permission. One primary
orchestrator, no new agents/goals/external audit/Daybreak. Keep long work moving
through documentation checkpoints; actively consume completion and failure.

Standing authority: fixes, isolated host/VM checks, fork tracker/commits/pushes,
classified immediate cleanup, H700 then SM8550 builds. No physical-device or
personal-cloud action, upstream PR, release publication, RAID conversion,
purchase or reserve change. D-INFRA-022 makes large test artifacts temporary:
only named active/immediately queued tests justify a hold; preserve compact
records and required source/licence material. Requested policy edit is already
published; no unrelated instruction edit is needed.

## Running now — 2026-10-07T07:29:42.801417+00:00

**H700 aarch64 firmware is BUILDING.** Frozen tree:
/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01,
branch build/m7-pixelelated-h700-01,
head43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa. Never sync/edit it during the job.
The only later source delta versus qualified16 is the recorded GCC12/SPIRV host
repair and seven generated ARM-path fixes; pins and target flags stay unchanged.

- Build owner /workspace/tmp/pixelelated-m7-h700-firmware-01.
- Run /workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01/.build-runs/20261007T063836Z-bd9973f1.
- Launcher4135030, runner4135031, watcher4135032, command4135063.
- Actual container5827382dc092ec65758bcfef2ebb0738fcfde21aeb5371093da21526a86e0dc5.
- Pinned image ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39.
- Source/cache/container mounts are verified in runtime-start.json. Global24,
  WebKit4; ARCH=aarch64, CUSTOM_VERSION=0.0.1, no DEVICE_ROOT override.
- Read build.status, actual process/container state and fresh thread logs for
  progress. Do not infer a stall solely from an unchanged top-level task count.
- Do not edit an in-flight script or reclaim swap while jobs are running.

**Automatic follow-up is also RUNNING**, waiting for actual build completion:
/workspace/tmp/pixelelated-m7-h700-firmware-acceptance-01, launcher818530.
Its run.path names the coordination worktree watcher. It consumes the build
owner result (creates owner-verification.json only if missing), checks actual
container exit, then invokes its sealed verify-firmware.py. This copies the
three firmware artifacts/checksums into the existing immutable candidate store,
checks independent inodes, installed identity/AArch64 binaries, ARM32 handoff
and lib32 hashes, both raw-image SYSTEM/kernel values versus the update tar,
and the exact DDR3/DDR4 bootloader bytes. Newly created scratch disks/SYSTEM
are removed after success. It is not physical boot acceptance or an RC claim.

If compilation fails, the follow-up records BUILD_FAILED and exits nonzero;
read the package log, preserve the failed owner, diagnose and repair source in
coordination, then recover only interrupted scopes before a fresh owner. Do
not silently replay or reset a failed job. If artifact acceptance fails, keep
its failed proof and fix the specific verification/product issue before any
next-device start. Neither build completion nor follow-up acceptance has yet
been claimed. The primary must still verify the follow-up's terminal channels,
input seals and actual exits with /tmp/pixelelated-verify-owner.py exactly once.
Read existing owner-verification.json rather than rerunning exclusive writes.

### Next in order

1. Supervise H700 build/follow-up; report stalls/failures/completion promptly.
2. Accept actual firmware/source/ARM-handoff proof; #497 remains open until it.
3. Remeasure capacity and prepare a separate frozen SM8550 tree from qualified
   product inputs; build/verify it as already authorized. No SM8550 compiler or
   tree has been started at this checkpoint; the gated controller below can
   start them after H700 acceptance. Inspect its actual state before acting. Do not wait for physical H700 testing to
   begin SM8550 compilation. Stage budget347,688,935,424bytes (323.81GiB).
4. Device/P5 gates remain: named physical adoption/smoke actions, corresponding
   source,14 known source/licence metadata gaps, public docs and manifest-bound
   release assets. No physical action or publication is implicit.

## Cleanup is DONE — do not replay

The user supplied the root readback and explicitly said to proceed. Exact owner
/workspace/tmp/pixelelated-m7-broad-cleanup-01 completed06:37:29; four0/eight seals
and actual exits verified06:38:00. All850 QA/firmware files,30 extraction paths
and four build trees09/10/12/14 are gone (884targets). Standard fork-worktree
helper used, all four unregistered. Measured recovery2,117,325,385,728bytes,
final available2,290,757,619,712bytes. Independent records51,070, source custody
objects14,489 and five temporary firmware holds rehashed. There are415 retirement
markers beside surviving records. #494 is closed, #493 remains for other old
stores and repeatable end-of-test retention. Enough headroom exists for both
recorded device-stage budgets; no additional drive is needed for them.

**Important historical limitation, #498:** administrator roots covered child
directories but omitted14 loose firmware files directly in rocknix-images.
They were explicitly authorized and passed hashes, unprivileged process,
container and external-reference checks, but NOT root-only reference coverage.
This was discovered after removal while writing markers. The original sealed
execution and acceptance remain intact; administrator-scope-gap.json records
the limitation. Do not retroactively say all targets had full root coverage.
The repository executor now checks every target is covered by administrator
roots; eight isolated controls pass. Its correction is a different script hash
from the executed owner. No further deletion is inferred. The initial marker
attempt failed before writes; the corrected markers use loose files' parent.
#498 is closed: the correction and limitation are published to next with both
exact-head checks passing. No additional payload was removed.

The actual root receipt is at
/workspace/tmp/pixelelated-m7-broad-root-readback-01/root-process-readback.json:
UID0,06:11:34,235userspace processes,zero unreadable,only four coordination-cwd
matches. The later ordinary-user live check used current visible references and
start times; all193 protected processes predated the snapshot. Protected fields
were NOT freshly reread. The attempted sudo-n refresh required authentication.
Do not ask the user to repeat this consumed check. Further cleanup needs a new
exact scope and appropriate fresh checks, not reuse of consumed authority.

Required source store /workspace/artifacts/pixelelated-build-custody/issue-494-device-capacity-01
and the referenced earlier#456 content store remain. QA16/17 source links to
replacement12 are historical commit/path records; some now dangle intentionally.
Keep the rclone source archive under
/workspace/tmp/rasteratops-m7-qa-01/recovered-inputs/ and current release inputs.
Five known-booted H700/SM8550 firmware holds are for the immediately queued
adoption/smoke recovery steps, released when each device's tests finish. No
completed VM disk has a hypothetical-future-test hold. Older immutable bundles
and other historical roots still require separate classification under#493;
this is unfinished scope, not a permanent generic fallback exemption.

The new executor/controls and compact completion receipts are in
 docs/qa-logs/2026-10-07-storage-retention/.
Current device startup/follow-up scripts and receipts are in
 docs/qa-logs/2026-10-07-device-builds/h700-firmware01*.
The full exact plan/retirement journal remain private under the accepted owners,
with hashes in committed summaries. Do not rewrite historical receipts.

## Accepted prerequisites and unchanged software qualification

H700 arm05 completed244/244, independently hashed7,866 files, checked797links,
938ARM ELF objects and244stamps. Manifest
116314730b3ce22407219f14c1646694ebabc2723a2c24c8ca9e553ff5783e18.
Failed owners and repairs#495/#496/#497 are retained. Before firmware, the fixed
swap helper restored full8GiB swap and preflight passed; no live-run swap recycle.

Qualified VM candidate16: distributionee014909137e03706e0b3020b8396be589aaa705;
ES72494bc72e3d64d4dcfeb4e6478052bbdf166c5b;
immutable /workspace/artifacts/pixelelated-candidates/sha256/7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a.
SYSTEM5767ee7d72f3c538259ee927ad681c63533d661997b64e6beac9d83fdc70812c.
QA20 passed15default suites,78screens,26RC2 upgrade checks; cloud02 passed318
checks across actual local WebDAV/SFTP/MinIO,zero failures/skips. Eight audit
findings resolved and both Fable passes accepted; no new audit call. RA33
Tobu15738/achievement100359 award/flush and125-game proof complete; no reset or
Dropbox check owed. Later work#432 FOSS observability,#464 RA automation,#395
disconnected alerts. A watcher records locally; it is not an off-session alert.

## Continuous device handoff — #492

Prepared owner /workspace/tmp/pixelelated-m7-sm8550-sequence-01. Publication
precedes launch; inspect controller-start.json/state.json/controller-result.json
and actual PID before assuming it is running. Never launch a duplicate. The
source and controls are in docs/qa-logs/2026-10-07-device-builds/sm8550-preparation01/.
Controller semantics: a standard watched waiter consumes H700 artifact acceptance
and verifies actual process exits; only then does prepare.py create a fresh
build/m7-pixelelated-sm8550-01 checkout from published next, with product bytes
equal to H700, full input hashes and enough measured capacity. Guarded swap
preflight runs while watched stages are stopped. It submits the canonical
SM8550 Docker build (ARM compatibility, then aarch64), captures actual container
and mounts, and submits independent artifact acceptance. #492/M7 get live
readback updates. The controller heartbeat is local; no off-session chat alert.

Stage paths:
- /workspace/tmp/pixelelated-m7-sm8550-wait-h700-01 (prepared)
- /workspace/repos/rocknix.worktrees/m7-pixelelated-sm8550-01 (not created yet)
- /workspace/tmp/pixelelated-m7-sm8550-build-01 (created after H700 acceptance)
- /workspace/tmp/pixelelated-m7-sm8550-acceptance-01 (created before submission)

All stages use normal watchers and exclusive result verification; the outer
controller only orchestrates them and has its own state/result. If it fails,
read the exact failed owner and preserve it. Do not reset or blindly replay
stages. A failed tracker write does not abandon an active compiler; its error
is retained separately. SM8550 proof covers GPT, ABL files, raw/update payloads,
installed architecture/identity and ARM handoff. These templates have not yet
accepted actual SM8550 artifacts. Four sequence controls and three container
recorder controls pass. No device flashing or release claim is inferred.

## Publication/checkpoint

Cleanup-completion publication16-retry01 is accepted on next
9e8cfeff855be64fa85ee84a0a9225e260462f1d, featurec1bd20406a0c54e3959f10fcf5ba2c85a241195d,
with four0/514seals/exits and both exact-next-head checks passing. Initial16
failed before staging because its preparer used the primary path; preserved.
The combined cleanup16-ci-01 owner is FAILED, not passed: it found two old
feature-only archive lines absent from next. #499 corrected exactly those two
lines; feature-only normal-hook commitfe471bde1ca154f7147a2d9f2468ac03bb4c83f2,
full local scan and exact-head hosted37586286848 pass. Both publication and
CI owners have verified exits. #498/#499 are closed with explicit evidence.
No product or instruction changed, and next never received those extra archives.

This next documentation/preparation publication owner is
/workspace/tmp/pixelelated-m7-device-sequence-publication-17. Its actual
publication.json/owner-verification.json identify later heads and acceptance.
Follow-up CI owner /workspace/tmp/pixelelated-m7-device-sequence-ci-01 must be
consumed on the exact heads. After publication and CI, launch the already sealed
sequence owner once and read back its PID, waiter watcher and state heartbeat.
Keep H700 actively supervised; do not stop merely for this checkpoint.

Previous checkpoint: .github/sessions/archived/saved-session-state-next-20261007T072942Z.md.
