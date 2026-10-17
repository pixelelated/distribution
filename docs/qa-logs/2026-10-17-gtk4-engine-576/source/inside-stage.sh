#!/bin/bash
set -euo pipefail
[ "$1" = webkitgtk ]
[ ! -e build.pixelelated-GENERIC_X64.x86_64/build/webkitgtk-2.54.1 ]
mkdir -p sources/webkitgtk
for suffix in '' .url .sha256; do
  [ ! -e "sources/webkitgtk/webkitgtk-2.54.1.tar.xz$suffix" ]
  cp --reflink=never -- "/source-input/webkitgtk-2.54.1.tar.xz$suffix" "sources/webkitgtk/webkitgtk-2.54.1.tar.xz$suffix"
done
python3 -I /build-owner/verify-source.py
exec ./scripts/build webkitgtk
