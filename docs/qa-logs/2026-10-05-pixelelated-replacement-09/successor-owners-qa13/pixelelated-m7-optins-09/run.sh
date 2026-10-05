#!/bin/bash
# Candidate-bound VM qualification; Refs #383, #409.
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement09
TASK_OWNER=/workspace/tmp/pixelelated-m7-optins-09
TASK_BUNDLE=$(realpath "${1:?verified candidate bundle required}")
cd "$TASK_TREE"
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
export VM_PAIR_DIR="$TASK_OWNER/pair"
export CLOUD_QA_STATE="$TASK_OWNER/cloud" CLOUD_QA_BACKEND=webdav
export CLOUD_QA_PORT=9040 CLOUD_QA_NAME=pixelelated-m7-optins-08
export ROCKNIX_ARTIFACTS="$TASK_OWNER/artifacts"
test ! -e "$TASK_OWNER/qa.start"
test "$(cat /workspace/tmp/pixelelated-m7-proxy-09/outer.rc)" = 0
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
cleanup() {
 result=$?
 trap - EXIT
 ./tools/vm-pair down || result=1
 ./tools/cloud-test-backend down || result=1
 printf '%s
' "$result" > "$TASK_OWNER/inner.rc"
 exit "$result"
}
trap cleanup EXIT
export CLOUD_QA_BACKEND=s3
export VM_PAIR_DIR="$TASK_OWNER/s3/pair" CLOUD_QA_STATE="$TASK_OWNER/s3/cloud"
./tools/vm-qa "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz" --only round-trip --backend s3
./tools/vm-pair down
./tools/cloud-test-backend down
export CLOUD_QA_BACKEND=webdav
export VM_PAIR_DIR="$TASK_OWNER/pair" CLOUD_QA_STATE="$TASK_OWNER/cloud"
./tools/cloud-pair-migration /workspace/artifacts/rocknix-images/x64-all-20260929-69e6039f8f/ROCKNIX-GENERIC_X64.x86_64-20260929.img.gz "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz" "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.tar" 2>&1 | tee "$TASK_OWNER/artifacts/pair-console.log"
./tools/vm-pair down
./tools/cloud-test-backend down
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
echo 'PASS S3 round-trip and mixed RC2/fresh pixelelated pair migration'
