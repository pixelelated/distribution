"""Build T18's Phase 4.6 packet and its manifest with the three-way scan (#665).

Usage: SECRET_PATTERNS=... python3 -I -B packet.py <worktree> <es tree> <out-packet.md> <out-manifest.json>

T17's builder (its stage-c/packet.py at 8667229959), adapted: the slice is the
EmulationStation fork's, read from git at the pin; the order at 2174265e9c and
the brief at 99515f83ad. Three files go whole (the job, the card and the page
sources); their three headers, CloudText.h, CloudText.cpp and CloudTextTests.cpp as
line-numbered excerpts covering every line 02, 03 and 04 cite, with 8 lines of
context, merged; the callers' cited lines (FileData.cpp, GuiMenu.cpp) the same
way. Trimmed from the start (D-WORKFLOW-195): the eight sources and the tests
whole would be about 365 KB with the analyses.

Every section passes the mask (the D-QA-021 sed's rule). Then, per section,
the three-way scan of what leaves:
  1. tools/forbidden-terms-check --stdin: 0 hits required, else exit 1;
  2. SECRET_PATTERNS (the push guard's, from the environment, applied with
     grep -E as guard-lib does), after proving it fires on a run-time fake
     line: every hit recorded by location and dispositioned;
  3. the mask's own changes and a credential-word scan of the masked text
     (key|pass|token|user|psk|secret|pin, case-insensitive): every hit is
     recorded by location with a shape class; a masked value whose original
     shape is a literal, or a word-hit followed by a literal, is `review`.
No hit's text and no masked original is written; locations and classes only.
A `review` or a value stops the build (exit 1).
"""
import hashlib, json, os, re, subprocess, sys

WT, ES, OUT, MANIFEST = sys.argv[1:5]
PIN, P1, BR = "16dbac5211eea7e70db7394372033be2be7df829", "2174265e9c", "99515f83ad"
A = "docs/audits/2026_10_26-epic-m6-es-cloud-pages"
MASK = re.compile(r"((token|key|passw[a-z]*|psk|user)[=:])[^ ]*", re.I)
WORD = re.compile(r"key|pass|token|user|psk|secret|\bpin\b", re.I)
SP = os.environ.get("SECRET_PATTERNS", "")
assert SP, "SECRET_PATTERNS unset"

WHOLE = ["es-app/src/CloudTransferJob.cpp", "es-app/src/ThreadedCloudSync.cpp", "es-app/src/guis/GuiCloudTransfer.cpp"]
LARGE = {"CloudText.h": "es-app/src/CloudText.h", "CloudText.cpp": "es-app/src/CloudText.cpp",
         "CloudTransferJob.h": "es-app/src/CloudTransferJob.h", "ThreadedCloudSync.h": "es-app/src/ThreadedCloudSync.h",
         "GuiCloudTransfer.h": "es-app/src/guis/GuiCloudTransfer.h",
         "CloudTextTests.cpp": "es-app/tests/unit/CloudTextTests.cpp",
         "FileData.cpp": "es-app/src/FileData.cpp", "GuiMenu.cpp": "es-app/src/guis/GuiMenu.cpp"}
# Lines the ask names beside those 02/03/04 cite.
EXTRA = {"CloudText.h": [(1, 30), (78, 110), (160, 220)], "CloudText.cpp": [(150, 200), (405, 485), (555, 645), (805, 880)],
         "CloudTextTests.cpp": [(632, 721), (859, 878), (907, 937)],
         "CloudTransferJob.h": [(17, 60), (199, 215)], "ThreadedCloudSync.h": [(14, 20), (60, 135), (190, 201)], "GuiCloudTransfer.h": [(14, 45), (64, 100), (150, 165)], "FileData.cpp": [(985, 1030)], "GuiMenu.cpp": [(5038, 5100)]}
CTX = 8


def git(*args):
    return subprocess.run(["git", "-C", WT, *args], check=True, capture_output=True, text=True).stdout


def es(path):
    return subprocess.run(["git", "-C", ES, "show", f"{PIN}:{path}"], check=True, capture_output=True, text=True).stdout


def worktree(path):
    with open(f"{WT}/{path}", encoding="utf-8") as s:
        return s.read()


def numbered(lines, start=1, width=5):
    return "\n".join(f"{n:>{width}}  {l}" for n, l in enumerate(lines, start))


def cites(texts):
    pat = re.compile(r"`?(" + "|".join(re.escape(n) for n in LARGE) + r")`?:(\d+)(?:-(\d+))?((?:,\s*`?:?\d+(?:-\d+)?`?)*)")
    out = {k: [] for k in LARGE}
    for t in texts:
        for m in pat.finditer(t):
            out[m.group(1)].append((int(m.group(2)), int(m.group(3) or m.group(2))))
            for x in re.findall(r"(\d+)(?:-(\d+))?", m.group(4) or ""):
                out[m.group(1)].append((int(x[0]), int(x[1] or x[0])))
    return out


def ranges(pairs, n):
    spans = sorted((max(1, a - CTX), min(n, b + CTX)) for a, b in pairs if a <= n)
    merged = []
    for a, b in spans:
        if merged and a <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    return merged


def shape(v):
    """The class of a masked original value; never the value."""
    v = v.strip().rstrip(",;)")
    if not v:
        return "empty"
    if re.match(r"""^["']?\$""", v):
        return "expansion"
    if re.match(r"""^["']?(\*+|<[^>]*>|x+|\.\.\.|…)""", v, re.I):
        return "placeholder"
    if re.match(r"""^["']?[A-Za-z_][A-Za-z0-9_.]*(\(|\[|$|["'],?$)""", v) and not re.match(r"""^["'][A-Za-z0-9_]{12,}["']?$""", v):
        return "identifier-or-word"
    if re.match(r"""^["']?["'](\s|$)""", v) or v in ('""', "''"):
        return "empty-string"
    if re.match(r"^[\[{(\"']", v):
        return "expression"
    if re.match(r"^\d{1,4}$", v):
        return "small-number"
    return "review"


# Hits the classifier sends to `review`, each read by shape (length, first and
# last two characters; never the text) and dispositioned here by (path, line):
# a slice file's own line for an excerpt, else the section's line.
DISPOSITIONS = {
    ("docs/decision-register.md", 21): "name: D-QA-021's prose naming rclone's `pass =`, `user =`, `token =`, `key =` (the read filter's own row)",
    ("es-app/src/ThreadedCloudSync.cpp", 123): "code: whyForToken compares a stamp's outcome token with a word (`token == \"folder-missing\"`)",
    ("es-app/src/ThreadedCloudSync.cpp", 124): "code: whyForToken compares a stamp's outcome token with a word",
    ("es-app/src/ThreadedCloudSync.cpp", 125): "code: whyForToken compares a stamp's outcome token with a word",
    ("es-app/src/ThreadedCloudSync.cpp", 126): "code: whyForToken compares a stamp's outcome token with a word",
    ("es-app/src/ThreadedCloudSync.cpp", 127): "code: whyForToken compares a stamp's outcome token with a word",
    ("es-app/src/CloudText.h", 108): "code: `bool knownToken = false;`, a member's initial value",
}


def disposed(path, line):
    m = re.match(r"^(.*):(\d+)-(\d+)$", path)
    if m:
        path, line = m.group(1), int(m.group(2)) + line - 1
    for (p, l), why in DISPOSITIONS.items():
        if (path == p or (not m and path.startswith(p))) and line == l:
            return why
    return None


sources, parts, masked_total = [], [], 0
scan = {"forbidden": [], "secret_patterns": [], "mask": [], "words": []}


def grep_lines(pattern, text, flags):
    r = subprocess.run(["grep", "-a", "-n", *flags, "-E", "-e", pattern], input=text, capture_output=True, text=True)
    assert r.returncode in (0, 1), ("grep", r.returncode)
    return [int(l.split(":", 1)[0]) for l in r.stdout.splitlines()]


def add(title, body, path, ref, kind, fence=True):
    global masked_total
    raw = body.splitlines()
    out = [MASK.sub(r"\1***", l) for l in raw]
    sid = len(sources) + 1
    for i, (a, b) in enumerate(zip(raw, out), 1):
        if a != b:
            classes = [shape(m.group(0)[len(m.group(1)):]) for m in MASK.finditer(a)]
            why = "review" if "review" in classes else "name (the masked token is not a literal)"
            if why == "review":
                why = disposed(path, i) or "review"
            scan["mask"].append({"section": sid, "line": i, "classes": classes, "disposition": why})
    masked_total += sum(1 for a, b in zip(raw, out) if a != b)
    data = "\n".join(out) + "\n"
    fr = subprocess.run([f"{WT}/tools/forbidden-terms-check", "--stdin"], input=data, capture_output=True, text=True)
    assert fr.returncode in (0, 1), ("forbidden-terms-check", fr.returncode, fr.stderr)
    if fr.returncode == 1:
        scan["forbidden"].append({"section": sid, "result": fr.stdout.strip()})
    for ln in grep_lines(SP, data, []):
        scan["secret_patterns"].append({"section": sid, "line": ln, "disposition": disposed(path, ln) or "review"})
    for i, l in enumerate(out, 1):
        for m in WORD.finditer(l):
            tail = l[m.end():m.end() + 40]
            follow = re.match(r"""[A-Za-z_]*\s*[=:]\s*(.*)""", tail)
            cls = "word"
            if follow:
                v = follow.group(1)
                cls = "masked" if v.startswith("***") else shape(v)
            hit = {"section": sid, "line": i, "word": m.group(0).lower(), "class": cls}
            if cls == "review" and disposed(path, i):
                hit["class"], hit["disposition"] = "dispositioned", disposed(path, i)
            scan["words"].append(hit)
    sources.append({"section": sid, "title": title, "path": path, "ref": ref, "kind": kind,
                    "sha256": hashlib.sha256(data.encode()).hexdigest(), "bytes": len(data.encode()),
                    "forbidden_terms_check": fr.stdout.strip()})
    parts.append(f"\n\n## {title}\n\n" + (f"```text\n{data}```" if fence else data))


# Prove the secret scan fires before trusting its silence: a fake line built at run time.
fake = "".join(["dev", "pass", "word=", "Q" * 6, "7" * 6]) + "\n"
assert grep_lines(SP, fake, []) == [1], "SECRET_PATTERNS did not fire on the run-time fake line"
fr = subprocess.run([f"{WT}/tools/forbidden-terms-check", "--stdin"], input="nothing here\n", capture_output=True, text=True)
assert fr.returncode == 0, ("forbidden-terms-check on a clean line", fr.returncode)

ask = worktree(f"{A}/stage-c/ask.md")
parts.append(ask.rstrip("\n"))
sources.append({"section": 0, "title": "ask", "path": f"{A}/stage-c/ask.md", "ref": "worktree", "kind": "ask",
                "sha256": hashlib.sha256(ask.encode()).hexdigest(), "bytes": len(ask.encode())})
analyses = {n: worktree(f"{A}/{n}") for n in ("02-forward-audit.md", "03-retrospective.md", "04-analysis.md")}
for n, t in analyses.items():
    add(f"The first reader's {n} (whole)", t, f"{A}/{n}", "worktree", "first reader", fence=False)

order = git("show", f"{P1}:docs/reviews/order.md")
add("Context 1: docs/reviews/order.md § T18", re.search(r"^### T18\..*?(?=^### T19\.)", order, re.S | re.M).group(0),
    "docs/reviews/order.md § T18", P1, "context")
brief = git("show", f"{BR}:docs/reviews/briefs/es-cloud-pages.md")
add("Context 2: the brief's § 4", re.search(r"^## 4\. The questions.*?(?=^## 5\.)", brief, re.S | re.M).group(0),
    "docs/reviews/briefs/es-cloud-pages.md § 4", BR, "context")
reg = worktree("docs/decision-register.md")
ids = ["D-UI-028", "D-UI-030", "D-UI-031", "D-UI-035", "D-UI-078", "D-UI-117", "D-CLOUD-077", "D-CLOUD-109", "D-CLOUD-119",
       "D-CLOUD-129", "D-CLOUD-130", "D-CLOUD-175"]
rows = [l for l in reg.splitlines() if any(l.startswith(f"| {x} |") for x in ids)]
assert len(rows) == len(ids), (len(rows), len(ids))
add("Context 3: the register rows", "\n\n".join(rows), "docs/decision-register.md rows " + ", ".join(ids), "worktree", "context")

for path in WHOLE:
    lines = es(path).splitlines()
    add(f"{path} @ {PIN[:10]} (whole, {len(lines)} lines)", numbered(lines), path, PIN, "slice file (whole)")

c = cites(list(analyses.values()))
for name, path in LARGE.items():
    lines = es(path).splitlines()
    pairs = c[name] + EXTRA.get(name, [])
    for a, b in ranges(pairs, len(lines)):
        add(f"{path} @ {PIN[:10]}: lines {a}-{b} (excerpt of {len(lines)})", numbered(lines[a - 1:b], a), f"{path}:{a}-{b}", PIN, "excerpt")

body = "\n".join(parts) + "\n"
review = ([h for h in scan["mask"] if h["disposition"] == "review"] + [h for h in scan["secret_patterns"] if h["disposition"] == "review"]
          + [h for h in scan["words"] if h["class"] == "review"] + scan["forbidden"])
summary = {
    "forbidden_terms_check": f"{len(scan['forbidden'])} section(s) with hits of {len(sources) - 1}; proven to run on a clean line",
    "secret_patterns": f"{len(scan['secret_patterns'])} line(s); proven to fire on a run-time fake line",
    "mask": f"{masked_total} line(s) masked; classes " + json.dumps(sorted({c for h in scan['mask'] for c in h['classes']})),
    "words": f"{len(scan['words'])} credential-word hit(s); classes " + json.dumps({k: sum(1 for h in scan['words'] if h['class'] == k) for k in sorted({h['class'] for h in scan['words']})}),
    "review": len(review),
}
manifest = {"schema": "t18-packet-manifest/1", "pin": PIN, "sources": sources, "scan": scan, "summary": summary,
            "packet": {"file": OUT.split("/")[-1], "bytes": len(body.encode()), "sha256": hashlib.sha256(body.encode()).hexdigest()}}
with open(MANIFEST, "w", encoding="utf-8") as s:
    json.dump(manifest, s, indent=1); s.write("\n")
if review:
    print(f"STOP: {len(review)} hit(s) need review; packet not written", file=sys.stderr)
    for h in review[:40]:
        src = next((x for x in sources if x["section"] == h.get("section")), {})
        print("  review:", src.get("path"), "line", h.get("line"), h.get("classes") or h.get("class") or h.get("result"), file=sys.stderr)
    sys.exit(1)
with open(OUT, "w", encoding="utf-8") as s:
    s.write(body)
print(len(sources), "sections;", len(body.encode()), "bytes;", json.dumps(summary))
