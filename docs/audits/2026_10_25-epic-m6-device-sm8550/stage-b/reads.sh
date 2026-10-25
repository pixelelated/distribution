#!/bin/bash
# T28 (#675) stage B: the reads behind 02's sections, each with exit and wall
# time. Read-only, as stage A: no fetch, no build, nothing on the Nova.
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-device-sm8550-675
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t28/tmp
OUT=/workspace/tmp/m6-t28/runner-b/out
A=docs/audits/2026_10_25-epic-m6-device-sm8550
S=projects/ROCKNIX/devices/SM8550
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
b01_dat_consumer() { git show 8ebaf8daad:$S/config/kernel-firmware.dat; git grep -n 'kernel-firmware.dat' 8ebaf8daad -- projects packages; git show 8ebaf8daad:projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk | sed -n '36,40p;57p;70p'; }
b02_confs() { for d in SM8550 SM8650 SM8750 SM8250; do printf '%s: ' $d; git show 8ebaf8daad:projects/ROCKNIX/devices/$d/linux/linux.aarch64.conf | grep -E '^CONFIG_(DRM_MSM|EXTRA_FIRMWARE)=' | tr '\n' ' '; echo; done; }
b03_sm8550_in_kernel() { for h in 8ebaf8daad 651150fc88; do echo "$h: $(git show $h:projects/ROCKNIX/packages/linux/package.mk | grep -n 'SM8550' | cut -c1-90)"; done; }
b04_updateabl_head() { git show 8ebaf8daad:projects/ROCKNIX/packages/rocknix/sources/scripts/updateabl | sed -n '7,36p'; }
b05_update_sh() { git show 8ebaf8daad:$S/bootloader/update.sh | cat -n; }
b06_install_branch() { git show 8ebaf8daad:projects/ROCKNIX/bootloader/install | sed -n '50,61p'; }
b07_functions() { git show 8ebaf8daad:distributions/ROCKNIX/config/functions | sed -n '226,231p;384,400p'; git show 8ebaf8daad:$S/options | sed -n '28p'; }
b08_kernel_branch() { git show 8ebaf8daad:projects/ROCKNIX/packages/linux/package.mk | sed -n '387,404p'; }
b09_mkimage_branches() { git show 8ebaf8daad:projects/ROCKNIX/bootloader/mkimage | sed -n '22,26p;81,83p;108,111p'; git grep -n 'rocknix-u-boot' 8ebaf8daad -- projects packages scripts distributions config; echo "upstream bootloader/mkimage rocknix-u-boot: $(git show 651150fc88:projects/ROCKNIX/bootloader/mkimage | grep -c 'rocknix-u-boot')"; echo "upstream properties: $(git grep -l 'rocknix-u-boot-dt-id' 651150fc88 -- $S | wc -l)"; }
b10_config_xml() { git show 8ebaf8daad:projects/ROCKNIX/config.xml | sed -n '130,145p'; git show 651150fc88:projects/ROCKNIX/config.xml | grep -n '<SM8550'; }
b11_upstream_update_sh() { git show 651150fc88:$S/bootloader/update.sh | cat -n; echo "rm lines: $(git show 651150fc88:$S/bootloader/update.sh | grep -c 'rm ')"; }
b12_loader_entry() { git show 651150fc88:projects/ROCKNIX/packages/virtual/arm-efi/package.mk | sed -n '13,23p'; git grep -n -E '^\s*(DISTRONAME|DISTRO_BOOTLABEL)=' 8ebaf8daad -- distributions/ROCKNIX/options; }
b13_inputplumber_nova() { for f in $(git ls-tree -r --name-only 8ebaf8daad -- $S/filesystem/usr/share/inputplumber); do printf '%s: ' "${f##*/}"; git show "8ebaf8daad:$f" | grep -n -E 'value: |capability_map_id|^name:' | tr '\n' ' ' | cut -c1-260; echo; done; }
b14_quirk_device() { git grep -n 'QUIRK_DEVICE=' 8ebaf8daad -- projects/ROCKNIX/packages/sysutils/autostart projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-info | cut -c1-160; }
b15_gamepadcalibration() { git diff 8ebaf8daad 651150fc88 -- projects/ROCKNIX/packages/tools/gamepadcalibration/package.mk; git log --format='%h %ad %s' --date=short 8ebaf8daad..651150fc88 -- projects/ROCKNIX/packages/tools/gamepadcalibration/package.mk; }
b16_kernel_firmware_generic() { git show 8ebaf8daad:packages/linux-firmware/kernel-firmware/package.mk | grep -E '^PKG_VERSION='; }
b17_bytes() { tr '\n' '\0' < .qa-scratch/t28/paths.txt | xargs -0 git ls-tree -r -l 8ebaf8daad -- | awk '{b+=$4; if ($5 ~ /\.dtsi?$/) t+=$4; if ($5 ~ /disabled$/) d+=$4; if ($5 ~ /filesystem/) f+=$4} END {print "total", b, "trees", t, "disabled", d, "filesystem", f}'; }
b18_readme() { git show 8ebaf8daad:projects/ROCKNIX/packages/tools/rocknix-abl/sources/README | sed -n '1,6p'; }
b19_device_facts() { for n in 17 18 19 20 27 28 31; do printf 'L%s: ' $n; git show 2174265e9c:docs/releases/device-facts.md | sed -n "${n}p" | awk -F'|' '{print $2}'; done; diff <(git show 2174265e9c:docs/releases/device-facts.md) <(git show 8ebaf8daad:docs/releases/device-facts.md) >/dev/null && echo "identical at 2174265e9c and 8ebaf8daad"; }
b20_unpack_glob() { git show 8ebaf8daad:scripts/unpack | sed -n '150,159p'; }
g_check() { python3 -I -B "$A/tools/t28-tables.py" check "$A/02-forward-audit.md"; python3 -I -B "$A/tools/t28-tables.py" counts; }
for f in $(declare -F | awk '{print $3}' | grep -E '^(b[0-9]{2}_|g_)' | sort); do run "$f" "$f"; done
cat "$OUT/runs.tsv"
