#!/bin/bash
# melonds-cases.sh -- T14 S8's control for #997 (melonds-upgrade-test): the
# stage-D test and the fixed one, over the tree's post-update, with:
#   host       -- the host's busybox as --busybox
#   unverified -- the same with --unverified-busybox (fixed only)
#   root       -- the build root's busybox
#   standin    -- a copy of it under a scratch tree shaped like a build root, a stand-in BUILD_ID in its etc/os-release
#   declared   -- a copy outside any root, with --busybox-from naming the image's BUILD_ID (fixed only)
# Each run has its own TMPDIR under the scratch. Nothing outside the scratch.
#   melonds-cases.sh <tree> <stage-D tools dir> <build root's image/system/usr/bin/busybox> <scratch>
set -u
T="$(cd "$1" && pwd)"; OLD="$(cd "$2" && pwd)"; BB="$3"; S="$4"; rm -rf "$S"; mkdir -p "$S"
PU="$T/projects/ROCKNIX/packages/rocknix/sources/post-update"
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
mkdir -p "$S/standin/image/system/usr/bin" "$S/standin/image/system/etc" "$S/loose"
cp "$BB" "$S/standin/image/system/usr/bin/busybox"; cp "$BB" "$S/loose/busybox"
printf 'NAME="stand-in"\nBUILD_ID="standin0000000000000000000000000000000000"\n' > "$S/standin/image/system/etc/os-release"
run() {  # <name> <tool> <busybox> [extra...]: prints rc
  local n=$1 t=$2 b=$3; shift 3; mkdir -p "$S/$n-tmp"
  TMPDIR="$S/$n-tmp" python3 -I "$t" --post-update "$PU" --busybox "$b" --output "$S/$n.json" "$@" > "$S/$n.txt" 2>&1; echo $?
}
counts() { echo "$(grep -c '^PASS' "$S/$1.txt") PASS $(grep -c '^FAIL' "$S/$1.txt") FAIL"; }
for side in old:"$OLD/melonds-upgrade-test" new:"$T/tools/melonds-upgrade-test"; do
  n=${side%%:*}; t=${side#*:}
  h=$(run "$n-host" "$t" /usr/bin/busybox); r=$(run "$n-root" "$t" "$BB"); si=$(run "$n-standin" "$t" "$S/standin/image/system/usr/bin/busybox")
  echo "  $n: host rc $h ($(counts $n-host)) | root rc $r ($(counts $n-root)) | stand-in rc $si ($(counts $n-standin))"
  if [ "$n" = old ]; then
    check "stage-D runs the host busybox and passes it as the candidate's (the positive)" "$([ "$h" = 0 ] && echo 0 || echo 1)"
    check "stage-D's receipt names no origin for the busybox (the positive)" "$(grep -q busybox_origin "$S/$n-host.json" && echo 1 || echo 0)"
  else
    u=$(run "$n-unverified" "$t" /usr/bin/busybox --unverified-busybox)
    dc=$(run "$n-declared" "$t" "$S/loose/busybox" --busybox-from 1a026648442321609b2288c2c9c06803817f9df2)
    lines=$(grep -cE '^(PASS|FAIL) ' "$S/$n-unverified.txt"); marked=$(grep -cE "^(PASS|FAIL) .* -- host busybox, not the candidate's$" "$S/$n-unverified.txt")
    echo "  $n: unverified rc $u, $marked of $lines lines marked | declared rc $dc ($(counts $n-declared))"
    check "fixed refuses the host busybox bare, exit 2" "$([ "$h" = 2 ] && grep -q 'not under a build root' "$S/$n-host.txt" && echo 0 || echo 1)"
    check "fixed with --unverified-busybox exits 3 with the marker on every line" "$([ "$u" = 3 ] && [ "$lines" -gt 0 ] && [ "$marked" = "$lines" ] && echo 0 || echo 1)"
    check "fixed passes the build root's busybox and names its BUILD_ID" "$([ "$r" = 0 ] && grep -q 'BUILD_ID 1a026648442321609b2288c2c9c06803817f9df2' "$S/$n-root.txt" && echo 0 || echo 1)"
    check "fixed accepts the stand-in root, its id in the receipt" "$([ "$si" = 0 ] && grep -q '"build_id": "standin0000000000000000000000000000000000"' "$S/$n-standin.json" && echo 0 || echo 1)"
    check "fixed accepts a declared origin and records it" "$([ "$dc" = 0 ] && grep -q '"from": "1a026648442321609b2288c2c9c06803817f9df2"' "$S/$n-declared.json" && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
