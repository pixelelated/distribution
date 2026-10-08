#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-520-ui-20261008/ui01/stage.sh
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-520-ui-20261008/ui01/inner.rc
exit "$rc"
