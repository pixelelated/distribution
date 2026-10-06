#!/bin/bash
set -uo pipefail
bash /tmp/pixelelated-cleanup-runtime-02/run.sh
result=$?
printf '%s\n' "$result" > /tmp/pixelelated-cleanup-runtime-02/outer.rc
exit "$result"
