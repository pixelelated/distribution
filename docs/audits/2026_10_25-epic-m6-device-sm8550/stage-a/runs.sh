#!/bin/bash
# T28 (#675) stage A: brief section 5's runs, each with its exit and wall time.
# Read-only: no fetch, no build, no compiler, no plan, no guest, nothing on the
# Nova or any handheld, no M7 build root, no tools/council/run call.
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-device-sm8550-675
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t28/tmp
OUT=/workspace/tmp/m6-t28/runner/out
mkdir -p "$TMPDIR" "$OUT" .qa-scratch/t28
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
C=projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf
r01_block() { bash /workspace/tmp/m6-t28/runner/scope.sh; }
r02_paths() { wc -l < .qa-scratch/t28/paths.txt; }
r03_branch_vs_hash() { echo "[$(tr '\n' '\0' < .qa-scratch/t28/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD -- | tail -1)]"; }
r04_lines() { for p in $(cat .qa-scratch/t28/paths.txt); do printf '%s ' "$(git show "8ebaf8daad:$p" | wc -l)"; done | awk '{s=0; for(i=1;i<=NF;i++) s+=$i; print s}'; }
r05_disabled() { git show 8ebaf8daad:projects/ROCKNIX/devices/SM8550/patches/linux/0053-add-hynitron-touchscreen.patch.disabled | wc -l; }
r06_conf_head() { git show "8ebaf8daad:$C" | sed -n '3p'; git show "8ebaf8daad:$C" | wc -l; }
r07_conf_diff() {
  git show "651150fc88:$C" > "$TMPDIR/up.conf"; git show "8ebaf8daad:$C" > "$TMPDIR/ours.conf"
  echo "removed=$(diff "$TMPDIR/up.conf" "$TMPDIR/ours.conf" | grep -c '^<') added=$(diff "$TMPDIR/up.conf" "$TMPDIR/ours.conf" | grep -c '^>')"
  diff "$TMPDIR/up.conf" "$TMPDIR/ours.conf" | grep -E '^[<>]'
}
r08_conf_distance() { for d in SM8650 SM8750 SM6115 SM4450 SM8250; do O=projects/ROCKNIX/devices/$d/linux/linux.aarch64.conf; printf '%s %s/%s ' "$d" "$(diff <(git show "8ebaf8daad:$C") <(git show "8ebaf8daad:$O") | grep -c '^<')" "$(diff <(git show "8ebaf8daad:$C") <(git show "8ebaf8daad:$O") | grep -c '^>')"; done; echo; }
r09_conf_fork() { git log --no-merges --format='%h %ad %an %s' --date=short c445081a59..8ebaf8daad -- "$C" | wc -l; }
r10_conf_upstream() { git log --format='%h %ad %an %s' --date=short 8ebaf8daad..651150fc88 -- "$C" | cut -c1-100; }
r11_kernel_case() { git show 8ebaf8daad:projects/ROCKNIX/packages/linux/package.mk | sed -n '29,35p' | grep -n -E 'SM8550|PKG_VERSION' | cut -c1-120; git show 651150fc88:projects/ROCKNIX/packages/linux/package.mk | grep -n -E 'SM8550\)|PKG_VERSION="7' | head -3 | cut -c1-120; }
r12_pins() { for p in tools/qcom-abl tools/rocknix-abl tools/mkbootimg linux-firmware/extra-firmware linux-firmware/kernel-firmware tools/inputplumber tools/gamepadcalibration; do for h in 8ebaf8daad 651150fc88; do f="projects/ROCKNIX/packages/$p/package.mk"; if git cat-file -e "$h:$f" 2>/dev/null; then printf '%s %s: %s\n' "$p" "$h" "$(git show "$h:$f" | grep -E '^PKG_(VERSION|SHA256|URL)=' | tr '\n' ' ' | cut -c1-200)"; else printf '%s %s: absent\n' "$p" "$h"; fi; done; done | sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'; }
r13_rocknix_abl_log() { git log --format='%h %ad %an %s' --date=short -3 8ebaf8daad -- projects/ROCKNIX/packages/tools/rocknix-abl/package.mk | cut -c1-120; }
r14_openabl() { git show 651150fc88:projects/ROCKNIX/packages/tools/openabl/package.mk | grep -E '^PKG_(VERSION|URL)=' | cut -c1-160; git log --format='%h %ad %s' --date=short 8ebaf8daad..651150fc88 -- projects/ROCKNIX/packages/tools/openabl | cut -c1-100; }
r15_update_sh() { git show 8ebaf8daad:projects/ROCKNIX/devices/SM8550/bootloader/update.sh | grep -n -E 'BOOT_DISK|rocknix_abl|updateabl|rm -rf|boot.hint' | cut -c1-120; }
r16_scripts_mkimage() { git show 8ebaf8daad:scripts/mkimage | grep -n -E 'qcom-abl' | cut -c1-120; }
r17_bootloader_mkimage() { git show 8ebaf8daad:projects/ROCKNIX/bootloader/mkimage | grep -n -E 'SM8550|rocknix_abl|rocknix-u-boot' | cut -c1-120; }
r18_kernel_abl_branch() { git show 8ebaf8daad:projects/ROCKNIX/packages/linux/package.mk | sed -n '387,404p' | grep -n -E 'dtb|mkbootimg|kernel.gz' | cut -c1-120; }
r19_embed_blocks() { git show 8ebaf8daad:projects/ROCKNIX/packages/linux/package.mk | sed -n '83p;208,277p' | grep -n -E 'SM8|H700|EXTRA_FIRMWARE|firmware' | head -12 | cut -c1-120; }
r20_config_xml() { git show 8ebaf8daad:projects/ROCKNIX/config.xml | sed -n '130,145p' | grep -c '<file>'; }
r21_updateabl() { git show 8ebaf8daad:projects/ROCKNIX/packages/rocknix/sources/scripts/updateabl | sed -n '60,75p' | cut -c1-120; }
r22_dts_count() { git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/devices/SM8550/linux/dts | wc -l; }
r23_nova_dts() { git show 8ebaf8daad:projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-retroidpocket-rpnova.dts | grep -n -E '#include|model|compatible' | cut -c1-100; }
r24_dt_id() { for f in $(git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/devices/SM8550/linux/dts); do git show "8ebaf8daad:$f" | grep -c 'rocknix-dt-id' || true; done | sort | uniq -c; }
r25_history() { tr '\n' '\0' < .qa-scratch/t28/paths.txt | xargs -0 git log --no-merges --format='%h %an' --since='2026-06-01T00:00:00Z' 8ebaf8daad -- | tee "$TMPDIR/hist.txt" | wc -l; echo "fork $(grep -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt")"; echo "with merges $(tr '\n' '\0' < .qa-scratch/t28/paths.txt | xargs -0 git log --format=%h --since='2026-06-01T00:00:00Z' 8ebaf8daad -- | wc -l)"; echo "directory $(git log --no-merges --format=%h --since='2026-06-01T00:00:00Z' 8ebaf8daad -- projects/ROCKNIX/devices/SM8550 | wc -l) / $(git log --format=%h --since='2026-06-01T00:00:00Z' 8ebaf8daad -- projects/ROCKNIX/devices/SM8550 | wc -l)"; echo "bare-date $(git log --no-merges --format=%h --since=2026-06-01 8ebaf8daad -- projects/ROCKNIX/devices/SM8550 | wc -l)"; }
r26_fork_since_base() { git log --no-merges --format=%h 651150fc88..8ebaf8daad -- projects/ROCKNIX/devices/SM8550 | wc -l; git log --format='%h %s' 651150fc88..8ebaf8daad -- projects/ROCKNIX/devices/SM8550 | cut -c1-100; }
r27_delta_29() { tr '\n' '\0' < .qa-scratch/t28/paths.txt | xargs -0 git diff --name-status 8ebaf8daad 651150fc88 -- | cut -c1-120; tr '\n' '\0' < .qa-scratch/t28/paths.txt | xargs -0 git diff --shortstat 8ebaf8daad 651150fc88 --; }
r28_delta_dir() { git diff --name-status 8ebaf8daad 651150fc88 -- projects/ROCKNIX/devices/SM8550 | cut -c1-120; git diff --shortstat 8ebaf8daad 651150fc88 -- projects/ROCKNIX/devices/SM8550; }
r29_boot_change() { git log --format='%h %ad %s' --date=short 8ebaf8daad..651150fc88 -- projects/ROCKNIX/devices/SM8550 scripts/mkimage projects/ROCKNIX/packages/tools/rocknix-abl projects/ROCKNIX/packages/tools/openabl | cut -c1-110; }
r30_makefile() { grep -n -E '^SM8550:|SM8550' Makefile | head -5 | cut -c1-100; sed -n '28,31p' config/options; }
r31_removal_rule() { echo "[$(git diff --stat 458e2bfda1 HEAD -- packages projects tools | tail -1)]"; }
for f in $(declare -F | awk '{print $3}' | grep -E '^r[0-9]{2}_' | sort); do run "$f" "$f"; done
cat "$OUT/runs.tsv"
