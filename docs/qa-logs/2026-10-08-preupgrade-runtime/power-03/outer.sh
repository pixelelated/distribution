#!/bin/bash
set +e
bash /workspace/tmp/pixelelated-m7-alignment-power-03/run.sh
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-m7-alignment-power-03/outer.rc
exit "$rc"
