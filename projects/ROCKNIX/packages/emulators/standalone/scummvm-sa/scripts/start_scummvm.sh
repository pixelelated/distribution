#!/bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2019-present Shanti Gilbert (https://github.com/shantigilbert)
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)

# Source predefined functions and variables
. /etc/profile

CONFIG_DIR="/storage/.config/scummvm"
ROMSPATH="/storage/roms"
BIOSPATH="${ROMSPATH}/bios"
RATMPCONF="/storage/.config/retroarch/retroarch.cfg"

shopt -s extglob
if [[ "$1" =~ ^(add|create|libretro)$ ]]
then
  GAME="$2"
else
  GAME="$1"
fi

# Seed the config on a first run. This has to come before games/ is made,
# which creates CONFIG_DIR and made the seed unreachable (#871).
if [ ! -d "${CONFIG_DIR}" ]; then
 mkdir -p "${CONFIG_DIR}"
 cp -rf /usr/config/scummvm/* "${CONFIG_DIR}/"
fi

if [ ! -d "${CONFIG_DIR}/games" ]
then
  mkdir -p "${CONFIG_DIR}/games"
fi

create_svm(){
  /usr/bin/scummvm --list-targets | tail -n +3 | cut -d " " -f 1 | \
  while read line
  do
    id=($line);
    filename=$(sed -n "/^\[$id\]/,/^\[/{s/^description=//p}" ${CONFIG_DIR}/scummvm.ini | \
      sed -e 's# (.*)# ('${id}')#g' -e "s#'##g" -e "s#: # - #g" -e "s#/#-#g" \
    )

    SVMPATH="$(sed -n "/^\[$id\]/,/^\[/{s/^path=//p}" ${CONFIG_DIR}/scummvm.ini)"
    # A name stays inside games/ (a / in a description made a path, #871)
    printf -- '--path="%s" %s\n' "${SVMPATH}" "${id}" >"${CONFIG_DIR}/games/${filename}.scummvm"
  done
}


case $1 in
  "libretro")
    GAME=$(cat "${GAME}" | awk 'BEGIN {FS="\""}; {print $2}')
    cd "${GAME}"
    /usr/bin/retroarch -L /tmp/cores/scummvm_libretro.so --config ${RATMPCONF} .
  ;;

  "add")
    if [ ! -d "${ROMSPATH}/scummvm" ]; then
      mkdir "${ROMSPATH}/scummvm"
    fi
    /usr/bin/scummvm --add --path="${ROMSPATH}/scummvm" --recursive
    mkdir -p ${BIOSPATH}
    cp ${CONFIG_DIR}/scummvm.ini ${BIOSPATH}/scummvm.ini
  ;;

  "create")
    create_svm
  ;;

  *)
    set_kill set "-9 scummvm"
    # The .scummvm file is data, never shell: --path="<dir>" <target> as
    # create_svm writes it, or a bare target. Its first line's words become
    # scummvm's arguments, the quoted path one of them.
    IFS= read -r SVM_LINE <"${GAME}"
    SVM_LINE="${SVM_LINE%$'\r'}"
    SVM_ARGS=()
    if [[ "${SVM_LINE}" =~ ^[[:space:]]*--path=\"([^\"]*)\"(.*)$ ]]; then
      SVM_ARGS=("--path=${BASH_REMATCH[1]}")
      SVM_LINE="${BASH_REMATCH[2]}"
    fi
    read -r -a SVM_REST <<<"${SVM_LINE}"
    SVM_ARGS+=("${SVM_REST[@]}")
    systemctl start fluidsynth
    /usr/bin/scummvm --fullscreen --joystick=0 --themepath=/usr/config/scummvm/themes "${SVM_ARGS[@]}"
    systemctl stop fluidsynth
  ;;
esac
