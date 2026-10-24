#!/bin/bash
# run.sh -- tools/fork-package-freshness's control (T10 S8, #946), in a
# throwaway repository under .qa-scratch/ with a known merge base, never the
# fork's repository and never the network (--list only).
#   run.sh [fork-package-freshness] [scratch-parent]
# The fixture: at the merge base, packages a and b. Upstream then deletes b
# and adds g. The fork edits a and adds f and g. The fork's additions since
# the merge base are f and g; a two-tree diff against upstream's tip counts b
# (upstream's deletion) and misses g (upstream added the same path).
set -u
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "${HERE}/../../.." && pwd)"
TOOL="$(readlink -f "${1:-${ROOT}/tools/fork-package-freshness}")"
PARENT="${2:-${ROOT}/.qa-scratch}"; mkdir -p "${PARENT}" || exit 2
S="$(mktemp -d -p "$(cd "${PARENT}" && pwd)" package-freshness.XXXXXX)" || exit 2
trap 'rm -rf "${S}"' EXIT
fail=0
check() { if eval "$2"; then echo "  ok    $1"; else echo "  FAIL  $1"; sed 's/^/          /' "${S}/out" | tail -4; fail=1; fi; }
g() { git -c user.name=t -c user.email=t@t -c commit.gpgsign=false -c core.hooksPath=/dev/null "$@"; }
pkg() { mkdir -p "packages/$1" && printf 'PKG_NAME="%s"\nPKG_VERSION="1.0"\n' "$1" > "packages/$1/package.mk"; }
cd "${S}" && git init -q -b main repo && cd repo || exit 2
mkdir -p tools; cp "${TOOL}" tools/fork-package-freshness; chmod +x tools/fork-package-freshness
pkg a; pkg b; g add packages; g commit -q -m base
g branch upstream-next
g checkout -q upstream-next; g rm -q -r packages/b; pkg g; g add packages; g commit -q -m upstream
g checkout -q main; echo '# a fork edit' >> packages/a/package.mk; pkg f; pkg g; g add packages; g commit -q -m fork
g branch next
g update-ref refs/remotes/upstream/next "$(git rev-parse upstream-next)"
listset() { grep -v 'rclone$' "${S}/out" | sed 's|^packages/||' | LC_ALL=C sort | tr '\n' ' '; }
tools/fork-package-freshness --list > "${S}/out" 2>&1; rc=$?
check "the set is the fork's additions since the merge base: f g (got: $(listset); rc ${rc})" '[ "${rc}" -eq 0 ] && [ "$(listset)" = "f g " ]'
FRESHNESS_BASE=refs/remotes/upstream/no-such-ref tools/fork-package-freshness --list > "${S}/out" 2>&1; rc=$?
check "a base ref it cannot resolve: exit 2, the ref named (rc ${rc})" '[ "${rc}" -eq 2 ] && grep -q "no-such-ref" "${S}/out"'
FRESHNESS_BASE=refs/remotes/upstream/no-such-ref tools/fork-package-freshness > "${S}/out" 2>&1; rc=$?
check "the same without --list: exit 2 before any network read (rc ${rc})" '[ "${rc}" -eq 2 ]'
if [ "${fail}" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
