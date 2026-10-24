# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2022-2024 JELOS (https://github.com/JustEnoughLinuxOS)
# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)

PKG_NAME="rkbin"
PKG_LICENSE="nonfree"
PKG_SITE="https://github.com/rockchip-linux/rkbin"
PKG_LONGDESC="rkbin: Rockchip Firmware and Tool Binaries"
PKG_TOOLCHAIN="manual"

case "${DEVICE}" in
  RK3588)
    # Pin rk3588 here until it hits mainline
    PKG_VERSION="7c35e21a8529b3758d1f051d1a5dc62aae934b2b"
    PKG_SHA256="18bde6ce71df308197db0e1d95fd73a19b6a32f4f0b6f5567333ef3c5b617452"
    ;;
  *)
    PKG_VERSION="74213af1e952c4683d2e35952507133b61394862"
    PKG_SHA256="b565faeab846950262c07e6debbd6519ea9e7f34943dbb305b9cea6b1026e11a"
    ;;
esac

PKG_URL="https://github.com/rockchip-linux/rkbin/archive/${PKG_VERSION}.tar.gz"

post_unpack() {
 if [ "${DEVICE}" == "RK3326" ]; then
  # RK3326: tune TPL for UART5 used on K36 clones
  cp -v ${PKG_BUILD}/bin/rk33/rk3326_ddr_333MHz_*.bin ${PKG_BUILD}/rk3326_ddr_uart5.bin
  ${PKG_BUILD}/tools/ddrbin_tool.py rk3326 -g ${PKG_BUILD}/rk3326_ddr_uart5.txt ${PKG_BUILD}/rk3326_ddr_uart5.bin
  sed -i 's|uart id=.*$|uart id=5|' ${PKG_BUILD}/rk3326_ddr_uart5.txt
  ${PKG_BUILD}/tools/ddrbin_tool.py rk3326 ${PKG_BUILD}/rk3326_ddr_uart5.txt ${PKG_BUILD}/rk3326_ddr_uart5.bin >/dev/null
 fi
}
