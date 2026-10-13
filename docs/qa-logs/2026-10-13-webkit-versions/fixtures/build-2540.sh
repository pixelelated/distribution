#!/bin/bash
set -euo pipefail
root=/workspace/repos/rocknix.worktrees/m7-pixelelated/build.pixelelated-GENERIC_X64.x86_64
pkg="$root/build/webkitgtk-2.54.1"
export PATH="$root/toolchain/bin:$PATH"
export TMPDIR=/work/tmp
export PKG_CONFIG_SYSROOT_DIR="$root/toolchain/x86_64-rocknix-linux-gnu/sysroot"
export PKG_CONFIG_LIBDIR="$PKG_CONFIG_SYSROOT_DIR/usr/lib/pkgconfig:$PKG_CONFIG_SYSROOT_DIR/usr/share/pkgconfig"
export CCACHE_DISABLE=1
cmake -S "$pkg" -B "$pkg/.x86_64-rocknix-linux-gnu"
ninja -C "$pkg/.x86_64-rocknix-linux-gnu" -n > /work/build-2540-plan.txt
ninja -C "$pkg/.x86_64-rocknix-linux-gnu" -j4
DESTDIR=/work/runtime-2.54.0 cmake --install "$pkg/.x86_64-rocknix-linux-gnu" --strip
