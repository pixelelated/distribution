#!/bin/bash
set +e
bash /workspace/tmp/pixelelated-m7-identity-ui02/run.sh
rc=$?
printf '%s\n' "$rc" > /workspace/tmp/pixelelated-m7-identity-ui02/outer.rc
exit "$rc"
