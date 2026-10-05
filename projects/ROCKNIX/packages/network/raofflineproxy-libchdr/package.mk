# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)

PKG_NAME="raofflineproxy-libchdr"
# The commit RAOfflineProxy pins as its third_party/libchdr submodule at the
# proxy's own pinned commit3036478f2b2d22db451396a48f44feee94e8462f,
# verified 2026-10-05 from its third_party gitlinks (#361). This advances
# 8e7b8bd through the parent's ANSI C compatibility update. Full pins and
# native regression receipts are retained in the proxy3036478 QA record.
# The proxy's tarball carries the submodule as an
# empty directory; these sources (libchdr and the miniz, lzma and zstd
# decoders it vendors under deps/) are compiled by raofflineproxy's recipe
# into libraproxy_rchash.so so a CHD disc image hashes the way RetroArch
# hashes it (fork #179). Source only: nothing here is built or installed on
# its own.
# freshness: pinned -- follows the third_party/libchdr submodule commit RAOfflineProxy names (fork #179)
PKG_VERSION="607694ca0812edfc9cc2030c64634fc2393668de"
PKG_SHA256="02e772a74c4e5ec110bb646e729e1910268d2dae2c76df2a1b35525cc3826a9c"
PKG_LICENSE="BSD-3-Clause"
PKG_SITE="https://github.com/rtissera/libchdr"
PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
PKG_DEPENDS_TARGET="toolchain"
PKG_LONGDESC="libchdr, at the commit RAOfflineProxy pins: the CHD reader the proxy's ROM scan hashes disc images through."
PKG_TOOLCHAIN="manual"
