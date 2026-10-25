#!/bin/bash
# t15-attribution.sh -- T15's attribution runs, after stage A: the suite under
# two constructed roots that each swap ONE dependency of the host run --
#   bbhost: the host's busybox (1.37.0) with the image's rclone (1.75.2)
#   rchost: the image's busybox (1.36.1) with the host's rclone (1.60.1-DEV)
# (each root under /workspace/tmp/m6-t15/roots/<name>/image/system, with the
# M7 image's avahi unit and os-release beside, so section m reads as in the
# image run) -- and one image run whose every output line is prefixed with
# the seconds since its start, for Q5's wall time by section. Started through
# vm-qa:158's launcher; TMPDIR under /workspace/tmp/m6-t15/. No guest.
#   t15-attribution.sh <worktree>
set -u
D="$(cd "$1" && pwd)"; cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t15/tmp; mkdir -p "$TMPDIR" .qa-scratch/t15
R7=/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system
SIGDFL='import os, signal, sys; signal.signal(signal.SIGINT, signal.SIG_DFL); signal.signal(signal.SIGPIPE, signal.SIG_DFL); os.execv(sys.argv[1], sys.argv[1:])'
summary() { printf '%s rc=%s %ss PASS=%s FAIL=%s SKIP=%s | first: %s | last: %s\n' "$1" "$3" "$4" "$(grep -c '^ *[0-9]* *    PASS  \|^    PASS  ' "$2")" "$(grep -c '^ *[0-9]* *    FAIL  \|^    FAIL  ' "$2")" "$(grep -c '    SKIP  ' "$2")" "$(head -1 "$2" | cut -c1-90)" "$(tail -1 "$2" | cut -c1-60)"; }
for n in bbhost rchost; do
  s=$(date +%s); QA_SYSTEM_ROOT=/workspace/tmp/m6-t15/roots/$n/image/system python3 -c "$SIGDFL" tools/last-good-scripts-test > ".qa-scratch/t15/run-$n.out" 2>&1; rc=$?
  summary "$n" ".qa-scratch/t15/run-$n.out" $rc $(( $(date +%s) - s ))
done
# the timed image run: python stamps each line with seconds since the start
s=$(date +%s)
QA_SYSTEM_ROOT="$R7" python3 -c "$SIGDFL" tools/last-good-scripts-test 2>&1 | python3 -I -u -c 'import sys,time
t0=time.monotonic()
for line in sys.stdin: sys.stdout.write("%8.1f %s" % (time.monotonic()-t0, line))' > .qa-scratch/t15/run-image-timed.out
rc=${PIPESTATUS[0]}
printf 'image-timed rc=%s %ss lines=%s last: %s\n' "$rc" $(( $(date +%s) - s )) "$(wc -l < .qa-scratch/t15/run-image-timed.out)" "$(tail -1 .qa-scratch/t15/run-image-timed.out | cut -c1-60)"
echo "attribution done $(date -u +%H:%M:%S)"
