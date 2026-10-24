#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
#
# s1-fixtures.sh -- T30 stream S1's fixtures (#677, #872: PL-012, PL-014,
# PL-029, PL-036). The helper link_storage_dir is run directly; each start
# script's plain variable assignments and its link region (between marker
# lines) are lifted from a commit or the worktree and run under the GENERIC_X64
# image's bash with the image's busybox applets and GNU grep borrowed read-only.
# /storage and /usr/config are rewritten to a fixture root, so nothing outside
# /workspace/tmp/m6-t30/ is touched.
#
#   s1-fixtures.sh <commit|WORKTREE>
#
# One line per case, PASS or FAIL with what was expected and each stub's call
# count. Exit 0 when every case passes, 1 when one fails, 2 when it cannot run.

set -u
REV=${1:?usage: s1-fixtures.sh <commit|WORKTREE>}
TREE=$(git -C "$(dirname "$0")" rev-parse --show-toplevel) || exit 2
IMG=${QA_SYSTEM_ROOT:-/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64/image/system}
[ -x "${IMG}/usr/bin/bash" ] && [ -x "${IMG}/usr/bin/busybox" ] || { echo "s1-fixtures: no image root at ${IMG}"; exit 2; }
SA=projects/ROCKNIX/packages/emulators/standalone
HELPER=projects/ROCKNIX/packages/rocknix/sources/scripts/link_storage_dir

FX=$(mktemp -d /workspace/tmp/m6-t30/fx-s1.XXXXXX) || exit 2
BIN=${FX}/bin; mkdir -p "${BIN}"
for a in sed awk cat cp mv cmp diff mkdir ln find wc readlink dirname basename rm head tail tr touch ls chmod sleep kill pidof printf echo; do
  ln -s "${IMG}/usr/bin/busybox" "${BIN}/${a}"
done
ln -s "${IMG}/usr/bin/bash" "${BIN}/bash"; ln -s "${IMG}/usr/bin/grep" "${BIN}/grep"
IBASH=${BIN}/bash

src() { if [ "${REV}" = WORKTREE ]; then cat "${TREE}/$1"; else git -C "${TREE}" show "${REV}:$1" 2>/dev/null; fi; }
# The helper at REV, run by the image's bash; absent at REV means every case
# that needs it fails, which is the base's answer.
if src "${HELPER}" > "${FX}/helper" && [ -s "${FX}/helper" ]; then
  printf '#!%s\nc=$(cat %s/calls.helper 2>/dev/null || echo 0); echo $((c + 1)) > %s/calls.helper\nexec %s %s/helper "$@"\n' "${IBASH}" "${FX}" "${FX}" "${IBASH}" "${FX}" > "${BIN}/link_storage_dir"
  chmod +x "${BIN}/link_storage_dir"
fi
lift() { # path start-ERE end-ERE [extra-lines]
  local out
  out=$(src "$1" | LS="$2" LE="$3" N="${4:-0}" awk 'f==0 && $0 ~ ENVIRON["LS"] {f=1} f==1 {print} f==1 && n>0 {n--; if (n==0) exit} f==1 && n==0 && $0 ~ ENVIRON["LE"] {if (ENVIRON["N"]+0 > 0) n=ENVIRON["N"]+0; else exit}')
  [ -n "${out}" ] || { echo "s1-fixtures: marker /$2/ not found in $1 at ${REV}" >&2; exit 2; }
  printf '%s\n' "${out}"
}
vars() { src "$1" | grep -E '^[A-Z_][A-Z0-9_]*=' | grep -v -F '$(' ; }
FAILS=0
verdict() { local name=$1 ok=$2 exp=$3; shift 3; local counts="" s
  for s in "$@"; do counts+=" ${s}=$(cat "${FX}/calls.${s}" 2>/dev/null || echo 0)"; done
  if [ "${ok}" = 0 ]; then echo "PASS ${name}: ${exp} (calls:${counts})"; else echo "FAIL ${name}: ${exp} (calls:${counts})"; FAILS=$((FAILS + 1)); fi; }
zero() { echo 0 > "${FX}/calls.helper"; }
rw() { sed -e "s#/storage#$1/storage#g" -e "s#/usr/config#$1/usr/config#g"; }
runs() { # root script-file
  env -i PATH="${BIN}" HOME="$1/storage" "${IBASH}" "$2" > "$2.out" 2>&1
}
islinkto() { [ -L "$1" ] && [ "$(readlink -f "$1")" = "$(readlink -f "$2")" ]; }

# ---- the helper ----
hrun() { env -i PATH="${BIN}" link_storage_dir "$@" > "${FX}/h.out" 2> "${FX}/h.err"; }
H=${FX}/h1; mkdir -p "$H/src/sub" "$H/tgt"; printf card > "$H/src/a.mcd"; printf state > "$H/src/sub/b.sav"; printf other > "$H/tgt/c.sav"
zero; hrun "$H/src" "$H/tgt"; rc=$?
{ [ $rc = 0 ] && islinkto "$H/src" "$H/tgt" && [ "$(cat "$H/tgt/a.mcd")" = card ] && [ "$(cat "$H/tgt/sub/b.sav")" = state ] && [ "$(cat "$H/tgt/c.sav")" = other ]; }
verdict helper-merge $? "a real source's two files arrive once beside the target's own, the source becomes the link, rc 0" helper
H=${FX}/h2; mkdir -p "$H/tgt"; ln -s "$H/tgt" "$H/src"; before=$(stat -c %Y-%i "$H/src" 2>/dev/null || ls -lid "$H/src")
zero; hrun "$H/src" "$H/tgt"; rc=$?
{ [ $rc = 0 ] && islinkto "$H/src" "$H/tgt" && [ "$(stat -c %Y-%i "$H/src" 2>/dev/null || ls -lid "$H/src")" = "$before" ]; }
verdict helper-already-linked $? "a source already linked to the target is left untouched, rc 0" helper
H=${FX}/h3; mkdir -p "$H/src" "$H/tgt"; printf card > "$H/src/a.mcd"; chmod 555 "$H/tgt"
zero; hrun "$H/src" "$H/tgt"; rc=$?; chmod 755 "$H/tgt"
{ [ $rc = 1 ] && [ -d "$H/src" ] && [ ! -L "$H/src" ] && [ "$(cat "$H/src/a.mcd")" = card ] && [ "$(grep -c '' "${FX}/h.err")" = 1 ]; }
verdict helper-copy-fails $? "a read-only target: the source stays a folder with its file, rc 1, one line on stderr" helper
H=${FX}/h4; mkdir -p "$H/src" "$H/tgt"; printf mine > "$H/src/a.mcd"; printf theirs > "$H/tgt/a.mcd"
zero; hrun "$H/src" "$H/tgt"; rc=$?
{ [ $rc = 1 ] && [ "$(cat "$H/src/a.mcd")" = mine ] && [ "$(cat "$H/tgt/a.mcd")" = theirs ]; }
verdict helper-conflict $? "the same name with different bytes on both sides: both kept, rc 1" helper
H=${FX}/h5; mkdir -p "$H"
zero; hrun "$H/p/src" "$H/tgt"; rc=$?
{ [ $rc = 0 ] && islinkto "$H/p/src" "$H/tgt"; }
verdict helper-absent-source $? "an absent source (and parent) becomes the link, rc 0" helper

# ---- the link sites: a real source folder with a file, the target holding another ----
site() { # name path start end source target
  local name=$1 path=$2 st=$3 en=$4 s=$5 t=$6 R="${FX}/site-$1"
  mkdir -p "$R"; zero
  { echo 'set_kill() { :; }; get_setting() { :; }'; vars "${path}" | rw "$R"; lift "${path}" "${st}" "${en}" | rw "$R"; } > "$R/s.sh" || exit 2
  mkdir -p "$R$s" "$R$t"; printf keep > "$R$s/keep.sav"; printf dot > "$R$s/.hidden.cfg"; printf other > "$R$t/other.sav"
  runs "$R" "$R/s.sh"
  { islinkto "$R$s" "$R$t" && [ "$(cat "$R$t/keep.sav" 2>/dev/null)" = keep ] && [ "$(cat "$R$t/.hidden.cfg" 2>/dev/null)" = dot ] && [ "$(cat "$R$t/other.sav")" = other ]; }
  verdict "site-${name}" $? "${s#/storage/} -> ${t#/storage/}: its file and its hidden file kept under the target, the folder a link" helper
}
site duckstation-memcards ${SA}/duckstation-sa/scripts/start_duckstation.sh '^#Link config dir to where appimage' '^# Keep default captures' /storage/.config/duckstation/memcards /storage/roms/psx/duckstation/memcards
site duckstation-savestates ${SA}/duckstation-sa/scripts/start_duckstation.sh '^#Link config dir to where appimage' '^# Keep default captures' /storage/.config/duckstation/savestates /storage/roms/savestates/psx
site rpcs3 ${SA}/rpcs3-sa/scripts/start_rpcs3.sh '^# Link certain RPCS3 folders' '^#Emulation Station Features' /storage/.config/rpcs3/dev_hdd0 /storage/roms/bios/rpcs3/dev_hdd0
site azahar ${SA}/azahar-sa/scripts/start_azahar.sh '^# Move sdmc & nand' '^# RK3588 - handle' /storage/.config/azahar/states /storage/roms/savestates/3ds
site drastic ${SA}/drastic-sa/scripts/start_drastic.sh '^#Link savestates to roms/savestates/nds' '^#Apply ES features' /storage/.config/drastic/savestates /storage/roms/savestates/nds
site ares ${SA}/ares-sa/scripts/start_ares.sh '^# Link  .config/ares to .local' '^# Emulation Station Features' /storage/.local/share/ares /storage/.config/ares
site skyemu ${SA}/skyemu-sa/scripts/start_skyemu.sh '^# Link  .config/dolphin-emu to .local' '^# Retroachievements' /storage/.local/share/Sky/SkyEmu /storage/.config/SkyEmu
site bigpemu ${SA}/bigpemu-sa/scripts/start_bigpemu.sh '^# Link bigpemu userdata' '^#Emulation Station Features' /storage/.bigpemu_userdata /storage/.config/bigpemu/userdata
site hatari ${SA}/hatarisa/scripts/start_hatari.sh '^# create symlink to hatari config dir' '^# Which file should hatari load' /storage/.hatari /storage/.config/hatari
site cemu ${SA}/cemu-sa/scripts/start_cemu.sh '^# create link to config directory' '^# Create symlink to logfile' /storage/.config/Cemu/share/mlc01 /storage/roms/bios/cemu/mlc01

# ---- flycast: the old script's own layout, then a second launch ----
F=${SA}/flycast-sa/scripts/start_flycast.sh; R=${FX}/flycast; mkdir -p "$R"
{ vars "$F" | rw "$R"; lift "$F" '^#Move save file storage/roms|^#Make flycast bios folder' '^#Link  .config/flycast to .local' 1 | rw "$R"; } > "$R/s.sh" || exit 2
mkdir -p "$R/storage/roms/dreamcast/data" "$R/storage/roms/bios/dc"; printf vmu > "$R/storage/roms/dreamcast/data/vmu_save_A1.bin"
ln -s "$R/storage/roms/bios/dc" "$R/storage/roms/dreamcast/data/dc"; zero
runs "$R" "$R/s.sh"; runs "$R" "$R/s.sh"
{ islinkto "$R/storage/roms/dreamcast/data" "$R/storage/roms/bios/dc" && [ "$(cat "$R/storage/roms/bios/dc/vmu_save_A1.bin" 2>/dev/null)" = vmu ] && [ ! -e "$R/storage/roms/bios/dc/dc" ] && [ ! -L "$R/storage/roms/bios/dc/dc" ]; }
verdict flycast-two-launches $? "after two launches dreamcast/data is a link to bios/dc, the VMU file kept, no dc link inside bios/dc" helper
# its gptokeyb: only the launch's own is ended
R=${FX}/flycast-kill; mkdir -p "$R"
printf '#!%s\nwhile :; do sleep 1; done\n' "${IBASH}" > "${BIN}/gptokeyb"; chmod +x "${BIN}/gptokeyb"
printf '#!%s\nsleep 1\n' "${IBASH}" > "${BIN}/flycast-stub"; chmod +x "${BIN}/flycast-stub"
{ echo 'GPTOKEYB=gptokeyb; CONF_DIR=/x; EMUPERF=""'; lift "$F" '^\$GPTOKEYB "flycast"' '^kill -9' | sed 's#/usr/bin/flycast#flycast-stub#'; } > "$R/s.sh" || exit 2
env -i PATH="${BIN}" gptokeyb & OTHER=$!
sleep 0.3; env -i PATH="${BIN}" "${IBASH}" "$R/s.sh" > "$R/s.out" 2>&1; sleep 0.3
LAUNCHED=$(env -i PATH="${BIN}" pidof gptokeyb | tr ' ' '\n' | grep -v -x "${OTHER}" | head -1)
{ kill -0 "${OTHER}" 2>/dev/null && [ -z "${LAUNCHED}" ]; }
verdict flycast-kill-own $? "the launch's gptokeyb ended, another gptokeyb left running" helper
kill -9 "${OTHER}" ${LAUNCHED} 2>/dev/null

# ---- OpenBOR: a pak file in Paks survives, the old link goes ----
O=${SA}/openbor/scripts/start_OpenBOR.sh; R=${FX}/openbor; mkdir -p "$R/storage/openbor/Paks" "$R/storage/roms/openbor"
printf pak > "$R/storage/openbor/Paks/mine.pak"; printf old > "$R/storage/roms/openbor/old.pak"; ln -s "$R/storage/roms/openbor/old.pak" "$R/storage/openbor/Paks/old.pak"
printf new > "$R/storage/roms/openbor/new.pak"; mkdir -p "$R/usr/config/openbor"; printf cfg > "$R/usr/config/openbor/master.cfg"
{ vars "$O" | rw "$R"; lift "$O" '^# Make sure the folders exists' 'ln -sf "\$1" "\$\{PAKS\}"' | rw "$R"; } > "$R/s.sh" || exit 2
zero; env -i PATH="${BIN}" "${IBASH}" "$R/s.sh" "$R/storage/roms/openbor/new.pak" > "$R/s.out" 2>&1
{ [ "$(cat "$R/storage/openbor/Paks/mine.pak" 2>/dev/null)" = pak ] && [ ! -e "$R/storage/openbor/Paks/old.pak" ] && [ -L "$R/storage/openbor/Paks/new.pak" ]; }
verdict openbor-paks $? "a pak file in Paks kept, the previous launch's link removed, the new link made" helper

# ---- NanoBoyAdvance: no gba_bios.bin directory, the old copy removed only when it is that copy ----
N=${SA}/nanoboyadvance-sa/scripts/start_nanoboyadvance.sh
ncase() { # name setup-function check-description check-command
  local R="${FX}/nba-$1"; mkdir -p "$R/usr/config/nanoboyadvance/bios" "$R/storage/roms/bios/gba"
  printf toml > "$R/usr/config/nanoboyadvance/config.toml"; printf keys > "$R/usr/config/nanoboyadvance/keymap.toml"; printf biosbytes > "$R/usr/config/nanoboyadvance/bios/gba_bios.bin"
  "$2" "$R"
  { lift "$N" '^#Make nanoboyadvance bios folder' '^#Set the cores to use' | rw "$R"; } > "$R/s.sh" || exit 2
  zero; runs "$R" "$R/s.sh"
  ( B="$R/storage/roms/bios/gba/gba_bios.bin"; eval "$4" ); verdict "nba-$1" $? "$3" helper
}
fresh() { :; }
oldcopy() { cp -r "$1/usr/config/nanoboyadvance" "$1/storage/roms/bios/gba/gba_bios.bin"; }
changed() { oldcopy "$1"; printf mine > "$1/storage/roms/bios/gba/gba_bios.bin/player-notes.txt"; }
realfile() { printf realbios > "$1/storage/roms/bios/gba/gba_bios.bin"; }
ncase fresh fresh "a fresh device gets no gba_bios.bin" '[ ! -e "$B" ]'
ncase old-copy oldcopy "the old script's exact copy is removed" '[ ! -e "$B" ]'
ncase changed-copy changed "a copy the player added to is kept" '[ -f "$B/player-notes.txt" ]'
ncase real-file realfile "a real BIOS file is kept" '[ "$(cat "$B")" = realbios ]'

echo "s1-fixtures: ${REV}: failures ${FAILS}; image root ${IMG}; fixture dir ${FX}"
[ "${FAILS}" = 0 ]
