#!/usr/bin/env python3
"""t14-packet.py -- build T14's Phase 4.6 packet: the first reader's 02/03/04
whole, the two rule sections from next (engineering-practices.md § Guards must
fail closed; upgrade-and-install.md § Verify on a device, not on the host), the
32 files at their read refs (line-numbered), and the stage-A run lines. Writes
<out-dir>/packet-body.md and packet-manifest.json (sha256 of every source).
Run from the lane worktree:
  python3 -I docs/audits/2026_10_24-epic-m6-tooling-state-tests/tools/t14-packet.py <out-dir>
"""
import hashlib, json, os, subprocess, sys
A = "docs/audits/2026_10_24-epic-m6-tooling-state-tests"
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
def show(ref, path):
    return subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, check=True).stdout
paths = [l.strip() for l in open(".qa-scratch/t14/paths.txt") if l.strip()]
if len(paths) != 32:
    sys.exit("expected 32 paths, got %d" % len(paths))
first = ["tools/rasteratops-cloud-layout-test", "tools/pixelelated-cloud-validator-test", "tools/pixelelated-content-scope-test",
         "tools/pixelelated-save-layout-test", "tools/pixelelated-vm-cloud-boundaries", "tools/rasteratops-vm-cloud-epic",
         "tools/pixelelated-state-check", "tools/settings-modes-test", "tools/melonds-upgrade-test"]
order = first + [p for p in paths if p not in first]
if sorted(order) != sorted(paths):
    sys.exit("the ordering lost or added a path")
man = {"sources": [], "built_by": f"{A}/tools/t14-packet.py"}
parts = []
for name in ("02-forward-audit.md", "03-retrospective.md", "04-analysis.md"):
    b = open(os.path.join(A, name), "rb").read()
    man["sources"].append({"path": f"{A}/{name}", "ref": "worktree", "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    parts.append(f"\n\n## The first reader's {name} (whole)\n\n" + b.decode())
ep = show("next", ".claude/rules/engineering-practices.md").decode()
ea, eb = ep.index("## Guards must fail closed"), ep.index("## Before deleting a duplicate")
ui = show("next", ".claude/rules/upgrade-and-install.md").decode()
ua = ui.index("## Verify on a device, not on the host"); ub = ui.find("\n## ", ua + 5); ub = len(ui) if ub < 0 else ub
for label, text in (("engineering-practices.md § Guards must fail closed (next)", ep[ea:eb]),
                    ("upgrade-and-install.md § Verify on a device, not on the host (next)", ui[ua:ub])):
    man["sources"].append({"path": label, "ref": "next", "sha256": hashlib.sha256(text.encode()).hexdigest(), "bytes": len(text.encode())})
    parts.append(f"\n\n## Context: {label}\n\n{text}")
for p in order:
    ref = "2174265e9c" if p.startswith("tools/test-fixtures/lint-audit-artifacts/") else "8ebaf8daad"
    b = show(ref, p)
    man["sources"].append({"path": p, "ref": ref, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    numbered = "\n".join(f"{i:5d}  {l}" for i, l in enumerate(b.decode().splitlines(), 1))
    parts.append(f"\n\n## File: {p} (at {ref}, {len(b.splitlines())} lines)\n\n```text\n{numbered}\n```")
runs = ".qa-scratch/t14/runs.txt"
b = open(runs, "rb").read()
man["sources"].append({"path": runs, "ref": "stage-A run lines", "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
parts.append(f"\n\n## The stage-A run lines (exit, wall, last line)\n\n```text\n{b.decode()}\n```")
body = "".join(parts)
open(os.path.join(out, "packet-body.md"), "w").write(body)
man["packet_body_sha256"] = hashlib.sha256(body.encode()).hexdigest(); man["packet_body_bytes"] = len(body.encode())
man["files_32"] = sum(1 for s in man["sources"] if s["path"] in paths)
man["files_32_bytes"] = sum(s["bytes"] for s in man["sources"] if s["path"] in paths)
json.dump(man, open(os.path.join(out, "packet-manifest.json"), "w"), indent=2)
print("sources", len(man["sources"]), "of which the 32:", man["files_32"], man["files_32_bytes"], "bytes; body bytes", man["packet_body_bytes"])
