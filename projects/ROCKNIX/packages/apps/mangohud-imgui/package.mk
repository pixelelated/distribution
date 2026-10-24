# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)

PKG_NAME="mangohud-imgui"
# The release mangohud's own subprojects/imgui.wrap names (source_url,
# source_filename and source_hash are the wrap's, byte for byte), carried as a
# source so the build never fetches it: mangohud's recipe used to curl this
# archive at configure, outside get_archive, the source cache and the
# checksum (#893). mangohud's recipe unpacks it from the source cache into
# subprojects/, under the directory the wrap names, and lays the wrap's patch
# over it. Source only: nothing here is built or installed on its own.
# freshness: pinned -- follows subprojects/imgui.wrap at mangohud's pinned commit (bump both together)
PKG_VERSION="1.91.6"
PKG_SHA256="c5fbc5dcab1d46064001c3b84d7a88812985cde7e0e9ced03f5677bec1ba502a"
PKG_LICENSE="MIT"
PKG_SITE="https://github.com/ocornut/imgui"
PKG_URL="${PKG_SITE}/archive/refs/tags/v${PKG_VERSION}.tar.gz"
PKG_SOURCE_NAME="imgui-${PKG_VERSION}.tar.gz"
PKG_DEPENDS_TARGET="toolchain"
PKG_LONGDESC="Dear ImGui, the immediate-mode GUI library mangohud draws its overlay with, at the release mangohud's meson wrap pins, as a source for mangohud's subprojects."
PKG_TOOLCHAIN="manual"
