# RG SP and Nova update acceptance — October 12

Both owner-approved updates are complete under #557. Distribution source is `bc9dfe8141d9561dc1d8502313d00a84c4566ee8`; displayed build identity is `0.0.1-dev+20261011T222153Z.gbc9dfe8141d9`. These are accepted engineering builds; no public RC is allocated.

| Device | Verified result | Preservation |
| --- | --- | --- |
| RG SP, H700 DDR3 | Full transfer SHA, SYSTEM/kernel/DTB/bootloader/ES/both RetroArch hashes; original mounts, empty update queue, new boot, frontend active with zero restarts | 163 protected files / 25,545,421 bytes, 5 recovery entries, credentials, paths and settings unchanged; accepted 04:09:27 UTC |
| Retroid Pocket Nova, SM8550 | Full transfer SHA, SYSTEM/kernel/ES/both RetroArch, all 5 ABL files and both actual ABL slots; original mounts, empty queue, new boot, frontend active with zero restarts | Configured safe scope contains no files; credentials/paths and all settings values unchanged; accepted 04:28:49 UTC |

All original stage/reboot result channels are zero, with actual owners exited. Each transfer used a partial file outside the update queue, device SHA verification and repeated unchanged-state guards. Exactly one approved reboot was sent per device. Both returned through the Tailnet. Automatic cloud startup/game-exit sync remains off. The separately accepted RG35XX SP was untouched.

The owner explicitly approved configuration hash checks and both reboots after previously approving the transfers. Private manifests retain full-file hashes and one canonical hash of all parsed settings values, including duplicate-value order. No raw configuration values were copied or displayed. Nova rewrote the bytes of `system.cfg`; its complete parsed settings hash is unchanged, as are its metadata and backup. Personal inventories and configuration hashes are excluded from this public packet.

Per-device `stage01/owner-verification.json`, `reboot01/owner-verification.json` and `preservation-summary.json` carry acceptance. Bounded startup error logs remain alongside installed readbacks; this is not a claim that logs are empty. No game, audio, screenshot, injected input or personal-cloud operation was performed. Zero frontend retries is one observation on this boot, not a measured failure-rate claim.

Both devices are returned to owner use. The subsequent #493 guarded removal of 17 superseded build trees is also complete; see [retention acceptance](../2026-10-12-storage-retention/oldtrees/README.md). Current firmware, required sources, compact records and current build caches remain protected. Earlier observation/tracker files in this directory remain historical; completion receipts supersede pending-approval status. The owner's later Nova shutdown observation is tracked separately in #558 and does not rewrite the original deployment result.

Public stage console-log copies normalize terminal blank lines to one newline for repository whitespace checks. `public-log-normalization.json` binds the before/after digests; private originals are unchanged. Original exit-code and acceptance receipts are copied without alteration.
