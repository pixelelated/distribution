# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
# Diagnostic overlay only: #576. GL candidate, Vulkan deliberately disabled.
PKG_NAME="gtk4"
PKG_VERSION="4.24.1"
PKG_SHA256="e98abe720e16129c8c0f50761dee0a2e9ae2478055e31018f6cf977fcf6513e9"
PKG_LICENSE="LGPL-2.1-or-later"
PKG_SITE="https://www.gtk.org/"
PKG_URL="https://download.gnome.org/sources/gtk/4.24/gtk-${PKG_VERSION}.tar.xz"
PKG_SOURCE_DIR="gtk-${PKG_VERSION}"
PKG_DEPENDS_TARGET="toolchain glib cairo pango harfbuzz harfbuzz-icu \
                    fribidi gdk-pixbuf graphene libepoxy libxkbcommon \
                    wayland wayland-protocols libdrm libpng tiff libjpeg-turbo"
PKG_LONGDESC="GTK4 Wayland and GL dependency for the isolated sign-in spike."
PKG_TOOLCHAIN="meson"
PKG_MAKE_OPTS_TARGET="-j2"
PKG_MESON_OPTS_TARGET="--wrap-mode=nofallback \
                       -Dx11-backend=false -Dwayland-backend=true \
                       -Dbroadway-backend=false -Dwin32-backend=false \
                       -Dmacos-backend=false -Dandroid-backend=false \
                       -Dandroid-runtime=disabled -Dvulkan=disabled \
                       -Dmedia-gstreamer=disabled -Dprint-cups=disabled \
                       -Dprint-cpdb=disabled -Dcloudproviders=disabled \
                       -Dtracker=disabled -Dcolord=disabled -Daccesskit=disabled \
                       -Dsysprof=disabled -Dintrospection=disabled \
                       -Ddocumentation=false -Dman-pages=false \
                       -Dbuild-demos=false -Dbuild-testsuite=false \
                       -Dbuild-examples=false -Dbuild-tests=false"

post_makeinstall_target() {
  ${TOOLCHAIN}/bin/glib-compile-schemas ${INSTALL}/usr/share/glib-2.0/schemas
}
