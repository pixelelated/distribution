#!/bin/bash
set -euo pipefail
TASK_OWNER=/workspace/tmp/pixelelated-m7-replacement-12
TASK_STAGING=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement11
TASK_NEW=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement12
TASK_OLD=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement10
TASK_ROOT=build.pixelelated-GENERIC_X64.x86_64
[ "$(pwd -P)" = "$TASK_NEW" ]
[ ! -e "$TASK_OWNER/copy.start" ]
[ ! -e "$TASK_NEW/$TASK_ROOT" ]
sha256sum -c "$TASK_OWNER/adoption-harness.sha256"
python3 "$TASK_OWNER/verify-source.py"
tools/rc-preflight --only proxy-schema
printf '%s\n' "$TASK_NEW/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/copy.run"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/copy.start"
trap 'result=$?; printf "%s\n" "$result" > "$TASK_OWNER/copy.rc"' EXIT
python3 "$TASK_OWNER/adopt-cache.py"
rsync -aHnc --numeric-ids --delete --itemize-changes "$TASK_OLD/$TASK_ROOT/" "$TASK_NEW/$TASK_ROOT/" > "$TASK_OWNER/cache-compare.txt"
[ ! -s "$TASK_OWNER/cache-compare.txt" ]
python3 - <<'CHECK'
from pathlib import Path
import json,datetime
p=Path('/workspace/tmp/pixelelated-m7-replacement-12');r=json.loads((p/'cache-relocation.json').read_text());r.update(checksum_equal=True,verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());(p/'cache-ready.json').write_text(json.dumps(r,indent=2)+'\n')
print('PASS relocated unconsumed independent cache; full checksum equality reverified',flush=True)
CHECK
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/copy.finish"
printf '0\n' > "$TASK_OWNER/cache-ready.rc"
