#!/bin/bash
# T37 (#684) stage B: the patch reach of the three packages on all 15 devices, sourced in the scratch
# export (ruling (k)) under env -i with HOME in scratch, by scripts/unpack:127-159's rule (the same
# computation as stage-a/s5-runs.sh R16, widened from GENERIC_X64 and H700 to every device).
X=/workspace/tmp/m6-t37/export; T=/workspace/tmp/m6-t37/tmp
[ -d "$X/.git" ] && { echo "STOP: the export is a git tree"; exit 2; }
[ -d "$X/config" ] || { echo "STOP: no export"; exit 2; }
rcs=0
for dv in AMD64:x86_64 GENERIC_X64:x86_64 H700:aarch64 RK3326:aarch64 RK3399:aarch64 RK3566:aarch64 RK3576:aarch64 RK3588:aarch64 S922X:aarch64 SM4450:aarch64 SM6115:aarch64 SM8250:aarch64 SM8550:aarch64 SM8650:aarch64 SM8750:aarch64; do for nm in emulationstation es-theme-art-book-next lowerdeck; do env -i HOME="$T/home" PATH=/usr/bin:/bin PROJECT=ROCKNIX DEVICE="${dv%%:*}" ARCH="${dv##*:}" bash -c 'cd "$2" || exit 2; . config/options "$1" >/dev/null 2>&1 || { echo "source FAILED $1"; exit 2; }
if [ "${TARGET_ARCH}" = "x86_64" ]; then PATCH_ARCH="x86"; elif [ "${PKG_IS_KERNEL_PKG}" = "yes" ]; then PATCH_ARCH="${TARGET_KERNEL_PATCH_ARCH:-${TARGET_ARCH}}"; else PATCH_ARCH="${TARGET_PATCH_ARCH:-${TARGET_ARCH}}"; fi
reach="${PKG_DIR}/patches ${PKG_DIR}/patches/${PATCH_ARCH} ${PKG_DIR}/patches/${PKG_VERSION} ${PKG_DIR}/patches/${PKG_VERSION}/${PATCH_ARCH} ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME} ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${PATCH_ARCH} ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${PKG_VERSION} ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}"
for d in ${PKG_PATCH_DIRS}; do case "$d" in /*) reach+=" $d";; *) reach+=" ${PKG_DIR}/patches/$d ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/$d ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}/$d";; esac; done
dirs=$(find "${PKG_DIR}/patches" -name "*.patch" -printf "%h\n" 2>/dev/null | sort -u)
[ -n "$dirs" ] || echo "${DEVICE}/${TARGET_ARCH}: $1 PATCH_ARCH=${PATCH_ARCH} PKG_PATCH_DIRS=[${PKG_PATCH_DIRS}] -> no patches/ directory with a .patch"
for d in $dirs; do v="NOT REACHED"; for r in $reach; do [ "$r" = "$d" ] && v="REACHED"; done; echo "${DEVICE}/${TARGET_ARCH}: $1 PATCH_ARCH=${PATCH_ARCH} PKG_PATCH_DIRS=[${PKG_PATCH_DIRS}] -> ${d#${PKG_DIR}/}/: $v"; done
for r in ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME} ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}; do [ -d "$r" ] && echo "${DEVICE}: $1 project-side patch dir present: ${r#$2/}"; done; true' _ "$nm" "$X"; rc=$?
rcs=$((rcs+rc)); done; done
echo "reach rc-sum=$rcs"
