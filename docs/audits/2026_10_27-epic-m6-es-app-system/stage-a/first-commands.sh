cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-app-system-680
cat .github/sessions/saved-session-state-feature-m6-es-app-system-680.md    # the pointer: the dispatch's two hashes; § 10 names the lines to check
git status --short | wc -l                                                   # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1               # empty: the read is of next's bytes
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-system-680; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                # the pin; 0
git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10                     # cada856d86: the merge base with ROCKNIX's master (not bccd715707, § 2)
git -C "$W" rev-parse --verify rocknix/master | cut -c1-10                    # f6c542872e, read from the shared refs
git -C "$W" rev-parse --verify origin/feature/m6-es-state-and-bridge-668 | cut -c1-9     # 3ae9610b0: T21's ES tip, whose CMakeLists and WifiText deltas § 2 names
git -C "$W" rev-parse --verify origin/feature/m6-es-achievements-pages-667 | cut -c1-9   # 5c0ddaaee: T20's ES tip, whose OfflineAchievementsText deltas § 2 names
git show origin/feature/m6-es-state-and-bridge-668:docs/audits/2026_10_26-epic-m6-es-state-and-bridge/05-punch-list.md | /usr/bin/grep -c '^## PL-'   # 26: PL-20 is routed here (#1186)
tools/register-check >/dev/null && echo register-ok
date -u +%H:%M:%S; tail -n 3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200   # who holds the host, with the time of the read: no guest before a grant on #680
