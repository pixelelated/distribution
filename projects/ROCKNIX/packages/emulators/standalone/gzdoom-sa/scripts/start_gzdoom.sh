#!/usr/bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2021-present 351ELEC (https://github.com/351ELEC)
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)

. /etc/profile
set_kill set "-9 gzdoom"

RUN_DIR="/storage/roms/doom"
CONFIG="/storage/.config/gzdoom/gzdoom.ini"
SAVE_DIR="/storage/roms/gzdoom"

#Emulation Station Features
GAME=$(echo "${1}"| sed "s#^/.*/##")
PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")


if [ ! -d "/storage/.config/gzdoom/" ]; then
  cp -rf /usr/config/gzdoom /storage/.config/
fi

if [ ! -f "/storage/.config/gzdoom/gzdoom.ini" ]; then
  cp -rf /usr/config/gzdoom/gzdoom.ini /storage/.config/gzdoom/
fi

# Check for newer pk3 files
SHASUMSRC=$(sha256sum "/usr/config/gzdoom/gzdoom.pk3" | awk '{print $1}')
SHASUMDST=$(sha256sum "/storage/.config/gzdoom/gzdoom.pk3" | awk '{print $1}')

# Quoted: a missing /storage copy made this a test error, skipping the copy (F-42)
if [ "$SHASUMSRC" != "$SHASUMDST" ]; then
  cp /usr/config/gzdoom/*.pk3 /storage/.config/gzdoom/
fi

# set resolution
sed -i '/vid_defheight=/c\vid_defheight='$(fbheight) /storage/.config/gzdoom/gzdoom.ini
sed -i '/vid_defwidth=/c\vid_defwidth='$(fbwidth) /storage/.config/gzdoom/gzdoom.ini

if [ ! -d "/storage/roms/doom/iwads" ]; then
  mkdir /storage/roms/doom/iwads
fi

if [ ! -d "/storage/roms/doom/mods" ]; then
  mkdir /storage/roms/doom/mods
fi

mkdir -p ${SAVE_DIR}

params=(-config "${CONFIG}" -savedir "${SAVE_DIR}")
params+=(+gl_es 1 +vid_preferbackend 3 +cl_capfps 0 +vid_fps 0)

if [ "$VSYNC" = "false" ]; then
  params+=(+vid_vsync 0)
else
  params+=(+vid_vsync 1)
fi

# A .doom value is one path, a quoted path, or several paths separated by
# spaces (as xargs split it before); each becomes its own argument.
doom_value() {
  local flag="$1" value="$2" words
  case "${value}" in
    \"*\"|\'*\') params+=("${flag}" "${value:1:${#value}-2}") ;;
    *)
      if [ -e "${value}" ]; then
        params+=("${flag}" "${value}")
      else
        read -r -a words <<<"${value}"
        params+=("${flag}" "${words[@]}")
      fi
    ;;
  esac
}

# EXT can be wad, WAD, iwad, IWAD, pwad, PWAD or doom
EXT=${1##*.}

# If its not a simple wad (extension .doom) read the file and parse the data
if [ "${EXT}" == "doom" ]; then
  dos2unix "${1}"
  local_savedir=""
  while IFS== read -r key value; do
    if [ "$key" == "IWAD" ]; then
      doom_value -iwad "$value"
    fi
    if [ "$key" == "MOD" ]; then
      doom_value -file "$value"
    fi
    if [ "$key" == "SAVEDIR" ]; then
      local_savedir="$value"
    fi
  done <"${1}"
  if [ -n "$local_savedir" ]; then
    mkdir -p "$local_savedir"
    params[3]="${local_savedir}"
  fi
else
  params+=(-iwad "${1}")
fi

#Set the cores to use
CORES=$(get_setting "cores" "${PLATFORM}" "${GAME}")
if [ "${CORES}" = "little" ]; then
  EMUPERF="${SLOW_CORES}"
elif [ "${CORES}" = "big" ]; then
  EMUPERF="${FAST_CORES}"
else
  ### All..
  unset EMUPERF
fi

cd "${RUN_DIR}"
${EMUPERF} /usr/bin/gzdoom "${params[@]}" >/var/log/gzdoom.log 2>&1
