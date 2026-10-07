#!/bin/bash
set -euo pipefail
trap 'rc=$?; printf "%s\n" "$rc" > /tmp/pixelelated-508-ui16/inner.rc' EXIT
python3 /tmp/pixelelated-508-ui16/run.py
