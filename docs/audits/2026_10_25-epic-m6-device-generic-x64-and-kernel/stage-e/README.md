# T11 stage E: the positives, kept on the branch (#658)

Every stream's case, as a command the acceptance re-run can repeat from this branch. Each positive's expectation fails on the unfixed file and holds on the fixed file. Each control holds on both.

- **The unfixed files** are at **`499628a049`** (the stage-D tip), in a shared clone: `git clone -q --no-checkout --shared <this worktree> <U>; git -C <U> checkout -q 499628a049 -- <the file>`. For example, `<U>/projects/ROCKNIX/bootloader/install`.
- **The fixed files** are this branch's at `fixed-at`.
- **The drivers** take the file under test first and `unfixed|fixed` second, then their case. They write only under `$TMPDIR` and print one verdict line last (`<driver> <case>: unfixed-expectation-met | fixed-expectation-met | UNEXPECTED ...`). They exit 0 when the named side's expectation is met, 1 when it is not, and 2 when they cannot run.
- **No guest, no build, no device.** Every case runs on the host.

Set up once, from the worktree's root:

```bash
export TMPDIR=/workspace/tmp/<yours>; mkdir -p "$TMPDIR"
S=docs/audits/2026_10_25-epic-m6-device-generic-x64-and-kernel/stage-e
U=<the clone at 499628a049>      # unfixed
```

## S1: `bootloader/install` and `bootloader/release` (#1090, PL-06, PL-03)

| Item | Driver and case | Unfixed: command, then the line it prints | Fixed: command, then the line it prints |
| --- | --- | --- | --- |
| #1090 | `s1/install-case.sh` `missing-syslinux` | `bash $S/s1/install-case.sh $U/projects/ROCKNIX/bootloader/install unfixed missing-syslinux` -> `install-case missing-syslinux: unfixed-expectation-met (rc=0 returned=yes completed=yes named=yes copied=no)` | `bash $S/s1/install-case.sh projects/ROCKNIX/bootloader/install fixed missing-syslinux` -> `install-case missing-syslinux: fixed-expectation-met (rc=1 returned=no completed=no named=yes copied=no)` |
| #1090 | `s1/release-case.sh` `unwritable` | `... $U/projects/ROCKNIX/bootloader/release unfixed unwritable` -> `release-case unwritable: unfixed-expectation-met (rc=0 carried-on=yes sourced-rc=1 copied=no)` | `... projects/ROCKNIX/bootloader/release fixed unwritable` -> `release-case unwritable: fixed-expectation-met (rc=1 carried-on=no sourced-rc=none copied=no)` |
| #1090 | `s1/release-case.sh` `empty` | `... unfixed empty` -> `release-case empty: unfixed-expectation-met (rc=0 carried-on=yes sourced-rc=1 copied=no)` | `... fixed empty` -> `release-case empty: fixed-expectation-met (rc=1 carried-on=no sourced-rc=none copied=no)` |
| PL-06 | `s1/install-case.sh` `grub` | `... install unfixed grub` -> `install-case grub: unfixed-expectation-met (rc=0 returned=yes completed=yes named=yes copied=yes)` | `... install fixed grub` -> `install-case grub: fixed-expectation-met (rc=1 returned=no completed=no named=yes copied=no)` |
| PL-06 | `s1/bootloaders.sh` | -- (a guard, not a positive) | `bash $S/s1/bootloaders.sh . HEAD` -> `bootloaders: every value kept (15 devices at HEAD)` |
| control | `s1/install-case.sh` `present-syslinux` | `... install unfixed present-syslinux` -> `install-case present-syslinux: unfixed-expectation-met (rc=0 returned=yes completed=yes named=yes copied=yes)` | `... install fixed present-syslinux` -> `install-case present-syslinux: fixed-expectation-met (rc=0 returned=yes completed=yes named=yes copied=yes)` |
| control | `s1/release-case.sh` `normal` | `... release unfixed normal` -> `release-case normal: unfixed-expectation-met (rc=0 carried-on=yes sourced-rc=0 copied=yes)` | `... release fixed normal` -> `release-case normal: fixed-expectation-met (rc=0 carried-on=yes sourced-rc=0 copied=yes)` |
| control | `s1/kept-loaders.sh` | `bash $S/s1/kept-loaders.sh $U/projects/ROCKNIX/bootloader/install unfixed` -> `kept-loaders: unfixed-expectation-met (u-boot=ok qcom-abl=ok arm-efi=ok)` | `bash $S/s1/kept-loaders.sh projects/ROCKNIX/bootloader/install fixed` -> `kept-loaders: fixed-expectation-met (u-boot=ok qcom-abl=ok arm-efi=ok)` |
| PL-03 | `sed -n 2p` | `# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)` | `# Copyright (C) 2026-present pixelelated (https://github.com/pixelelated)` |

`release-case`'s *sourced-rc* is what `.` returned, which `scripts/image` never reads. The defect is that the image step carried on (`carried-on=yes`), not the sourced status.

## S2: the launcher (#1089)

The driver is `s2/launcher-case.py`, run as `python3 -I -B $S/s2/launcher-case.py <launcher> <side> <case>`, with `<launcher>` = `$U/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm` (unfixed) or `projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm` (fixed). It needs `qemu-img` and the host's OVMF pair. QEMU itself is a stub that refuses to run, and `pgrep -x qemu-system-x86` is read before and after every case.

| Item | Case | Unfixed: the line it prints | Fixed: the line it prints |
| --- | --- | --- | --- |
| #1089 | `pidfile-symlink` | `launcher-case pidfile-symlink: unfixed-expectation-met (rc=0 prints-target=yes refused-naming-link=no qemu-before=0 qemu-after=0)` | `launcher-case pidfile-symlink: fixed-expectation-met (rc=1 prints-target=no refused-naming-link=yes qemu-before=0 qemu-after=0)` |
| #1089 | `socket-swap` | `launcher-case socket-swap: unfixed-expectation-met (raised=no path-present=no live-answers=no ...)` | `launcher-case socket-swap: fixed-expectation-met (raised=yes path-present=yes live-answers=yes ...)` |
| #1089 | `same-paths` | `launcher-case same-paths: unfixed-expectation-met (rc=0 both-in-command=yes ...)` | `launcher-case same-paths: fixed-expectation-met (rc=1 both-in-command=no ...)` |
| control | `pidfile-regular` | `... unfixed-expectation-met (rc=0 prints-path=yes ...)` | `... fixed-expectation-met (rc=0 prints-path=yes ...)` |
| control | `socket-dead` | `... unfixed-expectation-met (raised=no path-present=no ...)` | the same, `fixed-expectation-met` |
| control | `socket-symlink`, `socket-notsock`, `socket-live` | each `unfixed-expectation-met (raised=yes path-present=yes ...)` | each `fixed-expectation-met (raised=yes path-present=yes ...)` |

## S3: the modeswitch rule and `options` (#1087, PL-10)

| Item | Driver | Unfixed: command, then the line it prints | Fixed: command, then the line it prints |
| --- | --- | --- | --- |
| #1087 | `s3/modeswitch-case.sh` | `bash $S/s3/modeswitch-case.sh $U/projects/ROCKNIX/packages/linux/udev.d/40-usb_modeswitch.rules unfixed` -> `modeswitch-case: unfixed-expectation-met (verify-rc=0 usb1=eject 1-0:1.0=eject)` | `bash $S/s3/modeswitch-case.sh projects/ROCKNIX/packages/linux/udev.d/40-usb_modeswitch.rules fixed` -> `modeswitch-case: fixed-expectation-met (verify-rc=0 usb1=none 1-0:1.0=none)` |
| PL-10 | `s3/options-comment.sh` | `bash $S/s3/options-comment.sh $U/projects/ROCKNIX/devices/GENERIC_X64/options unfixed` -> `options-comment: unfixed-expectation-met (why-named=no)` | `bash $S/s3/options-comment.sh projects/ROCKNIX/devices/GENERIC_X64/options fixed` -> `options-comment: fixed-expectation-met (why-named=yes)` |

`modeswitch-case` needs `udevadm` (udev 259 here) and the host's USB root hub `usb1` (`1d6b:0002`) with its interface `1-0:1.0`. It runs udev's matcher (`udevadm test`, which simulates and runs no `RUN` program) over a copy of the rule with line 7's IDs, and only those, swapped for the hub's. That is a synthetic input, named. The host has no `0cf3:20ff` dongle, no `umockdev` and no USB block device, so the fixed rule's firing on a block child is not shown.

## S4: `dtb_overlay` (#1088)

The driver is `s4/dtb-overlay-case.sh <dtb_overlay> <side> <case>`, with `<dtb_overlay>` = `$U/projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/sources/dtb_overlay` (unfixed) or `projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/sources/dtb_overlay` (fixed). It runs the script under bash (the image's `/bin/sh`), inside `bwrap` with a tmpfs root that holds a fixture `/flash`, a stub `/etc/profile.d/001-functions` (settings in `/state`) and a `mount` stub.

| Item | Case | Unfixed: the line it prints | Fixed: the line it prints |
| --- | --- | --- | --- |
| #1088 | `remount-fail` | `dtb-overlay-case remount-fail: unfixed-expectation-met (rc=0 setting=(unset)->driver-gpu-panthor.dtbo testerr=no)` | `dtb-overlay-case remount-fail: fixed-expectation-met (rc=1 setting=(unset)->(unset) testerr=no)` |
| #1088 | `none-clear` | `... none-clear: unfixed-expectation-met (rc=1 setting=driver-gpu-panthor.dtbo->driver-gpu-panthor.dtbo ...)` | `... none-clear: fixed-expectation-met (rc=0 setting=driver-gpu-panthor.dtbo->None ...)` |
| #1088 | `spaced-arg` | `... spaced-arg: unfixed-expectation-met (rc=1 ... testerr=yes)` | `... spaced-arg: fixed-expectation-met (rc=1 ... testerr=no)` |
| #1088 | `empty-arg` | `... empty-arg: unfixed-expectation-met (rc=1 ... testerr=yes)` | `... empty-arg: fixed-expectation-met (rc=1 ... testerr=no)` |
| #1088 | `dash-arg` | `... dash-arg: unfixed-expectation-met (rc=1 ... testerr=no)`: under bash, `[ -o = None ]` is a comparison, not an operator | `... dash-arg: fixed-expectation-met (rc=1 ... testerr=no)` |
| control | `normal` | `... normal: unfixed-expectation-met (rc=0 setting=(unset)->driver-gpu-panthor.dtbo ...)` | the same, `fixed-expectation-met` |

## Everything at once

`bash $S/run-all.sh $U "$PWD"` runs every row above, on both sides, and ends with `run-all: 47 rows, 0 unexpected, 0 could not run` (exit 0) at `0c32b2bac6`.
