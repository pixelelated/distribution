#!/bin/bash
# calculate_stamp against a device-level file that find_file_path reads (#652):
# the shape of kernel-firmware and projects/ROCKNIX/devices/<D>/config/kernel-firmware.dat.
# The fixture package takes kernel-firmware's PKG_NEED_UNPACK lines from the
# recipe at a commit (or the working tree), evaluated against the fixture tree.
#   sb-stamp-device-config.sh <empty scratch dir> [commit|WORKTREE]
D=$(git rev-parse --show-toplevel); R=${2:-8ebaf8daad}
SB=${1:?usage: sb-stamp-device-config.sh <empty scratch dir> [commit|WORKTREE]}; mkdir "$SB" || exit 2; SB=$(cd "$SB" && pwd)
KF=projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk
if [ "$R" = WORKTREE ]; then cat "$D/$KF"; else git -C "$D" show "$R:$KF"; fi | grep '^PKG_NEED_UNPACK' > "$SB/need.sh"
F=$SB/tree
mkdir -p "$F/projects/ROCKNIX/packages/linux-firmware/fixturefw" "$F/projects/ROCKNIX/devices/H700/config"
printf 'PKG_NAME="fixturefw"\nPKG_VERSION="1"\n' > "$F/projects/ROCKNIX/packages/linux-firmware/fixturefw/package.mk"
printf 'brcm/fixture-a.bin\n' > "$F/projects/ROCKNIX/devices/H700/config/kernel-firmware.dat"
: > "$SB/cache_global"
NOONEXIT=yes   # no build is running: config/functions sets no EXIT trap
. "$D/config/functions"
run() {
  ( cd "$F" && ROOT="$F" PROJECT_DIR="$F/projects" PROJECT=ROCKNIX DEVICE=H700 PKG_NAME=fixturefw \
    PKG_DIR="$F/projects/ROCKNIX/packages/linux-firmware/fixturefw" PKG_STAMP= \
    PKG_NEED_UNPACK="$(PROJECT_DIR="$F/projects" PROJECT=ROCKNIX DEVICE=H700 PKG_NAME=fixturefw DISTRO_DIR="$F/distributions" DISTRO=ROCKNIX bash -c ". $SB/need.sh; echo \"\$PKG_NEED_UNPACK\"")" \
    _CACHE_PACKAGE_GLOBAL="$SB/cache_global" "$@" )
}
found=$(run bash -c ". $D/config/functions; find_file_path config/kernel-firmware.dat && echo \"\$FOUND_PATH\"")
echo "find_file_path resolves: ${found#$F/}"
a=$(run calculate_stamp)
printf 'brcm/fixture-b.bin\n' >> "$F/projects/ROCKNIX/devices/H700/config/kernel-firmware.dat"
b=$(run calculate_stamp)
[ "$a" = "$b" ] && echo "RESULT: the device's firmware list changed and the stamp did not move ($a)" || echo "RESULT: the stamp moved"
