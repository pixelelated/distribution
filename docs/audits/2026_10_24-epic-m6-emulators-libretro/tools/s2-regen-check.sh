#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
#
# s2-regen-check.sh -- S2's test (M6 T3, #650): the five launch tables
# regenerated from <tree>, compared with the three images, and every retroarch
# core each table names checked against that image's usr/lib/libretro.
#
#   s2-regen-check.sh <tree> <outdir>
#   XS=<xmlstarlet> s2-regen-check.sh <tree> <outdir>
#
# XS is the build's own host xmlstarlet (regen-es-systems.sh's third
# argument); it defaults to <tree>/.qa-scratch/t3-regen/xs/xml, the copy
# stage B took from the M7 GENERIC_X64 root's toolchain/bin/xml.
#
# A system whose games are .sh files (idtech) is excluded from the core check:
# runemu.sh:488 runs a .sh ROM itself, so its "core" is never loaded.
set -u
TREE=$(cd "$1" && pwd) OUT=$(mkdir -p "$2" && cd "$2" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
XS=${XS:-$TREE/.qa-scratch/t3-regen/xs/xml}
R=/workspace/repos/rocknix.worktrees
declare -A IMG=(
  [GENERIC_X64]=$R/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system
  [H700]=$R/m7-signin-h700-build-20261023-06/build.pixelelated-H700.aarch64/image/system
  [SM8550]=$R/m7-signin-sm8550-build-20261023-03/build.pixelelated-SM8550.aarch64/image/system)
rc_all=0
while read -r dev arch e32 wm gles; do
  rm -rf "$OUT/$dev"
  # env -i, as stage B ran it: mk_es_systems orders the table with ls | sort
  # (functions:106), and the build sorts in the C locale.
  env -i PATH=/usr/bin:/bin "$HERE/regen-es-systems.sh" "$TREE" "$OUT/$dev" "$XS" "$dev" "$arch" "$e32" "$wm" "$gles" > "$OUT/$dev.log" 2>&1
  rc=$?
  t="$OUT/$dev/install/usr/config/emulationstation/es_systems.cfg"
  line="$dev: regen rc=$rc systems=$(grep -c '<system>' "$t" 2>/dev/null)"
  if [ -n "${IMG[$dev]:-}" ]; then
    cmp -s "$t" "${IMG[$dev]}/usr/config/emulationstation/es_systems.cfg" && line+=" image=identical" || line+=" image=DIFFERS"
    miss=$(python3 -I - "$t" "${IMG[$dev]}/usr/lib/libretro" <<'EOF'
import os, sys, xml.etree.ElementTree as ET
t, lib = sys.argv[1:3]
have = {f[:-len("_libretro.so")] for f in os.listdir(lib) if f.endswith("_libretro.so")}
out = []
for s in ET.parse(t).getroot().findall("system"):
    if ".sh" in (s.findtext("extension") or "").split() and len((s.findtext("extension") or "").split()) == 1:
        continue
    for e in s.findall("emulators/emulator"):
        if e.get("name") != "retroarch": continue
        for c in e.findall("cores/core"):
            if c.text not in have: out.append(f"{s.findtext('name')}/{c.text}")
print(len(out), " ".join(out))
EOF
)
    line+=" missing-cores=$miss"
  fi
  echo "$line"
  [ "$rc" -eq 0 ] || rc_all=1
done <<'DEVICES'
GENERIC_X64 x86_64 no swaywm-env no
H700 aarch64 true swaywm-env yes
RK3326 aarch64 true swaywm-env yes
RK3566 aarch64 true swaywm-env yes
SM8550 aarch64 true swaywm-env no
DEVICES
exit $rc_all
