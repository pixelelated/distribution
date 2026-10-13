#!/bin/bash
set -euo pipefail
root=/workspace/repos/rocknix.worktrees/m7-pixelelated/build.pixelelated-GENERIC_X64.x86_64
pkg="$root/build/gstreamer-1.29.2"
export PATH="$root/toolchain/bin:$PATH"
export TMPDIR=/work/tmp
export XDG_CACHE_HOME=/work/cache
export PKG_CONFIG_SYSROOT_DIR="$root/toolchain/x86_64-rocknix-linux-gnu/sysroot"
export PKG_CONFIG_LIBDIR="$PKG_CONFIG_SYSROOT_DIR/usr/lib/pkgconfig:$PKG_CONFIG_SYSROOT_DIR/usr/share/pkgconfig"
ROOT=/work/recipes
DISTRO=ROCKNIX
NOONEXIT=yes
set +u
source /work/functions
set -u
source /work/recipes/override.mk
pre_configure_target
meson configure "$pkg/.x86_64-rocknix-linux-gnu" ${PKG_MESON_OPTS_TARGET}
ninja -C "$pkg/.x86_64-rocknix-linux-gnu" -j2
meson install -C "$pkg/.x86_64-rocknix-linux-gnu" --destdir /work/installed-before --no-rebuild --strip
cp -a /work/installed-before /work/installed-old
cp -a /work/installed-before /work/installed-new
source /work/recipes/packages/multimedia/gstreamer/gstreamer/package.mk
INSTALL=/work/installed-old
post_makeinstall_target
source /work/recipes/override.mk
INSTALL=/work/installed-new
post_makeinstall_target
