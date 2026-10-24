#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
#
# regen-es-systems.sh -- the launch table regenerated on the host from the
# tree's own shell (M6 T3, #650; brief section 5, "the generated table").
#
#   regen-es-systems.sh <tree> <outdir> <xmlstarlet> DEVICE ARCH ENABLE_32BIT WINDOWMANAGER PREFER_GLES
#
# Sources distributions/ROCKNIX/config/functions and the emulators
# metapackage's recipe from <tree>, then runs the recipe's
# makeinstall_target under errexit (config/path sets set -e for the real
# build). Every path the run writes is under <outdir>: ESTMP, the doc
# cache, SYSDOC and INSTALL. Nothing touches /usr or /storage on the host.
#
# <xmlstarlet> is the build's own host tool, copied from a build root's
# toolchain/bin and passed by path. add_es_system calls it for every core,
# not only for the final format, so without it the systems come out with
# no emulators.
#
# get_pkg_version is the build engine's (config/functions); here it is a
# stub reading PKG_VERSION="..." from the recipe that pkgcheck would check:
# the projects/ROCKNIX override first, else the generic one. It counts its
# calls and its misses into <outdir>/stub-get_pkg_version.txt, because a
# stub is part of the claim (blindspot 74). The core-pins it produces is
# compared with the image's core-pins, not trusted.
set -e
TREE=$1 OUT=$2 XS=$3
export DEVICE=$4 ARCH=$5 ENABLE_32BIT=$6 WINDOWMANAGER=$7 PREFER_GLES=$8
[ -d "$TREE/projects" ] && [ -n "$OUT" ] && [ -x "$XS" ] && [ -n "$DEVICE" ] && [ -n "$ARCH" ] || {
  echo "usage: $0 <tree> <outdir> <xmlstarlet> DEVICE ARCH ENABLE_32BIT WINDOWMANAGER PREFER_GLES" >&2; exit 2; }
mkdir -p "$OUT/bin" "$OUT/install"
ln -sf "$XS" "$OUT/bin/xmlstarlet"
export PATH="$OUT/bin:/usr/bin:/bin"
export ROOT="$OUT/root" INSTALL="$OUT/install" TARGET_TYPE=""
export PKG_DIR="$TREE/projects/ROCKNIX/packages/virtual/emulators"
export SYSDOCROOT="$OUT/doc" SYSDOC="$OUT/doc/SUPPORTED_EMULATORS_AND_CORES"
export PROJECT_DIR="$TREE/projects" PROJECT=ROCKNIX
# ROOT is where clean_es_cache and clean_doc_cache put their caches and
# where add_es_system reads config/emulators/*.conf, so it carries the
# tree's config/ (a symlink, read only) and nothing else of the tree.
mkdir -p "$ROOT"; ln -sfn "$TREE/config" "$ROOT/config"
: > "$OUT/stub-get_pkg_version.txt"
get_pkg_version() {
  local f
  f=$(find "$TREE/projects/ROCKNIX/packages" "$TREE/packages" -path "*/$1/package.mk" 2>/dev/null | head -1)
  if [ -z "$f" ]; then echo "miss $1" >> "$OUT/stub-get_pkg_version.txt"; return 0; fi
  echo "call $1 ${f#"$TREE"/}" >> "$OUT/stub-get_pkg_version.txt"
  sed -n 's/^PKG_VERSION="\([^"]*\)".*/\1/p' "$f" | head -1
}
cd "$OUT"
. "$TREE/distributions/ROCKNIX/config/functions"
. "$PKG_DIR/package.mk"
makeinstall_target
echo "regen: DEVICE=$DEVICE ARCH=$ARCH rc=0 systems=$(grep -c '<system>' "$ROOT/.es_cache/$DEVICE/.es_systems.cfg")"
