#!/bin/bash
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement01
TASK_OWNER=/workspace/tmp/pixelelated-m7-replacement-01
TASK_CONTAINER_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated
TASK_CACHE=/workspace/cache/rocknix-sources
cd "$TASK_TREE"
[ "$(id -u)" = 1000 ]
[ ! -e "$TASK_OWNER/build.start" ]
[ "$(cat "$TASK_OWNER/copy.rc")" = 0 ]
[ -f "$TASK_OWNER/copy.finish" ]
[ ! -s "$TASK_OWNER/cache-compare.txt" ]
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
  printf '%s\n' "$result" > "$TASK_OWNER/inner.rc"
  exit "$result"
}
trap finish EXIT
export DOCKER_WORK_DIR="$TASK_CONTAINER_TREE"
export DOCKER_EXTRA_OPTS="-v /workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git -v $TASK_CACHE:$TASK_CONTAINER_TREE/sources"
PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64 PACKAGE=raofflineproxy make docker-package-clean
rm -f build.pixelelated-GENERIC_X64.x86_64/.stamps/image/build_target
make docker-GENERIC_X64
python3 "$TASK_OWNER/verify-source.py"
python3 - <<'PY'
from pathlib import Path
import json
j=json.loads(Path('/workspace/tmp/pixelelated-m7-replacement-01/inputs.json').read_text())
root=Path(j['build_root'])/'image/system'
release=(root/'etc/os-release').read_text()
assert 'OS_NAME="pixelelated"' in release and j['distribution_commit'] in release and j['distribution_branch'] in release
assert (root/'usr/bin/raofflineproxy-ctl').read_bytes()==Path('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl').read_bytes()
for p in ['LICENSE.md','TRADEMARK.md']:
 assert (root/'usr/share/licenses/pixelelated'/p).read_bytes()==Path(p).read_bytes(),p
print('PASS assembled corrected proxy bytes and new identity/licence payload',flush=True)
PY
