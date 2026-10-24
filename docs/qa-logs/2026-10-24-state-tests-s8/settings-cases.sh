#!/bin/bash
# settings-cases.sh -- T14 S8's control for #997 (settings-modes-test): the
# stage-D test and the fixed one, over the tree's profile.d/001-functions and
# chksysconfig, with:
#   host       -- the host's busybox as --busybox
#   unverified -- the same with --unverified-busybox (fixed only: stage D has no such flag),
#                 over the tree's functions and over the gnu-only copy below (a failing case)
#   root       -- the build root's busybox
#   standin    -- a copy of it under a scratch tree shaped like a build root, whose etc/os-release names a stand-in BUILD_ID
#   space      -- the build root's busybox with a TMPDIR whose path holds a space
#   gnu-only   -- a copy of 001-functions whose settings_base reads the live file with `cat --squeeze-blank`, an option the image's busybox cat lacks
# Each run has its own TMPDIR under the scratch. Nothing outside the scratch.
#   settings-cases.sh <tree> <stage-D tools dir> <build root's image/system/usr/bin/busybox> <scratch>
set -u
T="$(cd "$1" && pwd)"; OLD="$(cd "$2" && pwd)"; BB="$3"; S="$4"; rm -rf "${S:?}"; mkdir -p "$S"
PROF="$T/projects/ROCKNIX/packages/rocknix/profile.d/001-functions"; CK="$T/projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig"
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
mkdir -p "$S/standin/image/system/usr/bin" "$S/standin/image/system/etc"
cp "$BB" "$S/standin/image/system/usr/bin/busybox"; printf 'NAME="stand-in"\nBUILD_ID="standin0000000000000000000000000000000000"\n' > "$S/standin/image/system/etc/os-release"
cp "$PROF" "$S/gnu-only-functions"; sed -i 's#^    cat "${J_CONF}"$#    cat --squeeze-blank "${J_CONF}"#' "$S/gnu-only-functions"
[ "$(grep -c '^    cat --squeeze-blank "${J_CONF}"$' "$S/gnu-only-functions")" = 1 ] || { echo "gnu-only mutation did not apply"; exit 2; }
run() {  # <name> <tool> <profile> <busybox> [extra...]: prints rc; only a *-space run's TMPDIR holds a space
  local n=$1 t=$2 pr=$3 b=$4 d; shift 4; case "$n" in *-space) d="$S/$n tmp";; *) d="$S/$n-tmp";; esac; mkdir -p "$d"
  TMPDIR="$d" python3 -I "$t" --profile "$pr" --chksysconfig "$CK" --busybox "$b" --output "$S/$n.json" "$@" > "$S/$n.txt" 2>&1; echo $?
}
counts() { echo "$(grep -c '^PASS' "$S/$1.txt") PASS $(grep -c '^FAIL' "$S/$1.txt") FAIL"; }
for side in old:"$OLD/settings-modes-test" new:"$T/tools/settings-modes-test"; do
  n=${side%%:*}; t=${side#*:}
  h=$(run "$n-host" "$t" "$PROF" /usr/bin/busybox)
  r=$(run "$n-root" "$t" "$PROF" "$BB")
  si=$(run "$n-standin" "$t" "$PROF" "$S/standin/image/system/usr/bin/busybox")
  g=$(run "$n-gnu-only" "$t" "$S/gnu-only-functions" "$BB")
  sp=$(run "$n-space" "$t" "$PROF" "$BB")
  echo "  $n: host rc $h ($(counts $n-host)) | root rc $r ($(counts $n-root)) | stand-in rc $si ($(counts $n-standin)) | gnu-only rc $g ($(counts $n-gnu-only)) | space rc $sp ($(counts $n-space))"
  if [ "$n" = old ]; then
    check "stage-D runs the host busybox and passes it as the candidate's (the positive)" "$([ "$h" = 0 ] && echo 0 || echo 1)"
    check "stage-D passes a writer using a GNU-only cat option: cat falls through to the host (the positive)" "$([ "$g" = 0 ] && echo 0 || echo 1)"
    check "stage-D breaks under a TMPDIR with a space: the unquoted wrapper (the positive)" "$(grep -q '^FAIL' "$S/$n-space.txt" && echo 0 || echo 1)"
  else
    u=$(run "$n-unverified" "$t" "$PROF" /usr/bin/busybox --unverified-busybox)
    lines=$(grep -cE '^(PASS|FAIL) ' "$S/$n-unverified.txt"); marked=$(grep -cE "^(PASS|FAIL) .* -- host busybox, not the candidate's$" "$S/$n-unverified.txt")
    uf=$(run "$n-unverified-failing" "$t" "$S/gnu-only-functions" /usr/bin/busybox --unverified-busybox)
    flines=$(grep -cE '^(PASS|FAIL) ' "$S/$n-unverified-failing.txt"); fmarked=$(grep -cE "^(PASS|FAIL) .* -- host busybox, not the candidate's$" "$S/$n-unverified-failing.txt")
    echo "  $n: unverified rc $u, $marked of $lines result lines marked | unverified with a failing case rc $uf ($(counts $n-unverified-failing)), $fmarked of $flines marked"
    check "fixed refuses the host busybox bare, exit 2, naming the remedy" "$([ "$h" = 2 ] && grep -q 'not under a build root' "$S/$n-host.txt" && echo 0 || echo 1)"
    check "fixed with --unverified-busybox exits 3 with the marker on every line" "$([ "$u" = 3 ] && [ "$lines" -gt 0 ] && [ "$marked" = "$lines" ] && echo 0 || echo 1)"
    check "fixed with --unverified-busybox and a failing case exits 1, the marker still on every line" "$([ "$uf" = 1 ] && grep -q '^FAIL' "$S/$n-unverified-failing.txt" && [ "$fmarked" = "$flines" ] && echo 0 || echo 1)"
    check "fixed passes the build root's busybox and names its BUILD_ID" "$([ "$r" = 0 ] && grep -q 'BUILD_ID 1a026648442321609b2288c2c9c06803817f9df2' "$S/$n-root.txt" && echo 0 || echo 1)"
    check "fixed accepts the stand-in build root, its id in the result" "$([ "$si" = 0 ] && grep -q '"build_id": "standin0000000000000000000000000000000000"' "$S/$n-standin.json" && echo 0 || echo 1)"
    check "fixed fails the GNU-only writer: cat is the image's busybox" "$([ "$g" = 1 ] && echo 0 || echo 1)"
    check "fixed passes under a TMPDIR with a space" "$([ "$sp" = 0 ] && ! grep -q '^FAIL' "$S/$n-space.txt" && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
