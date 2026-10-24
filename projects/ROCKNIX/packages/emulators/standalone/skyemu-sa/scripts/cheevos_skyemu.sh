#! /bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2025-present ROCKNIX (https://github.com/ROCKNIX)

. /etc/profile

LOG_FILE="/var/log/cheevos.log"

# Extract username, password, token, if enabled, and hardcore mode from system.cfg
username=$(get_setting "global.retroachievements.username")
token=$(get_setting "global.retroachievements.token")
enabled=$(get_setting "global.retroachievements")

# Write a private file whole, once: mode 0600, temp and rename.
write_private() { # file content
  local tmp
  mkdir -p "${1%/*}" || return 1
  tmp=$(umask 077; mktemp "${1}.XXXXXX") || return 1
  if printf '%s' "$2" > "${tmp}" && mv -f "${tmp}" "$1"; then
    return 0
  fi
  rm -f "${tmp}"
  return 1
}

RA_TOKEN_FILE="/storage/.config/SkyEmu/ra_token.txt"

# Off, or on with no token: an empty token file, so the previous account is
# not signed in (#861).
if [ "${enabled}" != "1" ]; then
  echo "RetroAchievements are not enabled, please turn them on in Emulation Station." > ${LOG_FILE}
  write_private "${RA_TOKEN_FILE}" "" || echo "SkyEmu's token file could not be cleared." >> ${LOG_FILE}
  exit 1
fi

# Check if api token is present in system.cfg
if [ -z "${token}" ]; then
    echo "RetroAchievements token is empty, please log in with your RetroAchievements credentials in Emulation Station." > ${LOG_FILE}
    write_private "${RA_TOKEN_FILE}" "" || echo "SkyEmu's token file could not be cleared." >> ${LOG_FILE}
    exit 1
fi

# The user and the token, private (#870)
write_private "${RA_TOKEN_FILE}" "${username}"$'\n'"${token}"$'\n' || echo "SkyEmu's token file could not be written." >> ${LOG_FILE}
