#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""s5-dolphin-split-check.py -- T30 stream S5 (#677, #872 PL-023): the split
of start_dolphin_gc.sh and start_dolphin_wii.sh into a shared library changed
no step. Each split script is rebuilt by inlining the library: every
`dolphin_shared_N "$@"` line becomes that function's body, the
`dolphin_face_swap_configs <custom> <fresh>` line becomes its body with the two
names put back, and the line sourcing the library is dropped. The result must
equal the script at BEFORE with exactly two named edits applied: the face-swap
function definitions moved out (they are in the library, unchanged), and the
dead `-v $GRENDERER` line replaced by its comment.

    python3 -I s5-dolphin-split-check.py <BEFORE commit> <AFTER commit|WORKTREE>

Prints PASS or FAIL per script with the first differing line; exit 0 when
both pass, 1 when one fails, 2 when it cannot run.
"""
import os, re, subprocess, sys

before, after = sys.argv[1:3]
tree = subprocess.run(["git", "-C", os.path.dirname(os.path.abspath(__file__)), "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
D = "projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/"

def src(rev, name):
    if rev == "WORKTREE":
        with open(os.path.join(tree, D + name)) as f:
            return f.read()
    r = subprocess.run(["git", "-C", tree, "show", f"{rev}:{D}{name}"], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"s5-dolphin-split-check: {name} not found at {rev}")
    return r.stdout

lib = src(after, "dolphin_common.sh")
funcs = {}
for m in re.finditer(r'^(dolphin_shared_\d+)\(\) \{\n(.*?)\n\}$', lib, re.S | re.M):
    funcs[m.group(1)] = m.group(2)
fs = re.search(r'^dolphin_face_swap_configs\(\) \{\n  local FACE_CUSTOM_CFG="\$1" FACE_FRESH_CFG="\$2"\n(.*?)\n\}$', lib, re.S | re.M)
face_defs_start = lib.index("# The face swap, applied once (#869).")
face_defs = lib[face_defs_start:lib.index("# The face swap's detection", face_defs_start)]
if not funcs or not fs:
    sys.exit("s5-dolphin-split-check: the library's functions were not found")
face_body = "\n".join(l[2:] if l.startswith("  ") else l for l in fs.group(1).split("\n"))

DEAD_OLD = '# Set video and audio backend\n  CMD="${CMD} -v $GRENDERER"\n\n'
DEAD_NEW = ('# Set the audio backend (the video backend is GFXBackend in the ini; a\n'
            '# "-v $GRENDERER" here was overwritten by the next line, #872 PL-023)\n')
fails = 0
for name in ("start_dolphin_gc.sh", "start_dolphin_wii.sh"):
    old = src(before, name)
    expected = old.replace(face_defs, "", 1).replace(DEAD_OLD, DEAD_NEW, 1)
    out = []
    for line in src(after, name).split("\n"):
        m = re.fullmatch(r'(dolphin_shared_\d+) "\$@"', line)
        f = re.fullmatch(r'dolphin_face_swap_configs "([^"]*)" "([^"]*)"', line)
        if line == ". /usr/bin/dolphin_common.sh":
            continue
        if m:
            out.append(funcs[m.group(1)])
        elif f:
            out.append(face_body.replace("${FACE_CUSTOM_CFG}", f.group(1)).replace("${FACE_FRESH_CFG}", f.group(2)).rstrip("\n"))
        else:
            out.append(line)
    rebuilt = "\n".join(out)
    if rebuilt == expected:
        print(f"PASS {name}: the split script with the library inlined equals {before}'s, with the two named edits")
    else:
        a, b = expected.split("\n"), rebuilt.split("\n")
        k = next((i for i in range(min(len(a), len(b))) if a[i] != b[i]), min(len(a), len(b)))
        print(f"FAIL {name}: first difference at line {k + 1}: expected {a[k] if k < len(a) else '<end>'!r}, rebuilt {b[k] if k < len(b) else '<end>'!r}")
        fails += 1
print(f"s5-dolphin-split-check: {before} -> {after}: {len(funcs)} shared functions; failures {fails}")
sys.exit(1 if fails else 0)
