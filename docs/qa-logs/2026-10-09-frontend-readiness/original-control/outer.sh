#!/bin/bash
set +e
bash /workspace/tmp/pixelelated-m7-readiness-control-01/run.sh
rc=$?
printf '%s\n' "$rc" > /workspace/tmp/pixelelated-m7-readiness-control-01/outer.rc
exit "$rc"
