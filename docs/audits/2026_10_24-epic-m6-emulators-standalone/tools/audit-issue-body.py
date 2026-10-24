#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
# Copied for M6 T30 (#677) from T3's docs/audits/2026_10_24-epic-m6-emulators-libretro/tools/audit-issue-body.py at b3cb4ec8c5
# (feature/m6-emulators-libretro-650); T30's changes, if any, are named below.
"""audit-issue-body.py -- the stage-D audit issue's body from the same item
list as 05-punch-list.md (tools/punch-items.py), so the issue's checkboxes
are the punch list's items, one each (M6 T30, #677; T3's text replaced -- the T30 change).

    python3 -I audit-issue-body.py > body.md

Checks every checkbox against tools/box-check's own PERSON/DEVICE/FACT
patterns and exits 1 on one that names a person or a device without a fact.
"""
import os, re, sys
from collections import Counter

here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "punch-items.py")).read()
ns = {}
exec(src[:src.index("\nout = []")], ns)
ITEMS = ns["ITEMS"]
tree = os.path.abspath(os.path.join(here, "../../../.."))
bc = open(os.path.join(tree, "tools/box-check")).read()
pat = {}
exec("\n".join(l for l in bc.splitlines() if re.match(r'^(PERSON|DEVICE|FACT) = re\.compile', l)), {"re": re}, pat)

c = Counter(i["sev"] for i in ITEMS)
o = []
o.append(f"Punch list of the M6 T30 audit (#677): the standalone emulators, 543 paths, `reviewed-at: c7e3dfcc87` (the slice's bytes equal to `next`'s `8ebaf8daad`). The audit is `docs/audits/2026_10_24-epic-m6-emulators-standalone/` on `feature/m6-emulators-standalone-677`. {len(ITEMS)} items: {c['Critical']} critical, {c['High']} high, {c['Medium']} medium, {c['Low']} low. Depth: Extended (GPT-6 Astra and Gemini 4 Argon, the latter on a trimmed packet, D-WORKFLOW-195).\n")
o.append("## Executive summary\n")
o.append("**The two High findings:**")
o.append("")
o.append("- A `.scummvm` file in the ROM library runs as shell, as root, at launch (PL-007, #859; proven on the guest).")
o.append("- Start scripts delete a real directory before linking it; a save state made in DuckStation from the Tools launcher is deleted by the next game launch (PL-012, #863; proven on the guest).")
o.append("")
o.append("**The exit hotkey does nothing** in DuckStation (every image; its psx default on the VM), OpenBOR, Mupen64Plus's simple core and the hatarisa route (PL-001 to PL-004). **The previous RetroAchievements session stays signed in** in five achievements scripts (PL-009). Six of the defects are fixed upstream after our base (class 1 with the base merge). `portaudio`'s source is gone (#849).")
o.append("")
o.append("**Time to play** (`runemu.sh` to the emulator, n = 3): gzdoom's first frame 1.03-3.13 s with Freedoom; ScummVM's first draw 0.64-1.08 s; ppsspp, x64sc and DuckStation 0.52-0.67 s to the process. Not the interface's press (an SSH launch).\n")
o.append("## Acceptance-criteria scorecard (#677, at stage D)\n")
o.append("Met: criteria 6, 7, 8, 9, 10, 11, 12 (21 = 21) and 14 (three guest cycles); the lint `PASS pre-issue artifacts`; open for later stages: 1 (05 lands with this issue), 2 (resolution), 4, 5, 13, 15, 16.\n")
o.append("## The items\n")
o.append("Each checkbox is ticked from its acceptance artifact when its Phase 7 outcome is recorded in `05-punch-list.md` (resolved with its commit, deferred to a named issue, or withdrawn with its reason).\n")
bad = []
for i in ITEMS:
    tr = f" ({i['tracked']})" if i.get("tracked") else ""
    line = f"- [ ] **{i['id']}** ({i['sev']}, {i['q']}, {i['cat']}){tr}: {i['title']}. Acceptance: {i['acc']}"
    if (pat["PERSON"].search(line) or pat["DEVICE"].search(line)) and not pat["FACT"].search(line):
        bad.append(i["id"])
    o.append(line)
o.append("\n## Pre-existing tracked scope (not punch items)\n")
o.append("#849 (portaudio's source: PL-013), #336 (the headless libretro runner, not this slice's), #648 (T1: `runemu.sh`, `input_sense`), #650 (T3: the launch table's file, where PL-005 and PL-022 live), #520 (the standalone save layout), #117 (TERM before KILL for RetroArch: PL-035's precedent).\n")
o.append("Refs #677, #798, #339.")
if bad:
    sys.exit("audit-issue-body: checkboxes naming a person or device without a fact: " + ", ".join(bad))
sys.stdout.write("\n".join(o) + "\n")
print(f"audit-issue-body: {len(ITEMS)} checkboxes, 0 box-check failures", file=sys.stderr)
