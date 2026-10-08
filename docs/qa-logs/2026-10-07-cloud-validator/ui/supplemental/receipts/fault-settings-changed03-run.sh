#!/bin/bash
set -uo pipefail
python3 -u /workspace/tmp/pixelelated-510-coverage02/fault-settings-changed03/control.py
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-510-coverage02/fault-settings-changed03/inner.rc
exit "$rc"
