#!/usr/bin/env python3
"""Read-only: count untracked docs/qa-logs files per worktree and which are absent from next."""
import json
import os
import subprocess
import sys

ROOT = "/workspace/repos/rocknix.worktrees"
PRIMARY = "/workspace/repos/rocknix"
OUT = sys.argv[1]

nxt = set(subprocess.run(["git", "-C", PRIMARY, "ls-tree", "-r", "--name-only", "next", "docs/qa-logs"],
                         check=True, capture_output=True, text=True).stdout.splitlines())
report = {"next_files": len(nxt), "worktrees": {}}
for name in sorted(os.listdir(ROOT)):
    w = os.path.join(ROOT, name)
    if not os.path.isdir(w):
        continue
    r = subprocess.run(["git", "-C", w, "ls-files", "--others", "--exclude-standard", "-z", "--", "docs/qa-logs"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        report["worktrees"][name] = {"error": r.stderr.strip()[:200]}
        continue
    files = [p for p in r.stdout.split("\0") if p]
    if not files:
        continue
    missing = [p for p in files if p not in nxt]
    size = 0
    for p in missing:
        try:
            size += os.lstat(os.path.join(w, p)).st_size
        except OSError:
            pass
    dirs = sorted({"/".join(p.split("/")[:3]) for p in missing})
    report["worktrees"][name] = {"untracked": len(files), "missing_from_next": len(missing),
                                 "missing_bytes": size, "missing_dirs": dirs}
json.dump(report, open(OUT, "w"), indent=1)
for k, v in report["worktrees"].items():
    print(k, {a: b for a, b in v.items() if a != "missing_dirs"})
