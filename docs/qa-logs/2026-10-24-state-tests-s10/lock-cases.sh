#!/bin/bash
# lock-cases.sh -- T14 S10's control for #1003 (wait-lock-test): two copies of
# the tree's 001-functions, each changed one way, run by the stage-D test and
# the fixed one (the fixed one under the given image busybox):
#   fails-and-proceeds -- wait_lock takes the lock and then returns 1
#   check-then-create  -- wait_lock's atomic link replaced by "if absent, write it": a holder it can
#                         see is still honoured, but two acquirers that both find it absent both
#                         take it. A 0.1 s sleep inside the window is a named substitution: it
#                         widens the window the real race has, so the case does not depend on luck
# and the unchanged file by the fixed test. Nothing outside the scratch.
#   lock-cases.sh <tree> <stage-D tools dir> <image busybox> <scratch>
set -u
T="$(cd "$1" && pwd)"; OLD="$(cd "$2" && pwd)"; BB="$3"; S="$4"; rm -rf "${S:?}"; mkdir -p "$S/tmp"
F="$T/projects/ROCKNIX/packages/rocknix/profile.d/001-functions"
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
cp "$F" "$S/fails"; cp "$F" "$S/advisory"
# line 256 is the `return 0` after the trap; anchor on the trap line before it
awk 'prev ~ /trap .rc=\$\?; \[ "\$\(cat "\$\{J_CONF_LOCK\}"/ && $0 == "      return 0" { print "      return 1"; prev=$0; next } { print; prev=$0 }' "$F" > "$S/fails"
[ "$(diff "$F" "$S/fails" | grep -c '^>')" = 1 ] && grep -qx '      return 1' "$S/fails" || { echo "fails mutation did not apply"; exit 2; }
sed -i 's#^        ln -T "${J_CONF_LOCK}.$$" "${J_CONF_LOCK}" 2>/dev/null && took=1$#        [ -e "${J_CONF_LOCK}" ] || { sleep 0.1; echo "$$" > "${J_CONF_LOCK}"; took=1; }#' "$S/advisory"
[ "$(diff "$F" "$S/advisory" | grep -c '^>')" = 1 ] || { echo "advisory mutation did not apply"; exit 2; }
run() { TMPDIR="$S/tmp" bash "$@" > "$S/out" 2>&1; echo $?; }
o1=$(run "$OLD/wait-lock-test" "$S/fails"); cp "$S/out" "$S/old-fails.txt"
o2=$(run "$OLD/wait-lock-test" "$S/advisory"); cp "$S/out" "$S/old-advisory.txt"
n1=$(run "$T/tools/wait-lock-test" --busybox "$BB" "$S/fails"); cp "$S/out" "$S/new-fails.txt"
n2=$(run "$T/tools/wait-lock-test" --busybox "$BB" "$S/advisory"); cp "$S/out" "$S/new-advisory.txt"
n0=$(run "$T/tools/wait-lock-test" --busybox "$BB" "$F"); cp "$S/out" "$S/new-plain.txt"
echo "  stage-D: fails-and-proceeds rc $o1 ($(tail -1 "$S/old-fails.txt")) | check-then-create rc $o2 ($(tail -1 "$S/old-advisory.txt"))"
echo "  fixed:   fails-and-proceeds rc $n1 ($(tail -1 "$S/new-fails.txt")) | check-then-create rc $n2 ($(tail -1 "$S/new-advisory.txt")) | plain rc $n0 ($(tail -1 "$S/new-plain.txt"))"
grep -h 'FAIL' "$S/new-advisory.txt" | sed 's/^/    check-then-create: /' | head -3
check "stage-D passes a wait_lock that returns 1 and proceeds (the positive)" "$([ "$o1" = 0 ] && echo 0 || echo 1)"
check "stage-D passes a check-then-create lock (the positive)" "$([ "$o2" = 0 ] && echo 0 || echo 1)"
check "fixed fails the wait_lock that returns 1" "$([ "$n1" = 1 ] && echo 0 || echo 1)"
check "fixed fails the check-then-create lock in the race" "$([ "$n2" = 1 ] && grep -q 'FAIL  .*overlapped\|FAIL  the lock was not each one' "$S/new-advisory.txt" && echo 0 || echo 1)"
check "fixed passes the tree's wait_lock under the image busybox" "$([ "$n0" = 0 ] && grep -q '^  tools: BusyBox v1.36.1' "$S/new-plain.txt" && echo 0 || echo 1)"
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
