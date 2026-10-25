python3 -I - <<'PY'
import json, collections, os
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
excl = ("projects/ROCKNIX/devices/H700/", "projects/ROCKNIX/devices/SM8550/", "projects/ROCKNIX/devices/GENERIC_X64/")
t25 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "devices"
       and (r["path"].startswith("projects/") or r["path"].startswith("packages/"))
       and not r["path"].startswith(excl) and r["reach"] in ("unreached", "unshipped")]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t25), "lines", L(t25), dict(collections.Counter(r["reach"] for r in t25)), dict(collections.Counter(r["tier"] for r in t25)))
print(dict(collections.Counter(r["language"] for r in t25)))
def unit(p):
    s = p.split("/")
    if p.startswith("projects/ROCKNIX/devices/"): return "/".join(s[:4])
    if p.startswith("projects/ROCKNIX/packages/"): return "projects/ROCKNIX/packages/{linux-drivers,linux-firmware}"
    return "/".join(s[:2])
u = collections.Counter(unit(r["path"]) for r in t25)
print("units", len(u), sorted(u.items()))
CODE = {"shell", "recipe", "udev", "python", "c", "make"}
rd = [r for r in t25 if r["language"] in CODE and r["tier"] != "vendor-carried" and r["reach"] != "unreached"]
print("read", L(rd), "rows", len(rd), "fork-own", sum(1 for r in rd if r["tier"] == "fork-own"))
print("shadowed", sum(1 for r in t25 if r.get("shadowed_by")), "fork-own", [r["path"] for r in t25 if r["tier"] == "fork-own"])
os.makedirs(".qa-scratch/t25", exist_ok=True)
open(".qa-scratch/t25/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t25, key=lambda r: r["path"])))
open(".qa-scratch/t25/rows.tsv", "w").write("".join("\t".join(str(r[k]) for k in ("reach", "tier", "lines", "language", "buildable_by", "shadowed_by", "path")) + "\n" for r in sorted(t25, key=lambda r: r["path"])))
PY
