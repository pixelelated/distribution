#!/bin/bash
set -euo pipefail
./scripts/build spirv-tools:host
python3 -I /workspace/tmp/pixelelated-m7-h700-arm-02/spirv-host-smoke.py
./scripts/build_distro
