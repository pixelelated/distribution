"""Shared by T35's generators (#682): the pin's bytes by `git show`, line checks, tables, asserted counts.

Every generator is run as

    python3 -I <generator> <es worktree> <commit> <paths.txt> [key=value ...]

and reads the 96 files at <commit> by `git -C <es worktree> show`, never the working
tree. A cited line is checked for its text at that commit; a row naming a file outside
the paths list, a cited line whose text has moved, or a count that differs from a
key=value expectation prints FAIL and exits 1. The last line is
`generated, asserted: ...`, which `02` quotes.
"""
import re
import subprocess
import sys

PIN = "16dbac5211eea7e70db7394372033be2be7df829"


class Ctx:
    def __init__(self, argv, usage):
        if len(argv) < 4:
            sys.exit("usage: " + usage)
        self.W, self.ref, self.paths_file = argv[1], argv[2], argv[3]
        self.paths = [l.strip() for l in open(self.paths_file) if l.strip()]
        self.inside = set(self.paths)
        self.expect = dict(a.split("=", 1) for a in argv[4:] if "=" in a)
        self.cache = {}
        self.fail = []

    def text(self, path):
        if path not in self.cache:
            r = subprocess.run(["git", "-C", self.W, "show", f"{self.ref}:{path}"], capture_output=True, text=True)
            if r.returncode:
                self.fail.append(f"{path} not at {self.ref}")
                self.cache[path] = ""
            else:
                self.cache[path] = r.stdout
        return self.cache[path]

    def lines(self, path):
        return self.text(path).split("\n")

    def line(self, path, n):
        L = self.lines(path)
        return L[n - 1] if 0 < n <= len(L) else ""

    def need(self, path, n, needle, outside=False):
        """Line n of path carries needle (a regex); path is one of the 96 unless outside."""
        if not outside and path not in self.inside:
            self.fail.append(f"{path} is not in the paths list")
            return ""
        t = self.line(path, n)
        if not re.search(needle, t):
            self.fail.append(f"{path}:{n} does not carry /{needle}/ (reads: {t.strip()[:90]!r})")
        return t

    def grep(self, pattern, paths=None):
        rx = re.compile(pattern)
        out = []
        for p in (paths or self.paths):
            for i, t in enumerate(self.lines(p), 1):
                if rx.search(t):
                    out.append((p, i, t))
        return out

    def enclosing(self, path, n):
        """The function a line sits in: the nearest earlier line that opens a definition."""
        L = self.lines(path)
        rx = re.compile(r"^(?:[\w:<>,\*&~ ]+\s)?([\w:~]+)\s*\([^;]*$")
        for i in range(n - 1, -1, -1):
            t = L[i]
            if t[:1] in (" ", "\t", "#", "/", "}", "{") or not t.strip():
                continue
            m = rx.match(t)
            if m:
                return m.group(1)
        return "(file scope)"

    def finish(self, name, counts, label):
        for k, v in self.expect.items():
            if str(counts.get(k)) != v:
                self.fail.append(f"{k} {counts.get(k)}, expected {v}")
        print()
        print(f"generated, asserted: {label}")
        if self.fail:
            for f in self.fail:
                print(f"FAIL {name}: {f}")
            sys.exit(1)


def short(path):
    return path.replace("es-core/src/", "")


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |")
    return "\n".join(out)
