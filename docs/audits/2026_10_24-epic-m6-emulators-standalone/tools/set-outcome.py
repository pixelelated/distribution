#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
# Copied for M6 T30 (#677) from T3's docs/audits/2026_10_24-epic-m6-emulators-libretro/tools/set-outcome.py at b3cb4ec8c5
# (feature/m6-emulators-libretro-650); T30's changes, if any, are named below.
"""set-outcome.py -- record a punch item's Phase 7 outcome in punch-items.py
(M6 T3, #650), so 05 is regenerated from one list rather than edited.

    python3 -I set-outcome.py <punch-items.py> <PL-NNN> <disp> <state|-> <note>

disp is open, deferred, resolved or withdrawn; state is a proved: class
(fix-pending-image, fix-host-regen, ...) or '-' for none. The note must cite
a commit in backticks or an issue number, as the lint requires.
"""
import re, sys

path, pl, disp, state, note = sys.argv[1:6]
assert disp in ("open", "deferred", "resolved", "withdrawn"), disp
assert disp == "open" or re.search(r"`[0-9a-f]{7,40}`|#\d+", note), "the note cites neither a commit nor an issue"
s = open(path).read()
i = s.index(f'dict(id="{pl}"')
j = s.index("\n dict(", i + 1) if "\n dict(" in s[i + 1:] else s.index("\n]", i)
item = s[i:j]
item = re.sub(r'disp="[^"]*"', f'disp="{disp}"', item, count=1)
item = re.sub(r', state="[^"]*"', "", item)
if state != "-":
    item = item.replace(f'disp="{disp}"', f'disp="{disp}", state="{state}"', 1)
esc = note.replace("\\", "\\\\").replace('"', '\\"')
item, n = re.subn(r'note="(?:[^"\\]|\\.)*"', lambda m: f'note="{esc}"', item, count=1)
assert n == 1, pl
open(path, "w").write(s[:i] + item + s[j:])
print(f"{pl}: {disp}{' (' + state + ')' if state != '-' else ''}")
