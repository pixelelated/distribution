"""Build T21's Phase 4.6 packet and its manifest with the three-way scan (#668).

Usage: SECRET_PATTERNS=... python3 -I -B packet.py <worktree> <es tree> <out-packet.md> <out-manifest.json>

T20's builder (its stage-c/packet.py at ffb6b686cb, itself T18's), adapted:
the slice is the EmulationStation fork's 14, read from git at the pin; the
shell writers from the distribution at 8ebaf8daad; the brief at 2f1d006461.
Six files go whole; every other file as line-numbered excerpts covering every
line 02, 03 and 04 cite plus the ranges named below, with 8 lines of
context, merged. Trimmed from the start (D-WORKFLOW-195).

The mask and the three-way scan are T20's unchanged: the forbidden-terms
check (proven to run on a clean line), the push guard's SECRET_PATTERNS
proven to fire on a run-time fake line, and the credential-word scan by shape
class. No hit's text and no masked original is written. A `review` stops the
build.
"""
import hashlib, json, os, re, subprocess, sys

WT, ES, OUT, MANIFEST = sys.argv[1:5]
PIN, BR, BASE = "16dbac5211eea7e70db7394372033be2be7df829", "2f1d006461", "8ebaf8daad"
A = "docs/audits/2026_10_26-epic-m6-es-state-and-bridge"
MASK = re.compile(r"((token|key|passw[a-z]*|psk|user)[=:])[^ ]*", re.I)
WORD = re.compile(r"key|pass|token|user|psk|secret|\bpin\b", re.I)
SP = os.environ.get("SECRET_PATTERNS", "")
assert SP, "SECRET_PATTERNS unset"

WHOLE = ["es-core/src/utils/AtomicFileUtil.h", "es-core/src/utils/AtomicFileUtil.cpp", "es-core/src/SystemConf.h",
         "es-core/src/SystemConf.cpp"]
LARGE = {"Settings.cpp": "es-core/src/Settings.cpp", "HttpReq.cpp": "es-core/src/HttpReq.cpp",
         "ApiSystem.cpp": "es-app/src/ApiSystem.cpp", "GuiWifi.cpp": "es-app/src/guis/GuiWifi.cpp",
         "ScreenScraper.cpp": "es-app/src/scrapers/ScreenScraper.cpp", "HttpReq.h": "es-core/src/HttpReq.h",
         "Settings.h": "es-core/src/Settings.h", "StringUtil.cpp": "es-core/src/utils/StringUtil.cpp",
         "Scraper.cpp": "es-app/src/scrapers/Scraper.cpp", "FileSystemUtil.cpp": "es-core/src/utils/FileSystemUtil.cpp",
         "TextEditComponent.cpp": "es-core/src/components/TextEditComponent.cpp", "main.cpp": "es-app/src/main.cpp",
         "GuiMenu.cpp": "es-app/src/guis/GuiMenu.cpp", "GuiBluetoothDevices.cpp": "es-app/src/guis/GuiBluetoothDevices.cpp"}
# Ranges the ask and the leads name beside the line citations 02, 03 and 04 make.
EXTRA = {"Settings.cpp": [(1, 20), (84, 130), (195, 210), (447, 723)],
         "HttpReq.cpp": [(1, 30), (96, 110), (125, 360), (361, 644)],
         "ApiSystem.cpp": [(564, 613), (616, 735), (798, 830), (872, 925), (982, 990), (1029, 1037), (1484, 1490), (1492, 1663),
                           (1868, 1890), (2080, 2090), (2233, 2333), (2335, 2440), (2505, 2520), (2585, 2595), (2915, 2922), (3486, 3510)],
         "GuiWifi.cpp": [(280, 400), (530, 585)], "ScreenScraper.cpp": [(27, 45), (265, 330), (700, 730), (857, 928), (976, 1090)],
         "HttpReq.h": [(1, 180)], "Settings.h": [(140, 165)], "StringUtil.cpp": [(426, 444), (505, 520), (715, 803)],
         "Scraper.cpp": [(425, 460), (520, 700), (779, 812)], "FileSystemUtil.cpp": [(642, 668), (1059, 1085), (1429, 1465)],
         "TextEditComponent.cpp": [(68, 94), (170, 185), (375, 378)], "main.cpp": [(1034, 1042)],
         "GuiMenu.cpp": [(2985, 2992), (3128, 3153), (3205, 3212), (5050, 5075), (8365, 8376), (9900, 9930)],
         "GuiBluetoothDevices.cpp": [(125, 152)]}
SHELL = {"projects/ROCKNIX/packages/rocknix/profile.d/001-functions": [(10, 16), (360, 441), (528, 610), (620, 625)],
         "projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl": [(38, 66), (150, 215), (415, 465), (485, 515)],
         "projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig": [(55, 106), (262, 330)],
         "projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-evidence": [(55, 80)],
         "projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool": [(280, 300)]}
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

# Hits the classifier sends to `review`, each read by shape (length, first and
# last two characters; never the text) and dispositioned here by (path, line).
DISPOSITIONS = {
    ('docs/audits/2026_10_26-epic-m6-es-state-and-bridge/02-forward-audit.md', 51): 'prose: L-12 quotes `key = it + "="`, a variable named key',
    ('docs/audits/2026_10_26-epic-m6-es-state-and-bridge/02-forward-audit.md', 89): 'prose: the query-parameter names devid and devpassword, no value',
    ('docs/audits/2026_10_26-epic-m6-es-state-and-bridge/02-forward-audit.md', 93): 'prose: the query-parameter names ssid and sspassword, no value',
    ('docs/decision-register.md', 5): "name: D-QA-021's prose naming rclone's field names and the read filter's own words",
    ('docs/audits/2026_10_26-epic-m6-es-state-and-bridge/stage-b/positives/shell-writers.out', 5): "evidence: a sentence naming the player's keys, no value",
    ('docs/audits/2026_10_26-epic-m6-es-state-and-bridge/stage-b/positives/state-units.out', 3): "evidence: a key's presence as 0 or 1 (has[name]=N)",
    ('docs/audits/2026_10_26-epic-m6-es-state-and-bridge/stage-b/positives/state-units.out', 12): "evidence: a key's presence as 0 or 1 (has[name]=N)",
    ('es-core/src/SystemConf.cpp', 366): 'code: `std::string key = it + "=";`, a key name built from a setting\'s name',
    ('es-core/src/HttpReq.cpp', 271): 'code: `userAgent` read from the options or the user-agent macro',
    ('es-app/src/ApiSystem.cpp', 568): 'comment: the phone keyboard option',
    ('es-app/src/ApiSystem.cpp', 901): "code: `tokens` from splitting a script's output line",
    ('es-app/src/ApiSystem.cpp', 1032): 'code: a setting read by its key name (`get("root.password")`)',
    ('es-app/src/scrapers/ScreenScraper.cpp', 40): 'code: a setting read by its key name (`getString("ScreenScraperDevPass")`)',
    ('es-app/src/scrapers/ScreenScraper.cpp', 49): "comment: the API's documented URL with its placeholders (devid=xxx)",
    ('es-app/src/scrapers/ScreenScraper.cpp', 874): 'code: a setting read by its key name',
    ('es-app/src/scrapers/ScreenScraper.cpp', 875): 'code: a setting read by its key name',
    ('es-app/src/scrapers/ScreenScraper.cpp', 890): 'code: a setting read by its key name',
    ('es-app/src/scrapers/ScreenScraper.cpp', 891): 'code: a setting read by its key name',
    ('es-app/src/scrapers/ScreenScraper.cpp', 1081): "code: `userInfo` from parsing the API's XML",
    ('es-app/src/guis/GuiMenu.cpp', 3131): "code: `tokens` from splitting a script's output line",
    ('es-app/src/guis/GuiMenu.cpp', 3209): "code: a row built from `getRootPassword()`'s result, no literal",
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


def trim02(text):
    out, section, cut = [], "", {"commands": 0, "atomic": 0, "writeall": 0}
    for line in text.split("\n"):
        if line.startswith("## "):
            section = line
        elif line.startswith("### "):
            section = line
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip()[1:-1])] if line.startswith("| ") else []
        if section.startswith("## The commands") and len(cells) == 12 and cells[5] == "none joined":
            cut["commands"] += 1
            continue
        if section.startswith("### 1.") and len(cells) == 9 and cells[2] not in ("write", "Kind") and not cells[2].startswith("---"):
            cut["atomic"] += 1
            continue
        if section.startswith("### 2.") and len(cells) == 8 and (cells[1].startswith("sysfs") or cells[1].startswith("the Windows")):
            cut["writeall"] += 1
            continue
        out.append(line)
    note = (f"\n\n**Trimmed for this packet (D-WORKFLOW-195):** § The commands omits its {cut['commands']} rows that join no external string; "
            f"§ The writers omits {cut['atomic']} `AtomicFile::` rows that are reads, types or comments and {cut['writeall']} "
            f"`writeAllText` rows that are sysfs or the Windows build. The full tables are in the audit folder.\n")
    return "\n".join(out) + note, cut


analyses["02-forward-audit.md"], CUT = trim02(analyses["02-forward-audit.md"])
assert CUT["commands"] == 93 and CUT["atomic"] == 32 and CUT["writeall"] == 17, CUT
for n, t in analyses.items():
    add(f"The first reader's {n} (whole)", t, f"{A}/{n}", "worktree", "first reader", fence=False)

brief = git("show", f"{BR}:docs/reviews/briefs/es-state-and-bridge.md")
add("Context 1: the brief's § 4", re.search(r"^## 4\. The questions.*?(?=^## 5\.)", brief, re.S | re.M).group(0),
    "docs/reviews/briefs/es-state-and-bridge.md § 4", BR, "context")
reg = worktree("docs/decision-register.md")
ids = ["D-CLOUD-078", "D-CLOUD-079", "D-NET-002", "D-NET-009", "D-SYS-011", "D-SYS-012", "D-QA-021", "D-UI-079",
       "D-WORKFLOW-166", "D-WORKFLOW-195"]
rows = [l for l in reg.splitlines() if any(l.startswith(f"| {x} |") for x in ids)]
assert len(rows) == len(ids), (len(rows), len(ids))
add("Context 2: the register rows", "\n\n".join(rows), "docs/decision-register.md rows " + ", ".join(ids), "worktree", "context")
def kill_summary(text):
    """kill-writer.out's summary lines, and one example line per kind of leftover; the cut stated."""
    keep, kinds, cut = [], set(), 0
    for line in text.splitlines():
        if line.startswith("==") or line.lstrip().startswith(("A:", "B:", "C:")):
            keep.append(line)
            continue
        kind = re.sub(r"[0-9]+", "N", line.split("left behind", 1)[1]) if "left behind" in line else ""
        kind = kind.split(";")[0]
        if kind not in kinds:
            kinds.add(kind); keep.append(line)
        else:
            cut += 1
    return "\n".join(keep) + f"\n(trimmed for this packet: {cut} kill-point lines like the ones shown; the whole file is in the audit folder)\n"


for n in ("kill-writer.out", "shell-writers.out", "state-units.out", "lifted.out"):
    text = worktree(f"{A}/stage-b/positives/{n}")
    add(f"Evidence: stage-b/positives/{n}", kill_summary(text) if n == "kill-writer.out" else text, f"{A}/stage-b/positives/{n}", "worktree", "evidence")
for n in ("g01-identity.txt", "g01-image-vs-tree.txt", "g02-modes.txt", "g03-argv.txt", "g04a-system-cfg.txt", "g04b-es-settings.txt", "g05-hostname.txt"):
    add(f"Evidence: guest-cycle/{n}", worktree(f"{A}/guest-cycle/{n}").replace("\r", ""), f"{A}/guest-cycle/{n}", "worktree", "evidence")

for path in WHOLE:
    lines = es(path).splitlines()
    add(f"{path} @ {PIN[:10]} (whole, {len(lines)} lines)", numbered(lines), path, PIN, "slice file (whole)")

c = cites(list(analyses.values()))
for name, path in LARGE.items():
    lines = es(path).splitlines()
    pairs = c[name] + EXTRA.get(name, [])
    if not pairs:
        continue
    for a, b in ranges(pairs, len(lines)):
        add(f"{path} @ {PIN[:10]}: lines {a}-{b} (excerpt of {len(lines)})", numbered(lines[a - 1:b], a), f"{path}:{a}-{b}", PIN, "excerpt")
for path, spans in SHELL.items():
    lines = git("show", f"{BASE}:{path}").splitlines()
    for a, b in ranges(spans, len(lines)):
        add(f"{path.rsplit('/', 1)[-1]} @ {BASE}: lines {a}-{b} (excerpt of {len(lines)})", numbered(lines[a - 1:b], a), f"{path}:{a}-{b}", BASE, "excerpt")

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
manifest = {"schema": "t21-packet-manifest/1", "pin": PIN, "sources": sources, "scan": scan, "summary": summary,
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
