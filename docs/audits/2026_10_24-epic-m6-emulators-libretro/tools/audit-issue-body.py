#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""audit-issue-body.py -- the stage-D audit issue's body from the same item
list as 05-punch-list.md (tools/punch-items.py), so the issue's checkboxes
are the punch list's items, one each (M6 T3, #650).

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
o.append(f"Punch list of the M6 T3 audit (#650): RetroArch and the libretro cores, 344 paths, `reviewed-at: d606301784` (the slice's bytes equal to `next`'s `8ebaf8daad`). The audit is `docs/audits/2026_10_24-epic-m6-emulators-libretro/` on `feature/m6-emulators-libretro-650`. {len(ITEMS)} items: {c['Critical']} critical, {c['High']} high, {c['Medium']} medium, {c['Low']} low.\n")
o.append("## Executive summary\n")
o.append("The launch table is the build's own: the host regeneration from the tree's shell is byte-identical to the GENERIC_X64, H700 and SM8550 images, and the guest's installed set equals the tree's.")
o.append("")
o.append("**The four High findings:**")
o.append("")
o.append("- The default PlayStation core on four built devices is installed where the launcher does not load it (#802).")
o.append("- The next base merge brings upstream's fix for that, and the new `yabadabadoo-lr`, as `build.${DISTRO}-` copies that fail on the fork's roots (#802).")
o.append("- SM8550's grep has no PCRE, so Install Steam stops at its Proton step (#806).")
o.append("- `aethersx2-sa`, dropped upstream for licensing, still ships on SM8550.")
o.append("")
o.append("**Currency:** all 14 upstream commits on the slice are `to merge`, two of them adapted. Of the 151 pins, 40 are current, 104 behind their project, 1 behind ROCKNIX and 6 not on their project's default branch. RetroArch is 7,623 commits behind master, and a bump is a re-cut of its patch series.")
o.append("")
o.append("**Time to play** on the image as built: 0.62 s to the first frame and 1.01 s game to game (n = 3).\n")
o.append("## Acceptance-criteria scorecard (#650, at the end of Phase 2)\n")
o.append("4 PASS (AC-06, AC-07, AC-08, AC-12); 5 PARTIAL (AC-01, AC-05, AC-09, AC-10, AC-11); 6 open for later stages of the lane (AC-02, AC-03, AC-04, AC-13, AC-14, AC-15); 0 FAIL. `02-forward-audit.md` § Criterion entries has each with its evidence.\n")
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
o.append("#336 (the libretro runner: RetroArch's menu and widget items are `deferred:#336` for the 2D cores), #762 (Kronos's options, T1's), #730 (`-P` in the launch line, T1's), #613 (the table's fallback symlink, T2's), #652 (T5: the table's default-marking mechanism, F-06), #669 (T22: grep's PCRE dependency, #806's recipe layer).\n")
o.append("Refs #650, #798, #339.")
if bad:
    sys.exit("audit-issue-body: checkboxes naming a person or device without a fact: " + ", ".join(bad))
sys.stdout.write("\n".join(o) + "\n")
print(f"audit-issue-body: {len(ITEMS)} checkboxes, 0 box-check failures", file=sys.stderr)
