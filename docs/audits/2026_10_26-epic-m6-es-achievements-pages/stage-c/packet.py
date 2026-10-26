"""Build T20's Phase 4.6 packet and its manifest with the three-way scan (#667).

Usage: SECRET_PATTERNS=... python3 -I -B packet.py <worktree> <es tree> <out-packet.md> <out-manifest.json>

T18's builder (its stage-c/packet.py on feature/m6-es-cloud-pages-665), adapted:
the slice is the EmulationStation fork's, read from git at the pin; the control
script from the distribution at 8ebaf8daad; the order at 2174265e9c and the
brief at 14852bd6ed. Four offline sources and rvz_hash.cpp go whole; the
library as its diff against bccd715707; every other file as line-numbered
excerpts covering every line 02, 03 and 04 cite, with 8 lines of context,
merged. Trimmed from the start (D-WORKFLOW-195).

The mask and the three-way scan are T18's unchanged (see its header): the
forbidden-terms check (0 hits), the push guard's SECRET_PATTERNS proven to
fire on a run-time fake line, and the credential-word scan by shape class.
No hit's text and no masked original is written. A `review` stops the build.
"""
import hashlib, json, os, re, subprocess, sys

WT, ES, OUT, MANIFEST = sys.argv[1:5]
PIN, P1, BR, CTL = "16dbac5211eea7e70db7394372033be2be7df829", "2174265e9c", "14852bd6ed", "8ebaf8daad"
BASE = "bccd715707"
A = "docs/audits/2026_10_26-epic-m6-es-achievements-pages"
MASK = re.compile(r"((token|key|passw[a-z]*|psk|user)[=:])[^ ]*", re.I)
WORD = re.compile(r"key|pass|token|user|psk|secret|\bpin\b", re.I)
SP = os.environ.get("SECRET_PATTERNS", "")
assert SP, "SECRET_PATTERNS unset"

WHOLE = ["es-app/src/OfflineAchievements.cpp", "es-app/src/OfflineScanJob.cpp", "es-app/src/guis/GuiOfflineScan.cpp",
         "es-app/src/ThreadedHasher.cpp", "external/libcheevos/rvz_hash.cpp"]
LARGE = {"RetroAchievements.cpp": "es-app/src/RetroAchievements.cpp",
         "GuiRetroAchievementsSettings.cpp": "es-app/src/guis/GuiRetroAchievementsSettings.cpp",
         "GuiRetroAchievements.cpp": "es-app/src/guis/GuiRetroAchievements.cpp",
         "GuiGameAchievements.cpp": "es-app/src/guis/GuiGameAchievements.cpp",
         "OfflineScanJob.h": "es-app/src/OfflineScanJob.h", "ThreadedHasher.h": "es-app/src/ThreadedHasher.h",
         "ApiSystem.cpp": "es-app/src/ApiSystem.cpp", "HttpReq.cpp": "es-core/src/HttpReq.cpp", "HttpReq.h": "es-core/src/HttpReq.h",
         "CloudText.cpp": "es-app/src/CloudText.cpp", "CloudText.h": "es-app/src/CloudText.h",
         "ProxyCards.cpp": "es-app/src/ProxyCards.cpp", "FileSystemUtil.cpp": "es-core/src/utils/FileSystemUtil.cpp",
         "Settings.cpp": "es-core/src/Settings.cpp", "SystemConf.cpp": "es-core/src/SystemConf.cpp", "Paths.cpp": "es-core/src/Paths.cpp"}
# Lines the ask names beside those 02/03/04 cite.
EXTRA = {"RetroAchievements.cpp": [(134, 195), (290, 345), (500, 525), (740, 800), (850, 930), (1010, 1072)],
         "GuiRetroAchievementsSettings.cpp": [(140, 175), (310, 365), (440, 560), (596, 640), (690, 808)],
         "ApiSystem.cpp": [(2262, 2293)], "HttpReq.cpp": [(170, 240), (555, 570)], "HttpReq.h": [(40, 80)],
         "CloudText.cpp": [(1018, 1066), (1186, 1275), (1300, 1345)], "CloudText.h": [(480, 510)],
         "ProxyCards.cpp": [(190, 400), (560, 600)], "FileSystemUtil.cpp": [(1365, 1430)],
         "ThreadedHasher.h": [(1, 76)], "OfflineScanJob.h": [(1, 100)]}
CTL_PATH = "projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl"
CTL_RANGES = [(300, 400), (440, 660), (700, 870), (1119, 1200), (1700, 1830), (1965, 2110), (2137, 2265), (2400, 2455)]
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
DISPOSITIONS_T18 = {
    ("docs/decision-register.md", 21): "name: D-QA-021's prose naming rclone's `pass =`, `user =`, `token =`, `key =` (the read filter's own row)",
    ("es-app/src/ThreadedCloudSync.cpp", 123): "code: whyForToken compares a stamp's outcome token with a word (`token == \"folder-missing\"`)",
    ("es-app/src/ThreadedCloudSync.cpp", 124): "code: whyForToken compares a stamp's outcome token with a word",
    ("es-app/src/ThreadedCloudSync.cpp", 125): "code: whyForToken compares a stamp's outcome token with a word",
    ("es-app/src/ThreadedCloudSync.cpp", 126): "code: whyForToken compares a stamp's outcome token with a word",
    ("es-app/src/ThreadedCloudSync.cpp", 127): "code: whyForToken compares a stamp's outcome token with a word",
    ("es-app/src/CloudText.h", 108): "code: `bool knownToken = false;`, a member's initial value",
    ("docs/audits/2026_10_26-epic-m6-es-cloud-pages/02-forward-audit.md", 383): "prose: T2's report quoted, `Not a pass: the exit sync had no cloud to reach`",
}
DISPOSITIONS = {
    ('docs/decision-register.md', 9): "name: D-QA-021's prose naming rclone's field names and the read filter's own words",
    ('es-app/src/CloudText.cpp', 1024): 'code: a why token compared with a fixed word (`token == "WORD"`)',
    ('es-app/src/CloudText.cpp', 1026): 'code: a why token compared with a fixed word (`token == "WORD"`)',
    ('es-app/src/CloudText.cpp', 1028): 'code: a why token compared with a fixed word (`token == "WORD"`)',
    ('es-app/src/CloudText.cpp', 1030): 'code: a why token compared with a fixed word (`token == "WORD"`)',
    ('es-app/src/CloudText.cpp', 1032): 'code: a why token compared with a fixed word (`token == "WORD"`)',
    ('es-app/src/CloudText.cpp', 1034): 'code: a why token compared with a fixed word (`token == "WORD"`)',
    ('es-app/src/CloudText.cpp', 1036): 'code: a why token compared with a fixed word (`token == "WORD"`)',
    ('es-app/src/CloudText.cpp', 1041): 'code: a why token compared with a fixed word (`token == "WORD"`)',
    ('es-app/src/CloudText.cpp', 1047): 'code: a why token compared with a fixed word (`token == "WORD"`)',
    ('es-app/src/CloudText.cpp', 1052): 'code: a why token compared with a fixed word (`token == "WORD"`)',
    ('es-app/src/CloudText.cpp', 1059): 'code: a why token compared with a fixed word (`token == "WORD"`)',
    ('es-app/src/CloudText.cpp', 1061): 'code: a why token compared with a fixed word (`token == "WORD"`)',
    ('es-app/src/CloudText.cpp', 1229): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/CloudText.cpp', 1233): 'code: `bool token = !value.empty();`, a parse flag',
    ('es-app/src/CloudText.cpp', 1241): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/CloudText.cpp', 1245): 'code: `bool token = !value.empty();`, a parse flag',
    ('es-app/src/CloudText.cpp', 1255): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/CloudText.cpp', 1263): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/CloudText.cpp', 1264): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/CloudText.cpp', 1265): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/CloudText.cpp', 1266): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/CloudText.cpp', 1267): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/CloudText.cpp', 1268): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/CloudText.cpp', 1269): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/CloudText.cpp', 1270): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/CloudText.cpp', 1312): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/CloudText.cpp', 1314): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/CloudText.cpp', 1323): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/CloudText.cpp', 1328): 'code: a stamp field\'s key compared with its fixed name (`key == "name"`)',
    ('es-app/src/RetroAchievements.cpp', 145): 'code: a local variable read from a setting by its key name (`get("global.retroachievements.<name>")`)',
    ('es-app/src/RetroAchievements.cpp', 146): 'code: a local variable read from a setting by its key name (`get("global.retroachievements.<name>")`)',
    ('es-app/src/RetroAchievements.cpp', 198): 'code: a method signature (`GameInfoAndUserProgress::getImageUrl`)',
    ('es-app/src/RetroAchievements.cpp', 291): 'code: a local variable read from a setting by its key name (`get("global.retroachievements.<name>")`)',
    ('es-app/src/RetroAchievements.cpp', 771): "code: an exception's English message naming an API (`GetUserRankAndScore`)",
    ('es-app/src/RetroAchievements.cpp', 789): 'code: a member assigned a URL built from a field (`info.userpic`)',
    ('es-app/src/guis/GuiRetroAchievementsSettings.cpp', 601): 'code: a local variable read from a setting by its key name',
    ('es-app/src/guis/GuiRetroAchievementsSettings.cpp', 602): 'code: a local variable read from a setting by its key name',
    ('es-app/src/guis/GuiRetroAchievementsSettings.cpp', 746): 'code: a local variable read from a setting by its key name',
    ('es-app/src/guis/GuiRetroAchievementsSettings.cpp', 747): 'code: a local variable read from a setting by its key name',
    ('es-app/src/guis/GuiRetroAchievementsSettings.cpp', 748): 'code: a local variable read from a setting by its key name',
    ('es-core/src/Paths.cpp', 101): 'code: a path built from the home path (`getHomePath()`)',
    ('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl', 768): 'code: an SQL query by cache key with a bound parameter (`cacheKey = ?`)',
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
add("Context 1: docs/reviews/order.md § T20", re.search(r"^### T20\..*?(?=^### T21\.)", order, re.S | re.M).group(0),
    "docs/reviews/order.md § T20", P1, "context")
brief = git("show", f"{BR}:docs/reviews/briefs/es-achievements-pages.md")
add("Context 2: the brief's § 4", re.search(r"^## 4\. The questions.*?(?=^## 5\.)", brief, re.S | re.M).group(0),
    "docs/reviews/briefs/es-achievements-pages.md § 4", BR, "context")
reg = worktree("docs/decision-register.md")
ids = ["D-UI-028", "D-UI-030", "D-UI-035", "D-UI-078", "D-UI-095", "D-UI-107", "D-RA-001", "D-RA-010", "D-RA-012", "D-RA-013",
       "D-RA-050", "D-RA-051", "D-QA-015", "D-QA-016", "D-QA-021", "D-WORKFLOW-195"]
rows = [l for l in reg.splitlines() if any(l.startswith(f"| {x} |") for x in ids)]
assert len(rows) == len(ids), (len(rows), len(ids))
add("Context 3: the register rows", "\n\n".join(rows), "docs/decision-register.md rows " + ", ".join(ids), "worktree", "context")
t19 = git("show", "d8c02be1c9:docs/audits/2026_10_26-epic-m6-offline-achievements/02-forward-audit.md")
add("Context 4: T19's 02 § What T20 inherits (at d8c02be1c9)", re.search(r"^## What T20 inherits.*?(?=^## The streams)", t19, re.S | re.M).group(0),
    "T19 02 § What T20 inherits", "d8c02be1c9", "context")
for n in ("reader", "slice", "num", "stamp", "readall", "lfg"):
    add(f"Evidence: stage-b/positives/{n}.out", worktree(f"{A}/stage-b/positives/{n}.out"), f"{A}/stage-b/positives/{n}.out", "worktree", "evidence")
for n in ("g02-sh-exec.txt", "g05-l20-startup-offline.txt", "g06-l13.txt", "g07-l01-tls.txt"):
    add(f"Evidence: guest-cycle/{n}", worktree(f"{A}/guest-cycle/{n}"), f"{A}/guest-cycle/{n}", "worktree", "evidence")

for path in WHOLE:
    lines = es(path).splitlines()
    add(f"{path} @ {PIN[:10]} (whole, {len(lines)} lines)", numbered(lines), path, PIN, "slice file (whole)")
lib = subprocess.run(["git", "-C", ES, "diff", BASE, PIN, "--", "external/libcheevos/CMakeLists.txt", "external/libcheevos/cheevos.cpp",
                      "external/libcheevos/cheevos.h", "external/libcheevos/libretro-common/src/utils/md5.c",
                      "external/libcheevos/rcheevos/src/rhash/hash_disc.c"], check=True, capture_output=True, text=True).stdout
add(f"The library's five edits: git diff {BASE}..{PIN[:10]}", lib, "external/libcheevos (diff)", PIN, "slice diff")

c = cites(list(analyses.values()))
for name, path in LARGE.items():
    lines = es(path).splitlines()
    pairs = c[name] + EXTRA.get(name, [])
    if not pairs:
        continue
    for a, b in ranges(pairs, len(lines)):
        add(f"{path} @ {PIN[:10]}: lines {a}-{b} (excerpt of {len(lines)})", numbered(lines[a - 1:b], a), f"{path}:{a}-{b}", PIN, "excerpt")
ctl = git("show", f"{CTL}:{CTL_PATH}").splitlines()
for a, b in ranges(CTL_RANGES, len(ctl)):
    add(f"raofflineproxy-ctl @ {CTL}: lines {a}-{b} (excerpt of {len(ctl)})", numbered(ctl[a - 1:b], a), f"{CTL_PATH}:{a}-{b}", CTL, "excerpt")

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
manifest = {"schema": "t20-packet-manifest/1", "pin": PIN, "sources": sources, "scan": scan, "summary": summary,
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
