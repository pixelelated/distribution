#!/bin/bash
set -euo pipefail
python3 -I /workspace/tmp/pixelelated-m7-sm8550-refresh-02/wait-runtime.py
./scripts/checkdeps
export NIX_PATH="nixpkgs=/workspace/tmp/pixelelated-m7-fex-header-control-01/runtime/nixpkgs"
export NIX_INSTALLER_NO_CHANNEL_ADD=1
export NIX_INSTALLER_NO_MODIFY_PROFILE=1
export NIX_CONFIG=$'build-users-group =
sandbox = false
max-jobs = 2
cores = 2'
python3 -I /workspace/tmp/pixelelated-m7-sm8550-refresh-02/verify-fex-cache.py
python3 -I /workspace/tmp/pixelelated-m7-sm8550-refresh-02/verify-fex.py
cp /workspace/tmp/pixelelated-m7-sm8550-refresh-02/artifacts/fex-package.json /workspace/tmp/pixelelated-m7-sm8550-refresh-02/artifacts/fex-cache-before-build.json
make SM8550
python3 -I /workspace/tmp/pixelelated-m7-sm8550-refresh-02/verify-fex.py
