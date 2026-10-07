#!/bin/bash
# Prepared, not executed: defaults and actual ROCKNIX RC2 adoption.
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16
TASK_OWNER=/workspace/tmp/pixelelated-m7-qa-20
TASK_BUNDLE=$(realpath "${1:?immutable candidate bundle required}")
cd "$TASK_TREE"
export VM_PAIR_DIR="$TASK_OWNER/pair"
export CLOUD_QA_STATE="$TASK_OWNER/cloud"
export ROCKNIX_ARTIFACTS="$TASK_OWNER/artifacts"
export CLOUD_QA_BACKEND=webdav
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
export RETROARCH_SRC="$TASK_TREE/build.pixelelated-GENERIC_X64.x86_64"
export QA_SYSTEM_ROOT="$RETROARCH_SRC/image/system"
export WALK_BASELINE=/workspace/artifacts/rocknix-images/walk-baseline
test -d "$WALK_BASELINE"
test ! -e "$TASK_OWNER/qa.start"
test "$(cat /workspace/tmp/pixelelated-m7-consent-02/outer.rc)" = 0
test "$(cat /workspace/tmp/pixelelated-m7-image-16/outer.rc)" = 0
sha256sum -c "$TASK_OWNER/harness.sha256"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
# vm-pair owns fixed ports and sockets. Refuse to disturb another guest.
python3 - <<'PY'
from pathlib import Path
for entry in Path('/proc').glob('[0-9]*/cmdline'):
    try:
        first = entry.read_bytes().split(b'\0', 1)[0].decode()
    except (OSError, UnicodeError):
        continue
    if Path(first).name.startswith('qemu-system-'):
        raise SystemExit('QA launch refused: existing QEMU PID ' + entry.parent.name)
PY
mkdir -p "$ROCKNIX_ARTIFACTS"
printf '%s\n' "$TASK_TREE/${RASTERATOPS_BUILD_RUN:?run through tools/watch-build}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
cleanup() {
  result=$?
  trap - EXIT
  ./tools/vm-pair down || result=1
  ./tools/cloud-test-backend down || result=1
  printf '%s\n' "$result" > "$TASK_OWNER/inner.rc"
  exit "$result"
}
trap cleanup EXIT
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
./tools/vm-pair up "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz"
python3 "$TASK_OWNER/check-payload.py" initial-clean
python3 "$TASK_OWNER/verify-renderer.py" virgl initial-clean --port 10022 --key "$VM_PAIR_DIR/qa-key" --out "$TASK_OWNER/artifacts"
python3 "$TASK_OWNER/identity-frames.py" initial-clean
./tools/vm-qa --skip-up "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz"
python3 "$TASK_OWNER/check-payload.py" clean
./tools/vm-upgrade-rehearsal \
 /workspace/artifacts/rocknix-images/x64-all-20260929-69e6039f8f/ROCKNIX-GENERIC_X64.x86_64-20260929.img.gz \
 "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.tar" \
 ee01490913
# The rehearsal stops both guests. Restart its actual upgraded disk for readback.
./projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm run --headless --daemonize "$VM_PAIR_DIR/vm-a.qcow2"
./tools/vm-serial wait --up-to 300
python3 "$TASK_OWNER/check-payload.py" upgrade
python3 "$TASK_OWNER/verify-renderer.py" virgl upgrade-virgl --port 10022 --key "$VM_PAIR_DIR/qa-key" --out "$TASK_OWNER/artifacts"
python3 "$TASK_OWNER/identity-frames.py" upgrade
./tools/vm-pair ssh a sync
./tools/vm-pair down
./projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm run --headless --daemonize --gl none --res 640x480 "$VM_PAIR_DIR/vm-a.qcow2"
./tools/vm-serial wait --up-to 300
TASK_PUBLIC=$(cat "$VM_PAIR_DIR/qa-key.pub")
./tools/vm-serial sh "mkdir -p /storage/.ssh && chmod 700 /storage/.ssh && echo '$TASK_PUBLIC' >> /storage/.ssh/authorized_keys && chmod 600 /storage/.ssh/authorized_keys && sync" >/dev/null
python3 "$TASK_OWNER/check-payload.py" upgrade-software
python3 "$TASK_OWNER/verify-renderer.py" software upgrade-software --port 10022 --key "$VM_PAIR_DIR/qa-key" --out "$TASK_OWNER/artifacts"
python3 "$TASK_OWNER/identity-frames.py" upgrade-software
./tools/vm-pair ssh a sync

./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
echo 'PASS pixelelated defaults, actual ROCKNIX RC2 upgrade and exact payload readback'
