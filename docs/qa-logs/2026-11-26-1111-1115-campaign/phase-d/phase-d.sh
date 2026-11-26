#!/bin/bash
# #1111/#1115 phase D: the cloud folder and connection screens on build 12, in
# English and French, at one panel size per run.
#
#   phase-d.sh --round <round worktree> --image <build 12 img.gz> --res 640x480|1280x800 \
#       --outdir DIR [--lang en,fr] [--only s01,s07,...]
#
# A fresh vm-pair guest, the QA WebDAV cloud seeded as tools/vm-qa seeds it
# (a run-time stanza, never in the tree). For each language: set it, reboot,
# then each screen: arm its state over ssh, walk from the carousel through the
# calibrated legs (tools/vm-walks/to-manage-cloud-storage; the counts are
# from ES d87891f24 and were read off frames on 2026-11-26), take the frames,
# put the state back. Frames under <lang>/<screen>/, the arming log beside.
# QA guest only. Exit 0 every walk ran, 1 one did not, 2 cannot run.
set -uo pipefail
round= image= res= out= langs=en,fr only=
while [ "$#" -ge 2 ]; do
    case "$1" in --round) round=$2 ;; --image) image=$2 ;; --res) res=$2 ;; --outdir) out=$2 ;;
        --lang) langs=$2 ;; --only) only=$2 ;; *) exit 2 ;; esac; shift 2
done
[ -x "$round/tools/vm-pair" ] && [ -r "$image" ] && [[ $res =~ ^[0-9]+x[0-9]+$ ]] && [ -n "$out" ] ||
    { echo "usage: $0 --round TREE --image IMG --res WxH --outdir DIR [--lang en,fr] [--only s01,...]" >&2; exit 2; }
! [ -e "$out" ] || { echo "cannot run: $out exists" >&2; exit 2; }
mkdir -p "$out" && out=$(cd "$out" && pwd) || exit 2
W=$round/tools/vm-walks
KEY=/tmp/rocknix-vm-pair/qa-key; MON=/tmp/rocknix-qemu-monitor.sock
SSHO=(-F /dev/null -p 10022 -i "$KEY" -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=no
      -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=10)
SCPO=(-F /dev/null -P 10022 -i "$KEY" -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=no
      -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=10)
S() { timeout 120 ssh -n "${SSHO[@]}" root@127.0.0.1 ". /etc/profile >/dev/null 2>&1; $*"; }
log() { echo "$*" | tee -a "$out/RESULT.txt"; }
die() { log "CANNOT RUN: $*"; exit 2; }
DATA=$HOME/.cache/rocknix-cloud-qa/data   # the QA backend's served tree (tools/cloud-test-backend status)

down() { local i; for i in $(seq 1 "$1"); do echo "key down"; echo "wait-for-change 4"; done; echo settle; }
open() { echo "key x"; echo "wait-for-change 30 1"; echo "settle 30 3"; }
back() { echo "key z"; echo "wait-for-change 10"; echo settle; }
hub() { echo wake; echo dismiss-dialogs; cat "$W/to-manage-cloud-storage.steps"; }
ctx() { echo 'c=$(cloud_remote folder-context | jq -r .context_id)'; }

# s01: the editor, the defaults preview and NO (C20, C24, C21, C03, C18 hub)
steps_s01() { hub; down 6; echo "shot hub-change-row"; open; echo "shot editor"; down 4; echo "shot defaults-row"; open; echo "shot defaults-preview"; back; echo "shot after-no"; }
arm_s01() { :; }; put_s01() { :; }
# s02: custom folders shown, then YES to the defaults (C21, C20)
steps_s02() { hub; down 6; open; echo "shot editor-custom"; down 4; open; echo "shot defaults-preview-custom"; echo "key x"; echo "wait-for-change 30 1"; echo "settle 30 3"; echo "shot editor-after-yes"; }
arm_s02() { S "$(ctx); cloud_remote set-folder saves /Custom/Saves \$c && cloud_remote folder-context | jq -c .paths"; }
put_s02() { S "$(ctx); cloud_remote default-folders \$c >/dev/null; cloud_remote folder-context | jq -c .paths"; }
# s03: the content folder at the cloud root (C19's display)
steps_s03() { hub; down 6; echo "shot hub-row-root"; open; echo "shot editor-content-root"; }
arm_s03() { S "$(ctx); cloud_remote set-folder content / \$c; cloud_remote folder-context | jq -c .paths"; }
put_s03() { put_s02; }
# s04: no connection selected (C10, C11, C03)
steps_s04() { hub; down 5; echo "shot hub-unselected"; down 1; open; echo "shot editor-unavailable"; }
arm_s04() { S ': > /storage/.config/rclone/active-connection; cloud_remote setup-info | grep -E "^STATE="'; }
put_s04() { S 'cloud_remote select qa-cloud; cloud_remote setup-info | grep -E "^STATE="'; }
# s05: a restored pointer that disagrees with the profile (C11)
steps_s05() { hub; down 6; echo "shot hub-review"; open; echo "shot editor-review"; }
arm_s05() { S "sed -i 's|^SAVES_REMOTE=.*|SAVES_REMOTE=\"/Restored/Other\"|' /storage/.config/cloud_sync.conf; cloud_remote setup-info | grep -E '^STATE='"; }
put_s05() { S 'cloud_remote select qa-cloud; cloud_remote setup-info | grep -E "^STATE="'; }
# s06: the defaults refused while the exit sync is on, switched on and off on the page (C06, C22, C03)
steps_s06() { hub; down 4; echo "key x"; echo "wait-for-change 6"; echo settle; echo "shot exit-sync-on"; down 2; open; down 4; open; echo "shot defaults-refused-autosync"; back; back; echo "key up"; echo "wait-for-change 4"; echo "key up"; echo "wait-for-change 4"; echo settle; echo "key x"; echo "wait-for-change 6"; echo settle; echo "shot exit-sync-off"; }
arm_s06() { :; }; put_s06() { S 'get_setting cloudsaves.gameexit'; }
# s07: one saved connection (C12, C03 in use, C18 connection page)
steps_s07() { hub; cat "$W/to-manage-cloud-connections.steps"; }
arm_s07() { :; }; put_s07() { :; }
# s08: a second connection on the same provider (C12 AVAILABLE CONNECTIONS)
steps_s08() { steps_s07; }
arm_s08() { S 'python3 /storage/m7-qa-d/conn.py add-two'; }
put_s08() { S 'python3 /storage/m7-qa-d/conn.py remove-two'; }
# s09: a connection's own page, and CHANGE CLOUD FOLDER LOCATIONS on it (C18, C03)
steps_s09() { hub; down 9; open; echo "shot connections"; open; echo "shot connection-page"; down 6; echo "shot connection-page-lower"; }
arm_s09() { :; }; put_s09() { :; }
# s10: CHECK CLOUD FOLDERS with the default categories; five results; the five instruction pages (C16, C17, C18, 1115 C04)
steps_s10() { hub; down 7; open; echo "shot folder-actions"; down 6; echo "shot check-focused"; echo "key x"; echo "wait-for-change 60 1"; echo "settle 60 3"; echo "shot results-top"
    local i; for i in 1 2 3 4 5; do open; echo "shot instructions-$i"; back; [ "$i" -lt 5 ] && { down 1; echo "shot results-at-$((i+1))"; }; done; }
arm_s10() { :; }; put_s10() { :; }
# s11: a settings folder past the entry limit: accessible, the check incomplete, saves still found (1115 C02, C04)
steps_s11() { hub; down 7; open; down 6; echo "key x"; echo "wait-for-change 60 1"; echo "settle 60 3"; echo "shot results-limited-top"; down 1; echo "shot results-limited-settings"; }
arm_s11() { mkdir -p "$DATA/pixelelated/Backups/many" && (cd "$DATA/pixelelated/Backups/many" && for i in $(seq -w 0 4096); do : > "f$i.bin"; done) && mkdir -p "$DATA/pixelelated/Saves/gb" && echo save > "$DATA/pixelelated/Saves/gb/Game.srm" && ls "$DATA/pixelelated/Backups/many" | wc -l; }
put_s11() { rm -rf "${DATA:?}/pixelelated/Backups/many" "${DATA:?}/pixelelated/Saves/gb"; ls "$DATA/pixelelated/Backups" | wc -l; }
# s12: the cloud stops answering: a real failure, not a limit (1115 C04)
steps_s12() { hub; down 7; open; down 6; echo "key x"; echo "wait-for-change 60 1"; echo "settle 60 3"; echo "shot results-failure"; }
arm_s12() { S "sed -i 's|^\(url = https\{0,1\}://[^:/]*\):[0-9]*|\1:9011|' /storage/.config/rclone/rclone.conf; grep -c ':9011' /storage/.config/rclone/rclone.conf"; }
put_s12() { S "sed -i 's|^\(url = https\{0,1\}://[^:/]*\):9011|\1:9010|' /storage/.config/rclone/rclone.conf; grep -c ':9010' /storage/.config/rclone/rclone.conf; cloud_remote select qa-cloud"; }
# s13: CHECK CLOUD SETUP's page and its CHANGE CLOUD FOLDER LOCATIONS (C18)
steps_s13() { hub; down 8; open; echo "wait 20"; echo "settle 60 3"; echo "shot setup-check"; down 8; echo "shot setup-check-lower"; }
arm_s13() { :; }; put_s13() { :; }

# s14: LINK FROM A COMPUTER and its CHANGE CLOUD FOLDER LOCATIONS (C18's computer entry point)
steps_s14() { hub; down 9; open; echo "shot connections"; down 2; echo "shot link-from-computer-row"; open; echo "wait 5"; echo "settle 30 3"; echo "shot computer-setup"; down 8; echo "shot computer-setup-lower"; }
arm_s14() { :; }; put_s14() { :; }

# s15: no saved connection at all (C12's empty state). Up twice from the hub's
# top wraps to its last row, MANAGE CLOUD CONNECTIONS (#1428's legs).
steps_s15() { hub; echo "shot hub-no-connections"; down 3; echo "shot hub-no-connections-lower"; echo "key up"; echo "wait-for-change 4"; echo "key up"; echo "wait-for-change 4"; echo "key up"; echo "wait-for-change 4"; echo "key up"; echo "wait-for-change 4"; echo "key up"; echo "wait-for-change 4"; echo settle; echo "shot hub-last-row"; open; echo "shot connections-none"; back; echo "key up"; echo "wait-for-change 4"; echo settle; open; echo "wait 20"; echo "settle 60 3"; echo "shot setup-check-none"; }
arm_s15() { S 'cd /storage/.config/rclone && sha256sum rclone.conf folder-profiles.json active-connection ../cloud_sync.conf 2>&1 | cut -c1-16,64- ; cd /; mv /storage/.config/rclone/rclone.conf /storage/m7-qa-d/rclone.conf.saved && rm -f /storage/.config/rclone/active-connection; cloud_remote setup-info | grep -E "^STATE="'; }
put_s15() { S 'mv /storage/m7-qa-d/rclone.conf.saved /storage/.config/rclone/rclone.conf && chmod 600 /storage/.config/rclone/rclone.conf && cloud_remote select qa-cloud; cloud_remote setup-info | grep -E "^STATE="; cd /storage/.config/rclone && sha256sum rclone.conf folder-profiles.json active-connection ../cloud_sync.conf 2>&1 | cut -c1-16,64- ; cd /;'; }
# s16: CLOUD SETUP CHECK to the foot of the page (C18's entry point there)
steps_s16() { hub; down 8; open; echo "wait 20"; echo "settle 60 3"; echo "shot setup-check-top"; echo "key up"; echo "wait-for-change 4"; echo "key up"; echo "wait-for-change 4"; echo settle; echo "shot setup-check-foot"; }
arm_s16() { :; }; put_s16() { :; }
# s17: an attempt to put the saves folder at the cloud root (#1480 criterion 1).
# The profile module refuses it ("Choose a separate folder for saves or
# settings backups.", cloud_connection_profiles.py: saves is never '' or '/'),
# so the frames show the hub and the editor unchanged.
ARM_REFUSED="s17"
steps_s17() { hub; down 6; echo "shot hub-saves-root"; open; echo "shot editor-saves-root"; }
# s18: removing a connection that is not in use: the confirmation, CANCEL, then REMOVE CONNECTION (#1111 C01, C08)
# The shared to-manage-cloud-connections walk ends after six downs, which land
# wherever the list length puts them (with two connections, on QA-TWO), so go
# to the list as s09 does: the page opens on the first connection.
to_two() { hub; down 9; open; echo "shot connections-two"; down 1; echo "shot two-focused"; open; echo "shot connection-two"; }
steps_s18() { to_two; down 6; echo "shot remove-row"; open; echo "shot remove-confirm"; back; echo "shot after-cancel"; open; echo "shot remove-confirm-again"; echo "key x"; echo "wait-for-change 60 1"; echo "settle 60 3"; echo "shot after-remove"; }
arm_s18() { S 'python3 /storage/m7-qa-d/conn.py add-two'; }
put_s18() { S 'python3 /storage/m7-qa-d/conn.py state; python3 /storage/m7-qa-d/conn.py repair'; }
# s19: EDIT CONNECTION on a connection whose endpoint stopped answering: backed out of (cancel), then saved, which re-verifies and fails; the section is kept byte for byte (#1111 C03, C06, C08)
# From build 14 (ES 274d3716b, #1483) back on the form returns to the connection
# page with the cursor on EDIT CONNECTION. On build 13 it returned to the list,
# and this walk then removed qa-two (640x480-more/*/s19, indexed walk-failed).
steps_s19() { to_two; down 5; echo "shot edit-row"; open; echo "shot edit-form"; back; echo "shot after-cancel"; open; echo "shot edit-form-again"; echo "key up"; echo "wait-for-change 4"; echo "key up"; echo "wait-for-change 4"; echo settle; echo "shot save-row"; open; echo "shot update-confirm"; echo "key x"; echo "wait-for-change 120 1"; echo "settle 120 3"; echo "shot update-failed"; echo "key x"; echo "wait-for-change 10"; echo settle; echo "shot after-failure-ok"; back; echo "shot after-failure-back"; }
arm_s19() { S 'python3 /storage/m7-qa-d/conn.py add-two >/dev/null && python3 /storage/m7-qa-d/conn.py break-two'; }
put_s19() { S 'python3 /storage/m7-qa-d/conn.py two-hash; python3 /storage/m7-qa-d/conn.py repair'; }
# s20: an unreadable setup (a line before rclone.conf's first section): the hub, CHECK CLOUD SETUP, MANAGE CLOUD CONNECTIONS and CLOUD FOLDER ACTIONS (#1111 C11)
steps_s20() { hub; down 5; echo "shot hub-unreadable"; down 3; open; echo "wait 20"; echo "settle 60 3"; echo "shot setup-check-unreadable"; back; down 1; open; echo "shot connections-unreadable"; back; echo "key up"; echo "wait-for-change 4"; echo "key up"; echo "wait-for-change 4"; echo settle; open; echo "shot folder-actions-unreadable"; }
arm_s20() { S "cp -p /storage/.config/rclone/rclone.conf /storage/m7-qa-d/rclone.conf.s20 && sed -i '1i not a section line' /storage/.config/rclone/rclone.conf && cloud_remote setup-info | grep -E '^STATE='"; }
put_s20() { S 'mv /storage/m7-qa-d/rclone.conf.s20 /storage/.config/rclone/rclone.conf && chmod 600 /storage/.config/rclone/rclone.conf && cloud_remote select qa-cloud; cloud_remote setup-info | grep -E "^STATE="'; }
# s21: the folder locations changed while CLOUD FOLDERS is open, then CHECK CLOUD FOLDERS: the stale-check wording (#1111 C11)
steps_s21() { hub; down 7; open; echo "shot folders-before-change"; }
mid_s21() { S "$(ctx); cloud_remote set-folder saves /Custom/Saves \$c && cloud_remote folder-context | jq -c .paths"; }
steps2_s21() { echo settle; down 6; echo "shot check-after-change"; echo "key x"; echo "wait-for-change 20 1"; echo settle; echo "shot check-refused"; echo "key x"; echo "wait-for-change 10"; echo settle; echo "shot after-ok"; }
put_s21() { put_s02; }
# s22: the selection emptied while CLOUD FOLDERS is open, then CHECK CLOUD FOLDERS: no selection, not the stale wording (#1111 C11)
steps_s22() { steps_s21; }
mid_s22() { S ': > /storage/.config/rclone/active-connection; cloud_remote setup-info | grep -E "^STATE="'; }
steps2_s22() { steps2_s21; }
put_s22() { put_s04; }
arm_s21() { :; }; arm_s22() { :; }
# s23: a connection saved but none selected: MANAGE CLOUD CONNECTIONS and CHECK CLOUD SETUP still say CHOOSE (#1482 criterion 3)
steps_s23() { hub; down 9; open; echo "shot connections-unselected"; back; echo "key up"; echo "wait-for-change 4"; echo settle; open; echo "wait 20"; echo "settle 60 3"; echo "shot setup-check-unselected"; }
arm_s23() { arm_s04; }; put_s23() { put_s04; }
# s24: LINK FROM THIS DEVICE, WEBDAV, then back on its form: where the add-a-connection wizard lands (#1483 criterion 3)
steps_s24() { hub; down 9; open; down 1; echo "shot link-row"; open; echo "shot providers"; down 8; echo "shot webdav-row"; open; echo "shot webdav-form"; back; echo "shot after-back"; }
arm_s24() { :; }; put_s24() { :; }
# s27 (diagnosis, 2026-11-26): build 14 s19 could not add qa-two right after s15 in both languages, and could on its own.
# Run after s15: the four files' hashes, the add's own error, a bare listing of qa-cloud, the state. Values never printed.
steps_s27() { hub; }
arm_s27() { S 'cd /storage/.config/rclone && sha256sum rclone.conf folder-profiles.json active-connection ../cloud_sync.conf 2>&1 | cut -c1-16,64- ; cd /; python3 /storage/m7-qa-d/conn.py add-two > /tmp/s27-add.out 2>&1; echo "add rc $?"; tail -n 2 /tmp/s27-add.out; rclone lsjson qa-cloud:/ --max-depth 1 2>&1 | head -c 400; echo; cloud_remote setup-info | grep -E "^(STATE|CONNECTION)="'; }
put_s27() { S 'python3 /storage/m7-qa-d/conn.py repair'; }
# s28: EDIT CONNECTION saved on a working qa-two: CONNECTION SAVED (it is not the active connection), then back (#1483 criterion 2)
steps_s28() { to_two; down 5; open; echo "shot edit-form"; echo "key up"; echo "wait-for-change 4"; echo "key up"; echo "wait-for-change 4"; echo settle; echo "shot save-row"; open; echo "shot update-confirm"; echo "key x"; echo "wait-for-change 120 1"; echo "settle 120 3"; echo "shot connection-saved"; back; echo "shot after-saved-back"; }
arm_s28() { S 'python3 /storage/m7-qa-d/conn.py add-two >/dev/null && python3 /storage/m7-qa-d/conn.py two-hash'; }
put_s28() { S 'python3 /storage/m7-qa-d/conn.py two-hash; python3 /storage/m7-qa-d/conn.py repair'; }
# s25: a fresh device: no rclone.conf and no folder-profiles.json (s15 moves only rclone.conf, which leaves a
# profile store naming qa-cloud: an inconsistent store, read as unavailable). Then the same pages as s15.
steps_s25() { steps_s15; }
arm_s25() { S "mkdir -p /storage/m7-qa-d/s25 && rm -f /storage/m7-qa-d/s25/* && cd /storage/.config/rclone && for f in rclone.conf folder-profiles.json active-connection; do [ -e \$f ] && cp -p \$f /storage/m7-qa-d/s25/; done; cp -p /storage/.config/cloud_sync.conf /storage/m7-qa-d/s25/ && ls /storage/m7-qa-d/s25 > /storage/m7-qa-d/s25.list && cd /storage/.config/rclone && rm -f rclone.conf folder-profiles.json active-connection && cloud_remote setup-info | grep -E '^STATE='"; }
put_s25() { S "cd /storage/.config/rclone && for f in folder-profiles.json active-connection; do grep -qx \$f /storage/m7-qa-d/s25.list || rm -f \$f; done; cd /storage/m7-qa-d/s25 && for f in rclone.conf folder-profiles.json active-connection; do [ -e \$f ] && cp -p \$f /storage/.config/rclone/; done; cp -p cloud_sync.conf /storage/.config/ && chmod 600 /storage/.config/rclone/rclone.conf && cloud_remote select qa-cloud; cloud_remote setup-info | grep -E '^STATE='"; }
# s26: every connection removed through the module, the player's way to an empty list; every file put back after.
steps_s26() { steps_s15; }
arm_s26() { S "mkdir -p /storage/m7-qa-d/s26 && rm -f /storage/m7-qa-d/s26/* && cd /storage/.config/rclone && for f in rclone.conf folder-profiles.json active-connection; do [ -e \$f ] && cp -p \$f /storage/m7-qa-d/s26/; done; cp -p /storage/.config/cloud_sync.conf /storage/m7-qa-d/s26/ && ls /storage/m7-qa-d/s26 > /storage/m7-qa-d/s26.list && python3 -c \"import sys; sys.path.insert(0, '/usr/bin'); import cloud_connections as c; c.remove('qa-cloud')\" && cloud_remote setup-info | grep -E '^STATE='"; }
put_s26() { S "cd /storage/.config/rclone && for f in folder-profiles.json active-connection; do grep -qx \$f /storage/m7-qa-d/s26.list || rm -f \$f; done; cd /storage/m7-qa-d/s26 && for f in rclone.conf folder-profiles.json active-connection; do [ -e \$f ] && cp -p \$f /storage/.config/rclone/; done; cp -p cloud_sync.conf /storage/.config/ && chmod 600 /storage/.config/rclone/rclone.conf && cloud_remote select qa-cloud; cloud_remote setup-info | grep -E '^STATE='"; }
arm_s17() { S "$(ctx); cloud_remote set-folder saves / \$c && cloud_remote folder-context | jq -c .paths"; }
put_s17() { put_s02; }

# s29: SIGN IN AGAIN on an OAuth-tier connection (qa-oauth, type dropbox, no sign-in), then back from the
# choice page (#1486). SIGN IN only starts the local broker; no typing method is chosen, so nothing reaches
# the provider. The put back reads the journal for the session's cancel.
steps_s29() { hub; down 9; open; echo "shot connections-oauth"; down 1; open; echo "shot oauth-page"; down 5; echo "shot signin-row"; open; echo "shot signin-confirm"; echo "key x"; echo "wait-for-change 60 1"; echo "settle 60 3"; echo "shot choice"; back; echo "wait 3"; echo settle; echo "shot after-back"; }
arm_s29() { S 'python3 /storage/m7-qa-d/conn.py add-oauth; cloud_remote list | cut -f1,2'; }
# The witness that back left the sign-in: the broker's own status (cancelled) and no broker running,
# read before this put back cancels anything. ES logs its cancel at Info, which the image does not keep.
put_s29() { S 'echo "oauth status: $(/usr/bin/cloud_oauth status 2>/dev/null)"; echo "brokers running: $(pgrep -c -f "cloud_oauth serv[e]")"; /usr/bin/cloud_oauth cancel >/dev/null 2>&1; python3 /storage/m7-qa-d/conn.py remove-oauth; cloud_remote list | cut -f1,2'; }

SCREENS="s01 s02 s03 s04 s05 s06 s07 s08 s09 s10 s11 s12 s13 s14 s15 s16 s17 s18 s19 s20 s21 s22 s23 s24 s25 s26 s27 s28 s29"
[ -n "$only" ] && SCREENS=${only//,/ }

log "== #1111/#1115 phase D at $res, $(date -u +%FT%TZ)"
pgrep -f 'qemu-system-x86_6[4]' >/dev/null && die "a QEMU guest is up; bring the pair down first"
( cd "$round" && VM_RES=$res timeout 900 tools/vm-pair up "$image" ) > "$out/vm-pair-up.log" 2>&1 || die "vm-pair up failed"
S 'grep -E "^(BUILD_ID|VERSION)=" /etc/os-release' | tee -a "$out/RESULT.txt" > "$out/os-release.txt" || die "no guest"
conf=$(mktemp); chmod 600 "$conf"
"$round/tools/cloud-test-backend" rclone-conf > "$conf" 2>/dev/null && grep -q '^type = webdav' "$conf" || { rm -f "$conf"; die "no QA stanza"; }
S 'mkdir -p /storage/.config/rclone'
scp -q "${SCPO[@]}" "$conf" root@127.0.0.1:/storage/.config/rclone/rclone.conf < /dev/null; rc=$?; rm -f "$conf"; [ "$rc" = 0 ] || die "stanza copy failed"
saves=$("$round/tools/cloud-test-backend" shipped-default SAVES_REMOTE) && backups=$("$round/tools/cloud-test-backend" shipped-default SETTINGS_REMOTE) || die "no shipped defaults"
S "chmod 600 /storage/.config/rclone/rclone.conf; cloud_sync_helper >/dev/null 2>&1; r=\$(cloud_remote active); rclone mkdir \"\${r}$saves\"; rclone mkdir \"\${r}$backups\"; cloud_remote folder-context | jq -c '{connection,paths}'" | tee -a "$out/RESULT.txt"
S 'mkdir -p /storage/m7-qa-d'; scp -q "${SCPO[@]}" "$(dirname "$0")/conn.py" root@127.0.0.1:/storage/m7-qa-d/conn.py < /dev/null || die "conn.py copy failed"
CLEAN='STATE=selected CONNECTION=qa-cloud SECTIONS=qa-cloud SYNC=off/off'
clean_state() {  # every screen starts from one selected qa-cloud, sync off (cal-640-en: s08 left review)
    local st; st=$(S 'python3 /storage/m7-qa-d/conn.py state' 2>&1)
    [ "$st" = "$CLEAN" ] && return 0
    log "   state before $1: $st -- repairing"
    st=$(S 'python3 /storage/m7-qa-d/conn.py repair' 2>&1)
    [ "$st" = "$CLEAN" ] || { log "   still not clean: $st"; return 1; }
}
reboot_guest() {
    local b0 b i; b0=$(S 'cat /proc/sys/kernel/random/boot_id')
    S 'sync; systemctl reboot' >/dev/null 2>&1
    for i in $(seq 1 60); do sleep 5; b=$(S 'cat /proc/sys/kernel/random/boot_id' 2>/dev/null); [ -n "$b" ] && [ "$b" != "$b0" ] && break; done
    [ -n "${b:-}" ] && [ "$b" != "$b0" ] || return 1
    for i in $(seq 1 60); do S 'pgrep -x emulationstation >/dev/null' && break; sleep 3; done; sleep 15
}
failed=0
for lang in ${langs//,/ }; do
    case "$lang" in en) code=en_US ;; fr) code=fr_FR ;; *) die "language $lang" ;; esac
    S "systemctl stop essway; set_setting system.language $code" >/dev/null 2>&1
    reboot_guest || die "the guest did not come back for $lang"
    mkdir -p "$out/$lang"
    for s in $SCREENS; do
        log "-- $lang $s"
        clean_state "$s" || { failed=1; continue; }
        # An arm that fails leaves the screen in the wrong state, so its rc is
        # recorded and fails the run -- unless the screen exists to show the
        # refusal (s17's arm was refused before this check existed and the
        # walk ran on regardless).
        echo "arm:" >> "$out/$lang/$s.arm.log"; "arm_$s" >> "$out/$lang/$s.arm.log" 2>&1; arc=$?
        armok=1
        case " $ARM_REFUSED " in
            *" $s "*) [ "$arc" != 0 ] || { log "   arm rc 0, but $s expects a refusal"; failed=1; armok=0; } ;;
            *) [ "$arc" = 0 ] || { log "   arm rc $arc (see $lang/$s.arm.log); walk skipped"; failed=1; armok=0; } ;;
        esac
        # A screen whose state was not set up is not walked: build 14's s19, with
        # no qa-two, walked into a provider form and pressed CONNECT (2026-11-26).
        if [ "$armok" = 0 ]; then
            { echo "put back:"; "put_$s" 2>&1; } >> "$out/$lang/$s.arm.log"
            continue
        fi
        "steps_$s" > "$out/$lang/$s.steps"
        timeout 600 "$round/tools/vm-visual-qa" --monitor "$MON" run "$out/$lang/$s.steps" --outdir "$out/$lang/$s" > "$out/$lang/$s.log" 2>&1
        rc=$?; [ "$rc" = 0 ] || { log "   walk rc $rc (see $lang/$s.log)"; failed=1; }
        # A screen that changes state part-way: mid_<s> runs with the first
        # walk's page still open, then steps2_<s> continues into <s>-b/.
        if [ "$rc" = 0 ] && declare -F "steps2_$s" >/dev/null; then
            echo "mid:" >> "$out/$lang/$s.arm.log"; "mid_$s" >> "$out/$lang/$s.arm.log" 2>&1 \
                || { log "   mid rc $? (see $lang/$s.arm.log)"; failed=1; }
            "steps2_$s" > "$out/$lang/$s-b.steps"
            timeout 600 "$round/tools/vm-visual-qa" --monitor "$MON" run "$out/$lang/$s-b.steps" --outdir "$out/$lang/$s-b" > "$out/$lang/$s-b.log" 2>&1
            rc=$?; [ "$rc" = 0 ] || { log "   walk rc $rc (see $lang/$s-b.log)"; failed=1; }
        fi
        { echo "put back:"; "put_$s" 2>&1; } >> "$out/$lang/$s.arm.log"
        # A walk that went astray can leave a form, a keyboard or a game list
        # open that the reset below does not close, and every later screen
        # then starts in the wrong place (s19 -> s20, 2026-11-26): reboot.
        [ "$rc" = 0 ] || reboot_guest || die "the guest did not come back after $lang $s"
        echo -e "wake\ndismiss-dialogs" | timeout 120 "$round/tools/vm-visual-qa" --monitor "$MON" run - --outdir "$out/$lang/$s-reset" > /dev/null 2>&1
        rm -rf "${out:?}/$lang/$s-reset"
    done
done
S "set_setting system.language en_US" >/dev/null 2>&1
( cd "$round" && tools/vm-pair down ) >> "$out/vm-pair-up.log" 2>&1
[ "$failed" = 0 ] && { log "PASSED (every walk ran; the frames are for review)"; exit 0; }
log "FAILED"; exit 1
