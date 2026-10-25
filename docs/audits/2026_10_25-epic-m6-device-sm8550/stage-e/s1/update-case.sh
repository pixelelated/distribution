#!/bin/bash
# T28 S1 (#1109): the SM8550 updater, judged against a fixture card.
#
#   update-case.sh <update.sh> <unfixed|fixed> <updateabl-fail|updateabl-slow-fail|copy-fail|success>
#
# update.sh runs under bash (the image's /bin/sh), inside bwrap with a tmpfs
# root holding fixtures for every path it reads or writes, as init:427-440
# calls it (BOOT_ROOT=/flash, SYSTEM_ROOT=/update exported):
#   /update/usr/share/bootloader/rocknix_abl/   the new build's ABL files
#   /update/usr/bin/updateabl                   a stub: exits 0, or 1, or sleeps then exits 1, by the case;
#                                               it appends one line to /log/updateabl.calls per run
#   /flash/                                     the boot partition, holding old boot/ and EFI/ directories
#   /storage/                                   for the update hint
#   /log/                                       the stubs' records
# and stubs first on PATH: mount (exits 0) and rm (records its arguments in
# /log/rm.log, then runs the real rm).
# Cases:
#   updateabl-fail       the stub updateabl exits 1 at once
#   updateabl-slow-fail  the stub updateabl sleeps 2 s, then exits 1
#   copy-fail            the source rocknix_abl directory is empty (cp's glob matches nothing); updateabl exits 0
#   success              every step succeeds
# Expectations:
#   unfixed: every case exits 0 with UPDATE in .boot.hint; in the updateabl
#            cases boot/ and EFI/ are removed.
#   fixed:   a failing case exits non-zero naming its step (updateabl, or
#            the copy), with no .boot.hint and boot/ and EFI/ still present.
#   success: both sides exit 0, /flash/rocknix_abl carries the source's
#            bytes, updateabl ran once, UPDATE is in .boot.hint, boot/ and
#            EFI/ are removed.
# Writes only under $TMPDIR. Nothing runs on a unit. Prints one verdict line
# last; exits 0 when the side's expectation is met, 1 when not, 2 when it
# cannot run.
set -u
F=${1:?update.sh}; SIDE=${2:?unfixed or fixed}; CASE=${3:?case}
[ -f "$F" ] || { echo "update-case: CANNOT -- no file $F"; exit 2; }
command -v bwrap >/dev/null || { echo "update-case: CANNOT -- no bwrap"; exit 2; }
W=$(mktemp -d "${TMPDIR:?}/s1-update.XXXXXX") || exit 2
B=$W/update/usr/share/bootloader/rocknix_abl
mkdir -p "$B" "$W/update/usr/bin" "$W/flash/boot" "$W/flash/EFI" "$W/storage" "$W/log" "$W/stub"
echo old > "$W/flash/boot/Image"; echo old > "$W/flash/EFI/BOOTAA64.EFI"
if [ "$CASE" != copy-fail ]; then
  head -c 258048 /dev/urandom > "$B/abl_signed-SM8550.elf"
  printf '#!/bin/sh\necho flash\n' > "$B/flash_abl.sh"
fi
case "$CASE" in
  updateabl-fail) U='exit 1' ;;
  updateabl-slow-fail) U='sleep 2; exit 1' ;;
  copy-fail|success) U='exit 0' ;;
  *) echo "update-case: CANNOT -- unknown case $CASE"; exit 2 ;;
esac
printf '#!/bin/sh\necho "updateabl-stub: run" >> /log/updateabl.calls\n%s\n' "$U" > "$W/update/usr/bin/updateabl"
printf '#!/bin/sh\nexit 0\n' > "$W/stub/mount"
printf '#!/bin/sh\necho "rm $*" >> /log/rm.log\nexec /usr/bin/rm "$@"\n' > "$W/stub/rm"
chmod +x "$W/update/usr/bin/updateabl" "$W/stub/"*
bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib \
  --symlink usr/lib64 /lib64 --symlink usr/sbin /sbin --dev /dev --tmpfs /tmp \
  --ro-bind "$W/update" /update --bind "$W/flash" /flash --bind "$W/storage" /storage \
  --bind "$W/log" /log --ro-bind "$W/stub" /stub --ro-bind "$F" /update.sh \
  --setenv PATH /stub:/usr/bin:/usr/sbin --setenv BOOT_ROOT /flash --setenv SYSTEM_ROOT /update \
  --setenv BOOT_PART /dev/mmcblk0p1 \
  bash /update.sh > "$W/out" 2> "$W/err"
rc=$?
hint=no; [ "$(cat "$W/storage/.boot.hint" 2>/dev/null)" = UPDATE ] && hint=yes
kept=no; [ -d "$W/flash/boot" ] && [ -d "$W/flash/EFI" ] && kept=yes
removed=no; [ ! -e "$W/flash/boot" ] && [ ! -e "$W/flash/EFI" ] && removed=yes
calls=0; [ -f "$W/log/updateabl.calls" ] && calls=$(wc -l < "$W/log/updateabl.calls")
same=no; [ "$CASE" != copy-fail ] && cmp -s "$B/abl_signed-SM8550.elf" "$W/flash/rocknix_abl/abl_signed-SM8550.elf" && \
  cmp -s "$B/flash_abl.sh" "$W/flash/rocknix_abl/flash_abl.sh" && same=yes
named=no
case "$CASE" in
  updateabl-fail|updateabl-slow-fail) grep -q 'update.sh: .*updateabl' "$W/out" "$W/err" && named=yes ;;
  copy-fail) grep -q -i 'update.sh: .*cop' "$W/out" "$W/err" && named=yes ;;
esac
sed 's/^/  | out: /' "$W/out"; sed 's/^/  | err: /' "$W/err"; [ -f "$W/log/rm.log" ] && sed 's/^/  | log: /' "$W/log/rm.log"
facts="rc=$rc hint=$hint boot-and-EFI=$([ $kept = yes ] && echo kept || { [ $removed = yes ] && echo removed || echo partial; }) updateabl-runs=$calls copied-same=$same named=$named"
case "$SIDE:$CASE" in
  unfixed:updateabl-fail|unfixed:updateabl-slow-fail) [ "$rc" = 0 ] && [ $hint = yes ] && [ $removed = yes ] && ok=1 || ok=0 ;;
  unfixed:copy-fail) [ "$rc" = 0 ] && [ $hint = yes ] && ok=1 || ok=0 ;;
  fixed:updateabl-fail|fixed:updateabl-slow-fail|fixed:copy-fail) [ "$rc" != 0 ] && [ $hint = no ] && [ $kept = yes ] && [ $named = yes ] && ok=1 || ok=0 ;;
  *:success) [ "$rc" = 0 ] && [ $hint = yes ] && [ $removed = yes ] && [ "$calls" = 1 ] && [ $same = yes ] && ok=1 || ok=0 ;;
  *) echo "update-case: CANNOT -- side $SIDE"; exit 2 ;;
esac
if [ "$ok" = 1 ]; then
  echo "update-case $CASE: $SIDE-expectation-met ($facts)"; exit 0
fi
echo "update-case $CASE: UNEXPECTED on $SIDE ($facts)"; exit 1
