#!/usr/bin/env python3
"""Static recipe/selector excerpts and owner mapping; nothing is sourced."""
import ast, collections, hashlib, json, posixpath, re, subprocess
from pathlib import Path
REPO='/workspace/repos/pixelelated/distribution.worktrees/m6-p1-survey-641'
P1='2174265e9cc1b248c0fbe27fa101875984d46d6b'
COORD='7f25f9f78b3da3a6b2c893397b58a3ce5a04be75'
OUT=Path(__file__).resolve().parent
defs=[n for n in ast.parse((OUT/'reproduce.py').read_text()).body if isinstance(n,ast.FunctionDef)]
exec(compile(ast.Module(body=defs,type_ignores=[]),'<read-only helper definitions>','exec'))
inv,rows,owned,owner,_=selection(P1)
_,crows,_,cowner,_=selection(COORD)
by_path={r['path']:r for r in rows if r['tree']=='distribution'}
cby_path={r['path']:r for r in crows if r['tree']=='distribution'}
pkgdirs={p[:-11] for p in by_path if p.endswith('/package.mk')}
sel=owned['patches-unshipped']
groups=collections.defaultdict(list)
for r in sel:
    p=r['path']; parents=posixpath.dirname(p).split('/')
    candidates=['/'.join(parents[:i]) for i in range(len(parents),0,-1)]
    root=next((x for x in candidates if x in pkgdirs),None)
    if root is None:
        if '/linux/' in p and p.endswith('.conf'): root='projects/ROCKNIX/packages/linux'
        else:
            name=p.split('/patches/',1)[1].split('/')[0]
            candidates=[x for x in pkgdirs if x.startswith('projects/ROCKNIX/packages/') and x.endswith('/'+name)]
            assert len(candidates)==1,(p,candidates)
            root=candidates[0]
    groups[root+'/package.mk'].append(r)
out={}
for p,rs in sorted(groups.items()):
    b1=show(P1,p); b2=show(COORD,p)
    excerpt=[]
    text=b2.decode().splitlines()
    for i,l in enumerate(text,1):
        if re.search(r'^\s*(?:PKG_(?:NAME|VERSION|SHA256|PATCH_DIRS|SOURCE_NAME|GIT_CLONE_BRANCH)\+?=|case |.*\)\s*$|if |elif |else|fi\b|esac\b|\. .*package\.mk|source .*package\.mk)|PKG_PATCH_DIRS|PKG_DEPENDS_UNPACK',l):
            excerpt.append([i,l])
    out[p]={**stats(rs),'owner_P1':owner(by_path[p]),'owner_coordinator':cowner(cby_path[p]),
        'modes_blobs':{v:tree(v,[p])[p] for v in (P1,COORD)},
        'sha256_P1':sha(b1),'sha256_coordinator':sha(b2),'identical':b1==b2,
        'version_lines':[[i,l] for i,l in enumerate(text,1) if re.match(r'\s*PKG_VERSION\+?=',l)],
        'static_selector_excerpt':excerpt,
        'member_directories':sorted({posixpath.dirname(r['path']) for r in rs})}
(OUT/'recipes.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
for p,r in out.items():
    print(json.dumps({'recipe':p,'members':r['paths'],'lines':r['inventory_lines'],
        'owner':r['owner_coordinator'],'same_at_both_refs':r['identical'],'pins':r['version_lines']}))
print('RECIPE_COUNT',len(out))
