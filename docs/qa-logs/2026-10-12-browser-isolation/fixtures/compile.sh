#!/bin/bash
set -eu
base=/workspace/repos/rocknix.worktrees/m7-pixelelated/build.pixelelated-GENERIC_X64.x86_64/toolchain
export PATH="$base/bin:$PATH"
export PKG_CONFIG_SYSROOT_DIR="$base/x86_64-rocknix-linux-gnu/sysroot"
export PKG_CONFIG_LIBDIR="$PKG_CONFIG_SYSROOT_DIR/usr/lib/pkgconfig:$PKG_CONFIG_SYSROOT_DIR/usr/share/pkgconfig"
export TMPDIR=/work/tmp
for variant in current historical; do
  "$base/bin/x86_64-rocknix-linux-gnu-gcc" --sysroot="$PKG_CONFIG_SYSROOT_DIR" -O2 /work/$variant.c -o /work/$variant $(pkg-config --cflags --libs gtk+-3.0 webkit2gtk-4.1) -latomic
done
