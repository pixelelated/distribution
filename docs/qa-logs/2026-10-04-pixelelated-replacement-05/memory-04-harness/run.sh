#!/bin/bash
# Candidate-bound VM qualification; Refs #383, #409.
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement05
TASK_OWNER=/workspace/tmp/pixelelated-m7-memory-04
TASK_BUNDLE=$(realpath "${1:?verified candidate bundle required}")
cd "$TASK_TREE"
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
export VM_PAIR_DIR="$TASK_OWNER/pair"
export CLOUD_QA_STATE="$TASK_OWNER/cloud" CLOUD_QA_BACKEND=webdav
export CLOUD_QA_PORT=9040 CLOUD_QA_NAME=pixelelated-m7-memory-04
export ROCKNIX_ARTIFACTS="$TASK_OWNER/artifacts"
test ! -e "$TASK_OWNER/qa.start"
test "$(cat /workspace/tmp/pixelelated-m7-optins-04/outer.rc)" = 0
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
 ./tools/vm-serial --socket /tmp/rocknix-qemu-serial-d.sock wait --up-to 300
 local public
 public=$(cat "$VM_PAIR_DIR/qa-key.pub")
 ./tools/vm-serial --socket /tmp/rocknix-qemu-serial-d.sock sh "mkdir -p /storage/.ssh && chmod 700 /storage/.ssh && echo '$public' >> /storage/.ssh/authorized_keys && chmod 600 /storage/.ssh/authorized_keys" >/dev/null
 python3 "$TASK_OWNER/seed.py"
}
measure() {
 local name=$1 count=$2; shift 2
 ./tools/es-launch-memory --port 10026 --identity "$VM_PAIR_DIR/qa-key" --warmup 5 --cycles "$count" --max-vmsize-kib 1024 --max-rss-kib 2048 --output "$TASK_OWNER/artifacts/$name" "$@"
}
start_guest auto 640x480
measure virgl-10 10
stop_guest
start_guest none 640x480
measure software-10 10
TASK_CLOUD_STARTED=1
./tools/cloud-test-backend up
./tools/cloud-test-backend rclone-conf > "$TASK_OWNER/qa-cloud.conf"
chmod 600 "$TASK_OWNER/qa-cloud.conf"
SSH=(ssh -n -i "$VM_PAIR_DIR/qa-key" -p 10026 -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR root@127.0.0.1)
"${SSH[@]}" 'mkdir -p /storage/.config/rclone; chmod 700 /storage/.config/rclone; cp /usr/config/cloud_sync.conf /storage/.config/cloud_sync.conf'
scp -q -i "$VM_PAIR_DIR/qa-key" -P 10026 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR "$TASK_OWNER/qa-cloud.conf" root@127.0.0.1:/storage/.config/rclone/rclone.conf
"${SSH[@]}" 'chmod 600 /storage/.config/rclone/rclone.conf; systemctl stop essway; . /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 1; cloud_setup --seed-folders; printf "pixelelated memory QA save\n" > /storage/roms/gb/M7Memory.srm; systemctl start essway'
measure software-sync-50 50 --expect-exit-sync
./tools/signin-memory 10026 --key "$VM_PAIR_DIR/qa-key" --seconds 30 --json > "$TASK_OWNER/artifacts/signin-memory.json"
cat "$TASK_OWNER/artifacts/signin-memory.json"
stop_guest
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
echo 'PASS installed launch memory and sign-in page load'
