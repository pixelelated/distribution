#!/usr/bin/env python3
"""T26 (#673): the merge debt -- what ROCKNIX changed in GuiMenu.cpp since the
merge base, against the fork's own hunks.

    python3 -I t26-merge.py <ES checkout> <base> <upstream ref> <pin> [--table]

Method, stated so the figures can be checked:
- The fork's hunks are `git diff -U0 <base> <pin>` over the file, in the
  base's line numbers.
- Each upstream commit that is not a merge (`git log --reverse --no-merges
  <base>..<upstream>` over the file) is diffed against its parent with
  `-U0` (a merge's first-parent diff repeats its side's commits, so merges
  are listed and counted, not diffed); its hunks are mapped to the base's
  line numbers through `git diff -U0 <base> <parent>` (a line inside a region
  the earlier commits changed maps to that region's start).
- An upstream hunk **meets** the fork when its base range, widened by three
  lines each side, overlaps a fork hunk's base range: git's merge needs the
  context lines unchanged, so such a hunk conflicts or needs reading. A hunk
  that meets nothing probably merges cleanly.
- Functions are `t26-defs.py`'s definitions of the base file, named for the
  base lines a hunk covers.
Exits 1 when a figure drifts from the counts asserted below.
"""
import importlib.util, os, re, subprocess, sys, tempfile, collections

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("t26defs", os.path.join(HERE, "t26-defs.py"))
t26defs = importlib.util.module_from_spec(spec); spec.loader.exec_module(t26defs)
EXPECT = {"commits": 9, "merges": 1, "upstream-hunks": 15, "meeting": 8, "fork-hunks": 148}
F = "es-app/src/guis/GuiMenu.cpp"
es, base, up, pin = sys.argv[1:5]

def git(*a):
    p = subprocess.run(["git", "-C", es] + list(a), capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("git %s: %s" % (" ".join(a), p.stderr.strip()))
    return p.stdout
HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", re.M)
def hunks(a, b):
    out = []
    for m in HUNK.finditer(git("diff", "-U0", a, b, "--", F)):
        os_, ol, ns, nl = int(m.group(1)), int(m.group(2) or 1), int(m.group(3)), int(m.group(4) or 1)
        out.append((os_, ol, ns, nl))
    return out
def to_base(hs, n):
    """Map a line number of the newer side of hunks hs to the older side."""
    off = 0
    for os_, ol, ns, nl in hs:
        if n < ns:
            break
        if n < ns + max(nl, 1):
            return os_                 # inside a changed region: its start
        off = (os_ + ol) - (ns + nl)
    return n + off

fork = hunks(base, pin)
with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as td:
    bp = os.path.join(td, "base.cpp"); open(bp, "w").write(git("show", "%s:%s" % (base, F)))
    bdefs = t26defs.definitions(bp)
fn = lambda a, b: sorted({d["name"].replace("GuiMenu::", "") for d in bdefs if d["start"] <= b and d["end"] >= a}) or ["(file scope)"]
allc = git("log", "--reverse", "--format=%H %ad %s", "--date=short", "%s..%s" % (base, up), "--", F).strip().split("\n")
commits = git("log", "--reverse", "--no-merges", "--format=%H %ad %s", "--date=short", "%s..%s" % (base, up), "--", F).strip().split("\n")
merges = [c for c in allc if c not in commits]
rows = []
for c in commits:
    h, date, subj = c.split(" ", 2)
    parent = git("rev-parse", h + "^").strip()
    pre = hunks(base, parent) if parent != git("rev-parse", base).strip() else []
    for os_, ol, ns, nl in hunks(parent, h):
        a = to_base(pre, os_); b = to_base(pre, os_ + max(ol, 1) - 1)
        meet = [f for f in fork if not (f[0] + max(f[1], 1) - 1 < a - 3 or f[0] > b + 3)]
        rows.append({"commit": h[:9], "date": date, "subject": subj, "base": (a, b), "del": ol, "add": nl,
                     "meets": meet, "funcs": fn(a, b)})
got = {"commits": len(allc), "merges": len(merges), "upstream-hunks": len(rows), "meeting": len([r for r in rows if r["meets"]]), "fork-hunks": len(fork)}
if "--table" in sys.argv:
    print("| Upstream commit | Date | Base lines | -/+ | Functions (base) | Fork hunks it meets |")
    print("| --- | --- | ---: | ---: | --- | --- |")
    for r in rows:
        print("| `%s` %s | %s | %d-%d | -%d/+%d | %s | %s |" % (r["commit"], r["subject"][:60].replace("|", "\\|"), r["date"], r["base"][0], r["base"][1],
              r["del"], r["add"], ", ".join("`%s`" % f for f in r["funcs"]),
              "; ".join("base %d-%d (-%d/+%d)" % (f[0], f[0] + max(f[1], 1) - 1, f[1], f[3]) for f in r["meets"]) or "none"))
print("upstream commits %d (%d merge(s): %s); the %d others' hunks %d, of which %d meet a fork hunk; fork hunks %d"
      % (got["commits"], len(merges), ", ".join(m[:9] for m in merges) or "none", len(commits), got["upstream-hunks"], got["meeting"], got["fork-hunks"]))
bycommit = collections.OrderedDict()
for r in rows:
    k = "%s %s" % (r["commit"], r["subject"][:50]); bycommit.setdefault(k, [0, 0]); bycommit[k][0] += 1; bycommit[k][1] += bool(r["meets"])
for k, (n, m) in bycommit.items():
    print("  %s: %d hunk(s), %d meeting the fork" % (k, n, m))
drift = {k: (got[k], EXPECT[k]) for k in EXPECT if got[k] != EXPECT[k]}
if drift:
    print("DRIFT (got, asserted):", drift); sys.exit(1)
print("asserted counts hold")
