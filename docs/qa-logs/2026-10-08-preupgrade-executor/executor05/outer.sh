#!/bin/bash
set +e
bash /workspace/tmp/pixelelated-m7-alignment-executor-05/run.sh
rc=$?
printf '%s\n' "$rc" > /workspace/tmp/pixelelated-m7-alignment-executor-05/outer.rc
exit "$rc"
