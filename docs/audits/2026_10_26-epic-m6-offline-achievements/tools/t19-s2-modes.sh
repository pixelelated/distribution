#!/usr/bin/env bash
# T19 S2 (#666, #1158; D-RA-049): the proxy's files are private.
#
#   t19-s2-modes.sh <ctl> <unit> <workdir>
#
# Runs the real <ctl> in t19-ctl-sandbox.sh's sandbox against a proxy folder
# seeded the way the unfixed build leaves it (folder 755, files 644, a
# subfolder), with two symlinks inside it pointing outside (a file and a
# folder), the control: neither target may change. The failure case is a
# real one, not a shim: a file bind-mounted read-only over itself, so its
# chmod fails with EROFS. Exit 0 when every check holds (the fixed ctl and
# unit), 1 when one does not (the unfixed), 2 when the run could not be made.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "${HERE}/t19-ctl-sandbox.sh"
[ $# -eq 3 ] || { sed -n '2,13p' "$0"; exit 2; }
CTL="$1"; UNIT="$2"; W="$3"
t19_setup "${CTL}" "${W}" || exit 2
t19_versions
PD="${T19_W}/storage/.config/raofflineproxy"
seed() {
    mkdir -p "${PD}/images" "${T19_W}/storage/elsewhere/dir"
    for f in proxy.sqlite3 last-scan scan.log images/a.png; do printf 'x\n' > "${PD}/${f}"; done
    printf 'x\n' > "${T19_W}/storage/elsewhere/target"
    ln -sfn /storage/elsewhere/target "${PD}/link-out"
    ln -sfn /storage/elsewhere/dir "${PD}/dlink-out"
    chmod 644 "${PD}/proxy.sqlite3" "${PD}/last-scan" "${PD}/scan.log" "${PD}/images/a.png" "${T19_W}/storage/elsewhere/target"
    chmod 755 "${PD}" "${PD}/images" "${T19_W}/storage/elsewhere/dir"
}
modes() { # every path under the folder with its mode, symlinks by lstat
    (cd "${T19_W}/storage" && find .config/raofflineproxy elsewhere -printf '%p %m %y\n' | sort)
}
seed
echo "  seeded: $(modes | tr '\n' ';')"

echo "  1. private-modes on the unfixed build's folder"
t19_ctl private-modes
echo "     rc ${RC}; stderr: $(head -c 300 "${ERR}" | tr '\n' '|')"
[ "${RC}" -eq 0 ]; t19_check $? "private-modes exits 0" "rc ${RC}"
[ "$(stat -c %a "${PD}")" = 700 ]; t19_check $? "the folder is 700" "$(stat -c %a "${PD}")"
bad=""; for f in proxy.sqlite3 last-scan scan.log images/a.png; do [ "$(stat -c %a "${PD}/${f}")" = 600 ] || bad="${bad} ${f}=$(stat -c %a "${PD}/${f}")"; done
[ -z "${bad}" ]; t19_check $? "every regular file under it is 600, the subfolder's included" "${bad}"
[ "$(stat -c %a "${T19_W}/storage/elsewhere/target")" = 644 ] && [ "$(stat -c %a "${T19_W}/storage/elsewhere/dir")" = 755 ]
t19_check $? "the symlinks' targets outside the folder are untouched (the control): file 644, folder 755" "target $(stat -c %a "${T19_W}/storage/elsewhere/target"), dir $(stat -c %a "${T19_W}/storage/elsewhere/dir")"
[ "$(readlink "${PD}/link-out")" = /storage/elsewhere/target ] && [ -e "${PD}/proxy.sqlite3" ] && [ -e "${PD}/images/a.png" ]
t19_check $? "nothing is removed and the symlinks stay as they were" "$(modes | tr '\n' ';')"

echo "  2. a second run"
before="$(modes)"
t19_ctl private-modes
[ "${RC}" -eq 0 ] && [ "$(modes)" = "${before}" ]; t19_check $? "a second run changes nothing and exits 0" "rc ${RC}; $(diff <(echo "${before}") <(modes) | tr '\n' '|')"

echo "  3. a file it cannot chmod (bind-mounted read-only over itself: EROFS)"
printf 'x\n' > "${PD}/locked.db"; chmod 644 "${PD}/locked.db"; printf 'x\n' > "${PD}/other.db"; chmod 644 "${PD}/other.db"
T19_BINDS=(--ro-bind "${PD}/locked.db" /storage/.config/raofflineproxy/locked.db)
t19_ctl private-modes
echo "     rc ${RC}; stderr: $(head -c 300 "${ERR}" | tr '\n' '|')"
[ "${RC}" -ne 0 ] && grep -q 'locked.db' "${ERR}"; t19_check $? "the failure is reported, naming the file, and the exit is non-zero" "rc ${RC}"
[ "$(stat -c %a "${PD}/other.db")" = 600 ]; t19_check $? "and the files it could change are changed" "other.db $(stat -c %a "${PD}/other.db")"
rm -f "${PD}/locked.db" "${PD}/other.db"

echo "  4. enable, from the unfixed build's modes"
chmod 644 "${PD}/proxy.sqlite3" "${PD}/last-scan" "${PD}/scan.log" "${PD}/images/a.png"; chmod 755 "${PD}"
printf 'system.hostname=X\nglobal.retroachievements=1\nglobal.retroachievements.hardcore=0\n' > "${T19_W}/storage/.config/system/configs/system.cfg"
chmod 644 "${T19_W}/storage/.config/system/configs/system.cfg"
t19_ctl enable
echo "     rc ${RC}; stdout: $(tr '\n' '|' < "${OUT}"); stderr: $(head -c 300 "${ERR}" | tr '\n' '|')"
[ "${RC}" -eq 0 ] && grep -q '^systemctl start raofflineproxy.service$' "${T19_W}/run/systemctl.log"; t19_check $? "enable succeeds and starts the service" "rc ${RC}"
[ "$(stat -c %a "${PD}")" = 700 ] && [ "$(stat -c %a "${PD}/proxy.sqlite3")" = 600 ] && [ "$(stat -c %a "${PD}/images/a.png")" = 600 ]
t19_check $? "enable leaves the folder 700 and its files 600" "folder $(stat -c %a "${PD}"), store $(stat -c %a "${PD}/proxy.sqlite3")"
M="${T19_W}/storage/.cache/services/raofflineproxy.conf"
[ -e "${M}" ] && [ "$(stat -c %a "${M}")" = 600 ]; t19_check $? "a file the ctl creates takes umask 077: the marker is 600" "marker $(stat -c %a "${M}" 2>/dev/null || echo absent)"
echo "     observed, not a check: system.cfg after enable's set_setting is $(stat -c %a "${T19_W}/storage/.config/system/configs/system.cfg") (was 644; prepare_settings_temp never relaxes the caller's umask, #421)"

echo "  5. the unit"
n1=$(grep -c '^UMask=0077$' "${UNIT}"); n2=$(grep -c '^ExecStartPre=-/usr/bin/raofflineproxy-ctl private-modes$' "${UNIT}")
[ "${n1}" -eq 1 ]; t19_check $? "the unit carries UMask=0077" "grep -c: ${n1}"
[ "${n2}" -eq 1 ]; t19_check $? "the unit runs private-modes as ExecStartPre (a failure logged, not fatal)" "grep -c: ${n2}"

echo "t19-s2-modes: ${FAILS} FAIL"
[ "${FAILS}" -eq 0 ]
