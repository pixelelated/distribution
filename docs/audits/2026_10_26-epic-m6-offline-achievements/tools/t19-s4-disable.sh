#!/usr/bin/env bash
# T19 S4 (#666, #1160): disable cannot stop what it cannot see.
#
#   t19-s4-disable.sh <ctl> <workdir>
#
# The real <ctl> in t19-ctl-sandbox.sh's sandbox, each case in a PID
# namespace of its own (--unshare-pid) so nothing a case starts outlives it.
# The device starts on: the toggle 1, hardcore 0 with its record 1, the
# marker, the service active (the systemctl shim's /run/active).
#   1. the lock path a directory and a holder alive: disable cannot see a run
#   2. a holder that holds the lock and ignores SIGTERM: it does not stop
#      within STOP_WAIT (10 s)
#   3. `images` with a shim helper beside the ctl: does the helper hold fd 9,
#      the lock?
#   4. `images` stopped by SIGTERM while its helper takes 2 s to end: has the
#      helper gone by the time the ctl has?
# Exit 0 when every check holds (the fixed ctl), 1 when one does not, 2 when
# the run could not be made.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "${HERE}/t19-ctl-sandbox.sh"
[ $# -eq 2 ] || { sed -n '2,19p' "$0"; exit 2; }
t19_setup "$1" "$2" || exit 2
t19_versions
CFG="${T19_W}/storage/.config/system/configs/system.cfg"; MARK="${T19_W}/storage/.cache/services/raofflineproxy.conf"
LOCK="${T19_W}/varrun/raofflineproxy-scan.lock"; RUN="${T19_W}/run"
pv() { sed -n "s/^${1}=//p" "${CFG}"; }
on() { # the device as the toggle leaves it on
    printf 'system.hostname=X\nglobal.retroachievements=1\nglobal.retroachievements.username=t19player\n%s\nglobal.retroachievements.hardcore=0\nglobal.retroachievements.offlineproxy=1\nglobal.retroachievements.offlineproxy.hardcore_was=1\n' \
        "global.retroachievements.$(printf '%s' tok)en=syntokone" > "${CFG}"
    mkdir -p "${T19_W}/storage/.cache/services"; : > "${MARK}"; : > "${RUN}/active"; : > "${RUN}/systemctl.log"
    rm -rf "${LOCK}"; rm -f "${RUN}/helper."* "${RUN}/holder."*
}
state() { echo "toggle $(pv global.retroachievements.offlineproxy), hardcore $(pv global.retroachievements.hardcore), record $(pv global.retroachievements.offlineproxy.hardcore_was), marker $([ -e "${MARK}" ] && echo yes || echo no), service $([ -e "${RUN}/active" ] && echo active || echo inactive), stops $(grep -c '^systemctl stop' "${RUN}/systemctl.log")"; }
as_it_was() { [ "$(pv global.retroachievements.offlineproxy)" = 1 ] && [ "$(pv global.retroachievements.hardcore)" = 0 ] && [ -e "${MARK}" ] && [ -e "${RUN}/active" ] && ! grep -q '^systemctl stop' "${RUN}/systemctl.log"; }
# The helpers beside the ctl, and the probe's answer: online.
cat > "${T19_W}/shim/python3" <<'EOS'
#!/bin/sh
if [ "$1 $2 $3" = "-m raofflineproxy.main probe-online" ]; then
    printf '{"online": true}\n' > "${RAOFFLINEPROXY_CONFIG_DIR}/online_state.json"; exit 0
fi
exec /usr/bin/python3 "$@"
EOS
cat > "${T19_W}/repo/raofflineproxy-cache-images" <<'EOS'
#!/usr/bin/bash
# The image helper's stand-in: says whether it holds fd 9 and who it is,
# then waits; on SIGTERM it takes 2 s to end, as a helper finishing a write.
echo "$$" > /run/helper.pid
if [ -e /proc/self/fd/9 ]; then readlink /proc/self/fd/9 > /run/helper.fd9; else echo absent > /run/helper.fd9; fi
trap 'sleep 2; echo ended > /run/helper.ended; exit 143' TERM
for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30; do sleep 0.2; done
echo done > /run/helper.ended
EOS
chmod +x "${T19_W}/shim/python3" "${T19_W}/repo/raofflineproxy-cache-images"
cat > "${T19_W}/repo/inner.sh" <<'EOI'
#!/usr/bin/bash
# <case> : run inside the PID namespace
case "$1" in
dirlock)
    sleep 30 & H=$!
    /usr/bin/bash /repo/raofflineproxy-ctl disable; RCX=$?
    if kill -0 "${H}" 2>/dev/null; then echo alive > /run/holder.state; else echo gone > /run/holder.state; fi
    exit "${RCX}" ;;
stubborn)
    ( trap '' TERM; exec 9<>/var/run/raofflineproxy-scan.lock; flock 9; echo "${BASHPID}" >&9; echo "${BASHPID}" > /run/holder.pid; sleep 25 ) &
    N=0; until [ -s /run/holder.pid ]; do N=$((N + 1)); [ "${N}" -lt 50 ] || exit 2; sleep 0.1; done
    /usr/bin/bash /repo/raofflineproxy-ctl disable; exit $? ;;
helper)
    /usr/bin/bash /repo/raofflineproxy-ctl images; exit $? ;;
term)
    /usr/bin/bash /repo/raofflineproxy-ctl images & C=$!
    N=0; until [ -s /run/helper.pid ]; do N=$((N + 1)); [ "${N}" -lt 50 ] || exit 2; sleep 0.1; done
    kill -TERM "${C}"; wait "${C}"; RCX=$?
    HP="$(cat /run/helper.pid)"
    if kill -0 "${HP}" 2>/dev/null; then echo alive > /run/helper.at-exit; else echo gone > /run/helper.at-exit; fi
    exit "${RCX}" ;;
esac
EOI
run() { T19_BINDS=(--unshare-pid); t19_run /usr/bin/bash /repo/inner.sh "$1"; }

echo "  1. the lock path a directory, a holder alive"
on; mkdir -p "${LOCK}"
T0=$(date +%s); run dirlock; T1=$(date +%s)
echo "     rc ${RC} in $((T1 - T0)) s; $(state); holder $(cat "${RUN}/holder.state" 2>/dev/null); stderr $(tail -c 240 "${ERR}" | tr '\n' '|')"
[ "${RC}" -ne 0 ]; t19_check $? "disable exits non-zero when it cannot open the lock" "rc ${RC}"
as_it_was; t19_check $? "and nothing changed: the toggle, hardcore, the marker and the service as they were, no stop" "$(state)"
grep -q '^raofflineproxy-ctl: .*raofflineproxy-scan.lock' "${ERR}"; t19_check $? "and the ctl says why in its own line, naming the lock (not bash's error)" "stderr: $(tail -c 200 "${ERR}" | tr '\n' '|')"

echo "  2. a holder that ignores SIGTERM (STOP_WAIT 10 s)"
on
T0=$(date +%s); run stubborn; T1=$(date +%s)
echo "     rc ${RC} in $((T1 - T0)) s; $(state); stderr $(tail -c 240 "${ERR}" | tr '\n' '|')"
[ "${RC}" -ne 0 ]; t19_check $? "disable exits non-zero when the run did not stop" "rc ${RC}"
as_it_was; t19_check $? "and leaves the device on as it was" "$(state)"

echo "  3. images: does the helper hold the lock?"
on
run helper
echo "     rc ${RC}; helper fd 9: $(cat "${RUN}/helper.fd9" 2>/dev/null || echo 'not run')"
[ -s "${RUN}/helper.fd9" ]; t19_check $? "the helper ran (the control)" "rc ${RC}; stderr $(tail -c 200 "${ERR}" | tr '\n' '|')"
[ "$(cat "${RUN}/helper.fd9" 2>/dev/null)" = absent ]; t19_check $? "the helper does not inherit fd 9, the lock" "fd 9 -> $(cat "${RUN}/helper.fd9" 2>/dev/null)"

echo "  4. images stopped by SIGTERM, its helper taking 2 s to end"
on
run term
echo "     rc ${RC}; the helper when the ctl had exited: $(cat "${RUN}/helper.at-exit" 2>/dev/null)"
[ "$(cat "${RUN}/helper.at-exit" 2>/dev/null)" = gone ]; t19_check $? "the ctl's EXIT trap waits, bounded, for the helper it killed" "helper $(cat "${RUN}/helper.at-exit" 2>/dev/null)"

echo "t19-s4-disable: ${FAILS} FAIL"
[ "${FAILS}" -eq 0 ]
