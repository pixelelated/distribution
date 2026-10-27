"""Compose 02-forward-audit.md from its template and the generators' tables (#679).

    python3 -I t32-02.py <audit folder> <es worktree> <commit> <paths.txt>

Substitutes, in stage-b/02-template.md:
  {{COVERAGE}}  one row per path (42): lines by grep -c (the inventory's
                rule), the inventory's tier (stage-a/membership.out's rows),
                the read's tier (the six files with a fork numstat are
                fork-modified; none is fork-added), the fork's numstat
                against cada856d86, and the leads naming the file (parsed
                from the template's own § The leads tables);
  {{VIEWS}} {{SCRAPERS}} {{SERVICES}} {{READS}} {{BOUNDS}} {{WORDS}}
                each generator's output, run here with its asserted counts.
Asserts 42 coverage rows, 6 fork-modified, 36 upstream-carried, 0
fork-added, and that every generator exits 0. Exits 1 on any difference,
writing nothing.
"""
import os
import re
import subprocess
import sys

A, W, C, PATHS = sys.argv[1:5]
T = os.path.join(A, "tools")
MB = "cada856d86"
tpl = open(os.path.join(A, "stage-b/02-template.md"), encoding="utf-8").read()
fail = []


def gen(script, *extra):
    r = subprocess.run([sys.executable, "-I", os.path.join(T, script), W, C, *extra], capture_output=True, text=True)
    if r.returncode:
        fail.append("%s exited %d: %s" % (script, r.returncode, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]))
    return r.stdout.rstrip("\n")


tables = {
    "VIEWS": gen("t32-views.py", "views=6,helpbars=2"),
    "SCRAPERS": gen("t32-scrapers.py", "scrapers=5,gated=3"),
    "SERVICES": gen("t32-services.py", "registrations=27,patterns=25,literal=16,allowed=27,posts=10"),
    "READS": gen("t32-reads.py", PATHS, "lines=49,calls=50,uncached=0"),
    "BOUNDS": gen("t32-bounds.py", PATHS, "constructions=9,new=7,stack=2,bounded=0"),
    "WORDS": gen("t32-words.py", PATHS, "lines=57,calls=69,msgids=50,empty=0,missing=0"),
}

paths = [l.strip() for l in open(PATHS) if l.strip()]
inv = {}
for line in open(os.path.join(A, "stage-a/membership.out")):
    m = re.match(r"^(\d+) (\S+) (fork-own|upstream-carried) (es-app/\S+)$", line.strip())
    if m:
        inv[m.group(4)] = (int(m.group(1)), m.group(3))
num = {}
for line in subprocess.run(["git", "-C", W, "diff", "--numstat", MB, C, "--"] + paths, capture_output=True, text=True, check=True).stdout.splitlines():
    a, r, p = line.split("\t")
    num[p] = (a, r)
added = subprocess.run(["git", "-C", W, "diff", "--diff-filter=A", "--name-only", "bccd715707", C, "--"] + paths, capture_output=True, text=True, check=True).stdout.split()
leads_text = tpl[tpl.index("## The leads"):tpl.index("## The views")]
rows, tiers = [], {"fork-modified": 0, "upstream-carried": 0, "fork-added": 0}
for p in paths:
    if p not in inv:
        fail.append("%s is not in the membership block's output" % p)
        continue
    lines, itier = inv[p]
    rtier = "fork-added" if p in added else ("fork-modified" if p in num else "upstream-carried")
    tiers[rtier] += 1
    base = os.path.basename(p)
    named = sorted(set(re.findall(r"\| (L-\d+|3\.\d+|\*\*3\.\d+\*\*) \|[^\n]*?" + re.escape(base), leads_text)))
    named = [n.strip("*") for n in named]
    rows.append("| `%s` | %d | %s | %s | %s | %s |" % (p, lines, itier, rtier, "%s/%s" % num[p] if p in num else "0/0", ", ".join(named) or "-"))
cov = "| Path | Lines (`grep -c`) | Inventory tier | Read tier | Fork +/- (against `cada856d86`) | Leads naming it |\n| --- | ---: | --- | --- | ---: | --- |\n" + "\n".join(rows)
cov += "\n\ngenerated, asserted: %d paths; read tiers fork-modified %d, upstream-carried %d, fork-added %d; inventory fork-own %d, upstream-carried %d" % (
    len(rows), tiers["fork-modified"], tiers["upstream-carried"], tiers["fork-added"],
    sum(1 for p in paths if inv.get(p, (0, ""))[1] == "fork-own"), sum(1 for p in paths if inv.get(p, (0, ""))[1] == "upstream-carried"))
if (len(rows), tiers["fork-modified"], tiers["upstream-carried"], tiers["fork-added"]) != (42, 6, 36, 0):
    fail.append("coverage %d rows, tiers %s; expected 42 and 6 / 36 / 0" % (len(rows), tiers))
tables["COVERAGE"] = cov
out = tpl
for k, v in tables.items():
    if "{{%s}}" % k not in out:
        fail.append("the template has no {{%s}}" % k)
    out = out.replace("{{%s}}" % k, v)
if "{{" in out:
    fail.append("an unfilled placeholder remains: " + re.search(r"\{\{\w+\}\}", out).group(0))
if fail:
    print("FAIL t32-02: " + "; ".join(fail))
    sys.exit(1)
open(os.path.join(A, "02-forward-audit.md"), "w", encoding="utf-8").write(out)
print("t32-02: coverage %d (fork-modified %d, upstream-carried %d, fork-added %d); views, scrapers, services, reads, bounds, words generated; wrote 02-forward-audit.md"
      % (len(rows), tiers["fork-modified"], tiers["upstream-carried"], tiers["fork-added"]))
