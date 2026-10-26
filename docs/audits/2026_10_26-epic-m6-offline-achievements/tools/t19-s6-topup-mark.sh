#!/usr/bin/env bash
# T19 S6 (#666, #1162): a top-up mark dated ahead of the clock is no mark.
#
#   t19-s6-topup-mark.sh <ctl> <workdir>
#
# The real <ctl> in t19-ctl-sandbox.sh's sandbox, the toggle on and an
# account signed in, RetroArch's history at RAOFFLINEPROXY_HISTORY. The
# probe answers offline and sleep returns at once, so a run that gets past
# the two gates (the half hour, and "was a game played since the last
# attempt?") is seen as the probe's refusal: exit 69 and its scan.log line.
#   1. the mark a day ahead, the history written now: past the gates?
#   2. the mark two hours back, the history older than it: the played
#      check holds (the control)
#   3. the mark ten minutes back: the half-hour gate holds (the control)
# Exit 0 when every check holds (the fixed ctl), 1 when one does not, 2 when
# the run could not be made.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "${HERE}/t19-ctl-sandbox.sh"
[ $# -eq 2 ] || { sed -n '2,17p' "$0"; exit 2; }
t19_setup "$1" "$2" || exit 2
t19_versions
CFG="${T19_W}/storage/.config/system/configs/system.cfg"; PD="${T19_W}/storage/.config/raofflineproxy"
MARK="${PD}/last-topup-attempt"; HIST="${T19_W}/storage/history.lpl"; LOG="${PD}/scan.log"
printf 'global.retroachievements=1\nglobal.retroachievements.username=t19player\n%s\nglobal.retroachievements.offlineproxy=1\n' "global.retroachievements.$(printf tok)en=syntokone" > "${CFG}"
cat > "${T19_W}/shim/python3" <<'EOS'
#!/bin/sh
if [ "$1 $2 $3" = "-m raofflineproxy.main probe-online" ]; then printf '{"online": false}\n' > "${RAOFFLINEPROXY_CONFIG_DIR}/online_state.json"; exit 0; fi
exec /usr/bin/python3 "$@"
EOS
printf '#!/bin/sh\nexit 0\n' > "${T19_W}/shim/sleep"
chmod +x "${T19_W}/shim/python3" "${T19_W}/shim/sleep"
topup() { : > "${LOG}"; T19_ENV=(--setenv RAOFFLINEPROXY_HISTORY /storage/history.lpl); t19_ctl topup; }
when() { date -u -d "@$(stat -c %Y "$1")" +%FT%TZ; }

echo "  1. the mark a day ahead of the clock, a game played now"
touch "${HIST}"; touch -d '+1 day' "${MARK}"
echo "     mark $(when "${MARK}"), history $(when "${HIST}"), now $(date -u +%FT%TZ)"
topup
echo "     rc ${RC}; scan.log: $(tr '\n' '|' < "${LOG}" | cut -c1-240); mark now: $([ -e "${MARK}" ] && when "${MARK}" || echo absent)"
[ "${RC}" -eq 69 ] && grep -q 'topup refused: offline by the proxy' "${LOG}"; t19_check $? "the run goes past the gates to the probe (here offline: exit 69)" "rc ${RC}"
! grep -q 'no game played since the last attempt' "${LOG}"; t19_check $? "it is not skipped as 'no game played'" "$(grep -o 'no game played[^|]*' "${LOG}" | head -1)"
grep -q 'dated ahead of the clock' "${LOG}" "${T19_W}/run/say.log" 2>/dev/null; t19_check $? "and the mark dated ahead is said" "scan.log: $(tr '\n' '|' < "${LOG}" | cut -c1-160)"

echo "  2. the mark two hours back, the history older than it (the control)"
touch -d '3 hours ago' "${HIST}"; touch -d '2 hours ago' "${MARK}"
topup
echo "     rc ${RC}; scan.log: $(tr '\n' '|' < "${LOG}" | cut -c1-200)"
[ "${RC}" -eq 0 ] && grep -q 'no game played since the last attempt' "${LOG}"; t19_check $? "no game played since the mark: skipped, rc 0" "rc ${RC}"

echo "  3. the mark ten minutes back (the control)"
touch "${HIST}"; touch -d '10 minutes ago' "${MARK}"
topup
echo "     rc ${RC}; scan.log: $(tr '\n' '|' < "${LOG}" | cut -c1-200)"
[ "${RC}" -eq 0 ] && [ ! -s "${LOG}" ]; t19_check $? "the half-hour gate holds: rc 0 before the probe, nothing logged" "rc ${RC}"

echo "t19-s6-topup-mark: ${FAILS} FAIL"
[ "${FAILS}" -eq 0 ]
