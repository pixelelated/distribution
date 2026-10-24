#!/usr/bin/env bash
# E7 (#652, PL-18): the Makefile's Docker targets under `make -n` (nothing is
# run: the docker-% recipe calls no $(MAKE), and its $(shell) lines test files
# and read `docker --version`), at a commit or from the working tree. HOME is a
# scratch directory holding an empty fixture options file, so the real one is
# never read. Prints counts and the mount arguments only, never a command line.
#   sb-make-n.sh <scratch-dir> [commit|WORKTREE]
set -u
S="${1:?scratch directory}"; R="${2:-8ebaf8daad}"
REPO="$(git rev-parse --show-toplevel)"
H="$S/home-$(date +%s%N)"; mkdir -p "$H/.ROCKNIX"; : > "$H/.ROCKNIX/options"
MK="$H/Makefile"; if [ "$R" = WORKTREE ]; then cp "$REPO/Makefile" "$MK"; else git -C "$REPO" show "$R:Makefile" > "$MK"; fi
mn() { (cd "$REPO" && env -i PATH=/usr/bin:/bin HOME="$H" "$@" make -n -f "$MK" "$T" 2>&1); }
T=docker-GENERIC_X64
echo "options mount: $(mn | grep -o -- "-v \"$H/.ROCKNIX/options[^\"]*\"" | sed "s#$H#<home>#g")"
echo "keys file set but missing: $(mn LOCAL_SSH_KEYS_FILE="$H/fixture-absent" | grep -c -- "-v \"$H/fixture-absent") -v argument(s)"
: > "$H/fixture-keys"
echo "keys file set and present: $(mn LOCAL_SSH_KEYS_FILE="$H/fixture-keys" | grep -c -- "-v \"$H/fixture-keys:$H/fixture-keys\"") -v argument(s)"
echo "ES source set but missing: $(mn EMULATIONSTATION_SRC="$H/fixture-no-src" | grep -c -- "-v \"$H/fixture-no-src") -v argument(s)"
targets=$(grep -o -E '^docker-[A-Za-z0-9_-]+:' "$MK" | tr -d ':' | sort -u)
devices=$(grep -o -E '^[A-Z0-9_]+:' "$MK" | tr -d ':' | grep -v -E '^(PHONY)$' | sort -u)
ok=0; bad=""
for T in $targets $(for d in $devices; do echo "docker-$d"; done); do
  if mn > /dev/null; then ok=$((ok+1)); else bad+=" $T"; fi
done
echo "make -n: $ok docker-* targets resolve; failed:${bad:- none}"
