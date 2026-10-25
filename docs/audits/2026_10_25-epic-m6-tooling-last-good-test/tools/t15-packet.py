#!/usr/bin/env python3
"""t15-packet.py -- build T15's Phase 4.6 packet of excerpts. The file is
1,167,697 bytes, too large to send whole, so the packet carries, per the
brief's § 1:
  - the section index (the 34 echo lines with their numbers) and the 15 groups;
  - the harness (:1-430: the header, the dispatch, check/skip/src_of,
    image_tool_source, the busybox copy and its wrappers);
  - the history helpers (f1_tree_at and its callers, :3198-3330) and :4255-4290;
  - stream A's setup and the sandbox helpers (:8895-9032);
  - the call sites and the verdict (:14177-14239);
  - and the sections the first reader's Q3 names as suspect, each whole:
    a (:429-517), b (:518-606), q (:1752-1859), t's patch block and verdict
    reading (:2033-2100, :2840-2856), v (:2991-3066), y4 (:8684-8905) and
    aa's two-argument check (:13818-13832);
plus the first reader's 02, 03 and 04 whole and the two rule sections from
next. Every excerpt is line-numbered at 8ebaf8daad and hashed in the
manifest, beside the whole file's sha256.
  python3 -I docs/audits/2026_10_25-epic-m6-tooling-last-good-test/tools/t15-packet.py <out-dir>
"""
import hashlib, json, os, re, subprocess, sys
A = "docs/audits/2026_10_25-epic-m6-tooling-last-good-test"
REF = "8ebaf8daad"; FILE = "tools/last-good-scripts-test"
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
def show(ref, path):
    return subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, check=True).stdout
whole = show(REF, FILE); lines = whole.decode().split("\n")
assert len(whole) == 1167697, len(whole)
ranges = [("the harness: header, dispatch, check/skip/src_of, image_tool_source, the busybox copy", 1, 430),
          ("a", 429, 517), ("b", 518, 606), ("q", 1752, 1859),
          ("t: the client, its patches and the compile message", 2033, 2100),
          ("t: the verdict reading", 2840, 2856), ("v", 2991, 3066),
          ("x/F1.: the history helpers and the first F1 checks", 3198, 3330),
          ("x/F2: the mupen64plus repair read from 417dcd8610", 4255, 4290),
          ("y4", 8684, 8905),
          ("y/A.: stream A's rclone, shims, nbin wrappers and the sandbox helpers", 8895, 9032),
          ("aa: the two-argument check", 13818, 13832),
          ("the call sites (ae, af, ag, ah) and the verdict", 14177, 14239)]
man = {"built_by": f"{A}/tools/t15-packet.py", "file": FILE, "ref": REF,
       "file_sha256": hashlib.sha256(whole).hexdigest(), "file_bytes": len(whole), "file_lines": len(lines) - 1,
       "excerpts": [], "sources": []}
parts = ["\n\n## The section index (every `echo \"  <letter>. \"` line, at 8ebaf8daad)\n\n```text\n"]
idx = [f"{i:5d}  {l}" for i, l in enumerate(lines, 1) if re.match(r'^echo "  [a-z]{1,2}\. ', l)]
grp = [f"{i:5d}  {l}" for i, l in enumerate(lines, 1) if re.match(r'^\s*echo "  [A-Z][A-Za-z0-9]*\. ', l) or re.match(r'^# y[1-4]\. ', l)]
parts.append("\n".join(idx) + "\n```\n\nThe groups inside x, y and z (echoed, or comment-headed):\n\n```text\n" + "\n".join(grp) + "\n```")
for label, a, b in ranges:
    seg = lines[a-1:b]
    text = "\n".join(seg)
    man["excerpts"].append({"label": label, "from": a, "to": b, "sha256": hashlib.sha256(text.encode()).hexdigest()})
    numbered = "\n".join(f"{i:5d}  {l}" for i, l in enumerate(seg, a))
    parts.append(f"\n\n## Excerpt: {label} (`:{a}-{b}` at {REF})\n\n```text\n{numbered}\n```")
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
body = "".join(parts)
open(os.path.join(out, "packet-body.md"), "w").write(body)
man["packet_body_sha256"] = hashlib.sha256(body.encode()).hexdigest(); man["packet_body_bytes"] = len(body.encode())
man["excerpt_lines"] = sum(e["to"] - e["from"] + 1 for e in man["excerpts"])
json.dump(man, open(os.path.join(out, "packet-manifest.json"), "w"), indent=2)
print("excerpts", len(man["excerpts"]), "lines", man["excerpt_lines"], "; body bytes", man["packet_body_bytes"])
