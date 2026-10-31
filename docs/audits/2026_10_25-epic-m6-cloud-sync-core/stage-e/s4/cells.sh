#!/bin/bash
# T16 stage E, S4 (#1304, PL-18). Run on a root: ROOT=<root> s4/cells.sh [cell ...]; the QA WebDAV up.
# The roots (root-pin4 at 8ebaf8daad, root-s4 at the tree) carry a blkid stand-in at usr/sbin/blkid:
# the image's util-linux blkid reads a card's superblock, the sandbox's /dev has no disk nodes and the
# host's blkid reads nothing without root, so a table stands in -- the device the cell's /storage is on
# has a UUID, any other has none (BLKID_NONE=1: none has one). Its calls go to the cell's log.
#  k15     (k15-at-the-run's rerun, and S4-empty) an empty record planted; check alone, then each twin
#          whole (--yes --saves-only) against the backend, the record after, then check again
#  symlink SAVESPATH a symlink to a tmpfs over /mnt/card2: identity, against the card /storage is on
#  missing SAVESPATH absent: identity, check, record, accept and the record after each -- with the
#          stand-in answering, and with no UUID (BLKID_NONE=1)
#  order   cloud_restore --yes --saves-only on a fresh cell with no saves folder; the tool beside a copy
#          of the scripts notes, each time it is called, whether the folder is there and the identity
#  border  cloud_backup --yes --saves-only with the saves folder absent, through the same noting tool:
#          whether the card is asked about before the folder is tested, and the run's why
#  nouuid  no UUID anywhere: check, a backup that completes, the record after; then a record an older
#          build wrote holding dev:unknown, check against it, the owner's accept, and check again
. "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/tools/lib.sh"
CELLS="${*:-k15 symlink missing order border nouuid}"
header "S4 the saves-root record and the card's identity"
DATA=${CLOUD_QA_STATE}/data; SV=${DATA}/pixelelated/Saves
RUN=$(date -u +%H%M%S)
REC=storage/.cache/cloud_sync/saves-root
rec() { if [ -e "${CELL}/${REC}" ]; then printf '%s (%s bytes)' "$(cat "${CELL}/${REC}")" "$(wc -c < "${CELL}/${REC}")"; else echo absent; fi; }
clean() { sed 's/\x1b\[[0-9;]*[A-Za-z]//g' | tr '\r' '\n' | grep -v -E '^(Transferred:|Checks:|Elapsed time:|Errors:|Transferring:)|^[[:space:]]*\*|^[[:space:]]*$' | mask; }

for c in ${CELLS}; do case "${c}" in
k15)
  for t in cloud_backup cloud_restore; do
    echo "== S4-k15 / S4-empty, ${t}: an empty record; check, the twin, the record, check ($(now))"
    new_cell "s4k15-${t}"; mkdir -p "${CELL}/storage/roms/savestates" "${SV}/savestates"
    printf 'local save %s\n' "${RUN}" > "${CELL}/storage/roms/savestates/k-${RUN}.state"
    printf 'cloud save %s\n' "${RUN}" > "${SV}/savestates/kc-${RUN}.state"
    : > "${CELL}/${REC}"
    echo "  the record planted: $(rec)"
    "${SBX}" bash -c "cloud_saves_root check > /tmp/c.out 2>&1; echo \"  check: rc=\$?\"; sed 's/^/    | /' /tmp/c.out" 2>&1
    "${SBX}" bash -c "${t} --yes --saves-only > /tmp/t.out 2>&1; echo \"  ${t} --yes --saves-only: rc=\$?\"; cat /tmp/t.out" 2>&1 | clean | sed -n '1p;/^>>> why/p;/SUMMARY/,$p' | sed 's/^/    /' | head -14
    echo "  the record after the twin: $(rec)"
    echo "  stamp: $(cat "${CELL}/storage/.cache/cloud_sync/last-${t#cloud_}" 2>/dev/null || echo none)"
    "${SBX}" bash -c "cloud_saves_root check > /tmp/c.out 2>&1; echo \"  check again: rc=\$?\"; sed 's/^/    | /' /tmp/c.out" 2>&1
    echo "  the blkid stand-in was asked: $(sort "${CELL}/log/blkid-standin.log" 2>/dev/null | uniq -c | sed 's/^ *//' | tr '\n' ';')"
    echo
  done ;;
symlink)
  echo "== S4-symlink: SAVESPATH /storage/roms a symlink to /mnt/card2, a tmpfs (the second card) ($(now))"
  new_cell s4sym; rmdir "${CELL}/storage/roms"; ln -s /mnt/card2 "${CELL}/storage/roms"
  SBX_EXTRA="--tmpfs /mnt/card2" "${SBX}" bash -c '
    echo "  /storage/roms -> $(readlink /storage/roms); mountinfo: $(grep -E " /mnt/card2 | /storage " /proc/self/mountinfo | awk "{print \$3, \$5, \$(NF-1)}" | tr "\n" ";")"
    echo "  stat -c %d: /storage $(stat -c %d /storage), /mnt/card2 $(stat -c %d /mnt/card2)"
    echo "  cloud_saves_root identity: $(cloud_saves_root identity)"
    echo "  with no symlink, the card /storage is on: $(CLOUD_SAVESPATH=/storage cloud_saves_root identity)"' 2>&1
  echo ;;
missing)
  for mode in standin none; do
    echo "== S4-missing (${mode}): SAVESPATH=/storage/nosaves, absent ($(now))"
    new_cell "s4miss-${mode}"; sed -i 's|^SAVESPATH=.*|SAVESPATH="/storage/nosaves"|' "${CELL}/storage/.config/cloud_sync.conf"
    env=""; [ "${mode}" = none ] && env="BLKID_NONE=1"
    for a in identity check record accept; do
      "${SBX}" bash -c "${env} cloud_saves_root ${a} > /tmp/a.out 2>&1; echo \"  ${a}: rc=\$? out: \$(tr '\n' '|' < /tmp/a.out)\"" 2>&1
      echo "    the record: $(rec)"
    done
  done; echo ;;
order)
  echo "== S4-order: cloud_restore --yes --saves-only, no saves folder ($(now))"
  new_cell s4order; rmdir "${CELL}/storage/roms"; mkdir -p "${SV}/savestates" "${CELL}/drv/bin"
  printf 'cloud save %s\n' "${RUN}" > "${SV}/savestates/o-${RUN}.state"
  for f in "${ROOT}"/usr/bin/cloud_* "${ROOT}"/usr/bin/rasteratops-settings-archive; do cp "${f}" "${CELL}/drv/bin/"; done
  mv "${CELL}/drv/bin/cloud_saves_root" "${CELL}/drv/bin/cloud_saves_root.real"
  cat > "${CELL}/drv/bin/cloud_saves_root" <<'EOD'
#!/bin/bash
p="${CLOUD_SAVESPATH:-$(sed -n 's/^SAVESPATH="\(.*\)"$/\1/p' /storage/.config/cloud_sync.conf | tail -1)}"
echo "cloud_saves_root $*: the folder ${p} $([ -d "${p}" ] && echo present || echo absent); identity '$(/drv/bin/cloud_saves_root.real identity)'" >> /var/log/s4-order.log
exec /drv/bin/cloud_saves_root.real "$@"
EOD
  chmod 755 "${CELL}/drv/bin/cloud_saves_root"
  "${SBX}" bash -c "/drv/bin/cloud_restore --yes --saves-only > /tmp/o.out 2>&1; echo \"  cloud_restore: rc=\$?\"; cat /tmp/o.out" 2>&1 | clean | sed -n '1p;/^>>> why/p;/SUMMARY/,$p' | sed 's/^/    /' | head -10
  echo "  the calls, in order:"; sed 's/^/    /' "${CELL}/log/s4-order.log" 2>/dev/null || echo "    none"
  echo "  the record: $(rec); the folder: $(ls -d "${CELL}/storage/roms" 2>/dev/null || echo absent)"
  echo ;;
border)
  echo "== S4-border: cloud_backup --yes --saves-only, the saves folder absent ($(now))"
  new_cell s4border; rmdir "${CELL}/storage/roms"; mkdir -p "${CELL}/drv/bin"
  for f in "${ROOT}"/usr/bin/cloud_* "${ROOT}"/usr/bin/rasteratops-settings-archive; do cp "${f}" "${CELL}/drv/bin/"; done
  mv "${CELL}/drv/bin/cloud_saves_root" "${CELL}/drv/bin/cloud_saves_root.real"
  cat > "${CELL}/drv/bin/cloud_saves_root" <<'EOD'
#!/bin/bash
p="${CLOUD_SAVESPATH:-$(sed -n 's/^SAVESPATH="\(.*\)"$/\1/p' /storage/.config/cloud_sync.conf | tail -1)}"
echo "cloud_saves_root $*: the folder ${p} $([ -d "${p}" ] && echo present || echo absent); identity '$(/drv/bin/cloud_saves_root.real identity)'" >> /var/log/s4-order.log
exec /drv/bin/cloud_saves_root.real "$@"
EOD
  chmod 755 "${CELL}/drv/bin/cloud_saves_root"
  "${SBX}" bash -c "/drv/bin/cloud_backup --yes --saves-only > /tmp/o.out 2>&1; echo \"  cloud_backup: rc=\$?\"; cat /tmp/o.out" 2>&1 | clean | sed -n '1p;/^>>> why/p;/^Game saves:/p' | sed 's/^/    /'
  echo "  the calls, in order:"; sed 's/^/    /' "${CELL}/log/s4-order.log" 2>/dev/null || echo "    none"
  echo "  the record: $(rec)"
  echo ;;
nouuid)
  echo "== S4-nouuid: no UUID anywhere (BLKID_NONE=1) ($(now))"
  new_cell s4nouuid; mkdir -p "${CELL}/storage/roms/savestates"; printf 'local save %s\n' "${RUN}" > "${CELL}/storage/roms/savestates/n-${RUN}.state"
  "${SBX}" bash -c "BLKID_NONE=1 cloud_saves_root check > /tmp/c.out 2>&1; echo \"  check: rc=\$? out: \$(tr '\n' '|' < /tmp/c.out)\"" 2>&1
  "${SBX}" bash -c "BLKID_NONE=1 cloud_backup --yes --saves-only > /tmp/t.out 2>&1; echo \"  cloud_backup --yes --saves-only: rc=\$?\"; cat /tmp/t.out" 2>&1 | clean | sed -n '1p;/^>>> why/p;/^Game saves:/p' | sed 's/^/    /'
  echo "  the record after a completed backup: $(rec)"
  echo "dev:unknown" > "${CELL}/${REC}"; echo "  a record an older build wrote: $(rec)"
  for env in "BLKID_NONE=1" ""; do
    "${SBX}" bash -c "${env} cloud_saves_root check > /tmp/c.out 2>&1; echo \"  check (${env:-the stand-in answering}): rc=\$? out: \$(tr '\n' '|' < /tmp/c.out)\"" 2>&1
    echo "    the record: $(rec)"
  done
  "${SBX}" bash -c "BLKID_NONE=1 cloud_saves_root accept > /tmp/a.out 2>&1; echo \"  accept (BLKID_NONE=1): rc=\$? out: \$(tr '\n' '|' < /tmp/a.out)\"" 2>&1
  echo "    the record: $(rec)"
  "${SBX}" bash -c "BLKID_NONE=1 cloud_saves_root check > /tmp/c.out 2>&1; echo \"  check after accept (BLKID_NONE=1): rc=\$? out: \$(tr '\n' '|' < /tmp/c.out)\"" 2>&1
  echo ;;
esac; done
echo "== end $(now)"
