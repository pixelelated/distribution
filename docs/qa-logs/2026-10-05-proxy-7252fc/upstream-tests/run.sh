#!/bin/bash
set -euo pipefail
TASK_OWNER=/tmp/pixelelated-proxy-7252fc/upstream-tests
TASK_SOURCE=/tmp/pixelelated-proxy-7252fc/patched-v3
[ ! -e "$TASK_OWNER/start" ]
date -u +%FT%TZ > "$TASK_OWNER/start"
printf '%s\n' "/workspace/repos/rocknix.worktrees/conflict-resolution/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
trap 'TASK_RC=$?; printf "%s\n" "$TASK_RC" > "$TASK_OWNER/inner.rc"' EXIT
cd "$TASK_SOURCE"
PYTHONPATH=. RAOFFLINEPROXY_CONFIG_DIR="$TASK_OWNER/config" python3 -m unittest discover -s linux/tests -p 'test_linux_*.py' > "$TASK_OWNER/tests.log" 2>&1
