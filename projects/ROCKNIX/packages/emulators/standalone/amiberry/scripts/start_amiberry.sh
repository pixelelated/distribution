#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 0riginally created by Escalade (https://github.com/escalade)
# Copyright (C) 2018-present 5schatten (https://github.com/5schatten)
# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)

. /etc/profile

set_kill set "-9 amiberry"

# Set some common variables
AMIBERRY_DIR="/storage/.config/amiberry"
AMIBERRY_CONFIG_DIR="${AMIBERRY_DIR}/conf"
AMIBERRY_TMP_DIR="/tmp/emulation/amiberry"
AMIBERRY_TMP_CONFIG="${AMIBERRY_TMP_DIR}/.amiberry_conf.uae"
AMIBERRY_LOG="/var/log/amiberry.log"
BIOS_PATH="/storage/roms/bios"
MAX_DRIVES=4
i=0

echo "Amiberry Log" > "${AMIBERRY_LOG}"

if [ ! -d "${AMIBERRY_TMP_DIR}" ]
then
  mkdir -p "${AMIBERRY_TMP_DIR}"
fi

if [ ! -d "${AMIBERRY_DIR}" ]
then
  cp -rf /usr/config/amiberry ${AMIBERRY_DIR}
fi

### Seed the configs the player does not have; a config the player
### changed is kept (it was overwritten every launch, #871).
mkdir -p "${AMIBERRY_DIR}/conf"
for CONF in /usr/config/amiberry/conf/*; do
  [ -e "${AMIBERRY_DIR}/conf/${CONF##*/}" ] || cp "${CONF}" "${AMIBERRY_DIR}/conf/"
done

find_gamepad() {
  # Check for js0 first, else fall back to joypad
  if grep -q "js0" /proc/bus/input/devices; then
    GAMEPAD=$(grep -b4 js0 /proc/bus/input/devices | awk 'BEGIN {FS="\""}; /Name/ {printf $2}')
  else
    GAMEPAD=$(grep -b4 joypad /proc/bus/input/devices | awk 'BEGIN {FS="\""}; /Name/ {printf $2}')
  fi
  sed -i "s|joyport1_friendlyname=.*|joyport1_friendlyname=${GAMEPAD}|" "${AMIBERRY_TMP_CONFIG}"
  echo "Gamepad used ${GAMEPAD}" >> "${AMIBERRY_LOG}"
}

# Which file should amiberry load?
echo "Trying to boot this game:" "$1" >> ${AMIBERRY_LOG}

# Change working directory cause amiberry loads assets from there
cd ${AMIBERRY_DIR}

# Create a clean working directory
if [ -d "${AMIBERRY_TMP_DIR}" ]; then
  echo "Clean up old working directory." >> ${AMIBERRY_LOG}
  rm -rf "${AMIBERRY_TMP_DIR}"
fi
mkdir -p "${AMIBERRY_TMP_DIR}"

# Check if the file is an Amiga 1200/CD32 game and set configuration options for an Amiga 1200
AMIBERRY_SET_CONF() {
  if echo "$1" | grep -q -E 'AGA|CD32' || ls "${AMIBERRY_TMP_DIR}" | grep -q -E 'AGA|CD32'; then
    echo "Loading Amiga 1200/CD32 config." >> ${AMIBERRY_LOG}
    cp ${AMIBERRY_CONFIG_DIR}/AmigaA1200-default.uae "${AMIBERRY_TMP_CONFIG}"
  else
    echo "Loading Amiga 500 config." >> ${AMIBERRY_LOG}
    cp ${AMIBERRY_CONFIG_DIR}/AmigaA500-default.uae "${AMIBERRY_TMP_CONFIG}"
  fi
  sed -i "s#@BIOS_PATH@#${BIOS_PATH}#g" ${AMIBERRY_TMP_CONFIG}
  # The key stays and takes the panel's size (the whole line was replaced
  # by the bare number, deleting the key, #871).
  sed -i "s#^gfx_width=.*\$#gfx_width=$(fbwidth)#" "${AMIBERRY_TMP_CONFIG}"
  sed -i "s#^gfx_height=.*\$#gfx_height=$(fbheight)#" "${AMIBERRY_TMP_CONFIG}"
  find_gamepad 
}

# Check if we are loading a .zip file
case "$1" in *.[zZ][iI][pP]) IS_ZIP=1 ;; *) IS_ZIP=0 ;; esac
if [ "${IS_ZIP}" = 1 ]; then
  
  # Unpack the zip file
  unzip -q -o "$1" -d "${AMIBERRY_TMP_DIR}"
  
  if [ -f "${AMIBERRY_TMP_DIR}"/*.*nfo ] && [ -f "${AMIBERRY_TMP_DIR}"/*/*.*lave ]; then

    # WHDLoad file detected
    echo "Loading a WHDLoad (.zip) file..." >> ${AMIBERRY_LOG}

    # Set default config
    AMIBERRY_SET_CONF "$1"

    # Add amiberry.uae conf & start amiberry with WHDLoad
    amiberry -f "${AMIBERRY_TMP_CONFIG}" --autoload "$1" >> ${AMIBERRY_LOG} 2>&1

  else
    # .zip file detected
    echo "Loading a .zip file..." >> ${AMIBERRY_LOG}

    # Set default config
    AMIBERRY_SET_CONF "$1"
  
    # Assign the archive's disk images, in name order, to floppy0-3: each
    # line written as data (echo -e read backslashes in a name and split it
    # on spaces, and every file in the folder became a floppy, #871)
    printf ';\n; *** temporary added Floppy Drives\n;\n' >> "${AMIBERRY_TMP_CONFIG}"
    echo "Assigned floppy drives:" >> "${AMIBERRY_LOG}"
    for FILE in "${AMIBERRY_TMP_DIR}"/*
    do
      case "${FILE,,}" in *.adf|*.adz|*.dms|*.ipf) ;; *) continue ;; esac
      [ -f "${FILE}" ] || continue
      printf 'floppy%d=%s\n' "$i" "${FILE}" | tee -a "${AMIBERRY_LOG}" >> "${AMIBERRY_TMP_CONFIG}"
      i=$(($i+1))
      # This emulator supports 4 floppies max
      if [ $i -eq ${MAX_DRIVES} ]; then
        break;
      fi
    done
    amiberry -f "${AMIBERRY_TMP_CONFIG}" >> ${AMIBERRY_LOG} 2>&1
  fi

# Check for WHDload files (.lha)
elif case "$1" in *.[lL][hH][aA]) true ;; *) false ;; esac; then
    
  #.lha file detected
  echo "Loading a WHDLoad (.lha) file..." >> ${AMIBERRY_LOG}

  # Set default config
  AMIBERRY_SET_CONF "$1"

  # Add amiberry.uae conf & start amiberry with WHDLoad
  amiberry -f "${AMIBERRY_TMP_CONFIG}" --autoload "$1" >> ${AMIBERRY_LOG} 2>&1

# Check for .uae config file
elif case "$1" in *.[uU][aA][eE]) true ;; *) false ;; esac; then

  # .uae file detected
  echo "Loading an .uae file..." >> ${AMIBERRY_LOG}

  # Load .uae config file
  amiberry -f "$1" >> ${AMIBERRY_LOG} 2>&1

# All other files (.adf .adz .ipf)
else

  #.adf or .adz or .ipf file detected
  echo "Loading a single .adf or .adz or .ipf file..." >> ${AMIBERRY_LOG}

  # Set default config
  AMIBERRY_SET_CONF "$1"

  # Add game file as floppy0 to amiberry.uae & start amiberry
  printf ';\n; *** temporary added Floppy Drives\n;\n' >> "${AMIBERRY_TMP_CONFIG}"
  printf 'floppy0=%s\n' "$1" >> "${AMIBERRY_TMP_CONFIG}"
  printf 'Assigned floppy drive:\nfloppy0=%s\n' "$1" >> "${AMIBERRY_LOG}"
  amiberry -f "${AMIBERRY_TMP_CONFIG}" >> ${AMIBERRY_LOG} 2>&1
fi

# Remove temporary dir
rm -rf "${AMIBERRY_TMP_DIR}"
