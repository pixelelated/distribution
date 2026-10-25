#!/bin/bash
# brief section 5's tiers block, as written (lines 364-376).
cd /workspace/repos/pixelelated/distribution.worktrees/m6-os-device-quirks-676 || exit 2
python3 -I - <<'PY'
import json
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
P = "projects/ROCKNIX/packages/hardware/quirks/devices/"
t = [r for r in rows if r["tree"] == "distribution" and r["path"].startswith(P)]
A = ["Retroid Pocket Nova", "QEMU Standard PC (Q35 + ICH9, 2009)"]
B = A + ["Anbernic RG40XX H", "Anbernic RG40XX V", "Anbernic RG CubeXX", "AYANEO Pocket ACE", "AYANEO Pocket DMG", "AYANEO Pocket DS", "AYANEO Pocket EVO", "AYANEO Pocket S 2K", "AYANEO Pocket S Mini", "AYN Odin 2", "AYN Odin 2 Portal", "AYN Thor", "Retroid Pocket 6", "Retroid Pocket 6 TOP-DPAD"]
def tally(names):
    s = [r for r in t if r["path"][len(P):].split("/")[0] in names]
    return len(s), sum(r["lines"] or 0 for r in s), sum(1 for r in s if r["tier"] == "fork-own")
print("A", tally(A)); print("B", tally(B)); print("rest", len(t) - tally(B)[0])
PY
