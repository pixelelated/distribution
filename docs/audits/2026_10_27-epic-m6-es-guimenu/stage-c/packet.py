"""Build T26's Phase 4.6 packet and its manifest with the three-way scan (#673).

Usage: SECRET_PATTERNS=... python3 -I -B packet.py <worktree> <es tree> <out-packet.md> <out-manifest.json>

T21's builder (its stage-c/packet.py at 3ae9610b0's lane, itself T20's and
T18's), adapted: the slice is GuiMenu.{h,cpp} read from git at the pin; the
header goes whole; GuiMenu.cpp as line-numbered excerpts covering every line
02, 03 and 04 cite, the fork's added definitions (stage-a/defs.txt), the
fork's classes and the main menu's constructor, with 8 lines of context,
merged. The unchanged upstream regions the lens does not reach are trimmed
and the manifest names every range sent (D-WORKFLOW-195).

The mask and the three-way scan are T21's unchanged: the forbidden-terms
check (proven to run on a clean line), the push guard's SECRET_PATTERNS
proven to fire on a run-time fake line, and the credential-word scan by shape
class. No hit's text and no masked original is written. A `review` stops the
build.
"""
import hashlib, json, os, re, subprocess, sys

WT, ES, OUT, MANIFEST = sys.argv[1:5]
PIN, BR, BASE, T21 = "16dbac5211eea7e70db7394372033be2be7df829", "4b0ee281b5", "8ebaf8daad", "3ae9610b0"
A = "docs/audits/2026_10_27-epic-m6-es-guimenu"
GM = "es-app/src/guis/GuiMenu.cpp"
MASK = re.compile(r"((token|key|passw[a-z]*|psk|user)[=:])[^ ]*", re.I)
WORD = re.compile(r"key|pass|token|user|psk|secret|\bpin\b", re.I)
SP = os.environ.get("SECRET_PATTERNS", "")
assert SP, "SECRET_PATTERNS unset"
CTX = 8

# The fork's classes and the constructor, beside the added definitions read from stage-a/defs.txt.
GM_EXTRA = [(160, 277), (665, 690), (5420, 5600), (10364, 10512)]
NEIGHBOURS = {
    "es-app/src/guis/GuiSettings.cpp": [(80, 100), (167, 262), (391, 440)],
    "es-core/src/guis/GuiMsgBox.cpp": [(105, 135), (284, 296)],
    "es-core/src/utils/FileSystemUtil.cpp": [(138, 260), (1122, 1180)],
    "es-core/src/utils/Platform.cpp": [(853, 935)],
    "es-core/src/resources/TextureResource.cpp": [(84, 150)],
    "es-core/src/components/ImageComponent.cpp": [(327, 420)],
    "es-core/src/components/SwitchComponent.cpp": [(50, 67), (111, 163)],
    "es-core/src/components/ComponentList.cpp": [(142, 170)],
    "es-core/src/Settings.cpp": [(30, 62), (140, 150)],
    "es-core/src/components/IList.h": [(105, 120), (414, 420)],
    "es-core/src/utils/StringUtil.cpp": [(426, 445)],
    "es-app/src/CloudText.cpp": [(14, 40)],
}
SHELL = {
    "projects/ROCKNIX/packages/network/rclone/sources/cloud_remote": [(240, 345)],
    "projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth": [(798, 806), (878, 890), (2798, 2812)],
    "projects/ROCKNIX/packages/rocknix/sources/scripts/setrootpass": [(1, 60)],
    "projects/ROCKNIX/packages/rocknix/profile.d/001-functions": [(120, 175)],
    "projects/ROCKNIX/packages/rocknix/sources/scripts/setsettings.sh": [(715, 800)],
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


def gm_cites(texts):
    """Every `:N` or `:N-M` the analyses cite with no file named before it on the cell, read as GuiMenu.cpp's."""
    out = []
    for t in texts:
        for line in t.split("\n"):
            for m in re.finditer(r"(?<![\w.])`?:(\d{2,5})(?:-(\d{2,5}))?`?", line):
                pre = line[max(0, m.start() - 40):m.start()]
                if re.search(r"[A-Za-z_0-9]+\.(cpp|h|py|sh|md|po)$|[A-Za-z_]+$|-functions$|cloud_\w+$|setrootpass$", pre.rstrip("`")):
                    continue                           # another file's line
                a = int(m.group(1)); b = int(m.group(2) or a)
                if b >= a and b - a < 2000:
                    out.append((a, b))
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
    ('es-app/src/guis/GuiMenu.cpp', 3119): "code: `tokens` from splitting a script's output line",
    ('es-app/src/guis/GuiMenu.cpp', 3131): "code: `tokens` from splitting a script's output line",
    ('es-app/src/guis/GuiMenu.cpp', 3209): "code: a row built from `getRootPassword()`'s result, no literal (BATOCERA-only)",
    ('es-app/src/guis/GuiMenu.cpp', 3264): 'code: a setting read by its key name (`get("root.password")`)',
    ('es-app/src/guis/GuiMenu.cpp', 3269): 'code: a setting read by its key name (`get("root.password")`)',
    ('es-app/src/guis/GuiMenu.cpp', 4854): 'code: `key`, the prefix of the remembered ticks (`cloudsync.pick.`)',
    ('es-app/src/guis/GuiMenu.cpp', 7266): 'code: a loop counter named `pass`',
    ('es-app/src/guis/GuiMenu.cpp', 7268): 'code: a loop counter named `pass`',
    ('es-app/src/guis/GuiMenu.cpp', 7409): "comment: naming the form's fields the log masks",
    ('es-app/src/guis/GuiMenu.cpp', 8312): 'code: a setting read by its key name (`get("wifi.key")`)',
    ('es-app/src/guis/GuiMenu.cpp', 8341): 'code: a username read by its key name',
    ('es-app/src/guis/GuiMenu.cpp', 8342): 'code: a username read by its key name',
    ('es-app/src/guis/GuiMenu.cpp', 8401): 'code: a setting read by its key name (`get("root.password")`)',
    ('es-app/src/guis/GuiMenu.cpp', 10070): 'code: a setting read by its key name (`get("wifi.key")`)',
    ('es-app/src/guis/GuiMenu.cpp', 10106): 'code: a setting read by its key name (`get("wifi.key")`)',
    ('es-app/src/guis/GuiMenu.cpp', 10157): 'code: a setting read by its key name (`get("wifi.key")`)',
    ('projects/ROCKNIX/packages/rocknix/sources/scripts/setsettings.sh', 731): "code: upstream's public translation-service URL; the value after `api_key=` is the project's name and is masked",
    ('projects/ROCKNIX/packages/rocknix/sources/scripts/setrootpass', 25): 'prose: the script naming itself (`setrootpass:`) in its refusal message',
    ('docs/audits/2026_10_27-epic-m6-es-guimenu/02-forward-audit.md', 22): 'prose: the file name `setrootpass` with its line range',
    ('docs/decision-register.md', 7): "name: D-QA-021's prose naming rclone's field names and the read filter's own words",
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

brief = git("show", f"{BR}:docs/reviews/briefs/es-guimenu.md")
add("Context 1: the brief's § 4", re.search(r"^## 4\. The questions.*?(?=^## 5\.)", brief, re.S | re.M).group(0),
    "docs/reviews/briefs/es-guimenu.md § 4", BR, "context")
reg = worktree("docs/decision-register.md")
ids = ["D-UI-023", "D-UI-039", "D-UI-046", "D-UI-079", "D-CLOUD-175", "D-CLOUD-178", "D-CLOUD-179", "D-WORKFLOW-080",
       "D-WORKFLOW-195", "D-QA-021"]
rows = [l for l in reg.splitlines() if any(l.startswith(f"| {x} |") for x in ids)]
assert len(rows) == len(ids), (len(rows), len(ids))
add("Context 2: the register rows", "\n\n".join(rows), "docs/decision-register.md rows " + ", ".join(ids), "worktree", "context")

add("Evidence: stage-b/positives/getshoutput.out", worktree(f"{A}/stage-b/positives/getshoutput.out"),
    f"{A}/stage-b/positives/getshoutput.out", "worktree", "evidence")
GUEST = ["g01-identity.txt", "g01-tree-hashes.txt", "g02-ondevice.txt", "g03-scroll.txt", "g04-videofilter.txt",
         "g05-open-writes.txt", "g08-relink.txt", "g10-qr.txt", "g11-fr.txt", "g12-close.txt", "retired.txt"]
for n in GUEST:
    add(f"Evidence: guest-cycle/{n}", worktree(f"{A}/guest-cycle/{n}").replace("\r", ""), f"{A}/guest-cycle/{n}", "worktree", "evidence")

hdr = es(PIN, "es-app/src/guis/GuiMenu.h").splitlines()
add(f"es-app/src/guis/GuiMenu.h @ {PIN[:10]} (whole, {len(hdr)} lines)", numbered(hdr), "es-app/src/guis/GuiMenu.h", PIN, "slice file (whole)")

gm = es(PIN, GM).splitlines()
added = []
for l in worktree(f"{A}/stage-a/defs.txt").splitlines():
    f = l.split("\t")
    if len(f) == 5 and f[4] == "added":
        added.append((int(f[1]), int(f[2])))
assert len(added) == 97, len(added)
GM_RANGES = ranges(gm_cites(list(analyses.values())) + added + GM_EXTRA, len(gm))
sent = 0
for a, b in GM_RANGES:
    add(f"{GM} @ {PIN[:10]}: lines {a}-{b} (excerpt of {len(gm)})", numbered(gm[a - 1:b], a), f"{GM}:{a}-{b}", PIN, "excerpt")
    sent += b - a + 1

for path, spans in NEIGHBOURS.items():
    lines = es(PIN, path).splitlines()
    for a, b in ranges(spans, len(lines)):
        add(f"{path} @ {PIN[:10]}: lines {a}-{b} (excerpt of {len(lines)})", numbered(lines[a - 1:b], a), f"{path}:{a}-{b}", PIN, "excerpt")
t21 = subprocess.run(["git", "-C", ES, "diff", PIN, T21, "--", "es-app/src/guis/GuiSettings.cpp"], check=True, capture_output=True, text=True).stdout
add(f"T21's change to GuiSettings.cpp ({PIN[:10]}..{T21}, not in the pin)", t21, "es-app/src/guis/GuiSettings.cpp (diff)", T21, "context")
for path, spans in SHELL.items():
    lines = git("show", f"{BASE}:{path}").splitlines()
    for a, b in ranges(spans, len(lines)):
        add(f"{path.rsplit('/', 1)[-1]} @ {BASE}: lines {a}-{b} (excerpt of {len(lines)})", numbered(lines[a - 1:b], a), f"{path}:{a}-{b}", BASE, "excerpt")

body = "\n".join(parts) + "\n"
review = ([h for h in scan["mask"] if h["disposition"] == "review"] + [h for h in scan["secret_patterns"] if h["disposition"] == "review"]
          + [h for h in scan["words"] if h["class"] == "review"] + scan["forbidden"])
trimmed, prev = [], 0
for a, b in GM_RANGES:
    if a > prev + 1:
        trimmed.append([prev + 1, a - 1])
    prev = b
if prev < len(gm):
    trimmed.append([prev + 1, len(gm)])
summary = {
    "forbidden_terms_check": f"{len(scan['forbidden'])} section(s) with hits of {len(sources) - 1}; proven to run on a clean line",
    "secret_patterns": f"{len(scan['secret_patterns'])} line(s); proven to fire on a run-time fake line",
    "mask": f"{masked_total} line(s) masked; classes " + json.dumps(sorted({c for h in scan['mask'] for c in h['classes']})),
    "words": f"{len(scan['words'])} credential-word hit(s); classes " + json.dumps({k: sum(1 for h in scan['words'] if h['class'] == k) for k in sorted({h['class'] for h in scan['words']})}),
    "review": len(review),
    "guimenu_cpp": f"{sent} of {len(gm)} lines sent in {len(GM_RANGES)} excerpts; {len(gm) - sent} trimmed in {len(trimmed)} ranges",
}
manifest = {"schema": "t26-packet-manifest/1", "pin": PIN, "sources": sources, "scan": scan, "summary": summary,
            "guimenu_cpp": {"sent": [list(r) for r in GM_RANGES], "trimmed": trimmed},
            "packet": {"file": OUT.split("/")[-1], "bytes": len(body.encode()), "sha256": hashlib.sha256(body.encode()).hexdigest()}}
with open(MANIFEST, "w", encoding="utf-8") as s:
    json.dump(manifest, s, indent=1); s.write("\n")
if review:
    print(f"STOP: {len(review)} hit(s) need review; packet not written", file=sys.stderr)
    for h in review[:60]:
        src = next((x for x in sources if x["section"] == h.get("section")), {})
        print("  review:", src.get("path"), "line", h.get("line"), h.get("classes") or h.get("class") or h.get("result"), file=sys.stderr)
    sys.exit(1)
with open(OUT, "w", encoding="utf-8") as s:
    s.write(body)
print(len(sources), "sections;", len(body.encode()), "bytes;", json.dumps(summary))
