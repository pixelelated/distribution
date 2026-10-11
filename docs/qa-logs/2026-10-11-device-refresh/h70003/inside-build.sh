#!/bin/bash
set -euo pipefail
python3 -I /workspace/tmp/pixelelated-m7-h700-refresh-03/container-ready.py
./scripts/checkdeps
make H700
