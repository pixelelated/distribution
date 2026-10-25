#!/bin/bash
# T11 S1 (#1090): source projects/ROCKNIX/bootloader/release the way
# scripts/image:285 does (INSTALL, RELEASE_DIR set; no set -e) and judge
# whether a failed copy is reported.
#
#   release-case.sh <release file> <unfixed|fixed> <unwritable|empty|normal>
#
# normal (the control): staged files and a writable destination; both sides
#   copy them and carry on with process rc 0.
# unwritable: staged files, but ${RELEASE_DIR}/3rdparty/bootloader is mode 555.
# empty:      ${INSTALL}/usr/share/bootloader exists and holds nothing.
#   unfixed: the sourced script returns (cp's status, which scripts/image
#            never reads) and the image step carries on: process rc 0.
#   fixed:   the step exits non-zero, so scripts/image stops.
# Writes only under $TMPDIR; prints one verdict line last; exits 0 when the
# named side's expectation is met, 1 when it is not, 2 when it cannot run.
set -u
F=${1:?release file}; SIDE=${2:?unfixed or fixed}; CASE=${3:?unwritable, empty or normal}
[ -f "$F" ] || { echo "release-case: CANNOT -- no file $F"; exit 2; }
[ "$(id -u)" != 0 ] || { echo "release-case: CANNOT -- root ignores mode 555"; exit 2; }
W=$(mktemp -d "${TMPDIR:?}/s1-release.XXXXXX") || exit 2
mkdir -p "$W/inst/usr/share/bootloader" "$W/rel"
case "$CASE" in
  unwritable) printf 'fixture\n' > "$W/inst/usr/share/bootloader/loader.bin"
              mkdir -p "$W/rel/3rdparty/bootloader"; chmod 555 "$W/rel/3rdparty/bootloader" ;;
  empty) ;;
  normal) printf 'fixture\n' > "$W/inst/usr/share/bootloader/loader.bin" ;;
  *) echo "release-case: CANNOT -- unknown case $CASE"; exit 2 ;;
esac
INSTALL="$W/inst" RELEASE_DIR="$W/rel" \
  bash -c 'set +e; . "$1"; echo "SOURCED-RETURNED rc=$?"' _ "$F" > "$W/out" 2>&1
rc=$?
chmod 755 "$W/rel/3rdparty/bootloader" 2>/dev/null
returned=no; grep -q '^SOURCED-RETURNED' "$W/out" && returned=yes
src_rc=$(sed -n 's/^SOURCED-RETURNED rc=//p' "$W/out")
sed 's/^/  | /' "$W/out"
facts="rc=$rc carried-on=$returned sourced-rc=${src_rc:-none}"
copied=no; [ -e "$W/rel/3rdparty/bootloader/loader.bin" ] && copied=yes
facts="$facts copied=$copied"
case "$SIDE:$CASE" in
  *:normal) [ "$rc" = 0 ] && [ "$returned" = yes ] && [ "$copied" = yes ] && ok=1 || ok=0 ;;
  unfixed:*) [ "$rc" = 0 ] && [ "$returned" = yes ] && ok=1 || ok=0 ;;
  fixed:*)   [ "$rc" != 0 ] && [ "$returned" = no ] && ok=1 || ok=0 ;;
  *) echo "release-case: CANNOT -- side $SIDE"; exit 2 ;;
esac
if [ "$ok" = 1 ]; then
  echo "release-case $CASE: $SIDE-expectation-met ($facts)"; exit 0
fi
echo "release-case $CASE: UNEXPECTED on $SIDE ($facts)"; exit 1
