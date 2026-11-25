#!/usr/bin/env python3
"""Read-only: group open unplaced bugs by the issue or audit their body says filed them."""
import json
import re
import sys
from collections import defaultdict

d = json.load(open(sys.argv[1]))
groups = defaultdict(list)
how = {}
for x in d:
    body = x.get("body") or ""
    head = body[:2500]
    n = x["number"]
    m = (re.search(r"(?i)\b(?:from|found (?:in|by|during|while)|raised (?:in|by)|follow-?up (?:to|from|of)|filed (?:from|under|by)|discovered (?:in|by|during)|source(?:d)? from|review(?:ed)? in|audit)\D{0,40}#(\d{2,4})", head)
         or re.search(r"(?i)(?:parent|epic|origin|related)\W{0,4}#(\d{2,4})", head))
    if m:
        key = "#" + m.group(1)
        how[n] = "phrase"
    else:
        refs = [r for r in re.findall(r"#(\d{2,4})\b", head) if int(r) != n]
        if refs:
            key = "#" + refs[0]
            how[n] = "first-ref"
        else:
            key = "none"
            how[n] = "none"
    groups[key].append(n)

out = {"total": len(d), "groups": {k: sorted(v) for k, v in sorted(groups.items(), key=lambda kv: -len(kv[1]))},
       "how": how}
json.dump(out, open(sys.argv[2], "w"), indent=1)
for k, v in list(out["groups"].items())[:40]:
    print(f"{k}\t{len(v)}\t{v[:12]}")
print("phrase", sum(1 for v in how.values() if v == "phrase"), "first-ref",
      sum(1 for v in how.values() if v == "first-ref"), "none", sum(1 for v in how.values() if v == "none"))
