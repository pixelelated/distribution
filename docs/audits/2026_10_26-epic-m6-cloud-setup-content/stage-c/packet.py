"""Build T17's Phase 4.6 packet and its manifest with the three-way scan (#664).

Usage: SECRET_PATTERNS=... python3 -I -B packet.py <worktree> <out-packet.md> <out-manifest.json>

The 14 are read from git at `8ebaf8daad`; the order at `2174265e9c`, the brief
at `71ded3ac40`. Four files go whole (the recipe, the one writer of
rclone.conf, the argv path, the bounded rclone); the ten others as
line-numbered excerpts covering every line 02, 03, 04 and the brief cite, with
8 lines of context, merged; the fixtures as their docstrings with their
outputs; the brief's § 4 only (D-WORKFLOW-195's trimmed shape, from the start:
the 14 are 536,642 bytes, the first build of this packet 437,469, and Argon's
ceiling was met at 438 KB on T30).

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

WT, OUT, MANIFEST = sys.argv[1], sys.argv[2], sys.argv[3]
R, P1, BR = "8ebaf8daad", "2174265e9c", "71ded3ac40"
A = "docs/audits/2026_10_26-epic-m6-cloud-setup-content"
RC = "projects/ROCKNIX/packages/network/rclone/sources"
SW = "projects/ROCKNIX/packages/network/cloud-signin-window"
BT = "projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool"
MASK = re.compile(r"((token|key|passw[a-z]*|psk|user)[=:])[^ ]*", re.I)
WORD = re.compile(r"key|pass|token|user|psk|secret|\bpin\b", re.I)
SP = os.environ.get("SECRET_PATTERNS", "")
assert SP, "SECRET_PATTERNS unset"

WHOLE = [f"{SW}/package.mk", f"{RC}/cloud_connections.py", f"{RC}/cloud_remote", f"{RC}/cloud_content_transfer"]
# Lines the brief cites in the large six (§ 2 and § 4), beside those 02/03/04 cite (read below).
BRIEF = {"cloud_oauth": [80, (179, 193), 300, 357, 516, 861, 915, 2062, 2206, 2413, 2442, 2819],
         "cloud_setup": [53, (69, 112), 137, 394, 495, 537, 543, (775, 776), 797, 926, 937],
         "cloud_content_restore": [77, (235, 279), 528, (837, 838), (885, 1060), (1271, 1271), (1405, 1411), (1482, 1487)],
         "backuptool": [(224, 239), (487, 518), (551, 558), (649, 655), (1283, 1347), (1608, 1620), 1822, 1885],
         "cloud_content_backup": [40, (230, 232), 252, (583, 585)],
         "cloud-signin-window.c": [],
         "cloud_device_id": [(1, 30), (120, 160), (280, 310)],
         "cloud_folder_validate": [(1, 60), (85, 120)],
         "cloud_log_scrub": [(1, 30), (55, 190)],
         "cloud_scan": [(1, 60), (140, 175), (220, 362)]}
LARGE = {"cloud_oauth": f"{RC}/cloud_oauth", "cloud_setup": f"{RC}/cloud_setup", "cloud_content_restore": f"{RC}/cloud_content_restore",
         "backuptool": BT, "cloud_content_backup": f"{RC}/cloud_content_backup", "cloud-signin-window.c": f"{SW}/sources/cloud-signin-window.c",
         "cloud_device_id": f"{RC}/cloud_device_id", "cloud_folder_validate": f"{RC}/cloud_folder_validate",
         "cloud_log_scrub": f"{RC}/cloud_log_scrub", "cloud_scan": f"{RC}/cloud_scan"}
CTX = 8


def git(*args):
    return subprocess.run(["git", "-C", WT, *args], check=True, capture_output=True, text=True).stdout


def worktree(path):
    with open(f"{WT}/{path}", encoding="utf-8") as s:
        return s.read()


def numbered(lines, start=1, width=5):
    return "\n".join(f"{n:>{width}}  {l}" for n, l in enumerate(lines, start))


def cites(texts):
    pat = re.compile(r"`?(" + "|".join(re.escape(n) for n in LARGE) + r")`?:(\d+)(?:-(\d+))?((?:,\s*\d+(?:-\d+)?)*)")
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


# Hits the classifier sends to `review`, each read by shape (length, first and last two
# characters; never the text) on 2026-10-26 and dispositioned here by (path, line):
# a slice file's own line for an excerpt, else the section's line.
DISPOSITIONS = {
    (f"{A}/02-forward-audit.md", 264): "name: prose naming the scrubbed keys `.key=`, `.password=`, `.token=` (backtick-closed)",
    (f"{A}/02-forward-audit.md", 306): "name: prose `?pin=` naming the query parameter",
    (f"{A}/02-forward-audit.md", 375): "name: prose `key=value`, the word value",
    (f"{A}/02-forward-audit.md", 387): "synthetic: the fixture's percent-encoded non-ASCII PIN (one accented letter)",
    (f"{A}/03-retrospective.md", 59): "name: prose `key=value`, the word value",
    (f"{A}/04-analysis.md", 104): "count: `0 wrong of 163` follows the word key in `tools/vocabulary-check`'s neighbourhood",
    ("docs/decision-register.md", 3): "name: D-QA-021's prose naming rclone's `pass =`, `user =`, `token =`, `key =`",
    (f"{RC}/cloud_oauth", 1149): "code: a JavaScript `e.key === \"Escape\"` comparison",
    (f"{RC}/cloud_oauth", 2052): "prose: a docstring, `PIN: the handheld ...`",
    (f"{RC}/cloud_oauth", 2336): "prose: a comment, `?pin= is still`",
    (f"{RC}/cloud_oauth", 2641): "code: a format string `PIN=%s` printed from holder.pin at run time",
    (f"{RC}/cloud_setup", 937): "code: a console label `Password:` and a `${ROOTPASS:-<not set>}` expansion (F-07's finding is that it shows)",
    (f"{SW}/sources/cloud-signin-window.c", 544): "code: `event->keyval == GDK_KEY_Escape`",
    (f"{SW}/sources/cloud-signin-window.c", 639): "code: a GtkWidget variable named key, assigned from an expression",
    (f"{A}/tools/t17-pin-fixture.py", 21): "synthetic: the fixture's percent-encoded non-ASCII PIN",
    (f"{A}/tools/t17-pin-fixture.py", 92): "synthetic: the fixture's percent-encoded non-ASCII PIN",
    (f"{A}/tools/t17-pin-fixture.py", 96): "synthetic: the fixture's percent-encoded non-ASCII PIN",
    (f"{A}/stage-b/fixture-pin.txt", 7): "synthetic: the fixture's percent-encoded non-ASCII PIN",
}


def disposed(path, line):
    """By (path, line); for an excerpt `<file>:<a>-<b>` the line is the file's own."""
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
        scan["secret_patterns"].append({"section": sid, "line": ln, "disposition": "review"})
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
add("Context 1: docs/reviews/order.md § T17", re.search(r"^### T17\..*?(?=^### T18\.)", order, re.S | re.M).group(0),
    "docs/reviews/order.md § T17", P1, "context")
brief = git("show", f"{BR}:docs/reviews/briefs/cloud-setup-content.md")
add("Context 2: the brief's § 4 (its § 2, the scope, is 01's and 02's)", re.search(r"^## 4\. The questions.*?(?=^## 5\.)", brief, re.S | re.M).group(0),
    "docs/reviews/briefs/cloud-setup-content.md § 4", BR, "context")
reg = worktree("docs/decision-register.md")
ids = ["D-CLOUD-023", "D-CLOUD-141", "D-CLOUD-142", "D-CLOUD-149", "D-CLOUD-175", "D-CLOUD-178", "D-CLOUD-179", "D-QA-021", "D-WORKFLOW-195"]
rows = [l for l in reg.splitlines() if any(l.startswith(f"| {x} |") for x in ids)]
assert len(rows) == len(ids), (len(rows), len(ids))
add("Context 3: the register rows", "\n\n".join(rows), "docs/decision-register.md rows " + ", ".join(ids), "worktree", "context")
add("Context 4: the interface's why table and its log of cloud_remote (ES pin 16dbac5211, read only)",
    worktree(f"{A}/stage-b/es-why-sentences.txt") + "\n" + worktree(f"{A}/stage-b/es-cloud-remote-log.txt"),
    f"{A}/stage-b/es-why-sentences.txt + es-cloud-remote-log.txt", "worktree", "context")

for path in WHOLE:
    lines = git("show", f"{R}:{path}").splitlines()
    add(f"{path} @ {R} (whole, {len(lines)} lines)", numbered(lines), path, R, "slice file (whole)")

c = cites(list(analyses.values()))
for name, path in LARGE.items():
    lines = git("show", f"{R}:{path}").splitlines()
    pairs = c[name] + [x if isinstance(x, tuple) else (x, x) for x in BRIEF[name]]
    for a, b in ranges(pairs, len(lines)):
        add(f"{path} @ {R}: lines {a}-{b} (excerpt of {len(lines)})", numbered(lines[a - 1:b], a), f"{path}:{a}-{b}", R, "excerpt")

for t in ("pin", "content", "archive", "mode"):
    src = worktree(f"{A}/tools/t17-{t}-fixture.py"); doc = src[:src.index('"""', src.index('"""') + 3) + 3]
    add(f"Fixture: tools/t17-{t}-fixture.py (its docstring; the code runs the product's own functions)", doc,
        f"{A}/tools/t17-{t}-fixture.py (docstring)", "worktree", "fixture")
    add(f"Fixture output: stage-b/fixture-{t}.txt", worktree(f"{A}/stage-b/fixture-{t}.txt"), f"{A}/stage-b/fixture-{t}.txt", "worktree", "fixture")

body = "\n".join(parts) + "\n"
review = ([h for h in scan["mask"] if h["disposition"] == "review"] + scan["secret_patterns"]
          + [h for h in scan["words"] if h["class"] == "review"] + scan["forbidden"])
summary = {
    "forbidden_terms_check": f"{len(scan['forbidden'])} section(s) with hits of {len(sources) - 1}; proven to run on a clean line",
    "secret_patterns": f"{len(scan['secret_patterns'])} line(s); proven to fire on a run-time fake line",
    "mask": f"{masked_total} line(s) masked; classes " + json.dumps(sorted({c for h in scan['mask'] for c in h['classes']})),
    "words": f"{len(scan['words'])} credential-word hit(s); classes " + json.dumps({k: sum(1 for h in scan['words'] if h['class'] == k) for k in sorted({h['class'] for h in scan['words']})}),
    "review": len(review),
}
manifest = {"schema": "t17-packet-manifest/1", "commit": R, "sources": sources, "scan": scan, "summary": summary,
            "packet": {"file": OUT.split("/")[-1], "bytes": len(body.encode()), "sha256": hashlib.sha256(body.encode()).hexdigest()}}
with open(MANIFEST, "w", encoding="utf-8") as s:
    json.dump(manifest, s, indent=1); s.write("\n")
if review:
    print(f"STOP: {len(review)} hit(s) need review; packet not written", file=sys.stderr)
    sys.exit(1)
with open(OUT, "w", encoding="utf-8") as s:
    s.write(body)
print(len(sources), "sections;", len(body.encode()), "bytes;", json.dumps(summary))
