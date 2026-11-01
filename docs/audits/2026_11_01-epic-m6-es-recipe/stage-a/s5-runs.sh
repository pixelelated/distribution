#!/bin/bash
# T37 (#684) stage A: the brief's section 5 runs, each wrapped in its own rc and a date +%s pair.
# Run from the distribution worktree. Changes from the brief's block, each recorded in 02:
#  - every read of the ES recipe also withholds :39 by line number (W39), because the mask M leaves
#    :39 unchanged (len 40, masked-differs=no, read at stage A);
#  - the candidate-provenance line under /workspace/repos/rocknix is not run (open item 16, the dispatch:
#    M7's; R3 section 2.3 and cmd 21 are cited instead);
#  - the stage-C checker line is not run (the checker does not exist at stage A);
#  - the removal check runs with the pointer's TIP-HASH filled: 94d8ef8e7e.
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684 || exit 2
export LC_ALL=C; G=/usr/bin/grep; P1=2174265e9c; MB=c445081a59; UN=651150fc88; U=projects/ROCKNIX/packages/ui/; E=${U}emulationstation/package.mk
Q=/home/max/Development/emulationstation-next.worktrees/qa-integration; PIN=16dbac5211eea7e70db7394372033be2be7df829
export TMPDIR=/workspace/tmp/m6-t37/tmp; mkdir -p "$TMPDIR/home"; df -i /workspace | tail -n 1
M='s/((token|key|pass(w[a-z]*)?|psk|user|login|devid|apikey) *[=:] *)[^ "]*/\1***/Ig'
W39='39s/.*/[:39 withheld]/'
X=/workspace/tmp/m6-t37/export
O=/workspace/tmp/m6-t37/stage-a/runs; mkdir -p "$O"
n=0
begin() { n=$((n+1)); R=$(printf 'R%02d' "$n"); echo; echo "## $R $1"; s=$(date +%s); }
end() { e=$(date +%s); echo "[$R] rc=$1 wall=$((e-s))s"; }

begin "scope: ls-tree of ui/ at P1, and paths.txt (expect 19, 15)"
git ls-tree -r --name-only "$P1" -- "$U" > "$O/$R.a"; rc=$?
wc -l < "$O/$R.a"; wc -l < .qa-scratch/t37/paths.txt
end $rc

begin "lines two ways (expect wc -l 19: 4649; grep -c 19: 4650; grep -c 15: 4561)"
for p in $(cat "$O/R01.a"); do git show "$P1:$p" | wc -l; done > "$O/$R.wc"; rc=$?
awk '{s+=$1} END {print "wc -l 19:", s}' "$O/$R.wc"
for p in $(cat "$O/R01.a"); do git show "$P1:$p" | $G -c ''; done > "$O/$R.gc"
awk '{s+=$1} END {print "grep -c 19:", s}' "$O/$R.gc"
for p in $(cat .qa-scratch/t37/paths.txt); do git show "$P1:$p" | $G -c ''; done > "$O/$R.gc15"
awk '{s+=$1} END {print "grep -c 15:", s}' "$O/$R.gc15"
for p in $($G -F -v -x -f .qa-scratch/t37/paths.txt "$O/R01.a"); do git show "$P1:$p" | $G -c ''; done > "$O/$R.gc4"
awk '{s+=$1} END {print "grep -c the four patches:", s, "files:", NR}' "$O/$R.gc4"
end $rc

begin "next against the tip on ui/ (expect no line)"
git diff --stat 8ebaf8daad "$P1" -- "$U" > "$O/$R.out"; rc=$?
tail -n 1 "$O/$R.out"; echo "lines=$(wc -l < "$O/$R.out")"
end $rc

begin "the fork's delta (expect 8 files changed, 463 insertions(+), 13 deletions(-); 251; 5; 246)"
git diff --shortstat "$MB" "$P1" -- "$U"; rc=$?
git log --oneline "$MB..$P1" -- "$U" | wc -l; git log --oneline --merges "$MB..$P1" -- "$U" | wc -l; git rev-list --count --no-merges "$MB..$P1" -- "$U"
git rev-list --no-merges "$MB..$P1" -- "$E" | wc -l
end $rc

begin "upstream's delta (expect 16; 8 files changed, 72 insertions(+), 75 deletions(-); 14 files changed, 83 insertions(+), 536 deletions(-); the name-status)"
git rev-list --count "$MB..$UN" -- "$U"; rc=$?
git diff --shortstat "$MB" "$UN" -- "$U"; git diff --shortstat "$P1" "$UN" -- "$U"; git diff --name-status "$MB" "$UN" -- "$U"
end $rc

begin "the 14 files by side (expect upstream-only 6 fork-only 6 both 2)"
up() { git diff --name-only "$MB" "$UN" -- "$U" | sort; }; fk() { git diff --name-only "$MB" "$P1" -- "$U" | sort; }
echo "upstream-only $(comm -23 <(up) <(fk) | $G -c '') fork-only $(comm -13 <(up) <(fk) | $G -c '') both $(comm -12 <(up) <(fk) | $G -c '')"; rc=$?
echo "both:"; comm -12 <(up) <(fk)
end $rc

begin "the three recipes' pins at MB, UN and P1"
for f in emulationstation lowerdeck themes/es-theme-art-book-next; do for h in "$MB" "$UN" "$P1"; do echo "$f @ $h: $(git show "$h:$U$f/package.mk" | $G -E '^PKG_(VERSION|SITE|GIT_CLONE_BRANCH)=' | tr '\n' ' ')"; done; done; rc=$?
end $rc

begin "the ES side by hash (expect 14; 724; cada856d86...; the pin for both refs)"
git -C "$Q" rev-list --count "$PIN..rocknix/master"; rc=$?
git -C "$Q" rev-list --count "rocknix/master..$PIN"; git -C "$Q" merge-base "$PIN" rocknix/master
git -C "$Q" rev-parse --short=10 test/qa-integration 2>&1; git -C "$Q" rev-parse --short=10 origin/test/qa-integration 2>&1
git -C "$Q" rev-list --count --first-parent --merges "$PIN..rocknix/master"
end $rc

begin "what the define selects, by hash (GLES3 lines; es-core 278-283)"
git -C "$Q" show "$PIN:CMakeLists.txt" > "$O/$R.cm"; rc=$?
$G -n -E 'GLES3|OPENGLES_30|GLSystem' "$O/$R.cm"; git -C "$Q" show "$PIN:es-core/CMakeLists.txt" | sed -n '278,283p'
end $rc

begin "FRIBIDI at 230-244; the build names at 303-330 through the mask; HFS_DEV_LOGIN's readers"
sed -n '230,244p' "$O/R09.cm"; rc=$?
sed -n '303,330p' "$O/R09.cm" | sed -E "$M"
git -C "$Q" grep -n -o HFS_DEV_LOGIN "$PIN" -- es-app/src
end $rc

begin "syntax: bash -n on the seven (expect rc=0 each)"
rcs=0
for p in emulationstation/package.mk lowerdeck/package.mk themes/es-theme-art-book-next/package.mk emulationstation/sources/es_settings emulationstation/sources/start_es.sh emulationstation/sources/serial_number_check emulationstation/autostart/001-emulationstation; do git show "$P1:$U$p" > "$TMPDIR/one" || echo "SHOW FAILED $p"; [ -s "$TMPDIR/one" ] || echo "EMPTY $p"; bash -n "$TMPDIR/one"; rc=$?
echo "rc=$rc $p"; rcs=$((rcs+rc)); done
rm -f "$TMPDIR/one"
end $rcs

begin "pkgcheck by name, positive first, control last"
rcs=0
for nm in emulationstation es-theme-art-book-next lowerdeck es-theme-no-such-package; do echo "find $nm: $(find packages projects -type f -path "*/$nm/package.mk" | tr '\n' ' ')"; tools/pkgcheck "$nm" > "$TMPDIR/pk" 2>&1; rc=$?
echo "pkgcheck $nm rc=$rc lines=$(wc -l < "$TMPDIR/pk") FAIL-lines=$($G -c 'FAIL' "$TMPDIR/pk") WARN-lines=$($G -c 'WARN' "$TMPDIR/pk")"; rcs=$((rcs+rc)); done
tools/pkgcheck emulationstation 2>/dev/null > "$TMPDIR/pk.out"; echo "stdout lines for emulationstation: $(wc -l < "$TMPDIR/pk.out")"
rm -f "$TMPDIR/pk" "$TMPDIR/pk.out"
end $rcs

begin "the scratch export, ruling (k) (expect export rc=0, the tip, worktree build roots: 0)"
[ -e "$X" ] && echo "STOP: $X exists before the export" && exit 3
mkdir -p "$X"; git rev-parse HEAD > "$TMPDIR/export-tip"
( set -o pipefail; git -C "$PWD" archive HEAD | tar -x -C "$X" ); rc=$?
echo "export rc=$rc tip=$(cat "$TMPDIR/export-tip") path=$X worktree build roots: $(ls -d build.* 2>/dev/null | wc -l)"
echo "export files: $(find "$X" -type f | wc -l) git-in-export: $(ls -d "$X/.git" 2>/dev/null | wc -l)"
end $rc

begin "effective fields, GENERIC_X64, in the export (named fields only; masked)"
test -e "$X/.rocknix/options" && echo "STOP: a .rocknix/options in the export" && exit 3
rcs=0
for nm in emulationstation es-theme-art-book-next lowerdeck; do env -i HOME="$TMPDIR/home" PATH=/usr/bin:/bin PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64 bash -c 'cd "$2" || exit 2; . config/options "$1" >/dev/null 2>&1; rc=$?
echo "source rc=$rc $1"; for v in PKG_VERSION PKG_URL PKG_SHA256 PKG_DEPENDS_TARGET PKG_CMAKE_OPTS_TARGET PKG_TOOLCHAIN PKG_NEED_UNPACK PKG_BUILD_FLAGS PKG_PATCH_DIRS PKG_ARCH TARGET_ARCH BASE_ONLY BATTERYPLUS_SUPPORT VULKAN_SUPPORT EMULATION_DEVICE; do printf "%s=%s\n" "$v" "${!v}"; done; printf "STAMP=%s\n" "$(calculate_stamp)"' _ "$nm" "$X" > "$TMPDIR/ef" 2>&1; rc=$?
sed -E "$M" "$TMPDIR/ef"; echo "[call rc=$rc]"; rcs=$((rcs+rc)); done
rm -f "$TMPDIR/ef"
end $rcs

begin "the call's writes, named (expect the two cache files in the export; 0 build roots in the worktree)"
ls -l "$X"/build.*/.cache_package_local "$X"/build.*/.cache_package_global; rc=$?
ls -d "$X"/build.* ; echo "worktree build roots: $(ls -d build.* 2>/dev/null | wc -l)"
end $rc

begin "the patch reach, GENERIC_X64 and H700, in the export (scripts/unpack:127-159's rule)"
rcs=0
for dv in GENERIC_X64:x86_64 H700:aarch64; do for nm in emulationstation es-theme-art-book-next lowerdeck; do env -i HOME="$TMPDIR/home" PATH=/usr/bin:/bin PROJECT=ROCKNIX DEVICE="${dv%%:*}" ARCH="${dv##*:}" bash -c 'cd "$2" || exit 2; . config/options "$1" >/dev/null 2>&1 || { echo "source FAILED $1"; exit 2; }
if [ "${TARGET_ARCH}" = "x86_64" ]; then PATCH_ARCH="x86"; elif [ "${PKG_IS_KERNEL_PKG}" = "yes" ]; then PATCH_ARCH="${TARGET_KERNEL_PATCH_ARCH:-${TARGET_ARCH}}"; else PATCH_ARCH="${TARGET_PATCH_ARCH:-${TARGET_ARCH}}"; fi
reach="${PKG_DIR}/patches ${PKG_DIR}/patches/${PATCH_ARCH} ${PKG_DIR}/patches/${PKG_VERSION} ${PKG_DIR}/patches/${PKG_VERSION}/${PATCH_ARCH} ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME} ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${PATCH_ARCH} ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${PKG_VERSION} ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}"
for d in ${PKG_PATCH_DIRS}; do case "$d" in /*) reach+=" $d";; *) reach+=" ${PKG_DIR}/patches/$d ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/$d ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}/$d";; esac; done
dirs=$(find "${PKG_DIR}/patches" -name "*.patch" -printf "%h\n" 2>/dev/null | sort -u)
[ -n "$dirs" ] || echo "${DEVICE}/${TARGET_ARCH}: $1 PATCH_ARCH=${PATCH_ARCH} PKG_PATCH_DIRS=[${PKG_PATCH_DIRS}] -> no patches/ directory with a .patch"
for d in $dirs; do v="NOT REACHED"; for r in $reach; do [ "$r" = "$d" ] && v="REACHED"; done; echo "${DEVICE}/${TARGET_ARCH}: $1 PATCH_ARCH=${PATCH_ARCH} PKG_PATCH_DIRS=[${PKG_PATCH_DIRS}] -> ${d#${PKG_DIR}/}/: $v"; done
for r in ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME} ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}; do [ -d "$r" ] && echo "${DEVICE}: $1 project-side patch dir present: ${r#$2/}"; done; true' _ "$nm" "$X"; rc=$?
rcs=$((rcs+rc)); done; done
end $rcs

begin "the install text (masked, :39 withheld)"
git show "$P1:$E" | sed "$W39" | $G -n -E 'ln -sf? |rm -f|\|\| true|^PKG_NEED_UNPACK=|PKG_PATCH_DIRS' | sed -E "$M" > "$O/$R.out"; rc=$?
cat "$O/$R.out"
end $rc

begin "the credential names, names and line numbers only (expect count lines: 5)"
git show "$P1:$E" | $G -c -E 'SCREENSCRAPER_RUNTIME_DEV_LOGIN|SCREENSCRAPER_DEV_LOGIN|CHEEVOS_DEV_LOGIN|GAMESDB_APIKEY|HFS_DEV_LOGIN' > "$O/$R.c"; rc=$?
echo "count lines: $(cat "$O/$R.c")"
git show "$P1:$E" | $G -n -o -E 'SCREENSCRAPER_RUNTIME_DEV_LOGIN|SCREENSCRAPER_DEV_LOGIN|CHEEVOS_DEV_LOGIN|GAMESDB_APIKEY|HFS_DEV_LOGIN'
end $rc

begin "ARMSX2 and vulkan in the catalog (expect armsx2 at 1331 1333 1393; 15 vulkan lines)"
git show "$P1:${U}emulationstation/config/common/es_features.cfg" > "$O/$R.cfg"; rc=$?
$G -n -i armsx2 "$O/$R.cfg" | cut -d: -f1 | tr '\n' ' '; echo; $G -c -i vulkan "$O/$R.cfg"
rm -f "$O/$R.cfg"
end $rc

begin "the text checks over the 15, after planted positives"
. .githooks/secret-patterns
printf '' | $G -E -e "$SECRET_PATTERNS" >/dev/null 2>&1; crc=$?
echo "secret-patterns compile rc=$crc (at most 1 compiles)"
planted="$(printf -- '-----BEGIN %s-----' 'OPENSSH PRIVATE KEY')"
echo "planted secret positive: $(printf '%s\n' "$planted" | $G -c -E -e "$SECRET_PATTERNS") plain: $(printf '%s\n' 'a plain line' | $G -c -E -e "$SECRET_PATTERNS")"
pna="$(printf 'x\xc3\xa9x')"; echo "planted non-ASCII positive: $(printf '%s\n' "$pna" | LC_ALL=C $G -c -P '[^\x00-\x7F]')"
na=0; sp=0
for p in $(cat .qa-scratch/t37/paths.txt); do git show "$P1:$p" > "$TMPDIR/t" || echo "SHOW FAILED $p"; a=$(LC_ALL=C $G -c -P '[^\x00-\x7F]' "$TMPDIR/t"); b=$($G -c -E -e "$SECRET_PATTERNS" "$TMPDIR/t"); echo "non-ascii=$a secret=$b $p"; [ "$a" -gt 0 ] && na=$((na+1)); [ "$b" -gt 0 ] && sp=$((sp+1)); done
echo "NON-ASCII FILES $na SECRET-PATTERN FILES $sp"
for p in $($G -F -v -x -f .qa-scratch/t37/paths.txt "$O/R01.a"); do git show "$P1:$p" > "$TMPDIR/t"; echo "the four: non-ascii=$(LC_ALL=C $G -c -P '[^\x00-\x7F]' "$TMPDIR/t") secret=$($G -c -E -e "$SECRET_PATTERNS" "$TMPDIR/t") $p"; done
rm -f "$TMPDIR/t"
echo "a planted forbidden-term line" | FORBIDDEN_PATTERNS='planted forbidden-term' tools/forbidden-terms-check --stdin; prc=$?
echo "forbidden-terms planted positive (stand-in pattern) rc=$prc"
for p in $(cat .qa-scratch/t37/paths.txt); do git show "$P1:$p"; done | tools/forbidden-terms-check --stdin; rc=$?
echo "forbidden-terms over the 15 rc=$rc"
python3 -B -I -c 'import sys,subprocess,xml.etree.ElementTree as ET
bad=0
for p in sys.argv[1:]:
    b=subprocess.run(["git","show","2174265e9c:"+p],capture_output=True,check=True).stdout
    try: ET.fromstring(b); print("xml ok",p)
    except ET.ParseError as e: bad+=1; print("xml FAIL",p,e)
print("XML FAILS",bad)' $($G -E '\.cfg$' .qa-scratch/t37/paths.txt)
end $rc

begin "freshness --list, both refs given (expect lines=48 ui=0)"
FRESHNESS_BASE="$UN" FRESHNESS_HEAD="$P1" tools/fork-package-freshness --list > "$TMPDIR/fr" 2>&1; rc=$?
echo "freshness --list rc=$rc lines=$(wc -l < "$TMPDIR/fr") ui=$($G -c 'packages/ui/' "$TMPDIR/fr")"
rm -f "$TMPDIR/fr"
end $rc

begin "the removal check against TIP-HASH 94d8ef8e7e (expect no line before stage E)"
git diff --stat 94d8ef8e7e HEAD -- packages projects tools > "$O/$R.out"; rc=$?
tail -n 1 "$O/$R.out"; echo "lines=$(wc -l < "$O/$R.out")"
end $rc

echo; echo "== done $(date -u +%Y-%m-%dT%H:%M:%SZ); worktree build roots: $(ls -d build.* 2>/dev/null | wc -l)"
