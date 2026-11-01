#!/usr/bin/env bash
# chunk-run.sh <block> <workdir>: T38 stage A (#685). Splits a brief block at its column-0
# comment lines and sources each chunk in this one shell, so the block's variables carry over;
# prints each chunk's UTC start and end, its wall seconds and the exit of its last command
# (the block's own rc=$? lines are the per-command record).
_B=$1; _W=$2; mkdir -p "$_W"
python3 -I - "$_B" "$_W" <<'PY'
import sys, os
b, w = sys.argv[1], sys.argv[2]
chunks = [[]]
for ln in open(b):
    if ln.startswith("# ") and chunks[-1]:
        chunks.append([])
    chunks[-1].append(ln)
for i, c in enumerate(chunks, 1):
    open(os.path.join(w, "chunk-%02d.sh" % i), "w").write("".join(c))
print("chunks:", len(chunks))
PY
for _c in "$_W"/chunk-*.sh; do
  printf '== %s begins %s: %s\n' "${_c##*/}" "$(date -u +%H:%M:%S)" "$(head -n 1 "$_c" | cut -c1-100)"
  _s=$(date +%s)
  . "$_c"
  _rc=$?
  _e=$(date +%s)
  printf '== %s ends %s, last command rc=%s, wall %ss\n' "${_c##*/}" "$(date -u +%H:%M:%S)" "$_rc" "$((_e-_s))"
done
