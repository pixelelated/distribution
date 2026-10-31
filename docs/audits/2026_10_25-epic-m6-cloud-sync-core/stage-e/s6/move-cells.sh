#!/bin/bash
# T16 stage E, S6's second follow-up (ruling 14 on #663, D-CLOUD-192): RCLONEOPTS's filter flags moved
# into the rules file once as the player's rules. Run on a root: ROOT=<root> s6/move-cells.sh [cell ...];
# the QA WebDAV up. An argv-recording rclone is first on PATH for the backups.
#  move    PL-015's conf shape: RCLONEOPTS carries --exclude \"*.tmp\" (escaped quotes, as conf_valid's
#          comment records it), a .tmp beside a save. The helper whole, once: the rules file, the conf's
#          RCLONEOPTS, the .bak, the log line; the donor's rclone lsf with the rules over the saves; the
#          helper again: the conf and the rules byte for byte; then cloud_backup --yes --saves-only:
#          rclone's argv and what reached the cloud
#  refuse  the same conf with the rules file cut before its catch-all and no .bak: the helper, the
#          conf line after it, then cloud_backup --yes --saves-only: its log's WARN and its outcome
. "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/tools/lib.sh"
CELLS="${*:-move refuse}"
header "S6's second follow-up: RCLONEOPTS's filter flags into the rules file (ruling 14)"
RUN=$(date -u +%H%M%S)
DATA=${CLOUD_QA_STATE}/data; C=/storage/.config
plant() { # <tag>: the cell's conf with PL-015's --exclude, a save and a .tmp named m-<run>-<tag>, the argv stand-in
  TAG="${RUN}-$1"
  python3 -I - "${CELL}${C}/cloud_sync.conf" <<'EOD'
import sys
p = sys.argv[1]; s = open(p).read()
old = 'RCLONEOPTS="--progress \\\n'
assert s.count(old) == 1, s.count(old)
open(p, "w").write(s.replace(old, 'RCLONEOPTS="--progress \\\n--exclude \\"*.tmp\\" \\\n'))
EOD
  mkdir -p "${CELL}/storage/roms/savestates" "${CELL}/drv/bin"
  printf 'save %s\n' "${TAG}" > "${CELL}/storage/roms/savestates/m-${TAG}.state"
  printf 'scratch %s\n' "${TAG}" > "${CELL}/storage/roms/savestates/m-${TAG}.tmp"
  printf '#!/bin/sh\necho "$*" >> /var/log/rclone-argv.log\nexec /usr/bin/rclone "$@"\n' > "${CELL}/drv/bin/rclone"; chmod 755 "${CELL}/drv/bin/rclone"
}
opts() { awk '/^RCLONEOPTS=/{p=1} p{printf "%s|", $0; if ($0 !~ /\\$/) {p=0}}' "$1"; }
helper() { "${SBX}" bash -c "/usr/bin/cloud_sync_helper /var/log/cloud_sync.log > /dev/null 2>&1; echo \"  the helper: rc=\$?\"" 2>&1; }
backup() {
  "${SBX}" bash -c "PATH=/drv/bin:\${PATH} cloud_backup --yes --saves-only > /tmp/b.out 2>&1; echo \"  cloud_backup --yes --saves-only: rc=\$?, \$(grep -E '^Game saves:' /tmp/b.out)\"" 2>&1 | mask
  echo "    the copy's argv: $(grep -E '^copy ' "${CELL}/log/rclone-argv.log" 2>/dev/null | tail -1 | grep -oE -- '--(exclude|include|filter)[^ ]*( [^-][^ ]*)?' | tr '\n' ' ' || true)"
  echo "    in the cloud: $(cd "${DATA}/pixelelated/Saves/savestates" 2>/dev/null && ls | grep -- "m-${TAG}\." | tr '\n' ' ')"
}

for c in ${CELLS}; do case "${c}" in
move)
  echo "== S6-move ($(now))"
  new_cell s6move; plant move; F="${CELL}${C}/cloud_sync.conf"; RF="${CELL}${C}/cloud_sync-rules.txt"
  echo "  the conf's RCLONEOPTS: $(opts "${F}")"
  helper
  echo "  after one run: RCLONEOPTS $(opts "${F}")"
  echo "    the rules file: '- *.tmp' on line $(grep -n -x -F -- '- *.tmp' "${RF}" | cut -d: -f1 | tr '\n' ' '); the catch-all on line $(grep -n -x -- '- /\*\*' "${RF}" | cut -d: -f1); the player's section heads line $(grep -n 'Your own rules' "${RF}" | cut -d: -f1)"
  echo "    cloud_sync.conf.bak: $([ -e "${F}.bak" ] && echo "kept, its RCLONEOPTS $(opts "${F}.bak")" || echo none)"
  echo "    the log: $(grep -E 'filter flags|allowlist' "${CELL}/log/cloud_sync.log" | cut -c22-220 | tr '\n' '|')"
  "${DONOR}/usr/bin/rclone" lsf -R --files-only --filter-from "${RF}" "${CELL}/storage/roms" --config /dev/null > "${CELL}/drv/lsf" 2>&1
  echo "    rclone lsf with these rules over the saves: rc=$? $(grep -- "m-${TAG}\." "${CELL}/drv/lsf" | tr '\n' ' ')"
  s1=$(sha256sum "${F}" "${RF}" | cut -c1-16 | tr '\n' ' ')
  helper
  echo "  the second run: conf and rules $([ "$(sha256sum "${F}" "${RF}" | cut -c1-16 | tr '\n' ' ')" = "${s1}" ] && echo "byte for byte as after the first (${s1})" || echo "CHANGED ($(sha256sum "${F}" "${RF}" | cut -c1-16 | tr '\n' ' '), were ${s1})")"
  backup
  echo ;;
refuse)
  echo "== S6-refuse: the rules file cut before its catch-all, no .bak ($(now))"
  new_cell s6refuse; plant refuse; F="${CELL}${C}/cloud_sync.conf"; RF="${CELL}${C}/cloud_sync-rules.txt"
  n=$(grep -n -x -- '- /\*\*' "${RF}" | cut -d: -f1); head -n $((n - 3)) "${RF}" > "${RF}.cut" && mv "${RF}.cut" "${RF}"
  c0=$(sha256sum "${F}" | cut -c1-16)
  helper
  echo "  the conf after the helper: $([ "$(sha256sum "${F}" | cut -c1-16)" = "${c0}" ] && echo "as it was (${c0})" || echo changed); RCLONEOPTS $(opts "${F}")"
  echo "    the helper's log: $(grep -E 'filter flags|catch-all' "${CELL}/log/cloud_sync.log" | cut -c22-200 | tr '\n' '|')"
  backup
  echo "    the run's log: $(grep -E 'allowlist|catch-all line; refusing' "${CELL}/log/cloud_sync.log" | grep cloud_backup | cut -c22-200 | tr '\n' '|')"
  echo ;;
esac; done
echo "== end $(now)"
