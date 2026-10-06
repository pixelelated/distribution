#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-replacement-15/copy-cache.sh
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-replacement-15/copy.outer.rc
exit "$result"
