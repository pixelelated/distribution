#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-image-05/run.sh "${1:?immutable bundle required}"
result=$?
printf '%s
' "$result" > /workspace/tmp/pixelelated-m7-image-05/outer.rc
exit "$result"
