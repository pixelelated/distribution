#!/bin/bash
# T27 (#674) stage A: the brief's section 5 runs, each with its exit and wall
# time. Read-only: no fetch, no build, no guest, no handheld, no
# tools/council/run. Recipe reads pass the masking sed (one line in the slice
# matches the credential read filter).
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-device-h700-674
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t27/tmp
OUT=/workspace/tmp/m6-t27/runner/out
mkdir -p "$TMPDIR" "$OUT" .qa-scratch/t27
R=8ebaf8daad
U=651150fc88
C=projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf
H=projects/ROCKNIX/devices/H700
MASK='s/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'
printf 'id\trc\tseconds\tstarted_utc\n' > "$OUT/runs.tsv"

run() {
  local id=$1; shift
  local t0 t1 rc started
  started=$(date -u +%H:%M:%S)
  t0=$(date +%s.%N)
  ( "$@" ) > "$OUT/$id.out" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  printf '%s\t%s\t%.2f\t%s\n' "$id" "$rc" "$(echo "$t1 - $t0" | bc)" "$started" >> "$OUT/runs.tsv"
}

r01_scope() { bash /workspace/tmp/m6-t27/runner/scope.sh; }
r02_conf_header() { git show "$R:$C" | sed -n '3p'; git show "$R:$C" | wc -l; }
r03_conf_vs_upstream() {
  git show "$U:$C" > "$TMPDIR/up.conf" || return 1
  git show "$R:$C" > "$TMPDIR/ours.conf" || return 1
  echo "removed=$(diff "$TMPDIR/up.conf" "$TMPDIR/ours.conf" | grep -c '^<') added=$(diff "$TMPDIR/up.conf" "$TMPDIR/ours.conf" | grep -c '^>')"
}
r04_conf_fork_edits() { git log --no-merges --format='%h %ad %an %s' --date=short c445081a59..$R -- "$C"; }
r05_conf_upstream_commits() { git log --format='%h %ad %an %s' --date=short $R..$U -- "$C"; }
r06_kernel_version() { git show $R:projects/ROCKNIX/packages/linux/package.mk | sed -n '29,35p' | grep -n -E 'H700|PKG_VERSION'; }
r07_pins() {
  for p in u-boot-DDR3 u-boot-DDR4 h700-suspend-stub u-boot; do
    for h in $R $U; do
      printf '%s %s: %s\n' "$p" "$h" "$(git show "$h:$H/packages/$p/package.mk" | grep -E '^PKG_(VERSION|SHA256|UBOOT_CONFIG)=' | tr '\n' ' ')"
    done
  done | sed -E "$MASK"
}
r08_defconfig_diff() {
  diff <(git show $R:$H/packages/u-boot-DDR3/sources/configs/anbernic_rg35xx_h700_lpddr3_defconfig) \
       <(git show $R:$H/packages/u-boot-DDR4/sources/configs/anbernic_rg35xx_h700_lpddr4_defconfig) | grep -c -E '^[<>]'
}
r09_update_sh() { git show $R:$H/bootloader/update.sh | grep -n -E 'dtb.img|vdd-dram|microvolts|seek' | cut -c1-120; }
r10_mkimage() { git show $R:projects/ROCKNIX/bootloader/mkimage | grep -n -E 'dtb.img|device_trees|SUBDEVICE' | cut -c1-120; }
r11_subdevices() { git show $R:distributions/ROCKNIX/config/functions | sed -n '220,228p' | grep -n SUBDEVICES; }
r12_dts_count() { git ls-tree -r --name-only $R -- $H/linux/dts | wc -l; }
r13_dts_includes() {
  for f in $(git ls-tree -r --name-only $R -- $H/linux/dts); do
    printf '%s: %s | %s\n' "$(basename "$f")" "$(git show "$R:$f" | grep -m1 '#include' | cut -c1-60)" "$(git show "$R:$f" | grep -m1 'rocknix-dt-id' | cut -c1-60)"
  done
}
r14_history() {
  tr '\n' '\0' < .qa-scratch/t27/paths.txt | xargs -0 git log --no-merges --format='%h %an' --since=2026-06-01 $R -- > "$TMPDIR/hist.txt" || return 1
  echo "total $(wc -l < "$TMPDIR/hist.txt")"
  echo "fork $(grep -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt")"
  echo "upstream $(grep -v -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt")"
}
r15_upstream_delta() { tr '\n' '\0' < .qa-scratch/t27/paths.txt | xargs -0 git diff --name-status $R $U -- | cut -c1-120; }
r16_removal_rule() { echo "dispatch tip: [$(git diff --stat ed7fd0ea50 HEAD -- packages projects tools | tail -1)]"; echo "read hash packages+projects: [$(git diff --stat $R HEAD -- packages projects | tail -1)]"; }

for f in $(declare -F | awk '{print $3}' | grep -E '^r[0-9]{2}_' | sort); do run "$f" "$f"; done
cat "$OUT/runs.tsv"
