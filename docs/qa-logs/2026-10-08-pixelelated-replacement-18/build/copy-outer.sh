#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-replacement-18/copy-cache.sh
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-replacement-18/copy.outer.rc
exit "$result"
