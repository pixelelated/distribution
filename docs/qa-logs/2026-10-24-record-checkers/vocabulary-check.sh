#!/bin/bash
# vocabulary-check.sh -- tools/vocabulary-check's control (T10 S9, #952): the
# tool, copied into a throwaway root under .qa-scratch/ (its ROOT is its own
# location), over constructed product-surface scripts and an empty
# EmulationStation stand-in. Never the real tree or checkout.
#   vocabulary-check.sh [vocabulary-check] [scratch-parent]
set -u
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "${HERE}/../../.." && pwd)"
TOOL="$(readlink -f "${1:-${ROOT}/tools/vocabulary-check}")"
PARENT="${2:-${ROOT}/.qa-scratch}"; mkdir -p "${PARENT}" || exit 2
S="$(mktemp -d -p "$(cd "${PARENT}" && pwd)" vocabulary.XXXXXX)" || exit 2
trap 'chmod -R u+r "${S}" 2>/dev/null; rm -rf "${S}"' EXIT
fail=0
check() { if eval "$2"; then echo "  ok    $1"; else echo "  FAIL  $1"; sed 's/^/          /' "${S}/out" | tail -4; fail=1; fi; }
R="${S}/r"; C="${R}/projects/ROCKNIX/packages/network/rclone/sources"; K="${R}/projects/ROCKNIX/packages/rocknix/sources/scripts"
mkdir -p "${R}/tools" "${C}" "${K}" "${S}/es/es-app/src"; cp "${TOOL}" "${R}/tools/vocabulary-check"
printf '#!/bin/sh\nsay_why "YOUR SAVES ARE BACKED UP"\n' > "${C}/cloud_backup"
printf '#!/bin/sh\nsay_why "BACKUP TO THE CLOUD FAILED"\n' > "${C}/cloud_scan"      # a script the old list never named
printf '#!/bin/sh\necho ">>> why YOUR SETTINGS ARE SAFE"\nnote "back up your settings first"\n' > "${K}/backuptool"
printf '#!/bin/sh\necho "BACKUP YOUR SAVES"\n' > "${K}/a-helper"                 # speaks no protocol: not a surface
run() { python3 -I "${R}/tools/vocabulary-check" --es "${S}/es" "$@" > "${S}/out" 2>&1; }
run; rc=$?
check "a wrong string in a script the old list never named is judged: FAIL cloud_scan (rc ${rc})" '[ "${rc}" -eq 1 ] && grep -q "FAIL .*cloud_scan" "${S}/out"'
check "the scripts read are printed, derived from the two directories" 'grep -q "reads 3 script(s)" "${S}/out" && grep -q "cloud_scan" "${S}/out"'
printf '#!/bin/sh\nsay_why "YOUR SAVES ARE BACKED UP"\n' > "${C}/cloud_scan"
chmod 000 "${C}/cloud_backup"
run; rc=$?
chmod 644 "${C}/cloud_backup"
check "a script that cannot be read: could not run, exit 2 (rc ${rc})" '[ "${rc}" -eq 2 ]'
run; rc=$?
check "clean scripts: exit 0 (rc ${rc})" '[ "${rc}" -eq 0 ]'
if [ "${fail}" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
