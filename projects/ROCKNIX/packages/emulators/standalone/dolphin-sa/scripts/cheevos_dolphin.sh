#! /bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)

. /etc/profile

LOG_FILE="/var/log/cheevos.log"

# Extract username, password, token, if enabled, and hardcore mode from system.cfg
username=$(get_setting "global.retroachievements.username")
password=$(get_setting "global.retroachievements.password")
token=$(get_setting "global.retroachievements.token")
enabled=$(get_setting "global.retroachievements")
hardcore=$(get_setting "global.retroachievements.hardcore")
encore=$(get_setting "global.retroachievements.encore")
unofficial=$(get_setting "global.retroachievements.unofficial")
[ -z "${unofficial}" ] && unofficial=$(get_setting "global.retroachievements.testunofficial")  # the spelling before 2026-09; EmulationStation writes .unofficial
hosturl=$(get_setting "global.retroachievements.customhost")

# Publish the generated session as one file so disabling or signing out cannot
# reuse an earlier active session. Saved ES account settings are read-only here.
INI_FILE="/storage/.config/dolphin-emu/RetroAchievements.ini"
temporary=""
trap '[ -z "${temporary}" ] || rm -f -- "${temporary}"' EXIT

settings_failed() {
  echo "Dolphin achievements settings could not be written; refusing launch." >> "${LOG_FILE}"
  local language="${LANGUAGE:-${LC_ALL:-${LC_MESSAGES:-${LANG:-en}}}}"
  language="${language,,}"
  local title="DOLPHIN DID NOT START"
  local message="Achievements settings could not be updated. Check the game storage and folder permissions, then try again."
  case "${language}" in
    fr|fr_*|fr-*|fr.*|fr@*|fr:*)
      title="DOLPHIN N’A PAS DÉMARRÉ"
      message="Les paramètres des succès n’ont pas pu être mis à jour. Vérifiez le stockage des jeux et les permissions des dossiers, puis réessayez."
      ;;
  esac
  printf 'DOLPHIN DID NOT START\n%s\n\n%s\n' "${title}" "${message}" > /tmp/launch_error.log
  exit 250
}

publish_settings() {
  temporary=$(umask 077; mktemp "${INI_FILE}.XXXXXX") || return 1
  if ! cat > "${temporary}" <<EOF
[Achievements]
DiscordPresenceEnabled = False
Enabled = ${enabled}
EncoreEnabled = ${encore}
HardcoreEnabled = ${hardcore}
ProgressEnabled = False
SpectatorEnabled = False
UnofficialEnabled = ${unofficial}
Username = ${username}
ApiToken = ${token}
HostUrl = ${hosturl}
EOF
  then
    return 1
  fi
  # -T refuses a destination directory instead of moving a token file into it.
  mv -fT -- "${temporary}" "${INI_FILE}" || return 1
  temporary=""
}

publish_disabled() {
  enabled="False"
  encore="False"
  hardcore="False"
  unofficial="False"
  username=""
  token=""
  hosturl=""
  publish_settings || settings_failed
}

# Check if RetroAchievements are enabled in Emulation Station
if [ "${enabled}" = 1 ]; then
  enabled="True"
else
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

# Set encore mode
if [ "${encore}" = 1 ]; then
  encore="True"
else
  encore="False"
fi

# Set unofficial mode
if [ "${unofficial}" = 1 ]; then
  unofficial="True"
else
  unofficial="False"
fi

# The offline toggle routes only a known casual session to a listening proxy
# (#584, D-RA-002). Keep the configured custom host for every fallback; never
# change saved settings or credentials here. An empty/unknown hardcore read
# is not permission to use a service that cannot queue hardcore awards.
# Dolphin2606 passes HostUrl to rc_client_set_host; its bundled rcheevos adds
# http:// to a host without a scheme. The bare host below therefore uses HTTP.
# Match PPSSPP's read-only IPv4-capable listener check (0 listening, 1 absent,
# 2 unreadable). A listening socket is not proof of proxy identity or readiness.
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

if [ "$(get_setting "global.retroachievements.offlineproxy")" = 1 ] && [ "${hardcore_raw}" = "0" ]; then
  proxy_listening
  case $? in
    0) hosturl="127.0.0.1:8080" ;;
    1) echo "Offline RetroAchievements is on but nothing is listening on 127.0.0.1:8080; keeping the configured achievements host." >> "${LOG_FILE}" ;;
    *) echo "Offline RetroAchievements is on but the listener tables could not be read; keeping the configured achievements host." >> "${LOG_FILE}" ;;
  esac
fi

publish_settings || settings_failed
