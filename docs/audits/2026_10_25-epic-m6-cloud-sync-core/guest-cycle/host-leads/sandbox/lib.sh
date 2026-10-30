# T16 host leads, sourced by each cell. No removal here: every cell works in a new directory.
HL=/workspace/tmp/m6-t16/hl
ROOT=${ROOT:-${HL}/root2}
DONOR=/workspace/artifacts/m6-donor/1a0266484423/image/system
WT=/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-sync-core-663
G=${WT}/docs/audits/2026_10_25-epic-m6-cloud-sync-core/guest-cycle
BE=/workspace/tmp/m6-t16/harness/tools/cloud-test-backend
export CLOUD_QA_STATE=${HL}/state CLOUD_QA_BACKEND=webdav CLOUD_QA_GUEST_HOST=127.0.0.1
export CLOUD_QA_DEFAULTS=/workspace/tmp/m6-t16/src/cloud_sync.conf.defaults
F='key|pass|token|user|psk'
mask() { sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'; }
now() { date -u +%FT%TZ; }

# What every cell's record opens with: the clock, the root, its checksums, the scripts' match
# with the guest's installed bytes, and every host program standing in for the image's.
header() {
    echo "== T16 host lead $1 -- $(now)"
    echo "donor root: ${DONOR} (BUILD_ID $(grep -o 'BUILD_ID="[0-9a-f]*' "${DONOR}/etc/os-release" | cut -c11-22)); sha256sum -c ../../SHA256SUMS:"
    ( cd "${DONOR}" && sha256sum -c ../../SHA256SUMS 2>&1 | sed 's/^/  /' )
    local same=0 n=0 f h
    for f in "${ROOT}"/usr/bin/cloud_backup "${ROOT}"/usr/bin/cloud_restore "${ROOT}"/usr/bin/cloud_capture \
             "${ROOT}"/usr/bin/cloud_net_ready "${ROOT}"/usr/bin/cloud_saves_root "${ROOT}"/usr/bin/cloud_sync_helper \
             "${ROOT}"/usr/bin/cloud_sync_cleanup_duplicates.sh "${ROOT}"/usr/bin/rasteratops-settings-archive \
             "${ROOT}"/usr/config/*; do
        n=$((n + 1)); h=$(sha256sum "${f}" | cut -c1-64); grep -q "^${h} " "${G}/installed.sha256" && same=$((same + 1))
    done
    echo "the scripts and /usr/config: git show 8ebaf8daad, ${same} of ${n} sha256-equal to the guest's installed bytes (guest-cycle/installed.sha256)"
    echo "from the donor: busybox $(${DONOR}/usr/bin/busybox | head -1 | cut -d' ' -f2) (146 applet links), $(${DONOR}/usr/bin/rclone version | head -1)"
    echo "host stand-ins (not in the donor): bash $(bash --version | head -1 | cut -d' ' -f4) (image: 5.3), $(gnutimeout --version | head -1) (image: 9.4), $(grep --version | head -1) (image: 3.9), python3 $(python3 --version | cut -d' ' -f2), ip (iproute2)"
    echo "sandbox: /workspace/tmp/m6-t16/hl/sbx.sh (copied to host-leads/sandbox/) (bwrap, own pid namespace, host network); backend: cloud-test-backend at 3a653eaec4, WebDAV 127.0.0.1:9010, state ${CLOUD_QA_STATE}"
    echo
}

# A fresh cell: storage with the shipped conf and rules, the QA remote's stanza, the card's folder.
new_cell() {
    CELL=${HL}/cells/$1.$(date -u +%H%M%S)
    mkdir -p "${CELL}/storage/.config/rclone" "${CELL}/storage/roms" "${CELL}/storage/.cache/cloud_sync" "${CELL}/drv"
    cp "${ROOT}/usr/config/cloud_sync.conf" "${CELL}/storage/.config/cloud_sync.conf"
    cp "${ROOT}/usr/config/cloud_sync-rules.txt" "${CELL}/storage/.config/cloud_sync-rules.txt"
    ( umask 077; "${BE}" rclone-conf > "${CELL}/storage/.config/rclone/rclone.conf" ) || return 1
    printf '%s\n' "$(sed -n 's/^\[\(.*\)\]$/\1/p' "${CELL}/storage/.config/rclone/rclone.conf" | head -1)" \
        > "${CELL}/storage/.config/rclone/active-connection"
    export CELL ROOT
}
