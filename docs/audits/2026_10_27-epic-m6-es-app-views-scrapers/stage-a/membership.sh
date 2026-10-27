python3 -I - <<'PY'
import json, collections, os, fnmatch, re
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
sl = json.load(open("docs/reviews/slices.json"))
k = [s for s in sl["slices"] if s["k"] == 32][0]; sels = k["select"] if isinstance(k["select"], list) else [k["select"]]
def expand(g):
    mm = re.search(r'\{([^{}]*)\}', g)
    if not mm: return [g]
    return [x for alt in mm.group(1).split(",") for x in expand(g[:mm.start()] + alt + g[mm.end():])]
def m(p, g): return fnmatch.fnmatchcase(p, g) or (g.endswith("/**") and p.startswith(g[:-2]))
def pick(sel):
    globs = sel.get("globs") or []; tiers = sel.get("tier"); areas = sel.get("areas") or [k["area"]]
    inc = [x[3:] for g in globs if g.startswith("es:") for x in expand(g)]
    exc = [x[4:] for g in globs if g.startswith("!es:") for x in expand(g)]
    return [r for r in rows if r["tree"] == "es" and r["area"] in areas and any(m(r["path"], g) for g in inc) and not any(m(r["path"], g) for g in exc) and (not tiers or r["tier"] in tiers)]
t32 = []
for sel in sels:
    for r in pick(sel):
        if r not in t32: t32.append(r)
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("selects", len(sels), "paths", len(t32), "lines", L(t32), dict(collections.Counter(r["reach"] for r in t32)), dict(collections.Counter(r["tier"] for r in t32)))
print(dict(collections.Counter(r["language"] for r in t32)))
print("fork-own lines by inventory tier:", L([r for r in t32 if r["tier"] == "fork-own"]))
os.makedirs(".qa-scratch/t32", exist_ok=True)
open(".qa-scratch/t32/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t32, key=lambda r: r["path"])))
for r in sorted(t32, key=lambda r: r["path"]): print(r["lines"], r["language"], r["tier"], r["path"])
PY
wc -l .qa-scratch/t32/paths.txt     # 42
W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-views-scrapers-679; PIN=16dbac5211eea7e70db7394372033be2be7df829; MB=cada856d86
while IFS= read -r p; do git -C "$W" show "$PIN:$p" | wc -l; done < .qa-scratch/t32/paths.txt | awk '{s+=$1} END {print "wc -l lines", s}'           # 17306
while IFS= read -r p; do git -C "$W" show "$PIN:$p" | /usr/bin/grep -c ''; done < .qa-scratch/t32/paths.txt | awk '{s+=$1} END {print "grep -c lines", s}'   # 17311
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t32/paths.txt | wc -l   # 42: every path exists at the merge base
while IFS= read -r p; do git -C "$W" cat-file -e "bccd715707:$p" 2>/dev/null && echo "IN BASE: $p"; done < .qa-scratch/t32/paths.txt | wc -l   # 42
git -C "$W" diff --numstat "$MB" "$PIN" -- $(cat .qa-scratch/t32/paths.txt) | awk '{a+=$1; r+=$2; n+=1} END {print n, "files", a, "added", r, "removed"}'   # 6 files 168 added 46 removed
git -C "$W" diff --numstat bccd715707 "$PIN" -- $(cat .qa-scratch/t32/paths.txt) | awk '{a+=$1; r+=$2; n+=1} END {print n, "files", a, "added", r, "removed"}'   # 6 files 168 added 46 removed: the same
