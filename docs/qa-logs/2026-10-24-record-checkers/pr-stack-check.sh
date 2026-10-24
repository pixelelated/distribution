#!/bin/bash
# pr-stack-check.sh -- tools/pr-stack-check's control (T10 S9, #955): the
# tool, copied into a throwaway root under .qa-scratch/ beside a stand-in
# pre-push (PERSONAL_PATTERNS) and a stub fork-worktree, run with --repo on a
# throwaway repository whose next renames a file, with a two-line map. A git
# shim on PATH logs every git call, so a forced worktree removal is seen.
# Never the fork's repository, its map or its worktrees.
#   pr-stack-check.sh [pr-stack-check] [scratch-parent]
set -u
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "${HERE}/../../.." && pwd)"
TOOL="$(readlink -f "${1:-${ROOT}/tools/pr-stack-check}")"
PARENT="${2:-${ROOT}/.qa-scratch}"; mkdir -p "${PARENT}" || exit 2
S="$(mktemp -d -p "$(cd "${PARENT}" && pwd)" pr-stack.XXXXXX)" || exit 2
REALGIT="$(command -v git)"
trap 'cd /; "${REALGIT}" -C "${S}/repo" worktree prune 2>/dev/null; rm -rf "${S}"' EXIT
fail=0
check() { if eval "$2"; then echo "  ok    $1"; else echo "  FAIL  $1"; sed 's/^/          /' "${S}/out" | tail -5; fail=1; fi; }
mkdir -p "${S}/r/tools" "${S}/r/.githooks" "${S}/r/docs/pr-series" "${S}/drafts" "${S}/bin"
cp "${TOOL}" "${S}/r/tools/pr-stack-check"
printf 'PERSONAL_PATTERNS=(\n  %s\n)\n' "'.claude/'" "'docs/'" "'plans/'" "'.githooks/'" "'research/'" "'seed/'" > "${S}/r/.githooks/pre-push"
printf '#!/bin/sh\necho "fork-worktree $*" >> "%s/calls"\nexit 1\n' "${S}" > "${S}/r/tools/fork-worktree"; chmod +x "${S}/r/tools/fork-worktree"
printf '#!/bin/sh\necho "git $*" >> "%s/calls"\nexec "%s" "$@"\n' "${S}" "${REALGIT}" > "${S}/bin/git"; chmod +x "${S}/bin/git"
G() { "${REALGIT}" -C "${S}/repo" "$@"; }
"${REALGIT}" init -q -b main "${S}/repo"
G config user.name t; G config user.email t@t; G config core.hooksPath /dev/null
for i in $(seq 1 30); do printf 'line %s of a file long enough for rename detection\n' "$i"; done > "${S}/repo/old.txt"
printf 'a\n' > "${S}/repo/a.txt"; G add -A; G commit -q -m base
G switch -q -c next; G mv old.txt new.txt; printf 'a changed\n' > "${S}/repo/a.txt"; G commit -q -a -m next
printf '## pkg: change a and move the file\na.txt\nnew.txt\n' > "${S}/map-rename"
printf '## pkg: change a and move the file\na.txt\nnew.txt\nold.txt\n' > "${S}/map-both"
printf 'Title: pkg: change a and move the file\n\nThis changes a and moves the file.\n' > "${S}/drafts/01-move.md"
run() { : > "${S}/calls"; ( cd "${S}" && PATH="${S}/bin:${PATH}" bash "${S}/r/tools/pr-stack-check" --repo "${S}/repo" --base main --from next --roots . --drafts "${S}/drafts" --map "$1" ) > "${S}/out" 2>&1; }
run "${S}/map-rename"; rc=$?
check "a map naming only a renamed file's new path fails: the old path stays upstream, by check 3 and by the built union (rc ${rc})" '[ "${rc}" -eq 1 ] && grep -q "no PR carries old.txt" "${S}/out" && grep -q "every PR together still differs from next: old.txt" "${S}/out"'
check "the EXIT trap removes its worktree without --force" '! grep -q "worktree remove --force" "${S}/calls"'
run "${S}/map-both"; rc=$?
check "the same map naming the old path too passes (rc ${rc})" '[ "${rc}" -eq 0 ] && grep -q "PASS" "${S}/out"'
check "the pass names the union compared with next" 'grep -q -i "every PR on main together equals next" "${S}/out"'
G branch -q pr-stack/1 main
run "${S}/map-both"; rc=$?
check "an existing pr-stack/1 branch is refused, not deleted (rc ${rc})" '[ "${rc}" -eq 2 ] && G rev-parse -q --verify pr-stack/1 >/dev/null'
if [ "${fail}" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
