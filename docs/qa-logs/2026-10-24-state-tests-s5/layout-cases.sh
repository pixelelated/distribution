#!/bin/bash
# layout-cases.sh -- T14 S5's control for #1004: do cloud-layout's legacy
# backup case and its two failure controls catch the defect they name? Three
# product mutations in scratch source roots, each run by the stage-D test and
# the fixed one with --case (TMPDIR unset: the stage-D sandbox would leak it):
#   backup-noop   current source, `backuptool backup` exits 0 writing nothing  -> T24-local-legacy-recovery
#   settle-skip   historical source (22571b47d2), `cloud_setup --seed-folders` exits 0 at once -> T17-seed-failed
#   restore-swallow historical source, cloud_restore makes the faulted listing then exits 0 -> T18-bucket-restore-unknown
# Nothing outside the scratch.
#   layout-cases.sh <tree> <stage-D tools dir> <rclone> <scratch>
set -u
T="$(cd "$1" && pwd)"; OLD="$(cd "$2" && pwd)"; RC="$3"; S="$4"; rm -rf "${S:?}"; mkdir -p "$S"
SRC=projects/ROCKNIX/packages/network/rclone/sources; BT=projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
src() {  # <dir> <commit or WORKTREE>
  mkdir -p "$1"
  if [ "$2" = WORKTREE ]; then mkdir -p "$1/$SRC" "$1/$(dirname "$BT")"; cp -r "$T/$SRC/." "$1/$SRC/"; cp "$T/$BT" "$1/$BT"
  else git -C "$T" archive "$2" -- "$SRC" "$BT" | tar -x -C "$1"; fi
}
cut_short() { sed -i "1a $2" "$1"; grep -qF "$2" "$1" || { echo "mutation did not apply to $1"; exit 2; }; }
src "$S/backup-noop" WORKTREE;  cut_short "$S/backup-noop/$BT" '[ "${1:-}" = backup ] && exit 0'
src "$S/settle-skip" 22571b47d2; cut_short "$S/settle-skip/$SRC/cloud_setup" '[ "${1:-}" = --seed-folders ] && exit 0'
src "$S/restore-swallow" 22571b47d2; cut_short "$S/restore-swallow/$SRC/cloud_restore" 'rclone lsf --dirs-only qa:/ROCKNIX/ >/dev/null 2>&1; exit 0'
run() {  # <tool> <source root> <case> <out> [extra]
  env -u TMPDIR python3 -I "$1" --source-root "$2" --rclone "$RC" --output "$4" --case "$3" ${5:-} > "$4.txt" 2>&1; echo $?
}
for m in backup-noop:T24-local-legacy-recovery:--archives-only settle-skip:T17-seed-failed: restore-swallow:T18-bucket-restore-unknown:; do
  mut=${m%%:*}; rest=${m#*:}; case_=${rest%%:*}; extra=${rest#*:}
  ro=$(run "$OLD/rasteratops-cloud-layout-test" "$S/$mut" "$case_" "$S/$mut-old" "$extra")
  rn=$(run "$T/tools/rasteratops-cloud-layout-test" "$S/$mut" "$case_" "$S/$mut-new" "$extra")
  echo "  $mut ($case_): stage-D rc $ro | fixed rc $rn | $(grep -m1 '^FAIL' "$S/$mut-new.txt" | cut -c1-100)"
  check "stage-D credits the $mut mutation (the positive)" "$([ "$ro" = 0 ] && echo 0 || echo 1)"
  check "fixed fails the $mut mutation" "$([ "$rn" != 0 ] && echo 0 || echo 1)"
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
