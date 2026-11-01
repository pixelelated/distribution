#!/bin/bash
# T37 (#684) stage D: the reads behind the three bugs' traces and PL-05's lowering (read-only git).
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684 || exit 2
G=/usr/bin/grep; P1=2174265e9c
echo "== post-update links into /storage"; git show $P1:projects/ROCKNIX/packages/rocknix/sources/post-update | awk 'NR>=31 && NR<=36 {printf "post-update:%d: %s\n", NR, $0}'
echo "== the shipped theme's XML naming logo.png (files): $($G -r -l 'logo.png' /workspace/tmp/m6-t37/stage-a/l22/xml --include='*.xml' 2>/dev/null | wc -l)"
echo "== the ARMSX2 feature"; git show $P1:projects/ROCKNIX/packages/ui/emulationstation/config/common/es_features.cfg | awk 'NR>=1392 && NR<=1395 {printf "es_features.cfg:%d: %s\n", NR, $0}'
echo "== the launcher's driver choice"; git show $P1:projects/ROCKNIX/packages/emulators/standalone/armsx2-sa/scripts/start_armsx2.sh | awk 'NR==47 || (NR>=213 && NR<=218) {printf "start_armsx2.sh:%d: %s\n", NR, $0}'
echo "== armsx2-sa's Turnip predicate"; git show $P1:projects/ROCKNIX/packages/emulators/standalone/armsx2-sa/package.mk | awk 'NR>=25 && NR<=31 {printf "armsx2-sa/package.mk:%d: %s\n", NR, $0}'
echo "== bare PKG_NEED_UNPACK words over packages/ and projects/: $(git grep -n -E '^PKG_NEED_UNPACK="[a-z]' $P1 -- packages projects | wc -l)"
