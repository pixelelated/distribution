#!/bin/bash
set -euo pipefail
TASK_OWNER=/tmp/pixelelated-proxy-7252fc/upstream-tests02
[ ! -e "$TASK_OWNER/start" ]
date -u +%FT%TZ > "$TASK_OWNER/start"
printf '%s\n' "/workspace/repos/rocknix.worktrees/conflict-resolution/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
trap 'TASK_RC=$?; printf "%s\n" "$TASK_RC" > "$TASK_OWNER/inner.rc"' EXIT
cd /tmp/pixelelated-proxy-7252fc/new/RAOfflineProxy-7252fc781392d45b22f50d1a92f9febc4d1fa172
PYTHONPATH=. RAOFFLINEPROXY_CONFIG_DIR="$TASK_OWNER/pristine-config" python3 -m unittest discover -v -s linux/tests -p 'test_linux_*.py' > "$TASK_OWNER/pristine.log" 2>&1
cd /tmp/pixelelated-proxy-7252fc/patched-v4
PYTHONPATH=. RAOFFLINEPROXY_CONFIG_DIR="$TASK_OWNER/patched-config" python3 -m unittest discover -v -s linux/tests -p 'test_linux_*.py' > "$TASK_OWNER/patched.log" 2>&1
