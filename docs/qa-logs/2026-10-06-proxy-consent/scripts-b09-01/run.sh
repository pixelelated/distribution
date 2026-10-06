#!/bin/bash
set -euo pipefail
TASK_OWNER=/tmp/pixelelated-p3-20261006/scripts-b09-01
test ! -e "$TASK_OWNER/start"
date -u +%FT%TZ > "$TASK_OWNER/start"
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
trap 'TASK_RC=$?; printf "%s\n" "$TASK_RC" > "$TASK_OWNER/inner.rc"' EXIT
sha256sum -c "$TASK_OWNER/inputs.sha256" > "$TASK_OWNER/input-verification.log"
export QA_SYSTEM_ROOT=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement12/build.pixelelated-GENERIC_X64.x86_64/image/system
export SOURCES_DIR=/tmp/pixelelated-p3-20261006/source-cache
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
export RAOFFLINEPROXY_RCHASH_LIB=/tmp/pixelelated-p3-20261006/patched-b09/.host-qualification-b09/libraproxy_rchash.so
python3 -c 'import os,signal; signal.signal(signal.SIGINT,signal.SIG_DFL); signal.signal(signal.SIGQUIT,signal.SIG_DFL); os.execv("./tools/last-good-scripts-test",["./tools/last-good-scripts-test"])' > "$TASK_OWNER/scripts.log" 2>&1
sha256sum -c "$TASK_OWNER/inputs.sha256" > "$TASK_OWNER/final-input-verification.log"
echo 'PASS complete scripts suite on current b09 proxy and actual candidate12 applets'
