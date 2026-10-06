#!/bin/bash
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement14
TASK_OWNER=/workspace/tmp/pixelelated-m7-cloud-01
TASK_BUNDLE=$(realpath "${1:?immutable candidate bundle required}")
cd "$TASK_TREE"
export VM_PAIR_DIR="$TASK_OWNER/pair"
export CLOUD_QA_STATE="$TASK_OWNER/cloud"
export CLOUD_QA_NAME=pixelelated-m7-cloud-01-s3
export ROCKNIX_ARTIFACTS="$TASK_OWNER/artifacts"
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
test ! -e "$TASK_OWNER/qa.start"
sha256sum -c "$TASK_OWNER/harness.sha256"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
python3 - <<'CHECK'
from pathlib import Path
import socket,os
for entry in Path('/proc').glob('[0-9]*/cmdline'):
    try: first = entry.read_bytes().split(b'\0',1)[0].decode()
    except (OSError,UnicodeError): continue
    if Path(first).name.startswith('qemu-system-'):
        raise SystemExit('existing QEMU: '+entry.parent.name)
for port in [9010,9011,9012,9013,10022,10023]:
    with socket.socket() as s: s.bind(('127.0.0.1',port))
v=os.statvfs('/workspace')
assert v.f_bavail*v.f_frsize > 64*1024**3, '64 GiB QA capacity margin required'
CHECK
printf '%s\n' "$TASK_TREE/${RASTERATOPS_BUILD_RUN:?run through tools/watch-build}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
cleanup() {
  result=$?
  trap - EXIT
  ./tools/vm-pair down || result=1
  for backend in webdav sftp s3; do
    ./tools/cloud-test-backend --backend "$backend" down || result=1
  done
  printf '%s\n' "$result" > "$TASK_OWNER/inner.rc"
  exit "$result"
}
trap cleanup EXIT
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
./tools/vm-pair up "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz"
python3 "$TASK_OWNER/check-payload.py" local-cloud
./tools/vm-pair ssh a 'rclone version; sha256sum /usr/bin/rclone' > "$TASK_OWNER/artifacts/installed-rclone.txt"
failures=0
for backend in webdav sftp s3; do
  echo "BEGIN local cloud backend $backend $(date -u +%FT%TZ)"
  if ./tools/vm-qa --skip-up --only round-trip --backend "$backend" "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz"; then
    echo "PASS backend suite $backend"
  else
    failures=$((failures + 1))
    echo "FAIL backend suite $backend"
  fi
  ./tools/cloud-test-backend --backend "$backend" down
  echo "END local cloud backend $backend $(date -u +%FT%TZ)"
done
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
test "$failures" = 0
echo 'PASS all three local cloud round-trip suites on frozen replacement14'
