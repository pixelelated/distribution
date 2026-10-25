#!/bin/bash
# T11 S3 (PL-10): does GENERIC_X64's options say why BOOTLOADER="syslinux"?
#
#   options-comment.sh <devices/GENERIC_X64/options> <unfixed|fixed>
#
# Reads the comment line directly above BOOTLOADER=.
#   unfixed: it names no reason (the generic "Additional bootloader settings").
#   fixed:   it names syslinux, BIOS and UEFI (scripts/mkimage writes both
#            loaders; vm/profile.json boots UEFI).
# Prints `grep -n -B1 'BOOTLOADER='` and one verdict line last; exits 0 when
# the side's expectation is met, 1 when not, 2 when it cannot run.
set -u
F=${1:?options file}; SIDE=${2:?unfixed or fixed}
[ -f "$F" ] || { echo "options-comment: CANNOT -- no file $F"; exit 2; }
grep -n -B1 'BOOTLOADER=' "$F" | sed 's/^/  | /'
above=$(grep -B1 'BOOTLOADER=' "$F" | head -1)
case "$above" in *'#'*) ;; *) above="" ;; esac
why=no
case "$above" in *syslinux*) case "$above" in *BIOS*) case "$above" in *UEFI*) why=yes ;; esac ;; esac ;; esac
case "$SIDE" in
  unfixed) [ "$why" = no ] && ok=1 || ok=0 ;;
  fixed)   [ "$why" = yes ] && ok=1 || ok=0 ;;
  *) echo "options-comment: CANNOT -- side $SIDE"; exit 2 ;;
esac
if [ "$ok" = 1 ]; then
  echo "options-comment: $SIDE-expectation-met (why-named=$why)"; exit 0
fi
echo "options-comment: UNEXPECTED on $SIDE (why-named=$why)"; exit 1
