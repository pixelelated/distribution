#!/bin/bash
set +e
bash /workspace/tmp/pixelelated-m7-alignment-executor-06/run.sh
rc=$?
printf '%s\n' "$rc" > /workspace/tmp/pixelelated-m7-alignment-executor-06/outer.rc
exit "$rc"
