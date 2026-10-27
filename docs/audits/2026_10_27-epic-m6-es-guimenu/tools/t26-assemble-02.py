#!/usr/bin/env python3
"""T26 (#673): assemble 02-forward-audit.md from stage-b/02-template.md.

    python3 -I t26-assemble-02.py <pin.cpp> <pin GuiMenu.h> <tests dir> <ES checkout> <distribution checkout>

Each `<!-- generated: NAME -->` marker in the template is replaced by the
output of the generator that makes it, run now at the pin's bytes; the
template's prose is copied as it is. A generator that exits non-zero stops
the assembly (exit 1): a table is never pasted from a run that did not hold.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.dirname(HERE)
pin, hdr, tests, es, dist = sys.argv[1:6]
tmp = os.environ.get("TMPDIR", "/tmp")
lines_file = os.path.join(tmp, "t26-assemble-lines.txt")

def run(*args):
    p = subprocess.run([sys.executable, "-I", "-B"] + list(args), capture_output=True, text=True, cwd=dist)
    if p.returncode != 0:
        sys.exit("generator failed (%d): %s\n%s" % (p.returncode, " ".join(args), p.stdout[-2000:] + p.stderr[-2000:]))
    return p.stdout

T = lambda name: os.path.join(HERE, name)
open(lines_file, "w").write(run(T("t26-structure.py"), pin, hdr, tests, "--lines"))
rows = run(T("t26-rows.py"), pin, dist, "8ebaf8daad", "--table", "--writes", "--live", lines_file)
pages = run(T("t26-pages.py"), pin, "--table")
trans = run(T("t26-structure.py"), pin, hdr, tests, "--transitions")
reads = run(T("t26-structure.py"), pin, hdr, tests, "--reads")
dups = run(T("t26-structure.py"), pin, hdr, tests, "--dups")
merge = run(T("t26-merge.py"), es, "bccd715707", "rocknix/master", "16dbac5211eea7e70db7394372033be2be7df829", "--table")

table = lambda out: "\n".join(l for l in out.split("\n") if l.startswith("|"))
summary = lambda out: "\n".join("- " + l.strip() for l in out.split("\n")
                                if l.strip() and not l.startswith("|") and not l.startswith("  ") and not l.startswith("writes ")
                                and not l.startswith("rows with") and l.strip() != "asserted counts hold")
def section(out, start, stop):
    s = out.find(start); e = out.find(stop, s + 1) if s >= 0 else -1
    return out[s:e if e >= 0 else len(out)].strip() if s >= 0 else ""

writes = section(rows, "writes outside every save hook", "greps (raw lines)")
writes = "```text\n" + writes + "\n```"
generated = {
    "pages-summary": summary(pages),
    "pages": table(pages),
    "rows-summary": summary(rows),
    "rows": table(rows),
    "rows-writes": writes,
    "transitions": table(trans),
    "reads": table(reads),
    "dups": table(dups),
    "merge": table(merge) + "\n\n" + summary(merge),
    "structure-summary": summary(run(T("t26-structure.py"), pin, hdr, tests)),
}
text = open(os.path.join(AUDIT, "stage-b", "02-template.md"), encoding="utf-8").read()
def put(m):
    name = m.group(1)
    if name not in generated:
        sys.exit("unknown marker: %s" % name)
    return generated[name]
out = re.sub(r"<!-- generated: ([a-z-]+) -->", put, text)
left = re.findall(r"<!-- generated: [a-z-]+ -->", out)
if left:
    sys.exit("markers left: %s" % left)
open(os.path.join(AUDIT, "02-forward-audit.md"), "w", encoding="utf-8").write(out)
print("02-forward-audit.md: %d lines, %d table rows" % (out.count("\n"), len([l for l in out.split("\n") if l.startswith("| ")])))
