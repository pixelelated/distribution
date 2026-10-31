#!/bin/bash
# T36 stage A: the three lanes' fixes already in this slice's files (ruling (d)), read as collisions, never re-made.
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-utils-resources-683; PIN=16dbac5211eea7e70db7394372033be2be7df829
echo "run at $(date -u +%FT%TZ)"
for x in "T20 d9afa5c7c origin/feature/m6-es-achievements-pages-667 es-core/src/utils/FileSystemUtil.cpp" \
         "T21 f7c16144d origin/feature/m6-es-state-and-bridge-668 es-core/src/utils/FileSystemUtil.cpp" \
         "T26 a5d2d3756 origin/feature/m6-es-guimenu-673 es-core/src/utils/Platform.cpp"; do
  set -- $x
  echo; echo "######## $1 $2 on $3 ($(git -C "$W" rev-parse --short=10 "$3")), $4"
  git -C "$W" merge-base --is-ancestor "$2" "$3" && echo "$2 is an ancestor of the tip"
  echo "--- git show $2 -- $4"
  git -C "$W" show --format='%H%n%an %ad%n%s%n%n%b' --date=iso "$2" -- "$4"
  echo "--- git diff PIN tip -- $4 (the tip's whole change to the file against the pin)"
  git -C "$W" diff "$PIN" "$3" -- "$4"
  echo "--- commits on the tip touching the file since the pin"
  git -C "$W" log --format='%h %ad %s' --date=short "$PIN".."$3" -- "$4"
done
