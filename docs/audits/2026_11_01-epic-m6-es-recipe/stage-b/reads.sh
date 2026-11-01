#!/bin/bash
# T37 (#684) stage B: the reads behind 02's rows, each a tool's own line. Read-only (git in the
# worktree and by hash in the ES checkout). Every ES-recipe read withholds :39 (W39) under the mask.
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684 || exit 2
export LC_ALL=C; G=/usr/bin/grep; P1=2174265e9c; MB=c445081a59; UN=651150fc88; U=projects/ROCKNIX/packages/ui/; E=${U}emulationstation/package.mk
Q=/home/max/Development/emulationstation-next.worktrees/qa-integration; PIN=16dbac5211eea7e70db7394372033be2be7df829
M='s/((token|key|pass(w[a-z]*)?|psk|user|login|devid|apikey) *[=:] *)[^ "]*/\1***/Ig'; W39='39s/.*/[:39 withheld]/'
n=0; begin() { n=$((n+1)); R=$(printf 'B%02d' "$n"); echo; echo "## $R $1"; }
begin "L-02 intent: the patch's addition (git log --diff-filter=A) and -S cpugov"
git log --format='%h %ad %s' --date=short --diff-filter=A "$P1" -- ${U}emulationstation/patches/x86_64/cpugov.patch; echo "rc=$?"
echo "-S cpugov commits: $(git log --format=%h -S cpugov "$P1" -- ${U}emulationstation | wc -l)"
echo "PKG_PATCH_DIRS outside recipes (scripts, config): $(git grep -n 'PKG_PATCH_DIRS' "$P1" -- scripts config | wc -l) lines: $(git grep -n 'PKG_PATCH_DIRS' "$P1" -- scripts config | cut -d: -f2,3 | tr '\n' ' ')"
git show "$P1:${U}emulationstation/patches/x86_64/cpugov.patch" | $G -n -E '^@@' 
begin "L-03 intent: -S for the device-path form, and the link's line history"
echo "-S 'ln -sf /usr/config/emulationstation/es_systems.cfg' commits: $(git log --format=%h -S'ln -sf /usr/config/emulationstation/es_systems.cfg' "$P1" | wc -l)"
for h in "$MB" "$UN"; do echo "$h: $(git show "$h:$E" | $G -n 'es_systems.cfg ${INSTALL}/etc' )"; done
echo "who installs /usr/config/emulationstation/es_systems.cfg (lines naming it, outside ui/):"; git grep -n -E 'usr/config/emulationstation/es_systems\.cfg|es_systems\.cfg' "$P1" -- projects packages ':!projects/ROCKNIX/packages/ui' | cut -c1-200 | head -8
begin "L-04 intent: -S logo.png over the recipe; the pin's resources/logo.png"
git log --format='%h %ad %s' --date=short -S'logo.png' "$P1" -- "$E"
echo "pin resources/logo.png: $(git -C "$Q" cat-file -t "$PIN:resources/logo.png" 2>&1)"
echo "pin readers of logo.png (es-app, es-core): $(git -C "$Q" grep -n -l 'logo.png' "$PIN" -- es-app/src es-core/src | tr '\n' ' ')"
begin "L-07 intent: -S localedef over the recipe"
git log --format='%h %ad %s' --date=short -S'localedef --force' "$P1" -- "$E"
for h in "$MB" "$UN"; do echo "$h localedef lines: $(git show "$h:$E" | $G -c 'localedef')"; done
begin "L-08: the catalog step and the pin's locale CMake"
git show "$P1:$E" | sed "$W39" | sed -n '67,68p' | sed -E "$M"
git -C "$Q" show "$PIN:locale/CMakeLists.txt" | awk 'NR==9||NR==25||NR==31 {printf "locale/CMakeLists.txt:%d: %s\n", NR, $0}'
echo "pin French catalog: $(git -C "$Q" cat-file -t "$PIN:locale/lang/fr/LC_MESSAGES/emulationstation2.po" 2>&1)"
begin "L-16: the licence line's history"
git log --format='%h %ad %s' --date=short -L7,7:"$E" "$P1" | $G -E '^[0-9a-f]{10} ' 
git log -L7,7:"$E" "$P1" | $G -E '^[-+]PKG_LICENSE'
begin "L-19: PKG_NEED_UNPACK and where scripts read it"
for h in "$MB" "$UN" "$P1"; do echo "$h: $(git show "$h:$E" | $G -n '^PKG_NEED_UNPACK=')"; done
echo "scripts/ readers: $(git grep -n 'PKG_NEED_UNPACK' "$P1" -- scripts | wc -l)"; git grep -n 'PKG_NEED_UNPACK' "$P1" -- config | cut -c1-160
git log --format='%h %ad %s' --date=short -S'PKG_NEED_UNPACK' "$P1" -- "$E"
echo "find -L busybox from the root finds: $(cd /workspace/tmp/m6-t37/export && find -L busybox -type f 2>/dev/null | wc -l) (the package's directory: $(git ls-tree -d --name-only "$P1" -- packages/sysutils/busybox projects/ROCKNIX/packages/sysutils/busybox | tr '\n' ' '))"
begin "L-06: the sed"
echo a-b-c | sed "s#-#_##g"; echo "device names with a hyphen: $(ls /workspace/tmp/m6-t37/export/projects/ROCKNIX/devices | $G -c -- -)"
for h in "$MB" "$UN"; do echo "$h: $(git show "$h:$E" | $G -n 's#-#_##g')"; done
begin "L-05: the log loop's names and the forwarded four"
git show "$P1:$E" | sed "$W39" | sed -n '42,44p' | sed -E "$M"
git show "$P1:scripts/get_env" | sed -n '14,15p' | sed -E "$M"
begin "L-20: the default theme at the pin"
git -C "$Q" show "$PIN:es-core/src/Settings.cpp" | $G -n '"ThemeSet"'
git -C "$Q" show "$PIN:es-app/src/CollectionSystemManager.cpp" | sed -n '1360,1366p'
begin "#1193: the four seeds' git modes and the install step"
git ls-tree "$P1" -- ${U}emulationstation/config/common/ | awk '{print $1, $4}'
git show "$P1:$E" | sed "$W39" | sed -n '77,78p'
begin "PL-029: start_es.sh:8, its sibling, and the pin's log path"
git show "$P1:${U}emulationstation/sources/start_es.sh" | sed -n '8p'; git show "$P1:${U}emulationstation/system.d/emustation.service" | sed -n '12p'
echo "pin main.cpp lines naming log-path: $(git -C "$Q" show "$PIN:es-app/src/main.cpp" | $G -c 'log-path')"
git -C "$Q" show "$PIN:es-core/src/Paths.cpp" | awk 'NR>=76 && NR<=81 {printf "Paths.cpp:%d: %s\n", NR, $0}'
for h in "$MB" "$UN"; do echo "$h start_es.sh: $(git show "$h:${U}emulationstation/sources/start_es.sh" | $G -n 'emulationstation ')"; done
begin "L-01: the tip's catalogue count of armsx2-sa vulkan driver features (the fixture's half without xmlstarlet)"
git show "$P1:${U}emulationstation/config/common/es_features.cfg" | python3 -B -I -c 'import sys,xml.etree.ElementTree as ET
r=ET.fromstring(sys.stdin.read()); n=sum(1 for c in r.iter("core") if c.get("name")=="armsx2-sa" for f in c.iter("feature") if f.get("name")=="vulkan driver")
print("tip armsx2-sa vulkan driver features:", n)'
echo "armsx2-sa's devices (virtual/emulators):"; git show "$P1:projects/ROCKNIX/packages/virtual/emulators/package.mk" | $G -n 'armsx2' | cut -c1-140
begin "the register rows section 9 names, at HEAD"
for id in D-WORKFLOW-012 D-WORKFLOW-024 D-WORKFLOW-162 D-WORKFLOW-164 D-WORKFLOW-165 D-WORKFLOW-166 D-INFRA-006 D-INFRA-007 D-WORKFLOW-213 D-WORKFLOW-214 D-WORKFLOW-215 D-WORKFLOW-216 D-WORKFLOW-217 D-UI-090 D-WORKFLOW-191 D-WORKFLOW-187 D-WORKFLOW-189 D-WORKFLOW-195 D-WORKFLOW-212 D-WORKFLOW-047 D-WORKFLOW-050 D-UI-079 D-WORKFLOW-144 D-WORKFLOW-145 D-WORKFLOW-146; do printf '%s :%s\n' "$id" "$($G -n -E "^\| ${id} \|" docs/decision-register.md | cut -d: -f1)"; done | tr '\n' ' '; echo
