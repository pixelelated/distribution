#!/usr/bin/env bash
# P14 (#652, F-25): get_git's cache check, when the cache directory exists but
# cannot be entered, runs `git clean -fdx` in the caller's directory. Runs the
# two functions from `scripts/get_git` at the read commit against a fixture
# worktree under the scratch directory given; prints what is left. Run as a
# non-root user (root can enter a mode-000 directory).
#   sb-get-git-pushd.sh <scratch-dir> [commit]
set -euo pipefail
S="${1:?scratch directory}"; R="${2:-8ebaf8daad}"
REPO="$(git rev-parse --show-toplevel)"
[ "$(id -u)" != 0 ] || { echo "run as a non-root user" >&2; exit 2; }
W="$S/wt-$(date +%s%N)"; mkdir -p "$W"; cd "$W"
git init -q . && git -c user.email=fixture-1@invalid -c user.name=fixture-1 commit -q --allow-empty -m fixture-1
printf 'build.*\n' > .gitignore
n=1; mkdir -p "build.fixture-$n" sources/pkg; echo "fixture-$n" > "build.fixture-$n/output"
echo fixture-2 > untracked-file
mkdir sources/pkg/pkg-v1 && chmod 000 sources/pkg/pkg-v1
echo "before: $(ls -A | tr '\n' ' ')"
{ echo 'set -e; set -o pipefail'
  echo "PACKAGE=\"$W/sources/pkg/pkg-v1\"; PKG_VERSION=fixture-3; PKG_URL=fixture-4"
  # the two functions by name, so a fix that moves lines is still lifted whole
  git -C "$REPO" show "$R:scripts/get_git" | sed -n '/^_clean_repo() {/,/^_update_submodules() {/p' | sed '$d'
  echo '_repo_exists_and_valid && echo "check: accepted" || echo "check: rejected rc=$?"'
} > "$S/harness-$$.sh"
bash -x "$S/harness-$$.sh" 2>&1 | grep -E '^\+ (pushd|_clean_repo|git clean)|Permission denied|^Removing|^check:' || true
echo "after: $(ls -A | tr '\n' ' ')"
[ -d sources/pkg/pkg-v1 ] && chmod 755 sources/pkg/pkg-v1 || true
