#!/usr/bin/env bash
# Build the two reviewer briefs for Phase 4.6 (#652) from the audit's current
# 02, 03, 04 and q6 files plus code excerpts at the read commit. Run from the
# worktree root. Each brief is the same packet; neither carries the other's output.
set -euo pipefail
A=docs/audits/2026_10_24-epic-m6-build-engine; SO=$A/second-opinions; R=8ebaf8daad
ex() { echo; echo "### \`$1\` lines $2 to $3 (at \`$R\`)"; echo; echo '```'; git show "$R:$1" | awk -v a="$2" -v b="$3" 'NR>=a && NR<=b {printf "%5d  %s\n", NR, $0}'; echo '```'; }
{
cat <<'EOF'
# Second opinion on a code audit -- M6.P2 T5, the build engine, epic tier

You are the second reader of a code audit. You cannot run commands or open
the repository; everything you may cite is in the packet below, and every
claim you make names the packet's `file:line` or the command output it rests
on. The first reader's verdicts are in the packet; do not take them as given.

The scope: 242 paths of a handheld Linux distribution's build engine (a
LibreELEC/ROCKNIX fork): the build scripts under `scripts/`, `config/` (the
shared shell helpers `config/functions`, the options, 139 system fragments),
`distributions/ROCKNIX/`, the `Makefile` and `Dockerfile`, and 19 upstream
GitHub workflows, read at one commit. Nothing was built: claims about
behaviour are proven by sandboxed calls of the functions with scratch
variables, by the install trees and logs of builds another lane ran, or are
marked as needing a build. The first reader is Claude Opus 5.5 (Anthropic);
you are a reviewer from another lab. The audit is a renovation: besides
defects, its findings answer seven questions (Q1 modernize, Q2 standards, Q3
bugs, Q4 package currency, Q5 efficiency, Q6 dead ends, Q7 clarity).

Answer in three parts, in this order:

1. **Your own findings first.** Read the packet's evidence -- the code
   excerpts at the end, the checks, the proofs -- and list every defect,
   gap, or unsafe seam you find that is not already one of the first
   reader's findings (F-01 to F-22). One line each: an id (G-01, G-02, ...),
   a severity (Critical / High / Medium / Low), the packet's `file:line`,
   what fails and when.
2. **Refute the first reader.** For every finding at Medium or above (High:
   F-16, F-18; Medium: F-01, F-02, F-03, F-04, F-09, F-17, F-19, F-20) and
   any Low you think mis-graded: agree, disagree, re-grade, or narrow -- and
   in each case say what would make the finding false and whether the
   packet shows it. Say whether F-16 and F-18 are really High, and whether
   any Low should be higher.
3. **What you could not judge.** The claims the packet does not let you
   verify, so the orchestrator knows where its evidence was thin.

Everyday words, no hedging: a finding either survives your reading or it
does not, and you say which.

---

EOF
for f in 02-forward-audit.md 03-retrospective.md 04-analysis.md q6-tables.md; do echo; echo "# Packet file: \`$f\`"; echo; cat "$A/$f"; done
echo; echo "# Packet: the code at the findings' sites"
ex scripts/get_env 1 22; ex Makefile 126 208; ex distributions/ROCKNIX/config/functions 95 219; ex scripts/mkimage 1 60; ex scripts/mkimage 160 334
ex scripts/get_git 1 60; ex scripts/get_git 190 239; ex scripts/get_archive 1 59; ex scripts/update_packages 40 66; ex scripts/build_distro 1 106; ex scripts/checkdeps 290 345
ex config/build-identity 1 44; ex scripts/image 56 125; ex config/functions 1095 1210; ex scripts/unpack 84 118; ex config/options 128 152
ex config/multithread 40 70; ex scripts/makefile_helper 1 30
} > "$SO/gpt-brief.md"
sed '1s/.*/# Second opinion on a code audit -- M6.P2 T5, the build engine, epic tier (the Gemini 4 Argon seat)/' "$SO/gpt-brief.md" > "$SO/gemini-argon-brief.md"
wc -c "$SO/gpt-brief.md" "$SO/gemini-argon-brief.md"
