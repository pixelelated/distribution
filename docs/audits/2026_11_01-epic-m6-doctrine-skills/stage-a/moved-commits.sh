#!/usr/bin/env bash
# T38 stage A (#685): which commit since the P1 tip touched which of the three moved files, and
# the merge 18747fbc52's own change to them against its first parent. Run from the lane's worktree.
date -u +%H:%M:%S
F=(.claude/skills/code-auditor/references/templates.md .claude/skills/council/IMPORTED-FROM.md .claude/skills/mini-retro/references/scoped-audit.md)
git log --format='%h' --name-only 2174265e9c..HEAD -- "${F[@]}" | sed '/^$/d'
echo "--- the merge 18747fbc52 against its first parent, on the three:"
git diff --stat 18747fbc52^1 18747fbc52 -- "${F[@]}"
