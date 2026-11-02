#!/usr/bin/env python3
"""Bounded #689 membership research; only immutable Git reads, stdout output.

Uses only the five pure selector functions from the pinned P1 tool, never its
generator, config sourcing, CLI entrypoint, or filesystem-reading loader.
"""
import ast
import hashlib
import json
import posixpath
import re
import subprocess
from collections import Counter, defaultdict

P1 = '2174265e9c'
COORD = '2c6885a54f'

def git(*args):
    return subprocess.check_output(['git', *args])

def show(rev, path):
    return git('show', f'{rev}:{path}')

def emit(label, value):
    print(label, json.dumps(value, sort_keys=True))

source = show(P1, 'tools/renovation-inventory').decode()
names = {'glob_re', 'glob_body', 'load_areas', 'assign', 'slice_of'}
functions = [node for node in ast.parse(source).body
             if isinstance(node, ast.FunctionDef) and node.name in names]
assert {node.name for node in functions} == names
ns = {'re': re, 'defaultdict': defaultdict, 'CannotRun': RuntimeError}
exec(compile(ast.Module(body=functions, type_ignores=[]), '<P1 pure selectors>', 'exec'), ns)
emit('SELECTOR_FUNCTIONS', {n.name: [n.lineno, n.end_lineno] for n in functions})
emit('PINS', {r: git('rev-parse', r).decode().strip() for r in [P1, COORD]})

def membership(rev):
    inv = json.loads(show(rev, 'docs/reviews/inventory.json'))
    doc = json.loads(show(rev, 'docs/reviews/slices.json'))
    compiled = []
    for sl in doc['slices']:
        assert 'gate' not in sl
        sels = sl.get('select', {})
        selectors = []
        for sel in sels if isinstance(sels, list) else [sels]:
            globs = sel.get('globs')
            selectors.append((set(sel.get('areas', [sl['area']])),
                ns['load_areas']([{'area': sl['id'], 'globs': globs}])[0] if globs else None,
                set(sel['reach']) if sel.get('reach') else None,
                bool(sel.get('rest')),
                set(sel['tier']) if sel.get('tier') else None))
        compiled.append((sl, selectors))
    rows = [dict(zip(inv['columns'], r)) for r in inv['rows']]
    area = [r for r in rows if r['area'] == 'patches-and-configs']
    owned = defaultdict(list)
    for row in area:
        hits = ns['slice_of'](row, compiled)
        assert len(hits) == 1, (row['path'], hits)
        owned[hits[0]].append(row)
    return inv, doc, rows, owned, compiled

inv, doc, rows, owned, compiled = membership(P1)
c_inv, c_doc, c_rows, c_owned, c_compiled = membership(COORD)
emit('INVENTORY_HEADER', {k:v for k,v in inv['header'].items() if k not in ['configs','escaped_rows']})
for path in ['docs/reviews/inventory.json', 'docs/reviews/inventory.md',
             'docs/reviews/areas.json', 'docs/reviews/slices.json', 'docs/reviews/order.md']:
    emit('LEDGER_IDENTITY', {'path': path, 'equal': show(P1,path)==show(COORD,path),
         'sha256': hashlib.sha256(show(P1,path)).hexdigest()})
emit('PATCH_AREA_OWNERS', {k: {'paths':len(v), 'lines':sum(r['lines'] or 0 for r in v),
      'reach':dict(Counter(r['reach'] for r in v))} for k,v in owned.items()})
selected = sorted(owned['patches-shipped'], key=lambda r:r['path'])
assert selected == sorted(c_owned['patches-shipped'], key=lambda r:r['path'])
paths = [r['path'] for r in selected]
emit('MEMBERSHIP', {'paths':len(paths), 'lines':sum(r['lines'] or 0 for r in selected),
     'path_list_sha256':hashlib.sha256(('\n'.join(paths)+'\n').encode()).hexdigest(),
     'coordinator_equal': True})
for field in ['tree','tier','tier_note','language','reach','shadowed_by','overlap']:
    emit('KINDS_'+field, dict(Counter(str(r[field]) for r in selected)))
emit('EXTENSIONS', dict(Counter(r['path'].rsplit('.',1)[-1] for r in selected)))
for configs in sorted({tuple(r['reachable_by']) for r in selected}):
    sub = [r for r in selected if tuple(r['reachable_by']) == configs]
    emit('REACH_GROUP', {'configs':configs,'paths':len(sub),'lines':sum(r['lines'] or 0 for r in sub)})

groups = defaultdict(list)
for row in selected:
    path = row['path']
    if '/patches/' in path:
        prefix, suffix = path.split('/patches/',1)
        group = prefix if prefix != 'projects/ROCKNIX' else prefix+'/patches/'+suffix.split('/')[0]
    else:
        group = path.rsplit('/',1)[0]
    groups[group].append(row)
emit('GROUP_COUNT',len(groups))
emit('DIRECT_PATCH_DIRECTORY_COUNT',len({r['path'].rsplit('/',1)[0] for r in selected}))
root_groups = defaultdict(list)
for row in selected:
    root = 'packages/' if row['path'].startswith('packages/') else 'projects/ROCKNIX/packages/' if row['path'].startswith('projects/ROCKNIX/packages/') else 'projects/ROCKNIX/patches/'
    root_groups[root].append(row)
for root, sub in sorted(root_groups.items()):
    emit('ROOT_GROUP',{'root':root,'paths':len(sub),'lines':sum(r['lines'] or 0 for r in sub)})
for group, sub in sorted(groups.items()):
    emit('PACKAGE_GROUP', {'group':group,'paths':len(sub),'lines':sum(r['lines'] or 0 for r in sub),
         'fork_written':sum(r['tier_note']=='fork-written' for r in sub)})

fork = [r for r in selected if r['tier_note']=='fork-written']
emit('FORK_WRITTEN_TOTAL',{'paths':len(fork),'lines':sum(r['lines'] or 0 for r in fork)})
for row in fork:
    emit('FORK_WRITTEN_ROW',{k:row[k] for k in ['path','lines','reach','reachable_by','last_fork_commit']})

identity = {}
for rev in [P1,COORD]:
    found = {}
    for entry in git('ls-tree','-r','-z',rev,'--',*paths).split(b'\0'):
        if not entry: continue
        metadata, path = entry.split(b'\t',1)
        mode,kind,oid = metadata.decode().split()
        found[path.decode()] = {'mode':mode,'kind':kind,'oid':oid}
    identity[rev] = found
    emit('EXISTENCE', {'rev':rev, 'present':len(found), 'missing':sorted(set(paths)-set(found)),
         'modes':dict(Counter(v['mode'] for v in found.values()))})
changed = [p for p in paths if identity[P1].get(p)!=identity[COORD].get(p)]
emit('CHANGED_SELECTED_PATHS',changed)
by_path = {r['path']:r for r in rows if r['tree']=='distribution'}
for path in paths:
    if identity[P1][path]['mode']=='120000':
        target = show(P1,path).decode()
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path),target))
        target_row = by_path.get(resolved)
        emit('SYMLINK',{'path':path,'target':target,'resolved':resolved,
             'target_slice':ns['slice_of'](target_row,compiled) if target_row else None,
             'target_inventory_lines':target_row['lines'] if target_row else None,
             'coordinator_target_equal':show(P1,resolved)==show(COORD,resolved)})
base = inv['header']['distribution']['merge_base']
for rev in [P1,COORD]:
    fork_delta = git('diff','--name-only','-z','--no-renames',base,rev,'--',*paths).decode().strip('\0').split('\0')
    emit('FORK_BASE_DELTA',{'base':base,'rev':rev,'paths':len(fork_delta),
         'equal_tier_note':sorted(fork_delta)==sorted(r['path'] for r in fork)})
for rev in [P1,COORD]:
    logical = newline = byte_count = 0
    mismatches = []
    for row in selected:
        path = row['path']
        if path not in identity[rev]: continue
        data = show(rev,path)
        lf = data.count(b'\n')
        count = lf + int(bool(data) and not data.endswith(b'\n'))
        if rev == P1 and data and not data.endswith(b'\n'):
            emit('UNTERMINATED',{'path':path,'lines':count,'mode':identity[P1][path]['mode']})
        logical += count
        newline += lf
        byte_count += len(data)
        if count != row['lines']:
            mismatches.append({'path':path,'inventory':row['lines'],'actual':count})
    emit('ACTUAL_CONTENT_TOTAL', {'rev':rev,'logical_lines':logical,'newline_count':newline,
         'bytes':byte_count,'inventory_mismatches':mismatches})

for row in selected:
    if row['reach']=='test': emit('TEST_ONLY_ROW',{k:row[k] for k in ['path','lines','reachable_by']})
for sid in ['patches-shipped-kernel','patches-unshipped']:
    emit('DISJOINT',{'slice':sid, 'intersection':sorted(set(paths)&{r['path'] for r in owned[sid]})})
    if sid == 'patches-shipped-kernel':
        for row in owned[sid]:
            if '/linux/' not in row['path'] and '/linux/patches/' not in row['path']:
                emit('T41_NON_LINUX_PATH',{k:row[k] for k in ['path','lines','reach']})

for row in rows:
    if row['path'] in ['projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf',
                       'projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf',
                       'projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk']:
        emit('NEIGHBOR_ROW',dict({k:row[k] for k in ['path','area','tier','lines','reach']},
             slice=ns['slice_of'](row,compiled)))
emit('PATCH_AREA_TOTAL',{'paths':sum(len(v) for v in owned.values()),
     'lines':sum(r['lines'] or 0 for v in owned.values() for r in v)})
for sid in ['emulators-libretro','offline-achievements']:
    dirs=Counter(r['path'].split('/patches/')[0] for r in owned[sid])
    emit('OTHER_PATCH_OWNER',{'slice':sid,'directories':dict(dirs)})
