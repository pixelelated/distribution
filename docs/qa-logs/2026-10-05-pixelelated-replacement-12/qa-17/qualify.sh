#!/bin/bash
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement12
TASK_OWNER=/workspace/tmp/pixelelated-m7-qa-17
TASK_BUNDLE=$(realpath "${1:?bundle required}")
cd "$TASK_TREE"
export VM_PAIR_DIR="$TASK_OWNER/pair" CLOUD_QA_STATE="$TASK_OWNER/cloud" CLOUD_QA_BACKEND=webdav
export ROCKNIX_ARTIFACTS="$TASK_OWNER/artifacts" ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
export RETROARCH_SRC="$TASK_TREE/build.pixelelated-GENERIC_X64.x86_64" QA_SYSTEM_ROOT="$TASK_TREE/build.pixelelated-GENERIC_X64.x86_64/image/system"
test ! -e "$TASK_OWNER/qa.start"
sha256sum -c "$TASK_OWNER/harness.sha256" > "$TASK_OWNER/artifacts/harness-before.log"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
python3 "$TASK_OWNER/clone-upgraded.py"
printf '%s\n' "$TASK_TREE/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
cleanup() {
 result=$?; trap - EXIT
 "$TASK_OWNER/tools/vm-pair" down || result=1
 ./tools/cloud-test-backend down || result=1
 printf '%s\n' "$result" > "$TASK_OWNER/inner.rc"
 exit "$result"
}
trap cleanup EXIT
ssh-keygen -q -t ed25519 -N '' -f "$VM_PAIR_DIR/qa-key" -C m7-qa17
boot_guest() {
 ./projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm run --headless --daemonize "$@" "$VM_PAIR_DIR/vm-a.qcow2"
 cat /tmp/rocknix-qemu.pid >> "$TASK_OWNER/guest-pids.txt"
 ./tools/vm-serial wait --up-to 300
 TASK_PUBLIC=$(cat "$VM_PAIR_DIR/qa-key.pub")
 ./tools/vm-serial sh "mkdir -p /storage/.ssh; chmod 700 /storage/.ssh; echo '$TASK_PUBLIC' >> /storage/.ssh/authorized_keys; chmod 600 /storage/.ssh/authorized_keys; sync" >/dev/null
}
boot_guest
python3 "$TASK_OWNER/check-payload.py" upgrade
python3 "$TASK_OWNER/verify-renderer.py" virgl upgrade-virgl --port 10022 --key "$VM_PAIR_DIR/qa-key" --out "$TASK_OWNER/artifacts"
python3 "$TASK_OWNER/identity-frames.py" upgrade
./tools/vm-pair ssh a sync
"$TASK_OWNER/tools/vm-pair" down
# Immediate reuse after the shared synchronous shutdown, without a sleep.
boot_guest --gl none --res 640x480
python3 "$TASK_OWNER/check-payload.py" upgrade-software
python3 "$TASK_OWNER/verify-renderer.py" software upgrade-software --port 10022 --key "$VM_PAIR_DIR/qa-key" --out "$TASK_OWNER/artifacts"
python3 "$TASK_OWNER/identity-frames.py" upgrade-software
./tools/vm-pair ssh a sync
"$TASK_OWNER/tools/vm-pair" down
boot_guest
# Replay the destructive predecessor before all three manager walks.
"$TASK_OWNER/qa-overlay/tools/vm-qa" --skip-up --only walks --walk match-dialog --walk manager-nes --walk manager-gb --walk manager-fbn
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
sha256sum -c "$TASK_OWNER/harness.sha256" > "$TASK_OWNER/artifacts/harness-after.log"
python3 "$TASK_OWNER/clone-upgraded.py" --verify-original
echo 'PASS scoped QA15 continuation: actual upgraded virgl/software readback and manager fixture recovery'
