#!/bin/bash
# T36 stage A: the brief's § 1 first commands, each line as it prints (run from the distribution worktree).
echo "run at $(date -u +%FT%TZ)"
git status --short | wc -l
git log --oneline -3
git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-utils-resources-683; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l
git -C "$W" rev-parse --abbrev-ref HEAD
git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10
git -C "$W" rev-parse --verify rocknix/master | cut -c1-10
git -C "$W" rev-parse --verify batocera/master | cut -c1-10
git -C "$W" merge-base "$PIN" batocera/master | cut -c1-10
for b in m6-es-launch-path-649 m6-es-cloud-pages-665 m6-es-achievements-pages-667 m6-es-state-and-bridge-668 m6-es-guimenu-673 m6-es-pages-678 m6-es-app-views-scrapers-679 m6-es-app-system-680 m6-es-core-components-681 m6-es-core-window-input-682; do printf '%s ' "$b"; git -C "$W" rev-parse --verify "origin/feature/$b" 2>&1 | cut -c1-10; done
tools/register-check >/dev/null && echo register-ok
date -u +%H:%M:%S; tail -n 6 /workspace/tmp/m7-m6-host-coordination.txt | cut -c1-200
# pgrep -c prints its count and exits 1 when it is 0, so the count is read as printed
q=$(pgrep -x qemu-system-x86 -r R,S,D,T | wc -l); c=$(pgrep -c -x 'cc1|cc1plus|collect2|ld|as|rustc|clang|clang\+\+' 2>/dev/null); echo "census: qemu $q, compilers ${c:-0}"
echo "(git status --short counts this run's own untracked stage-a/ directory at stage A)"
