#! /bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2022-present Hector Calvarro (https://github.com/kelvfimer)
# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)

. /etc/profile

FLYCAST_CFG="/storage/.config/flycast/emu.cfg"
LOG_FILE="/var/log/cheevos.log"

# Extract username, token, if enabled, and hardcore mode from system.cfg
username=$(get_setting "global.retroachievements.username")
token=$(get_setting "global.retroachievements.token")
enabled=$(get_setting "global.retroachievements")
hardcore=$(get_setting "global.retroachievements.hardcore")

# Write [SECTION]'s keys as data: awk reads each value from the environment,
# so no sign-in value reaches sed or the shell; every other key and section
# is kept, the section ends at the next [header], and the file is replaced
# only once the new one is written (temp and rename).
write_section() { # file section key=value...
  local file="$1" section="$2" pair keys="" tmp
  local -a envs=()
  shift 2
  for pair in "$@"; do keys="${keys} ${pair%%=*}"; envs+=("V_${pair%%=*}=${pair#*=}"); done
  [ -e "${file}" ] || : > "${file}" || return 1
  tmp=$(umask 077; mktemp "${file}.XXXXXX") || return 1
  if env "${envs[@]}" KEYS="${keys}" SECTION="[${section}]" awk '
      BEGIN { n = split(ENVIRON["KEYS"], k, " "); for (i = 1; i <= n; i++) want[k[i]] = 1 }
      function rest(   i) { for (i = 1; i <= n; i++) if (!done[k[i]]) { print k[i] " = " ENVIRON["V_" k[i]]; done[k[i]] = 1 } }
      /^\[/ { if (insec) { rest(); insec = 0 } if ($0 == ENVIRON["SECTION"]) { insec = 1; seen = 1 } print; next }
      insec { key = $0; sub(/[ \t]*=.*/, "", key); sub(/^[ \t]+/, "", key)
              if (key in want) { if (!done[key]) print key " = " ENVIRON["V_" key]; done[key] = 1; next } }
      { print }
      END { if (insec) rest(); else if (!seen) { print ENVIRON["SECTION"]; rest() } }
    ' "${file}" > "${tmp}" && mv -f "${tmp}" "${file}"; then
    return 0
  fi
  rm -f "${tmp}"
  return 1
}

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

# Off, or on with no token: publish a disabled session -- the flag off, the
# user and the token cleared -- so the previous account is not signed in (#861).
publish_disabled() {
  write_section "${FLYCAST_CFG}" achievements "Enabled=no" "UserName=" "Token=" \
    || echo "flycast's achievements settings could not be written." >> ${LOG_FILE}
}

# Check if RetroAchievements are enabled in Emulation Station (quoted: an
# empty read fell through as enabled, #870)
if [ "${enabled}" != "1" ]; then
    echo "RetroAchievements are not enabled, please turn them on in Emulation Station." > ${LOG_FILE}
    publish_disabled
    exit 1
fi

# Check if api token is present in system.cfg
if [ -z "${token}" ]; then
    echo "RetroAchievements token is empty, please log in with your RetroAchievements credentials in Emulation Station." > ${LOG_FILE}
    publish_disabled
    exit 1
fi

# Set hardcore mode
if [ "${hardcore}" = 1 ]; then
  hardcore="true"
else
  hardcore="false"
fi

# Update emulator config with RetroAchievements settings, as data
write_section "${FLYCAST_CFG}" achievements "Enabled=yes" "HardcoreMode=${hardcore}" "UserName=${username}" "Token=${token}" \
  || echo "flycast's achievements settings could not be written." >> ${LOG_FILE}
