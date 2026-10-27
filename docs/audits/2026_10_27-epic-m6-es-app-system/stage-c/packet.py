"""Build T33's Phase 4.6 packet and its manifest with the three-way scan (#680; T32's stage-c/packet.py, #679, adapted).

Usage: SECRET_PATTERNS=... python3 -I -B packet.py <worktree> <es tree> <out-packet.md> <out-manifest.json>

The fork's 27 added files and NetworkThread.cpp/.h go whole and line-numbered;
of the 46 upstream-carried files (and es-app/CMakeLists.txt, Win32ApiSystem.cpp)
only the ranges 02, 03 and 04 cite, with 8 lines of context, merged
(D-WORKFLOW-195); the two binaries (.ico, .aps) send nothing. Then the
neighbours the leads turn on. The manifest names every range sent and every
range trimmed, per file.

The mask and the three-way scan are T26's, unchanged through T32: the
forbidden-terms check (proven to run on a clean line), the push guard's
SECRET_PATTERNS (proven to fire on a run-time fake line), and the
credential-word scan by shape class. No hit's text and no masked original is
written. A `review` stops the build.
"""
import hashlib, json, os, re, subprocess, sys

WT, ES, OUT, MANIFEST = sys.argv[1:5]
PIN, BR = "16dbac5211eea7e70db7394372033be2be7df829", "c48f8b387e"
A = "docs/audits/2026_10_27-epic-m6-es-app-system"
MASK = re.compile(r"((token|key|passw[a-z]*|psk|user)[=:])[^ ]*", re.I)
WORD = re.compile(r"key|pass|token|user|psk|secret|\bpin\b", re.I)
SP = os.environ.get("SECRET_PATTERNS", "")
assert SP, "SECRET_PATTERNS unset"
CTX = 8
FORK = ["AppWindow.h", "CaptureRotation.cpp", "CaptureRotation.h", "CaptureRotationText.cpp", "CaptureRotationText.h",
        "CheevosIndex.cpp", "CheevosIndex.h", "CheevosRetry.cpp", "CheevosRetry.h", "CloudExit.h", "CloudFolderValidation.cpp",
        "CloudFolderValidation.h", "CloudOffer.cpp", "CloudOffer.h", "DisplayAspect.cpp", "DisplayAspect.h", "DisplayAspectText.cpp",
        "DisplayAspectText.h", "FolderMerge.h", "GameCubeRvzHashRetry.h", "JourneyTiers.h", "OfflineAchievementsText.cpp",
        "OfflineAchievementsText.h", "RunLock.h", "TextFit.h", "WifiText.cpp", "WifiText.h", "NetworkThread.cpp", "NetworkThread.h"]
WHOLE = ["es-app/src/" + f for f in FORK]
EXTRA_WHOLE = []
BINARY = ("es-app/EmulationStation.aps", "es-app/src/es_icon.ico")
NEIGHBOURS = {
    "es-app/src/views/ViewController.cpp": [(490, 560), (1119, 1160)],
    "es-app/src/FileData.cpp": [(985, 1005), (1160, 1170), (1200, 1212), (2185, 2195)],
    "es-app/src/SystemData.cpp": [(120, 130), (465, 490), (650, 660), (1196, 1290), (1560, 1572), (1648, 1664)],
    "es-app/src/main.cpp": [(800, 850), (890, 900), (955, 978), (1316, 1334)],
    "es-core/src/watchers/WatchersManager.cpp": [(85, 105), (165, 200)],
    "es-core/src/utils/FileSystemUtil.cpp": [(225, 265), (340, 350)],
    "es-app/src/guis/GuiGamelistOptions.cpp": [(60, 80), (165, 180), (250, 270), (420, 440), (595, 610)],
    "es-app/src/guis/GuiCollectionSystemsOptions.cpp": [(225, 232), (360, 372), (485, 500)],
    "es-app/src/guis/GuiGamelistFilter.cpp": [(8, 45), (220, 268)],
    "es-app/src/guis/GuiMenu.cpp": [(5750, 5760), (8495, 8520)],
    "es-app/src/guis/GuiRetroAchievementsSettings.cpp": [(185, 195), (250, 262), (800, 810)],
}


def git(*args):
    return subprocess.run(["git", "-C", WT, *args], check=True, capture_output=True, text=True).stdout


def es(rev, path):
    return subprocess.run(["git", "-C", ES, "show", f"{rev}:{path}"], check=True, capture_output=True).stdout.decode("utf-8", "replace")


def worktree(path):
    with open(f"{WT}/{path}", encoding="utf-8") as s:
        return s.read()


def numbered(lines, start=1, width=5):
    return "\n".join(f"{n:>{width}}  {l}" for n, l in enumerate(lines, start))


def cites(texts):
    """{file: [(a, b)]}: every `File.cpp:N[-M]` the analyses cite, and every `:N[-M]` after it on the same line."""
    out = {}
    for t in texts:
        for line in t.split("\n"):
            cur = None
            for m in re.finditer(r"(`?([A-Za-z][A-Za-z]+\.(?:cpp|h)):(\d{1,5})(?:-(\d{1,5}))?`?)|(?<![\w.])`:(\d{1,5})(?:-(\d{1,5}))?`", line):
                if m.group(2):
                    cur = m.group(2)
                    a, b = int(m.group(3)), int(m.group(4) or m.group(3))
                elif cur:
                    a, b = int(m.group(5)), int(m.group(6) or m.group(5))
                else:
                    continue
                if b >= a and b - a < 2000:
                    out.setdefault(cur, []).append((a, b))
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


# Hits the classifier sends to `review`, each read by shape and dispositioned
# here by (path, line): a slice file's own line for an excerpt, else the
# section's line. Filled from the first build's STOP list, each read at its line.
DISPOSITIONS = {
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

brief = git("show", f"{BR}:docs/reviews/briefs/es-app-system.md")
add("Context 1: the brief's § 4", re.search(r"^## 4\. The questions.*?(?=^## 5\.)", brief, re.S | re.M).group(0),
    "docs/reviews/briefs/es-app-system.md § 4", BR, "context")
reg = worktree("docs/decision-register.md")
ids = ["D-CLOUD-049", "D-CLOUD-078", "D-UI-039", "D-UI-051", "D-UI-079", "D-UI-112", "D-WORKFLOW-050",
       "D-WORKFLOW-164", "D-WORKFLOW-165", "D-WORKFLOW-195", "D-WORKFLOW-209", "D-WORKFLOW-210", "D-WORKFLOW-211"]
rows = [l for l in reg.splitlines() if any(l.startswith(f"| {x} |") for x in ids)]
assert len(rows) == len(ids), (len(rows), len(ids))
add("Context 2: the register rows", "\n\n".join(rows), "docs/decision-register.md rows " + ", ".join(ids), "worktree", "context")

add("Evidence: stage-c/runs.txt (the host harnesses)", worktree(f"{A}/stage-c/runs.txt"), f"{A}/stage-c/runs.txt", "worktree", "evidence")
for n in ("floor.md", "includes.out", "build-pin.txt"):
    add(f"Evidence: stage-c/{n}", worktree(f"{A}/stage-c/{n}"), f"{A}/stage-c/{n}", "worktree", "evidence")
for n in sorted(os.listdir(f"{WT}/{A}/guest-cycle")):
    if n.endswith(".txt"):
        add(f"Evidence: guest-cycle/{n}", worktree(f"{A}/guest-cycle/{n}").replace("\r", ""), f"{A}/guest-cycle/{n}", "worktree", "evidence")

sent_lines = {}
for f in WHOLE + EXTRA_WHOLE:
    lines = es(PIN, f).splitlines()
    add(f"{f} @ {PIN[:10]} (whole, {len(lines)} lines)", numbered(lines), f, PIN, "slice file (whole)")
    sent_lines[f.rsplit("/", 1)[1]] = {"sent": [[1, len(lines)]], "trimmed": [], "lines": len(lines)}

paths = [l.strip() for l in open(f"{WT}/.qa-scratch/t33/paths.txt") if l.strip()]
cited = cites(list(analyses.values()))
for p in paths:
    f = p.rsplit("/", 1)[1]
    if p in WHOLE or p in EXTRA_WHOLE or p in BINARY:
        continue
    lines = es(PIN, p).splitlines()
    spans = ranges(cited.get(f, []), len(lines))
    trimmed, prev = [], 0
    for a, b in spans:
        if a > prev + 1:
            trimmed.append([prev + 1, a - 1])
        prev = b
    if prev < len(lines):
        trimmed.append([prev + 1, len(lines)])
    sent_lines[f] = {"sent": [list(r) for r in spans], "trimmed": trimmed, "lines": len(lines)}
    for a, b in spans:
        add(f"{p} @ {PIN[:10]}: lines {a}-{b} (excerpt of {len(lines)})", numbered(lines[a - 1:b], a), f"{p}:{a}-{b}", PIN, "excerpt")

for path, spans in NEIGHBOURS.items():
    lines = es(PIN, path).splitlines()
    for a, b in ranges(spans, len(lines)):
        add(f"{path} @ {PIN[:10]}: lines {a}-{b} (excerpt of {len(lines)})", numbered(lines[a - 1:b], a), f"{path}:{a}-{b}", PIN, "excerpt")

body = "\n".join(parts) + "\n"
review = ([h for h in scan["mask"] if h["disposition"] == "review"] + [h for h in scan["secret_patterns"] if h["disposition"] == "review"]
          + [h for h in scan["words"] if h["class"] == "review"] + scan["forbidden"])
assert len(sent_lines) == 75, len(sent_lines)
sent_total = sum(b - a + 1 for v in sent_lines.values() for a, b in v["sent"])
all_total = sum(v["lines"] for v in sent_lines.values())
summary = {
    "forbidden_terms_check": f"{len(scan['forbidden'])} section(s) with hits of {len(sources) - 1}; proven to run on a clean line",
    "secret_patterns": f"{len(scan['secret_patterns'])} line(s); proven to fire on a run-time fake line",
    "mask": f"{masked_total} line(s) masked; classes " + json.dumps(sorted({c for h in scan['mask'] for c in h['classes']})),
    "words": f"{len(scan['words'])} credential-word hit(s); classes " + json.dumps({k: sum(1 for h in scan['words'] if h['class'] == k) for k in sorted({h['class'] for h in scan['words']})}),
    "review": len(review),
    "slice": f"{sent_total} of {all_total} slice lines sent; {len(WHOLE) + len(EXTRA_WHOLE)} files whole; "
             f"{sum(1 for v in sent_lines.values() if not v['sent'])} files with no line cited (sent nothing)",
}
manifest = {"schema": "t33-packet-manifest/1", "pin": PIN, "sources": sources, "scan": scan, "summary": summary,
            "slice_files": sent_lines,
            "packet": {"file": OUT.split("/")[-1], "bytes": len(body.encode()), "sha256": hashlib.sha256(body.encode()).hexdigest()}}
with open(MANIFEST, "w", encoding="utf-8") as s:
    json.dump(manifest, s, indent=1); s.write("\n")
if review:
    print(f"STOP: {len(review)} hit(s) need review; packet not written", file=sys.stderr)
    for h in review[:80]:
        src = next((x for x in sources if x["section"] == h.get("section")), {})
        print("  review:", src.get("path"), "line", h.get("line"), h.get("classes") or h.get("class") or h.get("result"), file=sys.stderr)
    sys.exit(1)
with open(OUT, "w", encoding="utf-8") as s:
    s.write(body)
print(len(sources), "sections;", len(body.encode()), "bytes;", json.dumps(summary))
