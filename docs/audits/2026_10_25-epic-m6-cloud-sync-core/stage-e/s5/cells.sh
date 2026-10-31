#!/bin/bash
# T16 stage E, S5 (PL-08, PL-09, PL-10, PL-14). Run on a root: ROOT=<root> s5/cells.sh [cell ...]; the
# QA WebDAV up for `recent`. The recipe's unpack() is read from the root's source (SRC: 8ebaf8daad by
# git show, or the tree).
#  probe   the twins' --progress-terminal-width lines; the donor rclone's help and its answer to the flag
#  awk     the donor busybox awk and gensub (cloud_restore's near_names comment)
#  fns     tools/t16-functions.py over the root's three scripts: the uncalled list
#  recent  cloud_backup as the game-exit sync starts it (--yes --saves-only --recent --automatic), then a
#          deliberate saves backup: the helper's lines in each run's log
#  grace   cloud_net_ready with an nmcli stand-in in /drv/bin (STATE, CONNECTIVITY from the cell): how long
#          to exit 0 for connected/full, connected/limited and connected (site only)/limited
#  unpack  the recipe's unpack() as a function over a scratch SOURCES holding a good zip, then a broken
#          one; errexit off, and on as config/path sets it; the cache's file and PKG_BUILD after each
. "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/tools/lib.sh"
A="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CELLS="${*:-probe awk fns recent grace unpack}"
SRCID=$(cat "${ROOT}/SRC")
header "S5 the exit path's cost, the dead code, the comments, the recipe's unpack"
RUN=$(date -u +%H%M%S)
clean() { sed 's/\x1b\[[0-9;]*[A-Za-z]//g' | tr '\r' '\n' | grep -v -E '^[[:space:]]*$' | mask; }

for c in ${CELLS}; do case "${c}" in
probe)
  echo "== S5-probe ($(now))"
  for f in cloud_backup cloud_restore; do echo "  ${f}: lines naming --progress-terminal-width: $(grep -c progress-terminal-width "${ROOT}/usr/bin/${f}")"; done
  echo "  donor rclone help | grep -c progress-terminal-width: $("${DONOR}/usr/bin/rclone" help 2>/dev/null | grep -c progress-terminal-width)"
  "${DONOR}/usr/bin/rclone" version --progress-terminal-width=80 > "${HL}/cells/s5probe.${RUN}.out" 2>&1
  echo "  donor rclone version --progress-terminal-width=80: rc=$? $(head -1 "${HL}/cells/s5probe.${RUN}.out" | cut -c1-80)"
  echo ;;
awk)
  echo "== S5-awk: the donor's awk ($(now))"
  echo "  awk -> $(readlink "${DONOR}/usr/bin/awk"); gensub: $(echo abc | "${DONOR}/usr/bin/busybox" awk '{ print gensub(/b/, "<b>", "g") }') rc=$?"
  n=$(grep -n 'gensub' "${ROOT}/usr/bin/cloud_restore" | head -1)
  echo "  cloud_restore's line: ${n:-none naming gensub}"
  echo ;;
fns)
  echo "== S5-fns: tools/t16-functions.py over the root's scripts ($(now))"
  D=$(mktemp -d "${HL}/cells/s5fns.XXXXXX")
  cp "${ROOT}/usr/bin/cloud_backup" "${ROOT}/usr/bin/cloud_restore" "${ROOT}/usr/bin/cloud_capture" "${D}/"
  python3 -I -B "${A}/tools/t16-functions.py" "${D}" "${WT}/.qa-scratch/t16/oracle.json" | python3 -c 'import json,sys; d=json.load(sys.stdin); print("  by script", d["by_script"], "| uncalled", d["uncalled"] or "none", "| the tool'"'"'s count deltas (it counts 8ebaf8daad)", d["deltas"] or "none")'
  echo ;;
recent)
  for args in "--yes --saves-only --recent --automatic" "--yes --saves-only"; do
    echo "== S5-recent: cloud_backup ${args} ($(now))"
    new_cell "s5recent${#args}"; mkdir -p "${CELL}/storage/roms/savestates"
    printf 'save %s\n' "${RUN}" > "${CELL}/storage/roms/savestates/r-${RUN}.state"
    "${SBX}" bash -c "cloud_backup ${args} > /tmp/r.out 2>&1; echo \"  rc=\$?\"; grep -E '^Game saves:' /tmp/r.out" 2>&1 | clean
    echo "  the log's helper lines: $(grep -c '\[cloud_sync_helper\]' "${CELL}/log/cloud_sync.log")"
    echo "  its lines on the rules and config: $(grep -E 'rules and config|Updating cloud sync' "${CELL}/log/cloud_sync.log" | cut -c22-160 | tr '\n' '|')"
  done; echo ;;
grace)
  echo "== S5-grace: cloud_net_ready, NetworkManager's answer from a stand-in ($(now))"
  new_cell s5grace
  mkdir -p "${CELL}/drv/bin"
  printf '#!/bin/sh\ncase "$*" in *CONNECTIVITY*) echo "${NM_CONN}" ;; *STATE*) echo "${NM_STATE}" ;; esac\n' > "${CELL}/drv/bin/nmcli"
  chmod 755 "${CELL}/drv/bin/nmcli"
  "${SBX}" bash -c '
    echo "  default route here: $(ip -4 route show default | head -1 | cut -d" " -f1-3)"
    for s in "connected:full" "connected:limited" "connected (site only):limited"; do
      t0=${EPOCHREALTIME}
      out=$(PATH=/drv/bin:${PATH} NM_STATE="${s%%:*}" NM_CONN="${s##*:}" cloud_net_ready --wait 20); rc=$?
      t1=${EPOCHREALTIME}
      ms=$(( (${t1/./} - ${t0/./}) / 1000 ))
      echo "  ${s%%:*}, connectivity ${s##*:}: rc=${rc} after ${ms} ms; stdout: ${out:-nothing}"
    done
    echo "  the log: $(grep cloud_net_ready /var/log/cloud_sync.log | cut -c22-200 | tr "\n" "|")"' 2>&1
  echo ;;
unpack)
  echo "== S5-unpack: the recipe's unpack() from ${SRCID} ($(now))"
  U=$(mktemp -d "${HL}/cells/s5unpack.XXXXXX")
  if [ "${SRCID}" = tree ]; then cp "${WT}/projects/ROCKNIX/packages/network/rclone/package.mk" "${U}/package.mk"
  else git -C "${WT}" show "${SRCID}:projects/ROCKNIX/packages/network/rclone/package.mk" > "${U}/package.mk"; fi
  sed -n '/^unpack() {/,/^}/p' "${U}/package.mk" > "${U}/fn"
  echo "  the function: $(wc -l < "${U}/fn") lines, sha256 $(sha256sum "${U}/fn" | cut -c1-16)"
  python3 -I -c 'import sys, zipfile; z = zipfile.ZipFile(sys.argv[1], "w"); z.writestr("rclone-v1.75.2-linux-amd64/rclone", "a stand-in binary\n"); z.close()' "${U}/good.zip"
  head -c 40 "${U}/good.zip" > "${U}/broken.zip"
  for z in good broken; do for e in off on; do
    S="${U}/${z}-${e}/sources"; B="${U}/${z}-${e}/build"; mkdir -p "${S}/rclone"
    cp "${U}/${z}.zip" "${S}/rclone/rclone-1.75.2.zip"; printf 'x  rclone-1.75.2.zip\n' > "${S}/rclone/rclone-1.75.2.zip.sha256"
    set_e=""; [ "${e}" = on ] && set_e="set -e;"
    bash -c "${set_e} SOURCES='${S}'; PKG_BUILD='${B}'; PKG_VERSION=1.75.2; RCLONE_ARCH=amd64; . '${U}/fn'; unpack > '${U}/${z}-${e}.out' 2>&1; echo \"returned \$?\"" > "${U}/${z}-${e}.rc" 2>&1
    rc=$?
    echo "  ${z} zip, errexit ${e}: the shell rc=${rc} ($(cat "${U}/${z}-${e}.rc" | tr '\n' ' ')); sources/rclone: $(cd "${S}/rclone" && ls | tr '\n' ' '); build: $(cd "${B}" 2>/dev/null && find . -type f | tr '\n' ' ')"
  done; done
  echo "  host unzip: $(unzip -v | head -1 | cut -c1-40) (the build container's runs the recipe)"
  echo ;;
esac; done
echo "== end $(now)"
