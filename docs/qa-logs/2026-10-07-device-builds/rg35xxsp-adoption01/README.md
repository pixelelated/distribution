# RG35XX SP adoption — #500

The explicitly authorized H700 transfer and single reboot completed successfully.
The predecessor was ROCKNIX69e6039f8f; the installed system is pixelelated0.0.1,
BUILD_ID43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa.

- Transfer1320970240bytes completed, matched on-device SHA256a419dc33e1f3be2c422cac4b89d85cf104f363c3da6ed7059e0a8aa531bfd014,
  then entered the update queue at11:15UTC. Four zero channels, sealed source
  and process exits independently verified11:16UTC.
- External power remained connected. Initial3% battery rose10% before the
  single reboot; device-act returned0. The device returned on the expected
  build at11:23:31UTC; essway was active by11:24:17UTC.
- Installed verification passed11:25:25UTC; four zero channels, sealed source
  and all process exits independently verified11:26:33UTC.
- SYSTEM, kernel, SP DTB, exact DDR4 bootloader bytes, EmulationStation,
  RetroArch and RetroArch32 hashes match accepted firmware. Boot ID changed
  from33c0063d-cfd3-46f8-8e54-5ff4f9727283 tobf8756cd-06f7-4192-bedb-7d02c5afb6a8.
  Update queue is empty; original /storage and /storage/roms mounts remain.
  Battery read14% after verification; external power connected.
- Interface and audio services read active/running with zero restarts and no
  failed units. Recorded scheduler/audio-policy journal messages also appear
  on the predecessor and in September work logs; do not claim an error-free
  journal or audio/gameplay acceptance.

Can this be done on the VM? Software migration is already qualified there.
This proof observes the actual H700 DDR4 bootloader, SP device tree, physical
card and Wi-Fi reconnection. See the standing H700 SP hardware fact.

No screenshot, injected input, game launch or deliberate cloud operation was
performed. Broader device smoke, source/licence/public-docs and publication
remain separate. This is successful adoption, not RC designation.

Private owners: `/workspace/tmp/pixelelated-m7-rg35xxsp-adoption-01` and
`/workspace/tmp/pixelelated-m7-rg35xxsp-reboot-01`. Both used normal watched
launchers. Their compact result/verification readbacks are retained here;
source scripts record the exact operations and must not be blindly rerun.
Large update payloads are not copied into the repository.
