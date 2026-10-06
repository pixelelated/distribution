#!/bin/bash
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement14
TASK_OWNER=/workspace/tmp/pixelelated-m7-ra-ui-01
TASK_BUNDLE=$(realpath "${1:?bundle required}")
cd "$TASK_TREE"
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
export RA_UI_TOOLS="$TASK_TREE/tools"
export ROCKNIX_ARTIFACTS="$TASK_OWNER/artifacts"
sha256sum -c "$TASK_OWNER/harness.sha256"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
python3 - <<'CHECK'
from pathlib import Path
import socket,os
for entry in Path('/proc').glob('[0-9]*/cmdline'):
 try:name=Path(entry.read_bytes().split(b'\0',1)[0].decode()).name
 except (OSError,UnicodeError):continue
 if name.startswith('qemu-system-'):raise SystemExit('existing QEMU '+entry.parent.name)
for port in [10026,5912]:
 with socket.socket() as s:s.bind(('127.0.0.1',port))
v=os.statvfs('/workspace');assert v.f_bavail*v.f_frsize>64*1024**3
CHECK
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
test ! -e "$TASK_OWNER/qa.start"
printf '%s\n' "$TASK_TREE/${RASTERATOPS_BUILD_RUN:?watch-build required}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
TASK_PID=''
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
 printf '%s\n' "$result" > "$TASK_OWNER/inner.rc"
 exit "$result"
}
trap cleanup EXIT
gunzip -c "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz" > "$TASK_OWNER/image.img"
qemu-img convert -f raw -O qcow2 "$TASK_OWNER/image.img" "$TASK_OWNER/guest-d.qcow2"
qemu-img resize "$TASK_OWNER/guest-d.qcow2" 16G >/dev/null
qemu-img check "$TASK_OWNER/guest-d.qcow2"
rm "$TASK_OWNER/image.img"
ssh-keygen -q -t ed25519 -N '' -f "$TASK_OWNER/pair/qa-key" -C pixelelated-ra-ui-qa
for TASK_RES in 640x480 1280x960; do
 ./projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm qemu-args --headless --gl none --res "$TASK_RES" --ssh-port 10026 --mac 52:54:00:52:4E:5B "$TASK_OWNER/guest-d.qcow2" > "$TASK_OWNER/artifacts/qemu-$TASK_RES.json"
 ./projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm run --headless --daemonize --gl none --res "$TASK_RES" --monitor /tmp/rocknix-qemu-monitor-d.sock --serial /tmp/rocknix-qemu-serial-d.sock --pidfile /tmp/rocknix-qemu-d.pid --vnc 12 --ssh-port 10026 --mac 52:54:00:52:4E:5B "$TASK_OWNER/guest-d.qcow2"
 TASK_PID=$(cat /tmp/rocknix-qemu-d.pid)
 printf '%s\n' "$TASK_PID" >> "$TASK_OWNER/guest-pids.txt"
 ./tools/vm-serial --socket /tmp/rocknix-qemu-serial-d.sock wait --up-to 300
 public=$(cat "$TASK_OWNER/pair/qa-key.pub")
 ./tools/vm-serial --socket /tmp/rocknix-qemu-serial-d.sock sh "mkdir -p /storage/.ssh && chmod 700 /storage/.ssh && echo '$public' >> /storage/.ssh/authorized_keys && chmod 600 /storage/.ssh/authorized_keys" >/dev/null
 python3 "$TASK_OWNER/check-payload.py" "ui-before-$TASK_RES"
 for TASK_LANG in en_US fr_FR; do
  extra=()
  if [ "$TASK_RES" = 640x480 ] && [ "$TASK_LANG" = en_US ]; then extra+=(--failure-control); fi
  python3 "$TASK_OWNER/ra-ui-test" --identity "$TASK_OWNER/pair/qa-key" --port 10026 --monitor /tmp/rocknix-qemu-monitor-d.sock --serial /tmp/rocknix-qemu-serial-d.sock --out "$TASK_OWNER/artifacts/$TASK_LANG-$TASK_RES" --build-id 7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2 --language "$TASK_LANG" --resolution "$TASK_RES" "${extra[@]}"
 done
 python3 "$TASK_OWNER/check-payload.py" "ui-after-$TASK_RES"
 stop_guest
done
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
echo 'PASS installed reconnect UI matrix; direct frame review remains required'
