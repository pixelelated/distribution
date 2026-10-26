#!/bin/bash
# T29 (#676) stage B: the reads behind 02's findings, each with exit and wall
# time. Read-only: no fetch, no build, no guest, nothing on a unit. Counts
# unfiltered (the paths carry spaces: -z reads and quoted names throughout).
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-os-device-quirks-676
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t29/tmp
OUT=/workspace/tmp/m6-t29/runner-b/out
A=docs/audits/2026_10_25-epic-m6-os-device-quirks
Q=projects/ROCKNIX/packages/hardware/quirks/devices
P=projects/ROCKNIX/packages/hardware/quirks/platforms
mkdir -p "$TMPDIR" "$OUT"
printf 'id\trc\tseconds\tstarted_utc\n' > "$OUT/runs.tsv"
run() {
  local id=$1; shift
  local t0 t1 rc started
  started=$(date -u +%H:%M:%S); t0=$(date +%s.%N)
  ( "$@" ) > "$OUT/$id.out" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  printf '%s\t%s\t%.2f\t%s\n' "$id" "$rc" "$(echo "$t1 - $t0" | bc)" "$started" >> "$OUT/runs.tsv"
}
s() { git show "8ebaf8daad:$1"; }
b01_tierB_blobs() {
  for e in "Retroid Pocket Nova" "QEMU Standard PC (Q35 + ICH9, 2009)" "Anbernic RG40XX H" "Anbernic RG40XX V" "Anbernic RG CubeXX" "AYANEO Pocket ACE" "AYANEO Pocket DMG" "AYANEO Pocket DS" "AYANEO Pocket EVO" "AYANEO Pocket S 2K" "AYANEO Pocket S Mini" "AYN Odin 2" "AYN Odin 2 Portal" "AYN Thor" "Retroid Pocket 6" "Retroid Pocket 6 TOP-DPAD"; do git ls-tree -r -z 8ebaf8daad -- "$Q/$e" | tr '\0' '\n'; done > "$TMPDIR/tierB.ls"
  echo "paths $(wc -l < "$TMPDIR/tierB.ls")"; awk '{print $1}' "$TMPDIR/tierB.ls" | sort | uniq -c
  echo "distinct blobs $(awk '$1!="120000"{print $3}' "$TMPDIR/tierB.ls" | sort -u | wc -l)"
}
b02_battery_test_copies() { git grep -n -F '[ ! ${BAT_LED_STATE} == "battery" ]' 8ebaf8daad -- projects/ROCKNIX/packages/hardware/quirks | cut -d: -f2- | sed 's|projects/ROCKNIX/packages/hardware/quirks/||'; echo "quoted: $(git grep -n -F '[ ! "${BAT_LED_STATE}" == "battery" ]' 8ebaf8daad -- projects/ROCKNIX/packages/hardware/quirks | cut -d: -f2- | sed 's|projects/ROCKNIX/packages/hardware/quirks/||' | tr '\n' ' ')"; }
b03_unit_and_default() { s projects/ROCKNIX/packages/sysutils/system-utils/system.d/batteryledstatus.service | grep -v -E '^\s*#|^\s*$'; echo "led.color defaults outside the quirks: $(git grep -n -E 'led\.color' 8ebaf8daad -- projects packages distributions | grep -v '/quirks/' | wc -l)"; }
b04_fixture() { python3 -I -B "$A/tools/t29-battery-unset.py"; s "$Q/Retroid Pocket 6/bin/battery_led_status" | sed -e 's|LED_PATH="/sys/devices/platform/"|LED_PATH="${LED_PATH:-/sys/devices/platform/}"|' -e 's|/sys/class/power_supply/battery/|${BATTERY_PATH}/|g' > "$TMPDIR/rp6-battery"; echo "--- RP6 (upstream):"; python3 -I -B "$A/tools/t29-battery-unset.py" --file "$TMPDIR/rp6-battery"; }
b05_h700_platform() { git ls-tree -r --name-only 8ebaf8daad -- "$P/H700" | sed "s|$P/H700/||"; s "$P/H700/030-analog_leds" | grep -n 'DEVICE_ANALOG'; bash -c 'unset DEVICE_ANALOG_STICKS_LED_CONTROL; [ $DEVICE_ANALOG_STICKS_LED_CONTROL == "true" ]; echo "unset flag: rc=$?"' 2>&1; }
b06_h700_trees() { T=projects/ROCKNIX/devices/H700/linux/dts/allwinner; for f in sun50i-h700-anbernic-rg-sp.dts sun50i-h700-anbernic-rg35xx-sp-v2-panel.dts sun50i-h700-anbernic-rg40xx-h.dts sun50i-h700-anbernic-rg40xx-v.dts sun50i-h700-anbernic-rgcubexx.dts; do echo "$f: stick-LED/uart nodes $(s $T/$f | grep -c -i -E 'uart2|kbd_backlight|rgb|joystick')"; done; }
b07_rewrites() { git grep -l -E 'cat <<EOF >/storage/\.config/profile\.d/' 8ebaf8daad -- "$Q" | wc -l; git grep -n -E 'sed -i .*retroarch\.cfg' 8ebaf8daad -- "$Q" | cut -d: -f2-3 | sed "s|$Q/||" | sort -u; s "$Q/AYN Odin 2/009-commander-cfg" | sed -n 6,11p; }
b08_rgb_no_default() { for f in "AYANEO Pocket EVO/bin/ledcontrol" "AYN Odin 2 Portal/bin/ledcontrol" "Retroid Pocket Nova/bin/ledcontrol"; do echo "== $f"; s "$Q/$f" | grep -n -E 'analogsticks\.led|analog_sticks_ledcontrol \$\{LEDS_CONFIG\}|LEDS_CONFIG="\$\{B\}'; done; s "$Q/AYN Odin 2/bin/achievements" | grep -n -E 'analogsticks\.led|LEDS_CONFIG\}|led\.color'; }
b09_brightness_dialects() { s "$Q/Retroid Pocket Nova/bin/ledcontrol" | grep -n -E 'max\)|mid\)|min\)'; s "$Q/AYN Thor/bin/battery_led_status" | grep -n -E 'led\.brightness|0-100|pct \* 255'; }
b10_device_writes() { s "$Q/AYANEO Pocket ACE/020-set-xbox-gamepad" | grep -n -E 'SERIAL_DEVICE|stty'; s "$Q/AYANEO Pocket DMG/bin/analog_sticks_ledcontrol" | grep -n -E 'SERIAL_DEVICE|exec 20'; s "$Q/Anbernic RG40XX V/bin/analog_sticks_ledcontrol" | grep -n -E 'SERIAL_DEVICE|RIGHT_|LEFT_RED \$LEFT'; }
b11_touchcontrol() { git ls-tree 8ebaf8daad -- "$Q/AYN Thor/" | sed "s|$Q/||"; s "$Q/AYN Thor/touchcontrol" | grep -n -E 'udevadm|rules\.d'; }
b12_bytes() { git ls-tree -r -l -z 8ebaf8daad -- "$Q/" | tr '\0' '\n' | awk '$4 != "-" {b+=$4; n++} END {print n " entries with a size, " b " bytes"}'; }
b13_pending() { git log --format='%h %ad %s' --date=short 8ebaf8daad..651150fc88 -- "$Q" | cut -c1-110; }
b14_rocknix_info() { s projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-info | sed -n 6,12p | cut -c1-140; }
b15_nova_history() { git log --format='%h %ad %an %s' --date=short c445081a59..8ebaf8daad -- "$Q/Retroid Pocket Nova" "$Q/QEMU Standard PC (Q35 + ICH9, 2009)" | cut -c1-120; git log --format='%h %ad %s' --date=short 8ebaf8daad..651150fc88 -- "$Q/Retroid Pocket Nova" | wc -l; }
g_check() { python3 -I -B "$A/tools/t29-tables.py" counts; }
for f in $(declare -F | awk '{print $3}' | grep -E '^(b[0-9]{2}_|g_)' | sort); do run "$f" "$f"; done
cat "$OUT/runs.tsv"
