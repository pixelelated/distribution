#!/bin/bash
set -euo pipefail
./scripts/build spirv-tools:host
python3 -I /workspace/tmp/pixelelated-m7-h700-arm-03/spirv-host-smoke.py
./scripts/build_distro
