#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-signin-ui-03/run.sh "${1:?immutable bundle required}"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-signin-ui-03/outer.rc
exit "$result"
