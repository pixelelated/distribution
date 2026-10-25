#!/usr/bin/env python3
"""#1070: KILL5's expectation at CLOUD_BACKUP_KEEP=2 against two retention
results, a correct one keeping the newest 2 and one hard-coded to 3 (unfixed:
the fixture and expectation as fx_kill5 wrote them; fixed: kill5_names()).
    python3 -I -B pos1070/drive.py <cloud-round-trip> unfixed|fixed"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import args, load, verdict

tool, expect = args()
crt = load(tool)
label, osn, keep = "QA-Device", "pixelelated", 2
if hasattr(crt, "kill5_names"):
    own, archive, expected = crt.kill5_names(label, osn, keep)
else:
    own = [f"2026_01_0{d}-000000-{label}-{osn}_SETTINGS.tar.gz" for d in (2, 3, 4)]
    archive = f"2026_02_01-000000-{label}-{osn}_SETTINGS.tar.gz"
    expected = sorted(own[1:] + [archive])
allm = sorted(own + [archive])
correct = allm[-keep:] == expected
hard3 = allm[-3:] == expected
print(f"keep={keep}: a correct retention reads {'PASS' if correct else 'FAIL'}; one hard-coded to 3 reads {'PASS' if hard3 else 'FAIL'}")
observed = "unfixed" if hard3 and not correct else "fixed" if correct and not hard3 else "neither"
verdict("pos1070", expect, observed, f"correct {'passes' if correct else 'fails'}, hard-coded-3 {'passes' if hard3 else 'fails'}")
