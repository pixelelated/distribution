#!/bin/bash
# T23 (#670): resolve package names to the directory a plan would use, per device,
# with config/functions' own get_pkg_directory. No build, no fetch; BUILD_DIR is
# outside the worktree so config/options' package caches land there.
#   resolve.sh <names-file> <out-file>   (run from the worktree root)
# no set -u: config/options reads unset variables by design
names=$1; out=$2; : > "$out"
export BUILD_DIR=/workspace/tmp/m6-t23/plan-build TMPDIR=/workspace/tmp/m6-t23/tmp
for cfg in GENERIC_X64:x86_64 H700:aarch64 SM8550:aarch64; do
  dev=${cfg%%:*}; arch=${cfg#*:}
  ( export PROJECT=ROCKNIX DEVICE=$dev ARCH=$arch
    . config/options "" >/dev/null 2>&1
    while read -r n; do
      [ -n "$n" ] || continue
      d=$( (get_pkg_directory "$n") 2>/dev/null ) || d="ERROR"
      printf '%s %s %s\n' "$dev" "$n" "${d#$PWD/}"
    done < "$names" ) >> "$out"
done
