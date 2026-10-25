# T27 stage E: the positives, kept on the branch (#674)

Stream S1's cases (#1095) as commands the acceptance re-run can repeat from this branch. Each positive's expectation fails on the unfixed file and holds on the fixed one. Each control holds on both.

- **The unfixed file** is `projects/ROCKNIX/devices/H700/bootloader/update.sh` at **`70df17982c`** (the stage-D tip), in a shared clone: `git clone -q --no-checkout --shared <this worktree> <U>; git -C <U> checkout -q 70df17982c -- projects/ROCKNIX/devices/H700/bootloader/update.sh`.
- **The fixed file** is this branch's at `fixed-at` (`22c4838f24`).
- **The driver,** `s1/update-case.sh <update.sh> <unfixed|fixed> <case>`, runs the script under bash (the image's `/bin/sh`), inside `bwrap` with a tmpfs root. The root holds fixture versions of `/flash`, `/update/usr/share/bootloader`, `/proc/device-tree/rocknix-dt-id`, a `vdd-dram` regulator under `/sys`, `/storage` and a boot disk image, with stubs for `mount`, `cp` and `dd` first on `PATH` per case. It writes only under `$TMPDIR` and prints one verdict line last. **Nothing runs on a unit.**
- **Everything at once:** `bash stage-e/run-all.sh <U> "$PWD"` prints `run-all: 12 rows, 0 unexpected, 0 could not run` (exit 0).

| Item | Case | Unfixed: the line it prints | Fixed: the line it prints |
| --- | --- | --- | --- |
| #1095 | `remount-fail` | `update-case remount-fail: unfixed-expectation-met (rc=0 dtb.img=old loader=yes ...)` | `update-case remount-fail: fixed-expectation-met (rc=1 dtb.img=old loader=no ... named=yes stray=0)` |
| #1095 | `copy-fail` | `update-case copy-fail: unfixed-expectation-met (rc=0 dtb.img=other(1000B) loader=yes ...)` | `update-case copy-fail: fixed-expectation-met (rc=1 dtb.img=old loader=no ... named=yes stray=0)` |
| #1095 | `dd-fail` | `update-case dd-fail: unfixed-expectation-met (rc=0 dtb.img=new loader=no ...)` | `update-case dd-fail: fixed-expectation-met (rc=1 dtb.img=new loader=no ... named=yes ...)` |
| #1095 | `success` | `update-case success: unfixed-expectation-met (rc=0 dtb.img=new loader=yes ...)` | the same, `fixed-expectation-met` |
| control | `ddr3` | `update-case ddr3: unfixed-expectation-met (rc=0 dtb.img=new ... ddr3-loader=yes ...)` | the same, `fixed-expectation-met` |
| control | `unknown-voltage` | `update-case unknown-voltage: unfixed-expectation-met (rc=0 dtb.img=new ... disk-untouched=yes ...)` | the same, `fixed-expectation-met` |
