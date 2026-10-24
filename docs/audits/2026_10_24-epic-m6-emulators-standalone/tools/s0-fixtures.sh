#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present pixelelated
#
# s0-fixtures.sh -- T30 stream S0's fixtures (#677, #872: PL-007, PL-008,
# PL-018, PL-019, PL-031). Each case lifts the real lines of one start script
# by marker lines, from a commit or from the worktree, and runs them under the
# GENERIC_X64 image's bash with the image's busybox applets and GNU grep
# borrowed read-only (nothing is started in that tree). The emulator binary is
# replaced by a printer that records its argument vector; a value after
# --ra-password or --ra-token is printed as <set:N>, never itself.
#
#   s0-fixtures.sh <commit|WORKTREE>
#
# Prints one line per case: PASS or FAIL, what was expected, and each stub's
# call count. Exit 0 when every case passes, 1 when one fails, 2 when it cannot
# run (no image root, a marker not found).

set -u
REV=${1:?usage: s0-fixtures.sh <commit|WORKTREE>}
TREE=$(git -C "$(dirname "$0")" rev-parse --show-toplevel) || exit 2
IMG=${QA_SYSTEM_ROOT:-/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64/image/system}
[ -x "${IMG}/usr/bin/bash" ] && [ -x "${IMG}/usr/bin/busybox" ] || { echo "s0-fixtures: no image root at ${IMG}"; exit 2; }
SA=projects/ROCKNIX/packages/emulators/standalone

FX=$(mktemp -d /workspace/tmp/m6-t30/fx-s0.XXXXXX) || exit 2
BIN=${FX}/bin; mkdir -p "${BIN}"
for a in sed awk xargs cat dos2unix tail cut cp mv cmp mkdir ln find wc stat readlink mktemp head tr printf echo basename dirname touch ls; do
  ln -s "${IMG}/usr/bin/busybox" "${BIN}/${a}"
done
ln -s "${IMG}/usr/bin/bash" "${BIN}/bash"; ln -s "${IMG}/usr/bin/grep" "${BIN}/grep"
IBASH=${BIN}/bash

# The printer: one line per argument, the call counted.
cat > "${BIN}/argv_print" <<'EOF'
#!/bin/bash
n=$1; shift
c=$(cat "${FXDIR}/calls.${n}" 2>/dev/null || echo 0); echo $((c + 1)) > "${FXDIR}/calls.${n}"
echo "argc=$#" > "${FXDIR}/argv.${n}"
mask=0
for a in "$@"; do
  if [ $mask = 1 ]; then echo "[<set:${#a}>]"; mask=0; else echo "[${a}]"; fi
  case "$a" in --ra-password|--ra-token) mask=1;; esac
done >> "${FXDIR}/argv.${n}"
EOF
chmod +x "${BIN}/argv_print"

src() { # the script's text at REV
  if [ "${REV}" = WORKTREE ]; then cat "${TREE}/$1"; else git -C "${TREE}" show "${REV}:$1"; fi
}
lift() { # path start-ERE end-ERE: the lines between the first start and the next end, inclusive
  local out
  out=$(src "$1" | LS="$2" LE="$3" awk 'f==0 && $0 ~ ENVIRON["LS"] {f=1} f==1 {print} f==1 && $0 ~ ENVIRON["LE"] {exit}')
  [ -n "${out}" ] || { echo "s0-fixtures: marker /$2/ not found in $1 at ${REV}" >&2; exit 2; }
  printf '%s\n' "${out}"
}
FAILS=0
verdict() { # case-name ok(0/1) expected stubs...
  local name=$1 ok=$2 exp=$3; shift 3
  local counts="" s
  for s in "$@"; do counts+=" ${s}=$(cat "${FX}/calls.${s}" 2>/dev/null || echo 0)"; done
  if [ "${ok}" = 0 ]; then echo "PASS ${name}: ${exp} (calls:${counts})"; else echo "FAIL ${name}: ${exp} (calls:${counts})"; FAILS=$((FAILS + 1)); fi
}
run() { # case-dir script-file: run under the image's bash, env cleared but for PATH and FXDIR
  env -i PATH="${BIN}" FXDIR="${FX}" HOME="${FX}/home" "${IBASH}" "$2" "${@:3}" > "$1/out" 2>&1
}
argv() { cat "${FX}/argv.$1" 2>/dev/null; }
reset() { local f; for f in "${FX}"/calls.*; do [ -e "$f" ] && echo 0 > "$f"; done; for f in "${FX}"/argv.*; do [ -e "$f" ] && : > "$f"; done; }

# ---- gopher64 (PL-019, #865): the password's slot ----
G=${SA}/gopher64-sa/scripts/start_gopher64.sh
GL=$(lift "$G" '^# Cheevos' '/usr/bin/gopher64 --fullscreen') || exit 2
gcase() { # name enabled user password tokenfile(yes/no) check
  local d="${FX}/g-$1"; mkdir -p "$d/home/.config/gopher64"
  reset
  [ "$5" = yes ] && printf '{\n  "username": "%s",\n  "token": "T0kenSynth3tic",\n  "enabled": true\n}\n' "$3" > "$d/home/.config/gopher64/retroachievements.json"
  {
    echo "get_setting() { case \"\$1\" in global.retroachievements) echo '$2';; global.retroachievements.username) echo '$3';; global.retroachievements.password) echo '$4';; esac; }"
    echo "CONF_DIR='$d/home/.config/gopher64'; GOPHER64_JSON=config.json; EMUPERF=''"
    printf '%s\n' "${GL}" | sed -e "s#/var/log/cheevos.log#$d/cheevos.log#g" -e 's#/usr/bin/gopher64 --fullscreen#argv_print gopher64 --fullscreen#'
  } > "$d/s.sh"
  run "$d" "$d/s.sh" "/storage/roms/n64/Wave Race.z64"
}
gcase empty-password 1 synthuser "" no
A=$(argv gopher64); { ! grep -qx '\[--ra-password\]' <<<"$A" && [ "$(tail -1 <<<"$A")" = "[/storage/roms/n64/Wave Race.z64]" ]; }; verdict gopher64-empty-password $? "no --ra-password and the ROM in its own slot, last" gopher64
gcase spaced-password 1 synthuser "pa ss" no
A=$(argv gopher64); { grep -qx 'argc=10' <<<"$A" && grep -A1 -x '\[--ra-password\]' <<<"$A" | grep -qx '\[<set:5>\]'; }; verdict gopher64-spaced-password $? "argc 10, the password one argument of 5 bytes" gopher64
gcase token-file 1 synthuser "pass" yes
A=$(argv gopher64); { grep -qx '\[--ra-token\]' <<<"$A" && ! grep -qx '\[--ra-password\]' <<<"$A"; }; verdict gopher64-token-file $? "gopher64's own token used, no password" gopher64
gcase disabled 0 synthuser "pass" no
A=$(argv gopher64); { grep -qx 'argc=6' <<<"$A" && ! grep -q -- '--ra-' <<<"$A"; }; verdict gopher64-disabled $? "argc 6, no --ra- argument" gopher64

# ---- Steam (PL-031, #871): the URI and -silent ----
S=${SA}/steam/scripts/start_steam.sh
SD=$(lift "$S" 'if \[\[ "\$1" == \*\.desktop' '^  fi$') || exit 2
SX=$(src "$S" | grep -m1 'FEX /usr/bin/steam -nobigpicture') || { echo "s0-fixtures: Steam's x86 launch line not found"; exit 2; }
SA64=$(src "$S" | grep -m1 'steamrtarm64/steam -deckard') || { echo "s0-fixtures: Steam's arm64 launch line not found"; exit 2; }
scase() { # name desktop-file-content (empty: Steam.desktop)
  local d="${FX}/s-$1"; mkdir -p "$d"; reset
  local f="$d/Game.desktop"; [ -z "$2" ] && f="$d/Steam.desktop"
  printf '%s\n' "${2:-Exec=steam}" > "$f"
  {
    echo 'f() {'
    echo '  local game_uri="" game_args=()'
    printf '%s\n' "${SD}"
    printf '%s\n' "${SX}" | sed -e 's#^ *FEX /usr/bin/steam#argv_print steamx86#'
    printf '%s\n' "${SA64}" | sed -e 's#^ */storage/.local/share/Steam/steamrtarm64/steam#argv_print steamarm64#'
    echo '}'
    echo 'f "$@"'
  } > "$d/s.sh"
  run "$d" "$d/s.sh" "$f"
}
scase game 'Exec=steam steam://rungameid/570'
X=$(argv steamx86); Y=$(argv steamarm64)
{ grep -A2 -x '\[-noshaders\]' <<<"$X" | sed -n 2,3p | tr '\n' ' ' | grep -qx '\[steam://rungameid/570\] \[-silent\] ' && grep -A2 -x '\[-noshaders\]' <<<"$Y" | sed -n 2,3p | tr '\n' ' ' | grep -qx '\[steam://rungameid/570\] \[-silent\] '; }
verdict steam-game-uri $? "the URI and -silent two arguments on both launch lines" steamx86 steamarm64
scase client ''
X=$(argv steamx86); [ "$(tail -1 <<<"$X")" = "[-noshaders]" ]; verdict steam-client $? "Steam.desktop: nothing after -noshaders" steamx86

# ---- yabasanshiro (PL-018, #871): the pad's name ----
Y=${SA}/yabasanshiro-sa/scripts/start_yabasanshiro.sh
YL=$(lift "$Y" 'Handle inputplumber platforms first' 'MAPPING_FILE=') || exit 2
ycase() { # name device-name
  local d="${FX}/y-$1"; mkdir -p "$d"; reset
  printf 'I: Bus=0003\nN: Name="%s"\nH: Handlers=event3 js0\n' "$2" > "$d/devices"
  {
    echo "xmlstarlet() { c=\$(cat \"\${FXDIR}/calls.xmlstarlet\" 2>/dev/null || echo 0); echo \$((c + 1)) > \"\${FXDIR}/calls.xmlstarlet\"; }"
    echo "HW_DEVICE=H700"
    printf '%s\n' "${YL}" | sed -e "s#/proc/bus/input/devices#$d/devices#g" -e "s#/storage/.emulationstation/es_input.cfg#$d/es_input.cfg#g"
    echo 'printf "%s\n" "${MAPPING_FILE}" > "${FXDIR}/mapping"'
  } > "$d/s.sh"
  ( cd "$d" && run "$d" "$d/s.sh" )
}
MARK=${FX}/y-marker
ycase crafted "Pad'; touch ${MARK}; '"
[ ! -e "${MARK}" ] && [ "$(cat "${FX}/mapping")" = "/usr/config/yabasanshiro/devices/keymapv2_Pad'; touch ${MARK}; '.json" ]
verdict yabasanshiro-crafted-name $? "no marker; the mapping file named after the pad's whole name" xmlstarlet
ycase plain "Microsoft X-Box 360 pad"
[ "$(cat "${FX}/mapping")" = "/usr/config/yabasanshiro/devices/keymapv2_Microsoft X-Box 360 pad.json" ]
verdict yabasanshiro-plain-name $? "keymapv2_Microsoft X-Box 360 pad.json, as before" xmlstarlet

# ---- gzdoom (PL-008, #860): a WAD path and a .doom file's values ----
Z=${SA}/gzdoom-sa/scripts/start_gzdoom.sh
ZL=$(lift "$Z" '^params=' '^#Set the cores') || exit 2
ZX=$(src "$Z" | grep -m1 '/usr/bin/gzdoom') || { echo "s0-fixtures: gzdoom's launch line not found"; exit 2; }
zcase() { # name rom
  local d="${FX}/z-$1"; mkdir -p "$d"; reset
  {
    echo "CONFIG=/storage/.config/gzdoom/gzdoom.ini; SAVE_DIR=/storage/roms/gzdoom; VSYNC=true; EMUPERF=''"
    printf '%s\n' "${ZL}"
    printf '%s\n' "${ZX}" | sed -e 's#/usr/bin/gzdoom#argv_print gzdoom#' -e "s#/var/log/gzdoom.log#$d/gzdoom.log#"
  } > "$d/s.sh"
  run "$d" "$d/s.sh" "$2"
}
mkdir -p "${FX}/doom"; W="${FX}/doom/Free Doom's Gate.wad"; : > "$W"
zcase apostrophe "$W"
A=$(argv gzdoom); grep -A1 -x '\[-iwad\]' <<<"$A" | grep -qxF "[${W}]"; verdict gzdoom-apostrophe $? "-iwad and the whole path, one argument" gzdoom
zcase plain "${FX}/doom/freedoom1.wad"
A=$(argv gzdoom); grep -A1 -x '\[-iwad\]' <<<"$A" | grep -qxF "[${FX}/doom/freedoom1.wad]"; verdict gzdoom-plain $? "-iwad and the path" gzdoom
: > "${FX}/doom/a b.pk3"
printf 'IWAD=%s\nMOD=%s\nMOD=%s %s\nSAVEDIR=%s\n' "${FX}/doom/freedoom2.wad" "${FX}/doom/a b.pk3" "${FX}/doom/m1.pk3" "${FX}/doom/m2.pk3" "${FX}/doom/sv" > "${FX}/doom/game.doom"
zcase doomfile "${FX}/doom/game.doom"
A=$(argv gzdoom)
{ grep -qxF "[${FX}/doom/a b.pk3]" <<<"$A" && grep -qxF "[${FX}/doom/m1.pk3]" <<<"$A" && grep -qxF "[${FX}/doom/m2.pk3]" <<<"$A" && grep -A1 -x '\[-savedir\]' <<<"$A" | grep -qxF "[${FX}/doom/sv]" && grep -A1 -x '\[-iwad\]' <<<"$A" | grep -qxF "[${FX}/doom/freedoom2.wad]"; }
verdict gzdoom-doom-file $? "an existing path with a space one argument, two listed paths two, SAVEDIR replacing -savedir" gzdoom

# ---- ScummVM (PL-007, #859): the .scummvm file is data ----
V=${SA}/scummvm-sa/scripts/start_scummvm.sh
VL=$(lift "$V" 'set_kill set "-9 scummvm"' 'systemctl stop fluidsynth') || exit 2
vcase() { # name content
  local d="${FX}/v-$1"; mkdir -p "$d"; reset
  printf '%s\n' "$2" > "$d/game.scummvm"
  {
    echo 'set_kill() { :; }; systemctl() { :; }'
    echo "GAME='$d/game.scummvm'"
    printf '%s\n' "${VL}" | sed -e 's#/usr/bin/scummvm#argv_print scummvm#'
  } > "$d/s.sh"
  run "$d" "$d/s.sh"
}
VM=${FX}/v-marker
vcase crafted "--path=\"/storage/roms/scummvm/x\" id; touch ${VM}"
[ ! -e "${VM}" ]; verdict scummvm-crafted $? "no marker" scummvm
vcase plain '--path="/storage/roms/scummvm/Flight of the Amazon Queen" queen'
A=$(argv scummvm); { [ "$(tail -2 <<<"$A" | tr '\n' ' ')" = "[--path=/storage/roms/scummvm/Flight of the Amazon Queen] [queen] " ]; }
verdict scummvm-plain $? "--path=<dir with spaces> and queen, two arguments" scummvm
vcase target-only 'queen'
A=$(argv scummvm); [ "$(tail -1 <<<"$A")" = "[queen]" ]; verdict scummvm-target-only $? "a bare target id is the last argument" scummvm

echo "s0-fixtures: ${REV}: failures ${FAILS}; image root ${IMG}; fixture dir ${FX}"
[ "${FAILS}" = 0 ]
