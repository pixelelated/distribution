# T32 (#679) stage A: the brief's § 1 first commands, as written (the cat's output is the pointer; recorded by its line count)
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-app-views-scrapers-679
wc -l .github/sessions/saved-session-state-feature-m6-es-app-views-scrapers-679.md
git status --short | wc -l
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here
W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-views-scrapers-679; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l
git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10
git -C "$W" rev-parse --verify rocknix/master | cut -c1-10
git -C "$W" rev-parse --verify origin/feature/m6-es-state-and-bridge-668 | cut -c1-9
git show origin/feature/m6-es-state-and-bridge-668:docs/audits/2026_10_26-epic-m6-es-state-and-bridge/05-punch-list.md | /usr/bin/grep -c '^## PL-'
tools/register-check >/dev/null && echo register-ok
tail -n 3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200
