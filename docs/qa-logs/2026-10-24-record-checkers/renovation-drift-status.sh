#!/bin/bash
# renovation-drift-status.sh -- tools/renovation-drift and renovation-status's
# control (T10 S9, #957): the three renovation tools copied into a throwaway
# repository under .qa-scratch/ with a constructed ledger (two slices, one
# drifting a little, one a lot) and a stub gh on PATH that answers the slice
# issues. Never the fork's ledger or tracker.
#   renovation-drift-status.sh [tools-dir] [scratch-parent]
set -u
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "${HERE}/../../.." && pwd)"
TOOLS="$(readlink -f "${1:-${ROOT}/tools}")"
PARENT="${2:-${ROOT}/.qa-scratch}"; mkdir -p "${PARENT}" || exit 2
S="$(mktemp -d -p "$(cd "${PARENT}" && pwd)" renovation.XXXXXX)" || exit 2
trap 'rm -rf "${S}"' EXIT
fail=0
check() { if eval "$2"; then echo "  ok    $1"; else echo "  FAIL  $1"; sed 's/^/          /' "${S}/out" | tail -6; fail=1; fi; }
R="${S}/r"; G() { git -C "${R}" "$@"; }
git init -q -b next "${R}"; G config user.name t; G config user.email t@t; G config core.hooksPath /dev/null
mkdir -p "${R}/tools" "${R}/docs/reviews" "${R}/docs/audits" "${R}/a1" "${R}/a2" "${S}/bin"
for t in renovation-inventory renovation-drift renovation-status; do cp "${TOOLS}/${t}" "${R}/tools/${t}"; done
for i in $(seq 1 100); do echo "f ${i}"; done > "${R}/a1/f.txt"
for i in $(seq 1 10); do echo "g ${i}"; done > "${R}/a2/g.txt"
cat > "${R}/docs/reviews/slices.json" <<'JSON'
{"sensitive": {"state": ["a1/**", "!a1/f.txt"]},
 "slices": [{"k": 1, "id": "s1", "area": "a1", "kind": "read", "depth": "Standard", "title": "one"},
            {"k": 2, "id": "s2", "area": "a2", "kind": "read", "depth": "Standard", "title": "two"},
            {"k": 3, "id": "s3", "area": "a3", "kind": "read", "depth": "Standard", "title": "three"},
            {"k": 4, "id": "s4", "area": "a4", "kind": "read", "depth": "Standard", "title": "four"}]}
JSON
python3 -I - "${R}/docs/reviews/inventory.json" <<'PY'
import json, sys
cols = ['tree', 'path', 'area', 'tier', 'tier_note', 'overlap', 'language', 'lines', 'patches', 'last_fork_commit',
        'last_upstream_commit', 'reach', 'reachable_by', 'buildable_by', 'shadowed_by']
row = lambda p, a, n: ['distribution', p, a, 'fork-own', None, False, 'text', n, None, None, None, 'n/a', [], [], None]
json.dump({"header": {"distribution": {"head": "0" * 40}}, "columns": cols,
           "rows": [row('a1/f.txt', 'a1', 100), row('a2/g.txt', 'a2', 10)]}, open(sys.argv[1], "w"))
PY
printf '# Order\n\n## The preliminary review of this order\n\nStatus: **reviewed**\n' > "${R}/docs/reviews/order.md"
G add -A; G commit -q -m base; FIX="$(G rev-parse HEAD)"
sed -i '1s/.*/f one changed/' "${R}/a1/f.txt"
for i in 1 2 3 4 5; do sed -i "${i}s/.*/g changed ${i}/" "${R}/a2/g.txt"; done
G commit -q -a -m drift
cat > "${S}/issues.json" <<JSON
[{"number": 901, "title": "M6.P2 E1/T1: one", "state": "CLOSED", "stateReason": "COMPLETED", "body": "reviewed-at: ${FIX}\nfixed-at: ${FIX}\n"},
 {"number": 902, "title": "M6.P2 E1/T2: two", "state": "CLOSED", "stateReason": "COMPLETED", "body": "reviewed-at: ${FIX}\nfixed-at: ${FIX}\n"},
 {"number": 903, "title": "M6.P2 E1/T3: three", "state": "CLOSED", "stateReason": "NOT_PLANNED", "body": "reviewed-at: ${FIX}\nfixed-at: ${FIX}\n"},
 {"number": 904, "title": "M6.P2 E1/T4: four", "state": "OPEN", "stateReason": null, "body": "reviewed-at: ${FIX}\nfixed-at: ${FIX}\n"}]
JSON
printf '#!/bin/sh\ncase "$*" in "issue list"*) cat "%s/issues.json" ;; *) echo "stub gh: $*" >&2; exit 1 ;; esac\n' "${S}" > "${S}/bin/gh"; chmod +x "${S}/bin/gh"
run() { ( cd "${R}" && PATH="${S}/bin:${PATH}" python3 -I "tools/$1" --distribution "${R}" "${@:2}" ) > "${S}/out" 2>&1; }
run renovation-drift; rc=$?
check "drift reads fixed-at from the slice issue: s1 reported (rc ${rc})" 'grep -q "^| 1 | s1 |" "${S}/out"'
check "a ! exclusion in a sensitive glob is honoured: s1 small, no sensitive file" 'grep -q "^| 1 | s1 | .* | -- | small |" "${S}/out"'
check "s2, every line changed (added and deleted count), re-opens, and drift exits 1 (rc ${rc})" '[ "${rc}" -eq 1 ] && grep -q "^| 2 | s2 | .*100.0 %.* re-open |" "${S}/out"'
check "a slice closed as not planned has no fixed-at for drift" '! grep -q "^| 3 | s3 |" "${S}/out"'
check "nor does an open issue with a fixed-at line" '! grep -q "^| 4 | s4 |" "${S}/out" && grep -q "^| 2 | s2 |" "${S}/out"'
run renovation-status; rc=$?
check "status: s1 closed, its Drift since the share and verdict (rc ${rc})" 'grep -q "^| 1 | a1 | s1 | .* | closed | #901 | .* | 2.0 %, small |" "${S}/out"'
check "status: s2 drifted, 100.0 %, re-open" 'grep -q "^| 2 | a2 | s2 | .* | drifted | #902 | .* | 100.0 %, re-open |" "${S}/out"'
check "status: s3, closed as not planned, is withdrawn, not closed" 'grep -q "^| 3 | a3 | s3 | .* | withdrawn | #903 |" "${S}/out"'
check "status: s4, open with reviewed-at and fixed-at, is fixed, not unreviewed" 'grep -q "^| 4 | a4 | s4 | .* | fixed | #904 |" "${S}/out"'
if [ "${fail}" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
