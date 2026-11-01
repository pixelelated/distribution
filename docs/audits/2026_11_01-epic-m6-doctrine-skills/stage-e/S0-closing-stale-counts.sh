#!/usr/bin/env bash
# T38 (#685) stage E, S0's closing: section 5's counting run in stage A chunk 18's form (R3 C21's terms, case-insensitive,
# begin-exploration added) over the 52 at fixed-at beside the dispatch tip, and outside the export. Prints one line per term.
#   bash S0-closing-stale-counts.sh <worktree> <fixed-at>
R=${1:?worktree}; F=${2:?fixed-at}
for t in 'rubber[- ]duck' 'copilot' '\.github/instructions' '\.github/prompts' 'test/qa-integration' 'opus[- ]4[.]8|claude-opus-4' 'gpt-5[.]5' 'gpt-5[.]6' 'mistral' 'trio' 'rasteratops' 'state-main' 'scaffold' 'begin-exploration'; do
  a=$(git -C "$R" grep -i -E "$t" 87c2ab0fed -- .claude/agents .claude/skills | wc -l); af=$(git -C "$R" grep -l -i -E "$t" 87c2ab0fed -- .claude/agents .claude/skills | wc -l)
  b=$(git -C "$R" grep -i -E "$t" "$F" -- .claude/agents .claude/skills | wc -l); bf=$(git -C "$R" grep -l -i -E "$t" "$F" -- .claude/agents .claude/skills | wc -l)
  o=$(git -C "$R" grep -i -E "$t" "$F" -- .claude/skills ':(exclude).claude/skills/council' ':(exclude).claude/skills/council-research' | wc -l)
  printf '%s: %s lines in %s files at the tip; %s lines in %s files at fixed-at, %s of them outside the export\n' "$t" "$a" "$af" "$b" "$bf" "$o"
done
