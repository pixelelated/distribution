# Historical cloud-path sweep reconciliation

The immutable first-sweep report has 56 hits under its broad `cloud-path`
rule. This receipt matches every original line to its actual baseline source
and classifies the corresponding frozen candidate15 source. Many hits are
upstream URLs or build paths. Historical and compatibility examples remain;
all changed cloud defaults use `/pixelelated`.

This is a retrospective mapping written now. It does not claim the mapping
was written in the historical implementation commits. The original sweep
remains unchanged. Whole-image brand/credential classification and VM
migration checks are separate evidence in this candidate's QA directory.

| Hit | Original location | Disposition | Candidate line |
| --- | --- | --- | --- |
| 1 | `distributions/ROCKNIX/options:186` | KEEP_UPSTREAM_URL | 186 |
| 2 | `projects/ROCKNIX/bootloader/install:53` | KEEP_BUILD_PATH | 53 |
| 3 | `projects/ROCKNIX/config.xml:48` | KEEP_BUILD_PATH | 48 |
| 4 | `projects/ROCKNIX/devices/RK3326/packages/u-boot-legacy/package.mk:9` | KEEP_UPSTREAM_URL | 9 |
| 5 | `projects/ROCKNIX/devices/RK3588/packages/u-boot/package.mk:9` | KEEP_UPSTREAM_URL | 9 |
| 6 | `projects/ROCKNIX/devices/S922X/packages/u-boot/package.mk:10` | KEEP_UPSTREAM_URL | 10 |
| 7 | `projects/ROCKNIX/packages/apps/commander/package.mk:8` | KEEP_UPSTREAM_URL | 8 |
| 8 | `projects/ROCKNIX/packages/apps/jstest-sdl/package.mk:9` | KEEP_UPSTREAM_URL | 9 |
| 9 | `projects/ROCKNIX/packages/apps/portmaster/package.mk:14` | KEEP_UPSTREAM_URL | 14 |
| 10 | `projects/ROCKNIX/packages/apps/rocknix-hotkey/package.mk:8` | KEEP_UPSTREAM_URL | 8 |
| 11 | `projects/ROCKNIX/packages/compress/cabextract/package.mk:9` | KEEP_UPSTREAM_URL | 9 |
| 12 | `projects/ROCKNIX/packages/emulators/libretro/idtech-lr/package.mk:12` | KEEP_UPSTREAM_URL | 12 |
| 13 | `projects/ROCKNIX/packages/emulators/standalone/aethersx2-sa/package.mk:8` | KEEP_UPSTREAM_URL | 8 |
| 14 | `projects/ROCKNIX/packages/emulators/standalone/drastic-sa/package.mk:8` | KEEP_UPSTREAM_URL | 8 |
| 15 | `projects/ROCKNIX/packages/graphics/libmali/package.mk:8` | KEEP_UPSTREAM_URL | 8 |
| 16 | `projects/ROCKNIX/packages/linux-drivers/chipone_tddi/package.mk:8` | KEEP_UPSTREAM_URL | 8 |
| 17 | `projects/ROCKNIX/packages/linux-drivers/rocknix-joypad/package.mk:8` | KEEP_UPSTREAM_URL | 8 |
| 18 | `projects/ROCKNIX/packages/linux-firmware/extra-firmware/package.mk:8` | KEEP_UPSTREAM_URL | 8 |
| 19 | `projects/ROCKNIX/packages/linux-firmware/extra-firmware/package.mk:9` | KEEP_UPSTREAM_URL | 9 |
| 20 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:16` | KEEP_LEGACY_COMMENT | 16 |
| 21 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:33` | CHANGED_CURRENT_DEFAULT | 57 |
| 22 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:34` | CHANGED_CURRENT_DEFAULT | 58 |
| 23 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:35` | CHANGED_CURRENT_DEFAULT | 59 |
| 24 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:103` | KEEP_LEGACY_COMMENT | 216 |
| 25 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:376` | KEEP_LEGACY_COMMENT | 509 |
| 26 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:377` | KEEP_LEGACY_COMMENT | 510 |
| 27 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:379` | KEEP_LEGACY_COMMENT | 512 |
| 28 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:479` | KEEP_LEGACY_COMMENT | 734 |
| 29 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:573` | KEEP_LEGACY_COMMENT | 1220 |
| 30 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:587` | KEEP_LEGACY_COMMENT | 1234 |
| 31 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:604` | KEEP_LEGACY_COMMENT | 1257 |
| 32 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:755` | KEEP_LEGACY_COMMENT | 1544 |
| 33 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_restore:1702` | KEEP_LEGACY_COMMENT | 1719 |
| 34 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_setup:693` | CHANGED_CURRENT_DEFAULT | 829 |
| 35 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_setup:694` | CHANGED_CURRENT_DEFAULT | 830 |
| 36 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_setup:702` | CHANGED_CURRENT_DEFAULT | 838 |
| 37 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf:30` | CHANGED_CURRENT_DEFAULT | 30 |
| 38 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf:34` | CHANGED_CURRENT_DEFAULT | 34 |
| 39 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf:46` | CHANGED_CURRENT_DEFAULT | 46 |
| 40 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf.defaults:30` | CHANGED_CURRENT_DEFAULT | 30 |
| 41 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf.defaults:34` | CHANGED_CURRENT_DEFAULT | 34 |
| 42 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf.defaults:46` | CHANGED_CURRENT_DEFAULT | 46 |
| 43 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync_helper:375` | KEEP_LEGACY_COMMENT | 375 |
| 44 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync_helper:469` | KEEP_LEGACY_COMMENT | 469 |
| 45 | `projects/ROCKNIX/packages/textproc/textviewer/package.mk:8` | KEEP_UPSTREAM_URL | 8 |
| 46 | `projects/ROCKNIX/packages/tools/inputplumber/package.mk:15` | KEEP_BUILD_PATH | 15 |
| 47 | `projects/ROCKNIX/packages/tools/rocknix-abl/package.mk:7` | KEEP_UPSTREAM_URL | 7 |
| 48 | `projects/ROCKNIX/packages/tools/rocknix-abl/package.mk:8` | KEEP_UPSTREAM_URL | 8 |
| 49 | `projects/ROCKNIX/packages/tools/rocknix-splash/package.mk:9` | CHANGED_FORK_SOURCE | 9, 8 |
| 50 | `projects/ROCKNIX/packages/tools/sound/soundfont-generaluser/package.mk:9` | KEEP_UPSTREAM_URL | 9 |
| 51 | `projects/ROCKNIX/packages/virtual/arm/package.mk:44` | KEEP_BUILD_PATH | 44 |
| 52 | `scripts/update_packages:7` | KEEP_BUILD_PATH | 7 |
| 53 | `scripts/update_packages:8` | KEEP_BUILD_PATH | 8 |
| 54 | `scripts/update_packages:9` | KEEP_BUILD_PATH | 9 |
| 55 | `scripts/update_packages:10` | KEEP_BUILD_PATH | 10 |
| 56 | `scripts/update_packages:16` | KEEP_BUILD_PATH | 16 |
