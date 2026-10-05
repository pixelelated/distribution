#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-signin-render-diagnostic-10/run.sh "${1:?immutable bundle required}"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-signin-render-diagnostic-10/outer.rc
exit "$result"
