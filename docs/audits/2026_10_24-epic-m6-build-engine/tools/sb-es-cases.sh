#!/bin/bash
# The launch table's constructed cases (#652; T3's F-06 cases A and B, and case C).
#   sb-es-cases.sh <scratch-dir> <xmlstarlet>
# Copies the tree's projects/ROCKNIX/packages, config and distributions into
# <scratch-dir>/fake{A,B,C}, edits the copy (never the tree), and runs
# regen-es-systems.sh (beside this file; T3's, unchanged) for GENERIC_X64.
set -u
D=$(cd "$(dirname "$0")/../../../.." && pwd); SB=$1 XS=$2
P=projects/ROCKNIX/packages/virtual/emulators/package.mk
for c in A B C; do
  mkdir "$SB/fake$c" || exit 2
  mkdir -p "$SB/fake$c/projects/ROCKNIX"
  cp -r "$D/projects/ROCKNIX/packages" "$SB/fake$c/projects/ROCKNIX/packages"
  cp -r "$D/config" "$SB/fake$c/config"; cp -r "$D/distributions" "$SB/fake$c/distributions"; ln -s "$D/packages" "$SB/fake$c/packages"
done
# A: two default lines in one emulator
sed -i 's/^  add_emu_core 3do retroarch opera true$/&\n  add_emu_core 3do retroarch opera_two true/' "$SB/fakeA/$P"
# B: a false core before the true one
sed -i 's/^  add_emu_core bbcmicro retroarch b2 true$/  add_emu_core bbcmicro retroarch first_false false\n&/' "$SB/fakeB/$P"
# C: a system registered after imageviewer whose fragment sets no SYSTEM_COMMAND or SYSTEM_RELEASE
sed -i 's/^  add_es_system imageviewer$/&\n\n  add_emu_core zzfixture retroarch fixture_core true\n  add_es_system zzfixture/' "$SB/fakeC/$P"
printf 'SYSTEM_NAME="zzfixture"\nSYSTEM_FULLNAME="Fixture"\nSYSTEM_MANUFACTURER="Fixture"\nSYSTEM_HARDWARE="Fixture"\nSYSTEM_PATH="/storage/roms/zzfixture"\nSYSTEM_EXTENSION=".zz"\nSYSTEM_PLATFORM="zzfixture"\nSYSTEM_THEME="zzfixture"\n' > "$SB/fakeC/config/emulators/zzfixture.conf"
for c in A B C; do
  env -i PATH=/usr/bin:/bin HOME="$SB" bash -x "$(dirname "$0")/regen-es-systems.sh" "$SB/fake$c" "$SB/out$c" "$XS" GENERIC_X64 x86_64 no swaywm-env no > "$SB/case$c.out" 2> "$SB/case$c.trace"
  echo "case $c rc=$?"
done
