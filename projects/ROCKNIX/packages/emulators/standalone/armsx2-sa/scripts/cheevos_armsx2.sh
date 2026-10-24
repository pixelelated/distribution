#! /bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)

. /etc/profile

ARMSX2_CFG="/storage/.config/ARMSX2/inis/PCSX2.ini"
ARMSX2_TOKEN="/storage/.config/ARMSX2/inis/secrets.ini"
LOG_FILE="/var/log/cheevos.log"

# Extract username, password, token, if enabled, and hardcore mode from system.cfg
username=$(get_setting "global.retroachievements.username")
password=$(get_setting "global.retroachievements.password")
token=$(get_setting "global.retroachievements.token")
enabled=$(get_setting "global.retroachievements")
hardcore=$(get_setting "global.retroachievements.hardcore")
encore=$(get_setting "global.retroachievements.encore")
leaderboards=$(get_setting "global.retroachievements.leaderboards")
unofficial=$(get_setting "global.retroachievements.unofficial")

# Convert values from 0/1 to true/false
to_bool() { [ "${1}" = "1" ] && echo "true" || echo "false"; }
hardcore=$(to_bool "${hardcore}")
encore=$(to_bool "${encore}")
leaderboards=$(to_bool "${leaderboards}")
unofficial=$(to_bool "${unofficial}")

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

# The token lives in secrets.ini, whatever PCSX2.ini holds (fork #170: testing
# PCSX2.ini never matched, and a Token line was appended at every launch). One
# [Achievements] section holding one Token line, whatever the file held
# before: the shipped seed's bare "Token =" (no value, no trailing space); the
# lines a pre-#170 image appended at every launch; a second [Achievements]
# header, which that image's no-section branch appended to a file that
# already had one -- a delete bounded by the next "[" line stopped at that
# header and never reached the Token lines under it, and the insert then put
# one after every header (#308 F-EM-03); an empty file, where sed's "$a" has
# no last line to append after, and no file at all (#308 F-EM-05, F-EM-09).
# ARMSX2 reads the first Token line of the section, so duplicates were
# harmless; they were still wrong, and an empty file launched logged out.
#
# So the file is rewritten whole, by one awk that reads it twice: the first
# pass keeps every line of every [Achievements] section but its header and
# Token lines; the second writes the file with the first such section
# holding the one Token and those lines, the later [Achievements] sections
# dropped (their lines already written) and every other line as it was; a
# file with no section, or no lines, gains the section. To a temp file with
# the owner's permissions only, then renamed over the old one, so a launch
# killed part-way leaves the file as it was.
write_token() { # token (empty clears it)
  mkdir -p "${ARMSX2_TOKEN%/*}"
  [ -e "${ARMSX2_TOKEN}" ] || : > "${ARMSX2_TOKEN}"
  ARMSX2_TOKEN_TMP="${ARMSX2_TOKEN}.tmp.$$"
  if ( umask 077; TOKEN="${1}" awk '
      FNR == 1 { pass++; section = 0 }
      /^\[/ { section = ($0 ~ /^\[Achievements\][[:space:]]*$/) }
      pass == 1 { if (section && $0 !~ /^\[/ && $0 !~ /^Token[[:space:]]*=/) keep[++kept] = $0; next }
      section {
          if (!written && $0 ~ /^\[/) {
              print "[Achievements]"; print "Token = " ENVIRON["TOKEN"]
              for (i = 1; i <= kept; i++) print keep[i]
              written = 1
          }
          next
      }
      { print }
      END { if (!written) { print "[Achievements]"; print "Token = " ENVIRON["TOKEN"] } }
  ' "${ARMSX2_TOKEN}" "${ARMSX2_TOKEN}" > "${ARMSX2_TOKEN_TMP}" ) && [ -s "${ARMSX2_TOKEN_TMP}" ] \
      && mv -f "${ARMSX2_TOKEN_TMP}" "${ARMSX2_TOKEN}"; then
      :
  else
      # The rewrite, the check and the rename are one operation: whichever
      # fails, the temp goes and secrets.ini is as it was (audit of the
      # fixes, gpt G-F2-07: the rename sat outside this branch).
      rm -f "${ARMSX2_TOKEN_TMP}"
      echo "ARMSX2's secrets.ini could not be rewritten; its token was left as it was." >> ${LOG_FILE}
  fi
}

# Off, or on with no token: publish a disabled session -- the flag off, the
# user and the token cleared -- so the previous account is not signed in (#861).
publish_disabled() {
  write_section "${ARMSX2_CFG}" Achievements "Enabled=false" "Username=" \
    || echo "ARMSX2's achievements settings could not be written." >> ${LOG_FILE}
  write_token ""
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

# Update emulator config with RetroAchievements settings, as data: every
# key, a first section included (#870), then the token in secrets.ini.
datets=$(date +%s%N | cut -b1-13)
write_section "${ARMSX2_CFG}" Achievements "Enabled=true" "Username=${username}" "ChallengeMode=${hardcore}" \
    "EncoreMode=${encore}" "LeaderboardNotifications=${leaderboards}" "UnofficialTestMode=${unofficial}" "LoginTimestamp=${datets}" \
  || echo "ARMSX2's achievements settings could not be written." >> ${LOG_FILE}
write_token "${token}"
