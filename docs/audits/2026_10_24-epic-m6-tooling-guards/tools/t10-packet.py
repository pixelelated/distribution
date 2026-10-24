#!/usr/bin/env python3
"""t10-packet.py -- build T10's Phase 4.6 packet: the ask, the first reader's
02/03/04, the 31 files at their read refs (line-numbered), the two rule
sections and ceremonies.md's table from next, and the constructed cases with
their output. Writes <out-dir>/packet-body.md and packet-manifest.json (sha256
of every source). Run from the lane worktree:
  python3 -I docs/audits/2026_10_24-epic-m6-tooling-guards/tools/t10-packet.py <out-dir>
"""
import hashlib, json, os, subprocess, sys
A = "docs/audits/2026_10_24-epic-m6-tooling-guards"
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
def show(ref, path):
    return subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, check=True).stdout
paths = [l.strip() for l in open(".qa-scratch/t10/paths.txt") if l.strip()]
assert len(paths) == 31, len(paths)
first = ["tools/forbidden-terms-check", "tools/fork-worktree"]
order = [".githooks/pre-push", ".githooks/guard-lib", ".githooks/secret-patterns", ".githooks/pre-commit", ".githooks/commit-msg", ".githooks/hooks-test"] + first
order += [p for p in paths if p not in order]
assert sorted(order) == sorted(paths)
man = {"sources": [], "built_by": f"{A}/tools/t10-packet.py"}
parts = []
for name in ("02-forward-audit.md", "03-retrospective.md", "04-analysis.md"):
    b = open(os.path.join(A, name), "rb").read()
    man["sources"].append({"path": f"{A}/{name}", "ref": "worktree", "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    parts.append(f"\n\n## The first reader's {name} (whole)\n\n" + b.decode())
rule = show("next", ".claude/rules/fork-workflow.md").decode()
pa, pb = rule.index("**Personal paths**"), rule.index("## Per-feature flow")
sa = rule.index("## Safety net"); sb = rule.index("## When to merge up")
cer = show("next", ".claude/rules/ceremonies.md").decode()
ca = cer.index("| Ceremony |"); cb = cer.index("The split is deliberate")
for label, text in (("fork-workflow.md § Personal paths (next)", rule[pa:pb]), ("fork-workflow.md § Safety net (next)", rule[sa:sb]), ("ceremonies.md's table (next)", cer[ca:cb])):
    man["sources"].append({"path": label, "ref": "next", "sha256": hashlib.sha256(text.encode()).hexdigest(), "bytes": len(text.encode())})
    parts.append(f"\n\n## Context: {label}\n\n{text}")
for p in order:
    ref = "2174265e9c" if p.startswith("tools/renovation-") else "8ebaf8daad"
    b = show(ref, p)
    man["sources"].append({"path": p, "ref": ref, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    numbered = "\n".join(f"{i:5d}  {l}" for i, l in enumerate(b.decode().splitlines(), 1))
    parts.append(f"\n\n## File: {p} (at {ref}, {len(b.splitlines())} lines)\n\n```text\n{numbered}\n```")
for p in (f"{A}/tools/t10-guard-gaps.sh", "/workspace/tmp/m6-t10/gaps-hash.txt"):
    b = open(p, "rb").read()
    man["sources"].append({"path": p, "ref": "worktree" if p.startswith("docs/") else "run output 16:36:51Z", "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    parts.append(f"\n\n## The constructed cases: {os.path.basename(p)}\n\n```text\n{b.decode()}\n```")
body = "".join(parts)
open(os.path.join(out, "packet-body.md"), "w").write(body)
man["packet_body_sha256"] = hashlib.sha256(body.encode()).hexdigest(); man["packet_body_bytes"] = len(body.encode())
man["files_31"] = sum(1 for s in man["sources"] if s["path"] in paths)
json.dump(man, open(os.path.join(out, "packet-manifest.json"), "w"), indent=2)
print("sources", len(man["sources"]), "of which the 31:", man["files_31"], "body bytes", man["packet_body_bytes"])
