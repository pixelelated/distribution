#!/bin/bash
# E4 (#652, #831, #832): the five devices' launch tables regenerated on the
# host from a tree (regen-es-systems.sh beside this file, T3's, unchanged),
# each copied to <outdir>/<DEVICE>.es_systems.cfg for a diff between trees.
#   sb-es-regen5.sh <tree> <outdir> <xmlstarlet>
# The devices' parameters are T3's (s2-regen-check.sh). env -i, so the table is
# sorted in the C locale as the build sorts it.
set -u
TREE=$(cd "$1" && pwd); OUT=$(mkdir -p "$2" && cd "$2" && pwd); XS=$3; HERE=$(cd "$(dirname "$0")" && pwd)
while read -r dev arch e32 wm gles; do
  env -i PATH=/usr/bin:/bin "$HERE/regen-es-systems.sh" "$TREE" "$OUT/$dev" "$XS" "$dev" "$arch" "$e32" "$wm" "$gles" > "$OUT/$dev.log" 2>&1
  rc=$?
  cp "$OUT/$dev/install/usr/config/emulationstation/es_systems.cfg" "$OUT/$dev.es_systems.cfg" 2>/dev/null
  echo "$dev: rc=$rc systems=$(grep -c '<system>' "$OUT/$dev.es_systems.cfg" 2>/dev/null)"
done <<'DEVICES'
GENERIC_X64 x86_64 no swaywm-env no
H700 aarch64 true swaywm-env yes
RK3326 aarch64 true swaywm-env yes
RK3566 aarch64 true swaywm-env yes
SM8550 aarch64 true swaywm-env no
DEVICES
