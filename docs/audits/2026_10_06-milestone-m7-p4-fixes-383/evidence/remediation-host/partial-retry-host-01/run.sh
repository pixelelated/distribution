#!/bin/bash
set -euo pipefail
TASK_OWNER=/workspace/tmp/pixelelated-m7-p4-partial-retry-host-01
cd /workspace/repos/rocknix.worktrees/conflict-resolution
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
trap 'result=$?; printf "%s\n" "$result" > "$TASK_OWNER/inner.rc"' EXIT
sha256sum -c "$TASK_OWNER/harness.sha256"
TASK_RCLONE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15/build.pixelelated-GENERIC_X64.x86_64/image/system/usr/bin/rclone
./tools/rasteratops-cloud-layout-test --rclone "$TASK_RCLONE" --case PL003-truncated --output "$TASK_OWNER/artifacts/focused"
set +e
./tools/rasteratops-cloud-layout-test --rclone "$TASK_RCLONE" --ref ffae61e343ba4f7aa53550c832fb5e230e13cb11 --case PL003-truncated-prefix --output "$TASK_OWNER/artifacts/old-prefix"
old_rc=$?
set -e
[ "$old_rc" = 1 ]
python3 - <<'CHECK'
import json
from pathlib import Path
j=json.loads(Path('/workspace/tmp/pixelelated-m7-p4-partial-retry-host-01/artifacts/old-prefix/results.json').read_text())
assert len(j)==4 and all(r['status']=='FAIL' and 'truncated retry did not complete' in r['why'] for r in j),j
print('PASS four old-source partial-file positives fail as expected',flush=True)
CHECK
for TASK_CASE in no-record different; do
 ./tools/rasteratops-cloud-layout-test --rclone "$TASK_RCLONE" --ref ffae61e343ba4f7aa53550c832fb5e230e13cb11 --case "PL003-truncated-$TASK_CASE" --output "$TASK_OWNER/artifacts/old-$TASK_CASE"
done
./tools/rasteratops-cloud-layout-test --rclone "$TASK_RCLONE" --output "$TASK_OWNER/artifacts/full"
sha256sum -c "$TASK_OWNER/harness.sha256"
echo 'PASS partial-file source repair; rebuilt installed UI acceptance remains required'
