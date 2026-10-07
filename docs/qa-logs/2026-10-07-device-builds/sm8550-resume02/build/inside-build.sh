#!/bin/bash
set -euo pipefail
export ARCH=aarch64
export NIX_PATH="nixpkgs=/workspace/tmp/pixelelated-m7-fex-header-control-01/runtime/nixpkgs"
export NIX_INSTALLER_NO_CHANNEL_ADD=1
export NIX_INSTALLER_NO_MODIFY_PROFILE=1
export NIX_CONFIG=$'build-users-group =
sandbox = false
max-jobs = 2
cores = 2'
test -d /nix/store/hymgd36hiy3g3pj7pyj6a53q7rbaip3i-fex-dev-rootfs
test -f /nix/store/a6b0pssdzris6023aqdgxvpvp3vqp8aw-toolchain_nix_x86_32.txt
test -f /nix/store/0y77jl567k50s0mpaz6878rpqdbynfqc-toolchain_nix_x86_64.txt
python3 -I /workspace/tmp/pixelelated-m7-sm8550-build-02/verify-arm.py
./scripts/build fex-emu:host
./scripts/build fex-emu:target
python3 -I /workspace/tmp/pixelelated-m7-sm8550-build-02/verify-fex.py
./scripts/build_distro
