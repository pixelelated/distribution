# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
# Copyright (C) 2023-present NeoTheFox (https://github.com/NeoTheFox)

PKG_NAME="simple-http-server"
PKG_VERSION="0.8.0"
PKG_LICENSE="MIT"
PKG_SITE="https://github.com/TheWaWaR/simple-http-server"
PKG_DEPENDS_TARGET="toolchain"
PKG_LONGDESC="Simple http server in Rust"
PKG_TOOLCHAIN="manual"

case ${ARCH} in
  x86_64)
    PKG_URL="${PKG_SITE}/releases/download/v${PKG_VERSION}/x86_64-unknown-linux-musl-simple-http-server"
    # the release binary's sha256 by trust on first use from the fetch of 2026-10-24, equal to the shared cache's 2026-08-26 stamp; the mirror has no copy (D-WORKFLOW-193/197, #890)
    PKG_SHA256="a16d73db4b33edc6aada0bb54088773dba8cb4d02eaa13364559552072d628cd"
    ;;
  arm)
    PKG_URL="${PKG_SITE}/releases/download/v${PKG_VERSION}/armv7-unknown-linux-musleabihf-simple-http-server"
    # the release binary's sha256 by trust on first use from the fetch of 2026-10-24, one witness: the fetch; the mirror has no copy (D-WORKFLOW-193/197, #890)
    PKG_SHA256="44d837d868fabb4eaea69251e29d522351d532ee2ccbb0c91e839681f8fdcd69"
    ;;
  aarch64)
    PKG_URL="${PKG_SITE}/releases/download/v${PKG_VERSION}/aarch64-unknown-linux-musl-simple-http-server"
    PKG_SHA256="88a523d339fa412575e497ee1741ffa4a7b6bdcfa23681a82eac7b8cd2bdf815"
    ;;
esac

unpack() {
  mkdir -p ${PKG_BUILD}
  cp ${SOURCES}/${PKG_NAME}/${PKG_NAME}-${PKG_VERSION}.${ARCH}*${PKG_NAME} ${PKG_BUILD}/simple-http-server
}

makeinstall_target() {
  mkdir -p ${INSTALL}/usr/bin
  install -Dm755 ${PKG_BUILD}/simple-http-server ${INSTALL}/usr/bin

  mkdir -p ${INSTALL}/usr/lib/systemd/system
  install -Dm644 ${PKG_DIR}/system.d/simple-http-server.service ${INSTALL}/usr/lib/systemd/system
}
