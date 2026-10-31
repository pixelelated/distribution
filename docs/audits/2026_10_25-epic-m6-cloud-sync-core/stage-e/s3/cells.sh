#!/bin/bash
# T16 stage E, S3 (#1302, #1303). Run on a root: ROOT=<root> s3/cells.sh
#  S3-fallback fixtures/load-config-fallback.sh (stage C's, unchanged) against both twins of the root
#  S3-sed      cloud_sync_helper whole in the sandbox on a conf holding the three old values its
#              one-time migrations rewrite, with /storage/.config a full card (a 256 KiB tmpfs,
#              filled: a temp copy cannot be written, an empty marker can), then with room again
. "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/tools/lib.sh"
A="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
header "S3 load_config's put-back, the helper's migrations"
echo "== S3-fallback ($(now))"
for f in cloud_backup cloud_restore; do
  D=$(mktemp -d "${HL}/cells/s3fx.XXXXXX"); cp "${ROOT}/usr/bin/${f}" "${D}/${f}"; cp "${ROOT}/usr/config/cloud_sync.conf" "${D}/cloud_sync.conf"
  echo "-- ${f}"; TMPDIR="${D}" bash "${A}/fixtures/load-config-fallback.sh" "${D}/${f}" 2>&1 | grep -v '^scratch:' | sed 's/^/  /'
done
echo
echo "== S3-sed: the helper on a full card, then with room ($(now))"
new_cell s3sed
cat > "${CELL}/drv/old.conf" <<'EOD'
BACKUPMETHOD="sync"
RCLONE_NET_OPTS="--contimeout 15s --timeout 30s --low-level-retries 2 --retries 1"
RCLONE_SYNC_NET_OPTS="--contimeout 5s --timeout 5s --retries 1 --max-duration 20s"
EOD
grep -v -E '^(BACKUPMETHOD|RCLONE_NET_OPTS|RCLONE_SYNC_NET_OPTS)=' "${ROOT}/usr/config/cloud_sync.conf" >> "${CELL}/drv/old.conf"
cp "${ROOT}/usr/config/cloud_sync-rules.txt" "${CELL}/drv/rules"
cat > "${CELL}/drv/sed.sh" <<'EOD'
C=/storage/.config
cp /drv/old.conf "${C}/cloud_sync.conf"; cp /drv/rules "${C}/cloud_sync-rules.txt"
dd if=/dev/zero of="${C}/.filler" bs=1024 2>/dev/null
: > "${C}/.probe" && echo "  full: an empty file still fits ($(df -k "${C}" | awk 'NR==2 {print $4}') KiB free)"
cp "${C}/cloud_sync.conf" "${C}/.copy" 2>/dev/null && echo "  NOT full: a copy fits" || echo "  full: a copy of the conf does not fit"
rm -f "${C}/.probe" "${C}/.copy"
state() {
  echo "  $1:"
  for m in .cloud_sync-copy-default-applied .cloud_sync-net-opts-retries-applied .cloud_sync-sync-net-opts-five-applied; do
    printf '    %-42s %s\n' "${m}" "$([ -e "${C}/${m}" ] && echo PRESENT || echo absent)"
  done
  echo "    $(grep -E '^BACKUPMETHOD=' "${C}/cloud_sync.conf")"
  echo "    $(grep -E '^RCLONE_NET_OPTS=' "${C}/cloud_sync.conf" | grep -o 'low-level-retries [0-9]*')"
  echo "    $(grep -E '^RCLONE_SYNC_NET_OPTS=' "${C}/cloud_sync.conf" | grep -o 'max-duration [0-9]*s')"
}
/usr/bin/cloud_sync_helper /var/log/cloud_sync.log >/dev/null 2>&1; echo "  helper on the full card: rc=$?"
state "after the run on the full card"
rm -f "${C}/.filler"
/usr/bin/cloud_sync_helper /var/log/cloud_sync.log >/dev/null 2>&1; echo "  helper with room again: rc=$?"
state "after the run with room"
echo "  the log's migration lines: $(grep -E 'BACKUPMETHOD|RCLONE_NET_OPTS|RCLONE_SYNC_NET_OPTS|could not' /var/log/cloud_sync.log | cut -c22-150 | tr '\n' '|')"
EOD
SBX_EXTRA="--size 262144 --tmpfs /storage/.config" "${SBX}" bash /drv/sed.sh 2>&1
echo "== end $(now)"
