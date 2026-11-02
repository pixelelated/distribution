#!/usr/bin/env python3
"""Extract immutable source headers/targets and identities, not a body review."""
import collections,hashlib,json,pathlib,re,subprocess,datetime
R=pathlib.Path(__file__).resolve().parents[1];bindings=json.loads((R/'stage-a/bindings.json').read_text());SRC=bindings['source'];UP=bindings['upstream'];BASE=bindings['fork_base']
def git(*a):return subprocess.check_output(['git',*a])
def tree(ref):
 out={}
 for e in git('ls-tree','-r','-z',ref).split(b'\0'):
  if e:
   meta,p=e.split(b'\t',1);mode,typ,oid=meta.decode().split();out[p.decode()]={'mode':mode,'type':typ,'oid':oid}
 return out
src=tree(SRC);up=tree(UP);base=tree(BASE);byoid=collections.defaultdict(list)
for p,m in up.items():byoid[m['oid']].append(p)
recipes=json.loads(git('show',SRC+':docs/qa-logs/2026-11-02-m6-resume/t43-preparation/recipes.json'));rows=json.loads((R/'stage-a/source/rows.json').read_text());out=[]
for row in rows:
 p=row['path'];raw=git('show',SRC+':'+p);lines=raw.decode(errors='replace').splitlines();kind='config' if p.endswith('.conf') else ('symlink' if src[p]['mode']=='120000' else 'patch');header=[];targets=[]
 if kind=='patch':
  stop=next((i for i,x in enumerate(lines) if x.startswith(('diff ','--- ','Index:'))),min(len(lines),80))
  header=[[i+1,x] for i,x in enumerate(lines[:min(stop,80)])]
  targets=[[i+1,x] for i,x in enumerate(lines) if x.startswith(('+++ ','--- ','diff --git ','Index:'))]
 elif kind=='config':header=[[i+1,x] for i,x in enumerate(lines[:12])]
 else:header=[[1,raw.decode()]]
 candidates=[rp for rp,v in recipes.items() if str(pathlib.PurePosixPath(p).parent) in v['member_directories']]
 if not candidates and (kind=='config' or '/patches/linux/' in p):candidates=['projects/ROCKNIX/packages/linux/package.mk']
 assert len(candidates)==1,(p,candidates)
 same=up.get(p);matches=[q for q in byoid[src[p]['oid']] if q!=p]
 status='identical-at-path' if same==src[p] else ('changed-at-path' if same else ('identical-blob-other-path' if matches else 'absent-at-path-no-identical-blob'))
 out.append({**row,**src[p],'kind':kind,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'header':header,'targets':targets,'source_recipe':candidates[0],'recipe_owner':recipes[candidates[0]]['owner_P1'],'base_identical':base.get(p)==src[p],'upstream':{'status':status,'same_path_tree':same,'same_blob_other_paths':matches},'inspection':'mechanically extracted header and target lines; source identity and recipe-directory association; vendor bodies not read line by line'})
(R/'stage-b').mkdir(exist_ok=True);(R/'stage-b/observations.json').write_text(json.dumps(out,indent=2)+'\n')
counts={'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':len(out),'kind':dict(collections.Counter(x['kind'] for x in out)),'upstream':dict(collections.Counter(x['upstream']['status'] for x in out)),'base_identical':sum(x['base_identical'] for x in out),'mail_from':sum(any(t.startswith('From: ') for n,t in x['header']) for x in out),'subject':sum(any(t.startswith('Subject: ') for n,t in x['header']) for x in out),'no_header':sum(not x['header'] for x in out),'recipes':len(set(x['source_recipe'] for x in out))}
(R/'stage-b/first-observations.json').write_text(json.dumps(counts,indent=2)+'\n')
with (R/'01-research-notes.md').open('a') as f:f.write('\n## '+counts['observed_at']+' — Own first observations, before prior verdicts\n\n'+json.dumps(counts,sort_keys=True)+'\n\nNative membership and header/target extraction are recorded in stage-b/observations.json. All 432 source mode/blob entries match the fork base. This proves selected net identity only, not authorship. Mail header absence is a provenance qualification, not automatically a defect. Upstream same-blob matching records candidate moves without asserting semantic supersession. Configuration headers and symlink literals are distinct from patch bodies. Prior verdicts have not yet been opened.\n')
print(json.dumps(counts,indent=2))
