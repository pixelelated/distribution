#!/bin/bash
# T37 (#684) stage B, L-01: the ARMSX2 lines in the ES recipe at each fork merge of upstream/next that
# R2 names, at each parent and at the result (read-only git).
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684 || exit 2
E=projects/ROCKNIX/packages/ui/emulationstation/package.mk
for h in c445081a59 651150fc88 2174265e9c; do echo "$h armsx2 lines: $(git show $h:$E | /usr/bin/grep -c -i armsx2)"; done
git log --format='%h %ad %s' --date=short -S'armsx2-sa' 651150fc88 -- $E
for m in a06539d8ec 049765fba0 fa2990c1e7 f370dc8787; do printf '%s %s parents:' "$m" "$(git log -1 --format=%ad --date=short $m)"; for p in $(git rev-parse $m^@); do printf ' %s=%s' "${p:0:10}" "$(git show $p:$E | /usr/bin/grep -c -i armsx2)"; done; echo " result=$(git show $m:$E | /usr/bin/grep -c -i armsx2)"; done
git show 651150fc88:$E | awk 'NR>=104 && NR<=108 {printf "651150fc88:%d: %s\n", NR, $0}'
