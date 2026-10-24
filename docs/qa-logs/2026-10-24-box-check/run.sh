#!/bin/bash
# run.sh -- tools/box-check's control (T10 S5, #941): the tool against the gh
# double, never against GitHub.
#   run.sh [box-check] [scratch-parent]
# The population is 458 open issues (the fork's count at 2026-10-24 16:29Z)
# with one failing checkbox at position 350, past the old --limit 300.
# Each case prints ok or FAIL; the run ends PASS (exit 0) or FAIL (1).
set -u
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "${HERE}/../../.." && pwd)"
TOOL="$(readlink -f "${1:-${ROOT}/tools/box-check}")"
PARENT="${2:-${ROOT}/.qa-scratch}"; mkdir -p "${PARENT}" || exit 2
S="$(mktemp -d -p "$(cd "${PARENT}" && pwd)" box-check-control.XXXXXX)" || exit 2
trap 'rm -rf "${S}"' EXIT
mkdir -p "${S}/bin" && cp "${HERE}/gh-double" "${S}/bin/gh" && chmod +x "${S}/bin/gh"
python3 -I - "${S}/issues.json" <<'PY'
import json, sys
items = [{"number": 1000 - i, "title": "issue %d" % i, "state": "OPEN",
          "body": "- [ ] the guest prints PASS for case %d" % i} for i in range(458)]
items[350]["body"] = "- [ ] the maintainer's word that it works"
json.dump(items, open(sys.argv[1], "w"))
PY
fail=0
check() { if eval "$2"; then echo "  ok    $1"; else echo "  FAIL  $1"; sed 's/^/          /' "${S}/out" | tail -3; fail=1; fi; }
bc() { PATH="${S}/bin:${PATH}" GH_DOUBLE_ISSUES="${S}/issues.json" "$@" "${TOOL}" --quiet > "${S}/out" 2>&1; }

bc env; rc=$?
check "458 open issues, a failing checkbox at 350: box-check fails (rc ${rc})" '[ "${rc}" -eq 1 ] && grep -q "FAIL  #650" "${S}/out"'
check "its count says 458" 'grep -q "box-check: 458 issue(s)" "${S}/out"'
bc env GH_DOUBLE_TOTAL=473; rc=$?
check "the tracker says 473 and the read returns 458: refused as a short read (rc ${rc})" '[ "${rc}" -eq 2 ] && grep -q "read 458 of 473" "${S}/out"'
bc env GH_DOUBLE_FAIL=1; rc=$?
check "the tracker does not answer: could not run, exit 2 (rc ${rc})" '[ "${rc}" -eq 2 ]'

if [ "${fail}" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
