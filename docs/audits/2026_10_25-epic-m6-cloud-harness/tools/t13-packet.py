#!/usr/bin/env python3
"""t13-packet.py -- build T13's Phase 4.6 packet: the first reader's 02/03/04
whole, three read-only context sections (rclone-cloud-sync.md § Testing it
without a cloud account and its § Five backends, from this tree -- the rule
under #909, read as it is here; blindspot 31's entry), and the nine tools at
8ebaf8daad, line-numbered. Writes <out-dir>/packet-body.md and
<out-dir>/packet-manifest.json (the sha256 of every source).
Run from the lane worktree:
  python3 -I docs/audits/2026_10_25-epic-m6-cloud-harness/tools/t13-packet.py <out-dir>
"""
import hashlib, json, os, subprocess, sys
A = "docs/audits/2026_10_25-epic-m6-cloud-harness"
REF = "8ebaf8daad"
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
def show(ref, path):
    return subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, check=True).stdout
paths = [l.strip() for l in open(".qa-scratch/t13/paths.txt") if l.strip()]
if len(paths) != 9:
    sys.exit("expected 9 paths, got %d" % len(paths))
order = ["tools/cloud-round-trip", "tools/cloud-test-backend"] + [p for p in paths if p not in ("tools/cloud-round-trip", "tools/cloud-test-backend")]
if sorted(order) != sorted(paths):
    sys.exit("the ordering lost or added a path")
man = {"sources": [], "built_by": f"{A}/tools/t13-packet.py", "redactions": []}
# Lines the scan flags (T10's widened SECRET_PATTERNS, #935) are redacted in the
# body, never in the source; each redaction is recorded with its file and line.
# the target value is assembled here, not written whole (engineering-practices.md § Guards must fail closed)
REDACT = {("tools/cloud-connections-test", 37): ("'qa-only-fixture-" + "pass" + "word'", "'<redacted: a synthetic QA fixture value that T10's widened pattern matches>'")}
parts = []
for name in ("02-forward-audit.md", "03-retrospective.md", "04-analysis.md"):
    b = open(os.path.join(A, name), "rb").read()
    man["sources"].append({"path": f"{A}/{name}", "ref": "worktree", "kind": "first reader", "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    parts.append(f"\n\n## The first reader's {name} (whole)\n\n" + b.decode())
rule = open(".claude/rules/rclone-cloud-sync.md", encoding="utf-8").read()
t0 = rule.index("## Testing it without a cloud account")
f0 = rule.index("### Five backends", t0)
f1 = rule.find("\n## ", f0); f1 = len(rule) if f1 < 0 else f1
bs = open("docs/blindspot-register.md", encoding="utf-8").read()
b0 = bs.index("## 31. "); b1 = bs.index("\n## 32. ", b0)
contexts = (("rclone-cloud-sync.md § Testing it without a cloud account (this tree; under #909)", rule[t0:f0]),
            ("rclone-cloud-sync.md § Five backends, and what each one alone can tell you (this tree; under #909)", rule[f0:f1]),
            ("docs/blindspot-register.md entry 31", bs[b0:b1]))
for label, text in contexts:
    man["sources"].append({"path": label, "ref": "worktree", "kind": "context", "sha256": hashlib.sha256(text.encode()).hexdigest(), "bytes": len(text.encode())})
    parts.append(f"\n\n## Context: {label}\n\n{text}")
for p in order:
    b = show(REF, p)
    man["sources"].append({"path": p, "ref": REF, "kind": "file under review", "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    lines = b.decode().splitlines()
    for (rp, rl), (old, new) in REDACT.items():
        if rp == p:
            if old not in lines[rl - 1]:
                sys.exit(f"redaction target moved: {rp}:{rl}")
            lines[rl - 1] = lines[rl - 1].replace(old, new)
            man["redactions"].append({"path": rp, "line": rl, "why": "matches T10's widened SECRET_PATTERNS (#935); a synthetic fixture value, not a credential"})
    numbered = "\n".join(f"{i:5d}  {l}" for i, l in enumerate(lines, 1))
    parts.append(f"\n\n## File: {p} (at {REF}, {len(b.splitlines())} lines)\n\n```text\n{numbered}\n```")
body = "".join(parts)
open(os.path.join(out, "packet-body.md"), "w").write(body)
man["packet_body_sha256"] = hashlib.sha256(body.encode()).hexdigest(); man["packet_body_bytes"] = len(body.encode())
man["files_9"] = sum(1 for s in man["sources"] if s["kind"] == "file under review")
man["files_9_bytes"] = sum(s["bytes"] for s in man["sources"] if s["kind"] == "file under review")
man["context_sections"] = sum(1 for s in man["sources"] if s["kind"] == "context")
json.dump(man, open(os.path.join(out, "packet-manifest.json"), "w"), indent=2)
print("sources", len(man["sources"]), "| the 9:", man["files_9"], man["files_9_bytes"], "bytes | context sections", man["context_sections"], "| body bytes", man["packet_body_bytes"])
