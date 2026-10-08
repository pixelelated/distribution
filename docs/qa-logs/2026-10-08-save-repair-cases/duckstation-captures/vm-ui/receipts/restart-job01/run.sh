#!/bin/bash
set -uo pipefail
python3 /workspace/tmp/pixelelated-520-ui-20261008/restart-job01/restart.py
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-520-ui-20261008/restart-job01/inner.rc
exit "$rc"
