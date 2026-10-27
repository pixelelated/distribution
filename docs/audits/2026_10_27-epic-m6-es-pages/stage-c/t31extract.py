"""Shared by T31's stage-C harnesses (#678): a C++ definition extracted as written,
by balanced braces with strings, chars and comments skipped, and a compile-and-run
of a harness under AddressSanitizer in the lane's scratch."""
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def function(src, head, name="extract"):
    m = re.search(head, src, re.M)
    if not m:
        sys.exit("FAIL %s: %s not found" % (name, head))
    i = src.index("{", m.end() - 1)
    depth, j = 0, i
    while True:
        c = src[j]
        if src.startswith("//", j):
            j = src.index("\n", j)
            continue
        if src.startswith("/*", j):
            j = src.index("*/", j) + 2
            continue
        if c in "\"'":
            j += 1
            while src[j] != c:
                j += 2 if src[j] == "\\" else 1
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[m.start():j + 1]
        j += 1


def run(harness, name, flags=("-fsanitize=address,undefined",)):
    with tempfile.TemporaryDirectory(prefix=name + "-", dir="/workspace/tmp/m6-t31/tmp") as d:
        d = Path(d)
        (d / "a.cpp").write_text(harness)
        b = subprocess.run(["g++", "-std=c++17", "-O0", "-g", *flags, str(d / "a.cpp"), "-o", str(d / "a"), "-pthread"],
                           capture_output=True, text=True)
        if b.returncode:
            print("FAIL %s: the extract does not compile\n%s" % (name, b.stderr[-2000:]))
            sys.exit(2)
        r = subprocess.run([str(d / "a")], capture_output=True, text=True, timeout=60)
        print(r.stdout.strip())
        # A sanitizer's verdict is its report: the warning heads, the frames in
        # the harness, and the summary (the tail alone hid which race it was).
        for line in r.stderr.splitlines():
            if line.startswith(("WARNING: ", "SUMMARY: ")) or (" a.cpp:" in line and line.lstrip().startswith("#")):
                print(line.replace(str(d) + "/", ""))
        if r.returncode and "FAIL" not in r.stdout:
            print("FAIL %s: rc %d %s" % (name, r.returncode, r.stderr[-800:]))
        sys.exit(1 if r.returncode else 0)
