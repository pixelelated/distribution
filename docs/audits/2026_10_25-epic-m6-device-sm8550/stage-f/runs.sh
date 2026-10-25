#!/bin/bash
# T28 (#675) stage F: the re-derivations at the tip. Read-only, as stages A to D.
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-device-sm8550-675
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t28/tmp
OUT=/workspace/tmp/m6-t28/runner-f/out
A=docs/audits/2026_10_25-epic-m6-device-sm8550
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
f01_tip() { git rev-parse --short HEAD; echo "status $(git status --short | wc -l)"; }
f02_block() { bash "$A/stage-a/scope.sh" | head -4; }
f03_read_at_reviewed() { echo "[$(tr '\n' '\0' < .qa-scratch/t28/paths.txt | xargs -0 git diff --stat 8ebaf8daad 458e2bfda1 -- | tail -1)]"; }
f04_removal_a_to_d() { echo "[$(git diff --stat 458e2bfda1 867039c467 -- packages projects tools | tail -1)]"; }
f05_stage_e_diff() { git diff --stat 867039c467 HEAD -- packages projects tools; }
f06_check_02() { python3 -I -B "$A/tools/t28-tables.py" check "$A/02-forward-audit.md"; python3 -I -B "$A/tools/t28-tables.py" counts; }
f07_greps() { echo "coverage $(awk '/^## Coverage/{p=1;next} /^## /{p=0} p' "$A/02-forward-audit.md" | grep -c -E '^\| `')"; echo "proved $(grep -c 'proved:' "$A/02-forward-audit.md") PROOF $(grep -c 'PROOF:' "$A/00-running-log.md")"; }
f08_run_all() { git show b13d5d8074:projects/ROCKNIX/devices/SM8550/bootloader/update.sh > "$TMPDIR/f-unfixed-update.sh"; "$A/stage-e/run-all.sh" "$TMPDIR/f-unfixed-update.sh" projects/ROCKNIX/devices/SM8550/bootloader/update.sh | tail -2; }
f09_provenance() { for f in gpt-probe gpt-audit; do python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); f=d["final"]; print(sys.argv[1].split("/")[-1], f["verification"]["result"], f["verification"]["observed"], f["effort_verification"]["result"], f["provider_verification"]["result"], d["facilitator_version"])' "$A/second-opinions/$f.md.provenance.json"; done; }
f10_tracker() {
  gh issue view 1109 --repo pixelelated/distribution --json number,state,labels --jq '"#\(.number) \(.state) \([.labels[].name]|join(","))"'
  gh issue view 1108 --repo pixelelated/distribution --json number,state,labels,milestone --jq '"#\(.number) \(.state) \([.labels[].name]|join(",")) \(.milestone.title)"'
  gh api repos/pixelelated/distribution/issues/675/sub_issues --jq '.[] | select(.number==1108) | "sub-issue of #675: #\(.number)"'
  gh api repos/pixelelated/distribution/issues/comments/6396876866 --jq '"#1099 comment " + .created_at + " names #1109: " + ((.body|test("#1109"))|tostring)'
  gh api repos/pixelelated/distribution/issues/comments/6396877061 --jq '"#1100 comment " + .created_at + " seven-tree: " + ((.body|test("Seven of the fourteen"))|tostring)'
}
f11_lint() { tools/lint-audit-artifacts "$A" --issue 1108 | tail -1; }
f12_boxes() { tools/box-check --issue 1109 | tail -1; tools/box-check --issue 1108 | tail -1; }
for f in $(declare -F | awk '{print $3}' | grep -E '^f[0-9]{2}_' | sort); do run "$f" "$f"; done
cat "$OUT/runs.tsv"
