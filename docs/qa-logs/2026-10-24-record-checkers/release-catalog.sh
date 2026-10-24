#!/bin/bash
# release-catalog.sh -- tools/release-catalog's control (T10 S9, #954): the
# tool, copied into a throwaway root under .qa-scratch/ (the page it writes is
# under its own root), over a constructed ARTIFACTS directory. Never the real
# artifacts or the real catalog.
#   release-catalog.sh [release-catalog] [scratch-parent]
set -u
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "${HERE}/../../.." && pwd)"
TOOL="$(readlink -f "${1:-${ROOT}/tools/release-catalog}")"
PARENT="${2:-${ROOT}/.qa-scratch}"; mkdir -p "${PARENT}" || exit 2
S="$(mktemp -d -p "$(cd "${PARENT}" && pwd)" release-catalog.XXXXXX)" || exit 2
trap 'rm -rf "${S}"' EXIT
fail=0
check() { if eval "$2"; then echo "  ok    $1"; else echo "  FAIL  $1"; sed 's/^/          /' "${S}/out" | tail -4; fail=1; fi; }
mkdir -p "${S}/r/tools" "${S}/a/h700-rc-one" "${S}/a/h700-unrecorded" "${S}/empty"; cp "${TOOL}" "${S}/r/tools/release-catalog"
printf 'H700 rc cut, constructed\nBUILD_ID 0123456789abcdef (one space after the key)\nBuilt     2026-10-24\nDelta     a constructed delta\n' > "${S}/a/h700-rc-one/RECORD.txt"
mkdir -p "${S}/a/h700-rc-keyfirst"; printf 'BUILD_ID fedcba9876543210 (the record opens with its key, no title)\nBuilt     2026-10-23\n' > "${S}/a/h700-rc-keyfirst/RECORD.txt"
run() { ARTIFACTS="$1" python3 -I "${S}/r/tools/release-catalog" "${@:2}" > "${S}/out" 2>&1; }
run "${S}/a" --write; rc=$?
P="${S}/r/docs/releases/catalog.md"
check "a BUILD_ID with one space after the key is read (rc ${rc})" '[ "${rc}" -eq 0 ] && grep -q "\`0123456789abcdef\`" "${P}"'
check "a record whose first line is BUILD_ID, with no title line, keeps its BUILD_ID" 'grep -q "\`fedcba9876543210\`" "${P}"'
check "a kept folder with no RECORD.txt is reported" 'grep -q "1 folder(s) without a RECORD.txt" "${S}/out"'
run "${S}/a" --unrecorded; rc=$?
check "--unrecorded names it (rc ${rc})" 'grep -q "h700-unrecorded" "${S}/out"'
run "${S}/empty" --write; rc=$?
check "an artifacts directory with no records: --write exits non-zero (rc ${rc})" '[ "${rc}" -ne 0 ]'
run "${S}/missing" --check; rc=$?
check "an artifacts directory that is not there: --check exits non-zero (rc ${rc})" '[ "${rc}" -ne 0 ]'
if [ "${fail}" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
