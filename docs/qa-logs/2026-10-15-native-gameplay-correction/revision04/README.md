# Revision04 source custody — actual owner03

This immutable source subpacket is bound to `/workspace/tmp/pix-m7-native-gameplay-20261015-03`, admission `ebed7b8ebcc040f2ae09acdf7531f8ab`, launcher PID `2430652` with recorded start ticks `112033043`. The source is `d4af5a255f4778a6ecf63ca5b37e05a0f1c83e3a`, branch `build/m7-p5-20261015-01`, VNC137. Root reported this owner active; no runtime result was read or qualified by this retention task. Admission and submission are not completion.

The unchanged private packet is `/tmp/m7-native-gameplay-lifecycle-20261015-03`, SHA256SUMS SHA-256 `c9d6faa5bb47950f5c73f947bf03fa925ba2fbdebc8a4d0c5ffb3824ae02379d`. [revision04-profiles.diff.gz](revision04-profiles.diff.gz) is the exact additive Revision03→04 change. Only `guest.py` gains bounded live profile reporting through the existing status response and unchanged `host-action.py` shared-lock route. The prior raw/SDL positive identity and failure cleanup corrections remain. Controller construction, input actions, normal launchers, gameplay/save/frame criteria, and the 1800-second family / 120-second cleanup / 120-second first-frame / 360-second scoring bounds remain unchanged.

The fixed profile allowlist, positive current controller identity, explicit missing-file handling, and exclusion of raw/account values from Flycast emu.cfg are described in [REVISION04.md](REVISION04.md). The original static review and earlier UNRUN wording describe source preparation; they are preserved as written and do not describe the later active owner's current state. Actual profile observations and gameplay evidence belong to root's runtime originals.

[source-packet.tar.gz](source-packet.tar.gz) contains 52 exact nonduplicate source members. [source-packet-member-manifest.json](source-packet-member-manifest.json) retains paths, hashes, sizes, modes and timestamps; every member was checked after archiving. All 52 omitted duplicate failed-export members match the [published failure archive](../../2026-10-15-native-gameplay-fixture-failure/README.md), whose missing guest-manifest/busy-unmount limits remain. The source archive plus that archive under `failed-originals/` reconstructs the full private packet and its original seal.

[prepared-owner-source-readback.json](prepared-owner-source-readback.json) verifies all 28 actual prepared-owner code/source hashes against this source packet and checks the original completed-image/source bindings. Exact configuration, preparation binding, admission, launcher-start and launcher-submission receipts are copied here. These are source and submission inputs only; no active-owner files were changed, no guest was contacted, and no lifecycle outcome is inferred.

Historical Revision03 bytes and its original durable seal remain untouched in the parent directory. This subdirectory has its own `SHA256SUMS`; the parent's `COMPLETE-SHA256SUMS` seals both immutable versions and the added index. No source, runtime, preparer, admission, staging, commit, or shared record was changed by this custody task.

Repository storage preserves the exact diff bytes as deterministic gzip;
`diff-storage.json` binds the raw identity and original seals. The original
private packet and archived source bytes remain unchanged.
