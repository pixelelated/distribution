#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""tick-checkboxes.py -- tick named checkbox lines in a fork issue's body,
refusing anything but that (M6 T30, #677; copied for T24, #671, from
`a020b3d375`, with only its scratch path changed).

    python3 -I tick-checkboxes.py <issue> <line> [<line> ...]

Written after a shell sed whose expression split on its spaces produced an
empty file, and `gh issue edit --body-file` then blanked three issue bodies
(#863, #864, #871; restored from the saved copies a minute later). This
writer refuses before any edit when the body cannot be read or is empty, a
named line is not an open checkbox ("- [ ]"), or the result differs from the
original anywhere but the named lines; after the edit it reads the body back
and fails unless it equals what was written. The original is kept beside the
new body under /workspace/tmp/m6-t24/ticks/.
"""
import json, os, subprocess, sys

REPO = "pixelelated/distribution"
issue, lines = sys.argv[1], [int(x) for x in sys.argv[2:]]
if not lines:
    sys.exit("tick-checkboxes: name at least one line")

def body():
    out = subprocess.run(["gh", "issue", "view", issue, "--repo", REPO, "--json", "body"],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)["body"]

old = body()
if not old.strip():
    sys.exit(f"tick-checkboxes: #{issue}'s body is empty; refusing")
rows = old.split("\n")
new_rows = list(rows)
for n in lines:
    if n < 1 or n > len(rows) or not rows[n - 1].lstrip().startswith("- [ ]"):
        sys.exit(f"tick-checkboxes: #{issue} line {n} is not an open checkbox; refusing")
    new_rows[n - 1] = rows[n - 1].replace("- [ ]", "- [x]", 1)
new = "\n".join(new_rows)
changed = [i + 1 for i, (a, b) in enumerate(zip(rows, new_rows)) if a != b]
if len(new_rows) != len(rows) or sorted(changed) != sorted(set(lines)) or not new.strip():
    sys.exit(f"tick-checkboxes: #{issue}: the result changes more than the named lines; refusing")

d = "/workspace/tmp/m6-t24/ticks"
os.makedirs(d, exist_ok=True)
open(f"{d}/{issue}.orig.md", "w").write(old)
open(f"{d}/{issue}.new.md", "w").write(new)
subprocess.run(["gh", "issue", "edit", issue, "--repo", REPO, "--body-file", f"{d}/{issue}.new.md"],
               capture_output=True, text=True, check=True)
back = body()
if back.rstrip("\n") != new.rstrip("\n"):
    sys.exit(f"tick-checkboxes: #{issue}: the readback differs from what was written; the original is {d}/{issue}.orig.md")
print(f"#{issue}: ticked line(s) {', '.join(map(str, lines))}; readback equal")
