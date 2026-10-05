#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-image-10/run.sh "${1:?immutable bundle required}"
result=$?
printf '%s
' "$result" > /workspace/tmp/pixelelated-m7-image-10/outer.rc
exit "$result"
