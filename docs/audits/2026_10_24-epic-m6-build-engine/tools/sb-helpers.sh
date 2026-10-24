#!/usr/bin/env bash
# E8 (#652, PL-21, PL-22, PL-23): upstream's helpers, each site run from a
# commit (or the working tree) over fixtures in the scratch directory given.
# config/functions is sourced with NOONEXIT=yes (no trap); scripts that would
# act on a real tree (makefile_helper, multithread, get_git) have their block
# lifted by marker or run against fixture paths only.
#   sb-helpers.sh <scratch-dir> [commit|WORKTREE]
set -u
S="${1:?scratch directory}"; R="${2:-8ebaf8daad}"
REPO="$(git rev-parse --show-toplevel)"
W="$S/run-$(date +%s%N)"; mkdir -p "$W"
src() { if [ "$R" = WORKTREE ]; then cat "$REPO/$1"; else git -C "$REPO" show "$R:$1"; fi; }
src config/functions > "$W/functions"; src config/build-identity > "$W/build-identity"
src config/multithread > "$W/multithread"; src scripts/makefile_helper > "$W/makefile_helper"; src scripts/get_git > "$W/get_git"
F() { env -i PATH=/usr/bin:/bin HOME="$W" NOONEXIT=yes W="$W" bash -c ". \"$W/functions\"; die() { echo \"die: \$*\"; exit 1; }; $1" 2>&1 | tail -3; }

echo "## exec_thread_safe with PKG_NAME empty: the lock's name"
F 'acquire_exclusive_lock() { echo "lock name: [$1]"; }; release_exclusive_lock() { :; }; PKG_NAME=""; exec_thread_safe true' | head -1

echo "## add_group bar when the group file has foobar"
mkdir -p "$W/inst/etc"; echo 'foobar:x:1:' > "$W/inst/etc/group"
F "INSTALL=\"$W/inst\"; add_group bar 2; grep -c '^bar:' \"$W/inst/etc/group\" | sed 's/^/bar lines: /'"

echo "## get_module_dir with two module directories"
mkdir -p "$W/linux/usr/lib/kernel-overlays/base/lib/modules/6.1.0-fixture" "$W/linux/usr/lib/kernel-overlays/base/lib/modules/6.1.0-fixture-old"
F "get_install_dir() { echo \"$W/linux\"; }; d=\$(get_module_dir); echo \"rc \$? name [\$d]\""

echo "## find_path -f with a wildcard that matches only a directory"
mkdir -p "$W/proj/ROCKNIX/devices/H700/config/fixture.d" "$W/proj/ROCKNIX/config"; echo fixture-1 > "$W/proj/ROCKNIX/config/fixture.dat"
F "PROJECT_DIR=\"$W/proj\" PROJECT=ROCKNIX DEVICE=H700 PKG_NAME=fixturepkg PKG_DIR=\"$W/none\" DISTRO_DIR=\"$W/none\" DISTRO=none; find_path -f 'config/fixture.d*' && echo \"FOUND_PATH \${FOUND_PATH#$W/}\" || echo 'no match'"

echo "## build identity when git status fails"
mkdir -p "$W/gitbin"; printf '#!/bin/sh\ncase "$1" in rev-parse) echo 0123456789abcdef0123456789abcdef01234567 ;; status) exit 128 ;; esac\n' > "$W/gitbin/git"; chmod +x "$W/gitbin/git"
env -i PATH="$W/gitbin:/usr/bin:/bin" OS_VERSION=0.0.1 BUILD_TIMESTAMP=20261024T000000Z bash -c ". \"$W/build-identity\"; pixelelated_build_identity; echo \"rc \$? BUILD_DIRTY=\${BUILD_DIRTY:-unset}\"" 2>&1 | tail -2

echo "## multithread: the statistics fail after a finished build, under set -e"
awk '/--max-procs \$\{THREADCOUNT\} \$\{buildopts\} \|\| result=1/{on=1; next} /rm -f "\$\{THREAD_CONTROL\}\/parallel.pid"/{exit} on' "$W/multithread" > "$W/stats.sh"
mkdir -p "$W/tc" "$W/root/tools"; echo fixture-2 > "$W/tc/history"; printf '#!/bin/sh\nexit 3\n' > "$W/root/tools/mtstats.py"; chmod +x "$W/root/tools/mtstats.py"
env -i PATH=/usr/bin:/bin THREAD_CONTROL="$W/tc" ROOT="$W/root" bash -c 'set -e; set -o pipefail; result=0; . "$0"; echo "after the statistics: reached, result=$result"' "$W/stats.sh" 2>&1 | tail -2; echo "exit: ${PIPESTATUS[0]}"

echo "## makefile_helper --distclean with no build root"
awk '/^  --distclean\)$/{on=1; next} on && /^    ;;$/{exit} on' "$W/makefile_helper" > "$W/distclean.sh"
mkdir -p "$W/br/.ccache"; echo fixture-3 > "$W/br/.ccache/f"
env -i PATH=/usr/bin:/bin BUILD_ROOT="$W/br" BUILD_BASE=build bash -c 'set -e; . "$0"; echo "distclean: completed"' "$W/distclean.sh" 2>&1 | tail -1
echo ".ccache: $([ -e "$W/br/.ccache" ] && echo 'still there' || echo removed)"

echo "## get_git called by scripts/get: the package name main sees"
export GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@invalid
git init -q "$W/up" && git -C "$W/up" commit -q --allow-empty -m fixture-4; V=$(git -C "$W/up" rev-parse HEAD)
mkdir -p "$W/sources/fixturepkg"
(cd "$W/sources/fixturepkg" && env -i PATH=/usr/bin:/bin HOME="$W" GIT_CONFIG_GLOBAL=/dev/null PACKAGE="$W/sources/fixturepkg/fixturepkg-$V" PKG_URL="$W/up" PKG_VERSION="$V" \
  bash -c 'lock_source_dir() { echo "lock: [$1]"; }; build_msg() { echo "message: $3"; }; . "$0"' "$W/get_git" fixturepkg 2>&1 | grep -E '^(lock|message):')
