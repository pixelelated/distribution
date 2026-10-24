#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""coverage-table.py -- 02-forward-audit.md's coverage table, one row per path
of the slice (M6 T3, #650 criterion 7).

    python3 -I coverage-table.py <tree> <audit-dir> > table.md

The membership is brief section 2's filter over docs/reviews/inventory.json.
Each row: the path in backticks, its group, its tier, its Q1 to Q7 cells and,
for a fork-own path, the fork commits read. A cell is the findings that name
the path (the FINDINGS map below, written from 02's findings), else the slice
table that answers it (Q4: q4-pins.json, q4a-dispositions.md; Q6:
q6-tables.md), else `n/a` with its reason. An upstream-carried recipe's Q1,
Q2, Q3 and Q7 read `n/a: upstream's recipe, unchanged here` (brief section 4)
unless a finding names it. The script asserts 344 rows and no empty cell.
"""
import json, re, subprocess, sys, os

tree, audit = sys.argv[1:3]
inv = json.load(open(os.path.join(tree, "docs/reviews/inventory.json")))
cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]

def gm(p, g):
    return re.fullmatch(re.escape(g).replace(r"\*\*/", "(?:.*/)?").replace(r"\*\*", ".*").replace(r"\*", "[^/]*"), p) is not None

rules = [({"emulators-and-cores"}, ["projects/ROCKNIX/packages/emulators/**"], ["projects/ROCKNIX/packages/emulators/standalone/**"], {"shipped", "test", "n/a"}),
         ({"patches-and-configs"}, ["projects/ROCKNIX/packages/emulators/libretro/retroarch/**"], [], None),
         ({"generic-packages"}, ["projects/ROCKNIX/packages/virtual/emulators/**"], [], None)]
sel = {}
for areas, inc, exc, reach in rules:
    for r in rows:
        if r["tree"] != "distribution" or r["area"] not in areas: continue
        if reach and r["reach"] not in reach: continue
        if not any(gm(r["path"], g) for g in inc) or any(gm(r["path"], g) for g in exc): continue
        sel[r["path"]] = r

LR = "projects/ROCKNIX/packages/emulators/libretro/"
VE = "projects/ROCKNIX/packages/virtual/emulators/"
RA = LR + "retroarch/"

# Findings by path prefix -> {question: text}. Written from 02's F-NN entries.
FINDINGS = [
    (RA + "package.mk", {"Q1": "F-13 (dead status checks)", "Q2": "PASS (header, guard 129-134)", "Q3": "F-11 (retroarch32 skipped silently, latent); F-08's mechanism", "Q5": "five tmp-*.mount at boot (not measured)", "Q6": "/etc/retroarch.cfg read by no script (row)", "Q7": "libass twice; `empty` dependency unexplained"}),
    (RA + "sources/GENERIC_X64/retroarch.cfg", {"Q1": "F-12 (24 keys not read)", "Q2": "PASS (no credential value shipped)", "Q3": "P1: installed = tree's hash", "Q5": "P2, P4 (log_verbosity: no measured cost)", "Q6": "F-12; F-14 (video_font_path)", "Q7": "Q7 copies table (F-12)"}),
    (RA + "sources/GENERIC_X64/", {"Q1": "n/a: a data file of four lines or a remap", "Q2": "PASS (P1 hash = tree's)", "Q3": "P1", "Q5": "n/a: read once at launch", "Q6": "Table 4 (built)", "Q7": "n/a: data"}),
    (RA + "sources/", {"Q1": "F-12 (not-read keys, same lines in every profile)", "Q2": "n/a: upstream's profile, unchanged here", "Q3": "F-12 (armhf core-updater URL on aarch64 profiles)", "Q5": "not measured: no guest for this panel", "Q6": "Table 4", "Q7": "F-12 (copies: SM4450 = SM8250 = SM8550)"}),
    (RA + "patches/0011-video-thread-wrapper", {"Q1": "n/a: a fix, current at the pin", "Q2": "PASS (applies at fuzz 0)", "Q3": "PASS (reading); not driven by the wrapper test", "Q4": "Q4 (c): superseded on master (#19518)", "Q5": "one mutex per post (not measured)", "Q6": "Table 5; retires with a bump", "Q7": "PASS (header says why)"}),
    (RA + "patches/0015-", {"Q1": "n/a: a fix", "Q2": "PASS (fuzz 0)", "Q3": "PASS: wrapper test 2000/2000, reversed 2011/2000", "Q4": "Q4 (c): fixed on master (#19577)", "Q5": "n/a: no added work on the frame path", "Q6": "Table 5; retires with a bump", "Q7": "PASS"}),
    (RA + "patches/0013-", {"Q1": "n/a", "Q2": "PASS (strings in us/fr)", "Q3": "PASS (header parse bounded, flags reset per callback)", "Q4": "Q4 (c): fails at master", "Q5": "n/a: one header scan per HTTP answer", "Q6": "Table 5; reached when the proxy is on", "Q7": "PASS"}),
    (RA + "patches/0014-", {"Q1": "deferred:#336 (widget surface)", "Q2": "PASS (fuzz 0)", "Q3": "PASS (reading)", "Q4": "Q4 (c): fails at master", "Q5": "deferred:#336", "Q6": "Table 5", "Q7": "deferred:#336"}),
    (RA + "patches/0016-", {"Q1": "deferred:#336", "Q2": "PASS", "Q3": "PASS; P3: floor 13 engages", "Q4": "Q4 (c): fails at master", "Q5": "deferred:#336", "Q6": "Table 5; reached (P3)", "Q7": "measured for Inter, drawn on M+ 1p (with F-14)"}),
    (RA + "patches/0017-", {"Q1": "deferred:#336", "Q2": "PASS", "Q3": "PASS (reading)", "Q4": "Q4 (c): fails at master", "Q5": "deferred:#336", "Q6": "F-14: its step engages on no shipped profile (P3)", "Q7": "F-14"}),
    (RA + "patches/0018-", {"Q1": "n/a", "Q2": "PASS", "Q3": "PASS: P3b on the guest; config_append_file read", "Q4": "Q4 (c): fails at master (#19223)", "Q5": "n/a: one pointer compare per load", "Q6": "Table 5; reached (P3b)", "Q7": "PASS"}),
    (RA + "patches/0019-", {"Q1": "deferred:#336", "Q2": "PASS", "Q3": "PASS (lock read at 676/728/1196/1220)", "Q4": "Q4 (c): fuzz at master", "Q5": "deferred:#336", "Q6": "Table 5", "Q7": "deferred:#336"}),
    (RA + "patches/0004-", {"Q2": "F-10 (applies only with fuzz)", "Q4": "Q4 (c): fuzz at master"}),
    (RA + "patches/", {"Q1": "n/a: an upstream patch, a provenance row", "Q2": "PASS at the pin (Q4 (c))", "Q3": "n/a: upstream's patch, unchanged here", "Q4": "Q4 (c) row", "Q5": "n/a: upstream's patch", "Q6": "Table 5", "Q7": "n/a: upstream's patch"}),
    (VE + "package.mk", {"Q1": "n/a: the table's idiom is T5's functions", "Q2": "pkgcheck rc 0 (install_script warn read); shellcheck read", "Q3": "F-05 (psx/st-v); F-08 (default psx core); F-06 (default rule, T5's)", "Q4": "F-07 (aethersx2), Q4 (a) rows 1, 3, 4", "Q5": "n/a: build time only", "Q6": "Table 2; F-18 (#16 closed)", "Q7": "F-06 comment; F-18"}),
    (VE + "sources/Install Steam.sh", {"Q1": "F-23 (deferred:M7-merge)", "Q2": "F-20 eval (deferred:M7-merge; M7's 6101242e14 fixes)", "Q3": "F-19 (grep -P on SM8550), F-21, F-22 (deferred:M7-merge)", "Q5": "F-23 lead (FEX re-fetch)", "Q6": "Table 3 (SM8550); F-23 dead assignments", "Q7": "F-23"}),
    (VE + "sources/Start Azahar.sh", {"Q2": "F-04 (line-2 shebang)"}),
    (VE + "sources/Start MelonDS.sh", {"Q2": "F-04 (line-2 shebang)"}),
    (VE + "sources/Start RPCS3.sh", {"Q3": "Q4 (a) row 9: kill target `rpcs3`, binary `rpcs3-sa`", "Q4": "Q4 (a) row 9 to merge"}),
    (VE + "sources/Start AetherSX2.sh", {"Q4": "Q4 (a) rows 1, 9 (F-07)"}),
    (VE + "sources/", {"Q1": "n/a: upstream's launcher, unchanged here", "Q2": "shellcheck read (§ shellcheck)", "Q3": "n/a: upstream's launcher, unchanged here", "Q4": "Q4 (a): no row unless named", "Q5": "n/a: standalone emulator start, T30's", "Q6": "Table 3", "Q7": "n/a: upstream's launcher, unchanged here"}),
    (VE + "udev.d/99-automount.rules", {"Q4": "Q4 (a) rows 11 to 13 to merge"}),
    (VE, {"Q1": "n/a: upstream's file, unchanged here", "Q2": "shellcheck read where shell", "Q3": "n/a: upstream's file, unchanged here", "Q4": "Q4 (a): no commit on it", "Q5": "n/a: boot or build only", "Q6": "installed on every built device (the recipe's makeinstall_target)", "Q7": "n/a: upstream's file, unchanged here"}),
    (LR + "sameboy-lr/package.mk", {"Q2": "F-02 (late binding, pkgcheck FAIL)", "Q6": "F-02 (dead option)"}),
    (LR + "flycast2021-lr/package.mk", {"Q2": "F-03 (cosmetic warn)", "Q7": "F-03"}),
    (LR + "melonds-ds-lr/package.mk", {"Q3": "F-15 (FetchContent at configure)", "Q4": "F-15 (eleven unpinned dependencies)"}),
    (LR + "easyrpg-lr/wildmidi/package.mk", {"Q2": "F-16 (short-hash pin)"}),
    (LR + "rotation-table-", {"Q1": "PASS (Python 3, stdlib)", "Q2": "PASS (floor guard, reason on refusal)", "Q3": "PASS: byte-identical to the image, constructed failures seen", "Q4": "n/a: the fork's own tool", "Q5": "1 to 3 s at build", "Q6": "reach n/a: build time; called by five recipes", "Q7": "PASS"}),
]
ROT = ["fbalpha2012-lr", "fbalpha2019-lr", "fbneo-lr", "mame2003-plus-lr", "mame2010-lr"]

q4 = {r["path"]: r for r in json.load(open(os.path.join(audit, "q4-pins.json")))["rows"]}
byhand = {"libxmp-lite": "behind-project (by hand)", "emuscv-lr": "behind-project (by hand)", "idtech-lr": "current (by hand)"}
fork_commits = {}
def commits(p):
    out = subprocess.run(["git", "-C", tree, "log", "--no-merges", "--format=%h", "c445081a59..8ebaf8daad", "--", p], capture_output=True, text=True).stdout.split()
    return " ".join(out[:6]) + (" ..." if len(out) > 6 else "")

def group(p):
    if p.startswith(RA): return 1
    if p.startswith(VE): return 2
    if p.startswith(LR + "rotation-table") or sel[p]["tier"] == "fork-own": return 3
    return 4

out = ["| Path | Group | Tier | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Fork commits read |", "| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
empty = []
for p in sorted(sel):
    r = sel[p]; cells = {}
    for prefix, qs in FINDINGS:
        if p.startswith(prefix):
            for k, v in qs.items(): cells.setdefault(k, v)
    name = p.split("/")[-2] if p.endswith("package.mk") else None
    if p.endswith("package.mk") and p.startswith(LR) and not p.startswith(RA + "package"):
        row = q4.get(p)
        cls = byhand.get(name) or (row["class"] if row else "?")
        cells.setdefault("Q4", f"Q4 (b): {cls}" + ("; Q4 (a) row" if name in ("np2kai-lr", "pcsx_rearmed-lr", "mame-lr", "emuscv-lr", "same_cdi-lr", "uae4arm-lr", "vircon32-lr", "flycast2021-lr", "doublecherrygb-lr") else ""))
        cells.setdefault("Q6", "Table 1")
        if name in ROT:
            cells.setdefault("Q3", "PASS: its table regenerates byte-identically")
            cells.setdefault("Q7", "F-17 (the hook in five copies)")
        if r["tier"] == "fork-own":
            for k in ("Q1", "Q2", "Q3", "Q7"): cells.setdefault(k, "PASS (the fork's delta read, group 3 table)")
            cells.setdefault("Q5", "n/a: build-time recipe")
        else:
            for k in ("Q1", "Q2", "Q3", "Q7"): cells.setdefault(k, "n/a: upstream's recipe, unchanged here")
            cells.setdefault("Q5", "n/a: upstream's recipe, build time")
    elif p.startswith(LR) and not p.startswith(RA):
        # a non-recipe file under a core's directory (other than patches, outside the membership)
        for k in ("Q1", "Q2", "Q3", "Q5", "Q7"): cells.setdefault(k, "n/a: upstream's file, unchanged here")
        cells.setdefault("Q4", "with its recipe's Q4 (b) row"); cells.setdefault("Q6", "with its recipe's Table 1 row")
    elif p.startswith(RA):
        for k in ("Q1", "Q2", "Q3", "Q5", "Q7"): cells.setdefault(k, "n/a: upstream's RetroArch file, unchanged here")
        cells.setdefault("Q4", "with RetroArch's Q4 (c)"); cells.setdefault("Q6", "installed by the recipe on every built device")
    for k in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"):
        if not cells.get(k): empty.append((p, k))
    fc = commits(p) if r["tier"] == "fork-own" else "-"
    esc = lambda s: s.replace("|", "/")
    out.append(f"| `{p}` | {group(p)} | {r['tier']}{' (fork-written)' if r['tier_note']=='fork-written' else ''} | " + " | ".join(esc(cells.get(k, '')) for k in ("Q1","Q2","Q3","Q4","Q5","Q6","Q7")) + f" | {fc} |")
assert not empty, f"empty cells: {empty[:10]}"
assert len(out) - 2 == 344, f"{len(out)-2} rows"
print("\n".join(out))
print(f"coverage-table: {len(out)-2} rows, 0 empty cells", file=sys.stderr)
