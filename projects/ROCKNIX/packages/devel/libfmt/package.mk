# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)

. ${ROOT}/packages/devel/libfmt/package.mk

case ${DEVICE} in
  SM4450|SM8250|SM8550|SM8650|SM8750|AMD64)
    ;;
  *)
    PKG_VERSION="9.1.0"
    # 9.1.0's archive, sha256 by trust on first use from the fetch of 2026-10-24, equal to the shared cache's 2026-08-26 stamp and ROCKNIX's mirror (D-WORKFLOW-193/196, #877)
    PKG_SHA256="5dea48d1fcddc3ec571ce2058e13910a0d4a6bab4cc09a809d8b1dd1c88ae6f2"
    PKG_URL="https://github.com/fmtlib/fmt/archive/${PKG_VERSION}.tar.gz"
    ;;
esac
