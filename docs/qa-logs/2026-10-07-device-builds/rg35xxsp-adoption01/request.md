## Maintainer request

> The rg35xx sp is now online. You have permission to transfer the build and reboot.

## Current state and scope

M7.P5 follows #492. H700 firmware from `43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa` passed artifact acceptance, including both DDR variants and 185 ARM handoff files. The online RG35XX SP currently runs ROCKNIX `69e6039f8fdbf971d3e6b694537f250036fdcd98`; its update queue is empty, LPDDR4 is confirmed at 1100000 microvolts, and external power is connected. Battery starts at 3%; recheck power after staging before reboot.

The explicit authorization covers transferring this accepted H700 update and rebooting to apply it. Stage the tar outside `.update`, verify its SHA256 on the device, then queue it. The update preserves `/storage` and uses the normal updater; normal configured shutdown/startup automation may run. Further gameplay, injected input, screenshots and deliberate personal-cloud actions are outside this authorization.

Can this be done on the VM? Common migration/software qualification already passed there. No: this observation is the actual H700 DDR4 bootloader, RG35XX SP device tree, physical storage and Wi-Fi reconnection after applying the update. See `docs/releases/device-facts.md`, row “H700 boot on the RG35XX SP (LPDDR4 unit)”.

## Acceptance criteria

- [ ] Credential-filtered preflight records the physical model/DTB, RAM voltage, predecessor BUILD_ID, boot ID, power, idle state, mounted storage and empty queue.
- [ ] Host and device SHA256 values match the accepted update `a419dc33e1f3be2c422cac4b89d85cf104f363c3da6ed7059e0a8aa531bfd014`; device-act records transfer and checksum-gated queueing.
- [ ] The authorized device-act reboot has a subsequent changed boot ID and readback of pixelelated 0.0.1 / BUILD_ID `43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa`, expected model/DTB, LPDDR4 voltage, storage mounts, exact installed binary hashes and empty update queue.
- [ ] Compact evidence, standing hardware fact and work log record the actual outcome; broader device smoke and release gates remain separately identified.

Evidence owner: `/workspace/tmp/pixelelated-m7-rg35xxsp-adoption-01`; compact repository evidence: `docs/qa-logs/2026-10-07-device-builds/rg35xxsp-adoption01/`. Preserve the applicable recovery firmware until this immediate adoption check completes; no unrelated cleanup is inferred.
