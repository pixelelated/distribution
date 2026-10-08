#!/bin/bash
# PREPARED ONLY: not launched as part of this worker's bounded task.
set -eu
cd /workspace/repos/rocknix.worktrees/conflict-resolution
qa_owner="$(mktemp -d /workspace/tmp/pixelelated-last-good-validator-broad-XXXXXXXX)"
mkdir "${qa_owner}/tmp"
TMPDIR="${qa_owner}/tmp" tools/watch-build-submit --owner "${qa_owner}" -- \
  --activity-dir "${qa_owner}" -- \
  env LAST_GOOD_SOURCE_ROOT=/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders \
      QA_SYSTEM_ROOT=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64/image/system \
      SOURCES_DIR=/workspace/cache/rocknix-sources \
      tools/last-good-scripts-test
printf 'Actively consume console.log, launcher-result.json, tool-wrapper.rc and the announced .build-runs status/rc under %s\n' "${qa_owner}"
