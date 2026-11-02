#!/bin/bash
# T41 stage A driver: runs the brief's (v2, 9313492990) `# STAGE A` block, then its runs block, in one shell, traced with UTC times
PS4='+ [$(date -u +%H:%M:%S)] '
echo "=== STAGE A begin $(date -u +%Y-%m-%dT%H:%M:%SZ)"
set -x
. /workspace/tmp/m6-t41/run/stage-a.sh
set +x
echo "=== STAGE A end / RUNS begin $(date -u +%Y-%m-%dT%H:%M:%SZ)"
set -x
. /workspace/tmp/m6-t41/run/runs.sh
set +x
echo "=== RUNS end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
