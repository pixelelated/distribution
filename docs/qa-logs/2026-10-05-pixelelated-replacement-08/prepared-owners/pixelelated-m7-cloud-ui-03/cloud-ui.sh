#!/bin/bash
# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2026-present rasteratops (https://github.com/rasteratops)
# The cloud epic's guest-d proof, promoted from run101 (#365).
# Requires an isolated GENERIC_X64 guest d and the synthetic WebDAV backend.
# Usage: tools/rasteratops-vm-cloud-epic --output DIR [--case CASE]
# Cases: A B C D E F G H I J K L T08 T11 T12 T17 T19 T23 T26
# --inject-failure exercises the exact assertion/exit path without a guest.
set -uo pipefail
R=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement08
P=""; requested="UI17 UI26"; injected=0
while [ $# -gt 0 ]; do
 case "$1" in
  --output) P="$2"; shift 2;; --case) requested="$2"; shift 2;;
  --inject-failure) injected=1; shift;;
  --help) sed -n '4,8p' "$0"; exit 0;;
  *) echo "unknown argument: $1" >&2; exit 2;;
 esac
done
[ -n "$P" ] || { echo '--output DIR is required' >&2; exit 2; }
mkdir -p "$P/logs" "$P/frames"; P=$(cd "$P" && pwd)
PASSES=0; FAILS=0; ITEM=cloud-epic; LOG="$P/logs/run.log"; FR="$P/frames"
say() { printf '%s %s\n' "$(date -u +%T)" "$*" | tee -a "$LOG"; }
check() { if [ "$1" = 0 ]; then say "PASS $2"; PASSES=$((PASSES+1)); else say "FAIL $2"; FAILS=$((FAILS+1)); fi; }
done_line() { say "done: $PASSES PASS, $FAILS FAIL"; }
if [ "$injected" = 1 ]; then check 1 'constructed assertion failure'; done_line; [ "$FAILS" -eq 0 ]; exit $?; fi
# Every letter is a separate process and fresh fixture, so ordering cannot rescue a case.
if [ -z "${PROOF_CASE:-}" ]; then
 total_rc=0
 for letter in $requested; do
  case "$letter" in UI17|UI26) ;; *) echo "unknown case $letter" >&2; exit 2;; esac
  PROOF_CASE="$letter" "$0" --output "$P/$letter" --case "$letter" || total_rc=1
 done
 exit "$total_rc"
fi
CASES="$PROOF_CASE"
PORT=10026; MON=/tmp/rocknix-qemu-monitor-d.sock; VNC=127.0.0.1:5912
KEY="${VM_PAIR_DIR:-/tmp/rocknix-vm-pair}/qa-key"
VQ="$R/tools/vm-visual-qa"
DATA="${CLOUD_QA_STATE:-$HOME/.cache/rocknix-cloud-qa}/data"
# The runner has no hostname flag: all writes are confined to guest d and the local QA backend.
[ -S "$MON" ] && [ -s /tmp/rocknix-qemu-d.pid ] && [ -f "$KEY" ] || { say 'guest d prerequisites absent'; exit 2; }
qa_pid=$(cat /tmp/rocknix-qemu-d.pid)
[[ "$qa_pid" =~ ^[0-9]+$ ]] && [ -r "/proc/$qa_pid/cmdline" ] && tr '\0' '\n' < "/proc/$qa_pid/cmdline" | grep -q 'qemu-system-x86_64' || { say 'guest pidfile is not a QEMU process'; exit 2; }
[ "${CLOUD_QA_BACKEND:-webdav}" = webdav ] && [ -d "$DATA" ] && [ ! -L "$DATA" ] || { say 'requires isolated WebDAV QA data'; exit 2; }
GRABPID=""
cleanup() {
 [ -z "${SSHPID:-}" ] || { kill "$SSHPID" 2>/dev/null || :; wait "$SSHPID" 2>/dev/null || :; }
 [ -z "$GRABPID" ] || { kill "$GRABPID" 2>/dev/null || :; wait "$GRABPID" 2>/dev/null || :; }
 if declare -F protocol_cleanup >/dev/null; then protocol_cleanup; fi
}
trap cleanup EXIT INT TERM
walk() {
 local rc
 "$VQ" --monitor "$MON" run "$1" --outdir "$2" >> "$LOG" 2>&1; rc=$?
 check "$rc" "walk $(basename "$1")"
 [ "$rc" -eq 0 ] || { done_line; exit 1; }
}
settle() { "$VQ" --monitor "$MON" settle >> "$LOG" 2>&1; }
grab_start() {
 mkdir -p "$FR/$1"; rm -f "$FR/$1.stop"
 python3 "$R/tools/vm-walks/cloud-epic/vnc-grab.py" "$VNC" "$FR/$1" "$1" "$FR/$1.stop" "${2:-0.7}" > "$FR/$1.capture.log" 2>&1 &
 GRABPID=$!; printf '%s\n' "$GRABPID" > "$FR/$1.capture.pid"
}
grab_stop() { touch "$FR/$1.stop"; [ -z "$GRABPID" ] || wait "$GRABPID"; GRABPID=""; }
wait_card() {
 local i n
 for i in $(seq 1 60); do
  n=$(G_ "pgrep -f 'cloud_backu[p]|cloud_restor[e]|rclon[e] ' | wc -l") || return 1
  [ "$n" = 0 ] && break; sleep 1
 done
 sleep "${1:-6}"
}

mask() { grep -v -i -E 'key|pass|token|user|psk'; }                                   # config dumps
maskl() { sed -E 's/((token|key|passw[a-z]*|psk|user|[?&]u|[?&]t|[?&]p)[=:])[^ &]*/\1***/Ig'; }   # the value masked, the key kept
MONC() { printf '%s\n' "$1" | socat -t 1 - "UNIX-CONNECT:$MON" >/dev/null 2>&1; }
G_() { ssh -n -i $KEY -p $PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o BatchMode=yes -o ConnectTimeout=8 root@127.0.0.1 "$@"; }
require_no_game() { G_ "! pgrep -f 'retroarc[h] -L' >/dev/null"; }
boot_id() { G_ 'cat /proc/sys/kernel/random/boot_id' 2>/dev/null; }
reboot_guest() { local b0; b0=$(boot_id); G_ 'sync; reboot' >/dev/null 2>&1; sleep 20
  local i; for i in $(seq 1 60); do [ -n "$(boot_id)" ] && [ "$(boot_id)" != "$b0" ] && break; sleep 3; done
  [ "$(boot_id)" != "$b0" ] || { say "  reboot: boot id did not change"; return 1; }
  for i in $(seq 1 40); do G_ 'pgrep -x emulationstation >/dev/null && curl -s -o /dev/null -m 3 http://127.0.0.1:1234/caps' 2>/dev/null && break; sleep 3; done
  sleep 15; require_no_game
  # and the boot's own work done before a script walks: the hasher and the top-up (/isIdle), the startup sync's card
  # (wait_card), a still screen (settle) -- run 5's E2-pl062 pressed START into a fading card, E2-pl068 walked a page
  # that was still loading, E2-pl061 launched under the hasher (D-QA-057, blindspot 64)
  local j idle=no; for j in $(seq 1 120); do [ "$(G_ "curl -s -o /dev/null -w '%{http_code}' -m 5 http://127.0.0.1:1234/isIdle")" = 200 ] && { idle=yes; break; }; sleep 1; done
  echo "$(date +%T)   reboot_guest: /isIdle $idle after ${j}s" >> "$LOG"; wait_card 3; settle; sleep 3; }
debug_reboot() { G_ 'systemctl stop essway; f=/storage/.config/emulationstation/es_settings.cfg; if grep -q "name=\"Debug\"" $f; then sed -i "s|<bool name=\"Debug\" value=\"[a-z]*\" />|<bool name=\"Debug\" value=\"true\" />|" $f; else sed -i "s|</config>|  <bool name=\"Debug\" value=\"true\" />\n</config>|" $f; fi; grep -c "name=\"Debug\" value=\"true\"" $f; sync' >/dev/null 2>&1; reboot_guest; }
CONF=/storage/.config/cloud_sync.conf; LABEL=GENERIC-X64
say "=== $ITEM on guest d, $(G_ 'grep -h ^BUILD_ID /etc/os-release; grep -c . /usr/bin/cloud_scan 2>/dev/null')"
conf() { G_ "sed -i -e 's|^SAVES_REMOTE=.*|SAVES_REMOTE=\"$1\"|' -e 's|^SETTINGS_REMOTE=.*|SETTINGS_REMOTE=\"$2\"|' -e 's|^CONTENT_REMOTE=.*|CONTENT_REMOTE=\"$3\"|' -e 's|^LAYOUT_KEEP=.*|LAYOUT_KEEP=\"\"|' $CONF; rm -rf /storage/.cache/cloud_sync/scan; grep -E '^(SAVES|SETTINGS|CONTENT)_REMOTE=|^LAYOUT_KEEP=' $CONF | tr '\n' ' '"; }
# the walk to the hub: MAIN MENU opens on GAME SETTINGS, or on RETROACHIEVEMENTS when the guest is signed in (one down
# first, guest-facts-that-break-proofs), then RESTORE or BACK UP, the scan page framed twice while it runs, then whatever
# follows it
RA_DOWN=$(G_ '. /etc/profile >/dev/null 2>&1; [ "$(get_setting global.retroachievements)" = 1 ] && printf "key down\nwait-for-change\n"')
to_page() { # <restore|backup> <tag>
  local f=$P/epic-$2.steps
  { printf 'wake\ndismiss-dialogs\nkey ret\nwait-for-change\nsettle\n%skey x\nwait-for-change\nsettle\nkey up\nwait-for-change\nkey up\nwait-for-change\nkey up\nwait-for-change\nsettle\nkey x\nwait-for-change\nsettle\nshot %s-hub\n' "$RA_DOWN" "$2"
    [ "$1" = restore ] && printf 'key down\nwait-for-change\n'
    printf 'key x\nwait-for-change\nshot %s-scan-0\nwait 1.5\nshot %s-scan-1\nsettle 90 3\nshot %s-after-scan\n' "$2" "$2" "$2"; } > "$f"
  walk "$f" "$FR"
}
steps() { local f=$P/epic-$1.steps; shift; printf '%s\n' "$@" | sed '/^$/d' > "$f"; walk "$f" "$FR"; }
host_tree() { (cd "$DATA" && find . -type f | sort | sed 's|^\./||' | tr '\n' ' '); }

# CASES is one independently reset case.
# The systems page remembers the picks (cloudsync.pick.restore.*), so a walk that ticks ROMS AND BIOS leaves it on
# for the next; written with the interface stopped (it writes its settings back as it stops), then started again
reset_picks() {
  G_ "systemctl stop essway; sleep 2; . /etc/profile >/dev/null 2>&1; for k in content media settings; do set_setting cloudsync.pick.restore.\$k 0; done; set_setting cloudsync.pick.restore.saves 1" >/dev/null 2>&1
  G_ 'systemctl start essway' >/dev/null 2>&1; sleep 25; require_no_game >/dev/null 2>&1; say "  picks reset: $(G_ '. /etc/profile >/dev/null 2>&1; echo content=$(get_setting cloudsync.pick.restore.content) saves=$(get_setting cloudsync.pick.restore.saves)')"; }
want() { case " $CASES " in *" $1 "*) return 0;; esac; return 1; }
# the interface's Info lines need Debug=true at that boot (debug_reboot); read before the next reboot wipes them
esl() { G_ "grep -a -E \"$1\" /var/log/es_log.txt 2>/dev/null" | maskl; }
# a boot with the step's frames: Debug set, the reboot, frames over VNC through the boot and the waiter's wait
boot_frames() { # <tag> <seconds after the guest is idle>
  grab_start "$1" 0.7; debug_reboot; sleep "$2"; grab_stop "$1"; require_no_game >/dev/null 2>&1
  say "  $1: $(ls "$FR/$1" 2>/dev/null | wc -l) frames under $FR/$1"; }
G_ 'systemctl stop essway; . /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; rm -f /storage/.config/.restore-finish-pending /storage/.config/cloud-layout-migration.json; rm -rf /storage/.cache/cloud_sync/scan; find /storage/roms -type f -name "*.srm" -delete' >/dev/null || exit 2
say "== setup: the QA remote on the guest (the host backend's conf), then the QA cloud holds the fork's earlier layout with files in every folder of ours; the guest points at it"
"$R/tools/cloud-test-backend" rclone-conf > $P/epic-rclone.conf && scp -q -i $KEY -P $PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR $P/epic-rclone.conf root@127.0.0.1:/tmp/rclone.conf; rm -f $P/epic-rclone.conf
G_ 'mkdir -p /storage/.config/rclone && mv /tmp/rclone.conf /storage/.config/rclone/rclone.conf && chmod 600 /storage/.config/rclone/rclone.conf && /usr/bin/cloud_sync_helper >/dev/null 2>&1; echo "remote: $(rclone listremotes | head -1)"' | tee -a "$LOG"
"$R/tools/cloud-test-backend" reset >/dev/null || exit 2; mkdir -p "$DATA/ROCKNIX/Saves/nes" "$DATA/ROCKNIX/Backups" "$DATA/ROCKNIX/Content/ROMs/nes" "$DATA/ROCKNIX/Content/BIOS" "$DATA/ROCKNIX/Saves-replaced/nes"
head -c 4000 /dev/urandom > "$DATA/ROCKNIX/Saves/nes/Probe.srm"; head -c 3000 /dev/urandom > "$DATA/ROCKNIX/Saves-replaced/nes/Probe.srm.1"
head -c 9000 /dev/urandom > "$DATA/ROCKNIX/Content/ROMs/nes/Probe.nes"; head -c 500 /dev/urandom > "$DATA/ROCKNIX/Content/BIOS/disksys.rom"
tar -czf "$DATA/ROCKNIX/Backups/2026_09_30-120000-$LABEL-ROCKNIX_SETTINGS.tar.gz" -C /tmp --files-from /dev/null 2>/dev/null || : > "$DATA/ROCKNIX/Backups/2026_09_30-120000-$LABEL-ROCKNIX_SETTINGS.tar.gz"
: > "$DATA/ROCKNIX/Backups/2026_09_29-090000-Retroid-Pocket-Nova-ROCKNIX_SETTINGS.tar.gz"
say "  cloud: $(host_tree)"
say "  guest conf: $(conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content)"
G_ '. /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; /usr/bin/cloud_sync_helper >/dev/null 2>&1; echo "label=$(/usr/bin/cloud_device_id --label)"' | tee -a "$LOG"

# The former chain assumed A had moved the cloud and B had left a held copy.
# Each case now constructs exactly that initial state itself.
case "$PROOF_CASE" in
 A|H) ;;
 *) mv "$DATA/ROCKNIX" "$DATA/pixelelated"; conf /pixelelated/Saves /pixelelated/Backups /pixelelated/Content >/dev/null;;
esac
if [ "$PROOF_CASE" = E ]; then cp -a "$DATA/pixelelated" "$DATA/_pixelelated_hold"; fi
case "$PROOF_CASE" in
 T17|T19|T23|T26)
  . "$R/tools/vm-walks/cloud-epic/migration-protocol.sh"
  protocol_main "$PROOF_CASE"
  done_line; [ "$FAILS" -eq 0 ]; exit $?;;
esac
reset_picks
G_ 'systemctl stop essway; rm -f /storage/.config/.restore-finish-pending; . /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; systemctl start essway' >/dev/null || exit 2
sleep 20


. "$R/tools/vm-walks/cloud-epic/migration-protocol.sh"
if want UI17; then
  say '== UI17: actual wizard failure, completion and next-boot recovery'
  protocol_init || exit 2
  # Limit the fault to layout discovery. The wizard connectivity check must
  # still reach its real backend; otherwise it never reaches folder setup.
  cat > "$P/layout-fault-rclone" <<'FAULT'
#!/bin/sh
parent=$(tr '\000' ' ' < "/proc/$PPID/cmdline")
case "$parent" in
 *cloud_migrate_layout*)
  if [ -f /tmp/cloud-epic-protocol/fault ] &&
     [ "$1 $2" = "$(cat /tmp/cloud-epic-protocol/fault)" ]; then
   printf '%s\n' "$1 $2" >> /tmp/cloud-epic-protocol/fired
   echo 'injected QA layout discovery failure' >&2
   exit 5
  fi;;
esac
exec /usr/bin/rclone "$@"
FAULT
  scp -q -i "$KEY" -P "$PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR "$P/layout-fault-rclone" root@127.0.0.1:/tmp/cloud-epic-protocol/rclone || exit 2
  G_ 'chmod 755 /tmp/cloud-epic-protocol/rclone' || exit 2
  "$R/tools/cloud-test-backend" reset >/dev/null || exit 2
  mkdir -p "$DATA/ROCKNIX/Saves/nes"
  printf 'UI17 original cloud progress\n' > "$DATA/ROCKNIX/Saves/nes/Setup.srm"
  conf /GAMES /GAMES/backup /GAMES/ROMs >/dev/null || exit 2
  remote=$(G_ '/usr/bin/rclone listremotes | head -1')
  [[ "$remote" =~ ^[A-Za-z0-9_-]+:$ ]] || exit 2
  G_ "printf '%s\n' 'lsd $remote' > /tmp/cloud-epic-protocol/fault" || exit 2
  protocol_snapshot > "$P/logs/UI17-before-cloud.json"
  protocol_pointers > "$P/logs/UI17-before-pointers.txt"
  G_ '/usr/bin/cloud_setup --check >/dev/null 2>&1'; check $? 'UI17 real connectivity gate passes despite layout-only fault'
  G_ '/usr/bin/cloud_migrate_layout --settle >/dev/null 2>&1'; rc=$?
  [ "$rc" -ne 0 ]; check $? 'UI17 selected layout operation really fails before driving wizard'
  G_ 'test -s /tmp/cloud-epic-protocol/fired && rm /tmp/cloud-epic-protocol/fired'; check $? 'UI17 control reached fault; clear only its test count'
  debug_reboot
  require_no_game || exit 2
  G_ 'rm -f /tmp/cloud-epic-protocol/fired' || exit 2
  # A shell held by this owner satisfies the wizard's actual SSH-session gate.
  ssh -n -i "$KEY" -p "$PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o BatchMode=yes root@127.0.0.1 'sleep 900' >/dev/null 2>&1 &
  SSHPID=$!; printf '%s\n' "$SSHPID" > "$P/held-ssh.pid"
  sleep 2
  G_ '/usr/bin/cloud_setup --connected' | tee -a "$LOG"
  f=$P/UI17-wizard.steps
  # Reuse the already-qualified case L route, with its screenshots renamed.
  cp "${TASK_SUPPLEMENT_OWNER:?}/wizard.steps" "$f"
  walk "$f" "$FR"
  kill "$SSHPID" 2>/dev/null || :; wait "$SSHPID" 2>/dev/null || :
  SSHPID=""
  G_ 'test -s /tmp/cloud-epic-protocol/fired'; check $? 'UI17 wizard folder scan reaches selected provider fault'
  esl 'cloud folder step: checking the folder \(end of cloud setup\)' > "$P/logs/UI17-wizard-folder.log"
  [ -s "$P/logs/UI17-wizard-folder.log" ]; check $? 'UI17 fault occurs at wizard folder step'
  steps UI17-dismiss 'shot UI17-scan-failed' 'key z' 'wait-for-change' 'settle 120 3' 'shot UI17-setup-complete'
  esl 'cloud_setup wizard: complete' > "$P/logs/UI17-wizard-complete.log"
  [ -s "$P/logs/UI17-wizard-complete.log" ]; check $? 'UI17 dismissing failure reaches actual wizard completion'
  protocol_snapshot > "$P/logs/UI17-failed-cloud.json"
  protocol_pointers > "$P/logs/UI17-failed-pointers.txt"
  cmp -s "$P/logs/UI17-before-cloud.json" "$P/logs/UI17-failed-cloud.json"; check $? 'UI17 failed scan and seeding preserve all cloud bytes; no README or marker added'
  cmp -s "$P/logs/UI17-before-pointers.txt" "$P/logs/UI17-failed-pointers.txt"; check $? 'UI17 failed scan and seeding leave inherited pointers unchanged'
  [ ! -e "$DATA/GAMES" ] && [ ! -e "$DATA/pixelelated" ]; check $? 'UI17 wizard creates neither old nor new root after settlement failure'
  steps UI17-close 'dismiss-dialogs'
  G_ 'rm /tmp/cloud-epic-protocol/fault; . /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 1' || exit 2
  boot_frames UI17-recovery-boot 15
  steps UI17-recover 'shot UI17-boot-move-question' 'key x' 'wait-for-change' 'settle 180 3' 'shot UI17-move-complete' 'key x' 'wait-for-change' 'settle' 'dismiss-dialogs'
  [ "$(cat "$DATA/pixelelated/Saves/nes/Setup.srm" 2>/dev/null)" = 'UI17 original cloud progress' ] && [ ! -e "$DATA/ROCKNIX/Saves/nes/Setup.srm" ]; check $? 'UI17 next-boot move preserves original save exactly once'
  [ "$(cat "$DATA/pixelelated/.layout" 2>/dev/null)" = layout=2 ]; check $? 'UI17 recovery publishes supported layout marker'
  G_ "grep -qx 'SAVES_REMOTE=\"/pixelelated/Saves\"' $CONF"; check $? 'UI17 recovery publishes current saves pointer'
  protocol_snapshot > "$P/logs/UI17-recovered-cloud.json"
  protocol_pointers > "$P/logs/UI17-recovered-pointers.txt"
  esl 'cloud folder step|cloud folder:' > "$P/logs/UI17-recovery-step.log"
  G_ 'journalctl -b -o short-iso -t cloud_migrate_layout --no-pager' | maskl > "$P/logs/UI17-recovery-journal.log"
  G_ 'test ! -e /storage/.config/cloud-layout-migration.json'; check $? 'UI17 recovery clears local pending record'
fi

if want UI26; then
  say '== UI26: unsupported marker refusal through actual transfer page'
  for kind in malformed future; do
    G_ 'systemctl stop essway; . /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; rm -f /storage/.config/cloud-layout-migration.json' || exit 2
    "$R/tools/cloud-test-backend" reset >/dev/null || exit 2
    mkdir -p "$DATA/ROCKNIX/Saves/nes" "$DATA/pixelelated/Saves/nes"
    printf 'UI26 original old progress\n' > "$DATA/ROCKNIX/Saves/nes/Old.srm"
    printf 'UI26 original current progress\n' > "$DATA/pixelelated/Saves/nes/Current.srm"
    case "$kind" in malformed) printf 'layout=banana\n';; future) printf 'layout=999\n';; esac > "$DATA/pixelelated/.layout"
    conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content >/dev/null || exit 2
    protocol_snapshot > "$P/logs/UI26-$kind-before-cloud.json"
    protocol_pointers > "$P/logs/UI26-$kind-before-pointers.txt"
    # A kept cloud folder avoids boot taking the surface before the manual
    # scan; it must not authorize a malformed/newer marker to be overwritten.
    G_ "sed -i 's|^LAYOUT_KEEP=.*|LAYOUT_KEEP=\"/ROCKNIX/Saves\"|' $CONF" || exit 2
    protocol_pointers > "$P/logs/UI26-$kind-before-pointers.txt"
    debug_reboot
    to_page restore "UI26-$kind"
    esl 'cloud_scan|CloudTransfer' > "$P/logs/UI26-$kind-interface.log"
    G_ 'test ! -e /storage/.cache/cloud_sync/scan/done'; check $? "UI26 $kind scan has no success stamp"
    G_ '/usr/bin/cloud_scan --folder' > "$P/logs/UI26-$kind-script.log" 2>&1; rc=$?
    [ "$rc" -ne 0 ]; check $? "UI26 $kind installed scan refuses unsupported marker"
    printf '%s\n' "$rc" > "$P/logs/UI26-$kind-script.rc"
    protocol_snapshot > "$P/logs/UI26-$kind-after-cloud.json"
    protocol_pointers > "$P/logs/UI26-$kind-after-pointers.txt"
    cmp -s "$P/logs/UI26-$kind-before-cloud.json" "$P/logs/UI26-$kind-after-cloud.json"; check $? "UI26 $kind UI/scan preserve every cloud byte and marker"
    cmp -s "$P/logs/UI26-$kind-before-pointers.txt" "$P/logs/UI26-$kind-after-pointers.txt"; check $? "UI26 $kind UI/scan preserve every pointer and keep choice"
    steps "UI26-$kind-close" "shot UI26-$kind-refusal" 'key z' 'wait-for-change' 'settle' 'dismiss-dialogs'
  done
fi
require_no_game; check $? 'supplemental UI route launched no game'
done_line
[ "$FAILS" -eq 0 ]
