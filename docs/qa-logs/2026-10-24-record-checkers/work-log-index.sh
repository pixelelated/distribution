#!/bin/bash
# work-log-index.sh -- tools/work-log-index's control (T10 S9, #949): the tool,
# copied into a throwaway root under .qa-scratch/ (its ROOT is its own
# location), over two constructed day files.
#   work-log-index.sh [work-log-index] [scratch-parent]
set -u
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "${HERE}/../../.." && pwd)"
TOOL="$(readlink -f "${1:-${ROOT}/tools/work-log-index}")"
PARENT="${2:-${ROOT}/.qa-scratch}"; mkdir -p "${PARENT}" || exit 2
S="$(mktemp -d -p "$(cd "${PARENT}" && pwd)" work-log-index.XXXXXX)" || exit 2
trap 'rm -rf "${S}"' EXIT
fail=0
check() { if eval "$2"; then echo "  ok    $1"; else echo "  FAIL  $1"; sed 's/^/          /' "${S}/out" | tail -4; fail=1; fi; }
mkdir -p "${S}/r/tools" "${S}/r/docs/work-logs/2026_10-work_logs"; cp "${TOOL}" "${S}/r/tools/work-log-index"
W="${S}/r/docs/work-logs/2026_10-work_logs/2026_10_15-work_log.md"
printf '## 01:00 UTC -- an entry at level two\n\ntext\n\n### 02:00 UTC -- an entry at level three\n\ntext\n\n### a sub-heading inside an entry\n' > "${W}"
python3 -I "${S}/r/tools/work-log-index" --write > "${S}/out" 2>&1; rc=$?
I="${S}/r/docs/work-logs/INDEX.md"
check "--write indexes the level-two entry (rc ${rc})" 'grep -q "01:00 an entry at level two" "${I}"'
check "--write indexes the timestamped level-three entry" 'grep -q "02:00 an entry at level three" "${I}"'
check "an untimed sub-heading is not an entry" '! grep -q "a sub-heading inside an entry" "${I}"'
grep -v "02:00" "${I}" > "${I}.cut" && mv "${I}.cut" "${I}"
python3 -I "${S}/r/tools/work-log-index" --check > "${S}/out" 2>&1; rc=$?
check "--check fails when the level-three entry is missing from INDEX.md (rc ${rc})" '[ "${rc}" -eq 1 ]'
mkdir -p "${S}/r/docs/work-logs/2026_09-work_logs"; printf '## 03:00 UTC -- the same date, filed in another month directory\n' > "${S}/r/docs/work-logs/2026_09-work_logs/2026_10_15-work_log.md"
python3 -I "${S}/r/tools/work-log-index" --check > "${S}/out" 2>&1; rc=$?
check "two day files for one date: an error, exit 2, both named (rc ${rc})" '[ "${rc}" -eq 2 ] && grep -q "2026_09-work_logs" "${S}/out" && grep -q "2026_10-work_logs" "${S}/out"'
if [ "${fail}" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
