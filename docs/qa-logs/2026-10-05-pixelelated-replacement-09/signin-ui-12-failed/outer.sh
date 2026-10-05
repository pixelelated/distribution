#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-signin-ui-12/run.sh "${1:?immutable bundle required}"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-signin-ui-12/outer.rc
exit "$result"
