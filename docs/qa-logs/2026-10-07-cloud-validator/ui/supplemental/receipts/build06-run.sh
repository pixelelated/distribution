#!/bin/bash
set -uo pipefail
python3 -u /workspace/tmp/pixelelated-510-coverage02/build06/build.py
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-510-coverage02/build06/inner.rc
exit "$rc"
