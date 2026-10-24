#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""t24-twin.py -- M6 T24 (#671) brief § 4 Q7: each LibreELEC `libretro-*` core
under packages/emulation/ against the ROCKNIX `*-lr` recipes under
projects/ROCKNIX/packages/emulators/libretro/, by name (`<core>-lr`, `_` read
as `-`) and by source (the github/gitlab repository of PKG_URL, else PKG_SITE,
after `PKG_*` substitution).

    python3 -I t24-twin.py <at-hash export>     # writes ./twin.json, prints a summary and one line per core

The export is `git archive 8ebaf8daad packages/emulation
projects/ROCKNIX/packages/emulators/libretro`. Nothing is read from the network.
"""
import os, re, sys, json
root = sys.argv[1]
def fields(path):
    v = {}
    for line in open(path, errors="replace"):
        m = re.match(r'^(PKG_[A-Z_]+)="([^"]*)"', line)
        if m and m.group(1) not in v: v[m.group(1)] = m.group(2)
    for _ in range(3):
        for k in v: v[k] = re.sub(r'\$\{?(PKG_[A-Z_]+)\}?', lambda m: v.get(m.group(1), m.group(0)), v[k])
    return v
def repo(v):
    for k in ("PKG_URL", "PKG_SITE"):
        m = re.search(r'github\.com/([^/]+)/([^/.#?]+)', v.get(k, ""))
        if m: return (m.group(1) + "/" + m.group(2)).lower()
        m = re.search(r'(gitlab\.com|codeberg\.org|bitbucket\.org)/([^/]+)/([^/.#?]+)', v.get(k, ""))
        if m: return (m.group(2) + "/" + m.group(3)).lower()
    return None
lr_dir = os.path.join(root, "projects/ROCKNIX/packages/emulators/libretro")
lrs = {}
for dp, dn, fn in os.walk(lr_dir):
    if "package.mk" in fn:
        n = os.path.basename(dp); v = fields(os.path.join(dp, "package.mk")); lrs[n] = (v, repo(v))
le_dir = os.path.join(root, "packages/emulation")
rows = []
for n in sorted(os.listdir(le_dir)):
    if not n.startswith("libretro-") or n == "libretro-common": continue
    v = fields(os.path.join(le_dir, n, "package.mk")); r = repo(v); base = n[len("libretro-"):]
    byname = sorted({x for x in (base + "-lr", base.replace("_", "-") + "-lr", base + "_lr") if x in lrs})
    bysrc = sorted(x for x, (lv, lr) in lrs.items() if r and lr == r)
    rows.append(dict(core=n, repo=r, pin=v.get("PKG_VERSION"), byname=byname, bysrc=bysrc,
                     twinpins={x: lrs[x][0].get("PKG_VERSION") for x in sorted(set(byname) | set(bysrc))}))
json.dump(rows, open("twin.json", "w"), indent=1)
print("cores", len(rows), "lr recipes", len(lrs))
print("name+src", sum(1 for r in rows if r["byname"] and r["bysrc"]), "name-only", sum(1 for r in rows if r["byname"] and not r["bysrc"]), "src-only", sum(1 for r in rows if r["bysrc"] and not r["byname"]), "none", sum(1 for r in rows if not r["byname"] and not r["bysrc"]), "no-repo", sum(1 for r in rows if not r["repo"]))
for r in rows:
    tag = "name+src" if r["byname"] and r["bysrc"] else "name" if r["byname"] else "src" if r["bysrc"] else "none"
    same = [x for x, p in r["twinpins"].items() if p == r["pin"]]
    print(tag, r["core"], r["repo"], "byname=" + ",".join(r["byname"]), "bysrc=" + ",".join(r["bysrc"]), "samepin=" + ",".join(same))
