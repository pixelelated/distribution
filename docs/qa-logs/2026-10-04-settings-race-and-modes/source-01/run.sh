#!/bin/bash
set -euo pipefail
TASK_OWNER=/workspace/tmp/pixelelated-m7-settings-source-01
cd /workspace/repos/rocknix.worktrees/conflict-resolution
test ! -e "$TASK_OWNER/start"
sha256sum -c "$TASK_OWNER/sources.sha256"
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?use shared watcher}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/start"
finish() { result=$?; trap - EXIT; sha256sum -c "$TASK_OWNER/sources.sha256" || result=1; printf '%s\n' "$result" > "$TASK_OWNER/inner.rc"; exit "$result"; }
trap finish EXIT
export QA_SYSTEM_ROOT=/workspace/tmp/pixelelated-m7-image-05/root
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
python3 -c 'import os,signal;signal.signal(signal.SIGINT,signal.SIG_DFL);signal.signal(signal.SIGPIPE,signal.SIG_DFL);os.execv("./tools/last-good-scripts-test",["./tools/last-good-scripts-test"])' > "$TASK_OWNER/artifacts/scripts.log" 2>&1
