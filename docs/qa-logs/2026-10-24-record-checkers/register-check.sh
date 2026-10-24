#!/bin/bash
# register-check.sh -- tools/register-check's control (T10 S9, #947): the
# tool, copied into a throwaway repository under .qa-scratch/ (its ROOT is
# its own location), over a constructed register. Every live document it
# lists exists there as an empty stand-in, so only the cases below speak.
#   register-check.sh [register-check] [scratch-parent]
set -u
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "${HERE}/../../.." && pwd)"
TOOL="$(readlink -f "${1:-${ROOT}/tools/register-check}")"
PARENT="${2:-${ROOT}/.qa-scratch}"; mkdir -p "${PARENT}" || exit 2
S="$(mktemp -d -p "$(cd "${PARENT}" && pwd)" register-check.XXXXXX)" || exit 2
trap 'rm -rf "${S}"' EXIT
fail=0
check() { if eval "$2"; then echo "  ok    $1"; else echo "  FAIL  $1"; sed 's/^/          /' "${S}/out" | tail -6; fail=1; fi; }
g() { git -C "${S}/r" -c user.name=t -c user.email=t@t -c commit.gpgsign=false -c core.hooksPath=/dev/null "$@"; }
git init -q -b main "${S}/r"; cd "${S}/r" || exit 2
mkdir -p tools docs/releases docs/pixelelated docs/reviews docs/upstream .claude/rules .claude/skills \
  projects/ROCKNIX/packages/network/rclone/sources projects/ROCKNIX/packages/network/raofflineproxy/sources \
  projects/ROCKNIX/packages/network/raofflineproxy/patches projects/ROCKNIX/packages/rocknix/sources/scripts \
  projects/ROCKNIX/packages/sysutils/systemd/scripts
for f in CLAUDE.md AGENTS.md NAMING.md docs/blindspot-register.md docs/cloud-sync-changelog.md docs/es-menu-map.md \
         docs/device-testing-policy.md docs/device-flashing-runbook.md docs/conflict-wizard-ia.md docs/releases/device-facts.md \
         docs/pixelelated/rename-plan.md docs/releases/versioning.md docs/reviews/README.md docs/upstream/README.md; do : > "${f}"; done
cp "${TOOL}" tools/register-check; chmod +x tools/register-check
# The copy is in tools/, a listed directory, so the IDs it cites in its own
# header need rows here, or a clean register would read as MISSING them.
TOOLIDS="$(grep -o -E 'D-[A-Z]+-[0-9]+' tools/register-check | sort -u)"
reg() {  # reg <decided rows...> -- a register with the shipped headers
  { printf '# Decision register\n\n## Decided\n\n| ID | Date | Decision | Refs |\n| --- | --- | --- | --- |\n'
    for r in "$@"; do printf '%s\n' "${r}"; done
    for i in ${TOOLIDS}; do printf '| %s | 2026-10-01 | **Cited by the tool under test.** | #1 |\n' "${i}"; done
    printf '\n## Open decisions\n\n| ID | Raised | Question | Home |\n| --- | --- | --- | --- |\n| D-X-9 | 2026-10-01 | **Open:** which way? | #1 |\n'; } > docs/decision-register.md
}
reg '| D-X-1 | 2026-10-01 | **First.** | #1 |' '| D-X-2 | 2026-10-01 | **Second.** | #1 |'
g add -A; g commit -q -m base
tools/register-check > "${S}/out" 2>&1; rc=$?
check "a clean register: exit 0 (rc ${rc})" '[ "${rc}" -eq 0 ]'
echo 'see D-X-2/3 for the pair' > docs/upstream/README.md
tools/register-check > "${S}/out" 2>&1; rc=$?
check "the second ID of a slash shorthand is looked up: D-X-3 MISSING (rc ${rc})" '[ "${rc}" -ne 0 ] && grep -q "MISSING D-X-3" "${S}/out"'
echo 'see D-X-1 and D-X-4' > docs/upstream/README.md
tools/register-check > "${S}/out" 2>&1; rc=$?
check "a citation in docs/upstream/README.md is read: D-X-4 MISSING (rc ${rc})" '[ "${rc}" -ne 0 ] && grep -q "MISSING D-X-4" "${S}/out"'
: > docs/upstream/README.md
reg '| D-X-1 | 2026-10-01 | **First, with an a|b pipe.** | #1 |' '| D-X-2 | 2026-10-01 | **Second.** | #1 |'
tools/register-check > "${S}/out" 2>&1; rc=$?
check "a decided row with an unescaped pipe: SHAPE D-X-1 (rc ${rc})" '[ "${rc}" -ne 0 ] && grep -q "SHAPE D-X-1" "${S}/out"'
reg '| D-X-1 | 2026-10-01 | **First, and since rewritten.** | #1 |' '| D-X-2 | 2026-10-01 | **Second.** | #1 |'
g add -A; g commit -q -m edit
tools/register-check > "${S}/out" 2>&1; rc=$?
check "a decided row edited in place since it was added: reported as EDITED D-X-1, not a failure (rc ${rc})" '[ "${rc}" -eq 0 ] && grep -q "EDITED D-X-1" "${S}/out"'
mkdir -p .claude/skills/x; : > .claude/skills/x/y.md; chmod 000 .claude/skills/x/y.md
tools/register-check > "${S}/out" 2>&1; rc=$?
chmod 644 .claude/skills/x/y.md
check "a file inside a listed directory that cannot be read fails the check (rc ${rc})" '[ "${rc}" -ne 0 ] && grep -q "UNREADABLE" "${S}/out"'
if [ "${fail}" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
