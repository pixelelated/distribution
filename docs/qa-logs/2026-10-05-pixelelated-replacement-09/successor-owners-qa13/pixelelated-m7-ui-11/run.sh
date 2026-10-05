#!/bin/bash
# Candidate-bound VM qualification; Refs #383, #409.
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement09
TASK_OWNER=/workspace/tmp/pixelelated-m7-ui-11
TASK_BUNDLE=$(realpath "${1:?verified candidate bundle required}")
cd "$TASK_TREE"
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
export VM_PAIR_DIR="$TASK_OWNER/pair"
export CLOUD_QA_STATE="$TASK_OWNER/cloud" CLOUD_QA_BACKEND=webdav
export CLOUD_QA_PORT=9040 CLOUD_QA_NAME=pixelelated-m7-ui-10
export ROCKNIX_ARTIFACTS="$TASK_OWNER/artifacts"
test ! -e "$TASK_OWNER/qa.start"
test "$(cat /workspace/tmp/pixelelated-m7-memory-09/outer.rc)" = 0
sha256sum -c "$TASK_OWNER/harness.sha256"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
python3 - <<'CHECK'
from pathlib import Path
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try: name=Path(p.read_bytes().split(b'\0',1)[0].decode()).name
 except (FileNotFoundError,ProcessLookupError):continue
 if name.startswith('qemu-system-'):raise SystemExit('Existing QEMU refuses isolated proof: '+p.parent.name)
CHECK
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
printf '%s\n' "$TASK_TREE/${RASTERATOPS_BUILD_RUN:?use watch-build}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
TASK_PID=''
TASK_CLOUD_STARTED=0
stop_guest() {
 if [ -n "$TASK_PID" ]; then
  python3 "$TASK_OWNER/stop-guest.py" "$TASK_PID" "$TASK_OWNER/guest-d.qcow2"
  TASK_PID=''
 fi
}
cleanup() {
 result=$?
 trap - EXIT
 stop_guest || result=1
 if [ "$TASK_CLOUD_STARTED" = 1 ]; then ./tools/cloud-test-backend down || result=1; fi
 printf '%s
' "$result" > "$TASK_OWNER/inner.rc"
 exit "$result"
}
trap cleanup EXIT
echo 'Preparing independent 16GiB candidate guest d'
gunzip -c "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz" > "$TASK_OWNER/image.img"
qemu-img convert -f raw -O qcow2 "$TASK_OWNER/image.img" "$TASK_OWNER/guest-d.qcow2"
qemu-img resize "$TASK_OWNER/guest-d.qcow2" 16G
qemu-img check "$TASK_OWNER/guest-d.qcow2"
qemu-img info --output=json "$TASK_OWNER/guest-d.qcow2" > "$TASK_OWNER/artifacts/disk-initial.json"
rm "$TASK_OWNER/image.img"
ssh-keygen -q -t ed25519 -N '' -f "$VM_PAIR_DIR/qa-key" -C pixelelated-m7-qa
start_guest() {
 local gl=$1 res=$2
 ./projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm qemu-args --headless --gl "$gl" --res "$res" --ssh-port 10026 --mac 52:54:00:52:4E:5B "$TASK_OWNER/guest-d.qcow2" > "$TASK_OWNER/artifacts/qemu-$gl-$res.json"
 ./projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm run --headless --daemonize --gl "$gl" --res "$res" --monitor /tmp/rocknix-qemu-monitor-d.sock --serial /tmp/rocknix-qemu-serial-d.sock --pidfile /tmp/rocknix-qemu-d.pid --vnc 12 --ssh-port 10026 --mac 52:54:00:52:4E:5B "$TASK_OWNER/guest-d.qcow2"
 TASK_PID=$(cat /tmp/rocknix-qemu-d.pid)
 printf '%s
' "$TASK_PID" > "$TASK_OWNER/guest.pid"
 python3 "$TASK_OWNER/capture-boot.py" --monitor /tmp/rocknix-qemu-monitor-d.sock --output "$TASK_OWNER/artifacts/boot-$res" --seconds 40
 ./tools/vm-serial --socket /tmp/rocknix-qemu-serial-d.sock wait --up-to 300
 local public
 public=$(cat "$VM_PAIR_DIR/qa-key.pub")
 ./tools/vm-serial --socket /tmp/rocknix-qemu-serial-d.sock sh "mkdir -p /storage/.ssh && chmod 700 /storage/.ssh && echo '$public' >> /storage/.ssh/authorized_keys && chmod 600 /storage/.ssh/authorized_keys" >/dev/null
 python3 "$TASK_OWNER/seed.py"
}
TASK_CLOUD_STARTED=1
./tools/cloud-test-backend up
mkdir -p "$CLOUD_QA_STATE/data/pixelelated/Saves" "$CLOUD_QA_STATE/data/pixelelated/Backups"
for TASK_RES in 640x480 1280x960; do
 start_guest auto "$TASK_RES"
 for TASK_LANG in en_US fr_FR; do
  python3 "$TASK_OWNER/ui.py" "$TASK_LANG" "$TASK_RES"
 done
 stop_guest
done
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
echo 'PASS four language/panel captures; visual review remains required'
