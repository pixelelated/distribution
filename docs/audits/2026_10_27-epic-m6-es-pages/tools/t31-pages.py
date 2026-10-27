"""One row per .cpp page of T31's slice: its class and base, what opens it, and what it starts (#678, § The pages).

    python3 -I t31-pages.py <es worktree> <commit> <paths.txt> <titles.md> <dialogs.md> <callers.txt>

Reads the sources at <commit> and the three tables the other generators wrote
(titles, dialogs, callers), so the row agrees with them by construction:
  - class and base: every `class X : public Y` in the file's header (a header
    that declares two classes lists both);
  - opened from: the callers table's files for the class;
  - starts: counts per file of runSystemCommand(, executeScript (Legacy and
    plain), std::thread, GuiLoading<, postToUiThread(, popen(, system( -- the
    census; which thread each runs on and its bound are written in 02 by
    reading each site;
  - dialogs: the dialogs table's sites in this file, each with where back lands;
  - title and map: the titles table's verdict.
Exits 1 when the .cpp page count is not 37 or a column's total disagrees with the
brief's runs (runSystemCommand 6, executeScript 5, std::thread 18,
GuiLoading< 18, postToUiThread 9 -- the brief counts lines of the .cpp and .h;
this tool counts the .cpp and .h of each page, comments excluded).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t31lib import in_comment_or_string, show  # noqa: E402

tree, commit, paths_file, titles_md, dialogs_md, callers_txt = sys.argv[1:7]
paths = [l.strip() for l in open(paths_file) if l.strip()]
COUNTS = [("runSystemCommand", r"\brunSystemCommand\s*\("), ("executeScript", r"\bexecuteScript(?:Legacy)?\s*\("),
          ("std::thread", r"\bstd::thread\b"), ("GuiLoading<", r"\bGuiLoading\s*<"), ("postToUiThread", r"\bpostToUiThread\s*\("),
          ("popen", r"(?<![\w.])popen\s*\("), ("system", r"(?<![\w.:>])system\s*\(")]
# popen 1, not the brief's 0: GuiMoonlight.cpp:42 writes `popen (` with a
# space, which the brief's `popen(` grep cannot see (corrected at stage B).
BRIEF = {"runSystemCommand": 6, "executeScript": 5, "std::thread": 18, "GuiLoading<": 18, "postToUiThread": 9, "popen": 1, "system": 0}

titles = {}
for line in open(titles_md):
    m = re.match(r"\| `([^`]+)` \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$", line)
    if m:
        titles[m.group(1)] = (m.group(2), m.group(3), m.group(4), m.group(5))
dialogs = {}
for line in open(dialogs_md):
    m = re.match(r"\| `([^:`]+):(\d+)` \| .*? \| (.*?) \| (.*?) \|", line)
    if m:
        dialogs.setdefault(m.group(1), []).append(":%s %s, back %s" % (m.group(2), m.group(3), m.group(4)))
callers = {}
for line in open(callers_txt):
    m = re.match(r"(\w+): \d+ line\(s\) in \d+ file\(s\)(?: -- (.*))?$", line.strip())
    if m:
        callers[m.group(1)] = sorted({c.split(":")[0] for c in (m.group(2) or "").replace(" ...", "").split(", ") if c})

totals = {k: 0 for k, _ in COUNTS}
rows = []
# A header with no .cpp beside it (GuiLoading.h, WifiScanProcess.h) is a row
# of its own, marked: it is no page, but what it starts counts.
units = [p for p in paths if p.endswith(".cpp")] + [p for p in paths if p.endswith(".h") and p[:-2] + ".cpp" not in paths]
for cpp in units:
    header_only = cpp.endswith(".h")
    stem = cpp.rsplit("/", 1)[1][:-2 if header_only else -4]
    texts = [show(tree, commit, cpp)] if not header_only else [""]
    header = cpp[:-4] + ".h" if not header_only else cpp
    htext = show(tree, commit, header) if header in paths else ""
    texts.append(htext)
    classes = re.findall(r"\bclass\s+(\w+)\s*(?:final\s*)?:\s*public\s+([\w:<>]+)", htext + "\n" + texts[0])
    counts = {}
    for k, pat in COUNTS:
        n = sum(1 for t in texts for m in re.finditer(pat, t) if not in_comment_or_string(t, m.start()))
        counts[k] = n
        totals[k] += n
    t = titles.get(stem + ".cpp", ("-", "-", "-", "-"))
    title = ", ".join(x for x in (t[0], t[1]) if x != "-") or ("not a _() literal: " + t[2] if t[2] != "-" else "-")
    starts = ", ".join("%s %d" % (k, v) for k, v in counts.items() if v) or "-"
    rows.append((stem + (" (header only)" if header_only else ""), "; ".join("%s : %s" % c for c in classes) or "-", ", ".join(callers.get(stem, [])) or "nothing",
                 starts, "; ".join(dialogs.get(stem + ".cpp", [])) or "-", title, t[3]))

print("| Page | Class : base | Opened from | Starts (census) | Dialogs (site, buttons, back) | Title | The map |")
print("| --- | --- | --- | --- | --- | --- | --- |")
for r in rows:
    print("| `%s` | %s | %s | %s | %s | %s | %s |" % tuple(x.replace("|", "\\|") for x in r))
print()
pages = sum(1 for r in rows if not r[0].endswith("(header only)"))
print("pages %d, header-only units %d; %s" % (pages, len(rows) - pages, ", ".join("%s %d" % kv for kv in totals.items())))
bad = ["%s %d, the brief's run %d" % (k, totals[k], v) for k, v in BRIEF.items() if totals[k] != v]
if pages != 37:
    bad.append("pages %d, expected 37" % pages)
if bad:
    print("FAIL t31-pages: " + "; ".join(bad))
    sys.exit(1)
