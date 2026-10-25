#!/bin/bash
# T29 (#676) stage A: brief section 2's membership block, as written (lines 87-105).
cd /workspace/repos/pixelelated/distribution.worktrees/m6-os-device-quirks-676 || exit 2
python3 -I - <<'PY'
import json, collections, os
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
P = "projects/ROCKNIX/packages/hardware/quirks/devices/"
t29 = [r for r in rows if r["tree"] == "distribution" and r["path"].startswith(P)]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t29), "lines", L(t29), dict(collections.Counter(r["reach"] for r in t29)), dict(collections.Counter(r["tier"] for r in t29)), dict(collections.Counter(r["area"] for r in t29)))
print(dict(collections.Counter(r["language"] for r in t29)))
rd = [r for r in t29 if r["language"] == "shell"]
print("read", len(rd), L(rd), "fork-own", sum(1 for r in rd if r["tier"] == "fork-own"), "fork-own paths", [r["path"][len(P):] for r in t29 if r["tier"] == "fork-own"])
ent = collections.defaultdict(lambda: [0, 0, 0])
for r in t29:
    e = r["path"][len(P):].split("/")[0]; ent[e][0] += 1; ent[e][1] += r["lines"] or 0; ent[e][2] += (r["tier"] == "fork-own")
print("entries", len(ent), "of which top-level symlinks", sum(1 for r in t29 if r["language"] == "symlink" and "/" not in r["path"][len(P):]))
os.makedirs(".qa-scratch/t29", exist_ok=True)
open(".qa-scratch/t29/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t29, key=lambda r: r["path"])))
open(".qa-scratch/t29/entries.tsv", "w").write("".join("%s\t%d\t%d\t%d\n" % (e, v[0], v[1], v[2]) for e, v in sorted(ent.items())))
PY
wc -l .qa-scratch/t29/paths.txt .qa-scratch/t29/entries.tsv     # 333, 88
