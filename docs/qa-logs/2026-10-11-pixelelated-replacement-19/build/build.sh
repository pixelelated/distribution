#!/bin/bash
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement19
TASK_OWNER=/workspace/tmp/pixelelated-m7-build19
TASK_CONTAINER_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated
TASK_CACHE=/workspace/cache/rocknix-sources
# Refuse the wrong watcher root before cleaning any package (#435).
[ "$(pwd -P)" = "$TASK_TREE" ] || { echo "Refusing build: start watch-build from the frozen worktree" >&2; exit 2; }
cd "$TASK_TREE"
[ "$(id -u)" = 1000 ]
[ ! -e "$TASK_OWNER/build.start" ]
[ "$(cat /workspace/tmp/pixelelated-m7-cache19-recheck/cache-ready.rc)" = 0 ]
[ -f /workspace/tmp/pixelelated-m7-cache19-recheck/cache-ready.json ]
[ -z "$(git status --porcelain)" ]
python3 "$TASK_OWNER/verify-source.py"
tools/rc-preflight --only proxy-schema
tools/build-preflight > "$TASK_OWNER/host-preflight.txt"
cat "$TASK_OWNER/host-preflight.txt"
printf '%s\n' "$TASK_TREE/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/build.start"
finish() {
  result=$?
  trap - EXIT
  if [ -n "${TASK_OBSERVER_PID:-}" ]; then kill "$TASK_OBSERVER_PID" 2>/dev/null || true; wait "$TASK_OBSERVER_PID" 2>/dev/null || true; fi
  printf '%s\n' "$result" > "$TASK_OWNER/inner.rc"
  exit "$result"
}
trap finish EXIT
export BUILD_QUALIFIER=dev
export BUILD_TIMESTAMP="$(python3 -c 'import json; print(json.load(open("/workspace/tmp/pixelelated-m7-build19/inputs.json"))["build_timestamp"])')"
export DOCKER_WORK_DIR="$TASK_CONTAINER_TREE"
export DOCKER_EXTRA_OPTS="-v /workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git -v $TASK_CACHE:$TASK_CONTAINER_TREE/sources"
for TASK_PACKAGE in rocknix rclone raofflineproxy emulationstation sway cloud-signin-window idtech-lr; do
 PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64 PACKAGE="$TASK_PACKAGE" make docker-package-clean
done
rm -f build.pixelelated-GENERIC_X64.x86_64/.stamps/image/build_target
export DOCKER_EXTRA_OPTS="$DOCKER_EXTRA_OPTS --name pixelelated-m7-build19 --label pixelelated.m7.owner=replacement19 --cidfile $TASK_OWNER/build.cid"
python3 -I -u "$TASK_OWNER/observe-container.py" &
TASK_OBSERVER_PID=$!
printf '%s\n' "$TASK_OBSERVER_PID" > "$TASK_OWNER/observer.pid"
make docker-GENERIC_X64
wait "$TASK_OBSERVER_PID"
TASK_OBSERVER_PID=
test -s "$TASK_OWNER/container-observed.json"
python3 "$TASK_OWNER/verify-source.py"
python3 "$TASK_OWNER/verify-installed.py"
