#!/usr/bin/env bash
# T19 S8 (#666, #1164): an unknown count is not a number.
#
#   t19-s8-counts.sh <ctl> <client-linux-dir> <workdir>
#
# The real <ctl> in t19-ctl-sandbox.sh's sandbox, the toggle on and an
# account signed in.
#   1. `ready` with the export (cached_game_ids.txt) a folder
#   2. `ready` with no export and the client's cached-games-count exiting 1
#      after a numeric line (a shim)
#   3. `ready` with a readable export of three ids (the control)
#   4. `account` with the login2 row `[]`
#   5. `account` with the row's Score `true`
#   6. `account` with numbers (the control)
#   7. `scan` with nothing to scan and the export a folder: what the stamp
#      says of ready= (the client on PYTHONPATH as /client)
# Exit 0 when every check holds (the fixed ctl), 1 when one does not, 2 when
# the run could not be made.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "${HERE}/t19-ctl-sandbox.sh"
[ $# -eq 3 ] || { sed -n '2,18p' "$0"; exit 2; }
CL="$(realpath "$2")"; [ -d "${CL}/raofflineproxy" ] || { echo "CANNOT: no client at ${CL}" >&2; exit 2; }
t19_setup "$1" "$3" || exit 2
t19_versions
CFG="${T19_W}/storage/.config/system/configs/system.cfg"; PD="${T19_W}/storage/.config/raofflineproxy"
EXPORT="${PD}/cached_game_ids.txt"; STORE="${PD}/proxy.sqlite3"
printf 'global.retroachievements=1\nglobal.retroachievements.username=t19player\n%s\nglobal.retroachievements.offlineproxy=1\n' "global.retroachievements.$(printf tok)en=syntokone" > "${CFG}"
cat > "${T19_W}/shim/python3" <<'EOS'
#!/bin/sh
case "$1 $2 $3" in
  "-m raofflineproxy.main probe-online") printf '{"online": true}\n' > "${RAOFFLINEPROXY_CONFIG_DIR}/online_state.json"; exit 0 ;;
  "-m raofflineproxy.main cached-games-count") [ -e /run/count-fails ] && { echo "5"; exit 1; } ;;
esac
exec /usr/bin/python3 "$@"
EOS
chmod +x "${T19_W}/shim/python3"
row() { # the login2 row's body
    python3 -I -c '
import sqlite3, sys
db = sqlite3.connect(sys.argv[1])
db.execute("CREATE TABLE IF NOT EXISTS api_cache (id INTEGER PRIMARY KEY AUTOINCREMENT, cacheKey TEXT NOT NULL UNIQUE, responseBody TEXT NOT NULL, sourceRomPath TEXT, cachedAt INTEGER NOT NULL, firstCachedAt INTEGER NOT NULL)")
db.execute("INSERT OR REPLACE INTO api_cache(cacheKey, responseBody, cachedAt, firstCachedAt) VALUES (?, ?, 0, 0)", ("login2::t19player", sys.argv[2]))
db.commit()' "${STORE}" "$1"
}
said() { echo "     rc ${RC}; stdout '$(tr '\n' '|' < "${OUT}")'; stderr $(grep '^raofflineproxy-ctl:' "${ERR}" | tr '\n' '|' | cut -c1-160)"; }

echo "  1. ready, the export a folder"
mkdir -p "${EXPORT}"; t19_ctl ready; said
[ "${RC}" -eq 2 ] && [ ! -s "${OUT}" ]; t19_check $? "cannot tell: exit 2, nothing on stdout" "rc ${RC}, stdout '$(cat "${OUT}")'"
rmdir "${EXPORT}"

echo "  2. ready, no export, the client failing after a numeric line"
: > "${STORE}"; : > "${T19_W}/run/count-fails"; t19_ctl ready; said; rm -f "${T19_W}/run/count-fails" "${STORE}"
[ "${RC}" -eq 2 ] && [ ! -s "${OUT}" ]; t19_check $? "cannot tell: exit 2, nothing on stdout" "rc ${RC}, stdout '$(cat "${OUT}")'"

echo "  3. ready, a readable export of three ids (the control)"
printf '101\n102\n103\n' > "${EXPORT}"; t19_ctl ready; said; rm -f "${EXPORT}"
[ "${RC}" -eq 0 ] && [ "$(cat "${OUT}")" = 3 ]; t19_check $? "3, exit 0" "rc ${RC}"

echo "  4. account, the login2 row []"
row '[]'; t19_ctl account; said
[ "${RC}" -eq 2 ] && [ ! -s "${OUT}" ]; t19_check $? "a row that is not an object is not 'no points': cannot tell" "rc ${RC}"
echo "  5. account, Score true"
row '{"Success":true,"User":"t19player","Score":true,"SoftcoreScore":5}'; t19_ctl account; said
[ "${RC}" -eq 2 ] && [ ! -s "${OUT}" ]; t19_check $? "a boolean is not a score: cannot tell" "rc ${RC}, stdout '$(cat "${OUT}")'"
echo "  6. account, numbers (the control)"
row '{"Success":true,"User":"t19player","Score":10,"SoftcoreScore":5}'; t19_ctl account; said
[ "${RC}" -eq 0 ] && [ "$(cat "${OUT}")" = "score=10 softcore=5" ]; t19_check $? "score=10 softcore=5" "rc ${RC}"
rm -f "${STORE}"

echo "  7. scan with nothing to scan, the export a folder: the stamp's ready="
mkdir -p "${T19_W}/storage/roms" "${EXPORT}"
T19_BINDS=(--ro-bind "${CL}" /client); T19_ENV=(--setenv PYTHONPATH /client); t19_ctl scan
echo "     rc ${RC}; stamp $(cat "${PD}/last-scan" 2>/dev/null || echo none)"
grep -q ' ready=unknown ' "${PD}/last-scan" 2>/dev/null; t19_check $? "the stamp records no count it did not read (ready=unknown)" "$(cat "${PD}/last-scan" 2>/dev/null)"
rmdir "${EXPORT}"

echo "t19-s8-counts: ${FAILS} FAIL"
[ "${FAILS}" -eq 0 ]
