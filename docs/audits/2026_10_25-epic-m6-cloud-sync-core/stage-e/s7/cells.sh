#!/bin/bash
# T16 stage E, S7 (PL-16, PL-20, PL-21, PL-22, PL-25). Run on a root: ROOT=<root> s7/cells.sh [cell ...];
# the QA WebDAV up for `clock` and `recent`. Stand-ins are in each cell's /drv/bin, first on PATH
# for the command they serve, and named in the cell.
#  term     twelve exit captures make a manifest of twelve claimed paths; then cloud_capture --full
#           in its own process group, a sha256sum stand-in sleeping 1 s before each hash, TERM to
#           the group at +4 s (systemd's stop: one TERM to every process in the cgroup)
#  full     the same manifest, --full with the same stand-in and CLOUD_CAPTURE_FULL_BOUND=5 (the
#           300 s bound shortened for the harness; the variable is new with the fix)
#  clock    a date stand-in that answers +%s for real once, then 3600 s ahead: cloud_backup
#           --yes --saves-only --automatic, then cloud_saves_root check --wait 15 against a record
#           of another card (the blkid stand-in of root-pin4 and root-s7)
#  wait     cloud_net_ready with an nmcli stand-in: --wait 010 with NetworkManager disconnected;
#           --wait 3 with an nmcli that takes 4 s to answer; and an uptime of 0.08 s (a file bound
#           over /proc/uptime -- static, so the run is ended by the cell's timeout 5)
#  retire   (ruling 8) the same manifest; cloud_capture --retire --unlink of one save in its own
#           group, an mv stand-in sleeping 2 s before each rename, TERM to the group at +1 s --
#           inside the unit (the row, then the file): does the unit finish?
#  sidecars the donor's rclone lsf --filter-from <the root's rules> over a planted tree
#  recent   a last-backup stamp of rc 0 a minute old, SAVES_REMOTE changed to a new folder, an old
#           save and a new one: cloud_backup --yes --saves-only --recent --automatic, twice
. "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/tools/lib.sh"
CELLS="${*:-term full retire clock wait sidecars recent}"
header "S7 the capture's TERM and bound, monotonic time, --wait, the sidecars, the saves folder's record"
RUN=$(date -u +%H%M%S)
DATA=${CLOUD_QA_STATE}/data
M="/storage/.cache/cloud_sync"

capture_cell() { # <name>: a cell with twelve claimed saves, a manifest, and the hasher stand-in
  new_cell "$1"
  mkdir -p "${CELL}/storage/roms/gb" "${CELL}/drv/bin"
  for i in $(seq 1 12); do printf 'save %s of %s\n' "${i}" "${RUN}" > "${CELL}/storage/roms/gb/G${i}.srm"; done
  "${SBX}" bash -c 'for i in $(seq 1 12); do cloud_capture --system gb --rom /storage/roms/gb/G${i}.gb --emulator retroarch --core gambatte --started 0 --exit 0 >/dev/null 2>&1 || echo "  exit capture ${i}: rc $?"; done' 2>&1
  printf '#!/bin/sh\nsleep 1\nexec /usr/bin/sha256sum "$@"\n' > "${CELL}/drv/bin/sha256sum"; chmod 755 "${CELL}/drv/bin/sha256sum"
  MAN=$(ls "${CELL}${M}"/manifest-*.json 2>/dev/null | head -1)
  echo "  the manifest: ${MAN##*/}, $(jq '.entries | length' "${MAN}" 2>/dev/null) entries, sha256 $(sha256sum "${MAN}" | cut -c1-16)"
}

for c in ${CELLS}; do case "${c}" in
term)
  echo "== S7-term ($(now))"
  capture_cell s7term; before=$(sha256sum "${MAN}" | cut -c1-16)
  cat > "${CELL}/drv/t.sh" <<'EOD'
t0=${EPOCHREALTIME}
PATH=/drv/bin:${PATH} setsid cloud_capture --full > /tmp/t.out 2>&1 &
pid=$!
sleep 4; t1=${EPOCHREALTIME}; kill -TERM -- "-${pid}" 2>/dev/null; echo "  TERM to the group at +$(( (${t1/./} - ${t0/./}) / 1000 )) ms"
wait "${pid}"; rc=$?; t2=${EPOCHREALTIME}
echo "  cloud_capture --full: rc=${rc}, ended $(( (${t2/./} - ${t1/./}) / 1000 )) ms after the TERM, $(( (${t2/./} - ${t0/./}) / 1000 )) ms in all"
echo "  its last-capture line for full: $(grep ' full' /storage/.cache/cloud_sync/last-capture | cut -d' ' -f2-4)"
echo "  its log: $(grep -E 'stopped|recorded|TERM' /var/log/cloud_sync.log | tail -2 | cut -c22-200 | tr '\n' '|')"
EOD
  "${SBX}" bash /drv/t.sh 2>&1
  echo "  the manifest after: $([ "$(sha256sum "${MAN}" | cut -c1-16)" = "${before}" ] && echo "byte for byte as planted (${before})" || echo "rewritten ($(sha256sum "${MAN}" | cut -c1-16), was ${before})")"
  echo ;;
full)
  echo "== S7-full ($(now))"
  capture_cell s7full; before=$(sha256sum "${MAN}" | cut -c1-16)
  "${SBX}" bash -c 't0=${EPOCHREALTIME}; PATH=/drv/bin:${PATH} CLOUD_CAPTURE_FULL_BOUND=5 cloud_capture --full > /tmp/f.out 2>&1; rc=$?; t1=${EPOCHREALTIME}; echo "  cloud_capture --full (CLOUD_CAPTURE_FULL_BOUND=5): rc=${rc} after $(( (${t1/./} - ${t0/./}) / 1000 )) ms"; echo "  its last-capture line for full: $(grep " full" /storage/.cache/cloud_sync/last-capture | cut -d" " -f2-4)"; echo "  its log: $(grep -E "bound|recorded" /var/log/cloud_sync.log | tail -1 | cut -c22-220)"' 2>&1
  echo "  the manifest after: $([ "$(sha256sum "${MAN}" | cut -c1-16)" = "${before}" ] && echo "byte for byte as planted" || echo "rewritten")"
  echo ;;
retire)
  echo "== S7-retire: a TERM inside the retire unit ($(now))"
  capture_cell s7retire; before=$(sha256sum "${MAN}" | cut -c1-16)
  printf '#!/bin/sh\nsleep 2\nexec /usr/bin/mv "$@"\n' > "${CELL}/drv/bin/mv"; chmod 755 "${CELL}/drv/bin/mv"
  cat > "${CELL}/drv/r.sh" <<'EOD'
t0=${EPOCHREALTIME}
PATH=/drv/bin:${PATH} setsid cloud_capture --retire --unlink /storage/roms/gb/G3.srm > /tmp/r.out 2>&1 &
pid=$!
sleep 1; t1=${EPOCHREALTIME}; kill -TERM -- "-${pid}" 2>/dev/null; echo "  TERM to the group at +$(( (${t1/./} - ${t0/./}) / 1000 )) ms"
wait "${pid}"; rc=$?; t2=${EPOCHREALTIME}
echo "  cloud_capture --retire --unlink: rc=${rc}, ended $(( (${t2/./} - ${t1/./}) / 1000 )) ms after the TERM"
echo "  the save: $([ -e /storage/roms/gb/G3.srm ] && echo "still there" || echo unlinked); its log: $(grep -E 'retired|unlinked|stopped' /var/log/cloud_sync.log | tail -2 | cut -c22-160 | tr '\n' '|')"
EOD
  "${SBX}" bash /drv/r.sh 2>&1
  echo "  the manifest: $([ "$(sha256sum "${MAN}" | cut -c1-16)" = "${before}" ] && echo "as planted" || echo "rewritten"); gb/G3.srm retired: $(jq -r '.retired | map(.path) | index("gb/G3.srm") != null' "${MAN}" 2>/dev/null); an entry still: $(jq -r '.entries["gb/G3.srm"] != null' "${MAN}" 2>/dev/null)"
  echo ;;
clock)
  echo "== S7-clock: the clock steps 3600 s ahead after the first date +%s ($(now))"
  new_cell s7clock; mkdir -p "${CELL}/storage/roms/savestates" "${CELL}/drv/bin"
  printf 'save %s\n' "${RUN}" > "${CELL}/storage/roms/savestates/c-${RUN}.state"
  printf '#!/bin/sh\nif [ "$1" = "+%%s" ]; then\n  if [ -e /tmp/date-stepped ]; then echo $(( $(/usr/bin/date +%%s) + 3600 )); else : > /tmp/date-stepped; /usr/bin/date +%%s; fi\nelse exec /usr/bin/date "$@"; fi\n' > "${CELL}/drv/bin/date"
  chmod 755 "${CELL}/drv/bin/date"
  "${SBX}" bash -c 'PATH=/drv/bin:${PATH} cloud_backup --yes --saves-only --automatic > /tmp/c.out 2>&1; echo "  cloud_backup --automatic: rc=$?, $(grep -E "^Game saves:" /tmp/c.out)"; echo "  its log: $(grep -E "not started|ceiling|automatic run" /var/log/cloud_sync.log | cut -c22-170 | tr "\n" "|")"' 2>&1
  echo "  the save in the cloud: $(ls "${DATA}/pixelelated/Saves/savestates/c-${RUN}.state" 2>/dev/null | wc -l)"
  echo "uuid:another-card" > "${CELL}${M}/saves-root"
  "${SBX}" bash -c 'rm -f /tmp/date-stepped; t0=${EPOCHREALTIME}; PATH=/drv/bin:${PATH} cloud_saves_root check --wait 15 > /tmp/w.out 2>&1; rc=$?; t1=${EPOCHREALTIME}; echo "  cloud_saves_root check --wait 15 (a record of another card): rc=${rc} after $(( (${t1/./} - ${t0/./}) / 1000 )) ms; $(head -1 /tmp/w.out)"' 2>&1
  echo ;;
wait)
  echo "== S7-wait: cloud_net_ready ($(now))"
  new_cell s7wait; mkdir -p "${CELL}/drv/bin"
  printf '#!/bin/sh\n[ -n "${NM_SLEEP}" ] && sleep "${NM_SLEEP}"\ncase "$*" in *CONNECTIVITY*) echo none ;; *STATE*) echo disconnected ;; esac\n' > "${CELL}/drv/bin/nmcli"
  chmod 755 "${CELL}/drv/bin/nmcli"
  printf '0.08 0.00\n' > "${CELL}/drv/uptime"
  "${SBX}" bash -c '
    run() { local t0 t1 rc; t0=${EPOCHREALTIME}; PATH=/drv/bin:${PATH} "$@" > /tmp/n.out 2>&1; rc=$?; t1=${EPOCHREALTIME}; echo "rc=${rc} after $(( (${t1/./} - ${t0/./}) / 1000 )) ms; $(grep -v "^>>>" /tmp/n.out | head -1 | cut -c1-90)"; }
    echo "  --wait 010, disconnected: $(run cloud_net_ready --wait 010)"
    echo "  --wait 3, nmcli answering after 4 s: $(NM_SLEEP=4 run cloud_net_ready --wait 3)"' 2>&1
  SBX_LATE="--ro-bind ${CELL}/drv/uptime /proc/uptime" "${SBX}" bash -c 'read -r up _ < /proc/uptime; echo "  /proc/uptime reads ${up}"; t0=${EPOCHREALTIME}; PATH=/drv/bin:${PATH} timeout 5 cloud_net_ready --wait 1 > /tmp/u.out 2>&1; rc=$?; t1=${EPOCHREALTIME}; echo "  --wait 1 at an uptime of 0.08 s: rc=${rc} after $(( (${t1/./} - ${t0/./}) / 1000 )) ms; $(grep -v "^>>>" /tmp/u.out | head -1 | cut -c1-100)"' 2>&1 || echo "  the uptime bind: CANNOT (bwrap refused it, rc $?)"
  echo ;;
sidecars)
  echo "== S7-sidecars: the donor's rclone lsf with the root's rules ($(now))"
  T=$(mktemp -d "${HL}/cells/s7side.XXXXXX")
  mkdir -p "${T}/tree/savefiles/psp"
  for f in a.sqlite a.sqlite-wal a.sqlite-shm a.sqlite-journal b.sqlite3 b.sqlite3-wal b.sqlite3-shm b.sqlite3-journal game.srm; do echo x > "${T}/tree/savefiles/psp/${f}"; done
  "${DONOR}/usr/bin/rclone" lsf -R --files-only --filter-from "${ROOT}/usr/config/cloud_sync-rules.txt" "${T}/tree" --config /dev/null > "${T}/lsf.out" 2>&1
  echo "  rc=$?; listed: $(tr '\n' ' ' < "${T}/lsf.out")"
  echo ;;
recent)
  echo "== S7-recent: SAVES_REMOTE changed, a last-backup stamp of rc 0 a minute old ($(now))"
  new_cell s7recent; F="${CELL}/storage/.config/cloud_sync.conf"
  sed -i "s|^SAVES_REMOTE=.*|SAVES_REMOTE=\"/pixelelated/Saves-${RUN}\"|" "${F}"
  mkdir -p "${CELL}/storage/roms/savestates"
  printf 'old\n' > "${CELL}/storage/roms/savestates/old-${RUN}.state"; touch -d '2 days ago' "${CELL}/storage/roms/savestates/old-${RUN}.state"
  printf 'new\n' > "${CELL}/storage/roms/savestates/new-${RUN}.state"
  echo "$(( $(date +%s) - 60 )) 0" > "${CELL}${M}/last-backup"
  for pass in first second; do
    "${SBX}" bash -c "cloud_backup --yes --saves-only --recent --automatic > /tmp/r.out 2>&1; echo \"  the ${pass} run: rc=\$?, \$(grep -E '^Game saves:' /tmp/r.out)\"" 2>&1
    echo "    its recent line: $(grep -h 'recent:' "${CELL}/log/cloud_sync.log" | tail -1 | cut -c22-160)"
    echo "    the new folder holds: $(cd "${DATA}/pixelelated/Saves-${RUN}" 2>/dev/null && find . -type f | sort | tr '\n' ' ')"
    echo "    last-backup-dest: $([ -e "${CELL}${M}/last-backup-dest" ] && sed 's/^[^:]*:/<remote>:/' "${CELL}${M}/last-backup-dest" || echo none); last-backup: $(cut -d' ' -f2- "${CELL}${M}/last-backup")"
  done
  echo ;;
esac; done
echo "== end $(now)"
