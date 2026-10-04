#!/bin/bash
set -uo pipefail
TASK_SWEEP=/tmp/pixelelated-m7-sweep-01
sha256sum -c "$TASK_SWEEP/harness.sha256" || exit 2
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_SWEEP/start"
python3 -u "$TASK_SWEEP/scan-artifact.py" --root /workspace/tmp/pixelelated-m7-image-03/root --allowlist "$TASK_SWEEP/allowlist.json" --patterns "$TASK_SWEEP/secret-patterns" --output "$TASK_SWEEP/report.json"
result=$?
printf '%s\n' "$result" > "$TASK_SWEEP/inner.rc"
exit "$result"
