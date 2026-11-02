"""Independent T44 immutable membership reader. No inventory producer execution.
Reads pinned Git objects; writes only small path/identity/count manifests here.
"""
import collections,functools,hashlib,json,pathlib,re,subprocess
D='/workspace/repos/pixelelated/distribution.worktrees/m6-p1-survey-641'
E='/home/max/Development/emulationstation-next'
P='2174265e9cc1b248c0fbe27fa101875984d46d6b';C='92e8d07b6163ec5ddd3e9b67f1c42a472b2911d1';S='16dbac5211eea7e70db7394372033be2be7df829'
EMPTY='4b825dc642cb6eb9a060e54bf8d69288fbee4904'
O=pathlib.Path(__file__).parent
def git(repo,*args):return subprocess.check_output(['git','-C',repo,*args])
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(repo,ref,path):return git(repo,'show',ref+':'+path)
def save(name,x):
 b=(json.dumps(x,sort_keys=True,indent=2)+'\n').encode();(O/name).write_bytes(b);return sha(b)
inputs=['docs/reviews/areas.json','docs/reviews/slices.json','docs/reviews/inventory.json','docs/reviews/inventory.md','docs/reviews/order.md','tools/renovation-inventory']
input_hashes={}
for p in inputs:
 a=blob(D,P,p);b=blob(D,C,p);input_hashes[p]={'P1_sha256':sha(a),'coordinator_sha256':sha(b),'equal':a==b}
inv=json.loads(blob(D,P,'docs/reviews/inventory.json'));sels=json.loads(blob(D,P,'docs/reviews/slices.json'))['slices'];rows=[dict(zip(inv['columns'],r)) for r in inv['rows'] if r[2]=='interface']
BASE=inv['header']['es']['merge_base'];UP=inv['header']['es']['upstream_head']
# Match the documented glob grammar independently, without importing the producer.
def expand(g):
 if '{' not in g:return [g]
 a=g.index('{');z=g.index('}',a);return [p for alt in g[a+1:z].split(',') for p in expand(g[:a]+alt+g[z+1:])]
@functools.lru_cache(None)
def regex(g):
 out='';i=0
 while i<len(g):
  if g[i:i+3]=='**/':out+='(?:.*/)?';i+=3
  elif g[i:i+2]=='**':out+='.*';i+=2
  elif g[i]=='*':out+='[^/]*';i+=1
  elif g[i]=='?':out+='[^/]';i+=1
  else:out+=re.escape(g[i]);i+=1
 return re.compile(out+'\\Z')
def globmatch(g,r):
 tree='es' if g.startswith('es:') else 'distribution';g=g[3:] if tree=='es' else g
 return tree==r['tree'] and any(regex(x).match(r['path']) for x in expand(g))
def match(s,sl,r):
 if r['area'] not in s.get('areas',[sl['area']]):return False
 if s.get('reach') and r['reach'] not in s['reach']:return False
 if s.get('tier') and r['tier'] not in s['tier']:return False
 if 'globs' not in s:return True
 return any(globmatch(g,r) for g in s['globs'] if not g.startswith('!')) and not any(globmatch(g[1:],r) for g in s['globs'] if g.startswith('!'))
compiled=[(sl,s) for sl in sels for s in (sl['select'] if isinstance(sl['select'],list) else [sl['select']])]
def owners(r):
 direct=[sl['id'] for sl,s in compiled if not s.get('rest') and match(s,sl,r)]
 return list(dict.fromkeys(direct or [sl['id'] for sl,s in compiled if s.get('rest') and match(s,sl,r)]))
assigned={};ambiguous=[]
for r in rows:
 ids=owners(r)
 if len(ids)!=1:ambiguous.append({'path':r['tree']+':'+r['path'],'owners':ids})
 else:assigned.setdefault(ids[0],[]).append(r)
t44=sorted(assigned['es-vendored-and-data'],key=lambda r:r['path']);paths=[r['path'] for r in t44]
def tree(ref):
 out={}
 for rec in git(E,'ls-tree','-rz',ref).split(b'\0'):
  if rec:
   m,p=rec.decode().split('\t',1);mode,kind,oid=m.split();out[p]={'mode':mode,'object_type':kind,'oid':oid}
 return out
trees={ref:tree(ref) for ref in [S,BASE,UP]};nt=trees[S]
numstat={}
for i in range(0,len(paths),150):
 for rec in git(E,'diff-tree','-r','--numstat','-z','--no-renames',EMPTY,S,'--',*paths[i:i+150]).split(b'\0'):
  if rec:
   added,deleted,p=rec.decode().split('\t',2);numstat[p]=None if added=='-' else int(added)
CODE={'shell','python','recipe','c','c++','c-header','c++-header','javascript','typescript','make','cmake','systemd','udev','script','perl','lua','rust','go','assembly','shader','docker','kconfig','html','css'}
def group(p):
 ps=p.split('/')
 if ps[0]=='external':return '/'.join(ps[:3]) if len(ps)>2 and ps[1]=='libcheevos' else '/'.join(ps[:2])
 if ps[0]=='locale':return '/'.join(ps[:2])
 if ps[0]=='resources':return '/'.join(ps[:2]) if len(ps)>2 else 'resources/(root)'
 if ps[0] in ['.github','scripts','tools','CMake','cmake']:return '/'.join(ps[:2]) if len(ps)>2 else ps[0]
 return ps[0] if len(ps)>1 else '(root)'
manifest=[];discrepancies=[]
for r in t44:
 p=r['path'];t=nt[p];b=None if t['mode']=='160000' else blob(E,S,p);old=trees[BASE].get(p);up=trees[UP].get(p)
 state='added-since-merge-base' if old is None else 'same-as-merge-base' if t==old else 'changed-since-merge-base'
 tier='upstream-carried' if state=='same-as-merge-base' else 'fork-own'
 binary=numstat.get(p) is None;logical=None if binary or b is None else b.count(b'\n')+(bool(b) and not b.endswith(b'\n'))
 if r['lines']!=numstat.get(p) or (b is not None and logical!=numstat.get(p)):discrepancies.append({'path':p,'inventory_lines':r['lines'],'git_numstat':numstat.get(p),'logical_blob_lines':logical})
 if r['tier']!=tier:discrepancies.append({'path':p,'inventory_tier':r['tier'],'derived_tier':tier})
 kind='symlink' if t['mode']=='120000' else 'gitlink' if t['mode']=='160000' else 'binary' if binary else 'text'
 manifest.append({'path':p,**t,'sha256':sha(b) if b is not None else None,'bytes':len(b) if b is not None else None,'inventory_lines':r['lines'],'git_numstat_lines':numstat.get(p),'text_logical_lines':logical,'newline_bytes':b.count(b'\n') if b is not None else None,'kind':kind,'language':r['language'],'tier':r['tier'],'tier_note':r['tier_note'],'group':group(p),'base_comparison':state,'fixed_upstream_same_identity':t==up,'read_formula_lines':(r['lines'] or 0) if r['language'] in CODE and r['tier']!='vendor-carried' and r['reach']!='unreached' else 0,'reach':r['reach'],'link_target':b.decode() if kind=='symlink' else None})
def aggregate(items):
 return {'paths':len(items),'inventory_lines':sum(x['inventory_lines'] or 0 for x in items),'text_logical_lines':sum(x['text_logical_lines'] or 0 for x in items),'bytes':sum(x['bytes'] or 0 for x in items),'text_newlines':sum(x['newline_bytes'] or 0 for x in items if x['kind']!='binary'),'read_formula_lines':sum(x['read_formula_lines'] for x in items),'fork_own_read_formula_lines':sum(x['read_formula_lines'] for x in items if x['tier']=='fork-own'),'tier':dict(collections.Counter(x['tier'] for x in items)),'kind':dict(collections.Counter(x['kind'] for x in items)),'mode':dict(collections.Counter(x['mode'] for x in items))}
groups={g:aggregate([x for x in manifest if x['group']==g]) for g in sorted({x['group'] for x in manifest})}
direct_candidates=[r for r in rows if r['tree']=='es' and not r['path'].startswith(('es-app/','es-core/'))]
removed=[{'path':r['path'],'owner':owners(r),'tier':r['tier'],'lines':r['lines']} for r in direct_candidates if r['path'] not in set(paths)]
neighbor={sl['k']:{'id':sl['id'],'select':sl['select'],'paths':len(assigned.get(sl['id'],[])),'lines':sum(r['lines'] or 0 for r in assigned.get(sl['id'],[])),'intersection':sorted(set(paths)&{r['path'] for r in assigned.get(sl['id'],[]) if r['tree']=='es'})} for sl in sels if sl['k'] in [20,21,34,35,36,37]}
path_bytes=''.join(p+'\n' for p in paths).encode();(O/'paths.txt').write_bytes(path_bytes)
objects=''.join('\t'.join([n['mode'],n['object_type'],n['oid'],n['path']])+'\n' for n in manifest).encode();(O/'object-identities.tsv').write_bytes(objects)
mh=save('manifest.json',{'distribution_P1':P,'coordinator':C,'ES_survey':S,'ES_fixed_merge_base':BASE,'ES_fixed_upstream':UP,'entries':manifest})
summary={'identity':'Codex / OpenAI; session01a19d11-dda5-72e3-86f9-416f36341c24; m6-p1-survey wN:p3','P1':P,'coordinator':C,'ES_survey':S,'ES_fixed_merge_base':BASE,'ES_fixed_upstream':UP,'input_hashes':input_hashes,'inventory_header_refs':{'distribution':inv['header']['distribution'],'es':inv['header']['es']},'scope':'T44 membership/boundary facts at survey pin only; no accepted later-history/import-version handoff duplication','interface_partition_ambiguities':ambiguous,'totals':aggregate(manifest),'groups':groups,'languages':{g:aggregate([x for x in manifest if x['language']==g]) for g in sorted({x['language'] for x in manifest})},'tier_base_states':{g:aggregate([x for x in manifest if x['base_comparison']==g]) for g in sorted({x['base_comparison'] for x in manifest})},'discrepancies':discrepancies,'naive_non_app_core_paths':len(direct_candidates),'excluded_by_nonrest':removed,'neighbor_boundaries':neighbor,'path_list_sha256':sha(path_bytes),'manifest_sha256':mh,'fork_own_paths':[x['path'] for x in manifest if x['tier']=='fork-own'],'binary_paths':[x['path'] for x in manifest if x['kind']=='binary'],'symlinks':[x for x in manifest if x['kind']=='symlink']}
top=lambda n:n['path'].split('/')[0] if '/' in n['path'] else '(root)'
summary['top_level_groups']={k:aggregate([n for n in manifest if top(n)==k]) for k in sorted({top(n) for n in manifest})}
summary['object_identity_tsv_sha256']=sha(objects)
summary['catalogues']={'po':35,'pot':1,'language_dirs':[n['path'].split('/')[2] for n in manifest if n['path'].startswith('locale/lang/')],'note':'Only survey-pin population derived; accepted later catalogue handoff belongs to T2.'}
assert sum(n['path'].endswith('.po') for n in manifest)==summary['catalogues']['po']
assert sum(n['path'].endswith('.pot') for n in manifest)==summary['catalogues']['pot']
summary['gitlinks']=[n for n in manifest if n['object_type']=='commit']
summary['fixed_upstream_equal_count']=sum(n['fixed_upstream_same_identity'] for n in manifest)
summary['seam_artifact_sha256']={p:sha(blob(E,S,p)) for p in ['.gitmodules','external/CMakeLists.txt','CMakeLists.txt','locale/CMakeLists.txt','locale/checkLocale.sh','getPoFromWebsite.sh','tests/app-unit/CMakeLists.txt','tests/app-unit/AppWindowTests.cpp','tests/app-unit/TextFitTests.cpp','tests/app-unit/fakes/components/AsyncNotificationComponent.h','tests/app-unit/fakes/SystemConf.h','tests/app-unit/fakes/Window.h','es-core/CMakeLists.txt','es-app/CMakeLists.txt']}
save('results.json',summary)
print(json.dumps({k:summary[k] for k in ['totals','tier_base_states','discrepancies','interface_partition_ambiguities','naive_non_app_core_paths','excluded_by_nonrest','neighbor_boundaries','path_list_sha256','manifest_sha256']},indent=2));print('GROUPS',json.dumps(groups,indent=1))
