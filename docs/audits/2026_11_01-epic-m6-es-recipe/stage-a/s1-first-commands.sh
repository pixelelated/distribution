cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684 || exit 2
echo "== date"; date -u +%Y-%m-%dT%H:%M:%SZ
echo "== cat pointer (lines)"; cat .github/sessions/saved-session-state-feature-m6-es-recipe-684.md | wc -l
echo "== status"; git status --short | wc -l                                                 # 0
echo "== log"; git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
echo "== ui stat vs next"; git diff --stat 8ebaf8daad HEAD -- projects/ROCKNIX/packages/ui | tail -n 1   # empty
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here
echo "== merge-base"; git merge-base 2174265e9c 651150fc88                                        # c445081a59518f37d9776e5412dd7b14910696f7
Q=/home/max/Development/emulationstation-next.worktrees/qa-integration; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$Q" cat-file -e "$PIN^{commit}" && echo pin-here
echo "== rocknix/master"; git -C "$Q" rev-parse --verify rocknix/master                               # f6c542872e..., the whole line
echo "== es merge-base"; git -C "$Q" merge-base "$PIN" rocknix/master                                # cada856d86..., the whole line
for r in origin/feature/m6-es-core-window-input-682 origin/feature/m6-es-core-utils-resources-683; do printf '%s ' "$r"; git -C "$Q" rev-parse --verify "$r" 2>&1; done   # each line recorded whole, hash or fatal:
echo "== pkgcheck"
for n in emulationstation es-theme-art-book-next lowerdeck; do find packages projects -type f -path "*/$n/package.mk"; tools/pkgcheck "$n"; rc=$?
echo "pkgcheck $n rc=$rc"; done
tools/register-check >/dev/null; rc=$?
echo "register-check rc=$rc"
date -u +%H:%M:%S; tail -n 6 /workspace/tmp/m7-m6-host-coordination.txt | cut -c1-200
