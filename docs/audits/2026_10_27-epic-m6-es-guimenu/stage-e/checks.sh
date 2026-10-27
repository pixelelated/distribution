#!/bin/bash
# T26 (#673) stage E: the checks every stream runs before its commit, over the ES worktree.
#   bash checks.sh <label>
# The stand-in syntax check of GuiMenu.cpp (T21's, copied here), the non-ASCII
# check over the lines added since the pin only, every harness under tests/
# (the ten the brief names and the slice's own), the menu-map check at the
# worktree's HEAD and the French count. One line each, with its rc.
set -uo pipefail
export LC_ALL=C
W=/home/max/Development/emulationstation-next.worktrees/m6-es-guimenu-673; PIN=16dbac5211eea7e70db7394372033be2be7df829
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-guimenu-673; H=$(cd "$(dirname "$0")" && pwd)
export TMPDIR=/workspace/tmp/m6-t26/tmp
export PUGIXML_INCLUDE_DIR=/workspace/cache/rocknix-sources/emulationstation/emulationstation-${PIN}/external
export RAPIDJSON_INCLUDE_DIR=/workspace/tmp/m6-t26/rapidjson/rapidjson-1.1.0/include
echo "== checks: ${1:-} ($(date -u +%H:%M:%SZ)), ES HEAD $(git -C "$W" rev-parse --short=10 HEAD), worktree changes $(git -C "$W" status --short | wc -l)"
bash "$H/syntax-check.sh" "$W" es-app/src/guis/GuiMenu.cpp; echo "syntax-check rc $?"
n=$(git -C "$W" diff "$PIN" -- . | grep -E '^\+' | grep -v '^+++' | grep -c -P '[^\x00-\x7F]'); echo "non-ASCII added lines: $n"
for t in maintenance-why cloud-sync-last-run cloud-oauth-lifetime cloud-set-systems-quoting cloud-gated-row cloud-folder-reopen cloud-content-selection cloud-oauth-await credential-quoting gpu-governor-save $(cd "$W/tests" && ls t26-*.py cloud-setup-repair-lifetime.py 2>/dev/null | sed 's/\.py$//'); do
  out=$(cd "$W" && timeout 600 python3 -I "tests/$t.py" 2>&1); rc=$?
  printf '%s rc=%s: %s\n' "$t" "$rc" "$(printf '%s\n' "$out" | tail -n 1 | cut -c1-140)"
done
out=$(cd "$D" && tools/es-menu-map-check --es-src "$W" --ref "$(git -C "$W" rev-parse HEAD)" 2>&1); rc=$?; printf '%s (rc %s)\n' "$(printf '%s\n' "$out" | tail -n 1)" "$rc"
out=$(cd "$D" && tools/es-untranslated --es-src "$W" --upstream bccd715707 2>&1); rc=$?; printf '%s (rc %s)\n' "$(printf '%s\n' "$out" | grep -m1 'fork string')" "$rc"
