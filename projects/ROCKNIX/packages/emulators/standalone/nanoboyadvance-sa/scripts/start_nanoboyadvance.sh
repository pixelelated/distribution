#!/bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2022-present JELOS (https://github.com/JustEnoughLinuxOS)
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)

. /etc/profile
set_kill set "-9 NanoBoyAdvance"

#Check if nanoboyadvance exists in .config
if [ ! -d "/storage/.config/nanoboyadvance" ]; then
    mkdir -p "/storage/.config/nanoboyadvance"
        cp -r "/usr/config/nanoboyadvance" "/storage/.config/"
fi

#Make nanoboyadvance bios folder
if [ ! -d "/storage/roms/bios/gba" ]; then
    mkdir -p "/storage/roms/bios/gba"
fi

#The old script copied the whole config folder to gba/gba_bios.bin, a
#directory nothing reads (config.toml's bios_path is bios/gba_bios.bin).
#Remove it only when it is exactly that copy.
OLD_BIOS_COPY="/storage/roms/bios/gba/gba_bios.bin"
if [ -d "${OLD_BIOS_COPY}" ] && [ ! -L "${OLD_BIOS_COPY}" ] && \
   diff -r "/usr/config/nanoboyadvance" "${OLD_BIOS_COPY}" >/dev/null 2>&1; then
  rm -rf "${OLD_BIOS_COPY}"
fi

#Set the cores to use
GAME=$(echo "${1}"| sed "s#^/.*/##")
PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
if [ "${CORES}" = "little" ]
then
  EMUPERF="${SLOW_CORES}"
elif [ "${CORES}" = "big" ]
then
  EMUPERF="${FAST_CORES}"
else
  ### All..
  unset EMUPERF
fi

#NanoBoyAdvance exits without a BIOS at bios_path (#886). Point it at the
#player's BIOS when there is one, else at the open BIOS the image ships;
#nothing is copied into the player's BIOS folder. A path the player chose
#that still exists is kept.
NBA_CFG="/storage/.config/nanoboyadvance/config.toml"
PLAYER_BIOS="/storage/roms/bios/gba_bios.bin"
OPEN_BIOS="/usr/config/nanoboyadvance/bios/gba_bios.bin"
if [ -f "${NBA_CFG}" ]; then
  CUR_BIOS=$(sed -n 's/^bios_path = "\(.*\)"$/\1/p' "${NBA_CFG}")
  if [ ! -f "${CUR_BIOS}" ] || [ "${CUR_BIOS}" = "${OPEN_BIOS}" ]; then
    NEW_BIOS="${CUR_BIOS}"
    if [ -f "${PLAYER_BIOS}" ]; then
      NEW_BIOS="${PLAYER_BIOS}"
    elif [ -f "${OPEN_BIOS}" ]; then
      NEW_BIOS="${OPEN_BIOS}"
    fi
    [ "${NEW_BIOS}" = "${CUR_BIOS}" ] || sed -i "s#^bios_path = .*#bios_path = \"${NEW_BIOS}\"#" "${NBA_CFG}"
  fi
fi

#Run nanoboyadvance emulator
${EMUPERF} /usr/bin/NanoBoyAdvance "${1}"
