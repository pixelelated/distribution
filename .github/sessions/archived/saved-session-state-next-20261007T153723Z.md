# Saved Session State

## Start here

Resume pixelelated M7 /0.0.1 from the actual owners below. This repository builds
an immutable handheld Linux OS, not an app. Primary `/workspace/repos/rocknix`
stays on `next`; coordination is `/workspace/repos/rocknix.worktrees/conflict-resolution`.
Read AGENTS.md and canonical `.claude/rules/` from next before changes. Never
sync a frozen build tree, edit an in-flight script, or replay completed tests.
The prior full checkpoint, cleanup/source-custody details, and publication
history are in `.github/sessions/archived/saved-session-state-next-20261007T111920Z.md`.
No new agents, goals, external audit or Daybreak. Never print credential values.

Standing authority covers fixes, host/VM tests, fork tracking/commits/pushes,
classified cleanup, and H700 then SM8550 compilation. The latest explicit
physical authorization is ONLY the RG35XX SP transfer and one reboot in #500:
“The rg35xx sp is now online. You have permission to transfer the build and reboot.”
No additional screenshot, input, game launch, deliberate personal-cloud action,
other device update/reboot, upstream PR, release publication or storage redesign.
Every device change uses `tools/device-act`; credential-filter readbacks.

## Current work — 2026-10-07 11:28 UTC

### #500 RG35XX SP adoption — COMPLETE

The authorized transfer and ONE reboot have completed. Do not repeat either.
The SP is running pixelelated0.0.1 /43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa.
Acceptance11:25:25UTC; four zero channels, one seal and all process exits
independently verified11:26:33UTC. Both owners already have exclusive
owner-verification.json receipts; read them rather than rerunning the verifier.

- Stage `/workspace/tmp/pixelelated-m7-rg35xxsp-adoption-01`: complete archive
  transferred and hash-checked before queueing. No partial remains.
- Reboot `/workspace/tmp/pixelelated-m7-rg35xxsp-reboot-01`: returned0; device
  returned11:23:31UTC, essway active11:24:17UTC. Boot ID changed from33c0063d
  tobf8756cd-06f7-4192-bedb-7d02c5afb6a8. Original storage mounts present;
  update queue empty. No failed units; ES/pipewire services active, zero restarts.
- Exact SYSTEM/kernel/SP DTB/DDR4 bootloader/ES/RetroArch/RetroArch32 hashes
  match the accepted bundle. Actual LPDDR4 voltage1100000microvolts.
- Battery began3%, reached10% on external power before reboot and14% afterward.
- Scheduler/audio-policy journal messages also appear on the predecessor and
  September25 work log. No new fault established; no audio/gameplay proof.
- Evidence `docs/qa-logs/2026-10-07-device-builds/rg35xxsp-adoption01/`, with
  filtered readbacks and exact operation scripts. Hardware fact updated.
  No screenshot/input/game or deliberate personal-cloud action performed.
- SSH alias remains `rg35xxsp`, LAN192.168.1.81. Reads need credential filtering;
  further state-changing actions need their own named authorization.

### #492 SM8550 build — continuous sequence active

H700 artifact acceptance is COMPLETE. The automatic controller advanced to
SM8550 at09:09UTC. Its ARM compatibility stage passed at09:28UTC. Aarch64
firmware is BUILDING (697/737 at11:18UTC with fresh package activity).

- Controller `/workspace/tmp/pixelelated-m7-sm8550-sequence-01`, PID3499961,
  start ticks45040028. `state.json` heartbeat every30s; `controller-result.json`
  only at terminal. Never launch a duplicate. It also updates #492 and M7.
- Frozen tree `/workspace/repos/rocknix.worktrees/m7-pixelelated-sm8550-01`,
  `build/m7-pixelelated-sm8550-01`, HEAD40f80c5151d5c9281be5ca95121e0a1fe0d918d9.
- Build owner `/workspace/tmp/pixelelated-m7-sm8550-build-01`;
  run `.build-runs/20261007T090954Z-976662f7` in that frozen tree.
  Runner701533, watcher701534, container9afb0ede6bd00471c7d994f88467d6e2c0c5f4a60e078cb0761814ae31647238.
- Acceptance owner `/workspace/tmp/pixelelated-m7-sm8550-acceptance-01`;
  run `.build-runs/20261007T090956Z-2b0cb48e` in primary. It waits for actual
  builder exit, verifies independent firmware custody, GPT/ABL/raw-update
  equality, installed identity and exact32-bit handoff, then removes scratch.
- Same pinned container988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39,
  global24/WebKit4. Guarded swap preflight passed between stages. Never reclaim
  swap while active jobs are running. Disk had1.9TiB available at11:04UTC.
- Consume actual SM build/acceptance terminal results and controller result;
  never call queueing or a status file acceptance. If tracker update fails,
  keep the builder alive and reconcile retained tracker errors separately.
- Watchers record locally; disconnected chat alerts remain #395. Active-session
  supervision and reporting are still needed. No claim of off-session delivery.

## Accepted H700 firmware

Frozen tree `/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01`,
branch `build/m7-pixelelated-h700-01`, commit43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa.
670/670 completed09:07:58UTC. Firmware acceptance passed09:08:34; owner exits,
four zero results and four seals independently verified09:08:36. Both DDR
variants, raw/update payload equality, installed identity and185 ARM handoff
files accepted. Owners `pixelelated-m7-h700-firmware-01` and
`pixelelated-m7-h700-firmware-acceptance-01` under `/workspace/tmp`.

Immutable bundle `/workspace/artifacts/pixelelated-candidates/sha256/d89b067a5176d7c02633bc9e72ee9b0f96dd3d626d343a0f16949e70c9daf710`.
Shared update `pixelelated-H700.aarch64-0.0.1-from-ROCKNIX.tar`,1320970240bytes,
SHA256a419dc33e1f3be2c422cac4b89d85cf104f363c3da6ed7059e0a8aa531bfd014.
H700 arm05 already accepted244tasks/7866files/797links/938ARMobjects;
manifest116314730b3ce22407219f14c1646694ebabc2723a2c24c8ca9e553ff5783e18.
#497 actual handoff proof is now available; remaining tracker reconciliation
must read all criteria before closing. No software pin/target flag changed.

## Completed qualification — never replay

Candidate16 distributionee014909137e03706e0b3020b8396be589aaa705,
ES72494bc72e3d64d4dcfeb4e6478052bbdf166c5b,
bundle7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a,
SYSTEM5767ee7d72f3c538259ee927ad681c63533d661997b64e6beac9d83fdc70812c.
15VM suites,78screens,26RC2 upgrade checks and318WebDAV/SFTP/MinIO checks passed.
Eight P4 audit findings resolved; both approved Fable transfers accepted.
RA33 Tobu15738/100359 award+flush and125-game proof complete; reset consumed.
No Dropbox check or new RA reset owed. #495/#496 build-host repairs complete;
#497 adds seven generated ARM-path fixes plus the recorded host repair versus16.
Later #432 FOSS observability, #464 RA reset automation, #395 off-session alerts.

## Cleanup/custody — completed batch must not repeat

Broad owner `/workspace/tmp/pixelelated-m7-broad-cleanup-01` is accepted:
850payloads,30extraction paths,four obsolete trees09/10/12/14;884targets absent;
recovered2117325385728bytes. Retained51070compact records and14489source objects.
#494 closed; #493 broader retirement/classification remains. D-INFRA-022 retains
large disks/firmware only for named active/immediately queued tests. Preserve
required source/licence material and compact evidence; historical references
alone do not require a disk. Named device recovery holds end when their tests do.

Historical #498 limitation: administrator scan omitted14authorized loose
firmware files; those had ordinary-user/container/reference checks but no
root-only coverage. Original receipts remain unchanged; supplementary gap
record retained. The corrected executor has eight passing coverage controls.
#498 closed; do not retrospectively claim full root coverage. Root receipt is
consumed; fresh cleanup needs a new exact scope/check, not a replay. #499 closed
with feature-only two-line archive correction and exact-head hosted proof;
the original combined CI owner remains FAILED (next passed, feature failed).
Preserve `/workspace/artifacts/pixelelated-build-custody/issue-494-device-capacity-01`,
prior #456 source store and referenced rclone archive under
`/workspace/tmp/rasteratops-m7-qa-01/recovered-inputs/`. Previous full checkpoint
names all retained dependencies and owner receipts.

## Publication and next actions

Last accepted publication17: feature1e3c7e8f633d867f55c3c1df79d708320231548d,
next40f80c5151d5c9281be5ca95121e0a1fe0d918d9. Its normal-hook commits/pushes,
remote refs, four result channels/25seals/exits verified. Both next checks and
feature wordlist check succeeded. No pending old CI replay.

1. #500 transfer/reboot/installed verification is complete; no repeat owed.
2. Continue consuming active SM8550 build/acceptance/controller outcomes.
3. Reconcile completed #492/#497 criteria from actual artifacts, without
   closing source/licence or publication requirements from a compile alone.
4. M7.P5 still owns separately named device smoke/adoption, corresponding source,
   fourteen known source/licence metadata gaps, public docs and manifest-bound
   release assets. No RC designation or publication inferred.

New publication owner `/workspace/tmp/pixelelated-m7-rg35xxsp-publication-01`
records actual integration/push in publication.json and owner-verification.json.
Read those receipts before assuming this checkpoint is published. Keep feature-only archive
history out of next: commit scoped changes and cherry-pick the new commit only;
never merge the whole divergent feature branch. Preserve normal hooks.
