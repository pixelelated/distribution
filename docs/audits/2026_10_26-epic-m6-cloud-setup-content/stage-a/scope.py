# T17 (#664): the brief's section 2 membership block, as written.
import json, collections, os, fnmatch, re
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
sl = json.load(open("docs/reviews/slices.json"))
k17 = [s for s in sl["slices"] if s["k"] == 17][0]; sel = k17["select"]
def expand(g):
    mm = re.search(r'\{([^{}]*)\}', g)
    if not mm: return [g]
    return [x for alt in mm.group(1).split(",") for x in expand(g[:mm.start()] + alt + g[mm.end():])]
inc = [x for g in sel["globs"] if not g.startswith("!") for x in expand(g)]; exc = [x for g in sel["globs"] if g.startswith("!") for x in expand(g[1:])]
def m(p, g): return fnmatch.fnmatchcase(p, g) or (g.endswith("/**") and p.startswith(g[:-2]))
t17 = [r for r in rows if r["tree"] == "distribution" and any(m(r["path"], g) for g in inc) and not any(m(r["path"], g) for g in exc)]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t17), "lines", L(t17), dict(collections.Counter(r["reach"] for r in t17)), dict(collections.Counter(r["tier"] for r in t17)))
print(dict(collections.Counter(r["language"] for r in t17)), dict(collections.Counter(r["area"] for r in t17)))
rc = [r for r in rows if r["tree"] == "distribution" and r["path"].startswith("projects/ROCKNIX/packages/network/rclone/")]
print("the rclone directory in the inventory", len(rc), L(rc), "of which this slice's", sum(1 for r in rc if r in t17), L([r for r in rc if r in t17]))
os.makedirs(".qa-scratch/t17", exist_ok=True)
open(".qa-scratch/t17/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t17, key=lambda r: r["path"])))
for r in sorted(t17, key=lambda r: r["path"]): print(r["lines"], r["language"], r["tier"], r["path"])
