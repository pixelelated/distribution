#!/bin/bash
# run.sh -- tools/forbidden-terms-check's control (T10 S6, #942, #936): the
# tool against throwaway trees under .qa-scratch/ with a stand-in list
# (FORBIDDEN_PATTERNS in the environment, as the CI passes the real one),
# never the real list and never the fork's tree.
#   run.sh [forbidden-terms-check] [scratch-parent]
# Each case prints ok or FAIL; the run ends PASS (exit 0) or FAIL (1).
set -u
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "${HERE}/../../.." && pwd)"
TOOL="$(readlink -f "${1:-${ROOT}/tools/forbidden-terms-check}")"
PARENT="${2:-${ROOT}/.qa-scratch}"; mkdir -p "${PARENT}" || exit 2
S="$(mktemp -d -p "$(cd "${PARENT}" && pwd)" forbidden-terms-control.XXXXXX)" || exit 2
trap 'rm -rf "${S}"' EXIT
export FORBIDDEN_PATTERNS='zebrafish[ -]quartet|qzx-estate'
unset FORBIDDEN_TERMS_FILE
WORD="$(printf 'zebra%s-quartet' fish)"
fail=0
check() { if eval "$2"; then echo "  ok    $1"; else echo "  FAIL  $1"; sed 's/^/          /' "${S}/out" | tail -3; fail=1; fi; }
g() { git -c user.name=t -c user.email=t@t -c commit.gpgsign=false -c core.hooksPath=/dev/null "$@"; }
tree() { rm -rf "${S}/$1"; git init -q -b main "${S}/$1"; }
ftc() { "${TOOL}" "$@" > "${S}/out" 2>&1; }

tree clean; echo plain > "${S}/clean/a.txt"; ln -s a.txt "${S}/clean/link"; g -C "${S}/clean" add -A; g -C "${S}/clean" commit -q -m c
ftc "${S}/clean"; rc=$?
check "a clean tree with a symlink: 0 hits, exit 0 (rc ${rc})" '[ "${rc}" -eq 0 ] && grep -q "0 hits in 2 tracked files" "${S}/out"'

tree link; echo plain > "${S}/link/a.txt"; ln -s "notes-on-the-${WORD}" "${S}/link/dangling"; g -C "${S}/link" add -A; g -C "${S}/link" commit -q -m l
ftc "${S}/link"; rc=$?
check "a symlink whose link text carries a listed word: a hit, exit 1 (rc ${rc})" '[ "${rc}" -eq 1 ]'
check "the hit is named by place, never by word" '! grep -q -i zebrafish "${S}/out"'

tree name; echo plain > "${S}/name/notes ${WORD}.txt"; g -C "${S}/name" add -A; g -C "${S}/name" commit -q -m n
ftc "${S}/name"; rc=$?
check "a clean file whose name carries a listed word: a hit, exit 1 (rc ${rc})" '[ "${rc}" -eq 1 ]'
check "the name is never printed" '! grep -q -i zebrafish "${S}/out"'

tree empty; echo plain > "${S}/empty/a.txt"; echo more > "${S}/empty/b.txt"; g -C "${S}/empty" add -A; g -C "${S}/empty" commit -q -m e; rm "${S}/empty/a.txt" "${S}/empty/b.txt"
ftc "${S}/empty"; rc=$?
check "a checkout whose tracked files are absent: could not run, exit 2 (rc ${rc})" '[ "${rc}" -eq 2 ]'

tree none; g -C "${S}/none" commit -q --allow-empty -m none
ftc "${S}/none"; rc=$?
check "a tree with no tracked files: could not run, exit 2 (rc ${rc})" '[ "${rc}" -eq 2 ]'

printf 'line one\nthe qzx-estate notes\n' | "${TOOL}" --stdin > "${S}/out" 2>&1; rc=$?
check "--stdin, unchanged: a listed word is a hit (rc ${rc})" '[ "${rc}" -eq 1 ] && ! grep -q -i qzx "${S}/out"'

if [ "${fail}" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
