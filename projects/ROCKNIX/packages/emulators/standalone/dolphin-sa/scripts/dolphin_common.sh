#!/bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)

# The steps start_dolphin_gc.sh and start_dolphin_wii.sh share, sourced by both
# (#872 PL-023). Each function is one shared stretch, moved verbatim and in the
# order the scripts run it; each script calls them with "$@", so a stretch
# that reads the launch's arguments still reads them. Only the steps that
# differ between GameCube and Wii stay in the two scripts.

dolphin_shared_1() {
EFBACCESS=$(get_setting skip_efb_cpu_access "${PLATFORM}" "${GAME}")
EFBTEXTURE=$(get_setting store_efb_to_texture_only "${PLATFORM}" "${GAME}")
XFBTEXTURE=$(get_setting store_xfb_to_texture_only "${PLATFORM}" "${GAME}")
TEXTURE_CACHE_ACCURACY=$(get_setting texture_cache_accuracy "${PLATFORM}" "${GAME}")
SYNC_GPU_THREAD=$(get_setting sync_gpu_thread "${PLATFORM}" "${GAME}")
RUMBLE=$(get_setting rumble "${PLATFORM}" "${GAME}")
WHACK=$(get_setting widescreen_hack "${PLATFORM}" "${GAME}")
WPC=$(get_setting write_protect_configs "${PLATFORM}" "${GAME}")

# Grab clean config files during boot, unless disabled in emulationstation
if [ "$WPC" != "false" ]; then
  cp -r /usr/config/dolphin-emu/GFX.ini ${CONF_DIR}/${GFX_INI}
  cp -r /usr/config/dolphin-emu/Dolphin.ini ${CONF_DIR}/${DOLPHIN_INI}
fi

# Set the cores to use
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

### Emulation Station features:
  # Anti-Aliasing
  if [ "$AA" = "2m" ]; then
    sed -i '/MSAA/c\MSAA = 2' ${CONF_DIR}/${GFX_INI}
    sed -i '/SSAA/c\SSAA = False' ${CONF_DIR}/${GFX_INI}
  elif [ "$AA" = "2s" ]; then
    sed -i '/MSAA/c\MSAA = 2' ${CONF_DIR}/${GFX_INI}
    sed -i '/SSAA/c\SSAA = True' ${CONF_DIR}/${GFX_INI}
  elif [ "$AA" = "4m" ]; then
    sed -i '/MSAA/c\MSAA = 4' ${CONF_DIR}/${GFX_INI}
    sed -i '/SSAA/c\SSAA = False' ${CONF_DIR}/${GFX_INI}
  elif [ "$AA" = "4s" ]; then
    sed -i '/MSAA/c\MSAA = 4' ${CONF_DIR}/${GFX_INI}
    sed -i '/SSAA/c\SSAA = True' ${CONF_DIR}/${GFX_INI}
  elif [ "$AA" = "8m" ]; then
    sed -i '/MSAA/c\MSAA = 8' ${CONF_DIR}/${GFX_INI}
    sed -i '/SSAA/c\SSAA = False' ${CONF_DIR}/${GFX_INI}
  elif [ "$AA" = "8s" ]; then
    sed -i '/MSAA/c\MSAA = 8' ${CONF_DIR}/${GFX_INI}
    sed -i '/SSAA/c\SSAA = True' ${CONF_DIR}/${GFX_INI}
  else
    sed -i '/MSAA/c\MSAA = 0' ${CONF_DIR}/${GFX_INI}
    sed -i '/SSAA/c\SSAA = False' ${CONF_DIR}/${GFX_INI}
  fi

  # Aspect Ratio
  if [ "$ASPECT" = "1" ]; then
    sed -i '/AspectRatio/c\AspectRatio = 1' ${CONF_DIR}/${GFX_INI}
  elif [ "$ASPECT" = "2" ]; then
    sed -i '/AspectRatio/c\AspectRatio = 2' ${CONF_DIR}/${GFX_INI}
  elif [ "$ASPECT" = "3" ]; then
    sed -i '/AspectRatio/c\AspectRatio = 3' ${CONF_DIR}/${GFX_INI}
  else
    sed -i '/AspectRatio/c\AspectRatio = 0' ${CONF_DIR}/${GFX_INI}
  fi

  # Audio Backend
  if [ "$AUDIOBE" = "lle" ]; then
    AUDIO_BACKEND="LLE"
  else
    AUDIO_BACKEND="HLE"
  fi
}

dolphin_shared_2() {
  # Shader Mode
  if [ "$SHADERM" = "0" ]; then
    sed -i '/ShaderCompilationMode =/c\ShaderCompilationMode = 0' ${CONF_DIR}/${GFX_INI}
  elif [ "$SHADERM" = "1" ]; then
    sed -i '/ShaderCompilationMode =/c\ShaderCompilationMode = 1' ${CONF_DIR}/${GFX_INI}
  elif [ "$SHADERM" = "2" ]; then
    sed -i '/ShaderCompilationMode =/c\ShaderCompilationMode = 2' ${CONF_DIR}/${GFX_INI}
  elif [ "$SHADERM" = "3" ]; then
    sed -i '/ShaderCompilationMode =/c\ShaderCompilationMode = 3' ${CONF_DIR}/${GFX_INI}
  fi

  #Shader Precompile
  if [ "$SHADERP" = "false" ]; then
    sed -i '/WaitForShadersBeforeStarting =/c\WaitForShadersBeforeStarting = False' ${CONF_DIR}/${GFX_INI}
  elif [ "$SHADERP" = "true" ]; then
    sed -i '/WaitForShadersBeforeStarting =/c\WaitForShadersBeforeStarting = True' ${CONF_DIR}/${GFX_INI}
  fi

  # Show FPS
  if [ "$FPS" = "true" ]; then
    sed -i '/ShowFPS/c\ShowFPS = True' ${CONF_DIR}/${GFX_INI}
  else
    sed -i '/ShowFPS/c\ShowFPS = False' ${CONF_DIR}/${GFX_INI}
  fi
}

dolphin_shared_3() {
  # Skip EFB CPU Access
  if [ "$EFBACCESS" = "false" ]; then
    sed -i '/EFBAccessEnable =/c\EFBAccessEnable = False' ${CONF_DIR}/${GFX_INI}
  else
    sed -i '/EFBAccessEnable =/c\EFBAccessEnable = True' ${CONF_DIR}/${GFX_INI}
  fi

  # Store EFB to texture only
  if [ "$EFBTEXTURE" = "false" ]; then
    sed -i '/EFBToTextureEnable =/c\EFBToTextureEnable = False' ${CONF_DIR}/${GFX_INI}
  else
    sed -i '/EFBToTextureEnable =/c\EFBToTextureEnable = True' ${CONF_DIR}/${GFX_INI}
  fi

  # Store XFB to texture only
  if [ "$XFBTEXTURE" = "false" ]; then
    sed -i '/XFBToTextureEnable =/c\XFBToTextureEnable = False' ${CONF_DIR}/${GFX_INI}
  else
    sed -i '/XFBToTextureEnable =/c\XFBToTextureEnable = True' ${CONF_DIR}/${GFX_INI}
  fi

  # Texture cache accuracy
  if [ "$TEXTURE_CACHE_ACCURACY" = "0" ]; then
    sed -i '/SafeTextureCacheColorSamples =/c\SafeTextureCacheColorSamples = 0' ${CONF_DIR}/${GFX_INI}
  elif [ "$TEXTURE_CACHE_ACCURACY" = "512" ]; then
    sed -i '/SafeTextureCacheColorSamples =/c\SafeTextureCacheColorSamples = 512' ${CONF_DIR}/${GFX_INI}
  else
    # Default to 128 = fast
    sed -i '/SafeTextureCacheColorSamples =/c\SafeTextureCacheColorSamples = 128' ${CONF_DIR}/${GFX_INI}
  fi

  # Widescreen Hack
  if [ "$WHACK" = "true" ]; then
    sed -i '/wideScreenHack =/c\wideScreenHack = True' ${CONF_DIR}/${GFX_INI}
  else
    sed -i '/wideScreenHack =/c\wideScreenHack = False' ${CONF_DIR}/${GFX_INI}
  fi
}

dolphin_shared_4() {
  echo "EFBACCESS set to: ${EFBACCESS}"
  echo "EFBTEXTURE set to: ${EFBTEXTURE}"
  echo "XFBTEXTURE set to: ${XFBTEXTURE}"
  echo "TEXTURE_CACHE_ACCURACY set to: ${TEXTURE_CACHE_ACCURACY}"
  echo "SYNC_GPU_THREAD set to: ${SYNC_GPU_THREAD}"
  echo "RUMBLE set to: ${RUMBLE}"
  echo "WHACK set to: ${WHACK}"
  echo "WPC set to: ${WPC}"
  echo "Launching /usr/bin/${DOLPHIN_CORE} ${CMD} -e ${1}"

# Run Dolphin emulator
  ${EMUPERF} /usr/bin/${DOLPHIN_CORE} ${CMD} -e "${1}"
}

# The face swap, applied once (#869). It exchanges S with E and W with N, so a
# second pass undoes it, and a file kept between launches (Hotkeys.ini, and
# the controller file this script does not copy afresh) flipped every launch.
# A swapped file's state is recorded beside it, as a hash of the file without
# the lines every launch rewrites (Device, and Back/Guide); a file whose hash
# matches is swapped, any other is not. A kept file with no record yet (every
# device before this change) is read once against the shipped file: equal to
# its swap, it is swapped; equal to it, it is not; changed by the player, it
# is taken as it stands.
face_key() {
  sed -e '/^Device = /d' -e 's/`Guide`/`Back`/g' "$1" | sha1sum | cut -d' ' -f1
}
face_swap_file() {
  sed -i -e 's/`Button S`/`Button %`/g' \
         -e 's/`Button E`/`Button S`/g' \
         -e 's/`Button %`/`Button E`/g' \
         -e 's/`Button W`/`Button %`/g' \
         -e 's/`Button N`/`Button W`/g' \
         -e 's/`Button %`/`Button N`/g' "$1"
}
face_swap_once() { # cfg want(yes|no) [shipped copy, for a kept file]
  local cfg="$1" want="$2" shipped="${3:-}" rec="$1.faceswap" state="no" swapped key
  key=$(face_key "${cfg}")
  if [ -f "${rec}" ]; then
    [ "$(cat "${rec}")" = "${key}" ] && state="yes"
  elif [ -n "${shipped}" ] && [ -f "${shipped}" ]; then
    swapped=$(mktemp) && cp "${shipped}" "${swapped}" && face_swap_file "${swapped}"
    if [ "${key}" = "$(face_key "${swapped}")" ]; then
      state="yes"
    elif [ "${key}" != "$(face_key "${shipped}")" ]; then
      state="${want}"
    fi
    rm -f "${swapped}"
  fi
  [ "${state}" = "${want}" ] || face_swap_file "${cfg}"
  if [ "${want}" = "yes" ]; then face_key "${cfg}" > "${rec}"; else rm -f "${rec}"; fi
}

# The face swap's detection and its application to the three input files.
# $1: the file a custom profile owns (left as the player bound it); $2: the
# file the calling script copies afresh every launch (no shipped twin).
dolphin_face_swap_configs() {
  local FACE_CUSTOM_CFG="$1" FACE_FRESH_CFG="$2"
  # Some SDL strings are set for XBox-style, even though they're physically Nintendo-style
  # so we need to check for that and set a flag if so.
  FACE_SWAP="no"
  if [ -n "${MAPLINE}" ]; then
    A_BTN="$(echo "${MAPLINE}" | tr ',' '\n' | sed -n 's/^a:b\([0-9]\{1,\}\)$/\1/p')"
    B_BTN="$(echo "${MAPLINE}" | tr ',' '\n' | sed -n 's/^b:b\([0-9]\{1,\}\)$/\1/p')"
    if [ -n "${A_BTN}" ] && [ -n "${B_BTN}" ] && [ "${A_BTN}" -gt "${B_BTN}" ]; then
      FACE_SWAP="yes"
    fi
  fi

  for CFG in "${CONF_DIR}/Hotkeys.ini" "${CONF_DIR}/GCPadNew.ini" "${CONF_DIR}/WiimoteNew.ini"; do
    [ -f "${CFG}" ] || continue
    sed -i "/^Device = /c\\Device = SDL/0/${SDL_DEVICE}" "${CFG}"

    # A custom profile is whatever the user bound in Dolphin's own UI, which
    # already records what the pad really reports; only the shipped profiles are
    # written positionally and need correcting.
    if ! { [ "${CON}" = "custom" ] && [ "${CFG}" = "${FACE_CUSTOM_CFG}" ]; }; then
      SHIPPED="/usr/config/dolphin-emu/${CFG##*/}"
      [ "${CFG}" = "${FACE_FRESH_CFG}" ] && SHIPPED=""
      face_swap_once "${CFG}" "${FACE_SWAP}" "${SHIPPED}"
    fi
  done
}

dolphin_shared_5() {
set_kill set "-9 ${DOLPHIN_CORE}"

# control-gen supplies param_device and the SDL controller database
control-gen_init.sh
source /storage/.config/gptokeyb/control.ini
get_controls

# Conf files vars
CONF_DIR="/storage/.config/dolphin-emu"
DOLPHIN_INI="Dolphin.ini"
GFX_INI="GFX.ini"
}

dolphin_shared_6() {
# Dolphin writes its shader and pipeline caches here but will not create the
# directory itself, so an orderly shutdown had nothing to flush into.
mkdir -p "/storage/.cache/dolphin-emu"

# Check if dolphin-emu exists in .config
if [ ! -d "${CONF_DIR}" ]; then
        cp -r "/usr/config/dolphin-emu" "/storage/.config/"
fi

# Check if Hotkeys.ini exists
if [ "${DOLPHIN_CORE}" = 'dolphin-emu' ]; then
  if [ ! -f "${CONF_DIR}/Hotkeys.ini" ]; then
        cp -r "/usr/config/dolphin-emu/Hotkeys.ini" "${CONF_DIR}/"
  fi
fi

# Check if GC controller dir exists in .config/dolphin-emu/GamecubeControllerProfiles
if [ ! -d "${CONF_DIR}/GamecubeControllerProfiles" ]; then
        cp -r "/usr/config/dolphin-emu/GamecubeControllerProfiles" "${CONF_DIR}/"
fi
}

dolphin_shared_7() {
  # Clock Speed
  if [ "$CLOCK" = "050" ]; then
    sed -i '/^Overclock =/c\Overclock = 0.5' ${CONF_DIR}/${DOLPHIN_INI}
    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
  elif [ "$CLOCK" = "075" ]; then
    sed -i '/^Overclock =/c\Overclock = 0.75' ${CONF_DIR}/${DOLPHIN_INI}
    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
  elif [ "$CLOCK" = "100" ]; then
    sed -i '/^Overclock =/c\Overclock = 1.0' ${CONF_DIR}/${DOLPHIN_INI}
    sed -i '/^OverclockEnable =/c\OverclockEnable = False' ${CONF_DIR}/${DOLPHIN_INI}
  elif [ "$CLOCK" = "125" ]; then
    sed -i '/^Overclock =/c\Overclock = 1.25' ${CONF_DIR}/${DOLPHIN_INI}
    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
  elif [ "$CLOCK" = "150" ]; then
    sed -i '/^Overclock =/c\Overclock = 1.5' ${CONF_DIR}/${DOLPHIN_INI}
    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
  elif [ "$CLOCK" = "200" ]; then
    sed -i '/^Overclock =/c\Overclock = 2.0' ${CONF_DIR}/${DOLPHIN_INI}
    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
  elif [ "$CLOCK" = "300" ]; then
    sed -i '/^Overclock =/c\Overclock = 3.0' ${CONF_DIR}/${DOLPHIN_INI}
    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
  elif [ "$CLOCK" = "400" ]; then
    sed -i '/^Overclock =/c\Overclock = 4.0' ${CONF_DIR}/${DOLPHIN_INI}
    sed -i '/^OverclockEnable =/c\OverclockEnable = True' ${CONF_DIR}/${DOLPHIN_INI}
  else
    sed -i '/^OverclockEnable =/c\OverclockEnable = False' ${CONF_DIR}/${DOLPHIN_INI}
  fi

  # Enable Cheats
  if [ "$ENBCHEATS" = "1" ]; then
    sed -i '/EnableCheats/c\EnableCheats = True' ${CONF_DIR}/${DOLPHIN_INI}
  else
    sed -i '/EnableCheats/c\EnableCheats = False' ${CONF_DIR}/${DOLPHIN_INI}
  fi

  # Graphics Backend
  if [ "$GRENDERER" = "vulkan" ]; then
    sed -i '/GFXBackend/c\GFXBackend = Vulkan' ${CONF_DIR}/${DOLPHIN_INI}
  elif [ "$GRENDERER" = "opengl" ]; then
    sed -i '/GFXBackend/c\GFXBackend = OGL' ${CONF_DIR}/${DOLPHIN_INI}
  else
    sed -i '/GFXBackend/c\GFXBackend = @GRENDERER@' ${CONF_DIR}/${DOLPHIN_INI}
  fi

  # Sync GPU thread
  if [ "$SYNC_GPU_THREAD" = "true" ]; then
    sed -i '/SyncGPU =/c\SyncGPU = True' ${CONF_DIR}/${DOLPHIN_INI}
  else
    sed -i '/SyncGPU =/c\SyncGPU = False' ${CONF_DIR}/${DOLPHIN_INI}
  fi

  # Internal Resolution
  if [ "$IRES" = "1" ]; then
    sed -i '/InternalResolution/c\InternalResolution = 1' ${CONF_DIR}/${GFX_INI}
  elif [ "$IRES" = "3" ]; then
    sed -i '/InternalResolution/c\InternalResolution = 3' ${CONF_DIR}/${GFX_INI}
  elif [ "$IRES" = "4" ]; then
    sed -i '/InternalResolution/c\InternalResolution = 4' ${CONF_DIR}/${GFX_INI}
  elif [ "$IRES" = "6" ]; then
    sed -i '/InternalResolution/c\InternalResolution = 6' ${CONF_DIR}/${GFX_INI}
  else
    sed -i '/InternalResolution/c\InternalResolution = 2' ${CONF_DIR}/${GFX_INI}
  fi
}

dolphin_shared_8() {
  # Qt reads its combos from Hotkeys.ini instead of Buttons/Hotkey, so the same
  # setting has to be swapped into the modifier half of every binding there.
  if [ -f "${CONF_DIR}/Hotkeys.ini" ]; then
    if [ "$HKEY" = "mode" ]; then
      sed -i 's/`Back`/`Guide`/g' ${CONF_DIR}/Hotkeys.ini
    else
      sed -i 's/`Guide`/`Back`/g' ${CONF_DIR}/Hotkeys.ini
    fi
  fi

  # Vsync
  if [ "$VSYNC" = "1" ]; then
    sed -i '/VSync =/c\VSync = True' ${CONF_DIR}/${GFX_INI}
  else
    sed -i '/VSync =/c\VSync = False' ${CONF_DIR}/${GFX_INI}
  fi

# SDL names a gamepad after the mapping it resolves, which is not always the
# joystick name control-gen reports.
SDL_DB="${SDL_GAMECONTROLLERCONFIG_FILE:-/storage/.config/gptokeyb/gamecontrollerdb.txt}"
SDL_DEVICE="${param_device}"
MAPLINE=""
if [ -n "${DEVICE}" ] && [ -f "${SDL_DB}" ]; then
  GUID_KEY="$(echo "${DEVICE}" | cut -c1-4)0000$(echo "${DEVICE}" | cut -c9-)"
  MAPLINE="$(awk -F, -v d="${DEVICE}" -v k="${GUID_KEY}" '!/^#/ && NF>1 {
      if ($1 == d) { exact = $0; exit }
      if (loose == "" && substr($1,5,4) == "0000") {
        g = substr($1,1,4) "0000" substr($1,9)
        if (g == k) { loose = $0 }
      }
    }
    END { print (exact != "" ? exact : loose) }' "${SDL_DB}")"
  MAPPED="$(echo "${MAPLINE}" | cut -d, -f2)"
  [ -n "${MAPPED}" ] && SDL_DEVICE="${MAPPED}"
fi
}

dolphin_shared_9() {
# The shared Dolphin data link was checked and prepared before settings writes.

@EXPORTS@

# Retroachievements
  /usr/bin/cheevos_dolphin.sh
  CHEEVOS_STATUS=$?
  # Disabled/logged-out is a valid launch only after the inactive INI is written.
  case "${CHEEVOS_STATUS}" in
    0|1) ;;
    *) exit "${CHEEVOS_STATUS}" ;;
  esac

# Set the audio backend (the video backend is GFXBackend in the ini; a
# "-v $GRENDERER" here was overwritten by the next line, #872 PL-023)
if [ ${DOLPHIN_CORE} = "dolphin-emu" ]; then
  CMD="-b -a ${AUDIO_BACKEND}"
else
  CMD="-p @DOLPHIN_BACKEND@ -a ${AUDIO_BACKEND}"
fi

# Debugging info:
  echo "GAME set to: ${GAME}"
  echo "PLATFORM set to: ${PLATFORM}"
}
