"""Root readback of the new T44 marker and records; no producer execution."""
from pathlib import Path
import datetime,hashlib,json,re,subprocess
TIP='523a25d5b0140be131c1de02881f21790f013f4f'
ACCEPTED='f01abd480f4e0b337a9fcdde2cec9bc1746b525d'
A='docs/audits/2026_11_02-epic-m6-es-vendored-and-data/'
OUT=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
events=[]
def git(*args):
 p=subprocess.run(['git',*args],capture_output=True);events.append({'argv':['git',*args],'rc':p.returncode,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)});assert p.returncode==0;return p.stdout
def show(path,ref=TIP):return git('show',ref+':'+path)
def tree(ref):
 result={}
 for row in git('ls-tree','-r','-z',ref).split(b'\0'):
  if row:
   meta,p=row.split(b'\t',1);result[p.decode()]=meta.decode()
 return result
old,new=tree(ACCEPTED),tree(TIP)
changed={p for p in old.keys()|new.keys() if old.get(p)!=new.get(p)}
exact={A+n for n in ['audit-completion.json','tracker-final-readback.json','tracker-completion.json']}
exact|={'.github/sessions/saved-session-state-feature-m6-es-vendored-and-data-691.md','docs/work-logs/2026_11-work_logs/2026_11_03-work_log.md','docs/work-logs/INDEX.md'}
assert all(p in exact or p.startswith(A+'completion/') for p in changed)
assert all(p in new and new[p].startswith('100644 blob ') for p in changed)
assert all(new.get(p)==v for p,v in old.items() if p.startswith(A))
assert sum(p.startswith(A) for p in old)==440
assert git('show','-s','--format=%P',TIP).decode().strip()==ACCEPTED
cache={p:show(p) for p in changed if p.startswith(A)}
marker=cache[A+'audit-completion.json'];assert sha(marker)=='e5de3cc09413bbb35d9bd32897eaaefd8ec56f113dfb0f468fe044a661a8638b'
m=json.loads(marker);assert m['schema']==1 and m['issue']==1413
for p,h in m['evidence'].items():
 assert not p.startswith('/') and '..' not in Path(p).parts
 if p not in cache:cache[p]=show(p)
 assert sha(cache[p])==h,p
live={x['issue_number']:x for x in json.loads((OUT/'live-issues.json').read_bytes())}
rb=json.loads(cache[m['tracker_readback']]);tc=json.loads(cache[m['tracker_completion']])
assert rb['number']==1413 and rb['body']==live[1413]['body'] and rb['state']==live[1413]['state']=='closed' and rb['state_reason']==live[1413]['state_reason']=='completed'
assert tc['verified_utc']==m['completed_at'] and tc['closed_completed']==[1413] and tc['body_sha256']==sha(rb['body'].encode())
dt=lambda x:datetime.datetime.fromisoformat(x.replace('Z','+00:00'))
assert dt(rb['closed_at'])<=dt(m['completed_at'])<=datetime.datetime.now(datetime.timezone.utc)
assert len(re.findall(r'^- \[x\]',rb['body'],re.M))==1 and '- [ ]' not in rb['body']
assert live[691]['state']=='open' and live[691]['body'].count('- [x]')==20 and '- [ ]' not in live[691]['body']
assert live[1414]['state']=='open' and live[1414]['body'].count('- [ ]')==5
assert 'fixed-at: '+ACCEPTED in live[691]['body'] and 'fixed-at-es: 55158d2a64c69fe295fb4e67fd174424a71b1b4d' in live[691]['body']
for v in json.loads(cache[A+'completion/coordinator-inputs.json']):
 b=show(v['path'],v['ref']);assert b==cache[v['retained_as']] and sha(b)==v['sha256']
runner=sha(cache[A+'completion/run.py']);bindings=[]
for p,b in list(cache.items()):
 if not p.endswith('/receipt.json'):continue
 r=json.loads(b);folder=p.rsplit('/',1)[0]
 if 'argv' not in r:continue
 assert r['rc']==0 and r['runner_sha256']==runner and r['cpus']==list(range(8,24)) and r['start']<=r['end'],p
 for s in ['stdout','stderr']:assert sha(cache[folder+'/'+s])==r[s+'_sha256']
 assert sha(cache[folder+'/scope.json'])==r['scope_sha256']
 bindings.append({'path':p,'argv':r['argv'],'rc':r['rc'],'stdout_sha256':r['stdout_sha256'],'stderr_sha256':r['stderr_sha256']})
checks=json.loads(cache[A+'completion/checks-readback.json'])['checks']
for name,v in checks.items():
 p=A+'completion/checks/'+name+'/receipt.json';assert sha(cache[p])==v['receipt_sha256'];r=json.loads(cache[p]);assert r['rc']==v['rc']==0
 for s in ['stdout','stderr']:assert r[s+'_sha256']==v[s+'_sha256']
for name in ['normal-lint','issue-lint']:assert cache[A+'completion/checks/'+name+'/stdout'].decode().rstrip().endswith('PASS')
assert cache[A+'completion/checks/marker/stdout'].decode().strip()=='PASS schema1 1413'
result={'result':'PASS immutable normal completion; external publication separate','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tip':TIP,'accepted':ACCEPTED,'marker_sha256':sha(marker),'evidence_hashes':len(m['evidence']),'accepted_files_unchanged':440,'changed_paths':sorted(changed),'new_command_bindings':bindings,'checks':len(checks),'closed_at':rb['closed_at'],'completed_at':m['completed_at'],'no_accepted_execution_replayed':True}
(OUT/'coordinator-verification.json').write_text(json.dumps(result,indent=2)+'\n');(OUT/'commands.json').write_text(json.dumps(events,indent=2)+'\n');(OUT/'audit-completion.json').write_bytes(marker)
print('PASS',len(m['evidence']),'evidence hashes',len(bindings),'command bindings',len(checks),'checks',len(changed),'changed paths; 440 accepted files unchanged')
