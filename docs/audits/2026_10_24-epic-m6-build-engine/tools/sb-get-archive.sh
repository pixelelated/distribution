#!/usr/bin/env bash
# E6 (#652, #834, D-WORKFLOW-193): scripts/get_archive, from a commit or the
# working tree, sourced as scripts/get sources it, with a wget shim on PATH that
# records its arguments and writes a fixed fixture body (no network). Four
# cases: a recipe with no PKG_SHA256, a wrong one, the right one, and an
# archive already cached whose recipe has no PKG_SHA256.
#   sb-get-archive.sh <scratch-dir> [commit|WORKTREE]
set -u
S="${1:?scratch directory}"; R="${2:-8ebaf8daad}"
REPO="$(git rev-parse --show-toplevel)"
W="$S/run-$(date +%s%N)"; mkdir -p "$W/bin" "$W/sources/fixturepkg"
if [ "$R" = WORKTREE ]; then cp "$REPO/scripts/get_archive" "$W/get_archive"; else git -C "$REPO" show "$R:scripts/get_archive" > "$W/get_archive"; fi
cat > "$W/bin/wget" <<'SHIM'
#!/bin/sh
echo "$*" >> "$WGET_LOG"
out=""; prev=""
for a in "$@"; do [ "$prev" = "-O" ] && out="$a"; prev="$a"; done
printf 'fixture-body\n' > "$out"
SHIM
chmod +x "$W/bin/wget"
good=$(printf 'fixture-body\n' | sha256sum | cut -d' ' -f1)
run() {   # $1 case name, $2 PKG_SHA256
  local P="$W/sources/fixturepkg/fixturepkg-1.0.tar.gz"
  : > "$W/wget.log"
  env -i PATH="$W/bin:/usr/bin:/bin" WGET_LOG="$W/wget.log" PACKAGE="$P" STAMP_URL="$P.url" STAMP_SHA="$P.sha256" \
    PKG_URL="https://fixture.invalid/fixturepkg-1.0.tar.gz" PKG_SHA256="$2" PKG_NAME=fixturepkg PKG_SOURCE_NAME=fixturepkg-1.0.tar.gz \
    DISTRO_MIRROR="https://mirror.invalid" VERBOSE=no GA="$W/get_archive" \
    bash -c 'die() { echo "die: $*" | tr "\n" " "; echo; exit 1; }
             build_msg() { :; }; pkg_lock_status() { :; }; lock_source_dir() { :; }
             . "$GA"' get fixturepkg > "$W/out" 2>&1
  local rc=$?
  echo "$1: exit $rc; wget calls $(wc -l < "$W/wget.log"); --no-check-certificate: $(grep -c -- '--no-check-certificate' "$W/wget.log"); stamp: $([ -f "$P.sha256" ] && echo written || echo none); $(grep -o 'die: .*' "$W/out" | cut -c1-140)"
}
rm -f "$W"/sources/fixturepkg/*; run "no PKG_SHA256" ""
rm -f "$W"/sources/fixturepkg/*; run "a wrong PKG_SHA256" "0000000000000000000000000000000000000000000000000000000000000000"
rm -f "$W"/sources/fixturepkg/*; run "the right PKG_SHA256" "$good"
# the right one again leaves the archive and its stamps cached; then the recipe loses its checksum
run "cached, then no PKG_SHA256" ""
