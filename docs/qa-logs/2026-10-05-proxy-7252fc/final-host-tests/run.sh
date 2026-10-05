#!/bin/bash
set -euo pipefail
TASK_OWNER=/tmp/pixelelated-proxy-7252fc/final-host-tests
TASK_SOURCE=/tmp/pixelelated-proxy-7252fc/patched-v6
TASK_REPO=/workspace/repos/rocknix.worktrees/conflict-resolution
[ ! -e "$TASK_OWNER/start" ]
date -u +%FT%TZ > "$TASK_OWNER/start"
printf '%s\n' "$TASK_REPO/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
trap 'TASK_RC=$?; printf "%s\n" "$TASK_RC" > "$TASK_OWNER/inner.rc"' EXIT
export RAOFFLINEPROXY_RCHASH_LIB=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement06/build.pixelelated-GENERIC_X64.x86_64/image/system/usr/lib/libraproxy_rchash.so
sha256sum "$RAOFFLINEPROXY_RCHASH_LIB" > "$TASK_OWNER/native-library.sha256"
cd "$TASK_SOURCE"
PYTHONPATH=. RAOFFLINEPROXY_CONFIG_DIR="$TASK_OWNER/patched-config" python3 -m unittest discover -v -s linux/tests -p 'test_linux_*.py' > "$TASK_OWNER/patched.log" 2>&1
cd "$TASK_REPO"
tools/raofflineproxy-integration-test --source "$TASK_SOURCE" --predecessor-source /tmp/pixelelated-proxy-865e21/patched > "$TASK_OWNER/integration.log" 2>&1
export QA_SYSTEM_ROOT=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement06/build.pixelelated-GENERIC_X64.x86_64/image/system
export SOURCES_DIR=/tmp/pixelelated-proxy-7252fc/source-cache
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
python3 -c 'import os,signal; signal.signal(signal.SIGINT,signal.SIG_DFL); signal.signal(signal.SIGQUIT,signal.SIG_DFL); os.execv("./tools/last-good-scripts-test",["./tools/last-good-scripts-test"])' > "$TASK_OWNER/scripts.log" 2>&1
