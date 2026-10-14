#!/usr/bin/env bash
# UNRUN: exact current recipe make_target; explicit GENERIC_X64 flags.
set -euo pipefail
export LC_ALL=C LANG=C
: "${PIX583_TC:?}" "${PIX583_WORK:?}"
export CCACHE_DISABLE=1
export CCACHE_TEMPDIR="$PIX583_WORK/tmp"
export TMPDIR="$PIX583_WORK/tmp"
CC="$PIX583_TC/bin/x86_64-rocknix-linux-gnu-gcc"
CFLAGS='-march=x86-64-v3 -mtune=generic -Wall -pipe -O2 -fomit-frame-pointer -fPIC -DPIC'
LDFLAGS='-march=x86-64-v3 -mtune=generic -Wl,--as-needed -fuse-ld=bfd -fPIC'
TARGET_NAME=x86_64-rocknix-linux-gnu
PKG_BUILD="$PIX583_WORK/sources/RAOfflineProxy-c7ebd1b6e777f3751ff0ecdf8aba54045844e00d"
get_build_dir() {
  case "$1" in
    raofflineproxy-rcheevos) printf '%s\n' "$PIX583_WORK/sources/rcheevos-1433173220a7eaede6a9ed7a18e94117be1821e0" ;;
    raofflineproxy-libchdr) printf '%s\n' "$PIX583_WORK/sources/libchdr-607694ca0812edfc9cc2030c64634fc2393668de" ;;
    *) return 2 ;;
  esac
}
source /plan/make-target.sh
# Trace the original complete argv and compiler/link diagnostics in selected-stage.stderr.
set -x
make_target
