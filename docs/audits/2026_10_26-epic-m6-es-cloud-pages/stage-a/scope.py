"""T18 (#665): the brief's section 2 membership block, as written there.

    python3 -I docs/audits/2026_10_26-epic-m6-es-cloud-pages/stage-a/scope.py   (from the distribution worktree)
"""
import json, re, collections, os
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
pat = re.compile(r"^es-app/src/(CloudText|ThreadedCloudSync|CloudTransferJob)\.[^/]+$|^es-app/src/guis/GuiCloud[^/]*$|^es-app/tests/.+$")
t18 = [r for r in rows if r["tree"] == "es" and pat.match(r["path"])]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t18), "lines", L(t18), dict(collections.Counter(r["reach"] for r in t18)), dict(collections.Counter(r["tier"] for r in t18)))
print(dict(collections.Counter(r["language"] for r in t18)))
CODE = {"c++", "c-header", "cmake", "python", "c"}
rd = [r for r in t18 if r["language"] in CODE]
print("read", len(rd), L(rd), "unread", [r["path"] for r in t18 if r not in rd])
src = [r for r in t18 if r["path"].startswith("es-app/src/")]; tst = [r for r in t18 if r["path"].startswith("es-app/tests/")]
print("sources", len(src), L(src), "tests", len(tst), L(tst))
os.makedirs(".qa-scratch/t18", exist_ok=True)
open(".qa-scratch/t18/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t18, key=lambda r: r["path"])))
for r in sorted(t18, key=lambda r: r["path"]): print(r["lines"], r["language"], r["tier"], r["path"])
print("es rows in the inventory:", sum(1 for r in rows if r["tree"] == "es"))
