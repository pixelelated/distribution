# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)

PKG_NAME="mangohud-implot"
# The release mangohud's own subprojects/implot.wrap names (source_url,
# source_filename and source_hash are the wrap's, byte for byte), carried as a
# source so the build never fetches it: mangohud's recipe used to curl this
# archive at configure, outside get_archive, the source cache and the
# checksum (#893). mangohud's recipe unpacks it from the source cache into
# subprojects/, under the directory the wrap names, and lays the wrap's patch
# over it. Source only: nothing here is built or installed on its own.
# freshness: pinned -- follows subprojects/implot.wrap at mangohud's pinned commit (bump both together)
PKG_VERSION="0.16"
PKG_SHA256="24f772c688f6b8a6e19d7efc10e4923a04a915f13d487b08b83553aa62ae1708"
PKG_LICENSE="MIT"
PKG_SITE="https://github.com/epezent/implot"
PKG_URL="${PKG_SITE}/archive/refs/tags/v${PKG_VERSION}.zip"
PKG_SOURCE_NAME="implot-${PKG_VERSION}.zip"
PKG_DEPENDS_TARGET="toolchain"
PKG_LONGDESC="ImPlot, ImGui's plotting extension, mangohud's graphs, at the release mangohud's meson wrap pins, as a source for mangohud's subprojects."
PKG_TOOLCHAIN="manual"
