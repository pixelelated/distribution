#!/bin/bash
# Read-only candidate analysis; Refs #344, #383, #409.
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement17
TASK_OWNER=/workspace/tmp/pixelelated-m7-image-17
TASK_BUNDLE=$(realpath "${1:?immutable candidate bundle required}")
cd "$TASK_TREE"
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
test ! -e "$TASK_OWNER/qa.start"
python3 -c 'import json; p="/workspace/tmp/pixelelated-m7-replacement-17/completion.json"; j=json.load(open(p)); assert j["result"]=="PASS" and j["issue"]==525 and set(j["corrected_verification_channels"].values())=={"0"}'
sha256sum -c "$TASK_OWNER/harness.sha256"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
printf '%s
' "$TASK_TREE/${RASTERATOPS_BUILD_RUN:?use watch-build}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
cleanup() { result=$?; trap - EXIT; printf '%s
' "$result" > "$TASK_OWNER/inner.rc"; exit "$result"; }
trap cleanup EXIT
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
python3 "$TASK_OWNER/extract.py" "$TASK_BUNDLE"
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
echo 'PASS extracted exact image payload; content sweeps remain separate'
