from prooflib import *
import functools,collections,ast
errors=[];facts={}
def check(ok,label,detail=None):
 if not ok:errors.append({'check':label,'detail':detail})
@functools.lru_cache(None)
def b(path,ref=FINAL):return blob(path,ref)
def jj(rel):return json.loads(b(A+rel))
canonical=lambda x:sha(json.dumps(x,sort_keys=True,separators=(',',':')).encode())
planbytes=b(A+'stage-h/retirement-plan.json');plan=json.loads(planbytes);res=jj('stage-h/retirement-result.json');census=jj('stage-h/closing-census.json');pc=jj('stage-h/planner-correction.json')
check(b(A+'stage-h/retirement-plan.json','fb97dd53bd8e936ff7402888c70fb6bc25f7180d')==planbytes,'plan committed at fb97 before mutation')
raw=ext('retirement-plan-v2.raw')
check(len(raw)==pc['raw_bytes'] and sha(raw)==pc['raw_sha256'] and raw.endswith(b'\\n') and raw[:-2]+b'\n'==planbytes,'exact literal-newline-only correction')
check(sha(planbytes)==res['committed_plan_sha256']==census['plan_sha256']==pc['stored_plan_sha256'],'plan hash chain')
commit=json.loads(ext('fg-plan-commit.json'));retire=jj('stage-h/retirement-run.json')
check(commit['exit']==0 and commit['finished']<retire['started']<=res['at']<=res['finished']<=retire['finished'],'plan commit predates mutation receipt')
check(set(plan['roots'])==set(res['roots']) and len(plan['roots'])==889,'same exact 889 roots')
counts=collections.Counter(x['status'] for x in res['roots'].values());check(dict(counts)=={'retired':881,'retained':8},'retirement statuses')
check(census['retired']==881 and census['retained']==8 and census['partial']==0 and census['retired_absence_confirmed'],'closing census totals')
check(plan['cache_metadata_before']==res['cache_metadata_after'] and len(plan['cache_metadata_before'])==21,'21 cache metadata pairs')
for x in [plan,res,census]:check(x['global_no_reference_assertion'] is False,'no global process assertion')
# Independent reconstruction of snapshot associations from accepted custody records, in memory.
cust=jj('stage-d/custody.json');expected={};categories=collections.Counter()
for root,v in cust['owned_receipt_bound_roots'].items():
 ev=jj(v['evidence']);snap=None
 if v['role']=='needed source members':snap=ev['input_snapshot']
 elif v['role'] in ('normal candidate','successful prefix'):
  found=[z['candidate_snapshot'] for z in ev.get('rows',[]) if z.get('candidate_root')==root]
  if found:snap=found[-1]
  elif ev.get('final_prefix_root')==root:snap=ev['final_prefix_snapshot']
 elif v['role']=='constructed guard fixture':
  snap={'prefix/'+k:x for k,x in ev['prefix_after'].items()}
  snap.update({'candidate/'+k:x for k,x in ev.get('failed_candidate',{}).items()})
 check(snap is not None,'retained custody snapshot exists',root)
 expected[root]=(snap,v['evidence'],'D')
for x in jj('stage-d/prefix-custody.json')['records']:expected[x['path']]=(x['observed_snapshot'],'stage-d/prefix-custody.json','current-prefix')
empty=jj('stage-d/empty-prefix-observation.json')['records']
for x in empty:expected[x['path']]=({},'stage-d/empty-prefix-observation.json','empty-current-only')
for filename in ['retirement-control-custody.json','retirement-control-custody-v2.json']:
 x=jj('stage-f/'+filename);creation=jj(x['creation_receipt'])
 check(x['root']==creation['root'],'F scratch creation binding',filename)
 expected[x['root']]=(x['final_snapshot'],'stage-f/'+filename,'new-F')
check(set(expected)==set(plan['roots']),'exact root scope from custody')
for root,entry in plan['roots'].items():
 snap,evidence,kind=expected[root];categories[kind]+=1
 check(entry['evidence']==evidence,'root evidence path',root)
 check(pathlib.PurePosixPath(root).parent==pathlib.PurePosixPath('/workspace/tmp/m6-t43') and not any(s in pathlib.PurePosixPath(root).name for s in ['cache','receipt','publication']),'root path confinement metadata',root)
 after=res['roots'][root]
 if entry['status']=='retained':
  check(after==entry and census['retained_roots'].get(root)==entry,'retained stays retained',root);continue
 check(entry['content_snapshot_sha256']==canonical(snap) and entry['files']==len(snap) and entry['bytes']==sum(x['bytes'] for x in snap.values()),'root expected snapshot binding',root)
 check(after['files']==entry['files'] and after['bytes']==entry['bytes'] and after['custody_class']==entry['custody_class'],'retired metadata binding',root)
 for own in [entry['owner_evidence'],after['owner_evidence']]:
  cm=own['completion'];cb=b(A+cm['receipt']);recorded=json.loads(cb)
  check(sha(cb)==cm['sha256'] and all(cm[k]==recorded[k] for k in ['argv','cwd','started','finished','exit']) and cm['termination']=='returned','own completion binding',root)
  check(cm['finished']<retire['started'],'own producer returned before retire',root)
  check(own['global_no_reference_assertion'] is False and '/proc/2389/cwd' in own['unknown_process_visibility_limit'],'preserve inaccessible process limit',root)
  check(all(z['references_to_root']==[] and z['role']=='current metadata/deletion observer' and z['state']=='active-observer' for z in own['known_jobs']),'known own observer record',root)
  if cm['receipt']=='stage-f/retirement-controls-v2-run.json':
   check(cm['accounted_known_children']==jj('stage-f/retirement-controls-v2.json')['known_children'],'joined-child binding',root)
 if kind=='empty-current-only':check(after['method']=='nonrecursive rmdir' and entry['empty_only'] and snap=={},'four empty prefixes narrow method',root)
check(set(census['four_empty_prefixes_nonrecursive_removed'])=={x['path'] for x in empty},'four exact empty prefixes')
# Original refusal and new control-to-program bindings.
old=b(A+'stage-f/failed-retirement.py');oldrun=jj('stage-f/retirement-controls-run.json')
check(sha(old)=='2b98e817e600b31cbe213cb03e063fc51697ee56eadbcfb8ddb91ede682991a8','original failed program preserved')
check(oldrun['exit']==1 and sha(b(A+'stage-f/retirement-controls-run.stderr'))=='304a35c54e67eae80ca8ac34f72914a399bf610ff373b2b2be590c50c2b10483','original rc1/stderr preserved')
controls=jj('stage-f/retirement-controls-v2.json')
for key,path in [('program_sha256','stage-f/retirement-tested-v2.py'),('scope_program_sha256','tools/retirement-owner-scope.py'),('controller_sha256','tools/retirement-controls.py')]:
 check(controls[key]==sha(b(A+path)),'cleanup tested-program binding',path)
check(len(controls['records'])==12 and all(x['passed'] for x in controls['records']),'11 refusals plus scoped positive')
for c in controls['records'][:-1]:check(c['expected_refusal'] in c['actual_message'] and c['started']<=c['finished'],'specific own control',c['name'])
children=controls['known_children'];check(len(children)==1 and children[0]['exit']==0 and children[0]['joined'] and children[0]['finished']<controls['records'][-1]['finished'],'known child joined before positive')
def functions(data):return {x.name:ast.dump(x,include_attributes=False) for x in ast.parse(data).body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))}
before=functions(b(A+'stage-f/retirement-tested-v2.py'));after=functions(b(A+'tools/retirement.py'))
changed=[k for k in set(before)|set(after) if before.get(k)!=after.get(k)]
check(set(changed)=={'plan','completed'},'only documented code corrections',changed)
check(all(before[k]==after[k] for k in pc['unchanged_guard_functions']),'original tested guard functions unchanged')
late=jj('stage-f/late-record-controls.json')
check(late['program_sha256']==sha(b(A+'tools/retirement.py')) and late['fixture_sha256']==sha(b(A+'stage-f/fixtures/unaccounted-child.json')),'late child control input program hashes')
check(late['actual_child_positive']['accounted_known_children']==children and late['plan_sha256']==sha(planbytes),'late child and plan binding')
facts={'plan_sha256':sha(planbytes),'plan_commit':res['committed_at'],'commit_finished':commit['finished'],'retire_started':retire['started'],'counts':dict(counts),'scope_categories':dict(categories),'cache_metadata_pairs':21,'fresh_cache_content_hash_claim':False,'own_controls':[x['name'] for x in controls['records']],'known_child':children[0]['pid'],'changed_functions_after_test':sorted(changed),'original_failure_exit':oldrun['exit'],'no_root_process_or_cache_inspection':True}
(P/'reconcile-cleanup-results.json').write_text(json.dumps({'errors':errors,'facts':facts},indent=2)+'\n')
print(json.dumps({'errors':errors,'facts':facts},indent=2))
