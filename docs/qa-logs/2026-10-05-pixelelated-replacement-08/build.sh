#!/bin/bash
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement08
TASK_OWNER=/workspace/tmp/pixelelated-m7-replacement-08
TASK_CONTAINER_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated
TASK_CACHE=/workspace/cache/rocknix-sources
# Refuse the wrong watcher root before cleaning any package (#435).
[ "$(pwd -P)" = "$TASK_TREE" ] || { echo "Refusing build: start watch-build from the frozen worktree" >&2; exit 2; }
cd "$TASK_TREE"
[ "$(id -u)" = 1000 ]
[ ! -e "$TASK_OWNER/build.start" ]
[ "$(cat "$TASK_OWNER/cache-ready.rc")" = 0 ]
[ -f "$TASK_OWNER/cache-ready.json" ]
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
for TASK_PACKAGE in emulationstation; do
 PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64 PACKAGE="$TASK_PACKAGE" make docker-package-clean
done
rm -f build.pixelelated-GENERIC_X64.x86_64/.stamps/image/build_target
make docker-GENERIC_X64
python3 "$TASK_OWNER/verify-source.py"
python3 - <<'PY'
from pathlib import Path
import json
j=json.loads(Path('/workspace/tmp/pixelelated-m7-replacement-08/inputs.json').read_text())
root=Path(j['build_root'])/'image/system'
release=(root/'etc/os-release').read_text()
assert 'OS_NAME="pixelelated"' in release and j['distribution_commit'] in release and j['distribution_branch'] in release
assert (root/'usr/bin/raofflineproxy-ctl').read_bytes()==Path('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl').read_bytes()
for p in ['LICENSE.md','TRADEMARK.md']:
 assert (root/'usr/share/licenses/pixelelated'/p).read_bytes()==Path(p).read_bytes(),p
import xml.etree.ElementTree as ET
for installed,source in [('etc/profile.d/999-export','projects/ROCKNIX/packages/hardware/quirks/profile.d/999-export'),('etc/profile.d/001-functions','projects/ROCKNIX/packages/rocknix/profile.d/001-functions'),('usr/bin/chksysconfig','projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig'),('usr/config/modules/gamelist.xml','projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml'),('usr/bin/cloud_setup','projects/ROCKNIX/packages/network/rclone/sources/cloud_setup'),('usr/bin/rocknix-memory-manager','projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-memory-manager')]:
 assert (root/installed).read_bytes()==Path(source).read_bytes(),installed
ET.parse(root/'usr/config/modules/gamelist.xml')
import subprocess
child=subprocess.run(['/bin/sh','-c',"OS_NAME=pixelelated; OS_VERSION=0.0.1; OS_BUILD=community; . \"$1\"; exec /bin/sh -c 'printf \"%s\\n\" \"${OS_NAME-unset}\" \"${OS_VERSION-unset}\" \"${OS_BUILD-unset}\"'",'assembled-export',str(root/'etc/profile.d/999-export')],env={'PATH':'/usr/bin:/bin'},text=True,capture_output=True)
assert child.returncode==0 and not child.stderr and child.stdout.splitlines()==['pixelelated','0.0.1','community'],(child.returncode,child.stdout,child.stderr)
init=(Path(j['build_root'])/'initramfs/init').read_text()
assert '[ \"GENERIC_X64\" = \"GENERIC_X64\" ] && [ \"${DEBUG}\" != \"yes\" ]' in init
assert '@DEVICENAME@' not in init
assert 'quiet console=ttyS0,115200 console=tty0' in Path('projects/ROCKNIX/devices/GENERIC_X64/options').read_text()
print('PASS assembled initramfs quiet fallback, OS_NAME export, XML/text, proxy, identity and licence payload',flush=True)
PY
