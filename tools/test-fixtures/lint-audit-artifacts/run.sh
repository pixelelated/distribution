#!/bin/bash
# run.sh -- tools/lint-audit-artifacts' fixtures, run together (T10 S7, #945):
# the renovation face's pass and fail fixtures (P1, #641), the index-boundary
# fixture, and two copies of the pass fixture made at run time under a dated
# epic name, one with underscores and one with hyphens, neither carrying a
# review plan (a dated epic folder from 2026-10-02 must).
#   run.sh [lint-audit-artifacts] [scratch-parent]
set -u
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "${HERE}/../../.." && pwd)"
LINT="$(readlink -f "${1:-${ROOT}/tools/lint-audit-artifacts}")"
PARENT="${2:-${ROOT}/.qa-scratch}"; mkdir -p "${PARENT}" || exit 2
S="$(mktemp -d -p "$(cd "${PARENT}" && pwd)" lint-fixtures.XXXXXX)" || exit 2
trap 'rm -rf "${S}"' EXIT
fail=0
check() { if eval "$2"; then echo "  ok    $1"; else echo "  FAIL  $1"; tail -3 "${S}/out" | sed 's/^/          /'; fail=1; fi; }
lint() { python3 -I "${LINT}" "$@" > "${S}/out" 2>&1; }
lint "${HERE}/fixture-epic-m6-renovation-pass"; rc=$?
check "the renovation face's pass fixture: PASS (rc ${rc})" '[ "${rc}" -eq 0 ] && tail -1 "${S}/out" | grep -qx PASS'
lint "${HERE}/fixture-epic-m6-renovation-fail"; rc=$?
check "the renovation face's fail fixture: a named FAIL (rc ${rc})" '[ "${rc}" -eq 1 ] && grep -q "CONTRACT FAILURE" "${S}/out"'
lint "${HERE}/fixture-epic-m6-index-boundary"; rc=$?
check "a cell quoting the Verification heading does not end the index: G2-I-01's missing entry is named (rc ${rc})" '[ "${rc}" -eq 1 ] && grep -q "no entry for G2-I-01 (gpt)" "${S}/out"'
for name in 2026_10_24-epic-m6-datecase 2026-10-24-epic-m6-datecase; do
  cp -r "${HERE}/fixture-epic-m6-renovation-pass" "${S}/${name}"
  lint "${S}/${name}"; rc=$?
  check "a dated epic folder ${name} without a review plan: refused like the other form (rc ${rc})" '[ "${rc}" -eq 1 ] && grep -q "review-plan.json" "${S}/out"'
done
if [ "${fail}" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
