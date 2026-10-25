#!/usr/bin/env python3
"""#1060, harness half: an absence judged on a listing that did not happen.
cloud-round-trip's listing helpers over a cloud-test-backend whose state does
not exist (under $TMPDIR). The backend is the one beside the tool unless
--backend names another (the stream's run used S1's fixed backend against
the unfixed harness).
    python3 -I -B pos1060/drive.py <cloud-round-trip> unfixed|fixed [--backend <cloud-test-backend>]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import args, load, scratch, verdict

tool, expect = args()
crt = load(tool)
if "--backend" in sys.argv:
    crt.BACKEND = os.path.abspath(sys.argv[sys.argv.index("--backend") + 1])
os.environ["CLOUD_QA_STATE"] = os.path.join(scratch("pos1060"), "no-such-state")
seen = {}
for fn in ("backend_files", "backend_sizes"):
    try:
        listing = getattr(crt, fn)("ROMs")
        seen[fn] = "passes" if "game.rom" not in list(listing) else "fails"
        print(f"{fn}: returned {listing!r}; step 27's absence check would read {'PASS' if seen[fn] == 'passes' else 'FAIL'}")
    except crt.Fail as e:
        seen[fn] = "Fail"
        print(f"{fn}: Fail: {str(e)[:150]}")
try:
    crt.backend("ls"); seen["backend"] = "returned"
except crt.Fail:
    seen["backend"] = "Fail"
except Exception as e:
    seen["backend"] = type(e).__name__
print(f"backend('ls'): {seen['backend']}")
observed = ("fixed" if all(v == "Fail" for v in seen.values())
            else "unfixed" if seen["backend_files"] == "passes" else "neither")
verdict("pos1060", expect, observed, ", ".join(f"{k} {v}" for k, v in seen.items()))
