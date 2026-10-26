#!/usr/bin/env bash
# T19 S5 (#666, #1161, #1166): a stamp, an undo or a restore that failed is
# reported, and the ctl's stderr outlives pending_lock.
#
#   t19-s5-writers.sh <ctl> <client-linux-dir> <workdir>
#
# The real <ctl> in t19-ctl-sandbox.sh's sandbox; <client-linux-dir> is the
# pin with the tree's patches applied (its linux/), on PYTHONPATH as /client.
#   1. scan with nothing to scan and last-scan a folder: the stamp cannot be
#      written -- does the run say so?
#   2. the same scan with no stamp yet (the control): the new line
#   3. enable whose toggle write fails and whose hardcore restore then fails:
#      does the undo say what it could not put back?
#   4. disable whose service will not stop: is it said, in the exit too?
#   5. ack_index_pending (lifted whole from <ctl>) whose put-back of a newer
#      marker fails: is the aside -- the only copy -- kept?
#   6. index-offline whose write fails while pending_lock holds the lock: does
#      fail's line reach stderr (#1166)?
# Exit 0 when every check holds (the fixed ctl), 1 when one does not, 2 when
# the run could not be made.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "${HERE}/t19-ctl-sandbox.sh"
[ $# -eq 3 ] || { sed -n '2,19p' "$0"; exit 2; }
CL="$(realpath "$2")"; [ -d "${CL}/raofflineproxy" ] || { echo "CANNOT: no client at ${CL}" >&2; exit 2; }
t19_setup "$1" "$3" || exit 2
t19_versions
CFG="${T19_W}/storage/.config/system/configs/system.cfg"; PD="${T19_W}/storage/.config/raofflineproxy"; RUN="${T19_W}/run"
MARK="${T19_W}/storage/.cache/services/raofflineproxy.conf"
pv() { sed -n "s/^${1}=//p" "${CFG}"; }
account() { printf 'global.retroachievements=1\nglobal.retroachievements.username=t19player\n%s\n' "global.retroachievements.$(printf tok)en=syntokone"; }
cat > "${T19_W}/shim/python3" <<'EOS'
#!/bin/sh
if [ "$1 $2 $3" = "-m raofflineproxy.main probe-online" ]; then printf '{"online": true}\n' > "${RAOFFLINEPROXY_CONFIG_DIR}/online_state.json"; exit 0; fi
exec /usr/bin/python3 "$@"
EOS
chmod +x "${T19_W}/shim/python3"; mkdir -p "${T19_W}/storage/roms"
scan() { T19_BINDS=(--ro-bind "${CL}" /client); T19_ENV=(--setenv PYTHONPATH /client); t19_ctl scan; }

echo "  1. scan, nothing to scan, last-scan a folder"
{ account; echo global.retroachievements.offlineproxy=1; } > "${CFG}"
mkdir -p "${PD}/last-scan"
scan
echo "     rc ${RC}; stdout $(tr '\n' '|' < "${OUT}"); stderr $(tail -c 300 "${ERR}" | tr '\n' '|')"
echo "     in the proxy folder: $(cd "${PD}" && find . -name 'last-scan*' | sort | tr '\n' ' ')"
[ "${RC}" -ne 0 ]; t19_check $? "the run ends non-zero" "rc ${RC}"
grep -qx '>>> why STAMP_UNWRITABLE' "${OUT}"; t19_check $? "and tells the page why" "stdout: $(tr '\n' '|' < "${OUT}")"
[ -z "$(cd "${PD}" && find . -name 'last-scan.tmp*')" ]; t19_check $? "and leaves no temporary, in the folder or under the stamp's name" "$(cd "${PD}" && find . -name 'last-scan.tmp*' | tr '\n' ' ')"
rm -rf "${PD:?}/last-scan"

echo "  2. scan, nothing to scan, no stamp yet (the control)"
scan
echo "     rc ${RC}; last-scan: $(cat "${PD}/last-scan" 2>/dev/null)"
[ "${RC}" -eq 0 ] && grep -q ' 0 scan .*note=NO_GAMES$' "${PD}/last-scan" 2>/dev/null; t19_check $? "the normal write is still the new line, rc 0" "rc ${RC}"

echo "  3. enable: the toggle's write fails, then hardcore's put-back fails"
{ account; echo global.retroachievements.hardcore=1; } > "${CFG}"
mkdir -p "${RUN}/fail-set.d"; echo 0 > "${RUN}/fail-set.d/global.retroachievements.offlineproxy"; echo 1 > "${RUN}/fail-set.d/global.retroachievements.hardcore"
t19_ctl enable
echo "     rc ${RC}; hardcore now $(pv global.retroachievements.hardcore) (was 1); stderr $(grep '^raofflineproxy-ctl:' "${ERR}" | tr '\n' '|')"
[ "${RC}" -ne 0 ]; t19_check $? "enable fails (the control)" "rc ${RC}"
grep -q '^raofflineproxy-ctl: .*global.retroachievements.hardcore could not be put back' "${ERR}"; t19_check $? "and says hardcore could not be put back, not that the device is as it was" "stderr: $(tail -c 300 "${ERR}" | tr '\n' '|')"
rm -rf "${RUN:?}/fail-set.d"

echo "  4. disable: the service will not stop"
{ account; echo global.retroachievements.hardcore=0; echo global.retroachievements.offlineproxy=1; echo global.retroachievements.offlineproxy.hardcore_was=1; } > "${CFG}"
mkdir -p "$(dirname "${MARK}")"; : > "${MARK}"; : > "${RUN}/active"; : > "${RUN}/fail-stop"
t19_ctl disable
echo "     rc ${RC}; toggle $(pv global.retroachievements.offlineproxy), hardcore $(pv global.retroachievements.hardcore), marker $([ -e "${MARK}" ] && echo yes || echo no); stderr $(tail -c 300 "${ERR}" | tr '\n' '|')"
[ "${RC}" -ne 0 ] && grep -q "^raofflineproxy-ctl: .*did not stop" "${ERR}"; t19_check $? "a service that did not stop is said, and the exit is non-zero" "rc ${RC}"
[ "$(pv global.retroachievements.offlineproxy)" = 0 ] && [ "$(pv global.retroachievements.hardcore)" = 1 ] && [ ! -e "${MARK}" ]; t19_check $? "and the rest of disable is done: toggle 0, hardcore back to 1, no marker" "toggle $(pv global.retroachievements.offlineproxy), hardcore $(pv global.retroachievements.hardcore)"
rm -f "${RUN}/fail-stop"

echo "  5. ack_index_pending: a newer marker, and its put-back fails"
{
    echo 'INDEX_PENDING=/storage/.config/raofflineproxy/index-pending; PENDING_LOCK=/var/run/raofflineproxy-index-pending.lock'
    sed -n '/^say() {/,/^}/p; /^slog() {/,/^}/p; /^pending_lock() {/,/^}/p; /^pending_unlock() {/,/^}/p; /^ack_index_pending() {/,/^}/p' "${T19_W}/repo/raofflineproxy-ctl"
    echo 'ack_index_pending older; echo "ack rc $?"'
} > "${T19_W}/repo/ack.sh"
grep -q '^ack_index_pending() {' "${T19_W}/repo/ack.sh" || { echo "CANNOT: ack_index_pending not found in the ctl"; exit 2; }
cat > "${T19_W}/shim/mv" <<'EOS'
#!/bin/sh
# Refuse only the put-back: a move from an aside onto the marker's own path.
a=""; b=""; for x in "$@"; do case "${x}" in -*) ;; *) a="${b}"; b="${x}" ;; esac; done
case "${a}:${b}" in *index-pending.ack.*:*/index-pending) echo "mv: refused (fixture)" >&2; exit 1 ;; esac
exec /t19bb/busybox mv "$@"
EOS
chmod +x "${T19_W}/shim/mv"
printf 'newer 1 2\n' > "${PD}/index-pending"
t19_run /usr/bin/bash /repo/ack.sh
echo "     ${RC}; $(cat "${OUT}"); stderr $(tail -c 240 "${ERR}" | tr '\n' '|'); left: $(cd "${PD}" && ls index-pending* 2>/dev/null | tr '\n' ' ')"
[ -n "$(cd "${PD}" && ls index-pending.ack.* 2>/dev/null)" ] && grep -q 'newer' "${PD}"/index-pending.ack.* 2>/dev/null; t19_check $? "the aside, the only copy of the newer marker, is kept" "left: $(cd "${PD}" && ls index-pending* 2>/dev/null | tr '\n' ' ')"
grep -q 'could not be put back' "${RUN}/say.log"; t19_check $? "and it is said (say, the journal's line)" "say: $(tail -n 2 "${RUN}/say.log" | tr '\n' '|')"
rm -f "${T19_W}/shim/mv"

echo "  6. index-offline whose write fails under pending_lock (#1166): does fail's line reach stderr?"
cat > "${T19_W}/shim/mv" <<'EOS'
#!/bin/sh
# Refuse only the publication of the marker's temporary, so the write fails
# while pending_lock is held.
for x in "$@"; do case "${x}" in *index-pending.tmp*) echo "mv: refused (fixture)" >&2; exit 1 ;; esac; done
exec /t19bb/busybox mv "$@"
EOS
chmod +x "${T19_W}/shim/mv"; rm -f "${PD}"/index-pending*
t19_ctl index-offline
echo "     rc ${RC}; stderr: $(tr '\n' '|' < "${ERR}" | cut -c1-240)"
[ "${RC}" -eq 1 ]; t19_check $? "index-offline fails (the control)" "rc ${RC}"
grep -q '^raofflineproxy-ctl: cannot write /storage/.config/raofflineproxy/index-pending$' "${ERR}"; t19_check $? "and fail's own line reaches stderr after pending_lock" "stderr: $(tr '\n' '|' < "${ERR}" | cut -c1-200)"
rm -f "${T19_W}/shim/mv"

echo "t19-s5-writers: ${FAILS} FAIL"
[ "${FAILS}" -eq 0 ]
