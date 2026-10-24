#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
#
# s3-fixtures.sh -- T30 stream S3's fixtures (#677, #872: PL-009, PL-010,
# PL-020, PL-021, PL-039). Runs the achievements scripts whole, from a commit
# or the worktree, under the GENERIC_X64 image's bash, GNU grep and busybox
# applets borrowed read-only. get_setting answers from a fixture file; /storage
# and /var/log are rewritten to a fixture root. Every sign-in value is
# SYNTHETIC; a check counts lines and never prints a value.
#
#   s3-fixtures.sh <commit|WORKTREE>
#
# Exit 0 all pass, 1 a failure, 2 cannot run.

set -u
REV=${1:?usage: s3-fixtures.sh <commit|WORKTREE>}
TREE=$(git -C "$(dirname "$0")" rev-parse --show-toplevel) || exit 2
IMG=${QA_SYSTEM_ROOT:-/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64/image/system}
[ -x "${IMG}/usr/bin/bash" ] && [ -x "${IMG}/usr/bin/busybox" ] || { echo "s3-fixtures: no image root at ${IMG}"; exit 2; }
SA=projects/ROCKNIX/packages/emulators/standalone

FX=$(mktemp -d /workspace/tmp/m6-t30/fx-s3.XXXXXX) || exit 2
BIN=${FX}/bin; mkdir -p "${BIN}"
for a in sed awk cat cp mv mkdir ln find wc readlink dirname basename rm head tail tr touch ls chmod stat printf echo cut date env; do
  ln -s "${IMG}/usr/bin/busybox" "${BIN}/${a}"
done
ln -s "${IMG}/usr/bin/bash" "${BIN}/bash"; ln -s "${IMG}/usr/bin/grep" "${BIN}/grep"; IBASH=${BIN}/bash
# mktemp is counted, so "written once, by temp and rename" can be read.
printf '#!%s\necho "$*" >> %s/mktemp.log\nexec %s mktemp "$@"\n' "${IBASH}" "${FX}" "${IMG}/usr/bin/busybox" > "${BIN}/mktemp"; chmod +x "${BIN}/mktemp"

src() { if [ "${REV}" = WORKTREE ]; then cat "${TREE}/$1"; else git -C "${TREE}" show "${REV}:$1" 2>/dev/null; fi; }
OLD='0LDsynthTOKENxyz'          # a previous session's token (synthetic)
NEWT='N3w/syn&th\tok'           # a new token holding / & and a backslash (synthetic)
FAILS=0
verdict() { local name=$1 ok=$2 exp=$3 extra=${4:-}
  if [ "${ok}" = 0 ]; then echo "PASS ${name}: ${exp}${extra:+ (${extra})}"; else echo "FAIL ${name}: ${exp}${extra:+ (${extra})}"; FAILS=$((FAILS + 1)); fi; }
# run <case> <script> <settings...>: settings as key=value, an absent key reads empty
run() {
  local c=$1 s=$2 R="${FX}/$1"; shift 2
  mkdir -p "$R/var/log"; : > "${FX}/mktemp.log"
  printf '%s\n' "$@" > "$R/settings"
  { echo "get_setting() { local l; while IFS= read -r l; do [ \"\${l%%=*}\" = \"\$1\" ] && { printf '%s\\n' \"\${l#*=}\"; return; }; done < '$R/settings'; }"
    src "$s" | sed -e '/^\. \/etc\/profile/d' -e "s#/storage#$R/storage#g" -e "s#/var/log#$R/var/log#g"
  } > "$R/s.sh"
  ( cd "$R" && umask 022 && env -i PATH="${BIN}" HOME="$R/storage" "${IBASH}" "$R/s.sh" > "$R/out" 2>&1 ); echo $? > "$R/rc"
}
rc() { cat "${FX}/$1/rc"; }
old_lines() { grep -r -c -F "${OLD}" "$@" 2>/dev/null | awk -F: '{s += $NF} END {print s + 0}'; }

# ---- PPSSPP ----
P=${SA}/ppsspp-sa/scripts/cheevos_ppsspp.sh
pseed() { local R="${FX}/$1/storage/.config/ppsspp/PSP/SYSTEM"; mkdir -p "$R"
  printf '[General]\nLanguage = en_US\n[Achievements]\nAchievementsEnable = True\nAchievementsUserName = olduser\nAchievementsSoundEffects = True\n[Graphics]\nFrameSkip = 0\n' > "$R/ppsspp.ini"
  printf '%s\n' "${OLD}" > "$R/ppsspp_retroachievements.dat"; }
pseed p-empty; run p-empty "$P" global.retroachievements=1 global.retroachievements.username=synthuser
R=${FX}/p-empty/storage/.config/ppsspp/PSP/SYSTEM
{ [ "$(rc p-empty)" = 1 ] && [ "$(old_lines "$R")" = 0 ] && grep -qx 'AchievementsEnable = False' "$R/ppsspp.ini" && grep -qx 'AchievementsSoundEffects = True' "$R/ppsspp.ini" && grep -qx 'FrameSkip = 0' "$R/ppsspp.ini"; }
verdict ppsspp-token-empty $? "switch on, token empty: rc 1, 0 old-token lines, AchievementsEnable = False, the other keys and sections kept" "old-token lines $(old_lines "$R")"
pseed p-off; run p-off "$P" global.retroachievements=0
R=${FX}/p-off/storage/.config/ppsspp/PSP/SYSTEM
{ [ "$(rc p-off)" = 1 ] && [ "$(old_lines "$R")" = 0 ] && grep -qx 'AchievementsEnable = False' "$R/ppsspp.ini"; }
verdict ppsspp-off $? "switch off: rc 1, 0 old-token lines, disabled" "old-token lines $(old_lines "$R")"
pseed p-new; run p-new "$P" global.retroachievements=1 global.retroachievements.username=synthuser "global.retroachievements.token=${NEWT}" global.retroachievements.hardcore=0
R=${FX}/p-new/storage/.config/ppsspp/PSP/SYSTEM
mode=$(stat -c %a "$R/ppsspp_retroachievements.dat" 2>/dev/null); writes=$(grep -c 'ppsspp_retroachievements.dat' "${FX}/mktemp.log")
{ [ "$(rc p-new)" = 0 ] && [ "$(cat "$R/ppsspp_retroachievements.dat")" = "${NEWT}" ] && [ "${mode}" = 600 ] && [ "${writes}" = 1 ] && grep -qx 'AchievementsEnable = True' "$R/ppsspp.ini" && grep -qx 'AchievementsUserName = synthuser' "$R/ppsspp.ini" && grep -qx 'AchievementsSoundEffects = True' "$R/ppsspp.ini"; }
verdict ppsspp-new-token $? "the token file holds the token byte for byte, mode 0600, written once by temp and rename; the section's keys set, the others kept" "mode ${mode}, temp writes ${writes}"

# ---- flycast ----
F=${SA}/flycast-sa/scripts/cheevos_flycast.sh
fseed() { local R="${FX}/$1/storage/.config/flycast"; mkdir -p "$R"
  printf '[config]\nDynarec.Enabled = yes\n[achievements]\nEnabled = yes\nHardcoreMode = false\nUserName = olduser\nToken = %s\n\n[input]\nMouseSensitivity = 100\n' "${OLD}" > "$R/emu.cfg"; }
fseed f-empty; run f-empty "$F" global.retroachievements=1 global.retroachievements.username=synthuser
R=${FX}/f-empty/storage/.config/flycast
{ [ "$(rc f-empty)" = 1 ] && [ "$(old_lines "$R")" = 0 ] && grep -qx 'Enabled = no' "$R/emu.cfg" && grep -qx 'MouseSensitivity = 100' "$R/emu.cfg"; }
verdict flycast-token-empty $? "switch on, token empty: rc 1, 0 old-token lines, Enabled = no, the other sections kept" "old-token lines $(old_lines "$R")"
fseed f-unset; run f-unset "$F" global.retroachievements.username=synthuser
R=${FX}/f-unset/storage/.config/flycast
{ [ "$(rc f-unset)" = 1 ] && [ "$(old_lines "$R")" = 0 ] && grep -qx 'Enabled = no' "$R/emu.cfg"; }
verdict flycast-switch-unset $? "the switch key unset: the disabled branch, rc 1" "rc $(rc f-unset)"
fseed f-new; run f-new "$F" global.retroachievements=1 global.retroachievements.username=synthuser "global.retroachievements.token=${NEWT}"
R=${FX}/f-new/storage/.config/flycast
{ [ "$(rc f-new)" = 0 ] && grep -qxF "Token = ${NEWT}" "$R/emu.cfg" && grep -qx 'Enabled = yes' "$R/emu.cfg" && grep -qx 'MouseSensitivity = 100' "$R/emu.cfg"; }
verdict flycast-new-token $? "a token holding / & and a backslash written byte for byte, Enabled = yes, the other sections kept"

# ---- ARMSX2 ----
A=${SA}/armsx2-sa/scripts/cheevos_armsx2.sh
aseed() { local R="${FX}/$1/storage/.config/ARMSX2/inis"; mkdir -p "$R"
  printf '[EmuCore]\nEnableCheats = false\n[Achievements]\nEnabled = true\nUsername = olduser\nChallengeMode = false\n' > "$R/PCSX2.ini"
  printf '[Achievements]\nToken = %s\n' "${OLD}" > "$R/secrets.ini"; }
aseed a-empty; run a-empty "$A" global.retroachievements=1 global.retroachievements.username=synthuser
R=${FX}/a-empty/storage/.config/ARMSX2/inis
{ [ "$(rc a-empty)" = 1 ] && [ "$(old_lines "$R")" = 0 ] && grep -qx 'Enabled = false' "$R/PCSX2.ini" && grep -qx 'EnableCheats = false' "$R/PCSX2.ini"; }
verdict armsx2-token-empty $? "switch on, token empty: rc 1, 0 old-token lines (PCSX2.ini and secrets.ini), Enabled = false" "old-token lines $(old_lines "$R")"
aseed a-unset; run a-unset "$A" global.retroachievements.username=synthuser
R=${FX}/a-unset/storage/.config/ARMSX2/inis
{ [ "$(rc a-unset)" = 1 ] && grep -qx 'Enabled = false' "$R/PCSX2.ini"; }
verdict armsx2-switch-unset $? "the switch key unset: the disabled branch, rc 1" "rc $(rc a-unset)"
R0=${FX}/a-first/storage/.config/ARMSX2/inis; mkdir -p "$R0"; printf '[EmuCore]\nEnableCheats = false\n' > "$R0/PCSX2.ini"
run a-first "$A" global.retroachievements=1 global.retroachievements.username=synthuser "global.retroachievements.token=${NEWT}" global.retroachievements.encore=1 global.retroachievements.leaderboards=1 global.retroachievements.unofficial=0
{ [ "$(rc a-first)" = 0 ] && grep -qxF "Token = ${NEWT}" "$R0/secrets.ini" && grep -qx 'EncoreMode = true' "$R0/PCSX2.ini" && grep -qx 'LeaderboardNotifications = true' "$R0/PCSX2.ini" && grep -qx 'UnofficialTestMode = false' "$R0/PCSX2.ini"; }
verdict armsx2-first-section $? "a first section carries EncoreMode, LeaderboardNotifications and UnofficialTestMode; the token byte for byte in secrets.ini"

# ---- SkyEmu ----
K=${SA}/skyemu-sa/scripts/cheevos_skyemu.sh
kseed() { local R="${FX}/$1/storage/.config/SkyEmu"; mkdir -p "$R"; printf 'olduser\n%s\n' "${OLD}" > "$R/ra_token.txt"; }
kseed k-empty; run k-empty "$K" global.retroachievements=1 global.retroachievements.username=synthuser
R=${FX}/k-empty/storage/.config/SkyEmu
{ [ "$(rc k-empty)" = 1 ] && [ "$(old_lines "$R")" = 0 ]; }
verdict skyemu-token-empty $? "switch on, token empty: rc 1, 0 old-token lines in ra_token.txt" "old-token lines $(old_lines "$R")"
kseed k-off; run k-off "$K" global.retroachievements=0
R=${FX}/k-off/storage/.config/SkyEmu
{ [ "$(rc k-off)" = 1 ] && [ "$(old_lines "$R")" = 0 ]; }
verdict skyemu-off $? "switch off: rc 1, 0 old-token lines" "old-token lines $(old_lines "$R")"
kseed k-new; run k-new "$K" global.retroachievements=1 global.retroachievements.username=synthuser "global.retroachievements.token=${NEWT}"
R=${FX}/k-new/storage/.config/SkyEmu; mode=$(stat -c %a "$R/ra_token.txt" 2>/dev/null)
{ [ "$(rc k-new)" = 0 ] && [ "$(sed -n 2p "$R/ra_token.txt")" = "${NEWT}" ] && [ "${mode}" = 600 ]; }
verdict skyemu-new-token $? "ra_token.txt holds the user and the token byte for byte, mode 0600" "mode ${mode}"

# ---- DuckStation's achievements script (S5 may remove it): the quoted test ----
D=${SA}/duckstation-sa/scripts/cheevos_duckstation.sh
if [ -z "$(src "$D")" ]; then
  echo "SKIP duckstation-switch-unset: cheevos_duckstation.sh is not in this tree (removed in S5 as dead, #872 PL-024)"
else
mkdir -p "${FX}/d-unset/storage/.config/duckstation"; printf '[Cheevos]\nEnabled = true\n\n' > "${FX}/d-unset/storage/.config/duckstation/settings.ini"
run d-unset "$D" global.retroachievements.username=synthuser
{ [ "$(rc d-unset)" = 1 ] && grep -q 'not enabled' "${FX}/d-unset/var/log/cheevos.log" && grep -qx 'Enabled = false' "${FX}/d-unset/storage/.config/duckstation/settings.ini"; }
verdict duckstation-switch-unset $? "the switch key unset: the disabled branch (its log line, Enabled = false), rc 1" "rc $(rc d-unset)"
fi

# ---- melonDS's set_key (PL-020): | and \ as data, on both paths ----
M=${SA}/melonds-sa/scripts/cheevos_melonds.sh
mcase() { # name seed-has-keys(yes/no)
  local R="${FX}/m-$1"; mkdir -p "$R/storage/.config/melonDS"
  [ "$2" = yes ] && printf 'RA_Enabled=0\nRA_Token=%s\nRA_Password=oldpw\nScreenSwap=0\n' "${OLD}" > "$R/storage/.config/melonDS/melonDS.ini"
  [ "$2" = yes ] || printf 'ScreenSwap=0\n' > "$R/storage/.config/melonDS/melonDS.ini"
  run "m-$1" "$M" global.retroachievements=1 global.retroachievements.username=synthuser "global.retroachievements.token=N3w|syn&th\\tok/x" 'global.retroachievements.password=p|w\d&/z'
  local I="$R/storage/.config/melonDS/melonDS.ini"
  { grep -qxF 'RA_Token=N3w|syn&th\tok/x' "$I" && grep -qxF 'RA_Password=p|w\d&/z' "$I" && grep -qx 'ScreenSwap=0' "$I" && [ "$(old_lines "$R/storage")" = 0 ]; }
  verdict "melonds-set-key-$1" $? "values holding | \\ & and / written byte for byte ($([ "$2" = yes ] && echo 'keys present: the replace path' || echo 'keys absent: the append path'))"
}
mcase replace yes
mcase append no

echo "s3-fixtures: ${REV}: failures ${FAILS}; image root ${IMG}; fixture dir ${FX}"
[ "${FAILS}" = 0 ]
