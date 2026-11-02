"""Independent immutable-receipt reconciliation. Never loads or runs producer code.
Only git show/ls-tree/diff/rev-list are invoked. No worktree/cache/private reads.
Output is a small JSON summary; input bytes stay in memory.
"""
import collections,csv,functools,hashlib,io,json,pathlib,re,subprocess
R='/workspace/repos/pixelelated/distribution.worktrees/m6-p1-survey-641'
T='d37670de318eb428604e4442f95defe10eade173'
S='9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1'
P='2174265e9cc1b248c0fbe27fa101875984d46d6b'
B='b6332dbc13f5929f05ec5ba23c44285c5ee56b38'
A='docs/audits/2026_11_02-epic-m6-patches-shipped/'
D=pathlib.Path(__file__).parent
def git(*args):return subprocess.check_output(['git','-C',R,*args])
def sha(b):return hashlib.sha256(b).hexdigest()
@functools.lru_cache(None)
def blob(p,ref=T):return git('show',ref+':'+p)
def j(p):return json.loads(blob(A+p))
errors=[]
def check(ok,detail):
 if not ok:errors.append(detail)
def trees(ref,paths):
 out={}
 for i in range(0,len(paths),150):
  for row in git('ls-tree','-rz',ref,'--',*paths[i:i+150]).split(b'\0'):
   if row:
    meta,p=row.decode().split('\t',1);mode,kind,oid=meta.split();out[p]={'mode':mode,'type':kind,'oid':oid}
 return out
def snapshot(x,where):check(sha(json.dumps(x['files'],sort_keys=True).encode())==x['sha256'],'snapshot metadata digest '+where)
ns=j('stage-b/native-inputs.json');tb=j('stage-b/tables.json');groups=j('stage-b/selection.json')
native={n['path']:n for n in ns};keys=set(native)
check(len(ns)==len(keys)==384,'native input population')
for name in ['native','coverage']:
 check(len(tb[name])==384 and {x['path'] for x in tb[name]}==keys,name+' exact keys')
leadpath='docs/qa-logs/2026-11-02-m6-resume/t42-inherited/leads.tsv'
leads=list(csv.DictReader(io.StringIO(blob(leadpath).decode()),delimiter='\t'))
ik=[(x['patch'],x['override']) for x in tb['inherited']]
check(len(ik)==len(set(ik))==50 and set(ik)=={(x['patch'],x['override']) for x in leads},'frozen inherited keys')
check(len({x['override'] for x in tb['inherited']})==26,'26 inherited overrides')
check(sha(blob(leadpath,S))==sha(blob(leadpath)),'frozen leads unchanged since seed')
f=tb['fork_written'];check(len(f)==12 and sum(x['logical_lines'] for x in f)==498,'fork 12/498')
check({x['path'] for x in f}=={x['path'] for x in ns if x['fork_written']},'fork exact keys')
for x in f:
 check(x['read_lines']=='1-'+str(x['logical_lines']),'fork range '+x['path'])
 check(x['patch_sha256']==native[x['path']]['patch_sha256'],'fork input hash '+x['path'])
counts={name:dict(collections.Counter(x[field] for x in tb[name])) for name,field in [('native','application_status'),('inherited','conclusion')]}
audit_paths=set(git('ls-tree','-r','--name-only',T,'--',A).decode().splitlines())
required_native=['origin_header','last_path_commit','targets','target_version','recipe_pin_per_plan','order_context','application','application_status','upstream_status','upstream_evidence','backport_status','carrying_reason','disposition','owner']
for n in tb['native']:
 check(all(isinstance(n[k],str) and n[k].strip() for k in required_native),'native required fields '+n['path'])
 check(bool(re.search(r'#\d+',n['owner'])),'native owner '+n['path'])
 check(all(A+p in audit_paths for p in n['receipts']),'native receipt links '+n['path'])
for n in tb['inherited']:
 check(all(isinstance(n[k],str) and n[k].strip() for k in ['prior_recipe_owner','target_pins','feature_architecture_and_intent','counterpart_source_evidence','prior_base_disposition','remaining_owner_action']),'inherited required fields '+str(n['index']))
 check(bool(re.search(r'#\d+',n['remaining_owner_action'])),'inherited owner '+str(n['index']))
 check(all(A+p in audit_paths for p in n['evidence']),'inherited receipt links '+str(n['index']))
check(len([p for p in audit_paths if p.startswith(A+'second-opinions/')])==1,'one-file Local plan')
check(j('second-opinions/review-plan.json')['reviewers']==[],'empty reviewers')
check(counts['native']=={'applies':151,'offset':38,'fuzz':22,'open-item':173},'native status counts')
check(counts['inherited']=={'already-carried':21,'not-applicable-with-reason':7,'unresolved-with-specific-evidence-needed':22},'inherited conclusion counts')
selectors=list(j('stage-a/seed/summary.json')['selector_sha256'])
allpaths=sorted(keys|{n['referent'] for n in ns}|set(selectors))
tt=trees(T,allpaths)
identities={}
for ref in [P,B,S]:
 tr=trees(ref,allpaths);changed=[p for p in allpaths if tr.get(p)!=tt.get(p)];identities[ref]={'paths':len(allpaths),'changed':changed};check(not changed,'source/selector/referent identity '+ref)
for n in ns:
 p=n['path'];check(tt[p]['mode']==n['mode'] and tt[p]['oid']==n['oid'],'native mode/blob '+p)
 check(sha(blob(p))==n['sha256'] and sha(blob(n['referent']))==n['patch_sha256'],'native/referent hash '+p)
 if n['mode']=='120000':check(blob(p).decode()==n['link_target'],'literal link '+p)
for x in tb['native']:
 n=native[x['path']]
 check(all(x[k]==n[k] for k in ['mode','oid','sha256','referent']),'table identity '+x['path'])
 check(x['referent_sha256']==n['patch_sha256'],'table referent hash '+x['path'])
for p,h in j('stage-a/seed/summary.json')['selector_sha256'].items():check(sha(blob(p))==h,'selector sha '+p)
check(j('stage-a/seed/tree.json')=={p:tt[p] for p in keys},'stage A seed identity table')
check(j('stage-a/source/tree.json')=={p:tt[p] for p in keys},'stage A source identity table')
allowed=[A,'.github/sessions/saved-session-state-feature-m6-patches-shipped-689.md','docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md','docs/work-logs/INDEX.md','docs/retros/2026-11-02-m6-patches-shipped.md']
def allowed_path(p):return any(p.startswith(a) if a.endswith('/') else p==a for a in allowed)
delta=git('diff','--name-only','-z',S,T).decode().strip('\0').split('\0');check(all(allowed_path(p) for p in delta),'final tree protected path')
commits=[]
for c in git('rev-list',S+'..'+T).decode().splitlines():
 ps=git('rev-list','--parents','-n','1',c).decode().split();check(len(ps)==2,'unexpected merge '+c)
 changed=git('diff','--name-only','-z',ps[1],c).decode().strip('\0').split('\0')
 check(all(allowed_path(p) for p in changed),'commit protected path '+c);commits.append({'commit':c,'changed_paths':len(changed)})
applications={g['id']:j('stage-b/application/'+g['id']+'.json') for g in groups}
hashes=[];pairs=0;rowcounts=collections.Counter();missing=[];prefix_checks=0
for g in groups:
 a=applications[g['id']];prev=None
 for row in a['rows']:
  rowcounts[row['status']]+=1
  if not (row.get('invoked') and 'normal' in row):continue
  pairs+=1
  check(row['diagnostic']['argv']==['patch','--dry-run','-p1','-N','--batch'] and row['normal']['argv']==['patch','-p1','-N','--batch'],'argv '+g['id'])
  check((row['normal']['rc']==0)==row['promoted'],'promotion '+g['id'])
  check(row['normal']['locale']==row['diagnostic']['locale']=='C','locale '+g['id'])
  check(sha(blob(row['referent'],S))==row['literal_sha256'],'literal hash '+g['id'])
  check(row['rendered_sha256']==row['patch_sha256'],'rendered identity '+g['id'])
  for phase in ['normal','diagnostic']:
   for stream in ['stdout','stderr']:
    p=row[phase][stream];actual=sha(blob(A+p));expected=row[phase][stream+'_sha256'];check(actual==expected,'stream hash '+p);hashes.append([p,actual])
  for phase in ['before','after']:snapshot(row[phase],g['id']+phase)
  if prev is not None:check(prev==row['before'],'retained prefix continuity '+g['id']);prefix_checks+=1
  prev=row['after'] if row['promoted'] else row['before']
  text=(blob(A+row['normal']['stdout'])+blob(A+row['normal']['stderr'])).decode()
  status='fails' if row['normal']['rc'] else 'fuzz' if 'fuzz' in text.lower() else 'offset' if 'offset' in text.lower() else 'applies'
  check(status==row['status'],'normal output classification '+g['id'])
 if len(a['rows'])<len(g['stack']):missing.append({'group':g['id'],'recorded':len(a['rows']),'selected':len(g['stack']),'missing':[x['path'] for x in g['stack'] if x['path'] not in {r['path'] for r in a['rows']}]})
rank={'applies':0,'offset':1,'fuzz':2,'open-item':3,'blocked':4,'fails':5}
for n in tb['native']:
 statuses=[]
 for g in groups:
  if n['path'] not in g['native']:continue
  rs=[r for r in applications[g['id']]['rows'] if r['path']==n['path']]
  if rs:statuses.append(rs[0]['status'])
  else:
   check(g['id'] in ['G202','G203'],'unexplained missing native row '+g['id']);statuses.append('open-item')
 check(max(statuses,key=rank.get)==n['application_status'],'worst native status '+n['path'])
archives=git('ls-tree','-r','--name-only',T,'--',A+'stage-b/application').decode().splitlines()
archives=[p for p in archives if '/archive-' in p and p.endswith('.json')]
for p in archives:
 x=json.loads(blob(p));check(x['sha256']==x['recipe_sha256'],'archive recorded identity '+p);snapshot(x['source_tree'],p)
check((pairs,len(hashes),len(archives))==(760,3040,116),'760/3040/116')
receipt_checks=[]
def receipt(x,stem):
 hs={}
 for stream in ['stdout','stderr']:
  p=A+stem+'.'+stream;h=sha(blob(p));check(h==x[stream+'_sha256'],'command output hash '+p);hs[stream+'_sha256']=h
 receipt_checks.append({'stem':stem,'rc':x['rc'],'argv':x['argv'],**hs})
for x,stem in zip(j('stage-a/commands.json'),['source','seed']):receipt(x,'stage-a/'+stem)
for x in j('stage-a/checks.json'):
 name=x['argv'][0].split('/')[-1];h=sha(blob(A+'stage-a/'+name+'.out'));check(h==x['output_sha256'],'stage A check '+name);receipt_checks.append({'stem':'stage-a/'+name,'rc':x['rc'],'output_sha256':h})
for x,stem in zip(j('stage-c/checks.json'),['rules','register','index','ceremony','forbidden','hooks']):receipt(x,'stage-c/'+stem)
for record,stem in [('stage-c/table-validation.json','stage-c/table-validation'),('stage-c/receipt-validation-command.json','stage-c/receipt-validation'),('stage-c/pre-issue-lint-command.json','stage-c/pre-issue-lint'),('stage-d/table-final.json','stage-d/table-final'),('stage-d/audit-body-update.json','stage-d/audit-body-update')]:receipt(j(record),stem)
for p in ['stage-d/checks.json','stage-d/issue-commands.json']:
 for x in j(p):receipt(x,'stage-d/'+x['name'])
partial=j('stage-b/application/partial-failure-control.json')
check(partial['normal']['rc']!=0 and not partial['promoted'] and partial['after']['sha256']!=partial['before']['sha256'] and not partial['successor']['invoked'],'partial failure guard')
for phase in ['normal','diagnostic']:
 x=partial[phase];receipt(x,x['stdout'].removesuffix('.stdout'))
for x,phase in zip(j('stage-b/nested-patch/receipt.json')['runs'],['diagnostic','normal']):receipt(x,'stage-b/nested-patch/'+phase)
pub=j('stage-d/publication-1.json');publication=[]
for x in pub['events']:publication.append({'name':x['name'],'rc':x['rc'],'stdout_sha256':sha(x['stdout'].encode()),'stderr_sha256':sha(x['stderr'].encode())})
check(pub['tip']==git('rev-list','--parents','-n','1',T).decode().split()[1],'publication binds parent not final tip')
live={}
for number in [1410,1411]:
 current=json.loads((D/f'issue-{number}.json').read_text());saved=j(f'stage-d/issue-{number}-final.json')
 live[str(number)]={'body_matches_retained':current['body']==saved['body'],'live_body_sha256':sha(current['body'].encode()),'state':current['state'],'milestone':current['milestone'],'labels':[x['name'] for x in current['labels']]}
 check(current['body']==saved['body'],'live issue differs '+str(number))
meta=['stage-a/seed/summary.json','stage-a/source/summary.json','stage-b/table-counts.json','stage-b/tables.json','stage-b/selection.json','stage-b/inherited-decisions.json','stage-b/nested-patch/receipt.json','stage-b/application/partial-failure-control.json','stage-c/negative-controls.json','stage-c/protected-path-controls.json','stage-c/receipt-validation.json','stage-d/checks.json','stage-d/issue-commands.json','stage-d/publication-1.json','05-punch-list.md','06-audit-summary.md','07-questions-for-the-maintainer.md','tools/validate.py','tools/apply-stacks.py','tools/tables.py','tools/nested-probe.py']
result={'identity':'Codex / OpenAI; session 01a19d11-dda5-72e3-86f9-416f36341c24; wN:p3 m6-p1-survey','tip':T,'seed':S,'scope':'Immutable metadata and retained-output reconciliation only; no producer or source execution; no private/cache/archive reads.','errors':errors,'counts':counts,'identity_comparisons':identities,'native_modes':dict(collections.Counter(n['mode'] for n in ns)),'fork_readings':{'paths':len(f),'lines':sum(x['logical_lines'] for x in f),'dolphin':[x['path'] for x in f if 'dolphin' in x['path']]},'changed_path_count':len(delta),'commits':commits,'application':{'groups':len(groups),'pairs':pairs,'output_hashes':len(hashes),'hash_manifest_sha256':sha(json.dumps(sorted(hashes),separators=(',',':')).encode()),'archive_projection_receipts':len(archives),'retained_prefix_continuities':prefix_checks,'row_statuses':dict(rowcounts),'missing_selected_rows':missing},'command_receipts':receipt_checks,'publication':{'receipt_tip':pub['tip'],'events':publication,'note':pub['note']},'live_issues':live,'artifact_sha256':{p:sha(blob(A+p)) for p in meta},'brief_sha256':sha(blob('docs/reviews/briefs/patches-shipped.md'))}
(D/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:result[k] for k in ['errors','counts','identity_comparisons','native_modes','fork_readings','changed_path_count','commits','live_issues','brief_sha256']},indent=2))
print('APPLICATION',json.dumps(result['application'],indent=2));print('COMMAND RECEIPTS',len(receipt_checks));print('RESULT_SHA256',sha((D/'results.json').read_bytes()))
