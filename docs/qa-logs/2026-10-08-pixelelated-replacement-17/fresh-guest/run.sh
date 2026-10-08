#!/bin/bash
set -euo pipefail
cd /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement17
test ! -e /workspace/tmp/pixelelated-m7-cf10-17/guest03/qa.start
sha256sum -c /workspace/tmp/pixelelated-m7-cf10-17/guest03/harness.sha256
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?use watch-build}" > /workspace/tmp/pixelelated-m7-cf10-17/guest03/run.path
date -u +%Y-%m-%dT%H:%M:%SZ > /workspace/tmp/pixelelated-m7-cf10-17/guest03/qa.start
trap 'result=$?; printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-cf10-17/guest03/inner.rc' EXIT
python3 -I -u /workspace/tmp/pixelelated-m7-cf10-17/guest03/create.py "${1:?immutable bundle required}"
