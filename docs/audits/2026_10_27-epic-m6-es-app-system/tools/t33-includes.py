"""04 § Q3's include graph for T33's slice (#680; T32's t32-includes.py renamed, its expectations set at stage C).

    python3 -I t33-includes.py <es worktree> <commit> <paths.txt> [in_lines=47,in_files=23,out_lines=410,es_core=143]

In: every `#include "<x>"` line in es-app/src and es-core/src outside the slice
paths whose target ends with one of the slice's headers (matched by the path
under es-app/src, or by its basename when the include names no directory),
counted per header. Out: every `#include` line in the slice's paths, and how many
of them resolve to a header under es-core/src (by the include's path, or by a
basename that exists only there). Printed: the inbound table, the outbound
split by target area, then three summary lines. Exits 1 when a count differs
from the one given.
"""
import collections
import os
import re
import subprocess
import sys



def show(tree, commit, path):
    # Bytes decoded with replacement: one es-core source is not UTF-8, and an
    # include line is ASCII either way.
    return subprocess.run(["git", "-C", tree, "show", "%s:%s" % (commit, path)],
                          capture_output=True, check=True).stdout.decode("utf-8", "replace")

tree, commit, paths_file = sys.argv[1:4]
want = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[4].split(","))) if len(sys.argv) > 4 else {}
paths = [l.strip() for l in open(paths_file) if l.strip()]
allfiles = subprocess.run(["git", "-C", tree, "ls-tree", "-r", "--name-only", commit, "--", "es-app/src", "es-core/src"],
                          capture_output=True, text=True, check=True).stdout.split()
core = set(f[len("es-core/src/"):] for f in allfiles if f.startswith("es-core/src/"))
app = set(f[len("es-app/src/"):] for f in allfiles if f.startswith("es-app/src/"))
core_base = collections.Counter(os.path.basename(f) for f in core)
app_base = collections.Counter(os.path.basename(f) for f in app)
headers = [p for p in paths if p.endswith(".h")]
rel = {h: h[len("es-app/src/"):] for h in headers}
inc = re.compile(r'^\s*#\s*include\s*[<"]([^">]+)[">]', re.M)

inbound, in_files = collections.Counter(), set()
for f in allfiles:
    if f in paths or not f.endswith((".cpp", ".h")):
        continue
    for m in inc.finditer(show(tree, commit, f)):
        t = m.group(1)
        for h, r in rel.items():
            if t == r or t.endswith("/" + r) or ("/" not in t and t == os.path.basename(r) and app_base[t] == 1):
                inbound[r] += 1
                in_files.add(f)
                break
out, areas = 0, collections.Counter()
for p in paths:
    for m in inc.finditer(show(tree, commit, p)):
        out += 1
        t = m.group(1)
        if t in core or (("/" not in t) and core_base[t] and not app_base[t]):
            areas["es-core"] += 1
        elif t in app or (("/" not in t) and app_base[t]):
            areas["es-app"] += 1
        else:
            areas["system or external"] += 1
print("| Slice header | Include lines from outside the slice |")
print("| --- | ---: |")
for r, n in inbound.most_common():
    print("| `%s` | %d |" % (r, n))
print()
print("| Target of the slice's includes | Lines |")
print("| --- | ---: |")
for a, n in areas.most_common():
    print("| %s | %d |" % (a, n))
print()
counts = {"in_lines": sum(inbound.values()), "in_files": len(in_files), "out_lines": out, "es_core": areas["es-core"]}
print("generated, asserted: inbound %d include lines from %d files outside the slice" % (counts["in_lines"], counts["in_files"]))
print("generated, asserted: outbound %d include lines in the slice's paths" % out)
print("generated, asserted: es-core edges %d of %d" % (areas["es-core"], out))
fail = ["%s %d, expected %d" % (k, counts[k], v) for k, v in want.items() if counts.get(k) != v]
if fail:
    print("FAIL t33-includes: " + "; ".join(fail))
    sys.exit(1)
