#!/usr/bin/env python3
"""Read every decision register this repository holds and compare it with next's (#1463).

Read-only. Sources: docs/decision-register.md at every local branch and
remote-tracking ref, and the working copy of every worktree under
../rocknix.worktrees. Prints, per area, the highest ID on next and the
highest anywhere (the next free ID is one above the latter); the IDs absent
from next; and the IDs whose date or text differs between sources, each text
with how many sources carry it. A difference can be a stale branch's older
copy of a row later corrected on next, a row edited after the fact, or one
ID used for two decisions: the table says which sources disagree, not why.

Usage: register-sweep.py [REPO]   (default: the current directory)
"""
import collections
import glob
import hashlib
import os
import re
import subprocess
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
ROW = re.compile(r"^\| (D-([A-Z]+)-(\d+)) \| (\d{4}-\d{2}-\d{2}) \| (.*)$")


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True)


sources = {}
for ref in git("for-each-ref", "--format=%(refname:short)", "refs/heads", "refs/remotes").stdout.split():
    shown = git("show", f"{ref}:docs/decision-register.md")
    if shown.returncode == 0:
        sources["ref:" + ref] = shown.stdout
for path in sorted(glob.glob(os.path.join(os.path.dirname(REPO), "rocknix.worktrees", "*", "docs", "decision-register.md"))):
    with open(path, errors="replace") as f:
        sources["worktree:" + path.split(os.sep)[-3]] = f.read()
if "ref:next" not in sources:
    sys.exit("register-sweep: cannot read next's register")

texts = collections.defaultdict(lambda: collections.defaultdict(set))
highest = collections.defaultdict(lambda: (0, ""))
on_next = collections.defaultdict(int)
for source, body in sources.items():
    for line in body.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        rid, area, number = m.group(1), m.group(2), int(m.group(3))
        texts[rid][(m.group(4), m.group(5).strip())].add(source)
        if number < 1000 and number > highest[area][0]:
            highest[area] = (number, source)
        if source == "ref:next":
            on_next[area] = max(on_next[area], number)

next_ids = {rid for rid, vals in texts.items() if any("ref:next" in s for s in vals.values())}
print(f"sources read: {len(sources)} ({sum(s.startswith('ref:') for s in sources)} refs)")
print("\narea      next max  highest anywhere  next free  where the highest is")
for area in sorted(highest):
    n, where = highest[area]
    print(f"{area:9} {on_next[area]:8}  {n:16}  {n + 1:9}  {where}")


def order(rid):
    _, area, number = rid.split("-")
    return area, int(number)


missing = sorted((r for r in texts if r not in next_ids), key=order)
print(f"\nIDs absent from next: {len(missing)}")
print(" ".join(missing))
CHECKER = os.path.join(REPO, "tools", "forbidden-terms-check")


def shown(text):
    """The text only when the fork's word list clears it; old branches keep
    rows written before #312's sweep, and this output is committed. A checker
    that cannot run clears nothing (fail closed): the digest stands alone."""
    excerpt = text[:160]
    try:
        ok = subprocess.run([CHECKER, "--stdin"], input=excerpt + "\n", capture_output=True,
                            text=True, timeout=30).returncode == 0
    except (OSError, subprocess.SubprocessError):
        ok = False
    return excerpt if ok else "(text withheld: not cleared by forbidden-terms-check)"


conflicts = sorted((r for r, v in texts.items() if len(v) > 1), key=order)
print(f"\nIDs with more than one date or text: {len(conflicts)}")
for rid in conflicts:
    print(f"\n{rid} ({'on next' if rid in next_ids else 'not on next'})")
    for (date, text), where in sorted(texts[rid].items(), key=lambda kv: -len(kv[1])):
        mark = " [next]" if "ref:next" in where else ""
        digest = hashlib.sha256(text.encode()).hexdigest()[:12]
        print(f"  {date} {len(where):3} sources{mark}, sha256 {digest}, {len(text)} chars, e.g. {', '.join(sorted(where)[:2])}")
        print(f"      {shown(text)}")
