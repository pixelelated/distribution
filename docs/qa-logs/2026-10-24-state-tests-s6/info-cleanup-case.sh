#!/bin/bash
# info-cleanup-case.sh -- T14 S6's follow-up control for #995: does
# rocknix-info-test remove its scratch when a check fails? The test as
# committed before the follow-up and the current one, each copied beside a
# rocknix-info whose /tmp/battery.percent is renamed (so the adaptation check
# raises), and beside the script as it is (a pass), each with a fresh TMPDIR.
# Nothing outside the scratch.
#   info-cleanup-case.sh <tree> <before-follow-up test> <scratch>
set -u
T="$(cd "$1" && pwd)"; BEFORE="$(readlink -f "$2")"; S="$3"; rm -rf "${S:?}"; mkdir -p "$S"
F=projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-info
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
mk() { mkdir -p "$1/tools" "$1/$(dirname "$F")" "$1-tmp"; cp "$2" "$1/tools/rocknix-info-test"; cp "$T/$F" "$1/$F"; }
for side in before:"$BEFORE" after:"$T/tools/rocknix-info-test"; do
  n=${side%%:*}; t=${side#*:}
  mk "$S/$n-failing" "$t"; sed -i 's#/tmp/battery.percent#/tmp/battery.pct#g' "$S/$n-failing/$F"
  TMPDIR="$S/$n-failing-tmp" python3 -I "$S/$n-failing/tools/rocknix-info-test" > "$S/$n-failing.txt" 2>&1; a=$?
  mk "$S/$n-passing" "$t"
  TMPDIR="$S/$n-passing-tmp" python3 -I "$S/$n-passing/tools/rocknix-info-test" > "$S/$n-passing.txt" 2>&1; b=$?
  la=$(ls -A "$S/$n-failing-tmp" | wc -l); lb=$(ls -A "$S/$n-passing-tmp" | wc -l)
  echo "  $n: failing rc $a, $la left | passing rc $b, $lb left"
  check "$n: the failing run fails and the passing one passes" "$([ "$a" = 1 ] && [ "$b" = 0 ] && echo 0 || echo 1)"
  check "$n: the passing run leaves nothing" "$([ "$lb" = 0 ] && echo 0 || echo 1)"
  if [ "$n" = before ]; then
    check "before: the failing run leaves its scratch (the positive)" "$([ "$la" -ge 1 ] && echo 0 || echo 1)"
  else
    check "after: the failing run leaves nothing" "$([ "$la" = 0 ] && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
