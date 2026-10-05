#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-replacement-12/adopt-cache.sh
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-replacement-12/copy.outer.rc
exit "$result"
