#!/bin/bash
# backup-contract-cases.sh -- T14 S5's follow-up control for #1004, after the
# coordinator's 22:08 UTC ruling: a backup whose layout read failed must exit
# 0, say COMPLETED, and copy only into the configured saves folder. Two
# mutations of the historical cloud_backup (22571b47d2, the last tree with the
# layout detection), each run by the test as committed before this follow-up
# and by the current one, --case T18-bucket-backup-unknown:
#   silent  -- the backup makes the faulted listing and exits 0, saying nothing and copying nothing
#   derived -- the backup's copy goes to /pixelelated/Saves, a derived folder, not the configured /ROCKNIX/Saves
# Nothing outside the scratch.
#   backup-contract-cases.sh <tree> <before-follow-up test> <rclone> <scratch>
set -u
T="$(cd "$1" && pwd)"; BEFORE="$(readlink -f "$2")"; RC="$3"; S="$4"; rm -rf "$S"; mkdir -p "$S"
SRC=projects/ROCKNIX/packages/network/rclone/sources; BT=projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
src() { mkdir -p "$1"; git -C "$T" archive 22571b47d2 -- "$SRC" "$BT" | tar -x -C "$1"; }
src "$S/silent"; sed -i '1a rclone lsf --dirs-only qa:/ROCKNIX/ >/dev/null 2>&1; exit 0' "$S/silent/$SRC/cloud_backup"
src "$S/derived"; sed -i 's#^        "${REMOTENAME}${SAVES_REMOTE}/" \\$#        "${REMOTENAME}/pixelelated/Saves/" \\#' "$S/derived/$SRC/cloud_backup"
grep -q '"${REMOTENAME}/pixelelated/Saves/" \\$' "$S/derived/$SRC/cloud_backup" || { echo "derived mutation did not apply"; exit 2; }
src "$S/plain"
run() { env -u TMPDIR python3 -I "$1" --source-root "$2" --rclone "$RC" --output "$3" --case T18-bucket-backup-unknown > "$3.txt" 2>&1; echo $?; }
for m in silent derived plain; do
  rb=$(run "$BEFORE" "$S/$m" "$S/$m-before"); ra=$(run "$T/tools/rasteratops-cloud-layout-test" "$S/$m" "$S/$m-after")
  echo "  $m: before rc $rb | after rc $ra | $(grep -m1 '^FAIL' "$S/$m-after.txt" | cut -c1-110)"
  if [ "$m" = plain ]; then
    check "the unmutated historical backup passes both" "$([ "$rb" = 0 ] && [ "$ra" = 0 ] && echo 0 || echo 1)"
  else
    check "before the follow-up the $m backup passes (the positive)" "$([ "$rb" = 0 ] && echo 0 || echo 1)"
    check "after it, the $m backup fails" "$([ "$ra" != 0 ] && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
