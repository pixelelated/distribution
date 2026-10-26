#!/usr/bin/env bash
# T19 S7 (#666, #1163): a pass skipped, unread or unable to remove is not a
# clean run.
#
#   t19-s7-not-clean.sh <ctl> <cache-images> <client-linux-dir> <workdir>
#
# The real <ctl> and <cache-images> in t19-ctl-sandbox.sh's sandbox, the pin
# with the tree's patches on PYTHONPATH as /client, the toggle on and an
# account signed in, an empty library and no top-up mark, so a `topup`
# reaches the client's recently played pass (run-smart-cache, a shim here).
#   1. the pass exits 0 with no result line
#   2. the pass exits 0 with a result line that does not parse
#   3. less than 60 s left: the pass is not run (a date shim moves the clock
#      on 850 s after the run's start)
#   4. run_image_pass (lifted whole from <ctl>) with no helper at its path
#   5. cache-images --verify, a damaged badge in a read-only folder so its
#      unlink fails (a real EACCES), in a network namespace of its own
# Exit 0 when every check holds (the fixed scripts), 1 when one does not, 2
# when the run could not be made.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "${HERE}/t19-ctl-sandbox.sh"
[ $# -eq 4 ] || { sed -n '2,19p' "$0"; exit 2; }
CI="$(realpath "$2")"; CL="$(realpath "$3")"; [ -d "${CL}/raofflineproxy" ] || { echo "CANNOT: no client at ${CL}" >&2; exit 2; }
t19_setup "$1" "$4" || exit 2
t19_versions
cp "${CI}" "${T19_W}/repo/raofflineproxy-cache-images"; chmod +x "${T19_W}/repo/raofflineproxy-cache-images"
CFG="${T19_W}/storage/.config/system/configs/system.cfg"; PD="${T19_W}/storage/.config/raofflineproxy"; RUN="${T19_W}/run"
STAMP="${PD}/last-scan"; LOG="${PD}/scan.log"
printf 'global.retroachievements=1\nglobal.retroachievements.username=t19player\n%s\nglobal.retroachievements.offlineproxy=1\n' "global.retroachievements.$(printf tok)en=syntokone" > "${CFG}"
mkdir -p "${T19_W}/storage/roms"
cat > "${T19_W}/shim/python3" <<'EOS'
#!/bin/sh
case "$1 $2 $3" in
  "-m raofflineproxy.main probe-online") printf '{"online": true}\n' > "${RAOFFLINEPROXY_CONFIG_DIR}/online_state.json"; exit 0 ;;
  "-m raofflineproxy.main run-smart-cache") echo called >> /run/sc.log; [ -e /run/sc.out ] && cat /run/sc.out; exit 0 ;;
esac
exec /usr/bin/python3 "$@"
EOS
chmod +x "${T19_W}/shim/python3"
topup() {
    rm -f "${STAMP}" "${PD}/last-topup-attempt" "${RUN}/sc.log"; : > "${LOG}"
    T19_BINDS=(--ro-bind "${CL}" /client); T19_ENV=(--setenv PYTHONPATH /client --setenv RAOFFLINEPROXY_HISTORY /storage/history.lpl)
    t19_ctl topup
}
seen() { echo "     rc ${RC}; stamp: $(cat "${STAMP}" 2>/dev/null || echo none); pass called: $(grep -c called "${RUN}/sc.log" 2>/dev/null || echo 0)"; }

echo "  1. the recently played pass exits 0 with no result line"
rm -f "${RUN}/sc.out"; topup; seen
[ "${RC}" -ne 0 ] && grep -q ' 1 topup .*why=' "${STAMP}" 2>/dev/null; t19_check $? "the run is not clean: rc non-zero and a stamp with a why" "rc ${RC}"
echo "  2. a result line that does not parse"
printf '%s\n' '{"type":"result","cached":' > "${RUN}/sc.out"; topup; seen; rm -f "${RUN}/sc.out"
[ "${RC}" -ne 0 ] && grep -q ' 1 topup .*why=' "${STAMP}" 2>/dev/null; t19_check $? "the run is not clean" "rc ${RC}"
echo "  2b. a result line that parses (the control)"
printf '%s\n' '{"type":"result","cached":0,"skipped":0,"limit_reached":false}' > "${RUN}/sc.out"; topup; seen; rm -f "${RUN}/sc.out"
[ "${RC}" -eq 0 ]; t19_check $? "a whole result with nothing cached is a clean run, rc 0" "rc ${RC}"

echo "  3. less than 60 s left for the pass"
cat > "${T19_W}/shim/date" <<'EOS'
#!/bin/sh
# The first `date +%s` is the run's START; every later one is 850 s on.
if [ "$1" = "+%s" ]; then
    n=$(cat /run/date.n 2>/dev/null || echo 0); echo $((n + 1)) > /run/date.n
    t=$(/t19bb/busybox date +%s); [ "${n}" -ge 1 ] && t=$((t + 850)); echo "${t}"; exit 0
fi
exec /t19bb/busybox date "$@"
EOS
chmod +x "${T19_W}/shim/date"; rm -f "${RUN}/date.n"
topup; seen; rm -f "${T19_W}/shim/date" "${RUN}/date.n"
[ "${RC}" -ne 0 ] && grep -q ' 1 topup .*why=TOOK_TOO_LONG' "${STAMP}" 2>/dev/null; t19_check $? "the run is not clean, and the stamp says TOOK_TOO_LONG" "rc ${RC}; $(grep -o 'no time left[^|]*' "${LOG}" | head -1)"

echo "  4. run_image_pass with no image helper"
{
    echo 'SCAN_LOG=/storage/.config/raofflineproxy/scan.log; IMAGE_HELPER=/repo/absent-helper; IMAGE_PASS_SECONDS=300'
    sed -n '/^say() {/,/^}/p; /^slog() {/,/^}/p; /^run_image_pass() {/,/^}/p' "${T19_W}/repo/raofflineproxy-ctl"
    echo 'run_image_pass topup 120; echo "rc $? why=${R_IMAGES_WHY}"'
} > "${T19_W}/repo/rip.sh"
grep -q '^run_image_pass() {' "${T19_W}/repo/rip.sh" || { echo "CANNOT: run_image_pass not found"; exit 2; }
t19_run /usr/bin/bash /repo/rip.sh; echo "     $(cat "${OUT}")"
grep -q '^rc [1-9]' "${OUT}" && grep -q 'why=SOME_IMAGES_NOT_SAVED' "${OUT}"; t19_check $? "a missing helper is a pass not done: non-zero, SOME_IMAGES_NOT_SAVED" "$(cat "${OUT}")"

echo "  5. cache-images --verify: a damaged badge it cannot remove"
SD="${PD}/image_cache/static/Badge"; mkdir -p "${SD}"; printf 'tiny' > "${SD}/7001.png"
T19_BINDS=(--ro-bind "${CL}" /client); T19_ENV=(--setenv PYTHONPATH /client --setenv RAOFFLINEPROXY_CONFIG_DIR /storage/.config/raofflineproxy --setenv RAOFFLINEPROXY_ROCKNIX_SYSTEM_CFG /storage/.config/system/configs/system.cfg)
t19_run /usr/bin/python3 -I -c '
import sys; sys.path.insert(0, "/client")
from raofflineproxy import cache_keys
from raofflineproxy.storage import Storage
s = Storage()
s.upsert_cache(cache_keys.patch(7, "t19player"), "{\"Success\":true,\"PatchData\":{\"Achievements\":[{\"BadgeURL\":\"https://media.retroachievements.org/Badge/7001.png\"}]}}")
s.close()'
[ "${RC}" -eq 0 ] || { echo "CANNOT: the store could not be seeded: $(tail -c 300 "${ERR}")"; exit 2; }
chmod 555 "${SD}"
T19_BINDS=(--unshare-net --ro-bind "${CL}" /client); T19_ENV=(--setenv PYTHONPATH /client --setenv RAOFFLINEPROXY_CONFIG_DIR /storage/.config/raofflineproxy --setenv RAOFFLINEPROXY_ROCKNIX_SYSTEM_CFG /storage/.config/system/configs/system.cfg)
t19_run /usr/bin/python3 -B /repo/raofflineproxy-cache-images --seconds 20 --verify
chmod 755 "${SD}"
echo "     rc ${RC}; stdout $(tr '\n' '|' < "${OUT}" | cut -c1-200); stderr $(grep -o 'could not be removed[^|]*' "${ERR}" | head -1)"
grep -q 'could not be removed' "${ERR}"; t19_check $? "the unlink failed (the control: a real EACCES)" "stderr: $(tail -c 200 "${ERR}" | tr '\n' '|')"
[ "${RC}" -eq 1 ] && grep -qx '>>> why SOME_IMAGES_NOT_SAVED' "${OUT}"; t19_check $? "the damaged image it could not remove counts as not saved: exit 1, SOME_IMAGES_NOT_SAVED" "rc ${RC}"

echo "t19-s7-not-clean: ${FAILS} FAIL"
[ "${FAILS}" -eq 0 ]
