#!/bin/bash
# T16 stage E, S2 (#1298, #1299, #1301, PL-19). Run on a root: ROOT=<root> s2/cells.sh [cell ...]
# Cells: group stamp kept sweep readers remote g01f. The QA WebDAV must be up at 100k
# (cloud-test-backend --backend webdav up with CLOUD_QA_BWLIMIT=100k). Host stand-ins: the header.
. "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/tools/lib.sh"
CELLS="${*:-group stamp kept sweep readers remote g01f}"
header "S2 the stop, the stamp, the kept copies, the sweep, the readers"
DATA=${CLOUD_QA_STATE}/data; SV=${DATA}/pixelelated/Saves
mkdir -p "${SV}/savestates" "${DATA}/pixelelated/Backups"
RUN=$(date -u +%H%M%S)
seed() { mkdir -p "$(dirname "${SV}/$1")"; head -c "$2" /dev/urandom > "${SV}/$1"; }
listing() { (cd "$1" 2>/dev/null && find . -type f | sort | sed 's|^\./||' | tr '\n' ' '); }

for c in ${CELLS}; do case "${c}" in
group)
  echo "== S2-group: cloud_restore --automatic as EmulationStation starts it (setsid sh -c), SIGTERM to the group at +5 s, SIGKILL at +6.5 s ($(now))"
  new_cell s2group; mkdir -p "${CELL}/storage/roms/savestates"; seed "savestates/g-${RUN}.state" 6291456
  cat > "${CELL}/drv/g.sh" <<'EOD'
S=$(date +%s)
setsid sh -c 'echo ">>> pid $$"; cloud_restore --yes --method=copy --update --saves-only --automatic' > /tmp/g.out 2>&1 &
sleep 1; G=$(sed -n 's/^>>> pid //p' /tmp/g.out | head -1); echo "group ${G}"
sleep 4; kill -TERM -- "-${G}" 2>/dev/null; echo "+$(( $(date +%s) - S ))s SIGTERM to the group"
sleep 1.5; kill -KILL -- "-${G}" 2>/dev/null; echo "+$(( $(date +%s) - S ))s SIGKILL to the group"
sleep 2; echo "+$(( $(date +%s) - S ))s alive: $(ps -o pid,args 2>/dev/null | grep -E 'timeout|rclone|cloud_restore' | grep -v grep | sed 's/--[a-z-]* [^ ]*//g' | cut -c1-60 | tr '\n' ';' )"
sleep 30; echo "+$(( $(date +%s) - S ))s the saves tree: $(cd /storage/roms && find . -type f | sort | tr '\n' ' ')"
echo "stamp last-restore: $(cat /storage/.cache/cloud_sync/last-restore 2>/dev/null || echo none)"
EOD
  "${SBX}" bash /drv/g.sh 2>&1; echo ;;
stamp)
  echo "== S2-stamp: an automatic restore, one small save landed, then TERM to the script's pid alone at +5 s ($(now))"
  new_cell s2stamp; mkdir -p "${CELL}/storage/roms/savestates"
  seed "savestates/a-${RUN}.state" 4096; seed "savestates/z-${RUN}.state" 6291456
  cat > "${CELL}/drv/s.sh" <<'EOD'
S=$(date +%s)
cloud_restore --yes --method=copy --update --saves-only --automatic > /tmp/s.out 2>&1 &
P=$!; sleep 5; kill -TERM "${P}"; echo "+$(( $(date +%s) - S ))s TERM to ${P}; landed then: $(cd /storage/roms && find . -type f ! -name '*.partial' | sort | tr '\n' ' ')"
wait "${P}"; rc=$?; echo "+$(( $(date +%s) - S ))s the script ended, rc ${rc}"
sleep 1; echo "alive after it: $(ps -o pid,args 2>/dev/null | grep -E 'timeout|rclone' | grep -v grep | wc -l) timeout/rclone"
echo "stamp last-restore: $(cat /storage/.cache/cloud_sync/last-restore 2>/dev/null || echo none)"
echo "the saves tree: $(cd /storage/roms && find . -type f | sort | tr '\n' ' ')"
EOD
  "${SBX}" bash /drv/s.sh 2>&1; echo ;;
kept)
  echo "== S2-kept: three local saves to be replaced; restore 1 (KILL2's deliberate shape, under setsid) stopped by SIGTERM then SIGKILL to its group after the small one lands; a fourth save then newer in the cloud; restore 2 completes; restore 3 completes ($(now))"
  new_cell s2kept; L=${CELL}/storage/roms/savestates; mkdir -p "${L}"
  for i in 1 2 3 4; do printf 'v1 local %s\n' "${i}" > "${L}/k${i}-${RUN}.state"; touch -d '2020-01-01 00:00' "${L}/k${i}-${RUN}.state"; done
  seed "savestates/k1-${RUN}.state" 2048; seed "savestates/k2-${RUN}.state" 1048576; seed "savestates/k3-${RUN}.state" 1048576
  cat > "${CELL}/drv/k.sh" <<'EOD'
R=/storage/.cache/cloud_sync/replaced
show() { echo "  $1 -- saves: $(cd /storage/roms/savestates && for f in *; do printf '%s(%s) ' "${f}" "$(head -c 8 "${f}" | grep -q '^v1 local' && echo v1 || echo cloud)"; done)"; echo "     replaced/: $(cd ${R} 2>/dev/null && find . -type f | sort | tr '\n' ' ')"; }
setsid sh -c 'echo ">>> pid $$"; cloud_restore --yes --saves-only' > /tmp/k1.out 2>&1 &
sleep 1; G=$(sed -n 's/^>>> pid //p' /tmp/k1.out | head -1)
sleep 3; kill -TERM -- "-${G}" 2>/dev/null; sleep 1.5; kill -KILL -- "-${G}" 2>/dev/null; sleep 3
show "after restore 1, stopped at +4 s"
: > /storage/.go-k4; while [ ! -e /storage/.k4-done ]; do sleep 0.2; done; sleep 1.2
cloud_restore --yes --saves-only > /tmp/k2.out 2>&1; echo "  restore 2 rc=$?"
show "after restore 2 (completed)"
sleep 1.2; cloud_restore --yes --saves-only > /tmp/k3.out 2>&1; echo "  restore 3 rc=$?"
show "after restore 3 (completed)"
EOD
  ( while [ ! -e "${CELL}/storage/.go-k4" ]; do sleep 0.2; done; seed "savestates/k4-${RUN}.state" 2048; : > "${CELL}/storage/.k4-done" ) &
  "${SBX}" bash /drv/k.sh 2>&1; wait; echo ;;
sweep)
  echo "== S2-sweep (a): what the shipped rules admit, the donor's rclone lsf over a tree with a .partial ($(now))"
  T=$(mktemp -d "${HL}/cells/s2lsf.XXXXXX"); mkdir -p "${T}/savestates"; : > "${T}/savestates/n.state"; : > "${T}/savestates/n.state.abcdefgh.partial"
  echo "  listed: $("${DONOR}/usr/bin/rclone" lsf -R --files-only --filter-from "${ROOT}/usr/config/cloud_sync-rules.txt" "${T}" | tr '\n' ' ')"
  echo "== S2-sweep (b): a restore that completes over a dirty tree, a partial left in a folder that refuses the removal and no download writes ($(now))"
  new_cell s2sweep; L=${CELL}/storage/roms/nes-ro; mkdir -p "${L}" "${CELL}/storage/roms/gba"
  : > "${L}/x.state.abcdefgh.partial"; chmod 555 "${L}"; seed "gba/ok-${RUN}.srm" 1024
  cat > "${CELL}/drv/w.sh" <<'EOD'
cloud_restore --yes --saves-only > /tmp/w.out 2>&1; echo "  restore rc=$?"
echo "  the partial: $(find /storage/roms -name '*.partial' | tr '\n' ' ')"
echo "  restore-tree-clean: $([ -e /storage/.cache/cloud_sync/restore-tree-clean ] && echo PRESENT || echo absent)"
echo "  the log: $(grep -i -E 'sweep|partial' /var/log/cloud_sync.log | cut -c1-120 | tr '\n' '|')"
EOD
  "${SBX}" bash /drv/w.sh 2>&1; chmod 755 "${L}"; echo ;;
readers)
  echo "== S2-readers: SAVESPATH as the twins read it (the helper, then source) and as cloud_saves_root and cloud_capture read it alone ($(now))"
  new_cell s2read
  cat > "${CELL}/drv/r.sh" <<'EOD'
C=/storage/.config/cloud_sync.conf; cp "${C}" /tmp/base; grep -v '^SAVESPATH=' /tmp/base > /tmp/nosaves
reader() { bash -c 'CONF=/storage/.config/cloud_sync.conf; . <(sed -n "/^conf_value() {/,/^}/p;/^saves_path() {/,/^}/p" "$1"); saves_path' _ "$1" 2>/dev/null; }
printf '  %-48s %-34s %-34s %-34s %s\n' form twins cloud_saves_root cloud_capture verdict
form() {
  { cat /tmp/nosaves; printf '%s\n' "$2"; } > "${C}"
  /usr/bin/cloud_sync_helper /var/log/cloud_sync.log >/dev/null 2>&1
  t=$(bash -c '. /storage/.config/cloud_sync.conf 2>/dev/null; echo "${SAVESPATH}"'); s=$(reader /usr/bin/cloud_saves_root); k=$(reader /usr/bin/cloud_capture)
  v=FAIL; [ "${t}" = "${s}" ] && [ "${s}" = "${k}" ] && v=PASS
  [ -z "${t}" ] && [ "$3" = refused ] && v="PASS (the twins refuse it: $3)"
  printf '  %-48s %-34s %-34s %-34s %s\n' "$1" "'${t}'" "'${s}'" "'${k}'" "${v}"
}
form 'double quotes, default' 'SAVESPATH="/storage/roms"'
form 'double quotes, a trailing comment' 'SAVESPATH="/storage/games-external/roms" # card'
form 'single quotes' "SAVESPATH='/storage/games-external/roms'"
form 'single quotes, a trailing comment' "SAVESPATH='/storage/games-external/roms' # card"
form 'unquoted, a trailing comment' 'SAVESPATH=/storage/games-external/roms # card'
form 'BACKUPPATH only (before the helper migrates)' 'BACKUPPATH="/storage/games-external/roms"'
form 'assigned twice (the last wins under source)' "$(printf 'SAVESPATH="/storage/roms"\nSAVESPATH="/storage/games-external/roms"')"
form 'empty' 'SAVESPATH=""' refused
EOD
  "${SBX}" bash /drv/r.sh 2>&1; echo ;;
remote)
  echo "== S2-remote: does a zero-byte marker object land on the QA WebDAV and read back (rclone touch, then lsf) ($(now))"
  new_cell s2rem; RC=${CELL}/storage/.config/rclone/rclone.conf; RN=$(head -1 "${CELL}/storage/.config/rclone/active-connection")
  RCLONE_CONFIG=${RC} "${DONOR}/usr/bin/rclone" mkdir "${RN}:pixelelated/Saves-replaced/t-${RUN}" 2>&1 | tail -1
  RCLONE_CONFIG=${RC} "${DONOR}/usr/bin/rclone" touch "${RN}:pixelelated/Saves-replaced/t-${RUN}/.completed" 2>&1 | tail -1; echo "  touch rc=${PIPESTATUS[0]}"
  echo "  lsf of the folder: $(RCLONE_CONFIG=${RC} "${DONOR}/usr/bin/rclone" lsf "${RN}:pixelelated/Saves-replaced/t-${RUN}/" 2>&1 | tr '\n' ' ')"
  echo "  one listing for every marker: $(RCLONE_CONFIG=${RC} "${DONOR}/usr/bin/rclone" lsf -R --files-only --include '/*/.completed' --include '/*/.recovered' "${RN}:pixelelated/Saves-replaced/" 2>&1 | tr '\n' ' ')"
  echo ;;
rprune)
  echo "== S2-rprune: cloud_backup's prune_replaced_remote, lifted, over folders on the QA WebDAV: A completed, B unmarked (a stopped run's), C recovered by an earlier run, P this run's ($(now))"
  new_cell s2rp; RC=${CELL}/storage/.config/rclone/rclone.conf; RN=$(head -1 "${CELL}/storage/.config/rclone/active-connection"); RT="${RN}:pixelelated/Saves-replaced-${RUN}"
  for d in A B C P; do printf 'copy\n' > "${CELL}/f"; RCLONE_CONFIG=${RC} "${DONOR}/usr/bin/rclone" copyto "${CELL}/f" "${RT}/${d}/savestates/s.state" 2>/dev/null; done
  RCLONE_CONFIG=${RC} "${DONOR}/usr/bin/rclone" touch "${RT}/A/.completed" 2>/dev/null
  RCLONE_CONFIG=${RC} "${DONOR}/usr/bin/rclone" touch "${RT}/C/.recovered.EARLIER" 2>/dev/null
  echo "  before the prune: $(RCLONE_CONFIG=${RC} "${DONOR}/usr/bin/rclone" lsf -R --files-only "${RT}/" 2>/dev/null | sort | tr '\n' ' ')"
  RCLONE_CONFIG=${RC} PATH="${DONOR}/usr/bin:${PATH}" bash -c '. <(sed -n "/^prune_replaced_remote() {/,/^}/p" "$1"); log_message() { :; }; RCLONE_LIST_OPTS=(); RCLONE_NET_OPTS_ARRAY=(); prune_replaced_remote "$2" P' _ "${ROOT}/usr/bin/cloud_backup" "${RT}"
  echo "  after the prune (pinned P): $(RCLONE_CONFIG=${RC} "${DONOR}/usr/bin/rclone" lsf -R --files-only "${RT}/" 2>/dev/null | sort | tr '\n' ' ')"
  echo ;;
g01f)
  echo "== S2-g01f: g01-timeout-pgid's shape with --foreground, as the fixed wrapper calls timeout ($(now); $(gnutimeout --version | head -1))"
  P=$(mktemp "${HL}/cells/g01f.XXXXXX")
  setsid bash -c 'gnutimeout --foreground 6 sleep 5 & T=$!; sleep 0.3; C=$(pgrep -P $T); printf "%s %s\n" "$T" "$C" > "$1"; echo "  script pid $$ pgid $(ps -o pgid= -p $$ | tr -d " "); timeout pid $T pgid $(ps -o pgid= -p $T | tr -d " "); child $C pgid $(ps -o pgid= -p $C | tr -d " ")"; wait' _ "${P}" &
  O=$!; sleep 0.6; read -r T C < "${P}"; G=$(ps -o pgid= -p "${O}" | tr -d ' ')
  kill -KILL -- "-${G}"; echo "  SIGKILL to the script's group -${G}"; sleep 0.5
  echo "  after: timeout $(kill -0 "${T}" 2>/dev/null && echo alive || echo gone); child $(kill -0 "${C}" 2>/dev/null && echo alive || echo gone)"
  echo ;;
esac; done
echo "== end $(now)"
