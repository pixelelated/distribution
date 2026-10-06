#!/bin/bash
set -euo pipefail
TASK_OWNER=/tmp/pixelelated-p3-20261006/host-b09-01
TASK_SOURCE=/tmp/pixelelated-p3-20261006/patched-b09
TASK_REPO=/workspace/repos/rocknix.worktrees/conflict-resolution
test ! -e "$TASK_OWNER/start"
date -u +%FT%TZ > "$TASK_OWNER/start"
printf '%s\n' "$TASK_REPO/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
trap 'TASK_RC=$?; printf "%s\n" "$TASK_RC" > "$TASK_OWNER/inner.rc"' EXIT
sha256sum -c "$TASK_OWNER/inputs.sha256" > "$TASK_OWNER/input-verification.log"
tools/pkgcheck raofflineproxy > "$TASK_OWNER/pkgcheck.log" 2>&1
tools/rc-preflight --only proxy-schema > "$TASK_OWNER/schema-note.log" 2>&1
bash "$TASK_OWNER/build-native.sh" > "$TASK_OWNER/native-build.log" 2>&1
export RAOFFLINEPROXY_RCHASH_LIB="$TASK_SOURCE/.host-qualification-b09/libraproxy_rchash.so"
sha256sum "$RAOFFLINEPROXY_RCHASH_LIB" > "$TASK_OWNER/native-library.sha256"
cd "$TASK_SOURCE"
PYTHONPATH=. RAOFFLINEPROXY_CONFIG_DIR="$TASK_OWNER/patched-config" python3 -m unittest discover -v -s linux/tests -p 'test_linux_*.py' > "$TASK_OWNER/patched.log" 2>&1
! grep -E 'skipped=| skipped ' "$TASK_OWNER/patched.log"
cd "$TASK_REPO"
tools/raofflineproxy-integration-test --source "$TASK_SOURCE" --predecessor-source /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement12/build.pixelelated-GENERIC_X64.x86_64/build/raofflineproxy-3036478f2b2d22db451396a48f44feee94e8462f > "$TASK_OWNER/integration.log" 2>&1
tools/raofflineproxy-integration-test --source "$TASK_SOURCE" --predecessor-source /tmp/pixelelated-proxy-865e21/patched > "$TASK_OWNER/historical-integration.log" 2>&1
sha256sum -c "$TASK_OWNER/inputs.sha256" > "$TASK_OWNER/final-input-verification.log"
echo 'PASS new coupled native build, full upstream Linux suite with no native skips and fork integration'
