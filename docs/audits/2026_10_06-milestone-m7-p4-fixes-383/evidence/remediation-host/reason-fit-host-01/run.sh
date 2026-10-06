#!/bin/bash
set -euo pipefail
TASK_OWNER=/workspace/tmp/pixelelated-m7-p4-reason-fit-host-01
cd /workspace/repos/rocknix.worktrees/conflict-resolution
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?watch-build required}" > "$TASK_OWNER/run.path"
date -u +%FT%TZ > "$TASK_OWNER/qa.start"
trap 'rc=$?; printf "%s\n" "$rc" > "$TASK_OWNER/inner.rc"; exit "$rc"' EXIT
export TMPDIR="$TASK_OWNER/tmp" CCACHE_DISABLE=1
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/m7-audit-remediation
sha256sum -c "$TASK_OWNER/harness.sha256"
tools/es-syntax-check --root /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15/build.pixelelated-GENERIC_X64.x86_64 "$ES_SRC/es-app/src/guis/GuiCloudTransfer.cpp" > "$TASK_OWNER/artifacts/syntax.log" 2>&1
cat "$TASK_OWNER/artifacts/syntax.log"
tools/vocabulary-check --es "$ES_SRC" > "$TASK_OWNER/artifacts/vocabulary.log" 2>&1
cat "$TASK_OWNER/artifacts/vocabulary.log"
git -C "$ES_SRC" diff --check
sha256sum -c "$TASK_OWNER/harness.sha256"
echo 'PASS source syntax and vocabulary; installed visual acceptance remains pending'
