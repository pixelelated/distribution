#! /bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2022-present Hector Calvarro (https://github.com/kelvfimer)
# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)

. /etc/profile

PPSSPP_ACHIEVEMENTS="/storage/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat"
PPSSPP_INI="/storage/.config/ppsspp/PSP/SYSTEM/ppsspp.ini"
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
# user and the token cleared -- so the previous account is not signed in
# (cheevos_dolphin.sh's publish_disabled shape, #861).
publish_disabled() {
  write_private "${PPSSPP_ACHIEVEMENTS}" "" \
    || echo "PPSSPP's achievements token file could not be cleared." >> ${LOG_FILE}
  write_section "${PPSSPP_INI}" Achievements "AchievementsEnable=False" "AchievementsUserName=" "AchievementsHost=" \
    || echo "PPSSPP's achievements settings could not be written." >> ${LOG_FILE}
}

# Check if RetroAchievements are enabled in Emulation Station. Quoted: an
# empty read used to make the test a syntax error that fell through to
# "enabled" (audit #186 PL-31).
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
hardcore_raw="${hardcore}"
if [ "${hardcore}" = 1 ]; then
  hardcore="True"
else
  hardcore="False"
fi

# OFFLINE RETROACHIEVEMENTS (fork #165, D-RA-002): PPSSPP's own achievements
# client behind AchievementsHost, pointed at the RAOfflineProxy service on
# loopback when the toggle is on, hardcore is off (the proxy refuses hardcore
# awards) and the port answers -- a host with nothing behind it would disable
# achievements for the session. Empty otherwise, which is PPSSPP's default
# host: this file travels in a settings backup, so a restored device with the
# toggle off must find the line cleared, not pointing at a dead port.
# PPSSPP reads the key from ppsspp.ini's [Achievements] (Core/Config.cpp:376
# at the pinned v1.20.2, afbc66a3) and, when it is not empty, hands it to
# rcheevos as the host (rc_client_set_host, Core/RetroAchievements.cpp:650-652)
# -- "a custom host, only useful for debugging against non-prod RA
# environments" in its own words, which is what the proxy is (#308 F-EM-07).
# Routed only when hardcore READ as off ("0" -- raofflineproxy-ctl enable
# writes the key), never when it read as nothing: an empty answer is a key
# that could not be read as much as one that is unset, and the proxy
# refuses hardcore awards, so unknown keeps the direct path (#186 PL-31).
#
# Whether the proxy is listening is read from the kernel's socket tables with
# bash's own read, not from netstat, which nothing PPSSPP ships declares and
# whose absence read as "nothing answers" (#308 F-EM-04): 127.0.0.1, 0.0.0.0
# or ::ffff:127.0.0.1 on port 8080 (1F90) in state LISTEN (0A) -- the
# listeners that take the IPv4 connection to 127.0.0.1:8080 PPSSPP is
# given. ::1 does not take it, and :: may be IPv6-only, which the table does
# not say, so neither counts (audit of the fixes, gpt G-D-02, gpt G-F2-02).
# That turns the proxy away never: its sockets are IPv4 (AF_INET in the
# client's proxy_service.py and boot.py), and the scripts suite holds this
# check and raofflineproxy-ctl's to the pinned client's own socket (audit of
# the fix round, claude G2-D-01, PL-033).
# 0 listening, 1 not, 2 when neither table could be read -- said apart in the
# log, since "couldn't tell" is not "nothing there". RAOFFLINEPROXY_PROC_NET
# stands in for /proc/net in the scripts suite, as it does for
# raofflineproxy-ctl listening.
proxy_listening() {
  local proc="${RAOFFLINEPROXY_PROC_NET:-/proc/net}" f readable=0 sl addr rem st rest
  for f in "${proc}/tcp" "${proc}/tcp6"; do
    [ -r "${f}" ] || continue
    readable=1
    while read -r sl addr rem st rest; do
      [ "${st}" = "0A" ] || continue
      case "${addr}" in
        0100007F:1F90|00000000:1F90|0000000000000000FFFF00000100007F:1F90) return 0 ;;
      esac
    done < "${f}"
  done
  [ "${readable}" -eq 1 ] && return 1
  return 2
}

host=""
if [ "$(get_setting "global.retroachievements.offlineproxy")" = 1 ] && [ "${hardcore_raw}" = "0" ]; then
  proxy_listening
  case $? in
    0) host="127.0.0.1:8080" ;;
    1) echo "Offline RetroAchievements is on but nothing is listening on 127.0.0.1:8080; launching direct." >> ${LOG_FILE} ;;
    *) echo "Offline RetroAchievements is on but this device couldn't tell whether the offline service is listening; launching direct." >> ${LOG_FILE} ;;
  esac
fi

# Update emulator config with RetroAchievements settings: the token file
# once, private; the [Achievements] keys as data.
write_private "${PPSSPP_ACHIEVEMENTS}" "${token}"$'\n' \
  || echo "PPSSPP's achievements token file could not be written." >> ${LOG_FILE}
write_section "${PPSSPP_INI}" Achievements "AchievementsEnable=True" "AchievementsUserName=${username}" \
    "AchievementsChallengeMode=${hardcore}" "AchievementsHost=${host}" \
  || echo "PPSSPP's achievements settings could not be written." >> ${LOG_FILE}
