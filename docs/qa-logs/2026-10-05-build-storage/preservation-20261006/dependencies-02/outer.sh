#!/bin/bash
set -uo pipefail
bash /tmp/pixelelated-cleanup-dependencies-02/run.sh
result=$?
printf '%s\n' "$result" > /tmp/pixelelated-cleanup-dependencies-02/outer.rc
exit "$result"
