#!/bin/bash
# T25 (#672) stage F: the re-derivations at the tip. Read-only, as stages A and B.
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-devices-unshipped-672
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t25/tmp
OUT=/workspace/tmp/m6-t25/runner-f/out
A=docs/audits/2026_10_25-epic-m6-devices-unshipped
T="$A/tools/t25-tables.py"
mkdir -p "$TMPDIR" "$OUT"
printf 'id\trc\tseconds\tstarted_utc\n' > "$OUT/runs.tsv"
run() {
  local id=$1; shift
  local t0 t1 rc started
  started=$(date -u +%H:%M:%S); t0=$(date +%s.%N)
  ( "$@" ) > "$OUT/$id.out" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  printf '%s\t%s\t%.2f\t%s\n' "$id" "$rc" "$(echo "$t1 - $t0" | bc)" "$started" >> "$OUT/runs.tsv"
}
f01_tip() { git rev-parse --short HEAD; git status --short | wc -l; }
f02_block() { bash "$A/stage-a/scope.sh"; wc -l < .qa-scratch/t25/paths.txt; }
f03_branch_vs_hash() { echo "[$(tr '\n' '\0' < .qa-scratch/t25/paths.txt | xargs -0 git diff --stat 8ebaf8daad HEAD -- | tail -1)]"; }
f04_removal_rule() { echo "[$(git diff --stat 8ebaf8daad HEAD -- packages projects tools/pkgcheck | tail -1)]"; echo "[$(git diff --stat b27889bce2 HEAD -- packages projects tools | tail -1)]"; }
f05_check_02() { python3 -I -B "$T" check "$A/02-forward-audit.md"; }
f06_check_04() { python3 -I -B "$T" check "$A/04-analysis.md"; }
f07_counts() { python3 -I -B "$T" counts; }
f08_greps() { echo "coverage $(grep -c -E '^\| `(packages|projects)/' "$A/02-forward-audit.md")"; echo "proved $(grep -c 'proved:' "$A/02-forward-audit.md") PROOF $(grep -c 'PROOF:' "$A/00-running-log.md")"; }
f09_provenance() { tr '\n' '\0' < .qa-scratch/t25/paths.txt | xargs -0 git diff --name-status c445081a59 8ebaf8daad -- | sort | uniq -c; tr '\n' '\0' < .qa-scratch/t25/paths.txt | xargs -0 git diff --name-status 651150fc88 8ebaf8daad -- | awk '{print $1}' | sort | uniq -c; }
f10_control() { grep -n -E '^(H700|SM8550):' Makefile; }
f11_tracker() {
  gh issue view 1101 --repo pixelelated/distribution --json number,state,title --jq '"#\(.number) \(.state) \(.title[0:90])"'
  gh api repos/pixelelated/distribution/issues/comments/6396356942 --jq '"#346 post " + .created_at + " " + ((.body|test("203")) | tostring) + " " + ((.body|test("301,712")) | tostring) + " " + ((.body|test("5,471")) | tostring)'
  gh issue view 1102 --repo pixelelated/distribution --json number,state,labels,milestone --jq '"#\(.number) \(.state) \([.labels[].name]|join(",")) \(.milestone.title)"'
  gh api repos/pixelelated/distribution/issues/672/sub_issues --jq '.[] | select(.number==1102) | "sub-issue of #672: #\(.number)"'
}
f12_lint() { tools/lint-audit-artifacts "$A" --issue 1102 | tail -1; }
for f in $(declare -F | awk '{print $3}' | grep -E '^f[0-9]{2}_' | sort); do run "$f" "$f"; done
cat "$OUT/runs.tsv"
