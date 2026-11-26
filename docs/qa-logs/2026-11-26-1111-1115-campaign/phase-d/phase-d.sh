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

SCREENS="s01 s02 s03 s04 s05 s06 s07 s08 s09 s10 s11 s12 s13"
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
        { echo "arm:"; "arm_$s" 2>&1; } >> "$out/$lang/$s.arm.log"
        "steps_$s" > "$out/$lang/$s.steps"
        timeout 600 "$round/tools/vm-visual-qa" --monitor "$MON" run "$out/$lang/$s.steps" --outdir "$out/$lang/$s" > "$out/$lang/$s.log" 2>&1
        rc=$?; [ "$rc" = 0 ] || { log "   walk rc $rc (see $lang/$s.log)"; failed=1; }
        { echo "put back:"; "put_$s" 2>&1; } >> "$out/$lang/$s.arm.log"
        echo -e "wake\ndismiss-dialogs" | timeout 120 "$round/tools/vm-visual-qa" --monitor "$MON" run - --outdir "$out/$lang/$s-reset" > /dev/null 2>&1
        rm -rf "${out:?}/$lang/$s-reset"
    done
done
S "set_setting system.language en_US" >/dev/null 2>&1
( cd "$round" && tools/vm-pair down ) >> "$out/vm-pair-up.log" 2>&1
[ "$failed" = 0 ] && { log "PASSED (every walk ran; the frames are for review)"; exit 0; }
log "FAILED"; exit 1
