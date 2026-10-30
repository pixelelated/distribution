"""Build T34's Phase 4.6 packet (#681, D-WORKFLOW-195) and its manifest: the 21
fork-modified files whole; of the 59 upstream-carried only the line ranges
02-forward-audit.md cites (each with 8 lines of context, merged); 02 (and 03, 04
once they exist) whole; the brief's § 4. Scans the packet before it can leave:
tools/forbidden-terms-check, the secret patterns, and every credential-shaped
word dispositioned by class (library plumbing / macro name / identifier /
setting name / header name / prose); a hit that is a value, or one it cannot
class, stops the packet (exit 1, nothing written).
    t34-packet.py <ES worktree> <out dir>"""
import hashlib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t34lib import PIN, BASE, COMP, AUDIT, ROOT, BRIEF, die, show, paths, git

W, OUT = sys.argv[1], sys.argv[2]
files = paths()
fork = set(git(W, "diff", "--name-only", BASE, PIN, "--", *files).split())
if len(fork) != 21:
    die("fork-modified: %d, expected 21" % len(fork))
docs = [n for n in ("02-forward-audit.md", "03-retrospective.md", "04-analysis.md", "05-punch-list.md") if os.path.exists(os.path.join(AUDIT, n))]
cited = {}
CTX = 8
for n in docs:
    cur = None
    for tok in re.findall(r"`([^`]+)`", open(os.path.join(AUDIT, n), encoding="utf-8").read()):
        for m in re.finditer(r"(?:([A-Za-z]+\.(?:cpp|h)):)?(\d+)(?:-(\d+))?", tok):
            if m.group(1):
                cur = m.group(1)
            if cur and m.group(2) and (m.group(1) or tok.startswith(":")):
                a = int(m.group(2)); b = int(m.group(3) or a)
                cited.setdefault(cur, []).append((a, b))
parts, sources, slice_files = [], [], {}
def add(section, title, path, ref, kind, text):
    b = text.encode("utf-8")
    sources.append({"section": section, "title": title, "path": path, "ref": ref, "kind": kind, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    parts.append("\n\n## %s\n\n%s" % (title, text))
sec = 0
for f in sorted(files):
    name = f[len(COMP):]
    lines = show(W, f).split("\n")
    n = len(lines) - (1 if lines[-1] == "" else 0)
    if f in fork:
        sec += 1
        add(sec, "%s (whole, fork-modified, at the pin)" % name, f, PIN[:10], "whole", "```text\n" + "\n".join("%5d  %s" % (i, l) for i, l in enumerate(lines[:n], 1)) + "\n```")
        slice_files[name] = {"sent": [[1, n]], "trimmed": [], "lines": n}
        continue
    rs = sorted((max(1, a - CTX), min(n, b + CTX)) for a, b in cited.get(name, []) if a <= n)
    merged = []
    for a, b in rs:
        if merged and a <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    sent, gaps, prev = [], [], 0
    for a, b in merged:
        sec += 1
        add(sec, "%s `:%d-%d` (an excerpt, upstream-carried, at the pin)" % (name, a, b), f, PIN[:10], "excerpt", "```text\n" + "\n".join("%5d  %s" % (i, lines[i - 1]) for i in range(a, b + 1)) + "\n```")
        sent.append([a, b])
        if a > prev + 1:
            gaps.append([prev + 1, a - 1])
        prev = b
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
packet = "# T34 (#681) packet: EmulationStation's core components at the pin %s\n" % PIN + "".join(parts) + "\n"
# the scan
ftc = subprocess.run([os.path.join(ROOT, "tools/forbidden-terms-check"), "--stdin"], input=packet.encode(), capture_output=True)
if ftc.returncode != 0:
    die("forbidden-terms-check refused the packet (rc %d)" % ftc.returncode)
sp = subprocess.run(["bash", "-c", '. "$1"; grep -E -c -e "$SECRET_PATTERNS"', "x", os.path.join(ROOT, ".githooks/secret-patterns")], input=packet.encode(), capture_output=True)
nsec = int(sp.stdout.decode().strip() or "0")
if nsec != 0:
    die("the secret patterns match %d packet line(s)" % nsec)
WORD = re.compile(r"(?i)\b(password|passwd|pass|token|secret|apikey|api_key|key|keys|user|username|psk|auth|credential)\b")
DISP = {  # (slice file, its line) -> the disposition, read in the packet; anything else stops the packet
 ("AsyncNotificationComponent.cpp", 204): "identifier: the joined candidate rows the card re-chooses on (`render`, `:200-224`)",
 ("AsyncNotificationComponent.cpp", 206): "identifier: the same", ("AsyncNotificationComponent.cpp", 207): "identifier: the same",
 ("AsyncNotificationComponent.cpp", 209): "identifier: the same", ("AsyncNotificationComponent.cpp", 216): "identifier: the same",
 ("AsyncNotificationComponent.cpp", 218): "identifier: the same", ("AsyncNotificationComponent.cpp", 219): "identifier: the same",
 ("AsyncNotificationComponent.cpp", 221): "identifier: the same",
 ("ComponentGrid.cpp", 394): "prose: a comment (a pad key)", ("ComponentGrid.cpp", 395): "prose: a comment (a pad key)",
 ("ComponentList.h", 50): "prose: a comment (the player)",
 ("IList.h", 273): "prose: a comment (the player, a pad key)",
 ("VideoVlcComponent.cpp", 660): "identifier: a VLC command-line option word",
 ("VideoVlcComponent.cpp", 866): "identifier: a VLC option word split from the options string",
 ("VideoVlcComponent.cpp", 867): "identifier: the same",
}
_drop = os.environ.get("T34_PACKET_DROP")  # the drift test only: <file>:<line> withheld
if _drop:
    DISP.pop((_drop.split(":")[0], int(_drop.split(":")[1])), None)
words, unclassed = [], []
plines = packet.split("\n")
prose_from = next((i for i, l in enumerate(plines, 1) if l.startswith("## The first reader's ") or l.startswith("## The brief's ")), len(plines) + 1)
cur = None
for i, l in enumerate(plines, 1):
    if l.startswith("## "):
        mm = re.match(r"## ([A-Za-z]+\.(?:cpp|h)) ", l)
        cur = mm.group(1) if mm else None
    for m in WORD.finditer(l):
        if i >= prose_from:
            words.append({"line": i, "word": m.group(1), "class": "prose (the analysis or the brief)"})
            continue
        fm = re.match(r"^\s*(\d+)  ", l)
        k = (cur, int(fm.group(1))) if (cur and fm) else None
        if k in DISP:
            words.append({"file": k[0], "file_line": k[1], "line": i, "word": m.group(1), "class": DISP[k]})
        else:
            unclassed.append((i, k, l[:160]))
if unclassed:
    die("credential-shaped words with no class: %s" % unclassed[:12])
os.makedirs(OUT, exist_ok=True)
pb = packet.encode("utf-8")
open(os.path.join(OUT, "t34-packet.md"), "wb").write(pb)
man = {"schema": "t34-packet-manifest-1", "pin": PIN, "sources": sources,
       "scan": {"forbidden": [], "secret_patterns": [], "mask": [], "words": words},
       "summary": {"forbidden_terms_check": ftc.stdout.decode().strip(), "secret_patterns": "%d line(s) match" % nsec, "mask": "0 value(s) masked", "words": "%d credential-shaped word(s), each classed; 0 a value" % len(words), "review": 0, "slice": "21 fork-modified whole, %d upstream-carried by cited ranges" % sum(1 for k, v in slice_files.items() if v["sent"] and k not in {x[len(COMP):] for x in fork})},
       "slice_files": slice_files, "packet": {"file": "t34-packet.md", "bytes": len(pb), "sha256": hashlib.sha256(pb).hexdigest()}}
json.dump(man, open(os.path.join(OUT, "packet-manifest.json"), "w"), indent=1)
print("t34-packet: %d bytes, %d lines, %d sources (%d docs), sha256 %s; %s; %s; %s" % (len(pb), packet.count("\n"), len(sources), len(docs), man["packet"]["sha256"][:16], man["summary"]["forbidden_terms_check"], man["summary"]["secret_patterns"], man["summary"]["words"]))
