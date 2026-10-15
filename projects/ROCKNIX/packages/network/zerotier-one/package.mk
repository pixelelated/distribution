# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2022-present kkoshelev (https://github.com/kkoshelev)
# Copyright (C) 2022-present fewtarius (https://github.com/fewtarius)
# Copyright (C) 2023-present NeoTheFox (https://github.com/NeoTheFox)

PKG_NAME="zerotier-one"
PKG_VERSION="1.16.0"
# Core code only; ext/ has separate terms. Nonfree controller omitted (#528).
PKG_LICENSE="MPL-2.0"
PKG_SHA256="aa9de313d365bf0efb3871aaa56f2d323a08f46df47b627c4eff4f4203fa7fc5"
PKG_SITE="https://www.zerotier.com"
PKG_URL="https://github.com/zerotier/ZeroTierOne/archive/refs/tags/${PKG_VERSION}.tar.gz"
PKG_DEPENDS_TARGET="toolchain nlohmann-json"
PKG_LONGDESC="A Smart Ethernet Switch for Earth"
PKG_TOOLCHAIN="manual"


unpack() {
    # The client does not build the separately licensed controller (#528).
    # Override extraction once so its headers cannot enter the build tree.
    mkdir -p "${PKG_BUILD}"
    tar --strip-components=1 --exclude="ZeroTierOne-${PKG_VERSION}/nonfree" \
        -xf "${SOURCES}/${PKG_NAME}/${PKG_NAME}-${PKG_VERSION}.tar.gz" \
        -C "${PKG_BUILD}" "ZeroTierOne-${PKG_VERSION}"
    [ ! -e "${PKG_BUILD}/nonfree" ] && [ ! -L "${PKG_BUILD}/nonfree" ]
}


make_target() {
    # Build libnatpmp for target
    make -C ${PKG_BUILD}/ext/libnatpmp CC=${CC}

	# Build zerotier-one
    cd ${PKG_BUILD}
    CPPFLAGS="${CPPFLAGS} -I${PKG_BUILD}/ext/libnatpmp" \
    LDLIBS="${LDLIBS} -L${PKG_BUILD}/ext/libnatpmp" \
    make -f make-linux.mk ZT_SSO_SUPPORTED=0 one
}

makeinstall_target() {
    make DESTDIR=${INSTALL} install
    rm -rf ${INSTALL}/usr/share/man/

    install -Dm755 ${PKG_DIR}/scripts/zerotier-join.sh ${INSTALL}/usr/sbin/
    mkdir -p ${INSTALL}/usr/lib/systemd/system
    install -Dm644 ${PKG_DIR}/system.d/zerotier-one.service ${INSTALL}/usr/lib/systemd/system/
}

