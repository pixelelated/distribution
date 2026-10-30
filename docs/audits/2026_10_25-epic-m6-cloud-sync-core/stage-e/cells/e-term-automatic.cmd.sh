#!/bin/bash
# Lead (e), F-03: cloud_restore --automatic --yes --saves-only, whole, against the QA WebDAV
# throttled to 100k (cloud-test-backend's own CLOUD_QA_BWLIMIT), one 6 MiB save to fetch (2 MiB finished before +9 s in the first try, 05:28).
# Arm term: TERM to the script's pid alone at +5 s, then watch until it exits.
# Arm termkill: TERM at +5 s, KILL at +9 s to the script's pid alone, then watch the transfer.
# Arm termkill-game (ARMS=termkill-game): as termkill, then at +11 s the "game" writes 10 bytes to the
# name the orphaned rclone is fetching; at the end, whose bytes the name holds.
# Completed at T16 stage E, S2 (D-WORKFLOW-211): the game's target is the name the transfer had
# open at +5 s, before the TERM, not the one open at +11 s -- which existed only while the defect
# left an orphan running. No assertion is changed.
# The sandbox has its own pid namespace: ps sees only this run; what is left dies with it.
. /workspace/tmp/m6-t16/hl/lib.sh
header "(e) TERM to an automatic restore"
DATA=${CLOUD_QA_STATE}/data
for arm in ${ARMS:-term termkill}; do
    mkdir -p "${DATA}/pixelelated/Saves/savestates"
    head -c 6291456 /dev/urandom > "${DATA}/pixelelated/Saves/savestates/e-${arm}.state"
    new_cell "e-${arm}"
    mkdir -p "${CELL}/storage/roms/savestates"
    printf '%s\n' "${arm}" > "${CELL}/drv/arm"
    [ "${arm}" = termkill-game ] && printf 'EXTRA_WAIT=30\n' > "${CELL}/drv/env"
    cat > "${CELL}/drv/e.sh" <<'EOS'
mask() { sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'; }
ARM=$(cat /drv/arm); S=$(date +%s); [ -e /drv/env ] && . /drv/env
snap() {
    echo "+$(( $(date +%s) - S ))s: script $(kill -0 "$P" 2>/dev/null && echo alive || echo gone);" \
         "partial: $(ls -l /storage/roms/savestates/ 2>/dev/null | awk '/partial/ {print $5}' | tr '\n' ' ')" \
         "landed: $(ls /storage/roms/savestates/ 2>/dev/null | grep -v partial | tr '\n' ' ')"
    ps -o pid,ppid,etimes,args 2>/dev/null | grep -E 'rclone|timeout|cloud_restore' | grep -v grep | cut -c1-150 | mask | sed 's/^/      /'
}
cloud_restore --automatic --yes --saves-only > /tmp/e.out 2>&1 &
P=$!
echo "cloud_restore --automatic --yes --saves-only started, pid ${P}"
sleep 5; snap; OPEN=$(ls /storage/roms/savestates/ | grep partial | head -1); kill -TERM "$P"; echo "TERM to ${P} at +$(( $(date +%s) - S ))s"
if [ "${ARM}" != term ]; then
    sleep 2; snap; sleep 2; snap
    kill -KILL "$P" 2>/dev/null && echo "KILL to ${P} at +$(( $(date +%s) - S ))s" || echo "the script was already gone at +9s"
fi
if [ "${ARM}" = termkill-game ]; then
    sleep 2; GAME=/storage/roms/savestates/${OPEN%.????????.partial}
    printf 'game save\n' > "${GAME}"; echo "+$(( $(date +%s) - S ))s: the game wrote ${GAME} ($(wc -c < "${GAME}") bytes) while ${part} is open"
fi
i=0; while kill -0 "$P" 2>/dev/null && [ "$i" -lt 60 ]; do sleep 1; i=$((i + 1)); done
echo "the script ended by +$(( $(date +%s) - S ))s"; wait "$P" 2>/dev/null; echo "its status (as its parent saw it): $?"
for t in 2 10 20 ${EXTRA_WAIT:-}; do sleep "$t"; snap; done
[ -n "${GAME:-}" ] && echo "-- the game's file at the end: ${GAME}, $(wc -c < "${GAME}") bytes, $(head -c 9 "${GAME}" | grep -q '^game save' && echo "the game's bytes" || echo "NOT the game's bytes: the orphan's rename landed on it")"
echo "-- the script's last lines (masked):"; tr '\r' '\n' < /tmp/e.out | grep -v -E '^(Transferred:|Checks:|Elapsed time:|Errors:|Transferring:)|^[[:space:]]*\*|^[[:space:]]*$' | mask | tail -8
echo "-- the log: deadline, interruption, exit (masked):"; grep -i -E 'deadline|automatic|interrupt|ceiling|exit|why' /var/log/cloud_sync.log | mask | tail -10
echo "-- stamp last-restore: $(cat /storage/.cache/cloud_sync/last-restore 2>/dev/null || echo none)"
echo "-- left in the saves tree: $(find /storage/roms -type f | sort | tr '\n' ' ')"
EOS
    echo; echo "=== arm ${arm} ($(now)); cell ${CELL}"
    "${HL}/sbx.sh" bash /drv/e.sh 2>&1
    echo "sandbox rc=$? at $(now)"
done
echo "== end $(now)"
