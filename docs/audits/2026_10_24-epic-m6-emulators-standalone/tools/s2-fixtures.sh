#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
#
# s2-fixtures.sh -- T30 stream S2's Steam fixture (#677, #872: PL-030). Sources
# the real start_steam.sh and runs the real wrapper lines of start_steam_x86.sh
# and start_steam_arm64.sh (from steam_ensure_fex_config_template to the binfmt
# restore), from a commit or the worktree, under the GENERIC_X64 image's bash
# and busybox. Every function the wrapper calls except steam_launch_bigpicture
# is a stub that records its call; gamescope, FEX and systemctl are stubs that
# record theirs. /storage and /tmp are rewritten to a fixture root.
#
#   s2-fixtures.sh <commit|WORKTREE>
#
# Expect, per flavour, steam_dual_screen_end and the binfmt restore recorded
# after the session returns. Exit 0 all pass, 1 a failure, 2 cannot run.

set -u
REV=${1:?usage: s2-fixtures.sh <commit|WORKTREE>}
TREE=$(git -C "$(dirname "$0")" rev-parse --show-toplevel) || exit 2
IMG=${QA_SYSTEM_ROOT:-/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64/image/system}
[ -x "${IMG}/usr/bin/bash" ] && [ -x "${IMG}/usr/bin/busybox" ] || { echo "s2-fixtures: no image root at ${IMG}"; exit 2; }
S=projects/ROCKNIX/packages/emulators/standalone/steam/scripts

FX=$(mktemp -d /workspace/tmp/m6-t30/fx-s2.XXXXXX) || exit 2
BIN=${FX}/bin; mkdir -p "${BIN}" "${FX}/tmp" "${FX}/storage"
for a in sed awk cat cp mv mkdir ln find wc readlink dirname basename rm head tail tr touch ls chmod sleep mktemp printf echo grep cut; do
  ln -s "${IMG}/usr/bin/busybox" "${BIN}/${a}"
done
ln -s "${IMG}/usr/bin/bash" "${BIN}/bash"; IBASH=${BIN}/bash
for s in systemctl gamescope FEX; do
  printf '#!%s\necho "%s $*" | cut -c1-60 >> %s/calls.log\nexit 0\n' "${IBASH}" "$s" "${FX}" > "${BIN}/$s"; chmod +x "${BIN}/$s"
done
src() { if [ "${REV}" = WORKTREE ]; then cat "${TREE}/$1"; else git -C "${TREE}" show "${REV}:$1" 2>/dev/null; fi; }
src "$S/start_steam.sh" | sed -e "s#/storage#${FX}/storage#g" -e "s#/tmp/#${FX}/tmp/#g" > "${FX}/start_steam.sh"
[ -s "${FX}/start_steam.sh" ] || { echo "s2-fixtures: start_steam.sh not found at ${REV}"; exit 2; }
STUBBED="steam_ensure_fex_config_template steam_prepare_storage_and_vdf steam_load_es_thunk_settings steam_apply_lsfg_settings steam_apply_fps_limit steam_set_cpu_affinity steam_debug_print steam_read_sway_geometry steam_setup_environment steam_scope_reexec_if_needed steam_dual_screen_begin steam_dual_screen_end steam_touch_calibration_begin steam_touch_calibration_end steam_arm64_binfmt_and_proton_prep"
FAILS=0
flavour() { # name wrapper restore-line
  local name=$1 w=$2 restore=$3 d="${FX}/$1" body
  mkdir -p "$d"; : > "${FX}/calls.log"
  body=$(src "$S/$w" | R="systemctl ${restore} systemd-binfmt" awk '/^steam_ensure_fex_config_template/{f=1} f{print} f && index($0, ENVIRON["R"]){exit}')
  [ -n "${body}" ] || { echo "s2-fixtures: wrapper lines not found in $w at ${REV}"; exit 2; }
  {
    echo "STEAM_MAIN_SCRIPT=$w; STEAM_FLAVOR=${name}; W=1280; H=800; REFRESH_HZ=60; TRANSFORM=0"
    echo ". ${FX}/start_steam.sh"
    for f in ${STUBBED}; do echo "$f() { echo $f >> ${FX}/calls.log; }"; done
    printf '%s\n' "${body}"
    echo "echo 'wrapper end' >> ${FX}/calls.log"
  } > "$d/s.sh"
  env -i PATH="${BIN}" HOME="${FX}/storage" "${IBASH}" "$d/s.sh" > "$d/out" 2>&1
  cp "${FX}/calls.log" "$d/calls.log"
  local after_end after_restore n_end n_restore
  n_end=$(grep -c '^steam_dual_screen_end' "$d/calls.log"); n_restore=$(grep -c "^systemctl ${restore} systemd-binfmt" "$d/calls.log")
  after_end=$(awk '/^systemctl start essway/{s=1} s && /^steam_dual_screen_end/{print "yes"; exit}' "$d/calls.log")
  after_restore=$(awk -v r="^systemctl ${restore} systemd-binfmt" '/^steam_dual_screen_end/{s=1} s && $0 ~ r {print "yes"; exit}' "$d/calls.log")
  if [ "${after_end}" = yes ] && [ "${after_restore}" = yes ]; then v=PASS; else v=FAIL; FAILS=$((FAILS + 1)); fi
  echo "${v} steam-${name}: after the session returns, steam_dual_screen_end then 'systemctl ${restore} systemd-binfmt' (calls: gamescope=$(grep -c '^gamescope' "$d/calls.log") essway-start=$(grep -c '^systemctl start essway' "$d/calls.log") dual_screen_end=${n_end} binfmt-${restore}=${n_restore})"
}
flavour x86 start_steam_x86.sh start
flavour arm64 start_steam_arm64.sh restart
echo "s2-fixtures: ${REV}: failures ${FAILS}; image root ${IMG}; fixture dir ${FX}"
[ "${FAILS}" = 0 ]
