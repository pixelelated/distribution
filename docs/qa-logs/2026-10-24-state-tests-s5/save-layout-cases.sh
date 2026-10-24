#!/bin/bash
# save-layout-cases.sh -- T14 S5's control for #1005: two runs, each by the
# stage-D test and the fixed one. (1) --busybox with a selection that uses no
# applet (filter-psp, pure rclone); (2) --ref at a tree older than a source
# file today's tree has (bc2dceb406^, before cloud_connections.py), with the
# same pure-rclone selection. Outputs under the scratch only.
#   save-layout-cases.sh <tree> <stage-D tools dir> <rclone> <busybox> <scratch>
set -u
T="$(cd "$1" && pwd)"; OLD="$(cd "$2" && pwd)"; RC="$3"; BB="$4"; S="$5"; rm -rf "$S"; mkdir -p "$S"
REF=$(git -C "$T" rev-parse --short bc2dceb406^)
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
for side in old:"$OLD/pixelelated-save-layout-test" new:"$T/tools/pixelelated-save-layout-test"; do
  n=${side%%:*}; t=${side#*:}
  python3 -I "$t" --source-root "$T" --rclone "$RC" --busybox "$BB" --output "$S/$n-psp" --cases filter-psp > "$S/$n-psp.txt" 2>&1; a=$?
  python3 -I "$t" --source-root "$T" --ref "$REF" --rclone "$RC" --output "$S/$n-ref" --cases filter-psp > "$S/$n-ref.txt" 2>&1; b=$?
  echo "  $n: --busybox --cases filter-psp rc $a | --ref $REF --cases filter-psp rc $b"
  if [ "$n" = old ]; then
    check "stage-D refuses a pure-rclone selection for applets it does not use (the positive)" "$([ "$a" != 0 ] && echo 0 || echo 1)"
    check "stage-D fails the receipt at a ref without a source today's tree has (the positive)" "$([ "$b" != 0 ] && echo 0 || echo 1)"
  else
    check "fixed runs the pure-rclone selection" "$([ "$a" = 0 ] && echo 0 || echo 1)"
    check "fixed writes the receipt from the ref's own files" "$([ "$b" = 0 ] && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
