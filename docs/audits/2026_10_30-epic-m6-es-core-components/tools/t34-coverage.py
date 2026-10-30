"""02 § Coverage: one row per path of the 80 (#681). Asserts 80 rows, 38 .cpp and
42 .h, read tiers 0 added / 21 modified / 59 upstream-carried against both bases,
21,984 lines by grep -c '', the fork's +591/-114, and every brief lead naming a
path in the 80.    t34-coverage.py <ES worktree> [paths file]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t34lib import PIN, BASE, COMP, die, git, show, paths, numstat, brief_leads

tree = sys.argv[1]
files = paths(sys.argv[2] if len(sys.argv) > 2 else None)
ns = numstat(tree, files)
ns_mb = numstat(tree, files, "cada856d86")
added = git(tree, "diff", "--diff-filter=A", "--name-only", BASE, PIN, "--", *files).split()
leads = brief_leads()
base_names = {f[len(COMP):] for f in files}
by_file = {}
for lid, names in leads.items():
    hit = names & base_names
    if not hit:
        die("lead %s names no path in the 80 (%s)" % (lid, sorted(names)))
    for n in hit:
        by_file.setdefault(n, []).append(lid)
rows, total, cpp, h, mod, ins, dele = [], 0, 0, 0, 0, 0, 0
for f in files:
    n = show(tree, f).count("\n") + (0 if show(tree, f).endswith("\n") else 1)
    total += n
    cpp += f.endswith(".cpp"); h += f.endswith(".h")
    a, d = ns.get(f, (0, 0))
    if ns.get(f) != ns_mb.get(f):
        die("the bases disagree on %s: %s against %s" % (f, ns.get(f), ns_mb.get(f)))
    tier = "fork-added" if f in added else ("fork-modified" if f in ns else "upstream-carried")
    inv = "fork-own" if tier != "upstream-carried" else "upstream-carried"
    mod += tier == "fork-modified"; ins += a; dele += d
    lids = sorted(by_file.get(f[len(COMP):], []), key=lambda x: (x[0] != "L", float(x[2:]) if x[0] == "L" else float(x)))
    rows.append("| `%s` | %d | %s | %s | %d/%d | %s |" % (f, n, inv, tier, a, d, ", ".join(lids) or "-"))
for got, want, what in [(len(rows), 80, "rows"), (cpp, 38, ".cpp"), (h, 42, ".h"), (len(added), 0, "fork-added"), (mod, 21, "fork-modified"),
                        (len(rows) - mod - len(added), 59, "upstream-carried"), (total, 21984, "lines by grep -c"), (ins, 591, "insertions"),
                        (dele, 114, "deletions"), (len(leads), 55, "brief leads (L-01..L-21, 3.1..3.34)")]:
    if got != want:
        die("%s: %d, expected %d" % (what, got, want))
print("| Path | Lines (`grep -c ''`) | Inventory tier | Read tier | Fork +/- (against `bccd715707`, equal against `cada856d86`) | Leads naming it |")
print("| --- | ---: | --- | --- | ---: | --- |")
print("\n".join(rows))
print()
print("Generated, asserted by `tools/t34-coverage.py`: %d rows; %d `.cpp`, %d `.h`; fork-added %d / fork-modified %d / upstream-carried %d (inventory fork-own %d / upstream-carried %d); %d lines by `grep -c ''`; fork +%d/-%d; %d brief leads, each naming a path in the 80." % (
    len(rows), cpp, h, len(added), mod, len(rows) - mod - len(added), mod + len(added), len(rows) - mod - len(added), total, ins, dele, len(leads)))
