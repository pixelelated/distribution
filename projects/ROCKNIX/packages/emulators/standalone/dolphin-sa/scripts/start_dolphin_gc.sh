#!/bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)

. /etc/profile
. /usr/bin/dolphin_common.sh

# Detect version of Dolphin
DOLPHIN_CORE=$(echo "${3}"| sed "s#^/.*/##")
if [ "${DOLPHIN_CORE}" = 'dolphin-qt-gc' ]; then
  DOLPHIN_CORE="dolphin-emu"
else
  DOLPHIN_CORE="dolphin-emu-nogui"
fi

dolphin_shared_5 "$@"
CONTROLLER_INI="GCPadNew.ini"

# Refuse ambiguous retained save paths before any configuration preparation.
if ! /usr/bin/python3 -I -S -B /usr/bin/dolphin-save-paths check gamecube; then
  exit 250
fi

dolphin_shared_6 "$@"

# Check if each stock profile exists in .config/dolphin-emu/GamecubeControllerProfiles
for PROFILE in east.stacked east.inline south.stacked south.inline; do
        if [ ! -f "${CONF_DIR}/GamecubeControllerProfiles/GCPadNew.ini.${PROFILE}" ]; then
                cp -r "/usr/config/dolphin-emu/GamecubeControllerProfiles/GCPadNew.ini.${PROFILE}" "${CONF_DIR}/GamecubeControllerProfiles/GCPadNew.ini.${PROFILE}"
        fi
done

# Check if GC custom controller profile exists in .config/dolphin-emu/GamecubeControllerProfiles
if [ ! -f "${CONF_DIR}/GamecubeControllerProfiles/GCPadNew.ini.custom" ]; then
        cp -r "/usr/config/dolphin-emu/GamecubeControllerProfiles/GCPadNew.ini.south.stacked" "${CONF_DIR}/GamecubeControllerProfiles/GCPadNew.ini.custom"
fi

# Prepare only known save links; retained real data requires an explicit choice.
if ! /usr/bin/python3 -I -S -B /usr/bin/dolphin-save-paths prepare gamecube; then
  exit 250
fi

# Make sure all Triforce Gecko codes are copied to GameSettings
for f in /usr/config/dolphin-emu/triforce_gecko_codes/*; do
  [ -e "/storage/.config/dolphin-emu/GameSettings/$(basename "$f")" ] || cp -fH "$f" "/storage/.config/dolphin-emu/GameSettings/"
done
rm -rf "/storage/.config/dolphin-emu/triforce_gecko_codes"

# Emulation Station Features
GAME=$(echo "${1}"| sed "s#^/.*/##")
PLATFORM=$(echo "${2}"| sed "s#^/.*/##")
AA=$(get_setting anti_aliasing "${PLATFORM}" "${GAME}")
ASPECT=$(get_setting aspect_ratio "${PLATFORM}" "${GAME}")
AUDIOBE=$(get_setting audio_backend "${PLATFORM}" "${GAME}")
ASWAPDISCS=$(get_setting auto_swap_discs "${PLATFORM}" "${GAME}")
CLOCK=$(get_setting clock_speed "${PLATFORM}" "${GAME}")
ENBCHEATS=$(get_setting enable_cheats "${PLATFORM}" "${GAME}")
GRENDERER=$(get_setting graphics_backend "${PLATFORM}" "${GAME}")
IRES=$(get_setting internal_resolution "${PLATFORM}" "${GAME}")
FPS=$(get_setting show_fps "${PLATFORM}" "${GAME}")
CON=$(get_setting gamecube_controller_profile "${PLATFORM}" "${GAME}")
SWAPSHOULDER=$(get_setting swap_shoulders "${PLATFORM}" "${GAME}")
HKEY=$(get_setting hotkey_enable_button "${PLATFORM}" "${GAME}")
SAVETYPE=$(get_setting save_type "${PLATFORM}" "${GAME}")
SAVEREG=$(get_setting save_gci_region "${PLATFORM}" "${GAME}")
SHADERM=$(get_setting shader_mode "${PLATFORM}" "${GAME}")
SHADERP=$(get_setting shader_precompile "${PLATFORM}" "${GAME}")
VSYNC=$(get_setting vsync "${PLATFORM}" "${GAME}")
SKIPBIOS=$(get_setting use_bios "${PLATFORM}" "${GAME}")
dolphin_shared_1 "$@"

  # Auto Swap Discs
  if [ "$ASWAPDISCS" = "0" ]; then
    sed -i '/AutoDiscChange/c\AutoDiscChange = False' ${CONF_DIR}/${DOLPHIN_INI}
  else
    sed -i '/AutoDiscChange/c\AutoDiscChange = True' ${CONF_DIR}/${DOLPHIN_INI}
  fi

dolphin_shared_7 "$@"

  # Save Type
  if [ "$SAVETYPE" = "8" ]; then
    sed -i '/SlotA/c\SlotA = 8' ${CONF_DIR}/${DOLPHIN_INI}
  else
    sed -i '/SlotA/c\SlotA = 1' ${CONF_DIR}/${DOLPHIN_INI}
  fi

  # Save Reg
  if [ "$SAVEREG" = "eur" ]; then
    sed -i '/GCIFolderAPath/c\GCIFolderAPath = \/storage\/roms\/bios\/GC\/EUR' ${CONF_DIR}/${DOLPHIN_INI}
  elif [ "$SAVEREG" = "jap" ]; then
    sed -i '/GCIFolderAPath/c\GCIFolderAPath = \/storage\/roms\/bios\/GC\/JAP' ${CONF_DIR}/${DOLPHIN_INI}
  else
    sed -i '/GCIFolderAPath/c\GCIFolderAPath = \/storage\/roms\/bios\/GC\/USA' ${CONF_DIR}/${DOLPHIN_INI}
  fi

dolphin_shared_2 "$@"

  # Skip Bios
  if [ "$SKIPBIOS" = "false" ]; then
    sed -i '/SkipIPL/c\SkipIPL = False' ${CONF_DIR}/${DOLPHIN_INI}
  else
    sed -i '/SkipIPL/c\SkipIPL = True' ${CONF_DIR}/${DOLPHIN_INI}
  fi

dolphin_shared_3 "$@"

  # GC Controller Profile
  # Devices with inline shoulders want L/R on the bumpers and Z on the analog
  # trigger, which is the reverse of the stacked layout actual hardware uses.
  if [ "$SWAPSHOULDER" = "true" ]; then
    SHOULDERS="inline"
  else
    SHOULDERS="stacked"
  fi

  if [ "$CON" = "east" ]; then
    cp -r ${CONF_DIR}/GamecubeControllerProfiles/GCPadNew.ini.east.${SHOULDERS} ${CONF_DIR}/${CONTROLLER_INI}
  elif [ "$CON" = "custom" ]; then
    cp -r ${CONF_DIR}/GamecubeControllerProfiles/GCPadNew.ini.custom ${CONF_DIR}/${CONTROLLER_INI}
  else
    cp -r ${CONF_DIR}/GamecubeControllerProfiles/GCPadNew.ini.south.${SHOULDERS} ${CONF_DIR}/${CONTROLLER_INI}
  fi

  # GC Controller Rumble
  if [ "$RUMBLE" = "false" ]; then
    sed -i '/^Rumble/d' ${CONF_DIR}/${CONTROLLER_INI}
  fi

  # GC Controller Hotkey Enable
  if [ "$HKEY" = "mode" ]; then
    sed -i '/^Buttons\/Hotkey =/c\Buttons\/Hotkey = Guide' ${CONF_DIR}/${CONTROLLER_INI}
  else
    sed -i '/^Buttons\/Hotkey =/c\Buttons\/Hotkey = Back' ${CONF_DIR}/${CONTROLLER_INI}
  fi

dolphin_shared_8 "$@"

dolphin_face_swap_configs "${CONF_DIR}/${CONTROLLER_INI}" "${CONF_DIR}/${CONTROLLER_INI}"

dolphin_shared_9 "$@"
  echo "CPU CORES set to: ${EMUPERF}"
  echo "AA set to: ${AA}"
  echo "ASPECT set to: ${ASPECT}"
  echo "AUDIOBE set to: ${AUDIOBE}"
  echo "ASWAPDISCS set to: ${ASWAPDISCS}"
  echo "CLOCK set to: ${CLOCK}"
  echo "DOLPHIN_BACKEND set to: ${DOLPHIN_BACKEND}"
  echo "ENBCHEATS set to: ${ENBCHEATS}"
  echo "GRENDERER set to: ${GRENDERER}"
  echo "IRES set to: ${IRES}"
  echo "FPS set to: ${FPS}"
  echo "CON set to: ${CON}"
  echo "SWAPSHOULDER set to: ${SWAPSHOULDER}"
  echo "HKEY set to: ${HKEY}"
  echo "SAVETYPE set to: ${SAVETYPE}"
  echo "SAVEREG set to: ${SAVEREG}"
  echo "SHADERM set to: ${SHADERM}"
  echo "SHADERP set to: ${SHADERP}"
  echo "VSYNC set to: ${VSYNC}"
  echo "SKIPBIOS set to: ${SKIPBIOS}"
dolphin_shared_4 "$@"
