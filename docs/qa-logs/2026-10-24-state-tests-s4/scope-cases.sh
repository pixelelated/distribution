#!/bin/bash
# scope-cases.sh -- T14 S4's control for #993: do content-scope's cases
# exercise what they name? Two product mutations of cloud_content_restore in
# a scratch source root (the rclone sources and backuptool copied, then
# changed), each run by the stage-D test and the fixed one with --cases:
#   noop  -- the script lists remotes and exits 0: the missing-* cases
#   early -- the script lists remotes and exits 1: the unreadable-* and partial-* cases
# and a --cases list carrying an unknown name. Nothing outside the scratch.
#   scope-cases.sh <tree> <stage-D tools dir> <rclone> <scratch>
set -u
T="$(cd "$1" && pwd)"; OLD="$(cd "$2" && pwd)"; RC="$3"; S="$4"; rm -rf "${S:?}"; mkdir -p "$S"
SRC=projects/ROCKNIX/packages/network/rclone/sources; BT=projects/ROCKNIX/packages/rocknix/sources/scripts
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
src() {  # <dir> <exit code or empty>: a source root, cloud_content_restore cut short if a code is given
  mkdir -p "$1/$SRC" "$1/$BT"; cp -r "$T/$SRC/." "$1/$SRC/"; cp "$T/$BT/backuptool" "$1/$BT/"
  [ -n "$2" ] && sed -i "1a rclone listremotes >/dev/null 2>\&1; exit $2" "$1/$SRC/cloud_content_restore"
  return 0
}
run() {  # <tool> <source root> <out> <cases>
  python3 -I "$1" --source-root "$2" --rclone "$RC" --output "$3" --cases "$4" > "$3.txt" 2>&1; echo $?
}
src "$S/noop" 0; src "$S/early" 1; src "$S/plain" ""
missing=missing-list,missing-scan,missing-all
failing=unreadable-list,unreadable-scan,unreadable-all,partial-list,partial-scan,partial-all
for side in old:"$OLD/pixelelated-content-scope-test" new:"$T/tools/pixelelated-content-scope-test"; do
  n=${side%%:*}; tool=${side#*:}
  a=$(run "$tool" "$S/noop" "$S/$n-noop" "$missing"); b=$(run "$tool" "$S/early" "$S/$n-early" "$failing")
  c=$(run "$tool" "$S/plain" "$S/$n-typo" "missing-list,no-such-case")
  echo "  $n: noop script, the missing cases rc $a | early-exit script, the failure cases rc $b | a --cases typo rc $c"
  if [ "$n" = old ]; then
    check "stage-D: the missing cases pass a script that never reads the library (the positive)" "$([ "$a" = 0 ] && echo 0 || echo 1)"
    check "stage-D: the failure cases pass a failure their fault did not cause (the positive)" "$([ "$b" = 0 ] && echo 0 || echo 1)"
    check "stage-D: an unknown --cases name is dropped, rc 0 (the positive)" "$([ "$c" = 0 ] && echo 0 || echo 1)"
  else
    check "fixed: the missing cases fail it" "$([ "$a" != 0 ] && echo 0 || echo 1)"
    check "fixed: the failure cases fail it" "$([ "$b" != 0 ] && echo 0 || echo 1)"
    check "fixed: an unknown --cases name exits 2" "$([ "$c" = 2 ] && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
