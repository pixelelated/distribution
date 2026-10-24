#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""write-completion.py -- the audit's completion marker, from the closed
punch-list issue read back from the tracker (M6 T14, #661; copied from T10's at 7182f743ea, itself T3's at 5f737500ce; ceremonies.md's
completed-audit marker, validated by tools/ceremony-check's
completed_audit_marker).

    python3 -I write-completion.py <tree> <audit-dir> <issue>

Refuses unless the issue reads closed, completed, with every checkbox ticked
and at least one. Writes tracker-final-readback.json (the issue as the API
returns it), tracker-completion.json (the verified time) and
audit-completion.json (both hash-bound with 04 and 05).
"""
import datetime as dt, hashlib, json, os, re, subprocess, sys

tree, audit, issue = sys.argv[1], sys.argv[2], int(sys.argv[3])
raw = subprocess.run(["gh", "api", f"repos/pixelelated/distribution/issues/{issue}"],
                     capture_output=True, text=True, check=True).stdout
data = json.loads(raw)
body = data.get("body") or ""
if data.get("state") != "closed" or data.get("state_reason") != "completed":
    sys.exit(f"refusing: #{issue} is {data.get('state')}/{data.get('state_reason')}, not closed/completed")
if not re.search(r"^\s*- \[x\]", body, re.M) or re.search(r"^\s*- \[ \]", body, re.M):
    sys.exit(f"refusing: #{issue} has an open checkbox or none ticked")
verified = dt.datetime.now(dt.timezone.utc).isoformat()
rel = lambda name: os.path.relpath(os.path.join(audit, name), tree)
with open(os.path.join(audit, "tracker-final-readback.json"), "w") as f:
    f.write(raw if raw.endswith("\n") else raw + "\n")
with open(os.path.join(audit, "tracker-completion.json"), "w") as f:
    json.dump({"result": "PASS", "exact_bodies_and_states": True, "closed_completed": [issue],
               "verified_utc": verified}, f, indent=2)
    f.write("\n")
def sha(name):
    with open(os.path.join(tree, name), "rb") as s:
        return hashlib.sha256(s.read()).hexdigest()
names = [rel(n) for n in ("04-analysis.md", "05-punch-list.md", "tracker-final-readback.json", "tracker-completion.json")]
marker = {"schema": 1, "issue": issue, "completed_at": verified,
          "tracker_readback": rel("tracker-final-readback.json"),
          "tracker_completion": rel("tracker-completion.json"),
          "evidence": {n: sha(n) for n in names}}
with open(os.path.join(audit, "audit-completion.json"), "w") as f:
    json.dump(marker, f, indent=2)
    f.write("\n")
print(f"write-completion: #{issue} closed/completed, {body.count('- [x]')} ticked; verified {verified}")
