from prooflib import *
import collections,functools,re,ast
errors=[];facts={};bindings=[]
def check(ok,label,detail=None):
 if not ok:errors.append({'check':label,'detail':detail})
def tree(ref):
 out={}
 for row in git('ls-tree','-r','-z',ref).split(b'\0'):
  if row:
   meta,path=row.split(b'\t',1);out[path.decode()]=tuple(meta.decode().split())
 return out
trees={ref:tree(ref) for ref in [SEED,D,FINAL]}
@functools.lru_cache(None)
def b(path,ref=FINAL):return blob(path,ref)
def jj(path,ref=FINAL):return json.loads(b(path,ref))
manifest=json.loads(ext('MANIFEST.json'));external={n:ext(n) for n in manifest['members']}
def ej(n):return json.loads(external[n])
pub=ej('publication.json')
commits=git('log','--reverse','--format=%H %P',SEED+'..'+FINAL).decode().splitlines()
prev=SEED
for line in commits:
 bits=line.split();check(len(bits)==2 and bits[1]==prev,'linear ancestry',line);prev=bits[0]
check([line.split()[0] for line in commits]==[D,*pub['record_commits']],'full ancestry exact')
facts['ancestry']=commits
changed={p for p in set(trees[D])|set(trees[FINAL]) if trees[D].get(p)!=trees[FINAL].get(p)}
NARR={A+x for x in ['00-running-log.md','04-analysis.md','05-punch-list.md','06-audit-summary.md','07-questions-for-the-maintainer.md','README.md']}
EXACT={'.github/sessions/saved-session-state-feature-m6-patches-unshipped-690.md','docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md','docs/work-logs/INDEX.md','docs/retros/2026-11-02-m6-patches-unshipped.md'}
TOOLN={'s1-input-contract.py','check-owner-outcomes.py','prepare-owner-outcomes.py','final-confinement.py','retirement.py','retirement-controls.py','retirement-owner-scope.py','final-record-scan.py','final-record-controls.py'}
allowed=lambda p:p in NARR|EXACT or any(p.startswith(A+'stage-'+s+'/') for s in 'efgh') or p in {A+'tools/'+n for n in TOOLN}
check(all(allowed(p) for p in changed),'final paths confined',[p for p in changed if not allowed(p)])
for line in commits[1:]:
 c=line.split()[0];rows=git('diff','--name-status',c+'^',c).decode().splitlines()
 check(all(x.split('\t',1)[0] in ('A','M') and allowed(x.split('\t',1)[1]) for x in rows),'per-commit records/no removal',c)
frozen={p:v for p,v in trees[D].items() if p.startswith(A) and p not in NARR}
check(len(frozen)==2923,'frozen count')
check(all(trees[FINAL].get(p)==v for p,v in frozen.items()),'frozen modes/blobs preserved')
seed_delta={p for p in set(trees[SEED])|set(trees[FINAL]) if trees[SEED].get(p)!=trees[FINAL].get(p)}
check(all(p.startswith(A) or p in EXACT for p in seed_delta),'whole source/rule/register identity outside records')
summary=jj(A+'stage-a/source/summary.json',D);source=jj(A+'stage-a/source/tree.json',D)
selected=set(source)|set(summary['recipe_sha256'])|set(summary['selector_sha256'])
check(all(trees[SEED].get(p)==trees[D].get(p)==trees[FINAL].get(p) for p in selected),'selected identity')
facts['identity']={'changed_records':len(changed),'frozen_D':len(frozen),'native':len(source),'recipes':len(summary['recipe_sha256']),'selectors':len(summary['selector_sha256']),'selected_union':len(selected),'D_programs':len([p for p in frozen if p.startswith(A+'tools/') and p.endswith('.py')]),'preserved02_sha256':sha(b(A+'02-forward-audit.md'))}
transport=jj(A+'stage-d/transport-manifest.json')
facts['transport_shape']={k:(len(v) if isinstance(v,(list,dict)) else v) for k,v in transport.items()}
check(sha(b(A+'02-forward-audit.md'))=='7500dde4d45de7cac02a0359b0f6171c4c6fea8b1d1045559971d024ea418869','preserved02 exact')
for p in [A+'README.md',A+'04-analysis.md',A+'05-punch-list.md',A+'06-audit-summary.md']:
 check('02-outcome-addendum.md' in b(p).decode(),'addendum link',p)
# Input manifest and matrix: comparison only, no accepted/new producer execution.
inputs=jj(A+'stage-e/input-manifest.json')
for rel,v in inputs['files'].items():
 path=A+rel;data=b(path,D)
 check(tuple(v[k] for k in ('mode','type','blob'))==trees[D][path] and sha(data)==v['stored_sha256'] and len(data)==v['stored_bytes'],'S1 immutable input',rel)
original=jj(A+'stage-b/open-inputs.json',D);plans={p['id']:p for p in jj(A+'stage-b/plans.json',D)}
matrix=jj(A+'stage-e/owner-outcomes.json')['outcomes']
check(set(matrix)=={r['path'] for r in original} and len(matrix)==93,'exact matrix keys')
def bound(v):
 path=A+v['path'];data=b(path,D)
 check(v['commit']==D and tuple(v[k] for k in ('mode','type','blob'))==trees[D][path] and sha(data)==v['stored_sha256'] and len(data)==v['stored_bytes'],'matrix bound record',v['path'])
owners=collections.Counter();status=collections.Counter();mixed=0
owner_map={'devices-unshipped':'T25 #672','image-packages':'T8 #655','emulators-standalone':'T30 #677','packages-dead-ends':'T23 #670','device-generic-x64-and-kernel':'T11 #658'}
for old in original:
 path=old['path'];row=matrix[path]
 check(all(row[k]==old[k] for k in ('owner','application','receipts')),'original row fields',path)
 check(row['source_input_status']=='open' and row['custody_outcome']=='recorded; source gap remains open','gap remains open',path)
 bound(row['original_binding']);owners[row['owner'].split(':',1)[0]]+=1
 expected={k for k,v in plans.items() if path in v['native_paths']}
 check({c['group'] for c in row['consumers']}==expected and len(row['consumers'])==len(expected),'all consumers',path)
 kinds=[]
 for c in row['consumers']:
  pp=plans[c['group']];rel='stage-b/application-overlay/'+pp['id']+'.json'
  if A+rel not in trees[D]:rel='stage-b/application/'+pp['id']+'.json'
  er=jj(A+rel,D);bound(c['evidence']);bound(c['plan_binding'])
  check(c['evidence']['path']==rel,'effective receipt precedence',c['group'])
  check(all(c[k]==pp[k] for k in ('consumer','recipe','pin','url','expected_sha256')) and c['recipe_owner']==pp['owner'] and c['owner_issues']==[owner_map[x] for x in pp['owner']],'consumer owner and source fields',c['group'])
  if er['status']=='open-item':
   check(c['status']=='open-item' and c['source_input_status']=='open' and c['missing_inputs']==er['limits'] and c['retained_normal_result'] is None,'open consumer preserved',c['group']);kinds.append('open')
  else:
   matches=[x for x in er['rows'] if x['path']==path];check(len(matches)==1,'positive source row unique',c['group'])
   z=matches[0];check(c['status']==z['status'] and c['retained_normal_result']=={k:z['normal'][k] for k in ('exit','stdout_sha256','stderr_sha256')} and c['missing_inputs']==[] and c['source_input_status']=='qualified-at-D','positive qualification preserved',c['group']);kinds.append('positive')
  check(bool(c['next_qualification_mechanism']),'next mechanism nonempty',c['group'])
  status[kinds[-1]]+=1
 check(row['mixed']==('positive' in kinds),'mixed flag',path);mixed+=row['mixed']
check(dict(owners)=={'T25 #672':9,'T11 #658':72,'T30 #677':3,'T23 #670':7,'T8 #655':2},'owner totals')
check(dict(status)=={'open':188,'positive':36} and mixed==6,'consumer totals')
facts['matrix']={'keys':len(matrix),'consumers':dict(status),'mixed':mixed,'wholly_open':len(matrix)-mixed,'owners':dict(owners),'immutable_inputs':len(inputs['files'])}
controls=jj(A+'stage-e/owner-outcome-controls.json');last=''
for i,c in enumerate(controls):
 name=c['name'];fixture=A+'stage-e/owner-outcomes.json' if name=='positive' else A+'stage-e/fixtures/'+name+'.json'
 check(sha(b(fixture))==c['fixture_sha256'],'S1 fixture hash',name)
 for stream in ('stdout','stderr'):check(sha(b(A+'stage-e/fixtures/'+name+'.'+stream))==c[stream+'_sha256'],'S1 output hash',name+'/'+stream)
 check(sha(b(A+'tools/check-owner-outcomes.py'))==c['reader_sha256'] and sha(b(A+'tools/s1-input-contract.py'))==c['input_reader_sha256'] and sha(b(A+'stage-e/input-manifest.json'))==c['immutable_input_manifest_sha256'],'S1 program/input hashes',name)
 check(c['exit']==(0 if i==7 else 1),'S1 actual exit',name)
 check(c['started']>=last and c['finished']>=c['started'],'S1 actual sequence',name);last=c['finished']
 if i<7:check(c['expected_refusal'] in b(A+'stage-e/fixtures/'+name+'.stderr').decode(),'S1 specific refusal',name)
facts['S1_controls']=[{'name':c['name'],'exit':c['exit'],'expected_refusal':c.get('expected_refusal')} for c in controls]
# Exact final changed-record scan: hash bytes, do not run the forbidden scanner.
scan=ej('exact-commit-records-v2.manifest.json');sr=ej('exact-commit-records-v2.result.json')
check(set(scan['files'])==changed and scan['count']==159 and scan['ref']==FINAL and scan['base']==D and scan['excluded_repository_paths']==[],'exact final scan membership')
payload=hashlib.sha256();total=0
for i,(path,v) in enumerate(scan['files'].items()):
 data=b(path);check(len(data)==v['bytes'] and sha(data)==v['sha256'],'exact scan file',path);total+=len(data)
 if i:payload.update(b'\n')
 payload.update(data)
check(total==35595500==scan['total_bytes'] and payload.hexdigest()==sr['stdin_sha256'] and sr['stdin_bytes']==total+158,'exact scan bytes/stdin')
check(sr['manifest_sha256']==sha(external['exact-commit-records-v2.manifest.json']) and sr['exit']==0,'scan result binding')
for stream in ['stdout','stderr']:check(sr[stream+'_sha256']==sha(external['exact-commit-records-v2.check.'+stream]),'scan output binding',stream)
facts['scan']={'count':len(changed),'bytes':total,'stdin_sha256':payload.hexdigest(),'scanner_replayed':False}
# All final publication artifact bindings.
for path,v in pub['retained_artifact_bindings'].items():check(len(b(path))==v['bytes'] and sha(b(path))==v['sha256'],'publication artifact binding',path)
(P/'reconcile-core-results.json').write_text(json.dumps({'errors':errors,'facts':facts},indent=2)+'\n')
print(json.dumps({'errors':errors,'facts':facts},indent=2))
