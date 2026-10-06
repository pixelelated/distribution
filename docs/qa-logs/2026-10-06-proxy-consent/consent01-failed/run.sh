#!/bin/bash
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement12
TASK_OWNER=/workspace/tmp/pixelelated-m7-consent-01
TASK_BUNDLE=$(realpath "${1:?verified candidate bundle required}")
cd "$TASK_TREE"
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
export VM_PAIR_DIR="$TASK_OWNER/pair"
test ! -e "$TASK_OWNER/qa.start"
test "$(cat /workspace/tmp/pixelelated-m7-qa-17/outer.rc)" = 0
sha256sum -c "$TASK_OWNER/harness.sha256"
test "$(cat /workspace/tmp/pixelelated-m7-subset-10/outer.rc)" = 0
python3 -I "$TASK_OWNER/prepare-dirs.py"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
python3 - <<'CHECK'
from pathlib import Path
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try: name=Path(p.read_bytes().split(b'\0',1)[0].decode()).name
 except (FileNotFoundError,ProcessLookupError):continue
 if name.startswith('qemu-system-'):raise SystemExit('Existing QEMU refuses isolated proxy proof: '+p.parent.name)
CHECK
printf '%s\n' "$TASK_TREE/${RASTERATOPS_BUILD_RUN:?use watch-build}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
TASK_QEMU_PID=''
cleanup() {
 result=$?
 trap - EXIT
 if [ -n "$TASK_QEMU_PID" ]; then
  python3 "$TASK_OWNER/vm-stop" /tmp/rocknix-qemu-d.pid "$TASK_OWNER/guest-d.qcow2" || result=1
 fi
 printf '%s\n' "$result" > "$TASK_OWNER/inner.rc"
 exit "$result"
}
trap cleanup EXIT
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
if [ ! -f "$TASK_OWNER/guest-d.qcow2" ]; then
 gunzip -c "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz" > "$TASK_OWNER/image.img"
 qemu-img convert -f raw -O qcow2 "$TASK_OWNER/image.img" "$TASK_OWNER/guest-d.qcow2"
 qemu-img resize "$TASK_OWNER/guest-d.qcow2" 16G
 qemu-img check "$TASK_OWNER/guest-d.qcow2"
 rm "$TASK_OWNER/image.img"
 ssh-keygen -q -t ed25519 -N '' -f "$TASK_OWNER/pair/qa-key" -C m7-proxy-qa
fi
./projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm run --headless --daemonize --res 640x480 --monitor /tmp/rocknix-qemu-monitor-d.sock --serial /tmp/rocknix-qemu-serial-d.sock --pidfile /tmp/rocknix-qemu-d.pid --vnc 12 --ssh-port 10026 --mac 52:54:00:52:4E:5B "$TASK_OWNER/guest-d.qcow2"
TASK_QEMU_PID=$(cat /tmp/rocknix-qemu-d.pid)
printf '%s\n' "$TASK_QEMU_PID" > "$TASK_OWNER/guest.pid"
./tools/vm-serial --socket /tmp/rocknix-qemu-serial-d.sock wait --up-to 300
TASK_PUBLIC=$(cat "$TASK_OWNER/pair/qa-key.pub")
./tools/vm-serial --socket /tmp/rocknix-qemu-serial-d.sock sh "mkdir -p /storage/.ssh && chmod 700 /storage/.ssh && echo '$TASK_PUBLIC' >> /storage/.ssh/authorized_keys && chmod 600 /storage/.ssh/authorized_keys" >/dev/null
python3 "$TASK_OWNER/host-proof.py"
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
echo 'PASS pixelelated frozen55d8ee8f75 installed consent and HTTP capture proof'
