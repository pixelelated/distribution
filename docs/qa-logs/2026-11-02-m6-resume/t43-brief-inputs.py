#!/usr/bin/env python3
"""T43 brief input verification: immutable Git reads only; no config/generator runs."""
import argparse, ast, csv, hashlib, io, json, posixpath, re, subprocess
from collections import Counter, defaultdict
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', default='.')
parser.add_argument('--ref', required=True)
parser.add_argument('--out', required=True)
args=parser.parse_args()
P1='2174265e9cc1b248c0fbe27fa101875984d46d6b'
def git(*argv):
    return subprocess.check_output(['git','-C',args.repo,*argv])
def show(ref,path):
    return git('show',f'{ref}:{path}')
source = show(P1, 'tools/renovation-inventory').decode()
names = {'glob_re', 'glob_body', 'load_areas', 'assign', 'slice_of'}
functions = [node for node in ast.parse(source).body
             if isinstance(node, ast.FunctionDef) and node.name in names]
assert {node.name for node in functions} == names
ns = {'re': re, 'defaultdict': defaultdict, 'CannotRun': RuntimeError}
exec(compile(ast.Module(body=functions, type_ignores=[]), '<P1 pure selectors>', 'exec'), ns)

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


ref=git('rev-parse','--verify',args.ref+'^{commit}').decode().strip()
selector_files=['docs/reviews/inventory.json','docs/reviews/inventory.md','docs/reviews/areas.json','docs/reviews/slices.json','docs/reviews/order.md','tools/renovation-inventory']
selector_hashes={}
for path in selector_files:
    original=show(P1,path); current_bytes=show(ref,path)
    assert original==current_bytes, 'selector/input bytes drift: '+path
    selector_hashes[path]=hashlib.sha256(current_bytes).hexdigest()
_,_,_,owned,_=membership(P1)
_,_,_,current,_=membership(ref)
rows=sorted(owned['patches-unshipped'],key=lambda r:r['path'])
assert rows==sorted(current['patches-unshipped'],key=lambda r:r['path']), 'membership drift'
paths=[r['path'] for r in rows]
path_bytes=('\n'.join(paths)+'\n').encode()
assert len(rows)==432 and sum(r['lines'] for r in rows)==328516
assert hashlib.sha256(path_bytes).hexdigest()=='8ec78172f80d28d28117eaf1efefe2c769ea58d07a57c3a16616b595fb429912'
def tree(rev):
    result={}
    for entry in git('ls-tree','-r','-z',rev,'--',*paths).split(b'\0'):
        if not entry:continue
        meta,path=entry.split(b'\t',1)
        mode,kind,oid=meta.decode().split()
        result[path.decode()]={'mode':mode,'type':kind,'oid':oid}
    return result
base_tree=tree(P1); tip_tree=tree(ref)
assert base_tree==tip_tree, 'source mode/blob drift'
logical=newlines=byte_count=0
links=[]
for row in rows:
    path=row['path']; data=show(ref,path)
    lf=data.count(b'\n'); count=lf+int(bool(data) and not data.endswith(b'\n'))
    assert count==row['lines'],path
    logical+=count;newlines+=lf;byte_count+=len(data)
    if tip_tree[path]['mode']=='120000':
        target=data.decode(); resolved=posixpath.normpath(posixpath.join(posixpath.dirname(path),target))
        assert not resolved.startswith('../') and not resolved.startswith('/'), 'unsafe symlink'
        referent=show(ref,resolved)
        assert referent==show(P1,resolved), 'referent bytes drift: '+resolved
        assert git('ls-tree',ref,'--',resolved)==git('ls-tree',P1,'--',resolved), 'referent mode/blob drift: '+resolved
        links.append({'path':path,'target':target,'resolved':resolved,'sha256':hashlib.sha256(referent).hexdigest()})
assert (logical,newlines,byte_count)==(328516,328512,10690267)
assert Counter(v['mode'] for v in tip_tree.values())=={'100644':428,'100755':2,'120000':2}
fork=[r for r in rows if r['tier_note']=='fork-written']
assert len(fork)==0
for sid in ['patches-shipped-kernel','patches-shipped','patches-dead']:
    assert not set(paths)&{r['path'] for r in current[sid]}, sid
recipe_packet='docs/qa-logs/2026-11-02-m6-resume/t43-preparation/recipes.json'
recipe_rows=json.loads(show('afdec2bf8b88135befcb7ec56efb3a7ea327bd73',recipe_packet))
assert len(recipe_rows)==31
recipe_hashes={}
for path,row in recipe_rows.items():
    data=show(ref,path)
    assert data==show(P1,path), 'context recipe drift: '+path
    assert hashlib.sha256(data).hexdigest()==row['sha256_P1'], path
    assert git('ls-tree',ref,'--',path)==git('ls-tree',P1,'--',path), path
    recipe_hashes[path]=hashlib.sha256(data).hexdigest()
out=Path(args.out)
assert not out.exists() or not any(out.iterdir()), 'output must be absent or empty'
out.mkdir(parents=True,exist_ok=True)
(out/'paths.txt').write_bytes(path_bytes)
(out/'rows.json').write_text(json.dumps(rows,indent=2)+'\n')
(out/'tree.json').write_text(json.dumps(tip_tree,sort_keys=True,indent=2)+'\n')
(out/'symlinks.json').write_text(json.dumps(links,indent=2)+'\n')
summary={'ref':ref,'p1':P1,'paths':432,'logical_lines':logical,'newlines':newlines,'bytes':byte_count,'regular':430,'fork_written_paths':0,'fork_written_lines':0,'reach':dict(Counter(r['reach'] for r in rows)),'path_list_sha256':hashlib.sha256(path_bytes).hexdigest(),'selector_sha256':selector_hashes,'recipe_sha256':recipe_hashes,'symlinks':links,'symlink_count':2}
(out/'summary.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
print(json.dumps(summary,sort_keys=True))
