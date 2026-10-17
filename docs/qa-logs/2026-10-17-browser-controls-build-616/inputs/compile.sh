#!/bin/bash
set -euo pipefail
export TMPDIR=/tmp
compile_one() {
  local base="$1" triple="$2" name="$3"
  export PATH="$base/toolchain/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
  export PKG_CONFIG_SYSROOT_DIR="$base/toolchain/$triple/sysroot"
  export PKG_CONFIG_LIBDIR="$PKG_CONFIG_SYSROOT_DIR/usr/lib/pkgconfig:$PKG_CONFIG_SYSROOT_DIR/usr/share/pkgconfig"
  "$base/toolchain/bin/$triple-gcc" --sysroot="$PKG_CONFIG_SYSROOT_DIR" -O2 -Wall /inputs/diagnostic.c -o "/work/$name" $(pkg-config --cflags --libs gtk+-3.0 webkit2gtk-4.1) -latomic
  "$base/toolchain/bin/$triple-readelf" -h -d "/work/$name" > "/work/$name.elf.txt"
  sha256sum "/work/$name"
}
compile_one '/workspace/repos/rocknix.worktrees/m7-pixelelated/build.pixelelated-GENERIC_X64.x86_64' 'x86_64-rocknix-linux-gnu' 'cloud-signin-window-GENERIC_X64'
compile_one '/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01/build.pixelelated-H700.aarch64' 'aarch64-rocknix-linux-gnu' 'cloud-signin-window-H700'
python3 -I /inputs/config-checks.py -- '/workspace/repos/rocknix.worktrees/m7-pixelelated/build.pixelelated-GENERIC_X64.x86_64/toolchain/x86_64-rocknix-linux-gnu/sysroot/usr/lib/ld-linux-x86-64.so.2' --library-path '/workspace/repos/rocknix.worktrees/m7-pixelelated/build.pixelelated-GENERIC_X64.x86_64/toolchain/x86_64-rocknix-linux-gnu/sysroot/usr/lib' /work/cloud-signin-window-GENERIC_X64 > /work/config-checks.json
