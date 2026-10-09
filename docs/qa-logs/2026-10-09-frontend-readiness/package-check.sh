#!/bin/bash
set -euo pipefail
CHECK_ROOT=$(mktemp -d /tmp/pix529-package.XXXXXX)
trap 'rm -rf -- "$CHECK_ROOT"' EXIT
PKG_DIR=/workspace/repos/rocknix.worktrees/m7-p5-frontend-readiness/projects/ROCKNIX/packages/wayland/compositor/sway
INSTALL=$CHECK_ROOT/install
DEVICE=GENERIC_X64
PKG_PATCH_DIRS=
. "$PKG_DIR/package.mk"
safe_remove() {
  for path in "$@"; do
    case "$path" in "$INSTALL"/*) rm -rf -- "$path";; *) return 1;; esac
  done
}
post_makeinstall_target
test -x "$INSTALL/usr/bin/sway-ready"
cmp "$PKG_DIR/scripts/sway-ready" "$INSTALL/usr/bin/sway-ready"
for dependency in bash busybox jq wlr-randr; do
  case " $PKG_DEPENDS_TARGET " in *" $dependency "*) ;; *) exit 1;; esac
done
printf 'PASS actual Sway post_makeinstall_target installs exact executable sway-ready and declares runtime dependencies\n'
