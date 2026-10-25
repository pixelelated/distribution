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
