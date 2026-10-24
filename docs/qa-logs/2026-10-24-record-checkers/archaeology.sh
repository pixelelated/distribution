#!/bin/bash
# archaeology.sh -- tools/archaeology's control (T10 S9, #950): the tool,
# copied into a throwaway repository under .qa-scratch/ (its ROOT is its own
# location), over a constructed blindspot register; --no-gh, so no tracker.
#   archaeology.sh [archaeology] [scratch-parent]
set -u
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "${HERE}/../../.." && pwd)"
TOOL="$(readlink -f "${1:-${ROOT}/tools/archaeology}")"
PARENT="${2:-${ROOT}/.qa-scratch}"; mkdir -p "${PARENT}" || exit 2
S="$(mktemp -d -p "$(cd "${PARENT}" && pwd)" archaeology.XXXXXX)" || exit 2
trap 'rm -rf "${S}"' EXIT
fail=0
check() { if eval "$2"; then echo "  ok    $1"; else echo "  FAIL  $1"; sed 's/^/          /' "${S}/out" | tail -4; fail=1; fi; }
git init -q -b main "${S}/r"; cd "${S}/r" || exit 2
mkdir -p tools docs .claude/rules "${S}/es"; cp "${TOOL}" tools/archaeology
export ES_SRC="${S}/es"   # an empty stand-in, so --reversal never reads a real checkout
echo 'the -x-starts-with-a-dash words' > docs/note.md
printf '# Blindspots\n\n| # | Blindspot | Seen |\n| --- | --- | --- |\n| 7 | **Archiving a tree that holds symlinks** -- busybox unzip refuses one | 2026-08-20 |\n\n## 29. A heading entry (2026-09-20)\n\nbody text\n' > docs/blindspot-register.md
git -c user.name=t -c user.email=t@t -c core.hooksPath=/dev/null add -A; git -c user.name=t -c user.email=t@t -c core.hooksPath=/dev/null commit -q -m base
run() { python3 -I tools/archaeology --no-gh "$@" > "${S}/out" 2>&1; }
run "busybox unzip"; rc=$?
check "a term only blindspot row 7 carries is found (rc ${rc})" '[ "${rc}" -eq 0 ] && grep -q "Archiving a tree that holds symlinks" "${S}/out"'
run "A heading entry"; rc=$?
check "a heading entry is still found (rc ${rc})" '[ "${rc}" -eq 0 ] && grep -q "29. A heading entry" "${S}/out"'
run "nothing-matches-this-term"; rc=$?
check "a successful search that finds nothing exits 0 (rc ${rc})" '[ "${rc}" -eq 0 ]'
run '(?:x)'; rc=$?
check "a term git log -G cannot compile: an error, exit 2, not zero hits (rc ${rc})" '[ "${rc}" -eq 2 ] && grep -q -i "git log failed" "${S}/out"'
python3 -I tools/archaeology --reversal '(' > "${S}/out" 2>&1; rc=$?
check "--reversal with a pattern grep cannot compile: exit 2 (rc ${rc})" '[ "${rc}" -eq 2 ]'
python3 -I tools/archaeology --reversal '-x-starts-with-a-dash' > "${S}/out" 2>&1; rc=$?
check "--reversal with a pattern that starts with a dash is searched, not taken for an option (rc ${rc})" '[ "${rc}" -eq 0 ] && grep -q "^1 line(s) carry the old words" "${S}/out"'
if [ "${fail}" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
