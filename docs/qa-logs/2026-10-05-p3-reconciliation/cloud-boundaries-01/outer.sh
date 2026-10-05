#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-cloud-boundaries-01/run.sh
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-cloud-boundaries-01/outer.rc
exit "$result"
