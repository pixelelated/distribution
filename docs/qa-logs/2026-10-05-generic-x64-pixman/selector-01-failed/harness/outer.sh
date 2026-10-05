#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-renderer-selector-01/run.sh "${1:?immutable bundle required}"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-renderer-selector-01/outer.rc
exit "$result"
