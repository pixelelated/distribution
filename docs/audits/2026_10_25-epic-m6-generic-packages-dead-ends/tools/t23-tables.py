#!/usr/bin/env python3
"""T23 (#670): the reachability table of the generic packages no image builds.

Reads only what stage A saved under .qa-scratch/t23/ (the inventory's rows at
2174265e9c, the five host plans from tools/viewplan, the per-device name
resolutions from config/functions' get_pkg_directory, the PKG_DEPENDS_UNPACK
lines at 8ebaf8daad) and asserts the brief's counts, so a missing row fails here
instead of printing an empty cell. It changes nothing in the tree.

    python3 -I t23-tables.py <worktree> stats        # the stage-A figures
    python3 -I t23-tables.py <worktree> reach        # 02 § Reachability rows (731)
    python3 -I t23-tables.py <worktree> coverage     # 02 § Coverage rows (1,604)
    python3 -I t23-tables.py <worktree> json         # the per-unit record
"""
import collections, json, os, re, sys
from pathlib import Path

W = Path(sys.argv[1]); S = W / '.qa-scratch/t23'; MODE = sys.argv[2]
DEVICES = ('GENERIC_X64', 'H700', 'SM8550')
CONFIGS = {'GENERIC_X64': ('GENERIC_X64-x86_64',), 'H700': ('H700-aarch64', 'H700-arm'),
           'SM8550': ('SM8550-aarch64', 'SM8550-arm')}
# Variables in PKG_DEPENDS_UNPACK the closure can expand: the device options set them.
VARS = {'H700': {'UBOOT_FIRMWARE': 'atf'}, 'GENERIC_X64': {'UBOOT_FIRMWARE': ''}, 'SM8550': {'UBOOT_FIRMWARE': ''}}

inv = json.load(open(S / 'inventory-rows.json')); rows = inv['rows']
byp = {r['path']: r for r in rows}
recipes = {r['path'][:-len('/package.mk')] for r in rows if r['path'].endswith('/package.mk')}
T = [r for r in rows if r['area'] == 'generic-packages' and r['reach'] in ('unreached', 'unshipped')]
assert len(T) == 1604, len(T)
assert sum(r['lines'] or 0 for r in T) == 95892
units = collections.defaultdict(list)
for r in T:
    p = os.path.dirname(r['path'])
    while p and p not in recipes: p = os.path.dirname(p)
    assert p, 'orphan ' + r['path']
    units[p].append(r)
tset = {r['path'] for r in T}
assert len(units) == 731 and sum(1 for u in units if u + '/package.mk' in tset) == 727

def plan(cfg):
    n = set()
    for l in open(S / f'plan-{cfg}.txt'):
        m = re.match(r'^\s*(build|install)\s+(\S+)', l)
        if m: n.add(m.group(2).split(':')[0])
    return n
host = {c: plan(c) for cs in CONFIGS.values() for c in cs}
# The container's plans, as the inventory recorded them (reachable_by on recipe rows, by directory name):
container = collections.defaultdict(set)
for r in rows:
    if r['path'].endswith('/package.mk'):
        for c in r['reachable_by'] or []:
            container[c].add(r['path'].split('/')[-2])
built = {d: set().union(*(host[c] | container[c] for c in CONFIGS[d])) for d in DEVICES}
host_built = {d: set().union(*(host[c] for c in CONFIGS[d])) for d in DEVICES}

res = collections.defaultdict(dict)
for f in ('resolve-units.txt', 'resolve-extra.txt'):
    for l in open(S / f):
        parts = l.split()
        res[parts[0]][parts[1]] = parts[2] if len(parts) > 2 else ''

def reached_dir(d, name):
    return res[d].get(name) if name in built[d] and res[d].get(name) else None

# Directories the plans build, per device (only names we resolved; every unit name and unpack name was).
built_dirs = {d: {res[d][n] for n in built[d] if res[d].get(n)} for d in DEVICES}

# The PKG_DEPENDS_UNPACK closure: a reached namer's unpack names are fetched and unpacked.
namers = collections.defaultdict(list)
for l in open(S / 'unpack-lines.txt'):
    path, ln, rest = l.split(':', 2)
    m = re.search(r'PKG_DEPENDS_UNPACK\+?="([^"]*)"', rest)
    if m: namers[os.path.dirname(path)].append((int(ln), m.group(1).split()))
unpacked = {d: collections.defaultdict(list) for d in DEVICES}   # target dir -> [(namer dir, line)]
for d in DEVICES:
    frontier = [n for n in namers if n in built_dirs[d]]
    seen = set(frontier)
    while frontier:
        n = frontier.pop()
        for ln, words in namers[n]:
            for w in words:
                w = re.sub(r'\$\{(\w+)\}', lambda m: VARS[d].get(m.group(1), '\0'), w)
                for x in w.split():
                    if '\0' in x or not x: continue
                    t = res[d].get(x)
                    if t:
                        if (n, ln) not in unpacked[d][t]: unpacked[d][t].append((n, ln))
                        if t in namers and t not in seen: seen.add(t); frontier.append(t)

def disposition(u):
    rs = units[u]; name = os.path.basename(u); rec = byp.get(u + '/package.mk', {})
    tier = 'fork-own' if any(r['tier'] == 'fork-own' for r in rs) else 'upstream-carried'
    reach = rec.get('reach') if u + '/package.mk' in tset else rs[0]['reach']
    sb = next((r['shadowed_by'] for r in rs if r.get('shadowed_by')), None)
    named = [d for d in DEVICES if name in built[d]]
    resolved = {d: res[d].get(name, '') for d in DEVICES}
    via = [(d, n, ln) for d in DEVICES for n, ln in unpacked[d].get(u, [])]
    self_built = [d for d in named if resolved[d] == u]
    other = sorted({resolved[d] for d in DEVICES if resolved[d] and resolved[d] != u})
    if self_built or via:
        disp = 'reached after all'
    elif other:
        o = other[0]; o_live = any(o in built_dirs[d] or o in unpacked[d] for d in DEVICES)
        o_row = byp.get(o + '/package.mk', {}).get('reach', '?')
        disp = 'shadowed copy, override live' if o_live or o_row in ('shipped', 'test') else 'shadowed copy, override dead too'
    elif tier == 'fork-own':
        disp = 'fork-own, dead'
    elif reach == 'unshipped':
        disp = 'unshipped'
    else:
        disp = 'dead, upstream-carried'
    return dict(unit=u, files=len(rs), lines=sum(r['lines'] or 0 for r in rs), tier=tier, reach=reach,
                recipe_in_set=u + '/package.mk' in tset, shadowed_by=sb, named=named,
                host_named=[d for d in DEVICES if name in host_built[d]], resolved=resolved, other=other,
                via=via, disposition=disp)

U = {u: disposition(u) for u in sorted(units)}

if MODE == 'stats':
    c = collections.Counter(x['disposition'] for x in U.values())
    print('units', len(U), 'recipe in set', sum(x['recipe_in_set'] for x in U.values()))
    print('dispositions', dict(c), 'sum', sum(c.values()))
    pn = [x for x in U.values() if x['recipe_in_set'] and x['named']]
    print('recipes whose name some plan builds', len(pn), '; of them shadowed (resolved elsewhere)',
          sum(1 for x in pn if x['other'] and x['disposition'] != 'reached after all'),
          '; resolved to themselves', sum(1 for x in pn if x['disposition'] == 'reached after all'))
    pn_host = [x for x in U.values() if x['recipe_in_set'] and x['host_named']]
    print('  by the host plans alone', len(pn_host))
    shn = [x for x in U.values() if x['shadowed_by'] and not x['named']]
    print('shadowed_by units with no plan naming the name', len(shn), [os.path.basename(x['unit']) for x in shn])
    shn_h = [x for x in U.values() if x['shadowed_by'] and not x['host_named']]
    print('  by the host plans alone', len(shn_h), [os.path.basename(x['unit']) for x in shn_h])
    print('shadowed_by units', sum(1 for x in U.values() if x['shadowed_by']), 'rows', sum(1 for r in T if r.get('shadowed_by')))
    pairs = collections.defaultdict(list)
    for u in U: pairs[os.path.basename(u)].append(u)
    print('basename pairs in the set', sum(1 for v in pairs.values() if len(v) > 1))
    for n, v in sorted(pairs.items()):
        if len(v) > 1: print('  ', n, '->', ', '.join(f"{os.path.relpath(u)} [{U[u]['disposition']}]" for u in v), '; resolves to', U[v[0]]['resolved']['GENERIC_X64'] or '-')
    print('reached after all:')
    for x in U.values():
        if x['disposition'] == 'reached after all':
            print('  ', x['unit'], 'reach', x['reach'], 'named', x['named'], 'via', sorted({f'{n}:{ln}' for d, n, ln in x['via']}), 'on', sorted({d for d, n, ln in x['via']}))
    named_any = set()
    for n, lst in namers.items():
        for ln, words in lst:
            for w in words:
                if '$' in w: continue
                for d in DEVICES:
                    t = res[d].get(w)
                    if t in units: named_any.add(t)
    print('units in the set named by some PKG_DEPENDS_UNPACK (any namer, by name, any device)', len(named_any))
    print('fork-own:', [(x['unit'], x['disposition']) for x in U.values() if x['tier'] == 'fork-own'])
elif MODE == 'json':
    print(json.dumps(U, indent=1))
elif MODE == 'reach':
    for x in U.values():
        res_s = '; '.join(f"{d} `{x['resolved'][d]}`" if x['resolved'][d] else f'{d} --' for d in DEVICES)
        via = '; '.join(f"{d}: `{n}:{ln}`" for d, n, ln in x['via']) or '--'
        print(f"| `{x['unit']}` | {x['files']} | {x['lines']} | {x['tier']} | {x['reach']} | "
              f"{('`' + x['shadowed_by'] + '`') if x['shadowed_by'] else '--'} | {', '.join(x['named']) or '--'} | "
              f"{res_s} | {via} | **{x['disposition']}** |")
elif MODE == 'coverage':
    owner = {r['path']: u for u, rs in units.items() for r in rs}
    for r in sorted(T, key=lambda r: r['path']):
        x = U[owner[r['path']]]
        print(f"| `{r['path']}` | {r['lines']} | {r['tier']} | {r['reach']} | `{x['unit']}` | {x['disposition']} |")
