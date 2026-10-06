#!/bin/bash
set -e
get_build_dir() {
 case "$1" in
  raofflineproxy-rcheevos) echo /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement10/build.pixelelated-GENERIC_X64.x86_64/build/raofflineproxy-rcheevos-1433173220a7eaede6a9ed7a18e94117be1821e0;;
  raofflineproxy-libchdr) echo /tmp/pixelelated-proxy-3036478/libchdr/libchdr-607694ca0812edfc9cc2030c64634fc2393668de;;
  *) return 1;;
 esac
}
source /workspace/repos/rocknix.worktrees/conflict-resolution/projects/ROCKNIX/packages/network/raofflineproxy/package.mk
CC=cc
CFLAGS=''
LDFLAGS=''
PKG_BUILD=/tmp/pixelelated-p3-20261006/patched-b09
TARGET_NAME=host-qualification-b09
make_target
