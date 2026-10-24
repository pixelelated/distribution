#!/bin/bash
# P13 (#652, #829, F-18): scripts/get_git's cache check, the functions
# `_clean_repo` and `_repo_exists_and_valid` lifted by name from a commit (or
# the working tree), over a fixture clone whose HEAD is an older commit B than
# its remote branch A, and over the same clone with a tracked file edited.
#   sb-get-git-head.sh <empty scratch dir> [commit|WORKTREE]
SB=${1:?usage: sb-get-git-head.sh <empty scratch dir> [commit|WORKTREE]}; R=${2:-8ebaf8daad}
REPO="$(git rev-parse --show-toplevel)"
mkdir "$SB" || exit 2; cd "$SB" || exit 2
if [ "$R" = WORKTREE ]; then cat "$REPO/scripts/get_git"; else git -C "$REPO" show "$R:scripts/get_git"; fi \
  | sed -n '/^_clean_repo() {/,/^_update_submodules() {/p' | sed '$d' > functions.sh
export GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@invalid
git init -q -b main upstream && echo fixture-1 > upstream/f && git -C upstream add f && git -C upstream commit -q -m B && B=$(git -C upstream rev-parse HEAD)
git -C upstream commit -q --allow-empty -m A && A=$(git -C upstream rev-parse HEAD)
git clone -q upstream cache && git -C cache reset -q --hard "$B"      # the cache as a build left it, pinned at B
PKG_URL="$SB/upstream"
check() {   # $1 = PKG_VERSION; runs the lifted check the way main does, in a subshell
  ( set -e; set -o pipefail; PACKAGE="$SB/cache"; PKG_VERSION="$1"; PKG_GIT_CLONE_BRANCH=""
    . "$SB/functions.sh"; _repo_exists_and_valid && echo accepted || echo refused ) 2>/dev/null | tail -1
}
for v in "$A" "$B" "${B:0:7}"; do
  echo "PKG_VERSION=${v:0:7}$([ ${#v} -lt 40 ] && echo ' (abbreviated)'): the cache is $(check "$v"); HEAD is $(git -C cache rev-parse --short HEAD) (B=${B:0:7}, A=${A:0:7})"
done
echo fixture-2 > cache/f   # a tracked file edited in the cache
r=$(check "$B"); echo "PKG_VERSION=${B:0:7} with a tracked file edited: the cache is $r; the file reads $(cat cache/f)"
