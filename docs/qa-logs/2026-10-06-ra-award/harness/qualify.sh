#!/bin/bash
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement14
TASK_OWNER=/workspace/tmp/pixelelated-m7-ra-01
TASK_BUNDLE=$(realpath "${1:?immutable candidate bundle required}")
cd "$TASK_TREE"
export VM_PAIR_DIR="$TASK_OWNER/pair"
export QA_KEY="$VM_PAIR_DIR/qa-key"
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
  printf 'set_link net0 on\n' | socat -t 1 - UNIX-CONNECT:/tmp/rocknix-qemu-monitor.sock >/dev/null 2>&1 || true
  if [ -f "$QA_KEY" ]; then
    ./tools/vm-pair ssh a 'raofflineproxy-ctl disable' >/dev/null 2>&1 || result=1
    ./tools/qa-accounts 10022 clear > "$TASK_OWNER/artifacts/account-cleanup.log" 2>&1 || result=1
  fi
  ./tools/vm-pair down || result=1
  printf '%s\n' "$result" > "$TASK_OWNER/inner.rc"
  exit "$result"
}
trap cleanup EXIT
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
./tools/vm-pair up "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz"
python3 "$TASK_OWNER/check-payload.py" ra-before
./tools/vm-pair ssh a '. /etc/profile >/dev/null 2>&1; set_setting global.retroachievements.hardcore 0'
./tools/vm-pair ssh a '. /etc/profile >/dev/null 2>&1; test "$(get_setting global.retroachievements.hardcore)" = 0'
./tools/ra-offline-test --port 10022 --identity "$QA_KEY" \
  --monitor /tmp/rocknix-qemu-monitor.sock --serial /tmp/rocknix-qemu-serial.sock \
  --roms /workspace/artifacts/rocknix-qa-roms --game tobu --frames "$TASK_OWNER/artifacts/frames" \
  2>&1 | tee "$TASK_OWNER/artifacts/ra-offline.log"
python3 "$TASK_OWNER/check-payload.py" ra-after
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
echo 'PASS ordinary Tobu offline award, reconnect, provider receipt and relaunch on frozen replacement14'
