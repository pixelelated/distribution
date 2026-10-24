#!/bin/bash
# unpack:90's test, lifted verbatim, over one and two matching directories (#652).
mkdir -p "${1:?usage: sb-unpack-glob.sh <empty scratch dir>}" && cd "$1" || exit 2
for n in one two; do
  U=$PWD/u-$n; mkdir -p "$U/fixturepkg-1.0"; [ $n = two ] && mkdir -p "$U/fixturepkg-1.0-extra"
  PKG_UNPACK_DIR=$U PKG_NAME=fixturepkg PKG_VERSION=1.0 PKG_SOURCE_DIR=
  if [ -z "${PKG_SOURCE_DIR}" -a -d "${PKG_UNPACK_DIR}/${PKG_NAME}-${PKG_VERSION}"* ]; then echo "$n: test true (would mv)"; else echo "$n: test false (rc $?), nothing moved"; fi
done
