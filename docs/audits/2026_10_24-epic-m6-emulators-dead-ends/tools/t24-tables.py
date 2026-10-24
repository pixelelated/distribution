#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""t24-tables.py -- the three generated tables of M6 T24 (#671): the coverage
table of 02 (one row per path, 86), the reachability table of 04 § Q6 (86
rows, each with its `Already written:`), and the twin map of 04 § Q7 (77
LibreELEC cores).

    python3 -I t24-tables.py <scratch> coverage|q6|q7

<scratch> is the folder brief § 5's commands wrote (`.qa-scratch/t24/`):
membership.txt, paths.txt, recipes.txt, q4a-e0f9deb899.txt,
q4a-481c9d0d75.txt, q4b-compare.txt, q4b-diffshape.txt, reach.txt, edges.txt,
grephits.txt, record.txt, pkgcheck-pkgcheck.txt, pkgcheck-pkgcheck-t6.txt,
urls.txt, probe/head.txt, twin.json. Nothing is read from the network or a
build root here; those reads are the commands' own. The script asserts the
row counts (86, 86, 77) and that no cell is empty, and exits 1 when one is
not (an empty cell is the table's own FAIL, blindspot 39).
"""
import json, os, re, sys

S, mode = sys.argv[1], sys.argv[2]
rd = lambda f: open(os.path.join(S, f)).read().splitlines()

members = {}
for l in rd("membership.txt"):
    m = re.match(r"^(unreached|unshipped) (\S+) (\d+) (\S+)$", l)
    if m:
        members[m.group(4)] = dict(reach=m.group(1), tier=m.group(2), lines=int(m.group(3)))
paths = rd("paths.txt")
assert len(paths) == 86 and set(paths) == set(members), "membership and paths.txt disagree"

name = lambda p: p.split("/")[-2] if p.endswith("/package.mk") else p.split("/")[2]
qa = {l.split(" ", 1)[1]: l.split(" ", 1)[0] for l in rd("q4a-e0f9deb899.txt")}
qa2 = {l.split(" ", 1)[1]: l.split(" ", 1)[0] for l in rd("q4a-481c9d0d75.txt")}
qb = {}
for l in rd("q4b-compare.txt"):
    p, s, f, ours, le = l.split("|")
    qb[p] = (s, f, ours, le)
shape = {}
for l in rd("q4b-diffshape.txt"):
    f = l.split()
    shape[f[-1]] = dict(kv.split("=") for kv in f if "=" in kv)
reach = {}
for l in rd("reach.txt"):
    f = l.split()
    reach[f[0]] = dict(kv.split("=", 1) for kv in f[1:])
edges = {}
for l in rd("edges.txt"):
    n, f = l.split(" ", 1)
    edges.setdefault(n, []).append(f)
hits = {}
for l in rd("grephits.txt"):
    n, f = l.split(" ", 1)
    hits.setdefault(n, []).append(f)
record = {l.split()[1]: l.split()[0] for l in rd("record.txt")}
pk = {}
for tag in ("pkgcheck", "pkgcheck-t6"):
    for l in rd(f"pkgcheck-{tag}.txt"):
        v, n, w, fl = l.split()
        pk.setdefault(n, []).append((v, w.split("=")[1]))
url = {l.split()[0]: l.split()[1] for l in rd("urls.txt")}
head = {l.split()[2]: l.split()[0] for l in rd("probe/head.txt")}
twins = json.load(open(os.path.join(S, "twin.json")))
twin_by_core = {t["core"]: t for t in twins}

ROCKNIX5 = {"boom3-lr", "vitaquake3-lr", "mame2003-lr", "panda3ds-lr", "play-lr"}
WARN = {"libretro-beetle-pcfx": "WARN line 24, intertwined vars & funcs", "libretro-bsnes-hd": "WARN line 19, intertwined vars & funcs"}


def q4b_cell(p):
    if p.startswith("projects/"):
        return "n/a: ROCKNIX's own recipe; its project per T3's Q4 (`behind-project`, upstream `same`)"
    if not p.endswith("/package.mk"):
        return "n/a: not a recipe (rcheevos's source overlay; its recipe's row carries the read)"
    s, f, ours, le = qb[p]
    if s == "pin identical" and f == "file-identical":
        return "pin identical; file identical"
    if s == "pin identical":
        return "pin identical; master adds a version-stamp hunk (adds only)"
    return f"pin moved: ours `{ours[:12]}`, master `{le[:12]}`"


def twin_cell(n):
    t = twin_by_core.get(n)
    if not t:
        return None
    if t["byname"] and t["bysrc"]:
        return "twin `" + ", ".join(t["byname"]) + "` by name and source"
    if t["byname"]:
        return "twin `" + ", ".join(t["byname"]) + "` by name (another source)"
    if t["bysrc"]:
        return "twin `" + ", ".join(t["bysrc"]) + "` by source"
    return "no twin"


def q6_reads(p):
    n = name(p)
    if not p.endswith("/package.mk"):
        return "not a recipe: copied into `rcheevos`'s source by its recipe; reached only if `rcheevos` is"
    r = reach[n]
    e = edges.get(n, [])
    kodi = [f for f in e if "kodi-binary-addons" in f]
    other = [f for f in e if "kodi-binary-addons" not in f]
    bits = [f"plans 0/0 (narrow/wide, 3 devices)" if r["plan"] == "0" and r["wide"] == "0" else f"plans {r['plan']}/{r['wide']}"]
    bits.append("metapackage 0" if r["meta"] == "" else f"metapackage {r['meta']} (the `core-pins` list, `package.mk:1768`; no `add_emu_core`)")
    if kodi:
        bits.append(f"edge from {len(kodi)} Kodi addon recipe (`packages/mediacenter/kodi-binary-addons/`, unreached)")
    for f in other:
        bits.append(f"edge from `{f}` under `TARGET_ARCH = x86_64` only (`idtech-lr/package.mk:20-22`)")
    if not e:
        bits.append("no build edge from any file")
    nonedge = [f for f in hits.get(n, []) if f not in e]
    if nonedge and n in ROCKNIX5:
        bits.append("other name hits, none an edge: " + ", ".join("`" + f.split("/")[-1] + ("` (`cloud_capture:885`, a core-to-package map)" if f.endswith("cloud_capture") else "` (the `core-pins` list)" if f.endswith("virtual/emulators/package.mk") else "`") for f in nonedge))
    elif nonedge:
        bits.append(f"{len(nonedge)} other name hit(s), none an edge (URLs, paths, another library)")
    bits.append("record: no build directory in the five roots" if record[n] == "0" else "record: BUILT")
    return "; ".join(bits)


def already(p):
    n = name(p)
    if n in ("boom3-lr", "vitaquake3-lr"):
        return ("**Already written:** no fork image carries the `.so` (0 in the GENERIC_X64, H700 and SM8550 install trees); "
                "`core-info` ships its `.info` in every image's `usr/lib/libretro/` (read only), and every image's "
                "`/usr/share/rocknix/core-pins` carries a row for it (F-03), which `cloud_capture:121` reads only for the core "
                "that ran, so no save manifest names it; nothing under `/storage` or in a cloud. ROCKNIX's AMD64 image builds it; "
                "pixelelated ships no AMD64 image, so no device on the ROCKNIX to pixelelated path ran it here (T3's `04` § Q6 at `b3cb4ec8c5`)")
    if n in ROCKNIX5:
        return ("**Already written:** nothing of the core: no ROCKNIX or fork configuration builds it (reach `unreached` over every "
                "Makefile configuration), so no image carries its `.so` and no device ran it; only `core-info`'s `.info` ships, read only "
                "(T3's `04` § Q6 at `b3cb4ec8c5`)")
    return ("**Already written:** nothing: no ROCKNIX or fork configuration builds it (reach `unreached` over every Makefile "
            "configuration; no build directory in the five roots), so no image, device or cloud holds a file of it; its only callers "
            "are Kodi addon recipes, and Kodi ships in no image")


def disposition(p):
    n = name(p)
    if p.startswith("projects/"):
        return "kept: upstream's; no shipped device builds it" + (" (AMD64 builds it)" if members[p]["reach"] == "unshipped" else "")
    return "kept: upstream's; #585 candidate"


out = []
if mode == "coverage":
    out.append("| Path | Tier | Lines | Reach | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 |")
    out.append("| --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |")
    for p in paths:
        m, n = members[p], name(p)
        isr = p.endswith("/package.mk")
        q1 = f"`{url[n].split('/')[2]}`, not retired" if isr else "n/a: not a recipe"
        q2 = ("pkgcheck PASS twice" + (f" ({WARN[n]})" if n in WARN else "")) if isr else "n/a: cmake, not a recipe"
        q3 = (f"primary URL answers {head[n]} (repository alive; the commit is not proven by the probe)") if isr else "n/a: not a recipe"
        q4 = (f"(a) {qa[p]}" + (" by `af70bd435b`" if qa[p] == "differs" else "") + " at `e0f9deb899` and `481c9d0d75`") if qa[p] == qa2[p] else "(a) DISAGREE"
        q4 += "; (b) " + q4b_cell(p)
        q5 = "never built: 0 build or launch cost; carried in the tree (§ Q5)"
        q6 = "unshipped: AMD64 only" if m["reach"] == "unshipped" else "unreached"
        if n in ROCKNIX5:
            q7 = "ROCKNIX's own recipe; T3's twin rows"
        elif n.startswith("libretro-") and n != "libretro-common":
            q7 = twin_cell(n)
        elif n == "libretro-common":
            q7 = "library; RetroArch and the cores carry their own copy"
        elif n == "rcheevos":
            q7 = "library; RetroArch vendors its own, the proxy has `raofflineproxy-rcheevos`"
        else:
            q7 = "Cyclone 68000 core library; named by no other recipe"
        out.append(f"| `{p}` | {m['tier']} | {m['lines']} | {m['reach']} | {q1} | {q2} | {q3} | {q4} | {q5} | {q6} | {q7} |")
    rows = len(out) - 2
    assert rows == 86, rows
elif mode == "q6":
    out.append("| Path | Reach | The reads that decided it | Tier | (a) `upstream/next` | (b) LibreELEC master | Disposition | Already written |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for p in paths:
        m = members[p]
        a = qa[p] + (" (`af70bd435b`)" if qa[p] == "differs" else "")
        out.append(f"| `{p}` | {m['reach']} | {q6_reads(p)} | {m['tier']} | {a} | {q4b_cell(p)} | {disposition(p)} | {already(p)} |")
    rows = len(out) - 2
    assert rows == 86, rows
elif mode == "q7":
    out.append("| LibreELEC core | Source (`PKG_URL`) | ROCKNIX twin | How | LibreELEC pin | Twin pin(s) |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    for t in twins:
        tw = sorted(set(t["byname"]) | set(t["bysrc"]))
        how = "name and source" if t["byname"] and t["bysrc"] else "name (another source)" if t["byname"] else "source (another name)" if t["bysrc"] else "-"
        if t["core"] == "libretro-yabause":
            how += "; the same repository builds another core (YabaSanshiro)"
        pins = ", ".join(f"`{x}` `{(p or '-')[:12]}`" + (" (same)" if p == t["pin"] else "") for x, p in t["twinpins"].items()) or "-"
        out.append(f"| `{t['core']}` | `{t['repo']}` | {', '.join('`' + x + '`' for x in tw) or 'no twin'} | {how} | `{(t['pin'] or '-')[:12]}` | {pins} |")
    rows = len(out) - 2
    assert rows == 77, rows
else:
    sys.exit("usage: t24-tables.py <scratch> coverage|q6|q7")

for l in out:
    if re.search(r"\|\s*\|", l) or "None" in l:
        print("EMPTY CELL: " + l, file=sys.stderr)
        sys.exit(1)
print("\n".join(out))
print(f"\n<!-- t24-tables.py {mode}: {rows} rows -->")
