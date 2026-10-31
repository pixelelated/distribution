#!/bin/bash
# T16 stage E, S6 (PL-12, PL-17, PL-23, D-CLOUD-185 under ruling 10). Run on a root:
# ROOT=<root> s6/cells.sh [cell ...]; the QA WebDAV up for `netopts`. Each helper cell runs
# cloud_sync_helper whole in the sandbox on a planted /storage/.config.
#  keytest    SAVES_REMOTE= removed, a comment naming it left: is the key added?
#  vedit      SAVES_REMOTE with a double space and a "-v " in the folder, RCLONEOPTS with --verbose
#  tmpro      a player's rule at the top of the rules file, /tmp read-only (SBX_LATE)
#  cutrules   the rules file cut inside the player's rules (mid-line), a whole .bak beside it; then no .bak
#  nonl       the merge marker present, a player's rule as the last line with no newline
#  createro   no conf, /storage/.config a full card (a 256 KiB tmpfs, filled): the create branch
#  freshsync  a conf the helper creates, then BACKUPMETHOD="sync" by hand, then the helper again
#  waitlast   cloud_saves_root check --wait (no value) under timeout 5
#  cleanup    cloud_sync_cleanup_duplicates.sh on two planted confs (G-07's comment, G-26's
#             continuation that looks like an assignment); bash -n of each after
#  netopts    cloud_backup --yes --saves-only with RCLONE_NET_OPTS carrying --delete-excluded and
#             RCLONEOPTS carrying --fast-list, an argv-recording rclone first on PATH
. "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/tools/lib.sh"
CELLS="${*:-keytest vedit tmpro cutrules nonl createro freshsync waitlast cleanup netopts}"
header "S6 the helper's seams, the twins' quoting and allowlist, --wait, the cleanup"
RUN=$(date -u +%H%M%S)
C=/storage/.config
helper() { "${SBX}" bash -c "/usr/bin/cloud_sync_helper /var/log/cloud_sync.log > /dev/null 2>&1; echo \"  helper rc=\$?\"" 2>&1; }
hlog() { grep -h -E "$1" "${CELL}/log/cloud_sync.log" 2>/dev/null | cut -c22-230 | sed 's/^/    log: /'; }

for c in ${CELLS}; do case "${c}" in
keytest)
  echo "== S6-keytest ($(now))"
  new_cell s6key; F="${CELL}${C}/cloud_sync.conf"
  sed -i 's|^SAVES_REMOTE=.*|# SAVES_REMOTE="/an/old/folder" (a note the player wrote)|' "${F}"
  echo "  before: $(grep -c '^SAVES_REMOTE=' "${F}") SAVES_REMOTE= lines, $(grep -c '^# SAVES_REMOTE=' "${F}") comment naming it"
  helper
  echo "  after: SAVES_REMOTE= lines: $(grep -c '^SAVES_REMOTE=' "${F}") ($(grep '^SAVES_REMOTE=' "${F}"))"
  hlog 'SAVES_REMOTE'
  echo ;;
vedit)
  echo "== S6-vedit ($(now))"
  new_cell s6vedit; F="${CELL}${C}/cloud_sync.conf"
  sed -i 's|^SAVES_REMOTE=.*|SAVES_REMOTE="/My  Saves/dev -v box"|' "${F}"
  sed -i 's|^RCLONEOPTS="--progress \\|RCLONEOPTS="--progress --verbose \\|' "${F}"
  echo "  before: $(grep '^SAVES_REMOTE=' "${F}") | $(grep '^RCLONEOPTS=' "${F}")"
  helper
  echo "  after:  $(grep '^SAVES_REMOTE=' "${F}") | $(grep '^RCLONEOPTS=' "${F}")"
  hlog 'verbose|conflicting'
  echo ;;
tmpro)
  echo "== S6-tmpro: /tmp read-only ($(now))"
  new_cell s6tmpro; F="${CELL}${C}/cloud_sync-rules.txt"
  { printf '+ /my-own-folder/**\n'; cat "${ROOT}/usr/config/cloud_sync-rules.txt"; } > "${F}.x" && mv "${F}.x" "${F}"
  : > "${CELL}${C}/.cloud_sync-rules-user-first-applied"
  echo "  before: the player's rule on line $(grep -n -x '+ /my-own-folder/\*\*' "${F}" | cut -d: -f1); sha256 $(sha256sum "${F}" | cut -c1-16)"
  SBX_LATE="--remount-ro /tmp" helper
  echo "  after:  the player's rule: $(grep -c -x '+ /my-own-folder/\*\*' "${F}") line(s); sha256 $(sha256sum "${F}" | cut -c1-16); .bak: $([ -e "${F}.bak" ] && echo present || echo absent); .new: $([ -e "${F}.new" ] && echo present || echo absent)"
  hlog 'scratch|Updated cloud_sync-rules|rules file'
  echo ;;
cutrules)
  for bak in whole none; do
    echo "== S6-cutrules: the rules file cut inside the player's rules, its .bak ${bak} ($(now))"
    new_cell "s6cut${bak}"; F="${CELL}${C}/cloud_sync-rules.txt"
    { printf '+ /my-own-folder/**\n+ /second-rule/**\n'; cat "${ROOT}/usr/config/cloud_sync-rules.txt"; } > "${CELL}/drv/whole"
    : > "${CELL}${C}/.cloud_sync-rules-user-first-applied"
    printf '+ /my-own-folder/**\n+ /sec' > "${F}"
    [ "${bak}" = whole ] && cp "${CELL}/drv/whole" "${F}.bak"
    echo "  the cut file: $(tr '\n' '|' < "${F}"); .bak: $([ -e "${F}.bak" ] && echo "whole, with both of the player's rules ($(grep -c -x -e '+ /my-own-folder/\*\*' -e '+ /second-rule/\*\*' "${F}.bak") lines)" || echo none)"
    cutsum=$(sha256sum "${F}" | cut -c1-16)
    helper
    echo "  after: catch-all $(grep -c -x -- '- /\*\*' "${F}"); '+ /my-own-folder/**' $(grep -c -x '+ /my-own-folder/\*\*' "${F}"), '+ /second-rule/**' $(grep -c -x '+ /second-rule/\*\*' "${F}"), '+ /sec' $(grep -c -x '+ /sec' "${F}"); the file $([ "$(sha256sum "${F}" | cut -c1-16)" = "${cutsum}" ] && echo "as it was (cut)" || echo replaced); .bak $([ -e "${F}.bak" ] && echo present || echo none)"
    hlog 'catch-all|Updated cloud_sync-rules'
  done; echo ;;
nonl)
  echo "== S6-nonl: the last line with no newline ($(now))"
  new_cell s6nonl; F="${CELL}${C}/cloud_sync-rules.txt"
  : > "${CELL}${C}/.cloud_sync-rules-user-first-applied"
  { cat "${ROOT}/usr/config/cloud_sync-rules.txt"; printf '+ /late-rule/**'; } > "${F}.x" && mv "${F}.x" "${F}"
  echo "  before: the last bytes $(tail -c 16 "${F}" | od -An -c | tr -s ' ' | cut -c1-70)"
  helper
  echo "  after: '+ /late-rule/**' on line(s) $(grep -n -x '+ /late-rule/\*\*' "${F}" | cut -d: -f1 | tr '\n' ' ')"
  echo ;;
createro)
  echo "== S6-createro: no conf, /storage/.config a full card ($(now))"
  new_cell s6create   # the tmpfs over /storage/.config starts empty: no conf, no rules
  printf 'C=/storage/.config\ndd if=/dev/zero of="${C}/.filler" bs=1024 2>/dev/null\n/usr/bin/cloud_sync_helper /var/log/cloud_sync.log >/dev/null 2>&1; echo "  helper rc=$?"\nls -a "${C}" | grep -v "^\\.*$\\|filler" | sed "s/^/    left in .config: /"\n' > "${CELL}/drv/c.sh"
  SBX_EXTRA="--size 262144 --tmpfs /storage/.config" "${SBX}" bash /drv/c.sh 2>&1
  hlog 'template|creating'
  echo ;;
freshsync)
  echo "== S6-freshsync ($(now))"
  new_cell s6fresh; rm -f "${CELL:?}${C}/cloud_sync.conf"
  helper
  echo "  created: $(grep '^BACKUPMETHOD=' "${CELL}${C}/cloud_sync.conf"); markers: $(cd "${CELL}${C}" && ls -a | grep -c 'applied$')"
  sed -i 's|^BACKUPMETHOD=.*|BACKUPMETHOD="sync"|' "${CELL}${C}/cloud_sync.conf"
  echo "  set by hand: $(grep '^BACKUPMETHOD=' "${CELL}${C}/cloud_sync.conf")"
  helper
  echo "  after the next run: $(grep '^BACKUPMETHOD=' "${CELL}${C}/cloud_sync.conf")"
  hlog 'BACKUPMETHOD'
  echo ;;
waitlast)
  echo "== S6-waitlast: cloud_saves_root check --wait, no value ($(now))"
  new_cell s6wait
  "${SBX}" bash -c 't0=${EPOCHREALTIME}; timeout 5 cloud_saves_root check --wait > /tmp/w.out 2>&1; rc=$?; t1=${EPOCHREALTIME}; echo "  rc=${rc} after $(( (${t1/./} - ${t0/./}) / 1000 )) ms; out: $(tr "\n" "|" < /tmp/w.out)"' 2>&1
  echo ;;
cleanup)
  echo "== S6-cleanup ($(now))"
  new_cell s6clean
  printf 'LOG_LEVEL="info"\nLOG_LEVEL="debug" # set by hand on the console \\\nSAVES_REMOTE="/pixelelated/Saves"\nSETTINGS_REMOTE="/pixelelated/Backups"\n' > "${CELL}/storage/g07.conf"
  printf 'RCLONEOPTS="--progress \\\nCONTENT_REMOTE=x \\\n--log-file /var/log/cloud_sync.log"\nCONTENT_REMOTE="/pixelelated/Content"\nLOG_LEVEL="info"\nLOG_LEVEL="info"\n' > "${CELL}/storage/g26.conf"
  for g in g07 g26; do
    echo "  ${g} before: $(tr '\n' '|' < "${CELL}/storage/${g}.conf")"
    "${SBX}" bash -c "cloud_sync_cleanup_duplicates.sh /storage/${g}.conf > /dev/null 2>&1; echo \"  rc=\$?\"; echo \"  ${g} after:  \$(tr '\n' '|' < /storage/${g}.conf)\"; bash -n /storage/${g}.conf && echo '  bash -n: ok' || echo '  bash -n: FAILS'; ( . /storage/${g}.conf; echo \"  sourced: LOG_LEVEL=\${LOG_LEVEL:-unset} SAVES_REMOTE=\${SAVES_REMOTE:-unset} CONTENT_REMOTE=\${CONTENT_REMOTE:-unset}\" )" 2>&1
  done; echo ;;
netopts)
  echo "== S6-netopts ($(now))"
  new_cell s6net; F="${CELL}${C}/cloud_sync.conf"
  sed -i 's|^RCLONE_NET_OPTS=.*|RCLONE_NET_OPTS="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1 --delete-excluded --bwlimit 1M"|' "${F}"
  sed -i 's|^RCLONEOPTS="--progress \\|RCLONEOPTS="--progress --fast-list \\|' "${F}"
  mkdir -p "${CELL}/storage/roms/savestates" "${CELL}/drv/bin"; printf 'save %s\n' "${RUN}" > "${CELL}/storage/roms/savestates/n-${RUN}.state"
  printf '#!/bin/sh\necho "$*" >> /var/log/rclone-argv.log\nexec /usr/bin/rclone "$@"\n' > "${CELL}/drv/bin/rclone"; chmod 755 "${CELL}/drv/bin/rclone"
  "${SBX}" bash -c "PATH=/drv/bin:\${PATH} cloud_backup --yes --saves-only > /tmp/n.out 2>&1; echo \"  rc=\$?\"; grep -E '^Game saves:' /tmp/n.out" 2>&1 | mask
  echo "  the copy's argv: $(grep -E '^copy ' "${CELL}/log/rclone-argv.log" | head -1 | mask | cut -c1-260)"
  echo "  --delete-excluded in any argv: $(grep -c -- '--delete-excluded' "${CELL}/log/rclone-argv.log"); --fast-list: $(grep -c -- '--fast-list' "${CELL}/log/rclone-argv.log")"
  hlog 'allowlist|network bound'
  echo ;;
esac; done
echo "== end $(now)"
