#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""q6-tables.py -- the reachability tables of M6 T3's Q6 (#650; brief section 4).

    python3 -I q6-tables.py <tree> <regen-dir> <out.md>

<regen-dir> holds tools/regen-es-systems.sh's output per device
(<regen-dir>/<DEVICE>/install/...), which is byte-identical to the image for
GENERIC_X64, H700 and SM8550. The five built devices are the fork's
(device-builds.md): H700, RK3326, RK3566, SM8550, GENERIC_X64.

Writes five tables:
  1. every *-lr recipe under emulators/libretro (131) with the built devices
     whose image carries it: directly (LIBRETRO_CORES, EMUS_32BIT,
     PKG_EMUS evaluated per device by sourcing the metapackage's global
     section in bash) or through a PKG_DEPENDS_TARGET of a recipe that is
     carried, transitively; checked against the inventory's reachable_by for
     the three images the fork ships;
  2. every add_es_system call's system (142) with, per device, whether the
     regenerated table has it, its emulator/core count, its default, and
     whether config/emulators/<system>.conf exists;
  3. every virtual/emulators/sources/*.sh (24) with the devices whose
     regenerated install tree carries it as /usr/config/modules/<name>;
  4. every retroarch/sources/<DEVICE>/ set (15) with whether the fork builds
     that device;
  5. every RetroArch patch (21) with the source files it touches.
Counts are compared and their differences listed, never asserted equal.
"""
import json, os, re, subprocess, sys

tree, regen, out = sys.argv[1:4]
DEVS = [("H700", "aarch64", "true"), ("RK3326", "aarch64", "true"), ("RK3566", "aarch64", "true"),
        ("SM8550", "aarch64", "true"), ("GENERIC_X64", "x86_64", "no")]
SHIPPED = {"H700": "H700-aarch64", "SM8550": "SM8550-aarch64", "GENERIC_X64": "GENERIC_X64-x86_64"}
L = "projects/ROCKNIX/packages/emulators/libretro"
V = "projects/ROCKNIX/packages/virtual/emulators"
mk = open(os.path.join(tree, V, "package.mk")).read()
glob_part = mk[:mk.index("install_script() {")]

def lists(dev, arch, e32):
    sh = f'DEVICE={dev}; ARCH={arch}; ENABLE_32BIT={e32}; TARGET_TYPE=; {glob_part}\n' \
         'echo "LC=$LIBRETRO_CORES"; echo "E32=$EMUS_32BIT"; echo "EMUS=$PKG_EMUS"; echo "RA=$PKG_RETROARCH"; echo "DEP=$PKG_DEPENDS_TARGET"'
    r = subprocess.run(["bash", "-c", sh], capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
    d = {}
    for line in r.stdout.splitlines():
        k, _, v = line.partition("=")
        d[k] = set(v.split())
    return d

recipes = {}
for root, ds, fs in os.walk(os.path.join(tree, L)):
    if "package.mk" in fs:
        name = os.path.basename(root)
        text = open(os.path.join(root, "package.mk")).read()
        deps = set()
        for m in re.finditer(r'PKG_DEPENDS_TARGET\+?="([^"]*)"', text):
            deps |= set(m.group(1).split())
        recipes[name] = {"path": os.path.relpath(os.path.join(root, "package.mk"), tree), "deps": deps}

def closure(start):
    seen, todo = set(), list(start)
    while todo:
        n = todo.pop()
        if n in seen: continue
        seen.add(n)
        if n in recipes: todo += [d for d in recipes[n]["deps"] if d in recipes]
    return seen

inv = json.load(open(os.path.join(tree, "docs/reviews/inventory.json")))
cols = inv["columns"]; irows = {r[1]: dict(zip(cols, r)) for r in inv["rows"] if r[0] == "distribution"}

direct = {}
for dev, arch, e32 in DEVS:
    d = lists(dev, arch, e32)
    direct[dev] = d["LC"] | d["E32"] | d["EMUS"]

# Table 1's columns are the inventory's (reachable_by + buildable_by, which
# P1's tool computed with each device's options and the dependency graph,
# conditional PKG_DEPENDS_TARGET included). The check: a recipe the
# metapackage lists directly for a device must be in the inventory's set for
# that device; a recipe in the inventory's set but not listed directly
# arrives through a dependency (idtech-lr's engines, easyrpg-lr's libraries).
CFG = {"H700": "H700-aarch64", "RK3326": "RK3326-aarch64", "RK3566": "RK3566-aarch64", "SM8550": "SM8550-aarch64", "GENERIC_X64": "GENERIC_X64-x86_64"}
o = []
lr = sorted(n for n in recipes if n.endswith("-lr") or n.endswith("_lr"))
o.append(f"### Table 1: the `*-lr` recipes ({len(lr)}) and the built devices whose image carries them\n")
o.append("Cells: `listed` (in the metapackage's `LIBRETRO_CORES`, `EMUS_32BIT` or `PKG_EMUS` for that device), `dep` (carried through another recipe's dependency), `-` (not carried). Source: the inventory's `reachable_by` and `buildable_by`; check: the metapackage's lists evaluated per device.\n")
o.append("| Recipe | Membership | H700 | RK3326 | RK3566 | SM8550 | GENERIC_X64 |\n| --- | --- | --- | --- | --- | --- | --- |")
disagree, none = [], []
for n in lr:
    r = irows.get(recipes[n]["path"], {})
    invset = set(r.get("reachable_by") or []) | set(r.get("buildable_by") or [])
    cells = []
    for d, _, _ in DEVS:
        inv_has = CFG[d] in invset
        if n in direct[d] and not inv_has: disagree.append(f"{n}@{d}")
        cells.append("listed" if (inv_has and n in direct[d]) else "dep" if inv_has else ("**listed, not in inventory**" if n in direct[d] else "-"))
    if all(c == "-" for c in cells): none.append(n)
    memb = "T24's (outside)" if r.get("reach") not in ("shipped", "test", "n/a") else r.get("tier")
    o.append(f"| `{n}` | {memb} | " + " | ".join(cells) + " |")
o.append(f"\n{len(lr)} recipes ({len([n for n in lr if irows.get(recipes[n]['path'],{}).get('reach') in ('shipped','test','n/a')])} in the membership); carried by no built device: {len(none)} ({', '.join('`'+x+'`' for x in none) or 'none'}); listed for a device but not in the inventory's set: {len(disagree)} ({', '.join(disagree) or 'none'}).\n")

calls = re.findall(r'^\s*add_es_system\s+(\S+)', mk, re.M)
o.append(f"### Table 2: the `add_es_system` calls ({len(calls)}; {len(set(calls))} distinct systems)\n")
import xml.etree.ElementTree as ET
tabs = {}
for dev, _, _ in DEVS:
    r = ET.parse(os.path.join(regen, dev, "install/usr/config/emulationstation/es_systems.cfg")).getroot()
    tabs[dev] = {s.findtext("name"): s for s in r.findall("system")}
o.append("| System | `.conf` | H700 | RK3326 | RK3566 | SM8550 | GENERIC_X64 |\n| --- | --- | --- | --- | --- | --- | --- |")
def cell(s):
    if s is None: return "-"
    cores = s.findall(".//core"); d = [c.text for c in cores if c.get("default") == "true"]
    return f"{len(s.findall('emulators/emulator'))}e/{len(cores)}c, default {d[0] if len(d)==1 else ('NONE' if not d else d)}"
noconf = []
for sname in sorted(set(calls)):
    conf = os.path.exists(os.path.join(tree, "config/emulators", sname + ".conf"))
    if not conf: noconf.append(sname)
    o.append(f"| `{sname}` | {'yes' if conf else '**no**'} | " + " | ".join(cell(tabs[d].get(sname)) for d, _, _ in DEVS) + " |")
o.append(f"\nSystems without a `.conf`: {noconf or 'none'}. Systems per regenerated table: " + ", ".join(f"{d} {len(tabs[d])}" for d, _, _ in DEVS) + ".\n")

srcs = sorted(f for f in os.listdir(os.path.join(tree, V, "sources")) if f.endswith(".sh"))
o.append(f"### Table 3: `virtual/emulators/sources/*.sh` ({len(srcs)}) and the devices that install them\n")
o.append("| Script | H700 | RK3326 | RK3566 | SM8550 | GENERIC_X64 |\n| --- | --- | --- | --- | --- | --- |")
noinst = []
for s in srcs:
    cells = ["yes" if os.path.exists(os.path.join(regen, d, "install/usr/config/modules", s)) else "-" for d, _, _ in DEVS]
    if "yes" not in cells: noinst.append(s)
    o.append(f"| `{s}` | " + " | ".join(cells) + " |")
o.append(f"\nInstalled on no built device: {len(noinst)} ({', '.join('`'+x+'`' for x in noinst) or 'none'}).\n")

sd = sorted(os.listdir(os.path.join(tree, L, "retroarch/sources")))
built = {d for d, _, _ in DEVS}
o.append(f"### Table 4: `retroarch/sources/<DEVICE>/` ({len(sd)})\n")
o.append("| Set | Files | The fork builds it |\n| --- | ---: | --- |")
for s in sd:
    o.append(f"| `{s}` | {len(os.listdir(os.path.join(tree, L, 'retroarch/sources', s)))} | {'yes' if s in built else 'no (kept for upstream)'} |")
o.append("")

pd = os.path.join(tree, L, "retroarch/patches")
ps = sorted(f for f in os.listdir(pd) if f.endswith(".patch")) + ["batteryplus/" + f for f in sorted(os.listdir(os.path.join(pd, "batteryplus")))]
o.append(f"### Table 5: the RetroArch patches ({len(ps)}) and the sources they touch at the pin\n")
o.append("| Patch | Files |\n| --- | --- |")
for p in ps:
    files = sorted({re.sub(r"^[^/]+/", "", l[4:].split("\t")[0].split(" ")[0]) for l in open(os.path.join(pd, p), errors="replace") if l.startswith("+++ ")})
    o.append(f"| `{p}` | " + ", ".join(f"`{f}`" for f in files) + " |")
open(out, "w").write("\n".join(o) + "\n")
print(f"q6-tables: {len(lr)} recipes ({len(none)} carried by none, {len(disagree)} listed but not in the inventory), {len(calls)} calls / {len(set(calls))} systems ({len(noconf)} without .conf), {len(srcs)} scripts ({len(noinst)} on no device), {len(sd)} source sets, {len(ps)} patches")
