# Saved Session State

> **Saved**: 2026-10-13T08:26:24.350000+00:00
> **Branch**: feature/m7-player-setup
> **Repo**: pixelelated/distribution

## Start here

pixelelated is an immutable Linux gaming distribution. Read next's AGENTS.md,
every-session rules, docs/device-testing-policy.md and the live M7 milestone
body before acting. Main /workspace/repos/rocknix stays on next. Coordinator
works in /workspace/repos/rocknix.worktrees/m7-player-setup; harness cwd
conflict-resolution is stale and must remain untouched. Current investigation
started from published1a37cde40ab0893c9c21c0a383c59ac0c1403b06.

The latest user asks to continue browser/rclone memory-pressure investigation
and resolve the provenance of the Nova's pre-existing account and metadata.
The exact request is recorded in #570 and #565. Existing owner operations are
not replayable authorizations. No owner device/cloud/account/save operation
occurred in this continuation. No firmware pin, browser policy or ES product
source has been promoted. The small trim proposal remains UNCOMPILED.

## Current focus and measured results

#570 now has a concrete allocator optimization to qualify. Actual normal ES
cloud handoff frees substantial heap without returning it to the OS. A tiny
ES-only target-built interposer at the post-deinit cloud_oauth-wait seam ran
four65second actual unauthenticated Dropbox trials: sham/trim/trim/sham.
Anonymous pages returned0/79504/77548/0KiB; trim2.049/2.018ms. Settled ES
anonymous medians113416/33752/33608/113024KiB. Minimum available
166708/223408/226884/164684KiB. Each case loaded/returned on its own unchanged frontend
PID; all four shared one boot, sampler0, memory guard clear. No proxy account or phone client;
cookie banner untouched, no completed login/input-usability proof.

This is allocator attribution, not a physical slowdown cure or compiled
production-patch proof. Initial browser-before-deinit overlap is unchanged.
WebProcess peak PSS is higher with trimming; no smaller-browser claim.
Two cases per mode/one boot/live provider and observer overhead limit timing
inference. Actual CLK_TCK100 recorded; PSI unavailable. Raw request URLs and
temporary pairing frames remain private; public packet keeps numeric evidence
and four reviewed provider-page frames. All four return frames reviewed too.

Packet: docs/qa-logs/2026-10-13-memory-state-followup/. Run
`python3 .../analyse-matrix.py` to recompute summaries. Exact compressed source
proposal and byte hashes are in cloud-handoff-trim.patch.gz/product-proposal.json.
Original ES pin c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78. Initial matrix was
invalidated/interrupted143 because missing PSI killed its sampler and case rc
ignored that failure. Retain matrix-invalid.json; never count or replay it.
Corrected matrix02 checks sampler health before launch/during/at completion.

All memory channels consumed, original paths restored, actual host PIDs exited,
exact VM stopped/disk/UEFI/keys retired;2,252,709,888allocated bytes recovered.
Owner /workspace/tmp/pix570-es-trim-20261013 is COMPLETE/RETIRED. Its old ports
10576/5961 and commands are historical. Never replay this owner.

## Nova provenance and executable gate

Read memory-state-followup/nova-provenance.md and nova-field-presence.json.
First fork install September29 was an in-place update retaining storage;
recorded actions show firmware staging/verify/reboot/reads, no config/gamelist
copy, but cannot exclude UI/unrecorded actions. The then-effective account
combination was incomplete, not proof of every field empty. Original fields
were populated before October9 update. Authors/entry path remain unknown.
September30 logs show empty restore then0B backup, settings backup skipped:
dates don't prove transferred games/settings. Recent-list positive playcounts
and lastplayed dates predate first fork install; metadata suffices for list
membership and does not prove local Nova gameplay. No credential values or
secret-derived hashes are public. Selected accepted-SYSTEM findings alone
never constituted a complete image scan.

New tools/pixelelated-state-check and tools/pixelelated-state-check-test plus
prepare-only release integration are source-reviewed and tested. Packet:
docs/qa-logs/2026-10-13-clean-state-runtime/. Actual ready fresh VM20 gate passes;
113guest synthetic-root controls pass. All142host root/payload/release-preparation
controls pass with final tool bytes (45d899 source, cc0f8 integrated). Initial
first-boot2 and host payload2 failures remain preserved, never relabelled.
Corrections handle comment-only upstream defaults, exact current-boot zero-work
scrub marker, valid retained partial/reordered scrub history, and canonical unused
ext4 slots. Final gate AST differs from guest-testedab47 only in empty_ext4;
guest execution path is unchanged. Actual future candidate payload and real
retained-storage upgrade are still owed. No whole-image credential guarantee.
The fresh VM/disk/UEFI are retired,2244313088allocated bytes recovered; no SSH
key/account/storage fixture was staged. Final payload scratch188178432bytes peak,
empty afterward. All original owner/wrapper/watcher channels and host PID exits
consumed. No runtime job is active. Old owners pix565-clean-state-20261013,
pix565-payload-20261013, both diagnostic owners and pix565-payload02-20261013
are COMPLETE; don't replay. Diagnostics are expected2, accepted final runs0.

## Visible lanes and ownership

Coordinator Herdr w4:p2 owns shared records, runtime and integration. Existing
visible workers retain their scoped checkouts; no new lane is needed:

- pix-memory w4:p8, m7-browser-memory-570: source-only7ebc601e32 WebKit cleanup
  policy packet (38verified inputs), integrated as894ac0aea9. No runtime lease;
  candidate changes strict threshold only. Hold while narrower ES trim qualifies.
- pix-nova w4:p9, m7-clean-state-565: COMPLETE45d899bdf3371937dfd494bc0a43e50ea1c4871e; integrated throughcc0f8b0aa7. Source-only assignment;
  coordinator owns all runtime evidence. No owner-device permission inferred.
- pix-gtk4 w4:p7, m7-gtk4-576: prior feasibility COMPLETE/held. GTK4/WebKit6
  dependency/native-keyboard spike remains uncompiled; no savings measured.

Prior lazy-proxy target bytecode experiment saves390KiB (0.38MiB), versus
5442KiB host-source-only result. Preserve existing offline functionality.
Both loopback component probes passed; full service/ES lifecycle unqualified.
Prior22 UA/breakpoint/phone trials are complete/retired. Do not repeat old
delivery03, bytecode or browser owners. D-WORKFLOW-163 still bounds those
diagnostic candidates; the new measured ES opportunity is the next narrow lead.

## Next steps, in order

1. Consume current record delivery below if necessary; never replay old owners.
2. Qualify the minimal ES cloud-handoff trim as actual source/binary: isolated
   ES branch fromc8dc72cf9e, syntax/package checks, source-bound normal sign-in,
   phone/native input, cancel/error/return/lifecycle flows and canonical frame
   index. Keep startup order/status handling. VM first, then the RG35XX SP bench device (H700, Tailnet100.74.205.40)
   for physical memory/input corroboration under D-QA-060 through tools/device-act.
   The separate RG SP100.75.221.73 and Nova are outside this browser test scope. A build
   or full cache copy first requires #493 lifecycle/capacity enforcement.
3. Finish #565 actual final-payload/clean-first-boot and real synthetic-account
   retained-storage upgrade qualification. Component fixtures aren't a real
   upgrade. Keep owner provenance uncertainty explicit; no Nova reset/cleanup
   is implied. #572 GStreamer packaging repair is published2292e9a298 but final
   assembled-image proof remains due. Existing latest stable WebKit2.54.1 is
   already pinned; no applicable upstream memory fix has been established.
4. #566 dedicated provider-supported ScreenScraper identity; no third-party
   credential reuse rights inferred. #567 conditional offline-RA notice on
   game-list refresh; #571 compact phone status without navigation/disconnect
   confusion. Each UI change needs canonical flow and same-source EN/FR frames.
5. #574 RVZ frontend achievement hashing/recognition; #575 standalone selected
   emulator save-on-exit/manager capability. Current selected Nova cores aren't
   known after read timeout; do not guess. #568 finalizing copy stays future.
6. #564 reproduced Steam failure on isolated ROCKNIX stable20261001 foundation
   c445081a59518f37d9776e5412dd7b14910696f7; #493 before full copies/builds;
   new-source clean/retained VM qualification and independent audit, then
   H700 followed bySM8550 builds, then #528/#344 publication/source/custody.
   No new RC number or public publication clearance is allocated.

## Resource and execution notes

Accepted VM20 source1a026648442321609b2288c2c9c06803817f9df2; accepted handheld
sourcebc9dfe8141d9561dc1d8502313d00a84c4566ee8. Frozen cache is
/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20. Absolute build
files expect container path /workspace/repos/rocknix.worktrees/m7-pixelelated.
Never mutate/hardlink mutable cache contents. Builder pinned at
ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39.
ES /home/max/Development/emulationstation-next is stale: use git show accepted
pin and an isolated feature checkout for edits.

Use require_escalated for active-path writes/network and host process checks.
Sandbox /proc is a separate PID namespace, not evidence of host PID absence.
/tmp is writable again; prior quota statement in archived checkpoint is stale.
Automatic approval service intermittently timed out/returned capacity failure;
fresh original requests later succeeded without bypass. No new permission is
required merely because a prior automatic review failed to execute.

Long commands use fresh existing owner with tools/watch-build-submit
`--owner OWNER -- --activity-dir OWNER -- COMMAND`. Submission is not success.
Consume actual inner result, launcher-result, tool-wrapper.rc, watcher build.rc
and actual host launcher/build/command/watcher/build.status PID exits. No
off-session notification exists; actively supervise and announce completion.
Keep durable compact logs/source/receipts; remove completed disposable disks.

## Record delivery

Delivery01 refused before push for a missing issue citation in an unpublished
formatting commit; all original channels1 and actual host exits are consumed.
The message was amended with identical file tree and verified remote unchanged.
The serial evidence is now byte-verified gzip (38 state-packet files); no test
result changed. Current fresh delivery owner is
/workspace/tmp/pix-m7-investigation-20261013/delivery02. It requires committed
clean feature/main, ff-only next integration, guarded push and exact-head hosted
record/wordlist success. Inspect result.json, launcher-result, tool-wrapper.rc,
watcher build.rc, actual host PID exits and origin HEAD before saying delivered.
Do not replay any completed owner or start a duplicate publisher. No external
code-audit transfer belongs to this delivery. Old delivery03 at1a37 is complete.
The current record includes fork-only tool registration in the hook, canonical
fork-workflow and instruction-files index; rules/register/index/ceremony gates
must pass before the push. No package.mk edit occurred.

Previous checkpoint: archived/saved-session-state-next-20261013T082624Z.md
