"""Shared readers for T34's generators (#681): the 80 paths, a file at the
pin, the fork's numstat, and the brief's two lead tables. Every generator
exits 1 when a count it asserts differs (the drift its stage-B record shows
it catching)."""
import os
import re
import subprocess
import sys

PIN = "16dbac5211eea7e70db7394372033be2be7df829"
BASE = "bccd715707"
HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(AUDIT, "..", "..", ".."))
BRIEF = os.path.join(ROOT, "docs/reviews/briefs/es-core-components.md")
COMP = "es-core/src/components/"


def die(msg):
    print("ASSERT: " + msg, file=sys.stderr)
    sys.exit(1)


def git(tree, *args):
    return subprocess.run(["git", "-C", tree] + list(args), capture_output=True, check=True).stdout.decode("utf-8", "replace")


def show(tree, path, commit=PIN):
    # bytes decoded latin-1 so VideoVlcComponent.cpp's 0x96 survives one byte for one char
    return subprocess.run(["git", "-C", tree, "show", "%s:%s" % (commit, path)], capture_output=True, check=True).stdout.decode("latin-1")


def paths(paths_file=None):
    p = paths_file or os.path.join(AUDIT, "stage-a/paths.txt")
    out = [l.strip() for l in open(p) if l.strip()]
    return out


def numstat(tree, files, base=BASE):
    rows = {}
    for l in git(tree, "diff", "--numstat", base, PIN, "--", *files).splitlines():
        a, d, f = l.split("\t")
        rows[f] = (int(a), int(d))
    return rows


def brief_leads():
    """{lead id: set of basenames in the 80 named in its lines cell} from the brief's L-table and floor table."""
    text = open(BRIEF, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"^\| (L-\d\d|\*\*3\.\d+\*\*|3\.\d+) \| (.+?) \|", text, re.M):
        lid = m.group(1).strip("*")
        out[lid] = set(re.findall(r"`([A-Za-z]+\.(?:cpp|h))(?::|`)", m.group(2)))
    return out
