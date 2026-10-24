# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)

PKG_NAME="dosbox-pure-lr"
# Pinned to 7f6e8fb738, a commit on none of the project's branches (its one
# branch, main, does not contain it; the hash still fetches). The reason is not
# recorded (#650 PL-027).
PKG_VERSION="7f6e8fb7385fa446d1444d671063268520bf9b54"
PKG_SHA256="b413767bf4d61e03c9a779cb0001bcc1bb68c78afbb058fd68d947a9f065f300"
PKG_LICENSE="GPL-2.0-or-later"
PKG_SITE="https://github.com/schellingb/dosbox-pure"
PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
PKG_DEPENDS_TARGET="toolchain"
PKG_LONGDESC="A port of DOSBox to libretro"

makeinstall_target() {
  mkdir -p ${INSTALL}/usr/lib/libretro
    cp -a dosbox_pure_libretro.so ${INSTALL}/usr/lib/libretro
}
