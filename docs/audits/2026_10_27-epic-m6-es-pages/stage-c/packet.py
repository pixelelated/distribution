"""Build T31's Phase 4.6 packet and its manifest with the three-way scan (#678).

Usage: SECRET_PATTERNS=... python3 -I -B packet.py <worktree> <es tree> <out-packet.md> <out-manifest.json>

T26's builder (its stage-c/packet.py), adapted: the twelve fork-touched files
go whole and line-numbered; of the 64 upstream-carried files only the ranges
02, 03 and 04 cite, with 8 lines of context, merged (D-WORKFLOW-195); then the
neighbours the leads turn on. The manifest names every range sent and every
range trimmed, per file.

The mask and the three-way scan are T26's unchanged: the forbidden-terms check
(proven to run on a clean line), the push guard's SECRET_PATTERNS (proven to
fire on a run-time fake line), and the credential-word scan by shape class. No
hit's text and no masked original is written. A `review` stops the build.
"""
import hashlib, json, os, re, subprocess, sys

WT, ES, OUT, MANIFEST = sys.argv[1:5]
PIN, BR = "16dbac5211eea7e70db7394372033be2be7df829", "34e130d2ce"
A = "docs/audits/2026_10_27-epic-m6-es-pages"
G = "es-app/src/guis/"
MASK = re.compile(r"((token|key|passw[a-z]*|psk|user)[=:])[^ ]*", re.I)
WORD = re.compile(r"key|pass|token|user|psk|secret|\bpin\b", re.I)
SP = os.environ.get("SECRET_PATTERNS", "")
assert SP, "SECRET_PATTERNS unset"
CTX = 8
WHOLE = ["GuiScraperRun.cpp", "GuiScraperRun.h", "WifiScanProcess.h", "GuiBios.cpp", "GuiBios.h", "GuiGameOptions.cpp",
         "GuiImageViewer.cpp", "GuiSaveState.cpp", "GuiSaveState.h", "GuiScraperStart.cpp", "GuiSettings.cpp", "GuiSettings.h"]
EXTRA_WHOLE = ["GuiLoading.h", "GuiMoonlight.cpp", "GuiAnalogSticksLedControls.cpp"]   # read whole by the first reader, small
NEIGHBOURS = {
    "es-core/src/guis/GuiMsgBox.cpp": [(25, 40), (105, 135)],
    "es-core/src/components/OptionListComponent.h": [(290, 330), (580, 634)],
    "es-core/src/Settings.cpp": [(469, 540), (636, 690)],
    "es-core/src/SystemConf.cpp": [(285, 320), (439, 490)],
    "es-core/src/utils/AtomicFileUtil.cpp": [(430, 452)],
    "es-app/src/ApiSystem.cpp": [(872, 930), (2233, 2300)],
    "es-app/src/SaveState.cpp": [(213, 250)],
    "es-app/src/SaveStateRepository.cpp": [(280, 296)],
    "es-app/src/DisplayAspect.cpp": [(55, 135)],
    "es-app/src/SystemData.cpp": [(2069, 2072)],
    "es-core/src/utils/FileSystemUtil.cpp": [(1122, 1150)],
    "es-app/src/guis/GuiMenu.cpp": [(2190, 2200), (5745, 5760)],
}


def git(*args):
    return subprocess.run(["git", "-C", WT, *args], check=True, capture_output=True, text=True).stdout


def es(rev, path):
    return subprocess.run(["git", "-C", ES, "show", f"{rev}:{path}"], check=True, capture_output=True, text=True).stdout


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
            for m in re.finditer(r"(`?([A-Z][A-Za-z]+\.(?:cpp|h)):(\d{1,5})(?:-(\d{1,5}))?`?)|(?<![\w.])`:(\d{1,5})(?:-(\d{1,5}))?`", line):
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
    ('docs/audits/2026_10_27-epic-m6-es-pages/02-forward-audit.md', 105): "prose: the pages table's GLOBAL HOTKEYS / JOYSTICKS HOTKEYS row (`hotkey`, a word)",
    ('docs/audits/2026_10_27-epic-m6-es-pages/02-forward-audit.md', 117): "prose: the pages table's GuiKeyMappingEditor row (class names)",
    ('docs/audits/2026_10_27-epic-m6-es-pages/02-forward-audit.md', 118): "prose: the pages table's GuiKeyboardLayout row (a class name)",
    ('docs/audits/2026_10_27-epic-m6-es-pages/02-forward-audit.md', 119): "prose: the pages table's KEYBOARDTOPADS row (a title)",
    ('docs/audits/2026_10_27-epic-m6-es-pages/02-forward-audit.md', 141): "prose: the dialogs tool's description (`GuiMsgBox` is not a credential; a word hit on a name)",
    ('docs/audits/2026_10_27-epic-m6-es-pages/02-forward-audit.md', 267): "prose: the rows' summary naming `password = true` as the rows' mode",
    ('docs/audits/2026_10_27-epic-m6-es-pages/02-forward-audit.md', 268): "prose: the rows' summary naming PLAYER PASSWORD's `password = false` mode",
    ('docs/audits/2026_10_27-epic-m6-es-pages/02-forward-audit.md', 325): "prose: the titles table's GuiControllersSettings row (HOTKEYS titles)",
    ('docs/audits/2026_10_27-epic-m6-es-pages/02-forward-audit.md', 339): "prose: the titles table's KEYBOARDTOPADS row",
    ('docs/audits/2026_10_27-epic-m6-es-pages/02-forward-audit.md', 403): "prose: L-04 naming the row's `password = false` mode",
    ('docs/audits/2026_10_27-epic-m6-es-pages/02-forward-audit.md', 550): 'prose: the #585 row naming `password = true` as the change',
    ('es-app/src/guis/GuiMoonlight.cpp', 87): 'code: a parse marker, the `key=` prefix a line is searched for (no value)',
    ('es-app/src/guis/GuiMoonlight.cpp', 147): 'code: a file name (`key.pem`) joined to a path',
    ('es-app/src/guis/GuiSettings.h', 112): "code: `mLifeToken`, a page's life token (a member name)",
    ('es-app/src/guis/GuiSettings.h', 113): 'code: `mLifeToken` made (a member name)',
    ('es-app/src/guis/GuiAnalogSticksLedControls.cpp', 18): "code: `tokens` from splitting a setting's line",
    ('es-app/src/guis/GuiControllersSettings.cpp', 66): "code: `autohotkeys`, a switch's variable name",
    ('es-app/src/guis/GuiControllersSettings.cpp', 225): "code: `restrictHotkeys`, a switch's variable name",
    ('es-app/src/guis/GuiKeyMappingEditor.cpp', 474): 'code: the class name `GuiKeyMappingEditor`',
    ('es-app/src/guis/GuiKeyMappingEditor.cpp', 489): 'code: the class name `GuiKeyMappingEditor`',
    ('es-app/src/guis/GuiKeyMappingEditor.cpp', 504): 'code: the class name `GuiKeyMappingEditor`',
    ('es-app/src/guis/GuiKeyMappingEditor.cpp', 513): 'code: the class name `GuiKeyMappingEditor`',
    ('es-app/src/guis/GuiKeyboardLayout.cpp', 168): 'code: the class name `GuiKeyboardLayout`',
    ('es-app/src/guis/GuiMetaDataEd.cpp', 598): 'code: a metadata key name compared (`key == "rating"`)',
    ('es-app/src/ApiSystem.cpp', 901): "code: `tokens` from splitting a script's output line",
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

brief = git("show", f"{BR}:docs/reviews/briefs/es-pages.md")
add("Context 1: the brief's § 4", re.search(r"^## 4\. The questions.*?(?=^## 5\.)", brief, re.S | re.M).group(0),
    "docs/reviews/briefs/es-pages.md § 4", BR, "context")
reg = worktree("docs/decision-register.md")
ids = ["D-UI-021", "D-UI-028", "D-UI-030", "D-UI-039", "D-UI-073", "D-UI-074", "D-UI-078", "D-UI-079", "D-CLOUD-053",
       "D-WORKFLOW-080", "D-WORKFLOW-195"]
rows = [l for l in reg.splitlines() if any(l.startswith(f"| {x} |") for x in ids)]
assert len(rows) == len(ids), (len(rows), len(ids))
add("Context 2: the register rows", "\n\n".join(rows), "docs/decision-register.md rows " + ", ".join(ids), "worktree", "context")

add("Evidence: stage-c/runs.txt (the host harnesses)", worktree(f"{A}/stage-c/runs.txt"), f"{A}/stage-c/runs.txt", "worktree", "evidence")
for n in sorted(os.listdir(f"{WT}/{A}/guest-cycle")):
    if n.endswith(".txt"):
        add(f"Evidence: guest-cycle/{n}", worktree(f"{A}/guest-cycle/{n}").replace("\r", ""), f"{A}/guest-cycle/{n}", "worktree", "evidence")

sent_lines = {}
for f in WHOLE + EXTRA_WHOLE:
    lines = es(PIN, G + f).splitlines()
    add(f"{G}{f} @ {PIN[:10]} (whole, {len(lines)} lines)", numbered(lines), G + f, PIN, "slice file (whole)")
    sent_lines[f] = {"sent": [[1, len(lines)]], "trimmed": [], "lines": len(lines)}

paths = [l.strip() for l in open(f"{WT}/.qa-scratch/t31/paths.txt") if l.strip()]
cited = cites(list(analyses.values()))
for p in paths:
    f = p.rsplit("/", 1)[1]
    if f in WHOLE or f in EXTRA_WHOLE:
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
assert len(sent_lines) == 76, len(sent_lines)
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
manifest = {"schema": "t31-packet-manifest/1", "pin": PIN, "sources": sources, "scan": scan, "summary": summary,
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
