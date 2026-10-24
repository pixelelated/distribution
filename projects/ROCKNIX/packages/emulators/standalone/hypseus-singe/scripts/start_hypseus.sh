#!/bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2021-present Shanti Gilbert (https://github.com/shantigilbert)
# Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)

. /etc/profile
set_kill set "-9 hypseus"

dir="${1}"
name=${dir##*/}
name=${name%.*}
config="/storage/.config/game/configs/hypseus"
configfile="${config}/hypinput.ini"

# Attempt to auto configure gamepad
GAMEPADINFO="$(sdljoytest -skip_loop)"
JOYNAME=$(echo "${GAMEPADINFO}" | grep "Joystick 0 name " | sed "s|Joystick 0 name ||" | sed "s|'||g")

# The pad's name is the device's own text: a / in it would leave the
# autoconfig folder (F-42)
GPFILE="/usr/share/libretro/autoconfig/${JOYNAME//\//}.cfg"

if [[ -f "${GPFILE}" ]]; then
        # Other keys to consider KEY_SCREENSHOT KEY_QUIT KEY_PAUSE
        for key in KEY_UP KEY_DOWN KEY_LEFT KEY_RIGHT KEY_BUTTON1 KEY_BUTTON2 KEY_BUTTON3 KEY_START1 KEY_COIN1; do
            case ${key} in
            "KEY_UP")
                button=$(cat "${GPFILE}" | grep -E '^input_up_btn\b' | cut -d '"' -f2)
                keyboard="1073741906 0"
                ;;
            "KEY_DOWN")
                button=$(cat "${GPFILE}" | grep -E '^input_down_btn\b' | cut -d '"' -f2)
                keyboard="1073741905 0"
                ;;
            "KEY_LEFT")
                button=$(cat "${GPFILE}" | grep -E '^input_left_btn\b' | cut -d '"' -f2)
                keyboard="1073741904 0"
                ;;
            "KEY_RIGHT")
                button=$(cat "${GPFILE}" | grep -E '^input_right_btn\b' | cut -d '"' -f2)
                keyboard="1073741903 0"
                ;;
            "KEY_BUTTON1")
                button=$(cat "${GPFILE}" | grep -E '^input_a_btn\b' | cut -d '"' -f2)
                keyboard="1073742048 0"
                ;;
            "KEY_BUTTON2")
                button=$(cat "${GPFILE}" | grep -E '^input_b_btn\b' | cut -d '"' -f2)
                keyboard="1073742050 0"
                ;;
            "KEY_BUTTON3")
                button=$(cat "${GPFILE}" | grep -E '^input_x_btn\b' | cut -d '"' -f2)
                keyboard="32 0"
                ;;
            "KEY_START1")
                button=$(cat "${GPFILE}" | grep -E '^input_start_btn\b' | cut -d '"' -f2)
                keyboard="49 0"
                ;;
            "KEY_COIN1")
                button=$(cat "${GPFILE}" | grep -E '^input_select_btn\b' | cut -d '"' -f2)
                keyboard="53 54"
                ;;
            esac

            # if the button is in fact a hat extract the number, else use the button number+1
            # A value that is neither a hat nor a number is skipped: it would
            # enter Bash arithmetic, which evaluates subscripts (F-42)
            if [[ "${button}" =~ ^h[0-9] ]]; then
                button="0 ${button:1:1}"
            elif [[ "${button}" =~ ^[0-9]+$ ]]; then
                button="$((button + 1))"
            else
                continue
            fi

            sed -i "s|${key}.*|${key} = ${keyboard} ${button} |" ${configfile}
        done
fi # finish auto gamepad

# The .commands file's words are arguments; read, not expanded, so a glob
# in it stays a word (F-42)
params=()
if [[ -f "${dir}/${name}.commands" ]]; then
    read -r -a params < "${dir}/${name}.commands"
fi

cd "${config}"

if [[ -f "${dir}/${name}.singe" ]]; then
    hypseus singe vldp -framefile "${dir}/${name}.txt" -script "${dir}/${name}.singe" -fullscreen -useoverlaysb 2 "${params[@]}"
else
    hypseus "${name}" vldp -framefile "${dir}/${name}.txt" -fullscreen -useoverlaysb 2 "${params[@]}"
fi
