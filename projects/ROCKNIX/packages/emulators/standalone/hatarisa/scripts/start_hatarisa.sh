#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present 5schatten (https://github.com/5schatten)
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)

. /etc/profile
set_kill set "-9 hatarisa"

# Set some common variables
HATARI_DIR_HOME=/storage/.hatari
HATARI_DIR=/storage/.config/hatari
HATARI_CONFIG_DIR=$HATARI_DIR/conf
HATARI_TMP_DIR=/tmp/hatari
HATARI_TMP_CONFIG="$HATARI_TMP_DIR"/.hatari-temp.cfg
HATARI_LOG="/var/log/hatari.log"
MAX_DRIVES=2
i=0

# create symlink to hatari config dir
link_storage_dir "$HATARI_DIR_HOME" "$HATARI_DIR"

# Which file should hatari load?
echo "Trying to boot this game:" "$1" >> $HATARI_LOG

# Create a clean working directory
if [ -d "$HATARI_TMP_DIR" ]; then
  echo "Clean up old working directory." >> $HATARI_LOG
  rm -rf "$HATARI_TMP_DIR"
fi
mkdir -p "$HATARI_TMP_DIR"

# Seed the default config if the player has none (it is copied to /storage
# only by the first boot's seed), then copy it to tmp
if [ ! -f "$HATARI_CONFIG_DIR/Atari-ST-default.cfg" ]; then
  mkdir -p "$HATARI_CONFIG_DIR"
  cp /usr/config/hatari/conf/Atari-ST-default.cfg "$HATARI_CONFIG_DIR/"
fi
cp "$HATARI_CONFIG_DIR/Atari-ST-default.cfg" "$HATARI_TMP_CONFIG"

# Check if we are loading a .zip file
if case "$1" in *.[zZ][iI][pP]) true ;; *) false ;; esac; then

  #unpack the zip file
  unzip -q -o "$1" -d "$HATARI_TMP_DIR"

  # Assign the archive's disk images, in name order, to floppy A and B:
  # each line written as data (echo -e read backslashes in a name and split
  # it on spaces, and every file in the folder became a floppy, #871)
  echo "Assigned floppy drives:" >> "$HATARI_LOG"
  for FILE in "$HATARI_TMP_DIR"/*
  do
    case "${FILE,,}" in *.st|*.msa|*.dim|*.stx|*.ipf) ;; *) continue ;; esac
    [ -f "$FILE" ] || continue
    i=$(($i+1))
    case "$i" in
    1) DRIVE=A ;;
    2) DRIVE=B ;;
    esac
    printf 'szDisk%sFileName = %s\n' "$DRIVE" "$FILE" | tee -a "$HATARI_LOG" >> "$HATARI_TMP_CONFIG"

    # This emulator supports 2 floppies max
    if [ $i -eq $MAX_DRIVES ]; then
      break;
    fi
  done

    # Start hatari with the floppies added to .hatari-temp.cfg
    nice -n -19 hatarisa --configfile "$HATARI_TMP_CONFIG" >> $HATARI_LOG 2>&1

# Check for .cfg config file
elif case "$1" in *.[cC][fF][gG]) true ;; *) false ;; esac; then
  nice -n -19 hatarisa --configfile "$1" >> $HATARI_LOG 2>&1
# All other files
else
  nice -n -19 hatarisa --configfile "$HATARI_TMP_CONFIG" --disk-a "$1" >> $HATARI_LOG 2>&1
fi
# Remove temporary dir
rm -rf "$HATARI_TMP_DIR"
