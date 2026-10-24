#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
#
# s4-fixtures.sh -- T30 stream S4's fixtures (#677, #872: PL-006, PL-011,
# PL-014b, PL-015, PL-017, PL-028, PL-032, PL-033, PL-038, PL-041). Each case
# runs a start script whole, or its lines lifted by marker, from a commit or
# the worktree, under the GENERIC_X64 image's bash, GNU grep and busybox
# applets borrowed read-only, with /storage, /usr/config, /usr/local/share and
# /tmp rewritten to a fixture root and the emulators replaced by a printer of
# their argument vector. Inputs are synthetic. One-line checks on the tree are
# marked [tree].
#
#   s4-fixtures.sh <commit|WORKTREE>
#
# Exit 0 all pass, 1 a failure, 2 cannot run.

set -u
REV=${1:?usage: s4-fixtures.sh <commit|WORKTREE>}
TREE=$(git -C "$(dirname "$0")" rev-parse --show-toplevel) || exit 2
IMG=${QA_SYSTEM_ROOT:-/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64/image/system}
[ -x "${IMG}/usr/bin/bash" ] && [ -x "${IMG}/usr/bin/busybox" ] || { echo "s4-fixtures: no image root at ${IMG}"; exit 2; }
SA=projects/ROCKNIX/packages/emulators/standalone

FX=$(mktemp -d /workspace/tmp/m6-t30/fx-s4.XXXXXX) || exit 2
BIN=${FX}/bin; mkdir -p "${BIN}"
for a in sed awk cat cp mv mkdir ln find wc readlink dirname basename rm head tail tr touch ls chmod stat printf echo cut sort sha1sum sha256sum cmp diff unzip mktemp env tee; do
  ln -s "${IMG}/usr/bin/busybox" "${BIN}/${a}"
done
ln -s "${IMG}/usr/bin/bash" "${BIN}/bash"; ln -s "${IMG}/usr/bin/grep" "${BIN}/grep"; IBASH=${BIN}/bash
cat > "${BIN}/argv_print" <<EOF
#!${IBASH}
n=\$1; shift
echo "argc=\$#" > "${FX}/argv.\${n}"
for a in "\$@"; do echo "[\${a}]"; done >> "${FX}/argv.\${n}"
EOF
chmod +x "${BIN}/argv_print"

src() { if [ "${REV}" = WORKTREE ]; then cat "${TREE}/$1"; else git -C "${TREE}" show "${REV}:$1" 2>/dev/null; fi; }
lift() { local out; out=$(src "$1" | LS="$2" LE="$3" awk 'f==0 && $0 ~ ENVIRON["LS"] {f=1} f==1 {print} f==1 && $0 ~ ENVIRON["LE"] {exit}')
  [ -n "${out}" ] || { echo "s4-fixtures: marker /$2/ not found in $1 at ${REV}" >&2; exit 2; }; printf '%s\n' "${out}"; }
# /tmp first: the fixture root itself lives under /workspace/tmp, so a later
# /tmp rewrite would hit the paths already rewritten.
rw() { sed -e "s#/tmp/#$1/tmp/#g" -e "s#/tmp\"#$1/tmp\"#g" | sed -e "s#/storage#$1/storage#g" -e "s#/usr/config#$1/usr/config#g" -e "s#/usr/local/share#$1/usr/local/share#g"; }
FAILS=0
verdict() { if [ "$2" = 0 ]; then echo "PASS $1: $3"; else echo "FAIL $1: $3"; FAILS=$((FAILS + 1)); fi; }
runin() { ( cd "$1" && env -i PATH="${BIN}" HOME="$1/storage" "${IBASH}" "$2" "${@:3}" > "$2.out" 2>&1 ); }

# ---- Mupen64Plus (PL-006, PL-028): run whole ----
mcase() { # name rom
  local R="${FX}/m-$1"; mkdir -p "$R/usr/local/share/mupen64plus" "$R/storage/.config"
  printf '[Core]\nVersion = 1\n' > "$R/usr/local/share/mupen64plus/mupen64plus.cfg"; printf '[Pad]\n' > "$R/usr/local/share/mupen64plus/default.ini"
  { echo 'set_kill() { :; }; get_setting() { :; }'
    src "${SA}/mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh" | sed -e '/^\. \/etc\/profile/d' | rw "$R" | sed -e "s#/usr/local/bin/mupen64plus#argv_print mupen64plus#"
  } > "$R/s.sh"
  rm -f "${FX}/argv.mupen64plus"; runin "$R" "$R/s.sh" "$2"
}
mkdir -p "${FX}/roms"; head -c 4096 /dev/urandom > "${FX}/roms/Wave Race.z64"
( cd "${FX}/roms" && python3 -I -c "import zipfile,sys; z=zipfile.ZipFile('Wave Race.zip','w'); z.write('Wave Race.z64'); z.close()" 2>/dev/null ) || { echo "s4-fixtures: cannot build the zip fixture"; exit 2; }
cp "${FX}/roms/Wave Race.z64" "${FX}/roms/Zippy Race.z64"
mcase zip "${FX}/roms/Wave Race.zip"; A=$(cat "${FX}/argv.mupen64plus" 2>/dev/null)
{ [ "$(tail -1 <<<"$A")" = "[${FX}/m-zip/tmp/mupen64plus/Wave Race.z64]" ] && grep -A1 -x '\[--configdir\]' <<<"$A" | grep -qxF "[${FX}/m-zip/storage/.config/mupen64plus]"; }
verdict mupen64plus-zip $? "a zipped .z64 reaches the emulator as the archive's member, the config dir in /storage"
mcase zippy "${FX}/roms/Zippy Race.z64"; A=$(cat "${FX}/argv.mupen64plus" 2>/dev/null)
{ [ "$(tail -1 <<<"$A")" = "[${FX}/roms/Zippy Race.z64]" ] && ! ls "${FX}/m-zippy/tmp/mupen64plus" 2>/dev/null | grep -q '\.z64$'; }
verdict mupen64plus-zippy-in-place $? "'Zippy Race.z64' is not unzipped, runs in place, no copy under /tmp/mupen64plus"

# ---- the redirection tests (PL-011): no file made, the acceptance grep empty ----
R=${FX}/redir; mkdir -p "$R"
{ echo 'IRES=2; SORIENTATION=1; SROTATION=0; OCM=2; CDS=1; SFXCR=100; CX4CR=100; CS=4; shasum1=aa; shasum2=bb'
  for f in melonds-sa/scripts/start_melonds.sh armsx2-sa/scripts/start_armsx2.sh mednafen/scripts/start_mednafen.sh daedalusx64-sa/scripts/start_daedalusx64.sh; do
    src "${SA}/$f" | grep -E '^[[:space:]]*if \[.*(IRES|SORIENTATION|SROTATION|OCM|CDS|SFXCR|CX4CR|CS|shasum1)\b' | sed -E 's/;?[[:space:]]*then[[:space:]]*$//' | sed -e 's/$/; then :; fi/'
  done; } > "$R/s.sh"
runin "$R" "$R/s.sh"
made=$(ls -A "$R" | grep -v -x -e s.sh -e s.sh.out | wc -l)
hits=$(for f in $(git -C "${TREE}" ls-files "${SA}" | grep -E '\.sh$' | grep -v aethersx2); do src "$f" | grep -E '\[ [^]]*[^-]( <>| >| <) [^]]*\]'; done | wc -l)
{ [ "${made}" = 0 ] && [ "${hits}" = 0 ]; }
verdict redirections $? "the ten tests evaluated in a fixture folder make no file (made ${made}); the acceptance grep finds ${hits} outside aethersx2"

# ---- amiberry (PL-015): the keys kept with the panel's size; configs seeded only when absent ----
R=${FX}/amiberry; mkdir -p "$R/usr/config/amiberry/conf" "$R/storage/.config/amiberry/conf" "$R/tmp/emulation/amiberry"
printf 'chipset=ecs\ngfx_width=720\ngfx_height=568\n@BIOS_PATH@\n' > "$R/usr/config/amiberry/conf/AmigaA500-default.uae"
cp "$R/usr/config/amiberry/conf/AmigaA500-default.uae" "$R/usr/config/amiberry/conf/AmigaA1200-default.uae"
printf 'mine=1\n' > "$R/storage/.config/amiberry/conf/AmigaA1200-default.uae"
{ echo 'fbwidth() { echo 640; }; fbheight() { echo 480; }; find_gamepad() { :; }'
  vars=$(src "${SA}/amiberry/scripts/start_amiberry.sh" | grep -E '^(AMIBERRY_[A-Z_]*|BIOS_PATH)=' | rw "$R"); printf '%s\n' "$vars"
  src "${SA}/amiberry/scripts/start_amiberry.sh" | LS='^### (Refresh|Seed) the configs' LE='^find_gamepad\(\) \{' awk 'f==0 && $0 ~ ENVIRON["LS"] {f=1} f && $0 ~ ENVIRON["LE"] {exit} f {print}' | rw "$R"
  lift "${SA}/amiberry/scripts/start_amiberry.sh" '^AMIBERRY_SET_CONF\(\) \{' '^\}' | rw "$R" | sed '/find_gamepad/d'
  echo 'AMIBERRY_SET_CONF "/storage/roms/amiga/game.adf"'; } > "$R/s.sh"
runin "$R" "$R/s.sh"
C="$R/tmp/emulation/amiberry/.amiberry_conf.uae"
{ grep -qx 'gfx_width=640' "$C" && grep -qx 'gfx_height=480' "$C" && grep -qx 'mine=1' "$R/storage/.config/amiberry/conf/AmigaA1200-default.uae"; }
verdict amiberry-config $? "gfx_width=640 and gfx_height=480 written as keys; the player's own AmigaA1200 config kept"

# ---- mednafen (PL-017) [tree] ----
M=$(src "${SA}/mednafen/scripts/start_mednafen.sh")
{ ! grep -qx 'set -x' <<<"$M" && grep -q -- '\.3dmode \${DM}"' <<<"$M"; }
verdict mednafen-3dmode $? "[tree] -vb.3dmode passes \${DM}; no set -x"

# ---- DraStic (PL-032): the newer image binary, the player's config kept ----
R=${FX}/drastic; mkdir -p "$R/usr/config/drastic/config" "$R/storage/.config/drastic/config"
printf 'NEW-BINARY' > "$R/usr/config/drastic/drastic"; printf 'shipped' > "$R/usr/config/drastic/config/drastic.cfg"
printf 'OLD-BINARY' > "$R/storage/.config/drastic/drastic"; printf 'mine' > "$R/storage/.config/drastic/config/drastic.cfg"
{ lift "${SA}/drastic-sa/scripts/start_drastic.sh" '^#Copy drastic files to \.config' '^if \[ ! -d "/storage/\.config/drastic/system" \]' | sed '$d' | rw "$R"; } > "$R/s.sh"
runin "$R" "$R/s.sh"
{ [ "$(cat "$R/storage/.config/drastic/drastic")" = NEW-BINARY ] && [ "$(cat "$R/storage/.config/drastic/config/drastic.cfg")" = mine ]; }
verdict drastic-refresh $? "a stale /storage binary is replaced by the image's; the player's drastic.cfg unchanged"

# ---- Dolphin (PL-033): the face swap once; a swapped file normalised ----
dcase() { # name want-swap(a>b yes/no) runs
  local R="${FX}/dol-$1"; mkdir -p "$R/usr/config/dolphin-emu" "$R/storage/.config/dolphin-emu"
  printf '[Hotkeys]\nDevice = SDL/0/old\nKeys/Toggle Pause = `Button S`\nKeys/Save = `Button W`&`Back`\n' > "$R/usr/config/dolphin-emu/Hotkeys.ini"
  [ -f "$R/storage/.config/dolphin-emu/Hotkeys.ini" ] || cp "$R/usr/config/dolphin-emu/Hotkeys.ini" "$R/storage/.config/dolphin-emu/"
  local ml="a:b0,b:b1"; [ "$2" = yes ] && ml="a:b1,b:b0"
  { echo "CONF_DIR=$R/storage/.config/dolphin-emu; CON=standard; CONTROLLER_INI=GCPadNew.ini; SDL_DEVICE=pad; MAPLINE='$ml'"
    lift "${SA}/dolphin-sa/scripts/start_dolphin_gc.sh" '^# Some SDL strings are set for XBox-style' '^done$' | rw "$R"; } > "$R/s.sh"
  local i; for i in $(seq 1 "$3"); do runin "$R" "$R/s.sh"; sha1sum < "$R/storage/.config/dolphin-emu/Hotkeys.ini" | cut -c1-40 >> "$R/hashes"; done
}
dcase twice yes 2; H1=$(sed -n 1p "${FX}/dol-twice/hashes"); H2=$(sed -n 2p "${FX}/dol-twice/hashes")
{ [ "$H1" = "$H2" ] && grep -qF 'Keys/Toggle Pause = `Button E`' "${FX}/dol-twice/storage/.config/dolphin-emu/Hotkeys.ini"; }
verdict dolphin-swap-once $? "two preparations with FACE_SWAP=yes leave Hotkeys.ini byte-identical, swapped once"
R=${FX}/dol-norm; mkdir -p "$R/storage/.config/dolphin-emu"
printf '[Hotkeys]\nDevice = SDL/0/old\nKeys/Toggle Pause = `Button E`\nKeys/Save = `Button N`&`Back`\n' > "$R/storage/.config/dolphin-emu/Hotkeys.ini"
dcase norm no 1
grep -qF 'Keys/Toggle Pause = `Button S`' "$R/storage/.config/dolphin-emu/Hotkeys.ini"
verdict dolphin-normalise $? "a Hotkeys.ini left swapped by the old script, no swap wanted, is normalised once"

# ---- the player's settings (PL-038) ----
R=${FX}/xemu; mkdir -p "$R/usr/config/xemu" "$R/storage/.config/xemu"; printf 'shipped' > "$R/usr/config/xemu/xemu.toml"; printf 'mine' > "$R/storage/.config/xemu/xemu.toml"
{ src "${SA}/xemu-sa/scripts/start_xemu.sh" | grep -E '^(SOURCE_DIR|CONF_DIR|XEMU_INI)=' | rw "$R"; lift "${SA}/xemu-sa/scripts/start_xemu.sh" '^#Copy Xemu config' 'XEMU_INI\}"$' | rw "$R"; } > "$R/s.sh"
runin "$R" "$R/s.sh"
[ "$(cat "$R/storage/.config/xemu/xemu.toml")" = mine ]; verdict xemu-settings-kept $? "a setting changed in xemu.toml survives the next preparation"
R=${FX}/dolgs; mkdir -p "$R/usr/config/dolphin-emu/triforce_gecko_codes" "$R/storage/.config/dolphin-emu/GameSettings"
printf 'shipped' > "$R/usr/config/dolphin-emu/triforce_gecko_codes/GVSJ8P.ini"; printf 'mine' > "$R/storage/.config/dolphin-emu/GameSettings/GVSJ8P.ini"
{ lift "${SA}/dolphin-sa/scripts/start_dolphin_gc.sh" '^# Make sure all Triforce Gecko codes' 'triforce_gecko_codes"$' | rw "$R"; } > "$R/s.sh"
runin "$R" "$R/s.sh"
[ "$(cat "$R/storage/.config/dolphin-emu/GameSettings/GVSJ8P.ini")" = mine ]; verdict dolphin-gamesettings-kept $? "a changed GameSettings file survives (the loop copies only what is absent: F-39's Dolphin claim withdrawn)"
M=$(src "${SA}/melonds-sa/scripts/start_melonds.sh")
! grep -q 'rm -rf "${CONF_DIR}/melonDS.toml"' <<<"$M"; verdict melonds-toml-kept $? "[tree] melonDS.toml is not deleted every launch (open: see the stream's record)"

# ---- NanoBoyAdvance (PL-014b): bios_path, and the recipe's check ----
ncase() { # name player-bios(yes/no)
  local R="${FX}/nba-$1"; mkdir -p "$R/usr/config/nanoboyadvance/bios" "$R/storage/.config/nanoboyadvance" "$R/storage/roms/bios"
  printf 'OPEN' > "$R/usr/config/nanoboyadvance/bios/gba_bios.bin"
  printf '[general]\nbios_path = "/storage/roms/bios/gba_bios.bin"\nbios_skip = false\n' | rw "$R" > "$R/storage/.config/nanoboyadvance/config.toml"
  [ "$2" = yes ] && printf 'PLAYER' > "$R/storage/roms/bios/gba_bios.bin"
  { lift "${SA}/nanoboyadvance-sa/scripts/start_nanoboyadvance.sh" '^#NanoBoyAdvance exits without a BIOS|^#Run nanoboyadvance emulator' '^#Run nanoboyadvance emulator' | rw "$R"; } > "$R/s.sh"
  runin "$R" "$R/s.sh"
}
ncase none no; R=${FX}/nba-none
{ grep -qxF "bios_path = \"$R/usr/config/nanoboyadvance/bios/gba_bios.bin\"" "$R/storage/.config/nanoboyadvance/config.toml" && [ -z "$(ls -A "$R/storage/roms/bios")" ]; }
verdict nba-open-bios $? "no player BIOS: bios_path points at the image's open BIOS; nothing written to the player's BIOS folder"
ncase player yes; R=${FX}/nba-player
{ grep -qxF "bios_path = \"$R/storage/roms/bios/gba_bios.bin\"" "$R/storage/.config/nanoboyadvance/config.toml" && [ "$(cat "$R/storage/roms/bios/gba_bios.bin")" = PLAYER ]; }
verdict nba-player-bios $? "a player BIOS: bios_path points at it, the file unchanged"
P=$(src "${SA}/nanoboyadvance-sa/package.mk"); SUM=$(sed -n 's/^PKG_OPEN_SOURCE_BIOS_SHA256="\(.*\)"$/\1/p' <<<"$P")
R=${FX}/nba-recipe; mkdir -p "$R"; printf 'NOT-THE-BIOS' > "$R/gba_bios.bin"
{ [ -n "${SUM}" ] && grep -q 'sha256sum -c' <<<"$P" && ! ( cd "$R" && echo "${SUM}  gba_bios.bin" | env -i PATH="${BIN}" sha256sum -c - >/dev/null 2>&1 ); }
verdict nba-recipe-check $? "the recipe records the open BIOS's sha256 and checks it; a mismatching file fails the check"

# ---- F-42 sites ----
R=${FX}/f42-melonds; mkdir -p "$R"; printf 'ScreenSizing=0\nScreen1Enabled=0\n' > "$R/melonDS.ini"
{ echo "CONF_DIR=$R; MELONDS_INI=melonDS.ini; SLAYOUT=6; DEVICE_HAS_DUAL_SCREEN=false"
  lift "${SA}/melonds-sa/scripts/start_melonds.sh" '^#Screen Layout' '^# Screen Swap' ; } > "$R/s.sh"
runin "$R" "$R/s.sh"
{ grep -qx 'Screen1Enabled=1' "$R/melonDS.ini" && grep -qx 'Screen1Layout=2' "$R/melonDS.ini"; }
verdict f42-melonds-last-line $? "a key on the last line is replaced, not lost (Screen1Enabled=1, Screen1Layout=2)"
R=${FX}/f42-m3u; mkdir -p "$R/roms/ps3/sub"; printf 'game/PS3_GAME\r\n' > "$R/roms/ps3/sub/a.m3u"; printf '/abs/path\n' > "$R/roms/ps3/b.m3u"
{ echo 'set -- "$1"'; lift "${SA}/rpcs3-sa/scripts/start_rpcs3.sh" '^elif \[\[ "\$\{1\}" == \*\.m3u \]\]; then' '^fi$' | sed '1s/^elif/if/'; echo 'echo "GAME_PATH=${GAME_PATH}"'; } > "$R/s.sh"
runin "$R" "$R/s.sh" "$R/roms/ps3/sub/a.m3u"; o1=$(grep '^GAME_PATH=' "$R/s.sh.out"); runin "$R" "$R/s.sh" "$R/roms/ps3/b.m3u"; o2=$(grep '^GAME_PATH=' "$R/s.sh.out")
{ [ "$o1" = "GAME_PATH=$R/roms/ps3/sub/game/PS3_GAME" ] && [ "$o2" = "GAME_PATH=/abs/path" ]; }
verdict f42-rpcs3-m3u $? "a relative M3U line resolves against the playlist's folder (CR dropped), an absolute one is kept"
R=${FX}/f42-vdf; mkdir -p "$R/storage/.local/share/Steam/steamapps"
printf '"libraryfolders"\n{\n\t"0"\n\t{\n\t\t"path" "/x"\n\t}\n\t"1"\n\t{\n\t\t"path" "/y"\n\t}\n}\n' > "$R/storage/.local/share/Steam/steamapps/libraryfolders.vdf"
# Only a /storage after a space or a quote is moved: the escaped \/storage in
# the sed replacement is data the function writes, not a path it opens.
{ lift "${SA}/steam/scripts/start_steam.sh" '^steam_prepare_storage_and_vdf\(\) \{' '^\}' | sed -e "s#\([ \"]\)/storage#\1$R/storage#g"; echo steam_prepare_storage_and_vdf; } > "$R/s.sh"
runin "$R" "$R/s.sh"
grep -qF '"2" {"path" "/storage/roms/steam"}' "$R/storage/.local/share/Steam/steamapps/libraryfolders.vdf"
verdict f42-steam-vdf $? "the library is added at the next free index (\"2\"), not a second \"1\""
R=${FX}/f42-pico8; mkdir -p "$R"
{ echo 'set -- "$1"'; lift "${SA}/pico-8/scripts/start_pico8.sh" '^shopt -s nocasematch' '^shopt -u nocasematch'; echo 'echo "OPTIONS=${OPTIONS}"'; } > "$R/s.sh"
runin "$R" "$R/s.sh" "/storage/roms/splore-carts/celeste.p8"
grep -qx 'OPTIONS=-run' "$R/s.sh.out"; verdict f42-pico8-splore $? "a cart in a folder named splore-carts runs the cart, not Splore"
R=${FX}/f42-hypseus; mkdir -p "$R/auto"; MARK=$R/hyp-marker
printf 'input_up_btn = "a[$(touch %s)]"\ninput_down_btn = "3"\n' "$MARK" > "$R/auto/pad.cfg"; printf 'KEY_UP = x\nKEY_DOWN = x\n' > "$R/hypinput.ini"
{ echo "GPFILE=$R/auto/pad.cfg; configfile=$R/hypinput.ini"
  lift "${SA}/hypseus-singe/scripts/start_hypseus.sh" '^if \[\[ -f "\$\{GPFILE\}" \]\]; then' '^fi # finish auto gamepad' | sed '1s/^if \[\[ -f "\${GPFILE}" \]\]; then/if true; then/'; } > "$R/s.sh"
runin "$R" "$R/s.sh"
{ [ ! -e "${MARK}" ] && grep -qx 'KEY_DOWN = 1073741905 0 4 ' "$R/hypinput.ini"; }
verdict f42-hypseus-arith $? "a button value holding a subscript is skipped, no marker; a number is used (+1)"
T42=$(for f in daedalusx64-sa/scripts/start_daedalusx64.sh cemu-sa/scripts/start_cemu.sh ppsspp-sa/scripts/start_ppsspp.sh vice-sa/scripts/start_vice.sh gzdoom-sa/scripts/start_gzdoom.sh yabasanshiro-sa/scripts/start_yabasanshiro.sh vita3k-sa/scripts/start_vita3k.sh dsperate-sa/scripts/start_dsperate.sh melonds-sa/scripts/start_melonds.sh amiberry/scripts/start_amiberry.sh hatarisa/scripts/start_hatarisa.sh; do src "${SA}/$f"; done)
{ grep -q 'link_storage_dir "/storage/.config/DaedalusX64/Roms"' <<<"$T42" && grep -qx 'cemu -g "\$1"' <<<"$T42" && ! grep -qF '//[\\]/}' <<<"$T42" \
  && grep -qF 'if [ "$SHASUMSRC" != "$SHASUMDST" ]; then' <<<"$T42" && grep -qF 'cp "${MAPPING_FILE}" "${CONFIG_DIR}/keymapv2.json"' <<<"$T42" \
  && grep -qF 'cd "$(dirname "${GAME}")"' <<<"$T42" && [ "$(grep -c -- '-iname "\*.nds"' <<<"$T42")" -ge 2 ] && ! grep -q 'echo -e \${ARGS}' <<<"$T42" \
  && grep -qF '/usr/config/hatari/conf/Atari-ST-default.cfg' <<<"$T42"; }
verdict f42-tree-sites $? "[tree] Daedalus links by the helper, cemu passes the game only, no backslash strip, gzdoom's test quoted, yabasanshiro's cp quoted, Vita3K's zip in its folder, DS archives found by -iname, no echo -e floppy lines, Hatari seeded"

echo "s4-fixtures: ${REV}: failures ${FAILS}; image root ${IMG}; fixture dir ${FX}"
[ "${FAILS}" = 0 ]
