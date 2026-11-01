#!/bin/bash
# T37 (#684) stage A, open item 9: mesa's effective GLES options per device, sourced in the scratch
# export (ruling (k)), named fields only. The command as run at 01:10 UTC; its output is mesa-gles.out.
cd /workspace/tmp/m6-t37/export || exit 2
sed -n '92,97p' projects/ROCKNIX/packages/graphics/mesa/package.mk; T=/workspace/tmp/m6-t37/tmp; for dv in AMD64:x86_64 GENERIC_X64:x86_64 H700:aarch64 RK3326:aarch64 RK3399:aarch64 RK3566:aarch64 RK3576:aarch64 RK3588:aarch64 S922X:aarch64 SM4450:aarch64 SM6115:aarch64 SM8250:aarch64 SM8550:aarch64 SM8650:aarch64 SM8750:aarch64; do env -i HOME="$T/home" PATH=/usr/bin:/bin PROJECT=ROCKNIX DEVICE="${dv%%:*}" ARCH="${dv##*:}" bash -c 'cd "$1" || exit 2; . config/options mesa >/dev/null 2>&1; rc=$?; g=$(printf "%s\n" $PKG_MESON_OPTS_TARGET | /usr/bin/grep -E "^-Dgles[12]=" | tr "\n" " "); echo "$2 source rc=$rc OPENGLES=${OPENGLES} OPENGLES_SUPPORT=${OPENGLES_SUPPORT} mesa-dir=${PKG_DIR#$1/} $g"' _ "$PWD" "$dv"; done 2>&1
