# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)

PKG_NAME="idtech-lr"
PKG_VERSION="1.0"
PKG_SHA256="ff35cde05801cfb27005229a6c55f20130ffa8f026ca27d7717c03152634e168"
# Launcher scripts only; bundled Doom data has separate terms tracked in #528.
PKG_LICENSE="GPL-2.0-only"
PKG_SITE="https://rocknix.org"
PKG_URL="https://raw.githubusercontent.com/ROCKNIX/packages/4cb65b687c90f56856e9d6a55e51f56a09955699/doom.tar.gz"
PKG_SOURCE_NAME="idtech-lr-doom-${PKG_VERSION}.tar.gz"
PKG_LONGDESC="Package for all iD Software game engines."
PKG_TOOLCHAIN="manual"

if [ "${OPENGLES_SUPPORT}" = yes ]; then
  PKG_DEPENDS_TARGET+=" ${OPENGLES}"
  PKG_DEPENDS_TARGET+=" ecwolf-lr prboom-lr tyrquake-lr vitaquake2-lr"
fi

if [ "${TARGET_ARCH}" = "x86_64" ]; then
  PKG_DEPENDS_TARGET+=" vitaquake3-lr boom3-lr"
fi

# The image ships this archive intact for first-boot extraction. Fetch it via
# scripts/get so both the immutable revision and checksum are recorded.
unpack() {
  mkdir -p "${PKG_BUILD}"
  cp "${SOURCES}/${PKG_NAME}/${PKG_SOURCE_NAME}" "${PKG_BUILD}/doom.tar.gz"
}

makeinstall_target() {
  mkdir -p ${INSTALL}/usr/config/idtech

  mkdir -p ${INSTALL}/usr/bin
    cp -a ${PKG_DIR}/scripts/* ${INSTALL}/usr/bin

  mkdir -p ${INSTALL}/usr/share/idtech
    cp -a ${PKG_DIR}/sources/* ${INSTALL}/usr/share/idtech
    cp "${PKG_BUILD}/doom.tar.gz" "${INSTALL}/usr/share/idtech/doom.tar.gz"
}

post_install() {
  case ${TARGET_ARCH} in
    aarch64)
      sed -i '/doom3/d' ${INSTALL}/usr/share/idtech/idtech_dirs
      sed -i '/quake3/d' ${INSTALL}/usr/share/idtech/idtech_dirs
      ;;
  esac
}
