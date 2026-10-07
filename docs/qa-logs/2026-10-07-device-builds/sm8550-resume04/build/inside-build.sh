#!/bin/bash
set -euo pipefail
export ARCH=aarch64
python3 -I /workspace/tmp/pixelelated-m7-sm8550-build-04/wait-runtime.py
test -d /nix && test -w /nix
./scripts/checkdeps
echo "PASS canonical pinned-container dependencies before proof/build work"
export NIX_PATH="nixpkgs=/workspace/tmp/pixelelated-m7-fex-header-control-01/runtime/nixpkgs"
export NIX_INSTALLER_NO_CHANNEL_ADD=1
export NIX_INSTALLER_NO_MODIFY_PROFILE=1
export NIX_CONFIG=$'build-users-group =
sandbox = false
max-jobs = 2
cores = 2'
python3 -I /workspace/tmp/pixelelated-m7-sm8550-build-04/verify-arm.py
python3 -I /workspace/tmp/pixelelated-m7-sm8550-build-04/proof-controls.py
./scripts/build_distro
