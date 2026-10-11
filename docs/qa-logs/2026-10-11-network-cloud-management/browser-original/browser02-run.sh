#!/bin/bash
set -euo pipefail
B=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18/build.pixelelated-GENERIC_X64.x86_64
export PKG_CONFIG_SYSROOT_DIR=$B/toolchain/x86_64-rocknix-linux-gnu/sysroot
export PKG_CONFIG_LIBDIR=$PKG_CONFIG_SYSROOT_DIR/usr/lib/pkgconfig:$PKG_CONFIG_SYSROOT_DIR/usr/share/pkgconfig
read -ra flags <<< "$("$B/toolchain/bin/pkg-config" --cflags --libs gtk+-3.0 webkit2gtk-4.1)"
"$B/toolchain/bin/x86_64-rocknix-linux-gnu-gcc" -O2 -march=x86-64-v3 --sysroot="$PKG_CONFIG_SYSROOT_DIR" projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c -o /tmp/pix535-537-browser02/cloud-signin-window "${flags[@]}" -latomic
sha256sum /tmp/pix535-537-browser02/cloud-signin-window
