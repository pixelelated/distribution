#!/bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)

. /etc/profile
. /usr/bin/dolphin_common.sh

# Detect version of Dolphin
DOLPHIN_CORE=$(echo "${3}"| sed "s#^/.*/##")
if [ "${DOLPHIN_CORE}" = 'dolphin-qt-wii' ]; then
  DOLPHIN_CORE="dolphin-emu"
else
  DOLPHIN_CORE="dolphin-emu-nogui"
fi

dolphin_shared_5 "$@"
GC_CONTROLLER_INI="GCPadNew.ini"

# Refuse ambiguous retained save paths before any configuration preparation.
if ! /usr/bin/python3 -I -S -B /usr/bin/dolphin-save-paths check wii; then
  exit 250
fi

dolphin_shared_6 "$@"

# Check if Wii controller dir exists in .config/dolphin-emu/WiiControllerProfiles
if [ ! -d "${CONF_DIR}/WiiControllerProfiles" ]; then
        cp -r "/usr/config/dolphin-emu/WiiControllerProfiles" "${CONF_DIR}/"
fi

# Check if Wii custom controller profile exists in .config/dolphin-emu
if [ ! -f "${CONF_DIR}/WiiControllerProfiles/custom.ini" ]; then
        cp -r "${CONF_DIR}/WiiControllerProfiles/vremote.ini" "${CONF_DIR}/WiiControllerProfiles/custom.ini"
fi

# Gamecube controller profile needed for hotkeys to work on SA
if [ "${DOLPHIN_CORE}" = 'dolphin-emu-nogui' ]; then
  cp -r "/storage/.config/dolphin-emu/GamecubeControllerProfiles/GCPadNew.ini.south.stacked" "/storage/.config/dolphin-emu/GCPadNew.ini"
else
  rm -r "/storage/.config/dolphin-emu/GCPadNew.ini"
fi

# Prepare only known save links; retained real data requires an explicit choice.
if ! /usr/bin/python3 -I -S -B /usr/bin/dolphin-save-paths prepare wii; then
  exit 250
fi

# Emulation Station Features
GAME=$(echo "${1}"| sed "s#^/.*/##")
PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
AA=$(get_setting anti_aliasing "${PLATFORM}" "${GAME}")
ASPECT=$(get_setting aspect_ratio "${PLATFORM}" "${GAME}")
AUDIOBE=$(get_setting audio_backend "${PLATFORM}" "${GAME}")
CLOCK=$(get_setting clock_speed "${PLATFORM}" "${GAME}")
ENBCHEATS=$(get_setting enable_cheats "${PLATFORM}" "${GAME}")
GRENDERER=$(get_setting graphics_backend "${PLATFORM}" "${GAME}")
IRES=$(get_setting internal_resolution "${PLATFORM}" "${GAME}")
FPS=$(get_setting show_fps "${PLATFORM}" "${GAME}")
CON=$(get_setting wii_controller_profile "${PLATFORM}" "${GAME}")
HKEY=$(get_setting hotkey_enable_button "${PLATFORM}" "${GAME}")
SHADERM=$(get_setting shader_mode "${PLATFORM}" "${GAME}")
SHADERP=$(get_setting shader_precompile "${PLATFORM}" "${GAME}")
VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
dolphin_shared_1 "$@"

dolphin_shared_7 "$@"

dolphin_shared_2 "$@"

  # Wii Controller Profile
  if [ "$CON" = "classic" ]; then
    cp -r ${CONF_DIR}/WiiControllerProfiles/classic.ini ${CONF_DIR}/WiimoteNew.ini
  elif [ "$CON" = "vremote" ]; then
    cp -r ${CONF_DIR}/WiiControllerProfiles/vremote.ini ${CONF_DIR}/WiimoteNew.ini
  elif [ "$CON" = "nunchuck" ]; then
    cp -r ${CONF_DIR}/WiiControllerProfiles/nunchuck.ini ${CONF_DIR}/WiimoteNew.ini
  elif [ "$CON" = "custom" ]; then
    cp -r ${CONF_DIR}/WiiControllerProfiles/custom.ini ${CONF_DIR}/WiimoteNew.ini
  else
    cp -r ${CONF_DIR}/WiiControllerProfiles/hremote.ini ${CONF_DIR}/WiimoteNew.ini
  fi

  # Wii Controller Rumble
  if [ "$RUMBLE" = "false" ]; then
    sed -i '/^Rumble/d' ${CONF_DIR}/WiimoteNew.ini
  fi

  # Wii Controller Hotkey Enable
  if [ "$HKEY" = "mode" ]; then
    sed -i '/^Buttons\/Hotkey =/c\Buttons\/Hotkey = Guide' ${CONF_DIR}/GCPadNew.ini
  else
    sed -i '/^Buttons\/Hotkey =/c\Buttons\/Hotkey = Back' ${CONF_DIR}/GCPadNew.ini
  fi
dolphin_shared_3 "$@"

# Skip bios always, it's untested for Wii
sed -i '/SkipIPL/c\SkipIPL = True' ${CONF_DIR}/${DOLPHIN_INI}

  # GC Controller Hotkey Enable
  if [ "$HKEY" = "mode" ]; then
    sed -i '/^Buttons\/Hotkey =/c\Buttons\/Hotkey = Guide' ${CONF_DIR}/${GC_CONTROLLER_INI}
  else
    sed -i '/^Buttons\/Hotkey =/c\Buttons\/Hotkey = Back' ${CONF_DIR}/${GC_CONTROLLER_INI}
  fi

dolphin_shared_8 "$@"

dolphin_face_swap_configs "${CONF_DIR}/WiimoteNew.ini" "${CONF_DIR}/WiimoteNew.ini"

dolphin_shared_9 "$@"
  echo "CPU CORES set to ${EMUPERF}"
  echo "AA set to: ${AA}"
  echo "ASPECT set to: ${ASPECT}"
  echo "AUDIOBE set to: ${AUDIOBE}"
  echo "CLOCK set to: ${CLOCK}"
  echo "DOLPHIN_BACKEND set to: ${DOLPHIN_BACKEND}"
  echo "ENBCHEATS set to: ${ENBCHEATS}"
  echo "GRENDERER set to: ${GRENDERER}"
  echo "IRES set to: ${IRES}"
  echo "FPS set to: ${FPS}"
  echo "CON set to: ${CON}"
  echo "HKEY set to: ${HKEY}"
  echo "SHADERM set to: ${SHADERM}"
  echo "SHADERP set to: ${SHADERP}"
  echo "VSYNC set to: ${VSYNC}"
dolphin_shared_4 "$@"
