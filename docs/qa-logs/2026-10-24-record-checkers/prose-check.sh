#!/bin/bash
# prose-check.sh -- tools/prose-check's control (T10 S9, #953): constructed
# drafts in a throwaway directory under .qa-scratch/, and the tool's own
# --self-test with the tool copied into a root that has no /workspace/tmp
# samples beside it. Never a real page.
#   prose-check.sh [prose-check] [scratch-parent]
set -u
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "${HERE}/../../.." && pwd)"
TOOL="$(readlink -f "${1:-${ROOT}/tools/prose-check}")"
PARENT="${2:-${ROOT}/.qa-scratch}"; mkdir -p "${PARENT}" || exit 2
S="$(mktemp -d -p "$(cd "${PARENT}" && pwd)" prose.XXXXXX)" || exit 2
trap 'rm -rf "${S}"' EXIT
fail=0
check() { if eval "$2"; then echo "  ok    $1"; else echo "  FAIL  $1"; sed 's/^/          /' "${S}/out" | tail -4; fail=1; fi; }
printf '# Page\n\nOpen the menu and choose a folder.\n\nThat'"'"'s it!\n' > "${S}/ends.md"
printf '# Page\n\nOpen the menu. Overall, the folder is chosen once.\n' > "${S}/overall.md"
printf '# Page\n\nSaves go to the folder. Saves come back on restore.\n' > "${S}/opener.md"
python3 -I "${TOOL}" "${S}/ends.md" > "${S}/out" 2>&1; rc=$?
check "a draft ending That's it! at the line's end fails (rc ${rc})" '[ "${rc}" -eq 1 ] && grep -q "sign-off" "${S}/out"'
python3 -I "${TOOL}" "${S}/overall.md" > "${S}/out" 2>&1; rc=$?
check "Overall, followed by a space fails (rc ${rc})" '[ "${rc}" -eq 1 ] && grep -q "sign-off" "${S}/out"'
python3 -I "${TOOL}" "${S}/opener.md" > "${S}/out" 2>&1; rc=$?
check "two consecutive sentences opening with the same word are reported, a warning (rc ${rc})" '[ "${rc}" -eq 0 ] && grep -q "warn: two consecutive sentences" "${S}/out"'
mkdir -p "${S}/r/tools"; cp "${TOOL}" "${S}/r/tools/prose-check"
[ -d "${ROOT}/tools/test-fixtures/prose" ] && mkdir -p "${S}/r/tools/test-fixtures" && cp -r "${ROOT}/tools/test-fixtures/prose" "${S}/r/tools/test-fixtures/prose"
( cd "${S}" && env -u PROSE_SAMPLES python3 -I "${S}/r/tools/prose-check" --self-test ) > "${S}/out" 2>&1; rc=$?
check "--self-test reads its samples from the tree, and passes (rc ${rc})" '[ "${rc}" -eq 0 ] && grep -q "samples from tools/test-fixtures/prose" "${S}/out" && ! grep -q "/workspace/tmp" "${S}/out" && grep -q "self-test: PASS" "${S}/out"'
check "--self-test carries the two new cases" 'grep -q "That.s it" "${S}/out" && grep -q "same word" "${S}/out"'
if [ "${fail}" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
