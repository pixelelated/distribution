#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-image-12/run.sh "${1:?immutable bundle required}"
result=$?
printf '%s
' "$result" > /workspace/tmp/pixelelated-m7-image-12/outer.rc
exit "$result"
