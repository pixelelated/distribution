#!/bin/bash
set +e
bash /workspace/tmp/pixelelated-m7-alignment-executor-04/run.sh
rc=$?
printf '%s\n' "$rc" > /workspace/tmp/pixelelated-m7-alignment-executor-04/outer.rc
exit "$rc"
