"""Who opens each page of T31's slice, at a commit of the EmulationStation tree (#678).

    python3 -I t31-callers.py <es worktree> <commit> <paths.txt>

For each class named by a slice file's basename, the lines outside that
class's own two files, under es-app/src and es-core/src at <commit>, that
construct it (`new Class(`, `make_shared<Class>`) or call a static of it
(`Class::name(`). The classes are the basenames, not a parse of the headers:
a header that declares a second class is named in the output, and a class
with no caller says so. Read by `git grep` at the commit, never the working
tree. Exits 1 when the class count is not the 39 basenames the 76 paths name.
"""
import re
import subprocess
import sys

tree, commit, paths_file = sys.argv[1:4]
paths = [l.strip() for l in open(paths_file) if l.strip()]
classes = sorted({re.sub(r"\.(cpp|h)$", "", p.rsplit("/", 1)[1]) for p in paths})

def grep(pattern):
    r = subprocess.run(["git", "-C", tree, "grep", "-n", "-P", pattern, commit, "--", "es-app/src", "es-core/src"],
                       capture_output=True, text=True)
    if r.returncode not in (0, 1):
        sys.exit("git grep failed: " + r.stderr)
    return [l[len(commit) + 1:] for l in r.stdout.splitlines()]

none = 0
for c in classes:
    own = (c + ".cpp", c + ".h")
    hits = [l for l in grep(r"(new\s+%s\s*[(<]|make_shared<%s>|\b%s::\w+\s*\()" % (c, c, c))
            if not l.split(":", 1)[0].rsplit("/", 1)[1] in own]
    files = sorted({l.split(":", 1)[0].rsplit("/", 1)[1] for l in hits})
    if not hits:
        none += 1
    print("%s: %d line(s) in %d file(s)%s" % (c, len(hits), len(files), (" -- " + ", ".join(
        "%s:%s" % (l.split(":")[0].rsplit("/", 1)[1], l.split(":")[1]) for l in hits[:8]) + (" ..." if len(hits) > 8 else "")) if hits else ""))
print("classes %d; with no caller outside their own files %d" % (len(classes), none))
if len(classes) != 39:
    print("FAIL t31-callers: %d classes, expected 39" % len(classes)); sys.exit(1)
