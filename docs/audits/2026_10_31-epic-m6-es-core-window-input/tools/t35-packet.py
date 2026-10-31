"""Build T35's Phase 4.6 packet (#682) and its manifest (T34's t34-packet.py's shape): the 13
fork-added and fork-modified files whole; of the 83 upstream-carried only the line ranges
02 to 05 cite (each with 8 lines of context, merged); 02 to 05 whole; the brief's § 4.
Scans the packet before it can leave: tools/forbidden-terms-check, the secret patterns, and
every credential-shaped word dispositioned by class; a hit that is a value, or one it
cannot class, stops the packet (exit 1, nothing written).
    t35-packet.py <ES worktree> <paths.txt> <out dir>"""
import hashlib
import json
import os
import re
import subprocess
import sys

W, PATHS, OUT = sys.argv[1:4]
PIN = "16dbac5211eea7e70db7394372033be2be7df829"
BASE = "bccd715707"
HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(AUDIT, "..", "..", ".."))
BRIEF = os.path.join(ROOT, "docs/reviews/briefs/es-core-window-input.md")


def die(m):
    print("t35-packet: " + m, file=sys.stderr)
    sys.exit(1)


def git(*a):
    return subprocess.run(["git", "-C", W] + list(a), capture_output=True, text=True, check=True).stdout


files = [l.strip() for l in open(PATHS) if l.strip()]
fork = set(git("diff", "--name-only", BASE, PIN, "--", *files).split())
if len(fork) != 13:
    die("fork-added and fork-modified: %d, expected 13" % len(fork))
by_base = {}
for f in files:
    by_base.setdefault(f.split("/")[-1], []).append(f)
docs = [n for n in ("02-forward-audit.md", "03-retrospective.md", "04-analysis.md", "05-punch-list.md") if os.path.exists(os.path.join(AUDIT, n))]
cited = {}
CTX = 8
for n in docs:
    cur = None
    for tok in re.findall(r"`([^`]+)`", open(os.path.join(AUDIT, n), encoding="utf-8").read()):
        for m in re.finditer(r"(?:([A-Za-z_/]+\.(?:cpp|h|txt)):)?(\d+)(?:-(\d+))?", tok):
            if m.group(1):
                b = m.group(1).split("/")[-1]
                cur = by_base[b][0] if len(by_base.get(b, [])) == 1 else None
            if cur and m.group(2) and (m.group(1) or tok.startswith(":")):
                a = int(m.group(2)); z = int(m.group(3) or a)
                cited.setdefault(cur, []).append((a, z))
parts, sources, slice_files = [], [], {}


def add(section, title, path, ref, kind, text):
    b = text.encode("utf-8")
    sources.append({"section": section, "title": title, "path": path, "ref": ref, "kind": kind, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    parts.append("\n\n## %s\n\n%s" % (title, text))


sec = 0
for f in sorted(files):
    name = f[len("es-core/"):] if f.startswith("es-core/") else f
    text = git("show", "%s:%s" % (PIN, f))
    lines = text.split("\n")
    n = len(lines) - (1 if lines[-1] == "" else 0)
    if f in fork:
        sec += 1
        add(sec, "%s (whole, fork-%s, at the pin)" % (name, "added" if f.endswith("LogPolicy.h") else "modified"), f, PIN[:10], "whole", "```text\n" + "\n".join("%5d  %s" % (i, l) for i, l in enumerate(lines[:n], 1)) + "\n```")
        slice_files[name] = {"sent": [[1, n]], "trimmed": [], "lines": n}
        continue
    rs = sorted((max(1, a - CTX), min(n, z + CTX)) for a, z in cited.get(f, []) if a <= n)
    merged = []
    for a, z in rs:
        if merged and a <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], z)
        else:
            merged.append([a, z])
    sent, gaps, prev = [], [], 0
    for a, z in merged:
        sec += 1
        add(sec, "%s `:%d-%d` (an excerpt, upstream-carried, at the pin)" % (name, a, z), f, PIN[:10], "excerpt", "```text\n" + "\n".join("%5d  %s" % (i, lines[i - 1]) for i in range(a, z + 1)) + "\n```")
        sent.append([a, z])
        if a > prev + 1:
            gaps.append([prev + 1, a - 1])
        prev = z
    if prev < n:
        gaps.append([prev + 1, n])
    slice_files[name] = {"sent": sent, "trimmed": gaps, "lines": n}
for n in docs:
    sec += 1
    add(sec, "The first reader's %s (whole)" % n, "%s/%s" % (os.path.relpath(AUDIT, ROOT), n), "worktree", "analysis", open(os.path.join(AUDIT, n), encoding="utf-8").read())
bt = open(BRIEF, encoding="utf-8").read()
q = bt[bt.index("## 4. The questions"):bt.index("## 5. The evidence floor")]
sec += 1
add(sec, "The brief's § 4, the questions", os.path.relpath(BRIEF, ROOT), "worktree", "brief", q)
packet = "# T35 (#682) packet: EmulationStation's window, input and the rest of es-core at the pin %s\n" % PIN + "".join(parts) + "\n"
ftc = subprocess.run([os.path.join(ROOT, "tools/forbidden-terms-check"), "--stdin"], input=packet.encode(), capture_output=True)
if ftc.returncode != 0:
    die("forbidden-terms-check refused the packet (rc %d)" % ftc.returncode)
sp = subprocess.run(["bash", "-c", '. "$1"; grep -E -c -e "$SECRET_PATTERNS"', "x", os.path.join(ROOT, ".githooks/secret-patterns")], input=packet.encode(), capture_output=True)
nsec = int(sp.stdout.decode().strip() or "0")
if nsec != 0:
    die("the secret patterns match %d packet line(s)" % nsec)
WORD = re.compile(r"(?i)\b(password|passwd|pass|token|secret|apikey|api_key|key|keys|user|username|psk|auth|credential)\b")
DISP = json.load(open(os.path.join(HERE, "t35-packet-disp.json"))) if os.path.exists(os.path.join(HERE, "t35-packet-disp.json")) else {}
_drop = os.environ.get("T35_PACKET_DROP")  # the drift test only: <file>:<line> withheld
if _drop:
    DISP.pop(_drop, None)
words, unclassed = [], []
plines = packet.split("\n")
prose_from = next((i for i, l in enumerate(plines, 1) if l.startswith("## The first reader's ") or l.startswith("## The brief's ")), len(plines) + 1)
cur = None
for i, l in enumerate(plines, 1):
    if l.startswith("## "):
        mm = re.match(r"## ([A-Za-z_/]+\.(?:cpp|h|txt)) ", l)
        cur = mm.group(1) if mm else None
    for m in WORD.finditer(l):
        if i >= prose_from:
            words.append({"line": i, "word": m.group(1), "class": "prose (the analysis or the brief)"})
            continue
        fm = re.match(r"^\s*(\d+)  ", l)
        k = "%s:%s" % (cur, fm.group(1)) if (cur and fm) else None
        if k in DISP:
            words.append({"file": cur, "file_line": int(fm.group(1)), "line": i, "word": m.group(1), "class": DISP[k]})
        else:
            unclassed.append((i, k, l[:160]))
if unclassed:
    for u in unclassed:
        print("UNCLASSED %s %s" % (u[1], u[2]), file=sys.stderr)
    die("%d credential-shaped word(s) with no class" % len(unclassed))
os.makedirs(OUT, exist_ok=True)
pb = packet.encode("utf-8")
open(os.path.join(OUT, "t35-packet.md"), "wb").write(pb)
man = {"schema": "t35-packet-manifest-1", "pin": PIN, "sources": sources,
       "scan": {"forbidden": [], "secret_patterns": [], "mask": [], "words": words},
       "summary": {"forbidden_terms_check": ftc.stdout.decode().strip(), "secret_patterns": "%d line(s) match" % nsec, "mask": "0 value(s) masked", "words": "%d credential-shaped word(s), each classed; 0 a value" % len(words), "review": 0,
                   "slice": "13 fork-added and fork-modified whole, %d upstream-carried by cited ranges" % sum(1 for k, v in slice_files.items() if v["sent"] and ("es-core/" + k) not in fork)},
       "slice_files": slice_files, "packet": {"file": "t35-packet.md", "bytes": len(pb), "sha256": hashlib.sha256(pb).hexdigest()}}
json.dump(man, open(os.path.join(OUT, "packet-manifest.json"), "w"), indent=1)
print("t35-packet: %d bytes, %d lines, %d sources (%d docs), sha256 %s; %s; %s; %s" % (len(pb), packet.count("\n"), len(sources), len(docs), man["packet"]["sha256"][:16], man["summary"]["forbidden_terms_check"], man["summary"]["secret_patterns"], man["summary"]["words"]))
