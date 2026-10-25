#!/bin/bash
# T28 (#675) stage C: the seat's claims, re-read at their lines. Read-only;
# the download cache is listed (tar -t) and hashed, never extracted or fetched.
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-device-sm8550-675
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t28/tmp
OUT=/workspace/tmp/m6-t28/runner-c/out
S=projects/ROCKNIX/devices/SM8550; T=$S/linux/dts/qcom
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
c01_g7_diff_positions() { git show 651150fc88:$S/linux/linux.aarch64.conf > "$TMPDIR/up.conf"; git show 8ebaf8daad:$S/linux/linux.aarch64.conf > "$TMPDIR/ours.conf"; diff "$TMPDIR/up.conf" "$TMPDIR/ours.conf" | grep -E '^[0-9]'; }
c02_g14_regdb() { git show 8ebaf8daad:projects/ROCKNIX/packages/linux/package.mk | sed -n '93,97p;285,302p'; git show 8ebaf8daad:$S/linux/linux.aarch64.conf | grep -E '^CONFIG_(CFG80211|CFG80211_REQUIRE_SIGNED_REGDB)='; }
c03_g30_touch() { git show 8ebaf8daad:$T/qcs8550-retroidpocket-rp6.dts | sed -n '349,370p'; git show 8ebaf8daad:$T/qcs8550-ayn-common.dtsi | sed -n '1585,1645p' | grep -n -E 'ts_|pins'; git show 8ebaf8daad:$T/qcs8550-ayn-thor.dts | sed -n '380,394p'; git show 8ebaf8daad:$T/qcs8550-retroidpocket-rpnova.dts | sed -n '18,28p'; }
c04_g32_ids() { for f in $(git ls-tree --name-only 8ebaf8daad $T/); do printf '%s: ' "${f##*/}"; git show 8ebaf8daad:$f | grep -E 'qcom,(board-id|msm-id)|rocknix-u-boot-dt-id' | tr -s '\t ' ' ' | tr '\n' ' '; echo; done; grep -m1 '| D-WORKFLOW-114 |' docs/decision-register.md | grep -o 'the Nova.s panel is 1280x960'; }
c05_g27_init() { git show 8ebaf8daad:projects/ROCKNIX/packages/sysutils/busybox/scripts/init | sed -n '341,368p;427,440p'; }
c06_g28_elf_sizes() { for f in /workspace/cache/rocknix-sources/rocknix-abl/rocknix-abl-*.tar.gz; do printf '%s: ' "${f##*/}"; tar -tvzf "$f" | grep 'abl_signed-SM8550.elf$' | awk '{print $3, $3 % 512, $3 % 4096}'; done; echo "1.2 sha256 $(sha256sum /workspace/cache/rocknix-sources/rocknix-abl/rocknix-abl-1.2.tar.gz | cut -c1-64)"; git show 8ebaf8daad:projects/ROCKNIX/packages/tools/rocknix-abl/package.mk | grep '^PKG_SHA256='; }
c07_g5_labels() { git grep -n -E '^\s*(DISTRONAME|DISTRO_BOOTLABEL|DISTRO_DISKLABEL)=' 8ebaf8daad -- distributions/ROCKNIX/options; }
for f in $(declare -F | awk '{print $3}' | grep -E '^c[0-9]{2}_' | sort); do run "$f" "$f"; done
cat "$OUT/runs.tsv"
