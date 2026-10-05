#!/bin/bash
set -euo pipefail
TASK_OWNER=/workspace/tmp/pixelelated-m7-cloud-boundaries-01
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement10
TASK_BUNDLE=/workspace/artifacts/pixelelated-candidates/sha256/1c69bcf5ab6ebdc3e893a6a989545ac7a23359f0e07baef4e9c2beaca94c52b4
cd "$TASK_TREE"
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
export ROCKNIX_ARTIFACTS="$TASK_OWNER/artifacts"
test ! -e "$TASK_OWNER/qa.start"
sha256sum -c "$TASK_OWNER/harness.sha256"
test -d "$TASK_OWNER/proof" && test -z "$(ls -A "$TASK_OWNER/proof")"
printf '%s\n' "$TASK_TREE/${RASTERATOPS_BUILD_RUN:?use watch-build}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
cleanup() {
 result=$?
 trap - EXIT
 printf '%s\n' "$result" > "$TASK_OWNER/inner.rc"
 exit "$result"
}
trap cleanup EXIT
python3 -I "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
python3 -I "$TASK_OWNER/proof.py" --tree "$TASK_TREE" --image "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz" --build-id d6e8390c93bed87efe2dcc23cd402a271cacd1c7 --output "$TASK_OWNER/proof"
python3 -I "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"
./tools/rasteratops-candidate-store verify "$TASK_BUNDLE"
echo 'PASS focused installed cloud boundary proof; no UI-frame claim'
