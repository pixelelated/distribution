#!/usr/bin/env python3
"""t22-packet.py -- build T22's Phase 4.6 packet (D-WORKFLOW-195, the brief § 1):
the first reader's 02/03/04 whole; the context sections (the order's § T22,
the brief's § 2 and § 4, the register rows the brief names); and the files
under review at 8ebaf8daad, line-numbered: the 29 units whole,
/usr/bin/autostart and profile.d/002-autostart, userconfig-setup, the
system-utils and quirks recipes, the busybox recipe and the flagged lines of
busybox-target.conf, scripts/init whole, the fork-own 24 -- and three slice
files the findings rest on (busybox/config/profile, udevil.conf's option
lines, 098-deviceutils). Writes <out-dir>/packet-body.md and
<out-dir>/packet-manifest.json (the sha256 of every source).
Run from the lane worktree:
  python3 -I docs/audits/2026_10_25-epic-m6-os-system-services/tools/t22-packet.py <out-dir>
"""
import hashlib, json, os, re, subprocess, sys
A = "docs/audits/2026_10_25-epic-m6-os-system-services"
REF = "8ebaf8daad"
P = "projects/ROCKNIX/packages/"
out = sys.argv[1]; os.makedirs(out, exist_ok=True)


def show(path):
    return subprocess.run(["git", "show", f"{REF}:{path}"], capture_output=True, check=True).stdout


paths = [l.strip() for l in open(".qa-scratch/t22/paths.txt") if l.strip()]
rows = {r["path"]: r for r in json.load(open(".qa-scratch/t22/rows.json"))}
units = [p for p in paths if re.search(r"\.(service|timer|socket|target|mount|path)$", p)]
if len(units) != 29:
    sys.exit(f"expected 29 units, got {len(units)}")
fork_own = [p for p in paths if rows[p]["tier"] == "fork-own"]
if len(fork_own) != 24:
    sys.exit(f"expected 24 fork-own paths, got {len(fork_own)}")
named = [P + n for n in ("sysutils/autostart/sources/autostart", "sysutils/autostart/profile.d/002-autostart",
                         "sysutils/systemd/scripts/userconfig-setup", "sysutils/system-utils/package.mk",
                         "hardware/quirks/package.mk", "sysutils/busybox/package.mk", "sysutils/busybox/scripts/init",
                         "sysutils/busybox/config/profile",
                         "sysutils/system-utils/sources/autostart/common/098-deviceutils")]
whole = []
for p in named + units + fork_own:
    if p not in whole:
        whole.append(p)
missing = [p for p in whole if p not in paths]
if missing:
    sys.exit(f"not in the 422: {missing}")
# excerpts: (path, [(first, last)], why)
EXCERPTS = [(P + "sysutils/busybox/config/busybox-target.conf", [(28, 32), (547, 558), (886, 896), (948, 952), (1008, 1012)],
             "the flagged lines (SUID, LOGIN, PASSWD, SU, HTTPD, CGI, NC, UDHCPD), not its 1,224 lines"),
            (P + "sysutils/udevil/config/udevil.conf", [(200, 245)], "the default and allowed options (F-04)")]

man = {"sources": [], "built_by": f"{A}/tools/t22-packet.py", "added_beyond_the_brief_list": [
    P + "sysutils/busybox/config/profile", P + "sysutils/system-utils/sources/autostart/common/098-deviceutils",
    P + "sysutils/udevil/config/udevil.conf (lines 200-245)"], "redactions": []}
parts = []
for name in ("02-forward-audit.md", "03-retrospective.md", "04-analysis.md"):
    b = open(os.path.join(A, name), "rb").read()
    man["sources"].append({"path": f"{A}/{name}", "ref": "worktree", "kind": "first reader", "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    parts.append(f"\n\n## The first reader's {name} (whole)\n\n" + b.decode())


def section(text, start, stop_re=r"\n#{1,3} "):
    i = text.index(start)
    m = re.compile(stop_re).search(text, i + len(start))
    return text[i:m.start() if m else len(text)]


order = open("docs/reviews/order.md", encoding="utf-8").read()
brief = open("docs/reviews/briefs/os-system-services.md", encoding="utf-8").read()
reg = open("docs/decision-register.md", encoding="utf-8").read()
ids = ["D-WORKFLOW-184", "D-SYS-002", "D-SYS-003", "D-SYS-006", "D-SYS-008", "D-SYS-009"] + \
      [f"D-NET-00{i}" for i in (1, 2, 3, 4, 5, 6, 9)] + \
      [f"D-CLOUD-{i:03d}" for i in (64, 72, 78, 79, 80, 82, 147)] + \
      ["D-INFRA-011", "D-INFRA-012", "D-INFRA-013", "D-QA-042", "D-QA-053", "D-QA-063", "D-UI-121",
       "D-WORKFLOW-083", "D-WORKFLOW-195", "D-WORKFLOW-209"]
rowsel = [l for l in reg.splitlines() if any(l.startswith(f"| {i} |") for i in ids)]
found = {i for i in ids if any(l.startswith(f"| {i} |") for l in rowsel)}
contexts = (("docs/reviews/order.md § T22", section(order, "### T22.", r"\n### T23\.")),
            ("the brief § 2 Scope", section(brief, "## 2. Scope", r"\n## 3\. ")),
            ("the brief § 4 The questions", section(brief, "## 4. The questions", r"\n## 5\. ")),
            ("docs/decision-register.md: the rows the brief names (" + ", ".join(sorted(found)) + ")", "\n".join(rowsel)))
man["register_rows_missing"] = sorted(set(ids) - found)
for label, text in contexts:
    man["sources"].append({"path": label, "ref": "worktree", "kind": "context", "sha256": hashlib.sha256(text.encode()).hexdigest(), "bytes": len(text.encode())})
    parts.append(f"\n\n## Context: {label}\n\n{text}")
for p in whole:
    b = show(p)
    man["sources"].append({"path": p, "ref": REF, "kind": "file under review", "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    lines = b.decode(errors="replace").splitlines()
    numbered = "\n".join(f"{i:5d}  {l}" for i, l in enumerate(lines, 1))
    parts.append(f"\n\n## File: {p[len(P):]} (at {REF}, {len(lines)} lines)\n\n```text\n{numbered}\n```")
for p, spans, why in EXCERPTS:
    b = show(p)
    lines = b.decode().splitlines()
    man["sources"].append({"path": p, "ref": REF, "kind": "excerpt", "lines": [list(s) for s in spans], "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    chunks = ["\n".join(f"{i:5d}  {lines[i - 1]}" for i in range(a, b2 + 1)) for a, b2 in spans]
    parts.append(f"\n\n## Excerpt: {p[len(P):]} (at {REF}; {why})\n\n```text\n" + "\n  ...\n".join(chunks) + "\n```")
body = "".join(parts)
open(os.path.join(out, "packet-body.md"), "w").write(body)
man["packet_body_sha256"] = hashlib.sha256(body.encode()).hexdigest(); man["packet_body_bytes"] = len(body.encode())
man["files_whole"] = len(whole); man["excerpts"] = len(EXCERPTS)
json.dump(man, open(os.path.join(out, "packet-manifest.json"), "w"), indent=2)
print(f"files whole {len(whole)}, excerpts {len(EXCERPTS)}, contexts {len(contexts)}, body {len(body.encode())} bytes, register rows {len(found)}/{len(ids)}")
