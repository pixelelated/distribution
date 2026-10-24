#!/bin/bash
# P8 (#652, PL-14, F-08): scripts/unpack's move of the unpacked tree, lifted
# from a commit (or the working tree) between its own markers (after the
# extract, up to the PKG_SOURCE_DIR fallback), over one and two matching
# directories. `die` is stubbed to print and exit, as config/functions' does.
#   sb-unpack-glob.sh <empty scratch dir> [commit|WORKTREE]
mkdir -p "${1:?usage: sb-unpack-glob.sh <empty scratch dir> [commit|WORKTREE]}" && cd "$1" || exit 2
R=${2:-8ebaf8daad}; REPO="$(git -C "$OLDPWD" rev-parse --show-toplevel)"
if [ "$R" = WORKTREE ]; then cat "$REPO/scripts/unpack"; else git -C "$REPO" show "$R:scripts/unpack"; fi \
  | awk '/^  pkg_call_finish$/{seen=1; next} seen && /^  fi$/ && !on {on=1; next} /^  if \[ ! -d "\$\{PKG_UNPACK_DIR\}\/\.intermediate" \]; then/{exit} on' > block.sh
for n in one two; do
  U=$PWD/u-$n; rm -rf "$U"; mkdir -p "$U/fixturepkg-1.0"; echo fixture-1 > "$U/fixturepkg-1.0/f"
  [ $n = two ] && { mkdir -p "$U/fixturepkg-1.0-extra"; echo fixture-2 > "$U/fixturepkg-1.0-extra/g"; }
  out=$(PKG_UNPACK_DIR=$U PKG_NAME=fixturepkg PKG_VERSION=1.0 PKG_SOURCE_DIR= bash -c 'die() { echo "die: $*"; exit 1; }; . ./block.sh; echo "exit 0"' 2>&1)
  echo "$n: $(echo "$out" | tr '\n' ' ')| .intermediate: $([ -f "$U/.intermediate/f" ] && echo 'holds the source' || echo 'nothing moved')"
done
echo "lifted block: $(wc -l < block.sh) lines"
