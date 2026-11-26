#!/bin/bash
# #1427 criteria 2-4 on a QA guest: COPY TO FREE SLOT from an AUTO SAVE that
# is the game's only state, through the manager's own north press.
#
#   free-slot-proof.sh --port 10022 --identity /tmp/rocknix-vm-pair/qa-key \
#       --monitor /tmp/rocknix-qemu-monitor.sock --round <round worktree> --outdir DIR
#
# The guest is a fresh vm-pair guest (no saves of its own). The game is a
# 32 KiB Game Boy ROM built here at run time, tools/ra-auto-slot-test's
# SlotProbe, so the core makes a real state. Other saves, a control set
# for a second game, are seeded first and must come through byte for byte.
#
#   1  a real AUTO SAVE: launch through the interface's API, RetroArch's clean
#      exit (SIGTERM, what the exit hotkey sends) writes SlotProbe.state.auto
#   2  negative: the transfer lock held, the north press on AUTO SAVE says a
#      sync is running and copies nothing
#   3  the north press with the lock free: SlotProbe.state appears, the same
#      bytes as the AUTO SAVE; the AUTO SAVE and every control file unchanged
#   4  reboot, reopen the manager: the copy is a tile, its bytes unchanged
#   5  a controlled exit replaces the AUTO SAVE; the copy is unchanged
#   6  the copy's tile, LAUNCH: RetroArch loads SlotProbe.state, and the copy
#      is unchanged after that session's exit
#
# Every step snapshots sha256 of the saves trees and of the capture records
# under /storage/.cache/cloud_sync (names and hashes only). Frames are under
# <step>/ for review against the flow. QA guest only.
# Exit 0 every check passed, 1 one did not, 2 cannot run.
set -uo pipefail
port= identity= monitor= round= out=
while [ "$#" -ge 2 ]; do
    case "$1" in
        --port) port=$2 ;; --identity) identity=$2 ;; --monitor) monitor=$2 ;;
        --round) round=$2 ;; --outdir) out=$2 ;;
        *) echo "usage: $0 --port P --identity KEY --monitor SOCK --round TREE --outdir DIR" >&2; exit 2 ;;
    esac
    shift 2
done
[[ $port =~ ^[1-9][0-9]{0,4}$ ]] && [ -r "$identity" ] && [ -S "$monitor" ] && [ -x "$round/tools/vm-visual-qa" ] && [ -n "$out" ] ||
    { echo "usage: $0 --port P --identity KEY --monitor SOCK --round TREE --outdir DIR" >&2; exit 2; }
! [ -e "$out" ] || { echo "cannot run: $out exists" >&2; exit 2; }
mkdir -p "$out" || exit 2
out=$(cd "$out" && pwd)
SSHO=(-F /dev/null -p "$port" -i "$identity" -o IdentitiesOnly=yes -o BatchMode=yes
      -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=10)
SCPO=(-F /dev/null -P "$port" -i "$identity" -o IdentitiesOnly=yes -o BatchMode=yes
      -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=10)
S() { timeout 120 ssh -n "${SSHO[@]}" root@127.0.0.1 ". /etc/profile >/dev/null 2>&1; $*"; }
log() { echo "$*" | tee -a "$out/RESULT.txt"; }
fails=0
check() { if [ "$1" = 0 ]; then log "  PASS  $2"; else log "  FAIL  $2"; fails=$((fails+1)); fi; }
die() { log "CANNOT RUN: $*"; exit 2; }

G=/storage/roms/gb; ST=/storage/roms/savestates/gb; ROM=$G/SlotProbe.gb
AUTO=$ST/SlotProbe.state.auto; COPY=$ST/SlotProbe.state

walk() {  # walk <outdir name> <step line>...
    local name=$1; shift
    printf '%s\n' "$@" | timeout 300 "$round/tools/vm-visual-qa" --monitor "$monitor" run - --outdir "$out/$name" \
        > "$out/$name.log" 2>&1
}
# The way to the manager from the gb carousel (StartupSystem gb): A to the
# list, north for GAME OPTIONS, A for the manager (tools/vm-walks/manager.steps).
TO_MANAGER=("settle" "shot 0-carousel" "key x" "wait-for-change" "settle" "shot 1-list"
            "key s" "wait-for-change 6" "settle" "shot 2-game-options" "key x" "wait-for-change 10" "settle 10 2" "shot 3-manager")
snap() {  # snap <label>: what is on disk, by hash
    S "cd /storage/roms/savestates && find . -type f -exec sha256sum {} + | sort -k2" > "$out/$1-saves.txt" 2>/dev/null
    S "cd $G && sha256sum * 2>/dev/null | sort -k2; cd /storage/roms/nes && sha256sum * 2>/dev/null | sort -k2" > "$out/$1-roms.txt" 2>/dev/null
    S "cd /storage/.cache/cloud_sync 2>/dev/null && find . -type f -exec sha256sum {} + | sort -k2" > "$out/$1-records.txt" 2>/dev/null
    S "cd $ST && stat -c '%Y %n' *" > "$out/$1-ls.txt" 2>/dev/null
}
h() { awk -v f="./gb/$1" '$2 == f {print $1}' "$out/$2-saves.txt"; }
controls() { grep -v '/gb/' "$out/$1-saves.txt"; }
idle() { local i; for i in $(seq 1 ${1:-90}); do [ "$(S "curl -s -o /dev/null -w '%{http_code}' -m 5 http://127.0.0.1:1234/isIdle")" = 200 ] && return 0; sleep 1; done; return 1; }
reboot_guest() {
    local b0 b i; b0=$(S 'cat /proc/sys/kernel/random/boot_id')
    S 'sync; systemctl reboot' >/dev/null 2>&1
    for i in $(seq 1 60); do sleep 5; b=$(S 'cat /proc/sys/kernel/random/boot_id' 2>/dev/null); [ -n "$b" ] && [ "$b" != "$b0" ] && break; done
    [ -n "$b" ] && [ "$b" != "$b0" ] || return 1
    idle 180 || return 1; sleep 10
}
running() { S 'pgrep -f "^/usr/bin/retroarc[h]" >/dev/null'; }
wait_core() {  # until RetroArch has started and run its core a while
    local i t up=0
    for i in $(seq 1 45); do running && break; sleep 2; done
    running || return 1
    for i in $(seq 1 40); do
        t=$(S 'p=$(pgrep -f "^/usr/bin/retroarc[h]" | head -1); [ -n "$p" ] && awk "{print \$14+\$15}" /proc/$p/stat 2>/dev/null || echo 0' | tr -d '\r'); t=${t:-0}
        [ "$t" -ge 200 ] && break; [ "$t" -gt 0 ] && up=$((up+1)); [ "$up" -ge 4 ] && [ "$t" -ge 30 ] && break
        sleep 1
    done
    sleep 3
}
quit() {  # RetroArch's clean exit, then until runemu.sh has returned
    S "pkill -TERM -f '^/usr/bin/retroarc[h]'" >/dev/null 2>&1
    local i; for i in $(seq 1 30); do S 'pgrep -f "^/usr/bin/retroarc[h]" >/dev/null || pgrep -f "/usr/bin/runemu[.]sh" >/dev/null' || return 0; sleep 1; done; return 1
}
loads() { S "grep -a -o 'Loading state \"[^\"]*\"' /var/log/exec.log 2>/dev/null"; }

log "== #1427 free-slot proof, $(date -u +%FT%TZ)"
S 'grep -E "^(BUILD_ID|VERSION|BUILD_BRANCH)=" /etc/os-release' | tee -a "$out/RESULT.txt" "$out/os-release.txt" >/dev/null
S 'test -d /storage/roms' || die "the guest does not answer"
S "test ! -e $ST || test -z \"\$(ls -A $ST)\"" || die "$ST is not empty: use a fresh guest"

# The game, and a control set of another game's saves the proof must not touch.
python3 - "$out/SlotProbe.gb" <<'PY'
import sys
rom = bytearray(0x8000)
rom[0x100:0x104] = bytes([0x00, 0xC3, 0x50, 0x01])
rom[0x104:0x134] = bytes.fromhex("CEED6666CC0D000B03730083000C000D0008111F8889000EDCCC6EE6DDDDD999BBBB67636E0EECCCDDDC999FBBB9333E")
rom[0x134:0x13D] = b"SLOTPROBE"
rom[0x147] = 0x03; rom[0x148] = 0x00; rom[0x149] = 0x02; rom[0x14A] = 0x01; rom[0x14B] = 0x33
x = 0
for i in range(0x134, 0x14D):
    x = (x - rom[i] - 1) & 0xFF
rom[0x14D] = x
code = bytes([0xF3, 0x3E, 0x0A, 0xEA, 0x00, 0x00, 0x3E, 0x55, 0xEA, 0x00, 0xA0, 0x18, 0xFE])
rom[0x150:0x150+len(code)] = code
open(sys.argv[1], "wb").write(rom)
PY
scp -q "${SCPO[@]}" "$out/SlotProbe.gb" root@127.0.0.1:/tmp/SlotProbe.gb || die "copy of the ROM failed"
S "mkdir -p $G $ST /storage/roms/nes /storage/roms/savestates/nes && mv /tmp/SlotProbe.gb $ROM &&
   head -c 4096 /dev/urandom > /storage/roms/nes/Ctrl.nes && head -c 8192 /dev/urandom > /storage/roms/nes/Ctrl.srm &&
   for f in Ctrl.state.auto Ctrl.state.auto.png Ctrl.state2 Ctrl.state2.png; do head -c 4096 /dev/urandom > /storage/roms/savestates/nes/\$f; done; sync" ||
    die "seeding failed"
# The VM draws with GL (RetroArch's default Vulkan has no device in QEMU), and
# the carousel opens on gb. Both take effect at the next start.
S 'sed -i "s/^video_driver = .*/video_driver = \"gl\"/" /storage/.config/retroarch/retroarch.cfg &&
   systemctl stop essway && sed -i "s|</config>|\t<string name=\"StartupSystem\" value=\"gb\" />\n</config>|" /storage/.config/emulationstation/es_settings.cfg && sync' ||
    die "the guest settings could not be written"
S 'grep -q "name=\"StartupSystem\" value=\"gb\"" /storage/.config/emulationstation/es_settings.cfg &&
   grep -q "^video_driver = \"gl\"" /storage/.config/retroarch/retroarch.cfg' ||
    die "StartupSystem gb or the GL driver did not land (es_settings.cfg or retroarch.cfg missing a line)"
S 'get_setting global.autosave; get_setting gb.autosave; get_setting global.incrementalsavestates' > "$out/settings.txt" 2>&1
reboot_guest || die "the guest did not come back after the first reboot"
snap 0-seeded

log "1. a real AUTO SAVE"
S 'rm -f /var/log/exec.log'
S "curl -s -o /dev/null -m 20 -X POST -H 'Content-Type: text/plain' --data '$ROM' http://127.0.0.1:1234/launch"
wait_core || die "RetroArch never started for the first run (see the guest's /var/log/exec.log)"
quit || die "RetroArch did not exit on SIGTERM"
sleep 3
snap 1-autosave
[ -n "$(h SlotProbe.state.auto 1-autosave)" ] || die "no SlotProbe.state.auto after the first run"
[ -z "$(h SlotProbe.state 1-autosave)" ] || die "a SlotProbe.state exists before any copy"
log "  SlotProbe.state.auto $(h SlotProbe.state.auto 1-autosave | cut -c1-16), thumbnail $(h SlotProbe.state.auto.png 1-autosave | cut -c1-16)"

reboot_guest || die "the guest did not come back before the manager"
walk 2-manager "${TO_MANAGER[@]}" "key right" "wait-for-change 4" "settle" "shot 4-auto-save-tile" ||
    die "the walk to the manager failed (2-manager.log)"

log "2. the transfer lock held: the north press refuses and copies nothing"
S 'nohup flock /var/run/cloud_sync.lock sleep 45 >/dev/null 2>&1 & sleep 1; flock -n /var/run/cloud_sync.lock true && echo FREE || echo HELD' > "$out/2-lock.txt"
grep -q HELD "$out/2-lock.txt" || die "the lock could not be held ($(cat "$out/2-lock.txt"))"
walk 2-locked "key s" "wait-for-change 6" "settle" "shot 5-lock-held-answer" "key x" "wait-for-change 4" "settle" "shot 6-after-ok" ||
    die "the locked press walk failed (2-locked.log)"
snap 2-locked
[ -z "$(h SlotProbe.state 2-locked)" ]; check $? "no SlotProbe.state while the lock is held"
[ "$(h SlotProbe.state.auto 2-locked)" = "$(h SlotProbe.state.auto 1-autosave)" ]; check $? "the AUTO SAVE unchanged by the refused press"
for i in $(seq 1 60); do S 'flock -n /var/run/cloud_sync.lock true' && break; sleep 1; done
S 'flock -n /var/run/cloud_sync.lock true' || die "the lock was not released"

log "3. the north press with the lock free"
walk 3-copy "key s" "wait-for-change 8" "shot 7-copy-answer" "settle" "shot 8-copy-settled" ||
    die "the copy walk failed (3-copy.log)"
sleep 3
snap 3-copied
a1=$(h SlotProbe.state.auto 1-autosave); a3=$(h SlotProbe.state.auto 3-copied); c3=$(h SlotProbe.state 3-copied)
[ -n "$c3" ]; check $? "SlotProbe.state (slot 0) exists after the press"
[ "$c3" = "$a1" ]; check $? "the copy has the AUTO SAVE's bytes ($(echo "$c3" | cut -c1-16))"
[ "$a3" = "$a1" ]; check $? "the AUTO SAVE unchanged by the copy"
if [ -n "$(h SlotProbe.state.auto.png 1-autosave)" ]; then
    [ "$(h SlotProbe.state.png 3-copied)" = "$(h SlotProbe.state.auto.png 1-autosave)" ]; check $? "the copy's thumbnail has the AUTO SAVE thumbnail's bytes"
fi
diff <(controls 0-seeded) <(controls 3-copied) > "$out/3-controls.diff"; check $? "every control save unchanged"
diff "$out/1-autosave-records.txt" "$out/3-copied-records.txt" > "$out/3-records.diff"
grep -q '^>' "$out/3-records.diff"; check $? "a capture record was written for the copy (3-records.diff)"
S "grep -a -E 'adopt|SlotProbe' /var/log/cloud_sync.log 2>/dev/null | tail -5" | grep -v -i -E 'key|pass|token|user|psk' > "$out/3-cloud_sync-log.txt"
walk 3-out "key z" "wait-for-change" "settle" "dismiss-dialogs" >/dev/null

log "4. reboot, reopen: the copy is still there"
reboot_guest || die "the guest did not come back before the reopen"
walk 4-reopen "${TO_MANAGER[@]}" "key right" "wait-for-change 4" "settle" "shot 4-second-tile" "key right" "wait-for-change 4" "settle" "shot 5-third-tile" \
    "key z" "wait-for-change" "settle" "dismiss-dialogs" || die "the reopen walk failed (4-reopen.log)"
snap 4-reopened
[ "$(h SlotProbe.state 4-reopened)" = "$c3" ]; check $? "the copy unchanged after a reboot and a reopen"

log "5. a controlled exit replaces the AUTO SAVE"
S 'rm -f /var/log/exec.log'
idle 60
S "curl -s -o /dev/null -m 20 -X POST -H 'Content-Type: text/plain' --data '$ROM' http://127.0.0.1:1234/launch"
wait_core || die "RetroArch never started for the second run"
quit || die "RetroArch did not exit on SIGTERM (second run)"
sleep 3
loads > "$out/5-loads.txt"
snap 5-exited
a5=$(h SlotProbe.state.auto 5-exited)
grep -q "SlotProbe.state.auto" "$out/5-loads.txt"; check $? "the second run started from the AUTO SAVE ($(tr '\n' ' ' < "$out/5-loads.txt"))"
if [ "$a5" != "$a1" ]; then check 0 "the AUTO SAVE was replaced by the exit ($(echo "$a5" | cut -c1-16))"
else
    m1=$(awk '$2 == "SlotProbe.state.auto" {print $1}' "$out/1-autosave-ls.txt"); m5=$(awk '$2 == "SlotProbe.state.auto" {print $1}' "$out/5-exited-ls.txt")
    [ "$m1" != "$m5" ]; check $? "the AUTO SAVE was rewritten by the exit (the same bytes; mtime $m1 -> $m5)"
fi
[ "$(h SlotProbe.state 5-exited)" = "$c3" ]; check $? "the copy unchanged by the exit"
diff <(controls 0-seeded) <(controls 5-exited) > "$out/5-controls.diff"; check $? "every control save unchanged"

log "6. LAUNCH from the copy"
reboot_guest || die "the guest did not come back before the slot launch"
walk 6-to-slot "${TO_MANAGER[@]}" "key right" "wait-for-change 4" "settle" "key right" "wait-for-change 4" "settle" "shot 4-slot-tile" ||
    die "the walk to the slot failed (6-to-slot.log)"
S 'rm -f /var/log/exec.log'
walk 6-launch "key x" "wait 2" || true
wait_core || die "RetroArch never started from the slot tile (6-to-slot/4-slot-tile.png says which tile)"
"$round/tools/vm-visual-qa" --monitor "$monitor" shot "$out/6-in-game.png" >/dev/null 2>&1
loads > "$out/6-loads.txt"
S "grep -a -E 'setsettings|state_slot' /var/log/exec.log 2>/dev/null | tail -4" | grep -v -i -E 'key|pass|token|user|psk' > "$out/6-launch-lines.txt"
quit || die "RetroArch did not exit on SIGTERM (slot run)"
sleep 3
snap 6-after-slot
grep -q 'SlotProbe.state"' "$out/6-loads.txt"; check $? "RetroArch loaded SlotProbe.state ($(tr '\n' ' ' < "$out/6-loads.txt"))"
[ "$(h SlotProbe.state 6-after-slot)" = "$c3" ]; check $? "the copy unchanged after its own session"
diff <(controls 0-seeded) <(controls 6-after-slot) > "$out/6-controls.diff"; check $? "every control save unchanged"

[ "$fails" = 0 ] && { log PASSED; exit 0; }
log "FAILED ($fails)"; exit 1
