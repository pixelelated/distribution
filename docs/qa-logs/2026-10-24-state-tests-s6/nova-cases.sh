#!/bin/bash
# nova-cases.sh -- T14 S6's control for #995 (nova-led-test): scratch source
# roots holding the three Nova scripts, changed one way per case, run by the
# stage-D test and the fixed one (--source-root):
#   regress   -- ledcontrol exits 3 after its writes (an EXIT trap), run under PYTHONOPTIMIZE=1
#   hardcoded -- ledcontrol's LED_PATH assigned a plain path, to a stand-in "host" LED tree under
#                the scratch (never /sys): a test that runs it writes outside its fixture
# Nothing outside the scratch.
#   nova-cases.sh <tree> <stage-D tools dir> <scratch>
set -u
T="$(cd "$1" && pwd)"; OLD="$(cd "$2" && pwd)"; S="$3"; rm -rf "${S:?}"; mkdir -p "$S"
B="projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin"
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
mk() { mkdir -p "$1/$B"; cp "$T/$B/ledcontrol" "$T/$B/analog_sticks_ledcontrol" "$T/$B/battery_led_status" "$1/$B/"; }
standin() {  # <dir>: an LED tree like the fixture's, every file "untouched" so any write shows
  local lr k d; for lr in l r; do for k in 1 2 3 4; do d="$1/multi-led$lr$k/leds/rgb:$lr$k"; mkdir -p "$d"; echo untouched > "$d/brightness"; echo untouched > "$d/multi_intensity"; done; done
}
for side in old:"$OLD/nova-led-test" new:"$T/tools/nova-led-test"; do
  n=${side%%:*}; t=${side#*:}
  mk "$S/$n-regress"; sed -i "1a trap 'exit 3' EXIT" "$S/$n-regress/$B/ledcontrol"
  PYTHONOPTIMIZE=1 python3 "$t" --source-root "$S/$n-regress" > "$S/$n-regress.txt" 2>&1; a=$?
  mk "$S/$n-hard"; standin "$S/$n-standin-host"
  sed -i "s#^LED_PATH=.*#LED_PATH=$S/$n-standin-host#" "$S/$n-hard/$B/ledcontrol"
  python3 -I "$t" --source-root "$S/$n-hard" > "$S/$n-hard.txt" 2>&1; b=$?
  written=$(grep -L -x untouched "$S/$n-standin-host"/multi-led*/leds/*/brightness | wc -l)
  echo "  $n: regression under PYTHONOPTIMIZE rc $a ($(tail -1 "$S/$n-regress.txt" | cut -c1-50)) | hardcoded LED_PATH rc $b, stand-in files written $written ($(tail -1 "$S/$n-hard.txt" | cut -c1-70))"
  if [ "$n" = old ]; then
    check "stage-D passes a ledcontrol that fails after its writes, under PYTHONOPTIMIZE=1 (the positive)" "$([ "$a" = 0 ] && echo 0 || echo 1)"
    check "stage-D runs a hardcoded LED_PATH and writes outside its fixture (the positive)" "$([ "$written" -gt 0 ] && echo 0 || echo 1)"
  else
    check "fixed fails that ledcontrol under PYTHONOPTIMIZE=1" "$([ "$a" != 0 ] && echo 0 || echo 1)"
    check "fixed refuses the hardcoded LED_PATH before running, writing nothing" "$([ "$b" != 0 ] && [ "$written" = 0 ] && grep -q 'LED_PATH is assigned without' "$S/$n-hard.txt" && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
