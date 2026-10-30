#!/bin/bash
# Lead (b), F-02: cloud_restore --yes --saves-only with SAVESPATH="" against the QA WebDAV, whole
# and unmodified in the sandbox. Arm ro: / read-only after the binds, as the image's squashfs is
# (/storage, /tmp, /run and /var/log writable). Arm rw: / writable, so rclone's own answer shows
# whatever the root's mode. Seeds two saves in the cloud; reads what changed after a marker.
. /workspace/tmp/m6-t16/hl/lib.sh
header "(b) SAVESPATH=\"\", cloud_restore --yes --saves-only"
DATA=${CLOUD_QA_STATE}/data
mkdir -p "${DATA}/pixelelated/Saves/savestates" "${DATA}/pixelelated/Saves/gba" "${DATA}/pixelelated/Backups"
printf 'cloud state b1\n' > "${DATA}/pixelelated/Saves/savestates/b1.state"
printf 'cloud save b2\n' > "${DATA}/pixelelated/Saves/gba/b2.srm"
echo "the cloud (the backend's data directory): $(cd "${DATA}" && find pixelelated -type f | sort | tr '\n' ' ')"
for arm in ctl ro rw bk; do
    new_cell "b-${arm}"
    [ "${arm}" = ctl ] && mkdir -p "${CELL}/storage/roms/savestates" && : > "${CELL}/drv/ctl"
    [ "${arm}" = bk ] && mkdir -p "${CELL}/storage/roms/gba" && printf 'local save\n' > "${CELL}/storage/roms/gba/bk.srm" && : > "${CELL}/drv/bk"
    cat > "${CELL}/drv/b.sh" <<'EOS'
F='key|pass|token|user|psk'
mask() { sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'; }
C=/storage/.config/cloud_sync.conf
: > /tmp/marker; sleep 1
[ -e /drv/ctl ] || sed -i 's/^SAVESPATH=.*/SAVESPATH=""/' "$C"; echo "conf: $(grep -n '^SAVESPATH' "$C")"
echo "/ is $(touch /t16-probe 2>/dev/null && echo writable || echo read-only)"
if [ -e /drv/bk ]; then cloud_backup --yes --saves-only > /tmp/b.out 2>&1; echo "cloud_backup rc=$?"; else cloud_restore --yes --saves-only > /tmp/b.out 2>&1; echo "cloud_restore rc=$?"; fi
echo "-- its output, protocol and prose lines (rclone's redraws dropped; masked):"
tr '\r' '\n' < /tmp/b.out | sed 's/\x1b\[[0-9;]*[A-Za-z]//g' | grep -v -E '^(Transferred:|Checks:|Elapsed time:|Errors:|Transferring:|Checking:)|^[[:space:]]*\*[[:space:]]|^[[:space:]]*$' | grep -v -i -E 'pass|token|psk' | mask | tail -30
echo "-- the log's lines for this run (masked):"
grep -i -E 'restore from|restore path|backup from|not on this device|overlap|backup.dir|error|why|refus|saves root|card|copy ' /var/log/cloud_sync.log | grep -v -i -E 'pass|token|psk' | mask | tail -20
for st in last-restore last-backup; do echo "-- stamp ${st}: $(cat /storage/.cache/cloud_sync/${st} 2>/dev/null || echo none)"; done
echo "-- the seeded saves by name, anywhere but /proc: $(find / -path /proc -prune -o \( -name b1.state -o -name b2.srm -o -name bk.srm \) -print 2>/dev/null | sort | tr '\n' ' ')"
echo "-- files newer than the marker, the whole tree but /proc, /dev and the marker:"
find / \( -path /proc -o -path /dev -o -path /host -o -path /donor -o -path /usr \) -prune -o -type f -newer /tmp/marker -print 2>/dev/null | grep -v -E "$F" | grep -v '^/tmp/marker$' | sort | head -40
echo "-- directories at / now: $(ls / | tr '\n' ' ')"
EOS
    echo; echo "=== arm ${arm} ($(now)); cell ${CELL}"
    RO=$(case "${arm}" in ro|bk) echo 1 ;; *) echo 0 ;; esac) "${HL}/sbx.sh" bash /drv/b.sh 2>&1
    echo "sandbox rc=$?"
done
echo "== end $(now)"
