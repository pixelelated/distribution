#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-settings-09/run.sh "${1:?immutable bundle required}"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-settings-09/outer.rc
exit "$result"
