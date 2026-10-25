#!/bin/bash
# T28 (#675) stage A: brief section 2's membership block, as written (lines 86-104).
cd /workspace/repos/pixelelated/distribution.worktrees/m6-device-sm8550-675 || exit 2
python3 -I - <<'PY'
import json, collections, os
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
t28 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "devices"
       and r["path"].startswith("projects/ROCKNIX/devices/SM8550/")]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t28), "lines", L(t28), dict(collections.Counter(r["reach"] for r in t28)), dict(collections.Counter(r["tier"] for r in t28)))
print(dict(collections.Counter(r["language"] for r in t28)))
CODE = {"shell", "recipe", "udev", "python", "c", "make"}
rd = [r for r in t28 if r["language"] in CODE and r["tier"] != "vendor-carried" and r["reach"] != "unreached"]
print("read", len(rd), L(rd), "fork-own", sum(1 for r in rd if r["tier"] == "fork-own"))
alld = [r for r in rows if r["tree"] == "distribution" and r["path"].startswith("projects/ROCKNIX/devices/SM8550/")]
print("whole directory in the inventory", len(alld), L(alld), dict(collections.Counter(r["area"] for r in alld)))
os.makedirs(".qa-scratch/t28", exist_ok=True)
open(".qa-scratch/t28/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t28, key=lambda r: r["path"])))
for r in sorted(t28, key=lambda r: r["path"]): print(r["reach"], r["tier"], r["lines"], r["path"])
PY
wc -l .qa-scratch/t28/paths.txt     # 29
