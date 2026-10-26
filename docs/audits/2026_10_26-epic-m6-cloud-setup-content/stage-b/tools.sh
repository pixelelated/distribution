#!/bin/bash
# T17 (#664) stage B: the five fork tools that exercise the 14, on the host,
# each with the rclone it ran recorded. No network beyond loopback; no guest;
# no M7 root (the rclone is M6's retained donor copy, or the host's where the
# tool hard-codes /usr/bin/rclone).
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-setup-content-664
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t17/tmp
OUT=/workspace/tmp/m6-t17/runner-b/out
DONOR=/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin
mkdir -p "$TMPDIR" "$OUT"
printf 'id\trc\tseconds\tstarted_utc\trclone\n' > "$OUT/tools.tsv"
tool() {
  local id=$1 rcl=$2; shift 2
  local t0 t1 rc started
  started=$(date -u +%H:%M:%S); t0=$(date +%s.%N)
  ( timeout 900 "$@" ) > "$OUT/$id.out" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  printf '%s\t%s\t%.1f\t%s\t%s\n' "$id" "$rc" "$(echo "$t1 - $t0" | bc)" "$started" "$rcl" >> "$OUT/tools.tsv"
}
HOSTRC="host $(readlink -f /usr/bin/rclone) $(/usr/bin/rclone version 2>/dev/null | head -1)"
DONORRC="donor $DONOR/rclone $($DONOR/rclone version 2>/dev/null | head -1)"
tool t1_cloud_connections_test "$HOSTRC" python3 -B tools/cloud-connections-test
tool t2_cloud_input_test "$HOSTRC (not used: wifictl/phone JS)" python3 -B tools/cloud-input-test
tool t3_validator_test "$DONORRC" python3 -B tools/pixelelated-cloud-validator-test --output "$OUT/t3" --rclone "$DONOR/rclone"
tool t4_content_scope_test "$DONORRC" python3 -B tools/pixelelated-content-scope-test --source-root . --rclone "$DONOR/rclone" --output "$OUT/t4"
tool t5_save_layout_test "$DONORRC" python3 -B tools/pixelelated-save-layout-test --source-root . --rclone "$DONOR/rclone" --output "$OUT/t5" --busybox "$DONOR/busybox"
echo done > "$OUT/finished"
