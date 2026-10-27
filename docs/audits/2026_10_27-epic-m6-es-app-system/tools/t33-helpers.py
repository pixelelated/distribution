"""02 § The helpers: one row per fork-added unit (#680, Q7 and Q5).

    python3 -I t33-helpers.py <es worktree> <commit> <paths.txt> [units=17,cases=12,built=7,files=27]

For each of the fork's 17 added units (27 files), from the tree: its lines,
its includers outside the 77 (the page or caller in another slice), its
case file (`es-app/tests/unit/<Unit>Tests.cpp` or
`tests/app-unit/<Unit>Tests.cpp`), whether a test target lists that case
file -- `es-unit-tests` in `es-app/tests/unit/CMakeLists.txt`, which T18 to
T32 built, or `app-unit-tests` in `tests/app-unit/CMakeLists.txt`, which no
lane has built (T18 `02:50-58`; stage C builds it) -- and its `_("` lines.
The French is t33-words.py's: every msgid the 77 carry has a translation
at the pin. Exits 1 on a count other than the one given.
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t33lib import show  # noqa: E402

UNITS = ["AppWindow", "CaptureRotation", "CaptureRotationText", "CheevosIndex", "CheevosRetry", "CloudExit", "CloudFolderValidation",
         "CloudOffer", "DisplayAspect", "DisplayAspectText", "FolderMerge", "GameCubeRvzHashRetry", "JourneyTiers",
         "OfflineAchievementsText", "RunLock", "TextFit", "WifiText"]

tree, commit, paths_file = sys.argv[1:4]
want = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[4].split(","))) if len(sys.argv) > 4 else {}
paths = [l.strip() for l in open(paths_file) if l.strip()]
listing = subprocess.run(["git", "-C", tree, "ls-tree", "-r", "--name-only", commit, "--", "es-app/tests/unit", "tests/app-unit"],
                         capture_output=True, text=True, check=True).stdout.split()
lists = {t: re.sub(r"#[^\n]*", "", show(tree, commit, "%s/CMakeLists.txt" % t)) for t in ("es-app/tests/unit", "tests/app-unit")}
target = {"es-app/tests/unit": "`es-unit-tests`, built by every lane", "tests/app-unit": "`app-unit-tests`, never built by a lane (stage C)"}
counts = {"units": 0, "cases": 0, "built": 0, "files": 0}
print("| Unit | Files (lines) | Includers outside the 77 | Case file | Built | `_(\"` lines |")
print("| --- | --- | --- | --- | --- | --- |")
for u in UNITS:
    files = [p for p in ("es-app/src/%s.cpp" % u, "es-app/src/%s.h" % u) if p in paths]
    if not files:
        print("FAIL t33-helpers: %s has no file in the 77" % u)
        sys.exit(1)
    counts["units"] += 1
    counts["files"] += len(files)
    srcs = {f: show(tree, commit, f) for f in files}
    out = subprocess.run(["git", "-C", tree, "grep", "-l", "-E", r'#include ["<]%s\.h[">]' % u, commit, "--", "es-app", "es-core"],
                         capture_output=True, text=True).stdout.split()
    inc = sorted(i for i in set(o.split(":", 1)[1] for o in out) - set(paths) if not i.startswith(("es-app/tests", "tests/")))
    case = [c for c in listing if c.endswith("/%sTests.cpp" % u)]
    built = "--"
    if case:
        counts["cases"] += 1
        d = case[0].rsplit("/", 1)[0]
        if "%sTests.cpp" % u in lists[d]:
            built = target[d]
            if d == "es-app/tests/unit":
                counts["built"] += 1
        else:
            built = "listed by no target"
    strings = sum(1 for s in srcs.values() for line in s.split("\n") if '_("' in line)
    inside = sorted(i for i in set(o.split(":", 1)[1] for o in out) & set(paths) if i not in files)
    inc_s = ", ".join("`%s`" % i.replace("es-app/src/", "") for i in inc) if inc else "none; in the 77: %s" % ", ".join("`%s`" % i.replace("es-app/src/", "") for i in inside)
    print("| `%s` | %s | %s | %s | %s | %d |" % (u, ", ".join("`%s` (%d)" % (f.rsplit("/", 1)[1], len(s.splitlines())) for f, s in srcs.items()),
                                              inc_s, "`%s`" % case[0] if case else "**none**", built, strings))
print()
print("generated, asserted: %d units in %d files; %d with a case file, %d of them built by `es-unit-tests`" % (counts["units"], counts["files"], counts["cases"], counts["built"]))
fail = ["%s %d, expected %d" % (k, counts[k], v) for k, v in want.items() if counts.get(k) != v]
if fail:
    print("FAIL t33-helpers: " + "; ".join(fail))
    sys.exit(1)
