#!/bin/bash
# KILL15's FAIL, read at the run: the guest cell judged `cloud_saves_root check`'s own last line
# as an outcome line. The player meets that text through the twins, which relay it (relay_refusal)
# and end with their own summary. Here: an empty saves-root record planted, then each twin whole
# (--yes --saves-only) in the sandbox; its last prose line, as tools/cloud-round-trip reads it.
# The refusal comes before any transfer, so no backend runs (none is up: 05:34 line on the host file).
. /workspace/tmp/m6-t16/hl/lib.sh
header "KILL15 at the run: an empty saves-root record under each twin"
echo "\$ (sandbox) cloud_saves_root check   (the guest cell's own invocation, for comparison)"
for t in check cloud_restore cloud_backup; do
    new_cell "k15-${t}"
    mkdir -p "${CELL}/storage/roms/savestates"; printf 'local save\n' > "${CELL}/storage/roms/savestates/k.state"
    : > "${CELL}/storage/.cache/cloud_sync/saves-root"
    case "${t}" in
        check) cmd='cloud_saves_root check' ;;
        *) cmd="${t} --yes --saves-only" ;;
    esac
    echo; echo "=== ${cmd} ($(now)); cell ${CELL}"
    "${HL}/sbx.sh" bash -c "${cmd} > /tmp/k.out 2>&1; echo \"rc=\$?\"; sed 's/\x1b\[[0-9;]*[A-Za-z]//g' /tmp/k.out | tr '\r' '\n' | grep -v -E '^(Transferred:|Checks:|Elapsed time:|Errors:|Transferring:)|^[[:space:]]*\*|^[[:space:]]*\$' | sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig' | tail -12" 2>&1
    echo "stamps: last-restore $(cat "${CELL}/storage/.cache/cloud_sync/last-restore" 2>/dev/null || echo none); last-backup $(cat "${CELL}/storage/.cache/cloud_sync/last-backup" 2>/dev/null || echo none); the local save $(cat "${CELL}/storage/roms/savestates/k.state")"
done
echo "== end $(now)"
