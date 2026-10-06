#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-p4-reason-fit-host-01/run.sh
rc=$?
printf '%s\n' "$rc" > /workspace/tmp/pixelelated-m7-p4-reason-fit-host-01/outer.rc
exit "$rc"
