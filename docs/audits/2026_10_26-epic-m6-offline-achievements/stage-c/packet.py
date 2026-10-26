"""Build T19's Phase 4.6 packet and its manifest with the three-way scan (#666).

Usage: SECRET_PATTERNS=... python3 -I -B packet.py <worktree> <patched proxy tree> <es tree> <out-packet.md> <out-manifest.json>

T18's builder (its stage-c/packet.py on feature/m6-es-cloud-pages-665),
adapted: the slice is the distribution's, read from git at 8ebaf8daad; the
upstream proxy is the cache's tarball at its pin, patched 18 of 18 at fuzz 0
(stage-a/unpack.txt); the order at 2174265e9c and the brief at 110943c58c.
The helpers, the unit and the daemon file go whole and line-numbered; five patches whole; the patched
upstream modules and EmulationStation's CloudText.cpp as line-numbered
excerpts of every line 02, 03 and 04 cite, with 8 lines of context, merged.
Trimmed (D-WORKFLOW-195): 407 KB at the first build (the ctl, the helpers,
the recipe and eight patches whole); 372 KB with the recipe and the image
helper as excerpts, patches 010, 012 and 015 out (the patched network.py's
bounded lookup in their place) and the brief's § 4 out (the ask carries the
questions); the ctl as excerpts of every cited line and the functions the
four families turn on, for the size T18's Argon met (348 KB).

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

WT, SRC, ES, OUT, MANIFEST = sys.argv[1:6]
C, P1, BR, ESPIN = "8ebaf8daad", "2174265e9c", "110943c58c", "16dbac5211eea7e70db7394372033be2be7df829"
PIN = C
A = "docs/audits/2026_10_26-epic-m6-offline-achievements"
PK = "projects/ROCKNIX/packages/network/raofflineproxy"
MASK = re.compile(r"((token|key|passw[a-z]*|psk|user)[=:])[^ ]*", re.I)
WORD = re.compile(r"key|pass|token|user|psk|secret|\bpin\b", re.I)
SP = os.environ.get("SECRET_PATTERNS", "")
assert SP, "SECRET_PATTERNS unset"

WHOLE = [f"{PK}/sources/raofflineproxy-refresh",
         f"{PK}/sources/raofflineproxy-cache-indexed", f"{PK}/system.d/raofflineproxy.service", f"{PK}/daemons/006-raofflineproxy"]
PATCHES = ["001-dorequest-4xx-passthrough", "007-cached-sign-in-of-the-configured-account", "008-log-upload-opt-in",
           "011-offline-login-header", "013-validate-a-cached-image-before-publishing-it"]
UP = "linux/raofflineproxy"
LARGE = {"proxy_service.py": f"{UP}/proxy_service.py", "auth.py": f"{UP}/auth.py", "network.py": f"{UP}/network.py",
         "storage.py": f"{UP}/storage.py", "utils.py": f"{UP}/utils.py", "log_uploader.py": f"{UP}/log_uploader.py",
         "usage_report.py": f"{UP}/usage_report.py", "config.py": f"{UP}/config.py", "es_export.py": f"{UP}/es_export.py",
         "CloudText.cpp": "es-app/src/CloudText.cpp",
         "cache-images": f"{PK}/sources/raofflineproxy-cache-images", "package.mk": f"{PK}/package.mk", "ctl": f"{PK}/sources/raofflineproxy-ctl"}
# Lines the ask names beside those 02/03/04 cite: the request path and the
# offline login whole, the credential resolution, the POST and GET paths.
EXTRA = {"proxy_service.py": [(268, 340), (440, 510), (1405, 1440), (1460, 1506)], "auth.py": [(1, 143)],
         "network.py": [(20, 40), (255, 345), (360, 420), (516, 580)], "storage.py": [(70, 160)], "utils.py": [(100, 130)],
         "usage_report.py": [(20, 60), (150, 200)], "log_uploader.py": [(1, 30), (60, 130), (354, 380)],
         "CloudText.cpp": [(1022, 1064), (1186, 1275), (1305, 1335)],
         "cache-images": [(1, 30), (134, 212), (271, 320), (395, 480)], "package.mk": [(1, 33), (116, 157)],
         # The ctl as excerpts: every line 02, 03 and 04 cite (as `ctl :N`, which cites() does not parse) and the
         # functions the four families turn on whole; checked against the cited set before the build.
         "ctl": [(1, 40), (255, 380), (405, 570), (590, 660), (754, 1035), (1060, 1300), (1410, 1440), (1660, 1965),
                 (1960, 2120), (2140, 2455)]}
CTX = 8


def git(*args):
    return subprocess.run(["git", "-C", WT, *args], check=True, capture_output=True, text=True).stdout


def dist(path):
    return git("show", f"{C}:{path}")


def up(path):
    if path.startswith("projects/"):
        return dist(path)
    if path.startswith("es-app/"):
        return subprocess.run(["git", "-C", ES, "show", f"{ESPIN}:{path}"], check=True, capture_output=True, text=True).stdout
    with open(f"{SRC}/{path}", encoding="utf-8") as s:
        return s.read()

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
    ('docs/audits/2026_10_26-epic-m6-offline-achievements/02-forward-audit.md', 46): "prose: the unit directive `User=` named in the first reader's text",
    ('docs/audits/2026_10_26-epic-m6-offline-achievements/02-forward-audit.md', 273): "prose: the unit directive `User=` named in the first reader's text",
    ('docs/audits/2026_10_26-epic-m6-offline-achievements/02-forward-audit.md', 322): "prose: the unit directive `User=` named in the first reader's text",
    ('docs/audits/2026_10_26-epic-m6-offline-achievements/02-forward-audit.md', 163): "prose: `at the pin:` followed by the public tarball's sha256 (= PKG_SHA256)",
    ('docs/audits/2026_10_26-epic-m6-offline-achievements/02-forward-audit.md', 291): 'prose: `older than the pin:` followed by words',
    ('docs/reviews/briefs/offline-achievements-proxy.md', 45): "prose: the brief's Q5, `at the pin:` followed by words",
    ('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl', 768): 'code: an SQL `cacheKey = ?` placeholder',
    ('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl', 1021): 'code: an SQL `cacheKey = ?` placeholder',
    ('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl', 1493): 'code: an SQL `cacheKey = ?` placeholder',
    ('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl', 1615): "code: the walk's boolean `passed`",
    ('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl', 1644): "code: the walk's boolean `passed`",
    ('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl', 1657): "code: the walk's boolean `passed`",
    ('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl', 1849): 'code: the name IMAGE_PASS_SECONDS and its default expansion',
    ('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl', 1855): 'comment: `no pass:` followed by words',
    ('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl', 2336): 'code: a log line `pass: cached=${...}`',
    ('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed', 57): 'code: the type annotation `user_agent: str`',
    ('projects/ROCKNIX/packages/network/raofflineproxy/patches/012-offline-image-miss.patch', 93): 'code: the type annotation `user_agent: str`',
    ('projects/ROCKNIX/packages/network/raofflineproxy/patches/013-validate-a-cached-image-before-publishing-it.patch', 54): 'code: the type annotation `user_agent: str`',
    ('projects/ROCKNIX/packages/network/raofflineproxy/patches/013-validate-a-cached-image-before-publishing-it.patch', 67): 'code: the type annotation `user_agent: str`',
    ('projects/ROCKNIX/packages/network/raofflineproxy/patches/015-bounded-name-lookup.patch', 156): 'code: the type annotation `user_agent: str`',
    ('linux/raofflineproxy/proxy_service.py', 260): 'code: the type annotation `user_agent: str | None`',
    ('linux/raofflineproxy/auth.py', 31): 'code: the parameter `user_agent: str = FALLBACK_USER_AGENT`',
    ('linux/raofflineproxy/auth.py', 139): 'code: a log format string `user=%s` and its argument',
    ('linux/raofflineproxy/network.py', 334): 'code: the type annotation `user_agent: str | None`',
    ('linux/raofflineproxy/network.py', 367): 'code: the type annotation `user_agent: str`',
    ('linux/raofflineproxy/storage.py', 153): 'code: an SQL trigger `cacheKey = new.cacheKey`',
    ('linux/raofflineproxy/usage_report.py', 47): 'code: the parameter `username: str`',
    ('es-app/src/CloudText.cpp', 1024): 'code: scanWhy/topUpWhy compare a why token with a word (`token == "..."`)',
    ('es-app/src/CloudText.cpp', 1026): 'code: scanWhy/topUpWhy compare a why token with a word (`token == "..."`)',
    ('es-app/src/CloudText.cpp', 1028): 'code: scanWhy/topUpWhy compare a why token with a word (`token == "..."`)',
    ('es-app/src/CloudText.cpp', 1030): 'code: scanWhy/topUpWhy compare a why token with a word (`token == "..."`)',
    ('es-app/src/CloudText.cpp', 1032): 'code: scanWhy/topUpWhy compare a why token with a word (`token == "..."`)',
    ('es-app/src/CloudText.cpp', 1034): 'code: scanWhy/topUpWhy compare a why token with a word (`token == "..."`)',
    ('es-app/src/CloudText.cpp', 1036): 'code: scanWhy/topUpWhy compare a why token with a word (`token == "..."`)',
    ('es-app/src/CloudText.cpp', 1041): 'code: scanWhy/topUpWhy compare a why token with a word (`token == "..."`)',
    ('es-app/src/CloudText.cpp', 1047): 'code: scanWhy/topUpWhy compare a why token with a word (`token == "..."`)',
    ('es-app/src/CloudText.cpp', 1052): 'code: scanWhy/topUpWhy compare a why token with a word (`token == "..."`)',
    ('es-app/src/CloudText.cpp', 1059): 'code: scanWhy/topUpWhy compare a why token with a word (`token == "..."`)',
    ('es-app/src/CloudText.cpp', 1061): 'code: scanWhy/topUpWhy compare a why token with a word (`token == "..."`)',
    ('es-app/src/CloudText.cpp', 1229): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1233): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1241): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1245): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1255): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1263): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1264): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1265): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1266): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1267): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1268): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1269): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1270): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1312): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1314): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1323): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
    ('es-app/src/CloudText.cpp', 1328): 'code: the stamp parsers compare a field\'s key with a word (`key == "..."`)',
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
add("Context 1: docs/reviews/order.md § T19", re.search(r"^### T19\..*?(?=^### T20\.)", order, re.S | re.M).group(0),
    "docs/reviews/order.md § T19", P1, "context")

for path in WHOLE:
    lines = dist(path).splitlines()
    add(f"{path} @ {C} (whole, {len(lines)} lines)", numbered(lines), path, C, "slice file (whole)")
for name in PATCHES:
    path = f"{PK}/patches/{name}.patch"
    add(f"{path} @ {C} (whole)", dist(path), path, C, "patch (whole)")

c = cites(list(analyses.values()))
for name, path in LARGE.items():
    lines = up(path).splitlines()
    pairs = c[name] + EXTRA.get(name, [])
    ref = ESPIN[:10] if path.startswith("es-app/") else (C if path.startswith("projects/") else "c7ebd1b6e7+18")
    for a, b in ranges(pairs, len(lines)):
        add(f"{path} @ {ref}: lines {a}-{b} (excerpt of {len(lines)})", numbered(lines[a - 1:b], a), f"{path}:{a}-{b}", ref, "excerpt")

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
manifest = {"schema": "t19-packet-manifest/1", "pin": PIN, "sources": sources, "scan": scan, "summary": summary,
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
