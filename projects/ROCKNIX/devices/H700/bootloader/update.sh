#!/bin/sh
# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)

[ -z "$SYSTEM_ROOT" ] && SYSTEM_ROOT=""
[ -z "$BOOT_ROOT" ] && BOOT_ROOT="/flash"
[ -z "$BOOT_PART" ] && BOOT_PART=$(df "$BOOT_ROOT" | tail -1 | awk {' print $1 '})

# init runs this after an update and prints success over its result, so a
# step that fails must say so and stop: a silent failure here can leave the
# card without a usable tree or loader (#1095).
fail() {
  echo "update.sh: $*" >&2
  mount -o remount,ro $BOOT_ROOT 2>/dev/null
  exit 1
}
UBOOT_BIN=""
VDD_REG_PATH=""

# identify the boot device
if [ -z "$BOOT_DISK" ]; then
  case $BOOT_PART in
    /dev/mmcblk*)
      BOOT_DISK=$(echo $BOOT_PART | sed -e "s,p[0-9]*,,g")
      ;;
  esac
fi

# mount $BOOT_ROOT rw
mount -o remount,rw $BOOT_ROOT || fail "could not remount $BOOT_ROOT read-write"

echo "Updating device trees..."
mkdir -p $BOOT_ROOT/device_trees || fail "could not create $BOOT_ROOT/device_trees"
cp -f $SYSTEM_ROOT/usr/share/bootloader/device_trees/* $BOOT_ROOT/device_trees || fail "could not copy the device trees"
mkdir -p $BOOT_ROOT/overlays || fail "could not create $BOOT_ROOT/overlays"
for o in $SYSTEM_ROOT/usr/share/bootloader/overlays/*; do
  [ -e "$o" ] || break
  cp -f "$o" $BOOT_ROOT/overlays || fail "could not copy the overlay $(basename "$o")"
done

DT_ID=$(cat /proc/device-tree/rocknix-dt-id)

UPDATE_DTB_SOURCE="$BOOT_ROOT/device_trees/$DT_ID.dtb"
if [ -f "$UPDATE_DTB_SOURCE" ]; then
  echo "Updating dtb.img from $(basename $UPDATE_DTB_SOURCE)..."
  # Whole or not at all: written beside the old one, renamed into place.
  if ! cp -f "$UPDATE_DTB_SOURCE" "$BOOT_ROOT/dtb.img.new"; then
    rm -f "$BOOT_ROOT/dtb.img.new"
    fail "could not write dtb.img; the previous one is unchanged"
  fi
  mv -f "$BOOT_ROOT/dtb.img.new" "$BOOT_ROOT/dtb.img" || fail "could not replace dtb.img"
fi

# detect DDR3/DDR4
for r in /sys/class/regulator/regulator.*/; do
  [[ "$(cat "$r/name" 2>/dev/null)" == "vdd-dram" ]] && VDD_REG_PATH=$r
done

if [ -n "${VDD_REG_PATH:-}" ]; then
  DCDC3_MICROVOLTS=$(cat "$VDD_REG_PATH/microvolts")
  case "$DCDC3_MICROVOLTS" in
    1200000)
      UBOOT_BIN="H700_DDR3_u-boot-sunxi-with-spl.bin"
      ;;
    1100000)
      UBOOT_BIN="H700_DDR4_u-boot-sunxi-with-spl.bin"
      ;;
  esac
fi

# update bootloader
if [ -n "${UBOOT_BIN:-}" ]; then
  if [ -f $SYSTEM_ROOT/usr/share/bootloader/$UBOOT_BIN ]; then
    [ -n "$BOOT_DISK" ] || fail "no boot disk found for $BOOT_PART; the u-boot loader was not written"
    echo "Updating u-boot on: $BOOT_DISK..."
    dd if=$SYSTEM_ROOT/usr/share/bootloader/$UBOOT_BIN of=$BOOT_DISK bs=1K seek=8 conv=fsync,notrunc &>/dev/null \
      || fail "could not write the u-boot loader $UBOOT_BIN to $BOOT_DISK"
  fi
fi

# mount $BOOT_ROOT ro
sync
mount -o remount,ro $BOOT_ROOT

echo "UPDATE" > /storage/.boot.hint
