#!/bin/bash
set -eu
root=/workspace/repos/rocknix.worktrees/m7-pixelelated/build.pixelelated-GENERIC_X64.x86_64
base="$root/toolchain"
src="$root/build/gstreamer-1.29.2"
export PATH="$base/bin:$PATH"
export PKG_CONFIG_SYSROOT_DIR="$base/x86_64-rocknix-linux-gnu/sysroot"
export PKG_CONFIG_LIBDIR="$PKG_CONFIG_SYSROOT_DIR/usr/lib/pkgconfig:$PKG_CONFIG_SYSROOT_DIR/usr/share/pkgconfig"
export TMPDIR=/work/tmp
"$base/bin/x86_64-rocknix-linux-gnu-gcc" --sysroot="$PKG_CONFIG_SYSROOT_DIR" -O2 /work/gst-probe.c -o /work/gst-probe $(pkg-config --cflags --libs gstreamer-1.0)
"$base/bin/x86_64-rocknix-linux-gnu-gcc" --sysroot="$PKG_CONFIG_SYSROOT_DIR" -O2 -DHAVE_CONFIG_H -I"$src" -I"$src/.x86_64-rocknix-linux-gnu" "$src/libs/gst/helpers/gst-plugin-scanner.c" -o /work/gst-plugin-scanner $(pkg-config --cflags --libs gstreamer-1.0 gmodule-2.0) -lm
cp "$PKG_CONFIG_SYSROOT_DIR/usr/lib/libgstcontroller-1.0.so.0.2902.0" /work/
