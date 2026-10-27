"""Compose 02-forward-audit.md from its template and the generators' tables (#680; T32's t32-02.py, #679, adapted).

    python3 -I t33-02.py <audit folder> <es worktree> <commit> <paths.txt>

Substitutes, in stage-b/02-template.md:
  {{COVERAGE}}  one row per path (77): lines by `grep -c ''` (the
                inventory's rule: a last line with no newline counts), the
                read tier from `git diff` against the fork's base
                bccd715707 (added: fork-added; modified: fork-modified;
                else upstream-carried), the inventory tier (fork-own for
                the first two), the fork's numstat against bccd715707, and
                the leads naming the file (parsed from the template's own
                § The leads tables);
  {{LIBRARY}} {{HELPERS}} {{WRITES}} {{READS}} {{BOUNDS}} {{WORDS}}
                each generator's output, run here with its asserted counts.
Asserts 77 coverage rows, read tiers 27 / 4 / 46, inventory 31 / 46, and
that every generator exits 0. Exits 1 on any difference, writing nothing.
"""
import os
import re
import subprocess
import sys

A, W, C, PATHS = sys.argv[1:5]
T = os.path.join(A, "tools")
BASE = "bccd715707"
tpl = open(os.path.join(A, "stage-b/02-template.md"), encoding="utf-8").read()
fail = []


def gen(script, *extra):
    r = subprocess.run([sys.executable, "-I", os.path.join(T, script), W, C, *extra], capture_output=True, text=True)
    if r.returncode:
        fail.append("%s exited %d: %s" % (script, r.returncode, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]))
    return r.stdout.rstrip("\n")


tables = {
    "LIBRARY": gen("t33-library.py", PATHS, "units=11"),
    "HELPERS": gen("t33-helpers.py", PATHS, "units=17,cases=12,built=7,files=27"),
    "WRITES": gen("t33-writes.py", PATHS, "lines=11"),
    "READS": gen("t33-reads.py", PATHS, "lines=83,calls=86,uncached=4"),
    "BOUNDS": gen("t33-bounds.py", PATHS, "http=4,process=6,waits=4,bounded=1"),
    "WORDS": gen("t33-words.py", PATHS, "lines=176,calls=223,msgids=196,empty=0,missing=0"),
}

paths = [l.strip() for l in open(PATHS) if l.strip()]
num = {}
for line in subprocess.run(["git", "-C", W, "diff", "--numstat", BASE, C, "--"] + paths, capture_output=True, text=True, check=True).stdout.splitlines():
    a, r, p = line.split("\t")
    num[p] = (a, r)
added = set(subprocess.run(["git", "-C", W, "diff", "--diff-filter=A", "--name-only", BASE, C, "--"] + paths, capture_output=True, text=True, check=True).stdout.split())
leads_text = tpl[tpl.index("## The leads"):tpl.index("## The library")]
rows, tiers, inv = [], {"fork-added": 0, "fork-modified": 0, "upstream-carried": 0}, {"fork-own": 0, "upstream-carried": 0}
for p in paths:
    data = subprocess.run(["git", "-C", W, "show", "%s:%s" % (C, p)], capture_output=True, check=True).stdout
    lines = data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)
    rtier = "fork-added" if p in added else ("fork-modified" if p in num else "upstream-carried")
    itier = "upstream-carried" if rtier == "upstream-carried" else "fork-own"
    tiers[rtier] += 1
    inv[itier] += 1
    base = os.path.basename(p)
    named = sorted(set(n.strip("*") for n in re.findall(r"\| (L-\d+|\*\*3\.\d+\*\*|3\.\d+) \|[^\n]*?`" + re.escape(base) + r"[`:]", leads_text)),
                   key=lambda n: (n.startswith("3."), float(n[2:]) if n.startswith("L-") else float(n.split(".")[1])))
    rows.append("| `%s` | %d | %s | %s | %s | %s |" % (p, lines, itier, rtier, "%s/%s" % num[p] if p in num else "0/0", ", ".join(named) or "-"))
cov = "| Path | Lines (`grep -c ''`) | Inventory tier | Read tier | Fork +/- (against `%s`) | Leads naming it |\n| --- | ---: | --- | --- | ---: | --- |\n" % BASE + "\n".join(rows)
cov += "\n\ngenerated, asserted: %d paths; read tiers fork-added %d, fork-modified %d, upstream-carried %d; inventory fork-own %d, upstream-carried %d" % (
    len(rows), tiers["fork-added"], tiers["fork-modified"], tiers["upstream-carried"], inv["fork-own"], inv["upstream-carried"])
if (len(rows), tiers["fork-added"], tiers["fork-modified"], tiers["upstream-carried"], inv["fork-own"]) != (77, 27, 4, 46, 31):
    fail.append("coverage %d rows, tiers %s, inventory %s; expected 77, 27 / 4 / 46, 31 / 46" % (len(rows), tiers, inv))
tables["COVERAGE"] = cov
out = tpl
for k, v in tables.items():
    if "{{%s}}" % k not in out:
        fail.append("the template has no {{%s}}" % k)
    out = out.replace("{{%s}}" % k, v)
if "{{" in out:
    fail.append("an unfilled placeholder remains: " + re.search(r"\{\{\w+\}\}", out).group(0))
if fail:
    print("FAIL t33-02: " + "; ".join(fail))
    sys.exit(1)
open(os.path.join(A, "02-forward-audit.md"), "w", encoding="utf-8").write(out)
print("t33-02: coverage %d (fork-added %d, fork-modified %d, upstream-carried %d; inventory %d / %d); library, helpers, writes, reads, bounds, words generated; wrote 02-forward-audit.md"
      % (len(rows), tiers["fork-added"], tiers["fork-modified"], tiers["upstream-carried"], inv["fork-own"], inv["upstream-carried"]))
