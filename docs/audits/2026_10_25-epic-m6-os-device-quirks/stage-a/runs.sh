#!/bin/bash
# T29 (#676) stage A: brief section 5's runs, each with its exit and wall time.
# Read-only: no fetch, no build, no compiler, no plan, no guest, nothing on a
# handheld, no M7 build root, no tools/council/run call. Counts unfiltered.
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-os-device-quirks-676
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t29/tmp
OUT=/workspace/tmp/m6-t29/runner/out
R=/workspace/tmp/m6-t29/runner
Q=projects/ROCKNIX/packages/hardware/quirks/devices
mkdir -p "$TMPDIR" "$OUT" .qa-scratch/t29
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
r01_block() { bash "$R/scope.sh"; }
r02_counts() { wc -l < .qa-scratch/t29/paths.txt; wc -l < .qa-scratch/t29/entries.tsv; }
r03_branch_vs_hash() { echo "[$(tr '\n' '\0' < .qa-scratch/t29/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD -- | tail -1)]"; }
r04_entries_symlinks() { git ls-tree --name-only 8ebaf8daad -- "$Q/" | wc -l; git ls-tree 8ebaf8daad -- "$Q/" | grep -c '^120000'; git ls-tree -r 8ebaf8daad -- "$Q/" | grep -c '^120000'; }
r05_autostart_profile() { git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/autostart/profile.d/002-autostart | sed -n '6,12p' | cut -c1-120; }
r06_autostart_loop() { git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/autostart/sources/autostart | sed -n '31,43p' | grep -n -E 'devices|-f ' | cut -c1-120; }
r07_package_mk() { git show 8ebaf8daad:projects/ROCKNIX/packages/hardware/quirks/package.mk | sed -n '15,20p' | cut -c1-120; }
r08_wrapper() { git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/ledcontrol | sed -n '14,17p' | cut -c1-120; }
r09_model_lines() { git grep -n -E '^\s*model = ' 8ebaf8daad -- 'projects/ROCKNIX/devices/H700/linux/dts/allwinner/*.dts' 'projects/ROCKNIX/devices/SM8550/linux/dts/qcom/*.dts' | sed 's/^8ebaf8daad://' | cut -c1-120; }
r10_dtid_patch() { git show 8ebaf8daad:projects/ROCKNIX/devices/H700/patches/linux/0154-rocknix-dt-id.patch | grep -n 'RG35XX' | head -4 | cut -c1-100; }
r11_has_none() { git grep -h -E '^\s*model = ' 8ebaf8daad -- 'projects/ROCKNIX/devices/H700/linux/dts/allwinner/*.dts' 'projects/ROCKNIX/devices/SM8550/linux/dts/qcom/*.dts' | sed -E 's/.*model = "([^"]*)".*/\1/' | sort -u | while IFS= read -r m; do printf '%s: ' "$m"; git cat-file -e "8ebaf8daad:$Q/$m" 2>/dev/null && echo HAS || echo NONE; done; printf '%s: ' 'QEMU Standard PC (Q35 + ICH9, 2009)'; git cat-file -e "8ebaf8daad:$Q/QEMU Standard PC (Q35 + ICH9, 2009)" && echo HAS; }
r12_tiers() { bash "$R/tiers.sh"; }
r13_fork_paths() { tr '\n' '\0' < .qa-scratch/t29/paths.txt | xargs -0 git log --no-merges --format='%h %ad %an %s' --date=short c445081a59..8ebaf8daad -- | wc -l; tr '\n' '\0' < .qa-scratch/t29/paths.txt | xargs -0 git log --no-merges --format='%h %an' --since='2026-06-01T00:00:00Z' 8ebaf8daad -- > "$TMPDIR/hist.txt"; wc -l < "$TMPDIR/hist.txt"; grep -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt"; }
r14_fork_dir() { git log --no-merges --format=%h c445081a59..8ebaf8daad -- "$Q" | wc -l; git log --no-merges --format='%h %an' --since='2026-06-01T00:00:00Z' 8ebaf8daad -- "$Q" > "$TMPDIR/hist-dir.txt"; wc -l < "$TMPDIR/hist-dir.txt"; grep -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist-dir.txt"; }
r15_delta() { git diff --name-status 8ebaf8daad 651150fc88 -- "$Q" | awk '{print $1}' | sort | uniq -c; git log --oneline 8ebaf8daad..651150fc88 -- "$Q" | wc -l; git log --no-merges --oneline 8ebaf8daad..651150fc88 -- "$Q" | wc -l; }
r16_delta_shipped() { git diff --name-status 8ebaf8daad 651150fc88 -- "$Q" | grep -E '^A' | grep -E 'Thor|Retroid Pocket 6/' | cut -c1-100; }
r17_shape() { bash "$R/shape.sh"; }
r18_spellings() { git ls-tree -r --name-only 8ebaf8daad -- "$Q" | grep -c -E '050-game-configs$'; git ls-tree -r --name-only 8ebaf8daad -- "$Q" | grep -c -E '050-game_configs$'; }
r19_fixture() { git show 8ebaf8daad:tools/nova-led-test | wc -l; git show 8ebaf8daad:tools/nova-led-test | grep -n -E 'devices/Retroid Pocket Nova/bin|LED_PATH|BATTERY_PATH' | head -4 | cut -c1-100; }
r21_patch_models() { git show 8ebaf8daad:projects/ROCKNIX/devices/H700/patches/linux/0154-rocknix-dt-id.patch | grep -E '^ \s*model = ' | sed -E 's/.*model = "([^"]*)".*/\1/' | while IFS= read -r m; do printf '%s (0154): ' "$m"; git cat-file -e "8ebaf8daad:$Q/$m" 2>/dev/null && echo HAS || echo NONE; done; }
r22_board_count() { { git grep -h -E '^\s*model = ' 8ebaf8daad -- 'projects/ROCKNIX/devices/H700/linux/dts/allwinner/*.dts' 'projects/ROCKNIX/devices/SM8550/linux/dts/qcom/*.dts'; git show 8ebaf8daad:projects/ROCKNIX/devices/H700/patches/linux/0154-rocknix-dt-id.patch | grep -E '^ \s*model = '; } | sed -E 's/.*model = "([^"]*)".*/\1/' > "$TMPDIR/models.txt"; echo "lines $(wc -l < "$TMPDIR/models.txt") distinct $(sort -u "$TMPDIR/models.txt" | wc -l) boards-distinct $(sort -u "$TMPDIR/models.txt" | grep -v -x 'AYN-Thor' | wc -l)"; sort "$TMPDIR/models.txt" | uniq -d; }
r20_removal_rule() { echo "[$(git diff --stat 5ee0dfefcf HEAD -- packages projects tools | tail -1)]"; }
for f in $(declare -F | awk '{print $3}' | grep -E '^r[0-9]{2}_' | sort); do run "$f" "$f"; done
cat "$OUT/runs.tsv"
