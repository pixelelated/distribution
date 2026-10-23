#!/bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2019-present Shanti Gilbert (https://github.com/shantigilbert)
# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)

# Source predefined functions and variables
. /etc/profile
. /etc/os-release

### Switch to performance mode early to speed up configuration and reduce time it takes to get into games.
performance

# Command line schema
# $1 = Game/Port
# $2 = Platform
# $3 = Core
# $4 = Emulator

ARGUMENTS="$@"
### The platform is the first -P<platform> argument after the ROM, taken
### whole. ${ARGUMENTS##*-P} read from the LAST "-P" anywhere in the joined
### line, so a netplay nick such as My-Player made the platform "layer"
### (#308, stream E2's reading of the launch command).
PLATFORM=""
for ARG in "${@:2}"; do case "${ARG}" in -P?*) PLATFORM="${ARG#-P}"; break ;; esac; done
### --core= and --emulator= are whole arguments too, the last of each
### winning as the launcher reads them (LaunchCommand.h); cutting them from
### the joined line let a state file's path or a nick holding the letters
### win instead (#730, #308's sibling).
### And the argument after a flag that takes a value is that value, never an
### option: a netplay nick that is itself an option word (--nick --core=x,
### one argument) was read as the core while the interface kept the core it
### built the command with (#730, T2's lead).
### The netplay markers and the relay session are read the same way, for the
### netplay block and RetroArch's command below (D-WORKFLOW-192).
CORE=""
EMULATOR=""
SKIP_VALUE=""
NETPLAY_HOST=""
NETPLAY_CLIENT=""
NETPLAY_SPECTATOR=""
NETPLAY_MITM_SESSION=""
for ARG in "${@:2}"; do
  if [ -n "${SKIP_VALUE}" ]; then
    [ "${SKIP_VALUE}" = "--netplaymode" ] && [ "${ARG}" = "spectator" ] && NETPLAY_SPECTATOR=1
    SKIP_VALUE=""
    continue
  fi
  case "${ARG}" in
    --core=*) CORE="${ARG#--core=}" ;;
    --emulator=*) EMULATOR="${ARG#--emulator=}" ;;
    --mitm-session=*) NETPLAY_MITM_SESSION="${ARG#--mitm-session=}" ;;
    --host) NETPLAY_HOST=1 ;;
    --connect) NETPLAY_CLIENT=1; SKIP_VALUE="${ARG}" ;;
    --nick|--port|--netplaymode) SKIP_VALUE="${ARG}" ;;
  esac
done
ROMNAME="$1"
BASEROMNAME=${ROMNAME##*/}

### Define the variables used throughout the script
BLUETOOTH_STATE=$(get_setting controllers.bluetooth.enabled)
VERBOSE=false
LOG_DIRECTORY="/var/log"
LOG_FILE="exec.log"
RUN_SHELL="/usr/bin/bash"
RETROARCH_TEMP_CONFIG="/storage/.config/retroarch/retroarch.cfg"
RETROARCH_APPEND_CONFIG="/tmp/.retroarch.cfg"
SET_SETTINGS_TMP="/tmp/shader"
OUTPUT_LOG="${LOG_DIRECTORY}/${LOG_FILE}"
SCRIPT_NAME=$(basename "$0")
DOLPHIN_LAUNCH=false

### The marker the global exit hotkey leaves behind (input_sense,
### execute_kill): cleared before the emulator starts, consumed by the exit
### mapping at the bottom of this script -- fork #92, D-LAUNCH-002. It sits
### in /tmp beside the kill data the same hotkey reads
### (/tmp/.process-kill-data) because /tmp is a tmpfs: a power cut wipes it,
### which is exactly what is wanted of a flag that must never outlive the
### boot. input.service and this script both run as root, so each can write
### and remove the other's marker.
EXIT_HOTKEY_MARKER="/tmp/.process-kill-requested"

### The previous game's exit restores run in the background, so the
### interface comes back at once (time to play); this launch waits for
### them, five seconds at most, before it sets its own (#727).
RESTORE_PIDFILE="/tmp/.runemu-restore.pid"
if [ -s "${RESTORE_PIDFILE}" ]
then
  RESTORE_PID=$(cat "${RESTORE_PIDFILE}")
  for _ in $(seq 1 50)
  do
    kill -0 "${RESTORE_PID}" 2>/dev/null || break
    sleep 0.1
  done
  rm -f "${RESTORE_PIDFILE}"
fi

### A game's fan profile is written into cooling.profile for its length;
### the device's own value waits in this marker, so a launch that never
### reached its restore (the interface killed, a power cut) is put right by
### the next launch, before it reads the device's value (#728).
FAN_RESTORE_MARKER="/storage/.cache/runemu-fan-restore"
if [ -f "${FAN_RESTORE_MARKER}" ]
then
  SAVED_FAN=$(cat "${FAN_RESTORE_MARKER}")
  if [ -n "${SAVED_FAN}" ]
  then
    set_setting cooling.profile "${SAVED_FAN}"
  else
    del_setting cooling.profile
  fi
  rm -f "${FAN_RESTORE_MARKER}"
fi

### Export Game Guide Path
GAME_GUIDE_PATH_CHECK="${1%.*}.txt"
if [ ! -f "${GAME_GUIDE_PATH_CHECK}" ]; then
  GAME_GUIDE_PATH_CHECK="No Game Guide Found"
fi
### Synchronous on purpose: 5 ms on the GENERIC_X64 guest (T1 #648, F-08).
/usr/bin/game-guides-tool "${1}"

### PortMaster's mapper.txt is shell; a name is written into it with \, ",
### $ and ` escaped, by awk rather than as sed's c\ text (#757).
function set_mapper_line() {
        local MAPPER="/storage/.config/PortMaster/mapper.txt" V
        V=$(printf '%s' "${2}" | sed -e 's/[\\"$`]/\\&/g')
        if [ -f "${MAPPER}" ]
        then
                K="${1}" V="${V}" awk 'BEGIN { k = ENVIRON["K"]; v = ENVIRON["V"] }
                        index($0, k "=") == 1 { print k "=\"" v "\""; next } { print }' "${MAPPER}" > "${MAPPER}.tmp" \
                        && mv -f "${MAPPER}.tmp" "${MAPPER}"
        fi
}

### Function Library
### Every line this script logs -- to exec.log or to its own stdout, which
### the journal keeps -- goes through redact_credentials (001-functions): a
### credential's value reads <redacted>, its key or flag stays. The
### "Executing ..." line carries an emulator's whole command line, and a
### standalone emulator can take a password there (gopher64's --ra-password);
### exec.log is what rocknix-evidence bundles (fork #176, D-INFRA-010). The
### emulator's own output is still redirected straight into the file below,
### not piped through a filter: a game's life must not depend on a second
### process staying alive to read its stdout. The bundle is filtered whole.
function log() {
        # Callers pass "$0" first; the line already starts with the script's name.
        [ "${1}" = "$0" ] && shift
        if [ "${LOG}" == true ]
        then
                if [[ ! -d "$LOG_DIRECTORY" ]]
                then
                        mkdir -p "$LOG_DIRECTORY"
                fi
                redact_credentials "${SCRIPT_NAME}: $*" 2>&1 | tee -a ${LOG_DIRECTORY}/${LOG_FILE}
        else
                redact_credentials "${SCRIPT_NAME}: $*"
        fi
}

function loginit() {
        # The launch log is one launch's, whatever the log level (fork #280).
        # The emulator's output is appended to it below whether or not this
        # script logs, and it used to be truncated only when the level was not
        # none -- so on a device with system.loglevel=none every launch since
        # the file was last removed sat in it, the interface read a rotated
        # game's SET_ROTATION line as the next game's, and rocknix-evidence
        # bundled weeks of launches as one. Truncate first, then the header.
        rm -f ${LOG_DIRECTORY}/${LOG_FILE}
        if [ "${LOG}" == true ]
        then
                redact_credentials <<EOF >${LOG_DIRECTORY}/${LOG_FILE}
Emulation Run Log - Started at $(date)

ARG1: $1
ARG2: $2
ARG3: $3
ARG4: $4
ARGS: $*
EMULATOR: ${EMULATOR}
PLATFORM: ${PLATFORM}
CORE: ${CORE}
ROM NAME: ${ROMNAME}
BASE ROM NAME: ${ROMNAME##*/}
USING CONFIG: ${RETROARCH_TEMP_CONFIG}
USING APPENDCONFIG : ${RETROARCH_APPEND_CONFIG}
GAME GUIDE PATH: ${GAME_GUIDE_PATH_CHECK}

EOF
        else
                : >${LOG_DIRECTORY}/${LOG_FILE}
                log $0 "Emulation Run Log - Started at $(date)"
        fi
}

### A governor setting is a name to look up, never a command to run (#704):
### the four the freqfunctions define; empty or default leaves the governor
### as it is; any other name the kernel offers (conservative, userspace) is
### said in the log rather than run.
function apply_governor() {
        case "${1}" in
                performance|ondemand|schedutil|powersave) "${1}" ;;
                ""|default) ;;
                *) log $0 "No governor function for (${1}); the governor is left as it is." ;;
        esac
}

### onlinethreads is defined only where 099-freqfunctions is installed (not
### x86_64): elsewhere there are no threads to set (#726).
function online_threads() {
        if type -t onlinethreads >/dev/null 2>&1
        then
                onlinethreads "$@"
        fi
}

function quit() {
        ${VERBOSE} && log $0 "Cleaning up and exiting"
        bluetooth enable
        set_kill set "emulationstation"
        clear_screen
        DEVICE_CPU_GOVERNOR=$(get_setting system.cpugovernor)
        apply_governor "${DEVICE_CPU_GOVERNOR}"
        exit $1
}

function clear_screen() {
        ${VERBOSE} && log $0 "Clearing screen"
        clear
}

function bluetooth() {
        if [ "$1" == "disable" ]
        then
                ${VERBOSE} && log $0 "Disabling BT"
                if [[ "${BLUETOOTH_STATE}" == "1" ]]
                then
                        NPID=$(pgrep -f rocknix-bluetooth-agent)
                        if [[ ! -z "$NPID" ]]; then
                                kill "$NPID"
                        fi
                fi
        elif [ "$1" == "enable" ]
        then
                ${VERBOSE} && log $0 "Enabling BT"
                if [[ "${BLUETOOTH_STATE}" == "1" ]]
                then
                        systemd-run rocknix-bluetooth-agent
                fi
        fi
}

### Enable logging
case $(get_setting system.loglevel) in
  off|none)
    LOG=false
  ;;
  verbose)
    LOG=true
    VERBOSE=true
  ;;
  *)
    LOG=true
  ;;
esac

### Prepare to load our emulator and game.
loginit "$1" "$2" "$3" "$4"
clear_screen
bluetooth disable
set_kill stop

### Determine which emulator we're launching and make appropriate adjustments before launching.
${VERBOSE} && log $0 "Configuring for ${EMULATOR}"
### The save state manager's arguments follow --controllers= on the command
### line. The interface writes them, this script reads them, setsettings.sh
### turns them into RetroArch's configuration (fork #196, D-UI-057):
###   -autosave 0|1       the exit auto save and auto-load, off or on, for this run
###   -state_slot N       RetroArch's current slot (-1 is its auto slot)
###   -state_file <path>  the state to start from: the .auto file, or a slot's
### Since es_savestates.cfg each of them can arrive on its own -- "-autosave 1
### -state_file <auto>" for the AUTO SAVE tile and for a plain launch with AUTO
### SAVE/LOAD on, "-autosave 0" alone for START NEW GAME, "-state_slot N
### -state_file <slot file>" for a numbered slot -- where the interface's
### built-in fallback always sent -state_slot with them. Sets CONTROLLERCONFIG,
### SNAPSHOT, AUTOSAVE and STATEFILE; call it with the script's own "$@".
function parse_savestate_arguments() {
  CONTROLLERCONFIG="${ARGUMENTS#*--controllers=*}"
  SNAPSHOT=""
  AUTOSAVE=""
  STATEFILE=""

  ### Each value is the argument after its flag, from the argument list --
  ### the shell already split it. The state file is a path, and ROM names
  ### carry spaces, parentheses and " - " (Mario Tennis - Power Tour (USA,
  ### Australia)), so it was always taken this way; the slot and the auto
  ### save were cut out of the joined line, where the FIRST " -state_slot "
  ### could be inside the ROM's own name ("Demo -state_slot 2 - Part.sfc")
  ### and win over the real flag (#308, the gpt seat's F-PB-17).
  local PREVIOUS="" ARGUMENT FLAGGED=0
  for ARGUMENT in "$@"
  do
    case "${PREVIOUS}" in
      -state_slot) SNAPSHOT="${ARGUMENT}" ;;
      -autosave)   AUTOSAVE="${ARGUMENT}" ;;
      -state_file) STATEFILE="${ARGUMENT}" ;;
    esac
    case "${ARGUMENT}" in
      -state_slot|-autosave|-state_file) FLAGGED=1 ;;
    esac
    PREVIOUS="${ARGUMENT}"
  done

  if [ "${FLAGGED}" -eq 1 ]
  then
    ### The controllers value ends where the first of them begins.
    CONTROLLERCONFIG="${CONTROLLERCONFIG%% -state_slot *}"
    CONTROLLERCONFIG="${CONTROLLERCONFIG%% -autosave *}"
    CONTROLLERCONFIG="${CONTROLLERCONFIG%% -state_file *}"
  else
    CONTROLLERCONFIG="${CONTROLLERCONFIG%% --*}"  # until a -- is found
  fi
}

case ${EMULATOR} in
  mednafen)
    set_kill set "-9 mednafen"
    RUNTHIS='${RUN_SHELL} /usr/bin/start_mednafen.sh "${ROMNAME}" "${CORE}" "${PLATFORM}"'
  ;;
  retroarch)
    # netplay.mode is this launch's: cleared, then set from its arguments,
    # read whole as the core is (above), so a nick holding --host is no
    # marker. The spectator first: a spectator connects, so its line carries
    # --connect too, and read client-first it joined as a player
    # (D-WORKFLOW-192, #776).
    del_setting netplay.mode

    if [ -n "${NETPLAY_SPECTATOR}" ]; then
      ${VERBOSE} && log $0 "Setup netplay spectator."
      set_setting "netplay.mode" "spectator"
    elif [ -n "${NETPLAY_HOST}" ]; then
      ${VERBOSE} && log $0 "Setup netplay host."
      set_setting netplay.mode "host"
    elif [ -n "${NETPLAY_CLIENT}" ]; then
      ${VERBOSE} && log $0 "Setup netplay client."
      set_setting netplay.mode "client"
    fi

    ### Set set_kill to kill the appropriate retroarch
    set_kill set "retroarch retroarch32"

    ### Assume we're running 64bit Retroarch
    RABIN="retroarch"

    case ${HW_ARCH} in
      aarch64)
        if [[ "${CORE}" =~ pcsx_rearmed32 ]] || \
           [[ "${CORE}" =~ gpsp ]] || \
           [[ "${CORE}" =~ desmume ]]
        then
          ### Configure for 32bit Retroarch
          ${VERBOSE} && log $0 "Configuring for 32bit cores."
          export RABIN="retroarch32"
        fi
      ;;
    esac


    ### Configure specific emulator requirements
    case ${CORE} in
      freej2me*)
        ${VERBOSE} && log $0 "Setup freej2me requirements."
        /usr/bin/freej2me.sh
        JAVA_HOME='/storage/jdk'
        export JAVA_HOME
        PATH="$JAVA_HOME/bin:$PATH"
        export PATH
        export _JAVA_OPTIONS="-Djava.awt.headless=true"
      ;;
      easyrpg*)
        # easyrpg needs runtime files to be downloaded on the first run
        ${VERBOSE} && log $0 "Setup easyrpg requirements."
        /usr/bin/easyrpg.sh
      ;;
    esac


    ### The relay session the interface was given (--mitm-session=<id>,
    ### D-WORKFLOW-192) goes to RetroArch's command as it came, when it is a
    ### word: it is spliced into RUNTHIS, which is eval'ed as root, so only
    ### characters within #702's filter pass, and anything else is dropped
    ### and said.
    MITM_ARG=""
    if [ -n "${NETPLAY_MITM_SESSION}" ]; then
      if [[ "${NETPLAY_MITM_SESSION}" =~ ^[A-Za-z0-9._:-]+$ ]]; then
        MITM_ARG="--mitm-session=${NETPLAY_MITM_SESSION}"
      else
        log $0 "Dropped --mitm-session (${#NETPLAY_MITM_SESSION} characters): a session is letters, digits, '.', ':', '_' and '-'."
      fi
    fi
    RUNTHIS='${EMUPERF} /usr/bin/${RABIN} -L /tmp/cores/${CORE}_libretro.so --config ${RETROARCH_TEMP_CONFIG} --appendconfig ${RETROARCH_APPEND_CONFIG} ${MITM_ARG} "${ROMNAME}"'

    parse_savestate_arguments "$@"

    # Configure platform specific requirements
    case ${PLATFORM} in
      "atomiswave")
        rm -f -- "${ROMNAME}".nvmem*
      ;;
      "scummvm")
        GAMEDIR=$(cat "${ROMNAME}" | awk 'BEGIN {FS="\""}; {print $2}')
        cd "${GAMEDIR}"
        RUNTHIS='${RUN_SHELL} /usr/bin/start_scummvm.sh libretro .'
      ;;
    esac

    ### Configure retroarch
    if [ -e "${SET_SETTINGS_TMP}" ]
    then
      rm -f "${SET_SETTINGS_TMP}"
    fi
    ### --state_file= goes ahead of --controllers=: setsettings reads CONTROLLERS
    ### as everything after --controllers=, and a state file's path is a ROM
    ### name, which can hold "p1" and would read as a controller (#196).
    ${VERBOSE} && log $0 "Execute setsettings (${PLATFORM} ${ROMNAME} ${CORE} --state_file=${STATEFILE} --controllers=${CONTROLLERCONFIG} --autosave=${AUTOSAVE} --snapshot=${SNAPSHOT})"
    (/usr/bin/setsettings.sh "${PLATFORM}" "${ROMNAME}" "${CORE}" --state_file="${STATEFILE}" --controllers="${CONTROLLERCONFIG}" --autosave="${AUTOSAVE}" --snapshot="${SNAPSHOT}" >${SET_SETTINGS_TMP})

    ### Enable RetroArch Network Control for this session on dual-screen devices
    ### so the bottom-screen UI can forward save-state / load-state / resume commands.
    if [ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ]; then
      echo 'network_cmd_enable = "true"' >> "${RETROARCH_APPEND_CONFIG}"
      echo 'network_cmd_port = "55355"'  >> "${RETROARCH_APPEND_CONFIG}"
      echo 'savestate_thumbnail_enable = "true"' >> "${RETROARCH_APPEND_CONFIG}"
      echo 'cheevos_custom_host = "http://127.0.0.1:4874"' >> "${RETROARCH_APPEND_CONFIG}"

      if ! pgrep -f 'python3 .*/lowerdeck/ra_proxy\.py' >/dev/null 2>&1; then
        ( python3 /usr/share/lowerdeck/ra_proxy.py >/dev/null 2>&1 ) &
        for _ in 1 2 3 4 5 6 7 8 9 10; do
          netstat -ln 2>/dev/null | grep -q ':4874 ' && break
          sleep 0.1
        done
      fi
    fi

    ### If setsettings wrote data in the background, grab it and assign it to EXTRAOPTS
    if [ -e "${SET_SETTINGS_TMP}" ]
    then
      EXTRAOPTS=$(cat ${SET_SETTINGS_TMP})
      rm -f ${SET_SETTINGS_TMP}
      ${VERBOSE} && log $0 "Extra Options: ${EXTRAOPTS}"
      ### EXTRAOPTS is spliced into RUNTHIS, which is eval'ed as root below,
      ### so it may hold only what an option and its value need; anything
      ### carrying a shell character is dropped whole, not run (#702, A-05).
      EXTRAOPTS_RE='[^[:alnum:][:space:]._/:,+@=-]'
      if [[ "${EXTRAOPTS}" =~ ${EXTRAOPTS_RE} ]]; then
        log $0 "Dropped setsettings.sh's extra options: they held a character no option needs."
        EXTRAOPTS=""
      fi
    fi

    if [[ ${EXTRAOPTS} != 0 ]]; then
      RUNTHIS=$(echo ${RUNTHIS} | sed "s|--config|${EXTRAOPTS} --config|")
    fi
  ;;
  *)
    case ${PLATFORM} in
      "setup")
        RUNTHIS='${RUN_SHELL} "${ROMNAME}"'
      ;;
      "gamecube"|"triforce")
        DOLPHIN_LAUNCH=true
        RUNTHIS='${RUN_SHELL} /usr/bin/start_dolphin_gc.sh "${ROMNAME}" "${PLATFORM}" "${CORE}"'
      ;;
      "wii"|"wiiware")
        DOLPHIN_LAUNCH=true
        RUNTHIS='${RUN_SHELL} /usr/bin/start_dolphin_wii.sh "${ROMNAME}" "${PLATFORM}" "${CORE}"'
      ;;
      "ports")
      if [[ "${ROMNAME,,}" == *".appimage" ]]; then
        RUNTHIS='${EMUPERF} "${ROMNAME}"'
      else
        RUNTHIS='${EMUPERF} ${RUN_SHELL} "${ROMNAME}"'
      fi
        chmod +x "${ROMNAME}"
        set_mapper_line ACTIVE_GAME "${ROMNAME}"
        set_mapper_line ACTIVE_PLATFORM "${PLATFORM}"
      ;;
      "windows")
        RUNTHIS='${EMUPERF} ${RUN_SHELL} "${ROMNAME}"'
        # Hook into Portmaster control mapping
        set_mapper_line ACTIVE_GAME "${ROMNAME}"
        set_mapper_line ACTIVE_PLATFORM "${PLATFORM}"
      ;;
      "shell")
        RUNTHIS='${RUN_SHELL} "${ROMNAME}"'
      ;;
      *)
        RUNTHIS='${RUN_SHELL} "/usr/bin/start_${CORE%-*}.sh" "${ROMNAME}" "${PLATFORM}"'
      ;;
    esac
  ;;
esac

### Execution time.
clear_screen
${VERBOSE} && log $0 "executing game: ${ROMNAME}"
${VERBOSE} && log $0 "script to execute: ${RUNTHIS}"

### Set the cores to use
CORES=$(get_setting "cores" "${PLATFORM}" "${ROMNAME##*/}")
${VERBOSE} && log $0 "Configure big.little (${CORES})"
case ${CORES} in
  little)
    EMUPERF="${SLOW_CORES}"
  ;;
  big)
    EMUPERF="${FAST_CORES}"
  ;;
  *)
    unset EMUPERF
  ;;
esac

### We need the original system cooling profile later so get it now!
COOLINGPROFILE=$(get_setting cooling.profile)

### Configure GPU performance mode
GPUPERF=$(get_setting "gpuperf" "${PLATFORM}" "${ROMNAME##*/}")
if [ ! -z ${GPUPERF} ]
then
  ${VERBOSE} && log $0 "Set GPU performance to (${GPUPERF})"
  gpu_performance_level ${GPUPERF}
  get_gpu_performance_level >/tmp/.gpu_performance_level
fi

if [ "${DEVICE_HAS_FAN}" = "true" ]
then
  ### Set any custom fan profile (make this better!)
  GAMEFAN=$(get_setting "cooling.profile" "${PLATFORM}" "${ROMNAME##*/}")
  if [ ! -z "${GAMEFAN}" ]
  then
    ${VERBOSE} && log $0 "Set fan profile to (${GAMEFAN})"
    printf '%s' "${COOLINGPROFILE}" > "${FAN_RESTORE_MARKER}"
    set_setting cooling.profile ${GAMEFAN}
    systemctl restart fancontrol
  fi
fi

### Display mode for emulation
DISPLAY_MODE=$(get_setting "display_mode" "${PLATFORM}" "${ROMNAME##*/}")
if [ ! -z "${DISPLAY_MODE}" ] && [ "${DISPLAY_MODE}" != "default" ]
then
  set_refresh_rate "${DISPLAY_MODE}"
fi

FORCEPACK=$(get_setting "forcepack" "${PLATFORM}" "${ROMNAME##*/}")
if [ ! -z "${FORCEPACK}" ] && [ "${FORCEPACK}" = "On" ]
then
    ${VERBOSE} && log $0 "Enabling panfrost forcepack"
    export PAN_MESA_DEBUG=forcepack
fi

### Offline all but the number of threads we need for this game if configured.
NUMTHREADS=$(get_setting "threads" "${PLATFORM}" "${ROMNAME##*/}")
if [ -n "${NUMTHREADS}" ] &&
   [ ! ${NUMTHREADS} = "default" ]
then
  ${VERBOSE} && log $0 "Configure active cores (${NUMTHREADS})"
  online_threads ${NUMTHREADS} 0
fi

### Set the governor mode for emulation
CPU_GOVERNOR=$(get_setting "cpugovernor" "${PLATFORM}" "${ROMNAME##*/}")
${VERBOSE} && log $0 "Set emulation performance mode to (${CPU_GOVERNOR})"
apply_governor "${CPU_GOVERNOR}"

### Check whether MangoHud is supported and enabled
if [ "${DEVICE_MANGOHUD_SUPPORT}" == "true" ]; then
  MANGOHUD_ENABLED=$(get_setting "rocknix.mangohud.enabled"  "${PLATFORM}" "${ROMNAME##*/}")
  if [ "${MANGOHUD_ENABLED}" = "1" ]; then
    # Enable GPU profiling and MangoHud
    gpu_profiling "on"
    RUNTHIS="/usr/bin/mangohud ${RUNTHIS}"
    ${VERBOSE} && log $0 "Enabling MangoHud"
  fi
fi

### Clear the exit hotkey marker on the way into the emulator, so a press
### left over from an earlier launch -- or from the carousel, where the same
### hotkey kills EmulationStation -- can never be read as this launch ending
### (fork #92). Both dispatch paths below run through here, and nothing above
### it starts an emulator; keep it that way.
rm -f "${EXIT_HOTKEY_MARKER}"

# If the rom is a shell script just execute it, useful for DOSBOX and ScummVM scan scripts
if [[ "${ROMNAME}" == *".sh" ]] && [ ! "${PLATFORM}" = "ports" ] && [ ! "${PLATFORM}" = "windows" ]; then
        ${VERBOSE} && log $0 "Executing shell script ${ROMNAME}"
        DOLPHIN_LAUNCH=false
        "${ROMNAME}" &>>${OUTPUT_LOG}
        ret_error=$?
else
        ${VERBOSE} && log $0 "Executing $(eval echo ${RUNTHIS})"
        # A Dolphin preparation refusal owns only this launch's native message.
        # Other emulator exit codes must not acquire a stale custom error.
        if [ "${DOLPHIN_LAUNCH}" = true ]; then
                rm -f /tmp/launch_error.log || quit 1
        fi
        eval ${RUNTHIS} &>>${OUTPUT_LOG}
        ret_error=$?
fi

### Switch back to performance mode to clean up
performance

clear_screen

### Disable touch on the secondary screen for dual screen devices
if [[ "${DEVICE_HAS_DUAL_SCREEN}" == "true" ]]; then
  # Disable touch events for Retroid Pocket devices to prevent focus loss
  if [[ "${QUIRK_DEVICE}" == "Retroid Pocket 5" || "${QUIRK_DEVICE}" == "Retroid Pocket Flip2" || "${QUIRK_DEVICE}" == "Retroid Pocket Mini" || "${QUIRK_DEVICE}" == "Retroid Pocket Mini V2" ]]; then
    swaymsg input "0:0:generic_ft5x06_(a0)" events disabled
    swaymsg input "0:0:generic_ft5x06_(8d)" events disabled
  fi
fi

### Go back to system display mode , if we had specialized mode defined
DISPLAY_MODE=$(get_setting "display_mode" "${PLATFORM}" "${ROMNAME##*/}")
if [ ! -z "${DISPLAY_MODE}" ] && [ "${DISPLAY_MODE}" != "default" ]
then
  DISPLAY_MODE=$(get_setting "system.display_mode")
  DISPLAY_OUTPUT=$(/usr/bin/wlr-randr | awk 'NR==1{print $1;}')
  if [ -z "${DISPLAY_MODE}" ]; then
    # if we have no system mode use the displays preferred mode
    /usr/bin/wlr-randr --output ${DISPLAY_OUTPUT} --preferred
  else
    # If we have user specifed system mode set that
    set_refresh_rate "${DISPLAY_MODE}"
  fi
fi

### Restore cooling profile. With no device value saved, the key is
### removed again rather than written empty (#728, A-09).
if [ "${DEVICE_HAS_FAN}" = "true" ]
then
  ${VERBOSE} && log $0 "Restore system cooling profile (${COOLINGPROFILE})"
  if [ -n "${COOLINGPROFILE}" ]
  then
    set_setting cooling.profile ${COOLINGPROFILE}
  else
    del_setting cooling.profile
  fi
  rm -f "${FAN_RESTORE_MARKER}"
fi

### The restores below run in the background as one job, recorded, so the
### next launch can wait for them (#727).
GPUPERF=$(get_setting "system.gpuperf")
NUMTHREADS=$(get_setting "system.threads")
rm -f /tmp/.gpu_performance_level 2>/dev/null
(
  if [ "${DEVICE_HAS_FAN}" = "true" ]
  then
    systemctl restart fancontrol
  fi

  ### Restore system GPU performance mode
  if [ ! -z ${GPUPERF} ]
  then
    ${VERBOSE} && log $0 "Restore system GPU performance mode (${GPUPERF})"
    gpu_performance_level ${GPUPERF}
  else
    ${VERBOSE} && log $0 "Restore system GPU performance mode (auto)"
    gpu_performance_level auto
  fi

  ### Reset the number of cores to use.
  ${VERBOSE} && log $0 "Restore active threads (${NUMTHREADS})"
  if [ -n "${NUMTHREADS}" ]
  then
    online_threads ${NUMTHREADS} 0
  else
    online_threads all 1
  fi
  rm -f "${RESTORE_PIDFILE}"
) &
echo $! > "${RESTORE_PIDFILE}"

### Disable GPU profiling
gpu_profiling "off"

### Capture and the game-exit save sync run from EmulationStation (FileData::launchGame, fork #21).
### Never spawn a second uploader here: it would run before ES resumes, so before capture, as a second writer on one remote (#21 DOES-NOT-BUILD).

${VERBOSE} && log $0 "Checking errors: ${ret_error} "
### Report how the launch ended. EmulationStation records play count, play time
### and last-played only on 0 (FileData::launchGame) and hands the same code to
### cloud_capture --exit. The global exit hotkey (input_sense, execute_kill) ends
### a standalone emulator with killall -9 and RetroArch with SIGTERM, so 137 and
### 143 are the player leaving, not a failed launch: a clean exit. Every other
### non-zero status still collapses to 1 -- ES keeps 200-300 for messages it can
### name, and an emulator's own codes would land in that range.
###
### 137/143 cover an emulator that dies on the signal. RetroArch does not: it
### catches SIGTERM and ends with its own exit(1), which is the same status as
### "Failed to load content", so no rule reading the code alone can tell a
### forced quit from a failed launch. The hotkey therefore says so itself --
### execute_kill touches ${EXIT_HOTKEY_MARKER} immediately before the killall,
### and a non-zero status that follows a press is read as the player leaving
### (fork #92, D-LAUNCH-002). A launch with no marker behaves exactly as before.
### Consume the marker here whatever happened, so it cannot reach another launch.
EXIT_HOTKEY_PRESSED=false
if [ -e "${EXIT_HOTKEY_MARKER}" ]
then
        EXIT_HOTKEY_PRESSED=true
        rm -f "${EXIT_HOTKEY_MARKER}"
fi
# Dolphin preparation uses the existing ES custom-error channel. Require its
# fresh message as well as its status; a native emulator's numeric exit alone
# is not a preparation refusal. This precedes the hotkey's clean-exit mapping.
if [ "${DOLPHIN_LAUNCH}" = true ] && [ "${ret_error}" = 250 ] &&
   [ -f /tmp/launch_error.log ] && [ ! -L /tmp/launch_error.log ]; then
        IFS= read -r DOLPHIN_ERROR_TITLE < /tmp/launch_error.log
        if [ "${DOLPHIN_ERROR_TITLE}" = "DOLPHIN DID NOT START" ]; then
                # Remove the fixed ownership line before ES displays localized text.
                DOLPHIN_VISIBLE_ERROR=$(mktemp /tmp/.dolphin-visible-error.XXXXXX) || quit 1
                if ! sed '1d' /tmp/launch_error.log > "${DOLPHIN_VISIBLE_ERROR}" ||
                   ! mv -f "${DOLPHIN_VISIBLE_ERROR}" /tmp/launch_error.log; then
                        rm -f "${DOLPHIN_VISIBLE_ERROR}"
                        quit 1
                fi
                quit 250
        fi
fi
case "${ret_error}" in
  0)
        quit 0
  ;;
  137|143)
        log $0 "emulator ended by signal (${ret_error}, the exit hotkey); a clean exit"
        quit 0
  ;;
  *)
        if [ "${EXIT_HOTKEY_PRESSED}" = true ]
        then
                log $0 "emulator exited ${ret_error} after the exit hotkey was pressed (marker consumed); a clean exit"
                quit 0
        fi
        log $0 "exiting with ${ret_error}"
        quit 1
  ;;
esac
