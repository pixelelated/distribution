#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-510-coverage02/ui01/stage.sh > /workspace/tmp/pixelelated-510-coverage02/ui01/artifacts/stage.log 2>&1
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-510-coverage02/ui01/inner.rc
exit "$rc"
