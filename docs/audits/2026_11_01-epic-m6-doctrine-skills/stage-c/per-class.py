"""per-class.py: per step, the allowlisted assertions of a checker run counted by allowlist file and class, from the
run's own detail files (`<out>/<step>.txt`, each allowed line ending `[<file>:<n> <class>]`), so the counts in `02`
are this command's. python3 -I per-class.py <out-dir>"""
import collections, pathlib, re, sys
out = pathlib.Path(sys.argv[1])
for step in ("refs", "stale", "contract"):
    lines = (out / f"{step}.txt").read_text().splitlines()
    c = collections.Counter()
    fails = 0
    for l in lines:
        if l.startswith("allowed"):
            m = re.search(r"\[(allow-[a-z]+\.txt):\d+ (\S+)\]$", l)
            if not m:
                sys.exit(f"per-class: refused: {step}.txt has an allowed line without its entry: {l[:80]}")
            c[(m.group(1), m.group(2))] += 1
        elif l.startswith("FAIL"):
            fails += 1
    total = sum(c.values())
    print(f"{step}: {total} allowlisted, {fails} FAIL")
    for (f, cls), n in sorted(c.items()):
        print(f"  {f} {cls}: {n}")
