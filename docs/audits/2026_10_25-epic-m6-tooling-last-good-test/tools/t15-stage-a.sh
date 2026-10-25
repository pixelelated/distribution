#!/bin/bash
# t15-stage-a.sh -- T15's stage-A runs of tools/last-good-scripts-test, in the
# order the brief's § 5 gives: the image's busybox (QA_SYSTEM_ROOT on the
# 069fc2704421 M7 root, read only), the host's (QA_SYSTEM_ROOT unset), then
# the twelve --old recipes of the header (:167-226) under the image's. Each run
# starts through vm-qa:158's launcher, SIGINT and SIGPIPE at default, with
# TMPDIR under /workspace/tmp/m6-t15/. One summary line per run on stdout;
# each run's output in .qa-scratch/t15/. No guest; nothing written outside
# the scratch and the temp root.
#   t15-stage-a.sh <worktree>
set -u
D="$(cd "$1" && pwd)"; cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t15/tmp; mkdir -p "$TMPDIR" .qa-scratch/t15
R7=/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system
SIGDFL='import os, signal, sys; signal.signal(signal.SIGINT, signal.SIG_DFL); signal.signal(signal.SIGPIPE, signal.SIG_DFL); os.execv(sys.argv[1], sys.argv[1:])'
echo "root: $("$R7/usr/bin/busybox" 2>&1 | head -1); $(sed -n 's/^BUILD_ID=//p' "$R7/etc/os-release")"
summary() {  # <label> <file> <rc> <seconds>
  printf '%s rc=%s %ss PASS=%s FAIL=%s SKIP=%s | first: %s | banner: %s | last: %s\n' "$1" "$3" "$4" \
    "$(grep -c '^    PASS  ' "$2")" "$(grep -c '^    FAIL  ' "$2")" "$(grep -c '^    SKIP  ' "$2")" \
    "$(head -1 "$2" | cut -c1-90)" "$(grep -m1 'a copy of' "$2" | cut -c1-120)" "$(tail -1 "$2" | cut -c1-80)"
}
s=$(date +%s); QA_SYSTEM_ROOT="$R7" python3 -c "$SIGDFL" tools/last-good-scripts-test > .qa-scratch/t15/run-image.out 2>&1; rc=$?; summary image .qa-scratch/t15/run-image.out $rc $(( $(date +%s) - s ))
s=$(date +%s); env -u QA_SYSTEM_ROOT python3 -c "$SIGDFL" tools/last-good-scripts-test > .qa-scratch/t15/run-host.out 2>&1; rc=$?; summary host .qa-scratch/t15/run-host.out $rc $(( $(date +%s) - s ))
for ref in 1d1503180d 53f390b1e9 c15050c897 8707919349 34aca64afd 0f7785e6ed d79281066c cee1656c33 28a80357ed 3387cf5da0 655f103cc5 70b6c70ca7; do
  s=$(date +%s); QA_SYSTEM_ROOT="$R7" BASE_REF=$ref python3 -c "$SIGDFL" tools/last-good-scripts-test --old > ".qa-scratch/t15/old-$ref.out" 2>&1; rc=$?
  summary "--old $ref" ".qa-scratch/t15/old-$ref.out" $rc $(( $(date +%s) - s ))
done
echo "stage-a done $(date -u +%H:%M:%S)"
