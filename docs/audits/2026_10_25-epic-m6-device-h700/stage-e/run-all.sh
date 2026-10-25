#!/bin/bash
# T27 stage E: run every S1 case on both sides.
#
#   run-all.sh <unfixed root> <fixed root>
#
# <unfixed root> holds projects/ROCKNIX/devices/H700/bootloader/update.sh at
# the stage-D tip 70df17982c (README.md's shared clone); <fixed root> is this
# branch's worktree at fixed-at. Exits 0 when every verdict is an expectation
# met, 1 otherwise, 2 when a case cannot run. Writes only under $TMPDIR.
set -u
U=${1:?unfixed root}; F=${2:?fixed root}
S=$(cd "$(dirname "$0")" && pwd)
: "${TMPDIR:?set TMPDIR to a scratch directory}"
P=projects/ROCKNIX/devices/H700/bootloader/update.sh
fail=0; cannot=0; n=0
for c in remount-fail copy-fail dd-fail success ddr3 unknown-voltage; do
  for side in unfixed fixed; do
    root=$U; [ "$side" = fixed ] && root=$F
    out=$(bash "$S/s1/update-case.sh" "$root/$P" "$side" "$c" 2>&1 | tail -1); rc=${PIPESTATUS[0]}
    n=$((n + 1)); echo "$out"
    case "$rc" in 0) ;; 2) cannot=$((cannot + 1)) ;; *) fail=$((fail + 1)) ;; esac
  done
done
echo "run-all: $n rows, $fail unexpected, $cannot could not run"
[ "$cannot" = 0 ] || exit 2
[ "$fail" = 0 ]
