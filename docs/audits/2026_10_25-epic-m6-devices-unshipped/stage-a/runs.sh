#!/bin/bash
# T25 (#672) stage A: brief section 2's block and section 5's checks, each
# with its exit and wall time. Read-only: no fetch, no build, no plan, no
# guest, no handheld, no M7 root, no tools/council/run.
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-devices-unshipped-672
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t25/tmp
OUT=/workspace/tmp/m6-t25/runner/out
mkdir -p "$TMPDIR" "$OUT" .qa-scratch/t25
TG="AMD64 RK3326 RK3399 RK3566 RK3576 RK3588 S922X SM4450 SM6115 SM8250 SM8650 SM8750"
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
P() { tr '\n' '\0' < .qa-scratch/t25/paths.txt; }
c01_block() { bash /workspace/tmp/m6-t25/runner/scope.sh; wc -l < .qa-scratch/t25/paths.txt; }
c02_paths() { wc -l < .qa-scratch/t25/paths.txt; }
c03_branch_vs_hash() { echo "[$(P | xargs -0 git diff --stat 8ebaf8daad HEAD -- | tail -1)]"; }
c04_target_lines() { grep -n -E '^(AMD64|RK3326|RK3399|RK3566|RK3576|RK3588|S922X|SM4450|SM6115|SM8250|SM8650|SM8750):' Makefile; echo "count $(grep -n -E '^(AMD64|RK3326|RK3399|RK3566|RK3576|RK3588|S922X|SM4450|SM6115|SM8250|SM8650|SM8750):' Makefile | wc -l)"; }
c05_world() { sed -n '42p' Makefile; }
c06_project_lines() { echo "PROJECT= lines $(grep -n 'PROJECT=' Makefile | wc -l); not ROCKNIX $(grep -n 'PROJECT=' Makefile | grep -v 'PROJECT=ROCKNIX' | wc -l)"; }
c07_prov_base() { P | xargs -0 git diff --name-status c445081a59 8ebaf8daad -- | sort | uniq -c; }
c08_prov_upstream() { P | xargs -0 git diff --name-status 651150fc88 8ebaf8daad -- | awk '{print $1}' | sort | uniq -c; }
c09_upstream_commits() { P | xargs -0 git log --oneline c445081a59..651150fc88 -- | wc -l; }
c10_fork_commits() { for d in $TG; do printf '%s %s:' "$d" "$(git log --format=%h 651150fc88..8ebaf8daad -- "projects/ROCKNIX/devices/$d" | wc -l)"; git log --format=' %h(%p)' 651150fc88..8ebaf8daad -- "projects/ROCKNIX/devices/$d" | tr '\n' ' '; echo; done; }
c11_upstream_since() { for d in $TG; do printf '%s ' "$d"; git log --oneline --since='2026-06-01T00:00:00Z' 651150fc88 -- "projects/ROCKNIX/devices/$d" | wc -l; done; }
c12_engine_refs() { for p in ARM Allwinner Amlogic Generic NXP Qualcomm RPi Rockchip Samsung; do printf '%s ' "$p"; git grep -n -w "$p" -- Makefile config scripts | wc -l; done; }
c13_hostname() { git grep -n 'DEFAULT_HOSTNAME' 8ebaf8daad -- packages/linux projects/ROCKNIX/packages/linux | cut -c1-160; }
c14_hostname_log() { git log --format='%h %ad %s' --date=short -3 8ebaf8daad -- packages/linux/package.mk projects/ROCKNIX/packages/linux/package.mk | cut -c1-120; }
c15_bytes() { P | xargs -0 git ls-tree -r -l 8ebaf8daad -- | awk '{b+=$4} END {print b " bytes"}'; }
c16_control_targets() { grep -n -E '^(H700|SM8550):' Makefile; echo "count $(grep -n -E '^(H700|SM8550):' Makefile | wc -l)"; }
c17_control_block() {
  python3 -I -c '
import json
inv=json.load(open("docs/reviews/inventory.json")); cols=inv["columns"]
rows=[dict(zip(cols,r)) for r in inv["rows"]]
t=[r for r in rows if r["tree"]=="distribution" and r["area"]=="devices" and (r["path"].startswith("projects/") or r["path"].startswith("packages/")) and "/H700/" in r["path"] and r["reach"]=="shipped"]
print("rows",len(t),"in-dir",sum(1 for r in t if r["path"].startswith("projects/ROCKNIX/devices/H700/")),"other",[r["path"] for r in t if not r["path"].startswith("projects/ROCKNIX/devices/H700/")])'
}
for f in $(declare -F | awk '{print $3}' | grep -E '^c[0-9]{2}_' | sort); do run "$f" "$f"; done
cat "$OUT/runs.tsv"
