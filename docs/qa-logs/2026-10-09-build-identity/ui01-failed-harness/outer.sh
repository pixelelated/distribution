#!/bin/bash
set +e
bash /workspace/tmp/pixelelated-m7-identity-ui01/run.sh
rc=$?
printf '%s\n' "$rc" > /workspace/tmp/pixelelated-m7-identity-ui01/outer.rc
exit "$rc"
