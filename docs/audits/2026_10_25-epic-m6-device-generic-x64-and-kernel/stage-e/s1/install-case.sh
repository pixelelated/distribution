#!/bin/bash
# T11 S1 (#1090, PL-06): source projects/ROCKNIX/bootloader/install the way
# scripts/image:280 does (INSTALL, BOOTLOADER, DEVICE set; no set -e) over a
# fixture INSTALL tree, and judge what the step did.
#
#   install-case.sh <install file> <unfixed|fixed> <missing-syslinux|grub|present-syslinux>
#
# present-syslinux (the control): syslinux files staged; both sides copy them
#   and return 0 with "completed".
# missing-syslinux: BOOTLOADER=syslinux and no ${INSTALL}/usr/share/syslinux.
#   unfixed: the step returns 0 and prints "installation completed".
#   fixed:   the step exits non-zero, naming the missing path.
# grub: BOOTLOADER=grub with a file under ${INSTALL}/usr/share/grub.
#   unfixed: the file is copied and the step returns 0 with "completed".
#   fixed:   the step exits non-zero naming "grub" and copies nothing.
# Writes only under $TMPDIR; prints one verdict line last; exits 0 when the
# named side's expectation is met, 1 when it is not, 2 when it cannot run.
set -u
F=${1:?install file}; SIDE=${2:?unfixed or fixed}; CASE=${3:?missing-syslinux, grub or present-syslinux}
[ -f "$F" ] || { echo "install-case: CANNOT -- no file $F"; exit 2; }
W=$(mktemp -d "${TMPDIR:?}/s1-install.XXXXXX") || exit 2
mkdir -p "$W/inst"
case "$CASE" in
  missing-syslinux) BL=syslinux ;;
  present-syslinux) BL=syslinux; mkdir -p "$W/inst/usr/share/syslinux"; printf 'fixture\n' > "$W/inst/usr/share/syslinux/ldlinux.e64" ;;
  grub) BL=grub; mkdir -p "$W/inst/usr/share/grub"; printf 'fixture\n' > "$W/inst/usr/share/grub/grubx64.efi" ;;
  *) echo "install-case: CANNOT -- unknown case $CASE"; exit 2 ;;
esac
INSTALL="$W/inst" BOOTLOADER="$BL" DEVICE=FIXTURE \
  bash -c 'set +e; . "$1"; echo "SOURCED-RETURNED rc=$?"' _ "$F" > "$W/out" 2>&1
rc=$?
out=$(cat "$W/out")
returned=no; grep -q '^SOURCED-RETURNED' "$W/out" && returned=yes
completed=no; grep -q 'installation completed' "$W/out" && completed=yes
copied=no; [ -e "$W/inst/usr/share/bootloader/grubx64.efi" ] || [ -e "$W/inst/usr/share/bootloader/ldlinux.e64" ] && copied=yes
named=no
case "$CASE" in
  missing-syslinux|present-syslinux) grep -q 'usr/share/syslinux' "$W/out" && named=yes ;;
  grub) grep -q 'grub' "$W/out" && named=yes ;;
esac
printf '%s\n' "$out" | sed 's/^/  | /'
facts="rc=$rc returned=$returned completed=$completed named=$named copied=$copied"
case "$SIDE:$CASE" in
  unfixed:missing-syslinux) [ "$rc" = 0 ] && [ "$returned" = yes ] && [ "$completed" = yes ] && ok=1 || ok=0 ;;
  fixed:missing-syslinux)   [ "$rc" != 0 ] && [ "$returned" = no ] && [ "$completed" = no ] && [ "$named" = yes ] && ok=1 || ok=0 ;;
  unfixed:grub)             [ "$rc" = 0 ] && [ "$completed" = yes ] && [ "$copied" = yes ] && ok=1 || ok=0 ;;
  fixed:grub)               [ "$rc" != 0 ] && [ "$returned" = no ] && [ "$named" = yes ] && [ "$copied" = no ] && ok=1 || ok=0 ;;
  *:present-syslinux)       [ "$rc" = 0 ] && [ "$returned" = yes ] && [ "$completed" = yes ] && [ "$copied" = yes ] && ok=1 || ok=0 ;;
  *) echo "install-case: CANNOT -- side $SIDE"; exit 2 ;;
esac
if [ "$ok" = 1 ]; then
  echo "install-case $CASE: $SIDE-expectation-met ($facts)"; exit 0
fi
echo "install-case $CASE: UNEXPECTED on $SIDE ($facts)"; exit 1
