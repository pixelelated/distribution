# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
# Diagnostic overlay only: #576, never install in an accepted build cache.
PKG_NAME="graphene"
PKG_VERSION="1.10.8"
PKG_SHA256="a37bb0e78a419dcbeaa9c7027bcff52f5ec2367c25ec859da31dfde2928f279a"
PKG_LICENSE="MIT"
PKG_SITE="https://ebassi.github.io/graphene/"
PKG_URL="https://download.gnome.org/sources/graphene/1.10/graphene-${PKG_VERSION}.tar.xz"
PKG_DEPENDS_TARGET="toolchain glib"
PKG_LONGDESC="Graphene geometry library, isolated GTK4 feasibility dependency."
PKG_TOOLCHAIN="meson"
PKG_MESON_OPTS_TARGET="--wrap-mode=nofallback -Dgobject_types=true \
                       -Dintrospection=disabled -Dgtk_doc=false \
                       -Dtests=false -Dinstalled_tests=false"
