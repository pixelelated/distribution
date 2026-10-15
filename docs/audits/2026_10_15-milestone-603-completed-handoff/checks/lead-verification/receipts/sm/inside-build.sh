#!/bin/bash
set -euo pipefail
python3 -I /workspace/tmp/pix-m7-sm8550-refresh-20261015-02/container-ready.py
python3 -I /workspace/tmp/pix-m7-sm8550-refresh-20261015-02/verify-fex.py --self-check
./scripts/checkdeps
export NIX_INSTALLER_NO_CHANNEL_ADD=1
export NIX_INSTALLER_NO_MODIFY_PROFILE=1
export NIX_CONFIG=$'build-users-group =
sandbox = false
max-jobs = 2
cores = 2'
make SM8550
python3 -I /workspace/tmp/pix-m7-sm8550-refresh-20261015-02/verify-fex.py
