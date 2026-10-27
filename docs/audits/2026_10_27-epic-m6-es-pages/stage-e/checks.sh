#!/bin/bash
# T31 (#678) stage E: the checks every stream runs before its commit, over the ES worktree (T26's checks.sh, adapted).
#   bash checks.sh <label> [<edited .cpp>...]
# The stand-in syntax check (T21's, copied here) over the .cpp files named; the
# non-ASCII check over the comment lines added to C++ sources since the pin (the
# xgettext trap, es-code-traps.md) and any non-ASCII added line by file; the
# unit tests by the lane's generated host build (tools/t31-build-tests.sh, the
# recipe's patched rapidjson; its own TOTAL line); every Python harness under
# tests/ at the worktree; the stage-C harnesses' default runs (the positives);
# the menu-map check at the worktree's HEAD; the French count at both bases.
# One line each, with its rc.
set -uo pipefail
export LC_ALL=C
W=/home/max/Development/emulationstation-next.worktrees/m6-es-pages-678; PIN=16dbac5211eea7e70db7394372033be2be7df829
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-pages-678; H=$(cd "$(dirname "$0")" && pwd); C=$H/../stage-c
export TMPDIR=/workspace/tmp/m6-t31/tmp
export PUGIXML_INCLUDE_DIR=/workspace/cache/rocknix-sources/emulationstation/emulationstation-${PIN}/external
export RAPIDJSON_INCLUDE_DIR=/workspace/tmp/m6-t31/rapidjson/rapidjson-1.1.0/include
label=${1:-}; shift || true
echo "== checks: ${label} ($(date -u +%H:%M:%SZ)), ES HEAD $(git -C "$W" rev-parse --short=10 HEAD), worktree changes $(git -C "$W" status --short | wc -l)"
# GuiMoonlight.cpp includes <pugixml.hpp> bare where ThemeData.h includes pugixml/src/pugixml.hpp (S3): the bare one by CPATH.
[ $# -gt 0 ] && { CPATH="$PUGIXML_INCLUDE_DIR/pugixml/src" bash "$H/syntax-check.sh" "$W" "$@"; echo "syntax-check rc $?"; }
B=/workspace/tmp/m6-t31/build-unit; out=$(bash "$H/../tools/t31-build-tests.sh" "$W" "$B" 2>&1); rc=$?; printf '%s\n' "$out" | grep -E "^(RUN|BUILD FAIL|TOTAL)"; echo "t31-build-tests rc $rc"
n=$(git -C "$W" diff "$PIN" -- '*.cpp' '*.h' | grep -E '^\+' | grep -v '^+++' | grep -c -P '(//|/\*|^\+\s*\*).*[^\x00-\x7F]'); echo "non-ASCII added comment lines in C++ sources: $n"
for f in $(git -C "$W" diff "$PIN" --name-only); do c=$(git -C "$W" diff "$PIN" -- "$f" | grep -E '^\+' | grep -v '^+++' | grep -c -P '[^\x00-\x7F]'); [ "$c" -gt 0 ] && echo "  non-ASCII added lines (any kind) in $f: $c"; done
for t in $( { git -C "$W" ls-files -- 'tests/*.py'; git -C "$W" ls-files --others --exclude-standard -- 'tests/*.py'; } | grep -E '^tests/[^/]+\.py$' | sort -u | sed -e 's#^tests/##' -e 's/\.py$//'); do
  out=$(cd "$W" && timeout 600 python3 -I "tests/$t.py" 2>&1); rc=$?
  printf '%s rc=%s: %s\n' "$t" "$rc" "$(printf '%s\n' "$out" | tail -n 1 | cut -c1-140)"
done
G=$W/es-app/src/guis
# From S3 on, Moonlight's positive is s03-moonlight.py, which compiles the whole page and runs it:
# l05-l06 reads the pin's snprintf and tilde shapes, which S3 removes, and stays the pin's record (D-WORKFLOW-210).
for h in "l01-start-drops.py $G/GuiSettings.cpp" "l02-led-not-saved.py $G/GuiAnalogSticksLedControls.cpp $G/GuiSettings.cpp" "s03-moonlight.py $W" "s04-copy-press.py $G/GuiSaveState.cpp" "s10-viewer-guard.py $G/GuiImageViewer.cpp" "s12-scrape-filters.py $G/GuiScraperStart.cpp" "l09-l10-scrape-page.py $G/GuiScraperRun.cpp" "l22-guiloading-race.py $G/GuiLoading.h"; do
  out=$(python3 -I $C/$h 2>&1); rc=$?
  printf 'stage-c/%s rc=%s: %s\n' "${h%% *}" "$rc" "$(printf '%s\n' "$out" | grep -v -E '^\s+#' | tail -n 1 | cut -c1-140)"
done
# From S4 on, tests/app-unit's bookkeeper-tests (the host has no cmake; the lane's script reads its CMake block).
out=$(bash "$H/../tools/t31-bookkeeper-tests.sh" "$W" /workspace/tmp/m6-t31/bk-build 2>&1); rc=$?; printf '%s\n' "$out" | grep -E '^\[doctest\] test cases|^BUILD FAIL'; echo "t31-bookkeeper-tests rc $rc"
out=$(cd "$D" && tools/es-menu-map-check --es-src "$W" --ref "$(git -C "$W" rev-parse HEAD)" 2>&1); rc=$?; printf '%s (rc %s)\n' "$(printf '%s\n' "$out" | tail -n 1)" "$rc"
for base in bccd715707 cada856d86; do out=$(cd "$D" && tools/es-untranslated --es-src "$W" --upstream $base 2>&1); rc=$?; printf '%s [%s] (rc %s)\n' "$(printf '%s\n' "$out" | grep -m1 'fork string')" $base "$rc"; done
