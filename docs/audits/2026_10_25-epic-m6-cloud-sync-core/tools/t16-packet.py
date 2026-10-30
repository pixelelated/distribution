#!/usr/bin/env python3
"""t16-packet.py -- build T16's Phase 4.6 packet, trimmed as D-WORKFLOW-195 says from the start
(the brief § 1: "a trimmed, scanned packet"): the first reader's 02/03/04 whole; the context
(the order's § T16, the brief's § 4, the register rows the brief names, es-player-text.md's
outcome vocabulary); the eleven smaller files under review whole, line-numbered; the three big
scripts (cloud_backup, cloud_restore, cloud_capture: 6,538 lines) as line-numbered excerpts
around every line 02 and 04 cite, with CONTEXT lines either side (a citation of MAX_SPAN lines or more is a function's
range in 02's tables and is not one), plus each script's head, its trap and its main, and the
capture's five cited regions by hand (02 and 04 cite them as bare ":136" after "the capture"); the evidence the findings rest on (the two fixtures, the host leads' records,
KILL2's and KILL15's guest lines, the harness's fx_kill15). Writes <out-dir>/packet-body.md and
<out-dir>/packet-manifest.json (the sha256 of every source; the excerpted spans).
Run from the lane worktree:
  python3 -I docs/audits/2026_10_25-epic-m6-cloud-sync-core/tools/t16-packet.py <out-dir>
"""
import hashlib, json, os, re, subprocess, sys
A = "docs/audits/2026_10_25-epic-m6-cloud-sync-core"
REF = "8ebaf8daad"
HREF = "3a653eaec4"          # the harness T13 fixed, the guest window's
R = "projects/ROCKNIX/packages/network/rclone/"
CONTEXT = 8
out = sys.argv[1]; os.makedirs(out, exist_ok=True)


def show(ref, path):
    return subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, check=True).stdout


def numbered(lines, a, b):
    return "\n".join(f"{i:5d}  {lines[i - 1]}" for i in range(a, b + 1))


WHOLE = ["autostart/102-cloud-saves", "package.mk", "sources/cloud_net_ready", "sources/cloud_saves_root",
         "sources/cloud_sync_helper", "sources/cloud_sync_cleanup_duplicates.sh",
         "sources/rasteratops-settings-archive", "sources/cloud_sync.conf", "sources/cloud_sync.conf.defaults",
         "sources/cloud_sync-rules.txt", "sources/cloud_sync-rules.txt.defaults"]
BIG = {"cloud_backup": "sources/cloud_backup", "cloud_restore": "sources/cloud_restore",
       "cloud_capture": "sources/cloud_capture"}
# Always shown: each script's head (its constants and exits), its traps, and the twins' main.
ALWAYS = {"cloud_backup": [(1, 120), (357, 385), (2490, 2510)], "cloud_restore": [(1, 160), (238, 380), (2207, 2324)],
          "cloud_capture": [(1, 140), (185, 200), (765, 805), (1075, 1090), (1640, 1690)]}
# A citation longer than this is a function's whole range (02 § The functions), not a cited line.
MAX_SPAN = 40

man = {"sources": [], "built_by": f"{A}/tools/t16-packet.py", "context_lines": CONTEXT, "redactions": []}
parts = []


def add_source(path, ref, kind, b, **extra):
    man["sources"].append(dict(path=path, ref=ref, kind=kind, sha256=hashlib.sha256(b).hexdigest(), bytes=len(b), **extra))


# 1. The first reader, whole; and the cited lines of the three big scripts, read from 02 and 04.
cited = {k: set() for k in BIG}
for name in ("02-forward-audit.md", "03-retrospective.md", "04-analysis.md"):
    b = open(os.path.join(A, name), "rb").read()
    add_source(f"{A}/{name}", "worktree", "first reader", b)
    parts.append(f"\n\n## The first reader's {name} (whole)\n\n" + b.decode())
    if name == "03-retrospective.md":
        continue
    skip = False
    for line in b.decode().splitlines():
        if line.startswith("## "):
            skip = line.startswith(("## The functions", "## The oracle", "## Coverage"))
        if skip:
            continue
        cur = None
        for m in re.finditer(r"(?:(cloud_backup|cloud_restore|cloud_capture)|(?<![\w./-])):(\d+)(?:-(\d+))?((?:,\s*\d+(?:-\d+)?)*)", line):
            if m.group(1):
                cur = m.group(1)
            if not cur:
                continue
            spans = [(int(m.group(2)), int(m.group(3) or m.group(2)))]
            for extra in re.findall(r"(\d+)(?:-(\d+))?", m.group(4) or ""):
                spans.append((int(extra[0]), int(extra[1] or extra[0])))
            for a, z in spans:
                if 0 < a <= z and z - a < MAX_SPAN:
                    cited[cur].add((a, z))

# 2. The context.
def section(text, start, stop_re):
    i = text.index(start)
    m = re.compile(stop_re).search(text, i + len(start))
    return text[i:m.start() if m else len(text)]


order = open("docs/reviews/order.md", encoding="utf-8").read()
brief = open("docs/reviews/briefs/cloud-sync-core.md", encoding="utf-8").read()
reg = open("docs/decision-register.md", encoding="utf-8").read()
rule = open(".claude/rules/es-player-text.md", encoding="utf-8").read()
ids = sorted(set(re.findall(r"D-[A-Z]+-\d{3}", section(brief, "## 1. Identity", r"\n## 5\. "))))
rowsel = [l for l in reg.splitlines() if any(l.startswith(f"| {i} |") for i in ids)]
found = sorted({i for i in ids if any(l.startswith(f"| {i} |") for l in rowsel)})
contexts = (("docs/reviews/order.md § T16", section(order, "### T16.", r"\n### T17\.")),
            ("the brief § 4 The questions", section(brief, "## 4. The questions", r"\n## 5\. ")),
            (".claude/rules/es-player-text.md § Outcome vocabulary (D-UI-028)", section(rule, "## Outcome vocabulary (D-UI-028)", r"\n## Anti-patterns")),
            ("docs/decision-register.md: the rows the brief's §§ 1-4 name (" + ", ".join(found) + ")", "\n".join(rowsel)))
man["register_rows_missing"] = sorted(set(ids) - set(found))
for label, text in contexts:
    add_source(label, "worktree", "context", text.encode())
    parts.append(f"\n\n## Context: {label}\n\n{text}")

# 3. The files under review: the eleven whole, the three in excerpt.
for f in WHOLE:
    b = show(REF, R + f)
    lines = b.decode(errors="replace").splitlines()
    add_source(R + f, REF, "file under review, whole", b)
    parts.append(f"\n\n## File: {f} (at {REF}, {len(lines)} lines, whole)\n\n```text\n{numbered(lines, 1, len(lines))}\n```")
for key, f in BIG.items():
    b = show(REF, R + f)
    lines = b.decode(errors="replace").splitlines()
    n = len(lines)
    want = sorted({(max(1, a - CONTEXT), min(n, z + CONTEXT)) for a, z in cited[key] if a <= n} | set(ALWAYS[key]))
    merged = []
    for a, z in want:
        if merged and a <= merged[-1][1] + 3:
            merged[-1][1] = max(merged[-1][1], z)
        else:
            merged.append([a, z])
    shown = sum(z - a + 1 for a, z in merged)
    add_source(R + f, REF, "file under review, excerpt", b, spans=merged, lines_shown=shown, lines_total=n)
    chunks = [numbered(lines, a, z) for a, z in merged]
    parts.append(f"\n\n## Excerpt: {f} (at {REF}; {shown} of {n} lines: every line 02 and 04 cite, "
                 f"{CONTEXT} lines either side, the head, the traps and main; a gap is marked ...)\n\n```text\n"
                 + "\n  ...\n".join(chunks) + "\n```")

# 4. The evidence the findings rest on.
EVID = [(f"{A}/fixtures/load-config-fallback.sh", "F-01's fixture"), (f"{A}/fixtures/trap-defer.sh", "F-03's fixture")]
for d in ("a-awk", "b-empty-savespath", "d-terminal-width", "f14-backup-dir-order", "k15-at-the-run"):
    EVID.append((f"{A}/guest-cycle/host-leads/{d}/out", f"host lead {d}"))
EVID += [(f"{A}/guest-cycle/host-leads/e-term-automatic/out", "host lead e, the term and termkill arms"),
         (f"{A}/guest-cycle/host-leads/e-term-automatic/out-game", "host lead e, the termkill-game arm")]
for p, why in EVID:
    b = open(p, "rb").read()
    add_source(p, "worktree", "evidence", b)
    parts.append(f"\n\n## Evidence: {p[len(A) + 1:]} ({why})\n\n```text\n{b.decode(errors='replace').rstrip()}\n```")
for p, start, stop, why in ((f"{A}/guest-cycle/cells-1.out", "=== KILL15", "\n\n", "KILL15 on the guest"),
                            (f"{A}/guest-cycle/cells-3.out", "=== KILL2", "\n\n", "KILL2 on the guest, 200k")):
    t = open(p, encoding="utf-8").read()
    i = t.index(start); j = t.find(stop, i)
    seg = t[i:j if j > 0 else len(t)]
    add_source(p, "worktree", "evidence, excerpt", seg.encode(), excerpt_of=f"{start} to the next blank line")
    parts.append(f"\n\n## Evidence: {p[len(A) + 1:]} ({why})\n\n```text\n{seg.rstrip()}\n```")
b = show(HREF, "tools/cloud-round-trip")
lines = b.decode(errors="replace").splitlines()
add_source("tools/cloud-round-trip", HREF, "harness, excerpt", b, spans=[[7747, 7772]])
parts.append(f"\n\n## Excerpt: tools/cloud-round-trip (at {HREF}; fx_kill15, F-15)\n\n```text\n{numbered(lines, 7747, 7772)}\n```")

body = "".join(parts)
open(os.path.join(out, "packet-body.md"), "w").write(body)
man["packet_body_sha256"] = hashlib.sha256(body.encode()).hexdigest(); man["packet_body_bytes"] = len(body.encode())
man["files_whole"] = len(WHOLE); man["files_excerpted"] = len(BIG); man["register_rows"] = found
json.dump(man, open(os.path.join(out, "packet-manifest.json"), "w"), indent=2)
ex = {k: (s["lines_shown"], s["lines_total"]) for k, s in zip(BIG, [s for s in man["sources"] if s["kind"] == "file under review, excerpt"])}
print(f"whole {len(WHOLE)}, excerpted {ex}, contexts {len(contexts)}, evidence {len(EVID) + 3}, "
      f"register rows {len(found)}/{len(ids)}, body {len(body.encode())} bytes")
