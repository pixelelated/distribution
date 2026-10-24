#!/bin/bash
# info-cases.sh -- T14 S6's control for #995 (rocknix-info-test): scratch
# roots holding a copy of the test (stage-D or fixed) beside a copy of
# rocknix-info, changed one way per case:
#   regress -- `exit 0` appended (a quirk failure no longer propagates), run under PYTHONOPTIMIZE=1
#   renamed -- /tmp/battery.percent spelled /tmp/battery.pct (the test's adaptation no longer matches; the script only tests and reads that path, so nothing is written on the host)
# Nothing outside the scratch; the renamed path is absent on the host, so the
# unadapted script reads nothing there.
#   info-cases.sh <tree> <stage-D tools dir> <scratch>
set -u
T="$(cd "$1" && pwd)"; OLD="$(cd "$2" && pwd)"; S="$3"; rm -rf "$S"; mkdir -p "$S"
F=projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-info
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
mk() {  # <dir> <test>
  mkdir -p "$1/tools" "$1/$(dirname "$F")"; cp "$2" "$1/tools/rocknix-info-test"; cp "$T/$F" "$1/$F"
}
for side in old:"$OLD/rocknix-info-test" new:"$T/tools/rocknix-info-test"; do
  n=${side%%:*}; t=${side#*:}
  mk "$S/$n-regress" "$t"; printf '\nexit 0\n' >> "$S/$n-regress/$F"
  PYTHONOPTIMIZE=1 python3 "$S/$n-regress/tools/rocknix-info-test" > "$S/$n-regress.txt" 2>&1; a=$?
  mk "$S/$n-renamed" "$t"; sed -i 's#/tmp/battery.percent#/tmp/battery.pct#g' "$S/$n-renamed/$F"
  python3 -I "$S/$n-renamed/tools/rocknix-info-test" > "$S/$n-renamed.txt" 2>&1; b=$?
  echo "  $n: regression under PYTHONOPTIMIZE rc $a ($(tail -1 "$S/$n-regress.txt" | cut -c1-60)) | renamed root rc $b ($(tail -1 "$S/$n-renamed.txt" | cut -c1-70))"
  if [ "$n" = old ]; then
    check "stage-D passes a regression under PYTHONOPTIMIZE=1 (the positive)" "$([ "$a" = 0 ] && echo 0 || echo 1)"
    check "stage-D runs a script whose root it no longer adapts, and passes (the positive)" "$([ "$b" = 0 ] && echo 0 || echo 1)"
  else
    check "fixed fails the regression under PYTHONOPTIMIZE=1" "$([ "$a" != 0 ] && echo 0 || echo 1)"
    check "fixed fails the unadapted root, naming it" "$([ "$b" != 0 ] && grep -q 'adaptation pattern not found in the script: /tmp/battery.percent' "$S/$n-renamed.txt" && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
