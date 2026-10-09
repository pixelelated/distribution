#!/bin/bash
set +e
bash /workspace/tmp/pixelelated-m7-readiness-fixed-01/run.sh
rc=$?
printf '%s\n' "$rc" > /workspace/tmp/pixelelated-m7-readiness-fixed-01/outer.rc
exit "$rc"
