"""Coordinator readback of P1's separately appended line-semantics row.

Run from a repository containing the two immutable research commits. This
executes the retained immutable-read reproducer, then counts the four referents
via git show. It writes nothing and compares the combined output with result.txt.
"""
from pathlib import Path
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
actual = subprocess.check_output([sys.executable, str(root / "reproduce.py")])
rows = [line.split(" ", 1) for line in actual.decode().splitlines()]
links = [json.loads(value) for key, value in rows if key == "SYMLINK"]
total = next(json.loads(value) for key, value in rows
             if key == "ACTUAL_CONTENT_TOTAL" and json.loads(value)["rev"] == "2174265e9c")
assert len(links) == 4
logical = total["logical_lines"] - len(links)
newlines = total["newline_count"]
for link in links:
    target = subprocess.check_output(["git", "show", "2174265e9c:" + link["resolved"]])
    literal = subprocess.check_output(["git", "show", "2174265e9c:" + link["path"]])
    assert literal.count(b"\n") == 0 and literal
    logical += target.count(b"\n") + int(bool(target) and not target.endswith(b"\n"))
    newlines += target.count(b"\n")
supplement = {
    "dereferenced_per_path_lines": logical,
    "dereferenced_per_path_newlines": newlines,
    "literal_git_blob_lines": total["logical_lines"],
    "regular_member_blob_lines": total["logical_lines"] - len(links),
    "symlink_entries": len(links),
}
combined = actual + ("LINE_SEMANTICS " + json.dumps(supplement, sort_keys=True) + "\n").encode()
assert combined == (root / "result.txt").read_bytes(), "research output differs"
print("PASS: main research output and independently counted supplement match result.txt")
