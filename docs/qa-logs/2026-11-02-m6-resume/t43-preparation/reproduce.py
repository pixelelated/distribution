#!/usr/bin/env python3
"""Bounded T43 immutable reads; private membership metadata only, no source export.

Execute only the five inspected pure selector functions, not the inventory
entrypoint, generator, filesystem loader, build planner or shell config.
"""
import ast, collections, hashlib, json, posixpath, re, subprocess
from pathlib import Path

REPO='/workspace/repos/pixelelated/distribution.worktrees/m6-p1-survey-641'
P1='2174265e9cc1b248c0fbe27fa101875984d46d6b'
COORD='7f25f9f78b3da3a6b2c893397b58a3ce5a04be75'
OUT=Path(__file__).resolve().parent
def git(*args): return subprocess.check_output(['git','-C',REPO,*args])
def show(ref,path): return git('show',f'{ref}:{path}')
def sha(b): return hashlib.sha256(b).hexdigest()
def lines(b): return b.count(b'\n')+int(bool(b) and not b.endswith(b'\n'))
def tree(ref,paths):
    d={}
    for entry in git('ls-tree','-r','-z',ref,'--',*paths).split(b'\0'):
        if entry:
            meta,path=entry.split(b'\t',1)
            mode,kind,oid=meta.decode().split()
            d[path.decode()]={'mode':mode,'kind':kind,'oid':oid}
    return d
def selection(ref):
    source=show(ref,'tools/renovation-inventory').decode()
    names={'glob_re','glob_body','load_areas','assign','slice_of'}
    funcs=[n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in funcs}==names
    ns={'re':re,'defaultdict':collections.defaultdict,'CannotRun':RuntimeError}
    exec(compile(ast.Module(body=funcs,type_ignores=[]),'<pinned pure selectors>','exec'),ns)
    inv=json.loads(show(ref,'docs/reviews/inventory.json'))
    spec=json.loads(show(ref,'docs/reviews/slices.json'))
    compiled=[]
    for sl in spec['slices']:
        sels=sl.get('select',{}); sels=sels if isinstance(sels,list) else [sels]
        cs=[]
        for sel in sels:
            globs=sel.get('globs')
            cs.append((set(sel.get('areas',[sl['area']])),
                ns['load_areas']([{'area':sl['id'],'globs':globs}])[0] if globs else None,
                set(sel['reach']) if sel.get('reach') else None,bool(sel.get('rest')),
                set(sel['tier']) if sel.get('tier') else None))
        compiled.append((sl,cs))
    rows=[dict(zip(inv['columns'],r)) for r in inv['rows']]
    owned=collections.defaultdict(list)
    for r in rows:
        if r['area']=='patches-and-configs':
            hits=ns['slice_of'](r,compiled)
            assert len(hits)==1,(r['path'],hits)
            owned[hits[0]].append(r)
    return inv,rows,owned,lambda r: ns['slice_of'](r,compiled),{
        n.name:{'lines':[n.lineno,n.end_lineno],'ast_sha256':sha(ast.dump(n).encode())} for n in funcs}

def stats(rows):
    return {'paths':len(rows),'inventory_lines':sum(r['lines'] or 0 for r in rows)}
def grouped(rows,key):
    out=collections.defaultdict(list)
    for r in rows: out[key(r)].append(r)
    return {k:stats(v) for k,v in sorted(out.items())}
def scope_group(r):
    p=r['path']
    if p.startswith('projects/ROCKNIX/devices/'):
        return '/'.join(p.split('/')[:4])
    if '/patches/' in p:
        before,after=p.split('/patches/',1)
        return before+'/'+after.split('/')[0] if before=='projects/ROCKNIX' else before
    return p.rsplit('/',1)[0]

all_data={ref:selection(ref) for ref in (P1,COORD)}
result={'refs':{'P1':P1,'coordinator':COORD},'inputs':{},'selector_functions':{},'populations':{}}
for ref,(inv,rows,owned,owner,funcs) in all_data.items():
    result['selector_functions'][ref]=funcs
    result['inputs'][ref]={p:{'sha256':sha(show(ref,p)),**tree(ref,[p])[p]} for p in [
        'tools/renovation-inventory','docs/reviews/inventory.json','docs/reviews/slices.json',
        'docs/reviews/areas.json','docs/reviews/order.md']}
    result['populations'][ref]={sid:stats(rs) for sid,rs in sorted(owned.items())}

inv,rows,owned,owner,_=all_data[P1]
selected=sorted(owned['patches-unshipped'],key=lambda r:r['path'])
cselected=sorted(all_data[COORD][2]['patches-unshipped'],key=lambda r:r['path'])
paths=[r['path'] for r in selected]
by_path={r['path']:r for r in rows if r['tree']=='distribution'}
ident={ref:tree(ref,paths) for ref in (P1,COORD)}
result['membership']={**stats(selected),'coordinator_rows_identical':selected==cselected,
    'path_list_sha256':sha(('\n'.join(paths)+'\n').encode()),
    'missing':{ref:sorted(set(paths)-set(ident[ref])) for ref in (P1,COORD)},
    'changed_modes_or_blobs':[p for p in paths if ident[P1].get(p)!=ident[COORD].get(p)]}
result['inventory_header']={k:v for k,v in inv['header'].items() if k not in ('configs','escaped_rows')}
result['columns']={k:dict(collections.Counter(str(r[k]) for r in selected)) for k in
    ['tree','tier','tier_note','language','reach','shadowed_by','overlap']}
result['modes']={ref:dict(collections.Counter(x['mode'] for x in ident[ref].values())) for ref in ident}
result['path_kinds']=dict(collections.Counter('patch' if r['path'].endswith('.patch') else
    'kernel-config' if '/linux/' in r['path'] and r['path'].endswith('.conf') else 'other' for r in selected))
result['directory_groups']=grouped(selected,lambda r:posixpath.dirname(r['path']))
result['scope_groups']=grouped(selected,scope_group)
result['buildable_combinations']=grouped(selected,lambda r:','.join(r['buildable_by']))
result['per_target_nonadditive']={cfg:stats([r for r in selected if cfg in r['buildable_by']])
    for cfg in sorted({c for r in selected for c in r['buildable_by']})}
fork=[r for r in selected if r['tier_note']=='fork-written']
result['fork_written']={'total':stats(fork),'rows':fork}
result['actual_content']={}; result['symlinks']=[]; result['configs']=[]
manifest=[]
for ref in (P1,COORD):
    total=collections.Counter(); mismatch=[]; unterminated=[]
    for r in selected:
        p=r['path']; data=show(ref,p); n=lines(data)
        total.update({'logical_lines':n,'newlines':data.count(b'\n'),'bytes':len(data)})
        if n!=r['lines']: mismatch.append({'path':p,'inventory':r['lines'],'actual':n})
        if data and not data.endswith(b'\n'): unterminated.append(p)
        if ref==P1:
            m=ident[ref][p]
            manifest.append('\t'.join([p,m['mode'],m['oid'],str(r['lines']),str(n),str(len(data)),
                 r['tier_note'] or '-',r['reach'],','.join(r['buildable_by'])]))
            if m['mode']=='120000':
                target=data.decode(); resolved=posixpath.normpath(posixpath.join(posixpath.dirname(p),target))
                tr=by_path.get(resolved)
                result['symlinks'].append({'path':p,'target':target,'resolved':resolved,
                    'target_owner':owner(tr) if tr else None,'target_row':tr,
                    'target_modes_blobs':{v:tree(v,[resolved]).get(resolved) for v in (P1,COORD)}})
            if not p.endswith('.patch'):
                result['configs'].append({'path':p,'header':[l for l in data.decode().splitlines()[:8]],
                    'lines':n,'buildable_by':r['buildable_by']})
    result['actual_content'][ref]={**total,'inventory_mismatches':mismatch,'unterminated':unterminated}
    base=inv['header']['distribution']['merge_base']
    delta=git('diff','--name-only','-z','--no-renames',base,ref,'--',*paths).decode().strip('\0')
    delta=delta.split('\0') if delta else []
    result.setdefault('fork_base_delta',{})[ref]={'base':base,'paths':delta,
        'matches_tier_note':sorted(delta)==sorted(r['path'] for r in fork)}
result['neighbor_intersections']={s:sorted(set(paths)&{r['path'] for r in owned[s]})
    for s in ['patches-shipped','patches-shipped-kernel','patches-dead']}
inbound=[]
for sid,rs in owned.items():
    if sid=='patches-unshipped': continue
    for r in rs:
        p=r['path']; mt=tree(P1,[p]).get(p)
        if mt and mt['mode']=='120000':
            target=show(P1,p).decode(); resolved=posixpath.normpath(posixpath.join(posixpath.dirname(p),target))
            if resolved in paths:
                inbound.append({'path':p,'slice':sid,'target':target,'resolved':resolved,
                    'link_modes_blobs':{v:tree(v,[p]).get(p) for v in (P1,COORD)}})
result['cross_slice_inbound_symlinks']=inbound
data=('path\tmode\tblob_at_both_refs\tinventory_lines\tlogical_lines\tbytes\ttier_note\treach\tbuildable_by\n'+'\n'.join(manifest)+'\n').encode()
if result['membership']['changed_modes_or_blobs']:
    raise RuntimeError('Use separate manifests: source identity drift found')
(OUT/'members.tsv').write_bytes(data)
result['membership']['manifest_sha256']=sha(data)
(OUT/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:result[k] for k in ['membership','modes','path_kinds','columns','scope_groups',
    'fork_written','actual_content','configs','symlinks','cross_slice_inbound_symlinks']},indent=2))
