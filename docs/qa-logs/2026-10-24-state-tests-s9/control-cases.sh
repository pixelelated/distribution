#!/bin/bash
# control-cases.sh -- T14 S9's control for #1001: pixelelated-state-check-test
# --self-test, the test and gate before the fix (the given copies) and the
# fixed pair, each in its own scratch tree (the two tools, the autostart unit
# and ppsspp-sa's sources, the only tree files the test reads):
#   crash   -- the gate's text() crashes (an AttributeError) instead of refusing
#              when it meets a NUL, so the NUL controls reach the catch-all
#   dropped -- the test's `case("clean-image", ...)` registration is deleted
#   plain   -- neither change
# Nothing outside the scratch.
#   control-cases.sh <tree> <gate before> <test before> <scratch>
set -u
T="$(cd "$1" && pwd)"; GB="$(readlink -f "$2")"; TB="$(readlink -f "$3")"; S="$4"; rm -rf "${S:?}"; mkdir -p "$S"
PS=projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/sources; U=projects/ROCKNIX/packages/sysutils/autostart/system.d/rocknix-autostart.service
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
tree() {  # <dir> <gate> <test>
  mkdir -p "$1/tools" "$1/$PS" "$1/$(dirname "$U")" "$1-tmp"; cp -r "$T/$PS/." "$1/$PS/"; cp "$T/$U" "$1/$U"
  cp "$2" "$1/tools/pixelelated-state-check"; cp "$3" "$1/tools/pixelelated-state-check-test"
}
run() { TMPDIR="$1-tmp" python3 -I "$1/tools/pixelelated-state-check-test" --self-test > "$1.json" 2>&1; echo $?; }
summary() { python3 -c 'import json,sys
try: d=json.load(open(sys.argv[1])); print(d["status"], d.get("control_count", "-"))
except Exception: print("unreadable")' "$1.json"; }
for side in before:"$GB":"$TB" after:"$T/tools/pixelelated-state-check":"$T/tools/pixelelated-state-check-test"; do
  IFS=: read -r n g t <<< "$side"
  tree "$S/$n-plain" "$g" "$t"; tree "$S/$n-crash" "$g" "$t"; tree "$S/$n-dropped" "$g" "$t"
  sed -i 's#^    require(b"\\0" not in data)$#    b"\\0" not in data or None.crash#' "$S/$n-crash/tools/pixelelated-state-check"
  grep -q 'None.crash' "$S/$n-crash/tools/pixelelated-state-check" || { echo "crash mutation did not apply"; exit 2; }
  sed -i '/^    case("clean-image", mode="clean-image")$/d' "$S/$n-dropped/tools/pixelelated-state-check-test"
  ! grep -q '^    case("clean-image", mode="clean-image")$' "$S/$n-dropped/tools/pixelelated-state-check-test" || { echo "drop did not apply"; exit 2; }
  a=$(run "$S/$n-plain"); b=$(run "$S/$n-crash"); c=$(run "$S/$n-dropped")
  echo "  $n: plain rc $a ($(summary "$S/$n-plain")) | crash rc $b ($(summary "$S/$n-crash")) | dropped rc $c ($(summary "$S/$n-dropped"))"
  check "$n: the plain pair passes" "$([ "$a" = 0 ] && echo 0 || echo 1)"
  if [ "$n" = before ]; then
    check "before: a gate that crashes on a NUL satisfies the NUL controls (the positive)" "$([ "$b" = 0 ] && echo 0 || echo 1)"
    check "before: a dropped registration passes, one control short (the positive)" "$([ "$c" = 0 ] && echo 0 || echo 1)"
  else
    check "after: the crash fails the run" "$([ "$b" != 0 ] && echo 0 || echo 1)"
    check "after: the dropped registration fails the run" "$([ "$c" != 0 ] && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
