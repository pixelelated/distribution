#!/usr/bin/env bash
# T19 S3 (#666, #1159): readiness is the service's own socket.
#
#   t19-s3-listening.sh <ctl> <workdir>
#
# The real <ctl> in t19-ctl-sandbox.sh's sandbox with a network namespace of
# its own (--unshare-net): a python stand-in bound to 0.0.0.0:8080, the way
# a foreign listener would hold the port, and the systemctl shim answering
# `show -p MainPID --value` with another process, the stand-in itself, or
# nothing. enable runs with a `start` that runs `listening --wait 2`, the
# unit's ExecStartPost. Exit 0 when every check holds (the fixed ctl), 1 when
# one does not (the unfixed), 2 when the run could not be made.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "${HERE}/t19-ctl-sandbox.sh"
[ $# -eq 2 ] || { sed -n '2,12p' "$0"; exit 2; }
t19_setup "$1" "$2" || exit 2
t19_versions
cat > "${T19_W}/repo/inner.sh" <<'EOI'
#!/usr/bin/bash
# <mainpid: other|own|none> <verb...>: the stand-in up, MainPID set, the ctl run.
WHO="$1"; shift
/usr/bin/python3 -I -c 'import socket,time
s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 8080)); s.listen(1); time.sleep(60)' &
SP=$!
N=0; until grep -q ':1F90 00000000:0000 0A' /proc/net/tcp; do N=$((N + 1)); [ "${N}" -lt 100 ] || { echo "stand-in never listened" >&2; kill "${SP}"; exit 2; }; sleep 0.1; done
case "${WHO}" in other) echo "$$" > /run/mainpid ;; own) echo "${SP}" > /run/mainpid ;; none) : > /run/mainpid; echo 0 > /run/mainpid ;; esac
echo "stand-in pid ${SP}; MainPID $(cat /run/mainpid); shell $$" >&2
/usr/bin/bash /repo/raofflineproxy-ctl "$@"; RCX=$?
kill "${SP}"; wait "${SP}" 2>/dev/null
exit "${RCX}"
EOI
CFG="${T19_W}/storage/.config/system/configs/system.cfg"; MARK="${T19_W}/storage/.cache/services/raofflineproxy.conf"
pv() { sed -n "s/^${1}=//p" "${CFG}"; }
run() { T19_BINDS=(--unshare-net); t19_run /usr/bin/bash /repo/inner.sh "$@"; }

echo "  1. listening, a stand-in on 0.0.0.0:8080 and MainPID another process"
run other listening; echo "     rc ${RC}; $(head -c 300 "${ERR}" | tr '\n' '|')"
[ "${RC}" -eq 1 ]; t19_check $? "listening is 1: the port is held, but not by the service" "rc ${RC}"
echo "  2. listening, MainPID the stand-in itself (the control)"
run own listening; echo "     rc ${RC}"
[ "${RC}" -eq 0 ]; t19_check $? "listening is 0 when the socket is the service's own" "rc ${RC}"
echo "  3. listening, no MainPID"
run none listening; echo "     rc ${RC}"
[ "${RC}" -eq 1 ]; t19_check $? "listening is 1 when the service has no main process" "rc ${RC}"
echo "  4. enable, the stand-in alone and a start that waits for the service's socket (the unit's ExecStartPost)"
printf 'system.hostname=X\nglobal.retroachievements=1\nglobal.retroachievements.hardcore=1\n' > "${CFG}"; touch "${T19_W}/run/start-runs-listening"
run other enable; echo "     rc ${RC}; stdout $(tr '\n' '|' < "${OUT}"); stderr $(tail -c 300 "${ERR}" | tr '\n' '|')"
[ "${RC}" -ne 0 ]; t19_check $? "enable fails" "rc ${RC}"
[ -z "$(pv global.retroachievements.offlineproxy)" ] && [ "$(pv global.retroachievements.hardcore)" = 1 ] && [ ! -e "${MARK}" ]
t19_check $? "and the device is as it was: the toggle unset, hardcore 1, no marker" "toggle '$(pv global.retroachievements.offlineproxy)', hardcore $(pv global.retroachievements.hardcore), marker $([ -e "${MARK}" ] && echo present || echo absent)"
echo "  5. enable, MainPID the stand-in (the control)"
run own enable; echo "     rc ${RC}; stdout $(tr '\n' '|' < "${OUT}")"
[ "${RC}" -eq 0 ] && [ "$(pv global.retroachievements.offlineproxy)" = 1 ]; t19_check $? "enable succeeds when the socket is the service's" "rc ${RC}, toggle $(pv global.retroachievements.offlineproxy)"
echo "t19-s3-listening: ${FAILS} FAIL"
[ "${FAILS}" -eq 0 ]
