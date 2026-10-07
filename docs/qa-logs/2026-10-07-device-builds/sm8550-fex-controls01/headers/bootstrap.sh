#!/bin/bash
set -euo pipefail
cd /out
export XDG_CACHE_HOME=/out/cache
export XDG_CONFIG_HOME=/out/config
export XDG_STATE_HOME=/out/state
export NIX_CONFIG=$'build-users-group =\nsandbox = false\nmax-jobs = 2\ncores = 2'
curl --fail --location --retry 2 --max-time 180 -o nix.tar.xz https://releases.nixos.org/nix/nix-2.35.2/nix-2.35.2-x86_64-linux.tar.xz
mkdir bootstrap
tar -xJf nix.tar.xz --strip-components=1 -C bootstrap
mkdir -p /nix/store
cp -a bootstrap/store/. /nix/store/
NIX_BIN=$(find /nix/store -maxdepth 3 -path '*-nix-2.35.2/bin' -type d)
test -n "${NIX_BIN}"
export PATH="${NIX_BIN}:${PATH}"
nix-store --load-db < bootstrap/.reginfo
curl --fail --location --retry 2 --max-time 180 -o nixpkgs.tar.xz https://releases.nixos.org/nixpkgs/nixpkgs-26.11pre1086972.7dd199b0e299/nixexprs.tar.xz
mkdir nixpkgs
tar -xJf nixpkgs.tar.xz --strip-components=1 -C nixpkgs
sha256sum nix.tar.xz nixpkgs.tar.xz > downloads.sha256
FEX_SOURCE=$(python3 -c 'import json;print(json.load(open("/out/inputs.json"))["fex"])')
nix-shell "${FEX_SOURCE}/Data/nix/LibraryForwarding/shell.nix" --arg pkgs 'import /out/nixpkgs {}' --run 'python3 -I /out/probe.py'
