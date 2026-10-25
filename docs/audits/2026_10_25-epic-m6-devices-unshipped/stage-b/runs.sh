#!/bin/bash
# T25 (#672) stage B: the tables' inputs and checks, each with its exit and
# wall time. Read-only: no fetch, no build, no plan, no guest, no handheld,
# no M7 root, no tools/council/run. Writes only under OUT and TMPDIR.
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-devices-unshipped-672
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t25/tmp
OUT=/workspace/tmp/m6-t25/runner-b/out
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
b01_tip_vs_hash_engine() {
  git diff --stat 8ebaf8daad HEAD -- Makefile config scripts | tail -1
  diff <(git show 8ebaf8daad:Makefile | grep -n -E '^[A-Z0-9_]+:|^world') <(grep -n -E '^[A-Z0-9_]+:|^world' Makefile) && echo "target lines: identical"
  diff <(git grep -n -w -E 'ARM|Allwinner|Amlogic|Generic|NXP|Qualcomm|RPi|Rockchip|Samsung' 8ebaf8daad -- Makefile config scripts | cut -d: -f2-) \
       <(git grep -n -w -E 'ARM|Allwinner|Amlogic|Generic|NXP|Qualcomm|RPi|Rockchip|Samsung' -- Makefile config scripts) && echo "engine references: identical"
}
b02_pkgcheck_slice() {
  grep '/package.mk$' .qa-scratch/t25/paths.txt | while IFS= read -r p; do
    a=${p#*/}; a=${a%/package.mk}
    tools/pkgcheck "$a" > "$TMPDIR/pc.one" 2> "$TMPDIR/pc.err"; rc=$?
    tr '\r' '\n' < "$TMPDIR/pc.err" | sed 's/\x1b\[K//g; s/\.\.\.$//' | grep -v '^$' > "$TMPDIR/pc.list"
    printf '%s\trc=%s\tself=%s\tof=%s\tfail=%s\twarn=%s\n' "$p" "$rc" "$(grep -c -x -F "$p" "$TMPDIR/pc.list")" \
      "$(wc -l < "$TMPDIR/pc.list")" "$(grep -F "$p" "$TMPDIR/pc.one" | grep -c FAIL)" "$(grep -F "$p" "$TMPDIR/pc.one" | grep -c WARN)"
    grep -F "$p" "$TMPDIR/pc.one" | sed 's/\x1b[^m]*m//g; s/\x1b(B//g' | sed 's/^/  | /'
  done
}
b03_pkgcheck_control() {
  C=/workspace/tmp/m6-t25/pkgcheck-control
  mkdir -p "$C/packages/t25-bad" "$C/projects"
  printf 'PKG_NAME="t25-bad"\nPKG_VERSION="1"\nPKG_SOURCE_DIR="${PKG_BUILD}/x"\n' > "$C/packages/t25-bad/package.mk"
  (cd "$C" && "$D/tools/pkgcheck" t25-bad 2>/dev/null | sed 's/\x1b[^m]*m//g; s/\x1b(B//g'; exit "${PIPESTATUS[0]}")
}
b04_pkgcheck_tree() {
  tools/pkgcheck 2>/dev/null > "$TMPDIR/pc.tree"; rc=$?
  sed 's/\x1b[^m]*m//g; s/\x1b(B//g' "$TMPDIR/pc.tree" | grep -o -E '^\[(FAIL|WARN)\]' | sort | uniq -c
  echo "recipes $(find packages projects -type f -name package.mk | wc -l)"
  echo "FAIL files in the slice: $(sed 's/\x1b[^m]*m//g; s/\x1b(B//g' "$TMPDIR/pc.tree" | grep '^\[FAIL\]' | grep -c -F -f <(grep '/package.mk$' .qa-scratch/t25/paths.txt))"
  return $rc
}
b05_hosts() {
  python3 -I -B - <<'PY'
import subprocess, re, collections
hosts = collections.Counter()
for p in [l for l in open(".qa-scratch/t25/paths.txt").read().split() if l.endswith("/package.mk")]:
    t = subprocess.run(["git", "show", "8ebaf8daad:" + p], capture_output=True, text=True).stdout
    v = {}
    for m in re.finditer(r'^\s*(PKG_[A-Z_]+)="([^"]*)"', t, re.M):
        v.setdefault(m.group(1), m.group(2))
    def sub(s):
        for _ in range(3):
            s = re.sub(r'\$\{?(PKG_[A-Z_]+)\}?', lambda m: v.get(m.group(1), m.group(0)), s)
        return s
    urls = re.findall(r'^\s*PKG_URL="([^"]*)"', t, re.M)
    hs = sorted({(re.match(r'[a-z+]+://([^/]+)', sub(u)).group(1) if re.match(r'[a-z+]+://', sub(u)) else "(none)") for u in urls}) or ["(no PKG_URL)"]
    for h in hs: hosts[h] += 1
    print(f"{p}\t{','.join(hs)}")
print("HOSTS", dict(hosts.most_common()))
PY
}
b06_hostname_strings() { git grep -h 'CONFIG_DEFAULT_HOSTNAME' 8ebaf8daad -- projects packages | sed 's/^[[:space:]]*//' | sort | uniq -c; }
b07_drift_226() {
  for d in AMD64 RK3326 RK3399 RK3566 RK3576 RK3588 S922X SM4450 SM6115 SM8250 SM8650 SM8750; do echo "projects/ROCKNIX/devices/$d"; done > "$TMPDIR/tdirs"
  tr '\n' '\0' < "$TMPDIR/tdirs" | xargs -0 git diff --stat 651150fc88 8ebaf8daad -- | tail -1
}
b08_kernel_edges() { git show 8ebaf8daad:projects/ROCKNIX/packages/linux/package.mk | sed -n '69,72p;81,84p;108,111p;200,204p'; sed -n '789,798p' config/functions; }
gen() { python3 -I -B "$T" "$1"; }
for f in $(declare -F | awk '{print $3}' | grep -E '^b[0-9]{2}_' | sort); do run "$f" "$f"; done
for s in counts units targets projects pins trees q6 q7 edges coverage; do run "g_$s" gen "$s"; done
cat "$OUT/runs.tsv"
