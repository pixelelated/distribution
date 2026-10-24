#!/usr/bin/env bash
# E7 (#652, #835): scripts/checkdeps' two host-changing blocks (the gcc
# alternative and the /nix preparation, to the end of the file), lifted by
# their markers from a commit or the working tree and run under set -e with
# DISTRO=ubuntu and shims for sudo and gcc-12 on PATH. The sudo shim records
# its arguments and runs nothing, so the host is never changed. The fixture
# relies on this host having no /nix and no gcc alternative (checked first).
#   sb-checkdeps.sh <scratch-dir> [commit|WORKTREE]
set -u
S="${1:?scratch directory}"; R="${2:-8ebaf8daad}"
REPO="$(git rev-parse --show-toplevel)"
[ ! -e /nix ] && ! update-alternatives --query gcc >/dev/null 2>&1 || { echo "this host has /nix or a gcc alternative: the fixture cannot show the changes" >&2; exit 2; }
W="$S/run-$(date +%s%N)"; mkdir -p "$W/bin"
if [ "$R" = WORKTREE ]; then cat "$REPO/scripts/checkdeps"; else git -C "$REPO" show "$R:scripts/checkdeps"; fi > "$W/checkdeps.src"
{ awk '/^# Configure gcc-12/{on=1} on{print} on && /^esac$/{exit}' "$W/checkdeps.src"
  awk '/^### NIX PREPARATION ###/{on=1} on' "$W/checkdeps.src"; } > "$W/blocks.sh"
printf '#!/bin/sh\necho "$*" >> "$SUDO_LOG"\n' > "$W/bin/sudo"; printf '#!/bin/sh\nexit 0\n' > "$W/bin/gcc-12"; chmod +x "$W/bin/sudo" "$W/bin/gcc-12"
for optin in "" 1; do
  : > "$W/sudo.log"
  env -i PATH="$W/bin:/usr/bin:/bin:/usr/sbin:/sbin" HOME="$W" SUDO_LOG="$W/sudo.log" DISTRO=ubuntu \
    ${optin:+CHECKDEPS_ALLOW_HOST_CHANGES=$optin} bash -c 'set -e; get_deps() { :; }; . "$0"' "$W/blocks.sh" > "$W/out" 2>&1
  rc=$?
  echo "CHECKDEPS_ALLOW_HOST_CHANGES=${optin:-unset}: exit $rc; sudo called $(wc -l < "$W/sudo.log") times ($(cut -d' ' -f1-2 "$W/sudo.log" | tr '\n' ',' | sed 's/,$//'))"
  grep -E '^checkdeps:|^\*\*\*\*' "$W/out" | sed 's/^/  /'
done
