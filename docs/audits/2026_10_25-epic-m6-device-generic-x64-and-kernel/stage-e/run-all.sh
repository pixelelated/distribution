#!/bin/bash
# T11 stage E: run every positive and control in README.md, on both sides.
#
#   run-all.sh <unfixed root> <fixed root>
#
# <unfixed root> holds the stream files at 499628a049 (README.md's shared
# clone); <fixed root> is this branch's worktree at fixed-at. Each row runs
# its driver against the unfixed file with `unfixed` and against the fixed
# file with `fixed` and prints the driver's verdict line. The bootloader
# guard runs against the fixed root's HEAD. Exits 0 when every verdict is
# an expectation met, 1 otherwise, 2 when a driver cannot run. Writes only
# under $TMPDIR, through the drivers.
set -u
U=${1:?unfixed root}; F=${2:?fixed root}
S=$(cd "$(dirname "$0")" && pwd)
: "${TMPDIR:?set TMPDIR to a scratch directory}"
B=projects/ROCKNIX/bootloader
L=projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm
R=projects/ROCKNIX/packages/linux/udev.d/40-usb_modeswitch.rules
O=projects/ROCKNIX/devices/GENERIC_X64/options
D=projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/sources/dtb_overlay
fail=0; cannot=0; n=0
row() { # <command...>: run one driver, print its last line, count the result
  local out rc
  out=$("$@" 2>&1 | tail -1); rc=${PIPESTATUS[0]}
  n=$((n + 1))
  echo "$out"
  case "$rc" in 0) ;; 2) cannot=$((cannot + 1)) ;; *) fail=$((fail + 1)) ;; esac
}
both() { # <driver runner> <relative file> <case or "">: unfixed then fixed
  local run=$1 rel=$2 c=$3
  row $run "$U/$rel" unfixed $c
  row $run "$F/$rel" fixed $c
}
for c in missing-syslinux grub present-syslinux; do both "bash $S/s1/install-case.sh" "$B/install" "$c"; done
both "bash $S/s1/kept-loaders.sh" "$B/install" ""
for c in unwritable empty normal; do both "bash $S/s1/release-case.sh" "$B/release" "$c"; done
row bash "$S/s1/bootloaders.sh" "$F" HEAD
for c in pidfile-symlink socket-swap same-paths pidfile-regular socket-dead socket-symlink socket-notsock socket-live; do
  both "python3 -I -B $S/s2/launcher-case.py" "$L" "$c"
done
both "bash $S/s3/modeswitch-case.sh" "$R" ""
both "bash $S/s3/options-comment.sh" "$O" ""
for c in remount-fail none-clear spaced-arg empty-arg dash-arg normal; do both "bash $S/s4/dtb-overlay-case.sh" "$D" "$c"; done
echo "run-all: $n rows, $fail unexpected, $cannot could not run"
[ "$cannot" = 0 ] || exit 2
[ "$fail" = 0 ]
