#!/bin/bash
# #1501 (and the ctl's misread rejected sign-in) on a QA guest already up
# (vm-pair, guest a): the SCAN GAMES FOR OFFLINE ACHIEVEMENTS page refused,
# for each case and language. Frames under OUT/<lang>/<case>/.
#   ra-refusal.sh ROUND OUT "case..." "lang..."
#   cases: password-401 (SIGN_IN_REFUSED), token-401 (a rejected token),
#          token-503 (a server that cannot answer: the retry control)
set -uo pipefail
ROUND=$1 OUT=$2 CASES=$3 LANGS=$4
F=$(dirname "$0")/fixture
KEY=/tmp/rocknix-vm-pair/qa-key; MON=/tmp/rocknix-qemu-monitor.sock
SSHO=(-F /dev/null -p 10022 -i "$KEY" -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=no
      -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=10)
SCPO=(-F /dev/null -P 10022 -i "$KEY" -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=no
      -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=10)
S() { timeout 300 ssh -n "${SSHO[@]}" root@127.0.0.1 ". /etc/profile >/dev/null 2>&1; $*"; }
mask() { sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'; }
log() { echo "$*" | tee -a "$OUT/RESULT.txt"; }
reboot_guest() {
    local b0 b i; b0=$(S 'cat /proc/sys/kernel/random/boot_id')
    S 'sync; systemctl reboot' >/dev/null 2>&1
    for i in $(seq 1 60); do sleep 5; b=$(S 'cat /proc/sys/kernel/random/boot_id' 2>/dev/null); [ -n "$b" ] && [ "$b" != "$b0" ] && break; done
    [ -n "${b:-}" ] && [ "$b" != "$b0" ] || return 1
    for i in $(seq 1 60); do S 'pgrep -x emulationstation >/dev/null' && break; sleep 3; done; sleep 15
}
mkdir -p "$OUT" || exit 2
S 'mkdir -p /storage/m7-qa-1501' && scp -q "${SCPO[@]}" "$F/standin.py" "$F/ra-refusal-guest.sh" root@127.0.0.1:/storage/m7-qa-1501/ < /dev/null || { log "CANNOT RUN: fixture copy"; exit 2; }
failed=0
for lang in $LANGS; do
    case "$lang" in en) code=en_US ;; fr) code=fr_FR ;; *) exit 2 ;; esac
    for c in $CASES; do
        mode=${c%-*} st=${c#*-}; d=$OUT/$lang/$c; mkdir -p "$d"
        log "-- $lang $c $(date -u +%T)"
        S "set_setting system.language $code; bash /storage/m7-qa-1501/ra-refusal-guest.sh account $mode" 2>&1 | mask | tee -a "$d.arm.log" >/dev/null
        reboot_guest || { log "CANNOT RUN: no guest after reboot"; exit 2; }
        S "bash /storage/m7-qa-1501/ra-refusal-guest.sh standin $st" >> "$d.arm.log" 2>&1 || { log "   stand-in did not answer $st"; failed=1; continue; }
        { echo wake; echo dismiss-dialogs; cat "$ROUND/tools/vm-walks/to-offline-achievements.steps"
          echo "key down"; echo "wait-for-change 6"; echo "key down"; echo "wait-for-change 6"; echo settle; echo "shot scan-row"
          echo "key x"; echo "wait-for-change 10"; echo settle; echo "shot confirm"
          echo "key x"; echo "wait-for-change 30 1"; echo "wait 8"; echo "settle 90 3"; echo "shot scan-result"; } > "$d.steps"
        timeout 600 "$ROUND/tools/vm-visual-qa" --monitor "$MON" run "$d.steps" --outdir "$d" > "$d.log" 2>&1; rc=$?
        [ "$rc" = 0 ] || { log "   walk rc $rc"; failed=1; }
        S 'cat /storage/.config/raofflineproxy/last-scan; grep -E "client: FAIL|scan done" /storage/.config/raofflineproxy/scan.log | tail -2' 2>&1 | mask | tee -a "$OUT/RESULT.txt" > "$d.stamp.txt"
    done
done
S "bash /storage/m7-qa-1501/ra-refusal-guest.sh release; set_setting system.language en_US" >> "$OUT/release.log" 2>&1
reboot_guest
log "done $(date -u +%T) failed=$failed"; exit $failed
