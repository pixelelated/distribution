#!/bin/bash
# T27 S1 (#1095): the H700 bootloader updater, judged against a fixture card.
#
#   update-case.sh <update.sh> <unfixed|fixed> <remount-fail|copy-fail|dd-fail|success|ddr3|unknown-voltage>
#
# Controls, the same on both sides: ddr3 (vdd-dram 1.2 V writes the DDR3
# loader) and unknown-voltage (1.3 V: exit 0, no loader written, the disk
# untouched), so the thresholds are shown unchanged.
#
# update.sh runs under bash (the image's /bin/sh), inside bwrap with a tmpfs
# root holding fixtures for every path it reads or writes, as init:427-440
# calls it (BOOT_ROOT=/flash, SYSTEM_ROOT=/update):
#   /update/usr/share/bootloader/   the new build's trees, overlay and loaders
#   /flash/                         the boot partition, with the old dtb.img
#   /proc/device-tree/rocknix-dt-id the running tree's id (a fixture file)
#   /sys/class/regulator/regulator.0/{name,microvolts}  vdd-dram at 1.1 V (DDR4)
#   /disk.img                       the boot disk (BOOT_DISK, BOOT_PART given)
#   /storage/                       for the update hint
# and stubs first on PATH:
#   remount-fail  mount fails, and /flash is read-only (mode 555/444), as a
#                 failed remount leaves it
#   copy-fail     cp writes half of the source and fails when the destination
#                 is dtb.img or a name beside it
#   dd-fail       dd fails
#   success       no stub; the real commands
# Expectations:
#   unfixed: remount-fail, copy-fail and dd-fail exit 0 (copy-fail with
#            dtb.img truncated); fixed: each exits non-zero naming the step,
#            with dtb.img byte-identical to the old one. success: both exit 0
#            with dtb.img the new tree and the loader at 8 KiB of the disk.
# Writes only under $TMPDIR. Nothing runs on a unit. Prints one verdict line
# last; exits 0 when the side's expectation is met, 1 when not, 2 when it
# cannot run.
set -u
F=${1:?update.sh}; SIDE=${2:?unfixed or fixed}; CASE=${3:?case}
[ -f "$F" ] || { echo "update-case: CANNOT -- no file $F"; exit 2; }
command -v bwrap >/dev/null || { echo "update-case: CANNOT -- no bwrap"; exit 2; }
[ "$(id -u)" != 0 ] || { echo "update-case: CANNOT -- root ignores the read-only modes"; exit 2; }
W=$(mktemp -d "${TMPDIR:?}/s1-update.XXXXXX") || exit 2
B=$W/update/usr/share/bootloader
mkdir -p "$B/device_trees" "$B/overlays" "$W/flash/device_trees" "$W/flash/overlays" \
         "$W/proc/device-tree" "$W/sys/class/regulator/regulator.0" "$W/storage" "$W/stub"
ID=sun50i-h700-anbernic-rg35xx-sp-v2-panel
head -c 4096 /dev/urandom > "$B/device_trees/$ID.dtb"
head -c 2048 /dev/urandom > "$B/device_trees/sun50i-h700-anbernic-rg-sp.dtb"
head -c 512 /dev/urandom > "$B/overlays/sun50i-h700-anbernic-rg35xx-2024-ddr3.dtbo"
head -c 8192 /dev/urandom > "$B/H700_DDR4_u-boot-sunxi-with-spl.bin"
head -c 8192 /dev/urandom > "$B/H700_DDR3_u-boot-sunxi-with-spl.bin"
head -c 4096 /dev/urandom > "$W/flash/dtb.img"; cp "$W/flash/dtb.img" "$W/old-dtb.img"
printf '%s\0' "$ID" > "$W/proc/device-tree/rocknix-dt-id"
printf 'vdd-dram\n' > "$W/sys/class/regulator/regulator.0/name"
printf '1100000\n' > "$W/sys/class/regulator/regulator.0/microvolts"
head -c 65536 /dev/zero > "$W/disk.img"
case "$CASE" in
  remount-fail)
    printf '#!/bin/sh\necho "mount-stub: $*" >&2\nexit 1\n' > "$W/stub/mount" ;;
  copy-fail)
    printf '#!/bin/sh\nfor last; do :; done\ncase "$last" in\n  */dtb.img|*/dtb.img.*) for src; do break; done; [ "$src" = -f ] && src=$2\n    head -c 1000 "$src" > "$last"; echo "cp-stub: failed part-way to $last" >&2; exit 1 ;;\nesac\nexec /usr/bin/cp "$@"\n' > "$W/stub/cp" ;;
  dd-fail)
    printf '#!/bin/sh\necho "dd-stub: $*" >&2\nexit 1\n' > "$W/stub/dd" ;;
  success) ;;
  ddr3) printf '1200000\n' > "$W/sys/class/regulator/regulator.0/microvolts" ;;
  unknown-voltage) printf '1300000\n' > "$W/sys/class/regulator/regulator.0/microvolts" ;;
  *) echo "update-case: CANNOT -- unknown case $CASE"; exit 2 ;;
esac
[ -e "$W/stub/mount" ] || printf '#!/bin/sh\nexit 0\n' > "$W/stub/mount"
chmod +x "$W/stub/"*
if [ "$CASE" = remount-fail ]; then
  chmod 444 "$W/flash/dtb.img"; chmod 555 "$W/flash/device_trees" "$W/flash/overlays" "$W/flash"
fi
bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib \
  --symlink usr/lib64 /lib64 --symlink usr/sbin /sbin --dev /dev --tmpfs /tmp \
  --ro-bind "$W/update" /update --bind "$W/flash" /flash --ro-bind "$W/proc" /proc \
  --ro-bind "$W/sys" /sys --bind "$W/storage" /storage --bind "$W/disk.img" /disk.img \
  --ro-bind "$W/stub" /stub --ro-bind "$F" /update.sh \
  --setenv PATH /stub:/usr/bin:/usr/sbin --setenv BOOT_ROOT /flash --setenv SYSTEM_ROOT /update \
  --setenv BOOT_PART /dev/mmcblk0p1 --setenv BOOT_DISK /disk.img \
  bash /update.sh > "$W/out" 2> "$W/err"
rc=$?
chmod -R u+w "$W/flash" 2>/dev/null
same_old=no; cmp -s "$W/flash/dtb.img" "$W/old-dtb.img" && same_old=yes
is_new=no; cmp -s "$W/flash/dtb.img" "$B/device_trees/$ID.dtb" && is_new=yes
size=$(stat -c %s "$W/flash/dtb.img" 2>/dev/null || echo 0)
loader=no; cmp -s <(dd if="$W/disk.img" bs=1K skip=8 count=8 2>/dev/null) "$B/H700_DDR4_u-boot-sunxi-with-spl.bin" && loader=yes
loader3=no; cmp -s <(dd if="$W/disk.img" bs=1K skip=8 count=8 2>/dev/null) "$B/H700_DDR3_u-boot-sunxi-with-spl.bin" && loader3=yes
untouched=no; cmp -s "$W/disk.img" <(head -c 65536 /dev/zero) && untouched=yes
stray=$(ls "$W/flash" | grep -c '^dtb\.img\.' || true)
sed 's/^/  | out: /' "$W/out"; sed 's/^/  | err: /' "$W/err"
named=no
case "$CASE" in
  remount-fail) grep -qi 'update.sh: .*remount' "$W/err" && named=yes ;;
  copy-fail) grep -qi 'dtb.img' "$W/err" && grep -q 'update.sh' "$W/err" && named=yes ;;
  dd-fail) grep -qi -E 'loader|u-boot|dd' "$W/err" && grep -q 'update.sh' "$W/err" && named=yes ;;
esac
facts="rc=$rc dtb.img=$( [ $same_old = yes ] && echo old || { [ $is_new = yes ] && echo new || echo "other(${size}B)"; } ) loader=$loader ddr3-loader=$loader3 disk-untouched=$untouched named=$named stray=$stray"
case "$SIDE:$CASE" in
  unfixed:remount-fail|unfixed:dd-fail) [ "$rc" = 0 ] && ok=1 || ok=0 ;;
  unfixed:copy-fail) [ "$rc" = 0 ] && [ "$same_old" = no ] && [ "$is_new" = no ] && ok=1 || ok=0 ;;
  fixed:remount-fail|fixed:copy-fail) [ "$rc" != 0 ] && [ "$same_old" = yes ] && [ "$named" = yes ] && [ "$stray" = 0 ] && ok=1 || ok=0 ;;
  fixed:dd-fail) [ "$rc" != 0 ] && [ "$named" = yes ] && ok=1 || ok=0 ;;
  *:ddr3) [ "$rc" = 0 ] && [ "$is_new" = yes ] && [ "$loader3" = yes ] && ok=1 || ok=0 ;;
  *:unknown-voltage) [ "$rc" = 0 ] && [ "$is_new" = yes ] && [ "$untouched" = yes ] && ok=1 || ok=0 ;;
  *:success) [ "$rc" = 0 ] && [ "$is_new" = yes ] && [ "$loader" = yes ] && ok=1 || ok=0 ;;
  *) echo "update-case: CANNOT -- side $SIDE"; exit 2 ;;
esac
if [ "$ok" = 1 ]; then
  echo "update-case $CASE: $SIDE-expectation-met ($facts)"; exit 0
fi
echo "update-case $CASE: UNEXPECTED on $SIDE ($facts)"; exit 1
