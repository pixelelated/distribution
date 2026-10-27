"""Every file-existence read, lock probe and parse in T31's slice (#678, Q4).

    python3 -I t31-reads.py <es worktree> <commit> <paths.txt> [kind=N,...]

The sites: Utils::FileSystem::exists( (cached unless its second argument is
false -- FileSystemUtil's enableCache default), isFlockHeld(, and the parses
atoi( / std::stoi( / std::stoul( / std::stol( / atof(. Each call is read by
balanced brackets (t31lib), so an argument that spans lines is whole. The
writer of each file and what a failure reads as are written in 02 by reading
the code at each line; this tool is the census they hang on.

Exits 1 when a kind's total differs from the kind=N list given (the brief's
reads and parses runs: exists 12, isFlockHeld 1, atoi 9).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t31lib import call_args, in_comment_or_string, show  # noqa: E402

tree, commit, paths_file = sys.argv[1:4]
KINDS = {"exists": r"\bFileSystem::exists", "isFlockHeld": r"\bisFlockHeld", "atoi": r"(?<!\w)(?:std::)?atoi",
         "stoi": r"\bstd::stoi", "stoul": r"\bstd::stoul", "stol": r"\bstd::stol\b", "atof": r"(?<!\w)(?:std::)?atof"}
rows, totals = [], {k: 0 for k in KINDS}
for path in [l.strip() for l in open(paths_file) if l.strip()]:
    src = show(tree, commit, path)
    for kind, pat in KINDS.items():
        for m in re.finditer(pat + r"\s*\(", src):
            if in_comment_or_string(src, m.start()):
                continue
            a, _ = call_args(src, src.index("(", m.start()))
            line = src.count("\n", 0, m.start()) + 1
            note = ""
            if kind == "exists":
                note = "uncached" if len(a) > 1 and a[1].strip() == "false" else "cached"
            rows.append((path.rsplit("/", 1)[1], line, kind, re.sub(r"\s+", " ", ", ".join(a))[:90], note))
            totals[kind] += 1
print("| Site | Kind | Argument(s) | Cache |")
print("| --- | --- | --- | --- |")
for f, l, k, arg, note in sorted(rows):
    print("| `%s:%d` | %s | `%s` | %s |" % (f, l, k, arg.replace("|", "\\|"), note or "-"))
print()
print("sites %d: %s" % (len(rows), ", ".join("%s %d" % kv for kv in totals.items() if kv[1])))
want = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[4].split(","))) if len(sys.argv) > 4 else {}
bad = ["%s %d, expected %d" % (k, totals.get(k, 0), v) for k, v in want.items() if totals.get(k, 0) != v]
if bad:
    print("FAIL t31-reads: " + "; ".join(bad))
    sys.exit(1)
