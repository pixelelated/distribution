#!/bin/bash
set -e
get_build_dir() {
 case "$1" in
  raofflineproxy-rcheevos) echo /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18/build.pixelelated-GENERIC_X64.x86_64/build/raofflineproxy-rcheevos-1433173220a7eaede6a9ed7a18e94117be1821e0;;
  raofflineproxy-libchdr) echo /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18/build.pixelelated-GENERIC_X64.x86_64/build/raofflineproxy-libchdr-607694ca0812edfc9cc2030c64634fc2393668de;;
  *) return 1;;
 esac
}
source /workspace/repos/rocknix.worktrees/m7-component-inputs/projects/ROCKNIX/packages/network/raofflineproxy/package.mk
CC=cc
CFLAGS=''
LDFLAGS=''
PKG_BUILD=/workspace/tmp/pix541-refresh72/final-patched
TARGET_NAME=host-qualification-541
make_target
