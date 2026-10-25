#!/usr/bin/env python3
"""t15-packet2.py -- the second packet the seat asked for under `## Sections I
need` (gpt-audit.md): the line ranges it named, at 8ebaf8daad, line-numbered,
plus the two callee tools F-07 turns on, settings-modes-test and
melonds-upgrade-test, at 8ebaf8daad (this file's read hash) and at 7c1d729b57
(T14's fixed tip, whose S8 contract is the one F-07 names), whole.
  python3 -I docs/audits/2026_10_25-epic-m6-tooling-last-good-test/tools/t15-packet2.py <out-dir>
"""
import hashlib, json, os, subprocess, sys
REF = "8ebaf8daad"; FILE = "tools/last-good-scripts-test"
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
def show(ref, path):
    return subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, check=True).stdout
lines = show(REF, FILE).decode().split("\n")
asked = [("F-08: x/C's applicability gate", 4540, 4565), ("F-08: aa's head", 13723, 13740), ("F-08: aa's tail", 13890, 13912),
         ("F-09: x/F2", 3990, 4015), ("F-09: x/F2", 4290, 4310), ("F-09: x/C", 6475, 6495), ("F-09: x/D (DT_OK and its guarded branches)", 6635, 7795),
         ("F-09: y/A", 10120, 10365), ("F-09: y/F1r", 11170, 11205),
         ("F-17: g to i", 839, 933), ("F-17: t", 2410, 2445), ("F-17: x/C7", 6495, 6525),
         ("F-19: z/S3F", 13665, 13722), ("F-21: z", 13390, 13430)]
man = {"built_by": "t15-packet2.py", "file": FILE, "ref": REF, "excerpts": [], "external": []}
parts = []
for label, a, b in asked:
    seg = lines[a-1:b]; text = "\n".join(seg)
    man["excerpts"].append({"label": label, "from": a, "to": b, "sha256": hashlib.sha256(text.encode()).hexdigest()})
    parts.append(f"\n\n## Excerpt: {label} (`:{a}-{b}` at {REF})\n\n```text\n" + "\n".join(f"{i:5d}  {l}" for i, l in enumerate(seg, a)) + "\n```")
for tool in ("tools/settings-modes-test", "tools/melonds-upgrade-test"):
    for ref in (REF, "7c1d729b57"):
        b = show(ref, tool)
        man["external"].append({"path": tool, "ref": ref, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
        parts.append(f"\n\n## External: {tool} at {ref} (whole)\n\n```text\n" + "\n".join(f"{i:5d}  {l}" for i, l in enumerate(b.decode().splitlines(), 1)) + "\n```")
body = "".join(parts)
open(os.path.join(out, "packet2-body.md"), "w").write(body)
man["body_sha256"] = hashlib.sha256(body.encode()).hexdigest(); man["body_bytes"] = len(body.encode())
man["excerpt_lines"] = sum(e["to"] - e["from"] + 1 for e in man["excerpts"])
json.dump(man, open(os.path.join(out, "packet2-manifest.json"), "w"), indent=2)
print("excerpts", len(man["excerpts"]), "lines", man["excerpt_lines"], "; external", len(man["external"]), "; body bytes", man["body_bytes"])
