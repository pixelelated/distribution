"""Read the new immutable completion record; never invoke accepted producers."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

TIP='fd1238800b61431a8febeebe8cf44f41d2384bbb'
ACCEPTED='8282cbcade3be32b437f7391be7e216d9a6b1074'
A='docs/audits/2026_11_02-epic-m6-patches-unshipped/'
OUT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
events=[]
def git(*args):
    r=subprocess.run(['git',*args],capture_output=True)
    events.append({'argv':['git',*args],'rc':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)})
    assert r.returncode==0,r.stderr
    return r.stdout
def show(path,ref=TIP):return git('show',ref+':'+path)
def tree(ref):
    result={}
    for row in git('ls-tree','-r','-z',ref).split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1);result[path.decode()]=meta.decode()
    return result
old,new=tree(ACCEPTED),tree(TIP)
changed={p for p in old.keys()|new.keys() if old.get(p)!=new.get(p)}
exact={'.github/sessions/saved-session-state-feature-m6-patches-unshipped-690.md','docs/work-logs/2026_11-work_logs/2026_11_03-work_log.md','docs/work-logs/INDEX.md',A+'audit-completion.json',A+'tracker-final-readback.json',A+'tracker-completion.json'}
assert all(p in exact or p.startswith(A+'completion/') for p in changed)
assert all(new.get(p)==v for p,v in old.items() if p.startswith(A))
assert git('show','-s','--format=%P',TIP).decode().strip()==ACCEPTED
for p in changed:assert p in new and new[p].startswith('100644 blob ')
marker=show(A+'audit-completion.json');assert sha(marker)=='d2e25d864705c2df0bdd371b89380262b810397d3691f9ce54410799e0752635'
m=json.loads(marker);assert m['schema']==1 and m['issue']==1412
cache={p:show(p) for p in changed if p.startswith(A)}
for p,h in m['evidence'].items():
    assert not p.startswith('/') and '..' not in Path(p).parts
    if p not in cache:cache[p]=show(p)
    assert sha(cache[p])==h,p
rb=json.loads(cache[m['tracker_readback']]);tc=json.loads(cache[m['tracker_completion']]);live=json.loads((OUT/'live-closed-audit.json').read_text())
assert rb['number']==live['issue_number']==1412 and rb['state']==live['state']=='closed' and rb['state_reason']==live['state_reason']=='completed'
assert rb['body']==live['body'] and len(re.findall(r'^- \[x\]',rb['body'],re.M))==1 and not re.search(r'^- \[ \]',rb['body'],re.M)
assert tc['result']=='PASS' and tc['exact_bodies_and_states'] and tc['closed_completed']==[1412] and tc['verified_utc']==m['completed_at']
dt=lambda x:datetime.datetime.fromisoformat(x.replace('Z','+00:00'))
assert dt(rb['closed_at'])<=dt(m['completed_at'])<=datetime.datetime.now(datetime.timezone.utc)
ci=json.loads(cache[A+'completion/source-issue-readback.json'])
assert ci['state']=='open' and ci['body'].count('- [x]')==20 and '- [ ]' not in ci['body']
assert 'reviewed-at: 601e4694f9726b2228d3571efdb5cfc061c6d442' in ci['body'] and 'fixed-at: '+ACCEPTED in ci['body']
co=json.loads(cache[A+'completion/coordinator-evidence.json'])
for path,v in co['bindings'].items():
    b=show(path,co['coordinator_commit']);assert b==cache[v['retained_path']] and sha(b)==v['sha256'] and len(b)==v['bytes']
checks=json.loads(cache[A+'completion/checks/results.json']);bindings=[]
producer=sha(show(A+'tools/record.py'));hashes={sha(b) for b in cache.values()}
for path,b in cache.items():
    if not path.endswith('.json'):continue
    record=json.loads(b)
    if not isinstance(record,dict) or not all(k in record for k in ('argv','exit','stdout_sha256','stderr_sha256')):continue
    assert record['stdout_sha256'] in hashes and record['stderr_sha256'] in hashes,path
    assert record['exit']==0 and record['producer_sha256']==producer,path
    assert record['affinity']==list(range(8,24))
    bindings.append({'path':path,'exit':record['exit'],'stdout_sha256':record['stdout_sha256'],'stderr_sha256':record['stderr_sha256']})
for name,v in checks.items():
    rec=json.loads(cache[v['receipt']]);assert rec['exit']==v['exit']==0 and rec['finished']==v['finished']
    for stream in ('stdout','stderr'):assert sha(cache[A+'completion/checks/'+name+'.'+stream])==rec[stream+'_sha256']
for name in ('lint','lint-issue'):assert cache[A+'completion/checks/'+name+'.stdout'].decode().rstrip().endswith('PASS')
assert 'PASS existing schema-1 completed_audit_marker: 1412' in cache[A+'completion/checks/marker.stdout'].decode()
result={'result':'PASS immutable completion marker and records; publication verification remains separate','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'accepted_source':ACCEPTED,'completion':TIP,'marker_sha256':sha(marker),'evidence_hashes':len(m['evidence']),'accepted_audit_files_unchanged':sum(p.startswith(A) for p in old),'changed_paths':sorted(changed),'new_command_bindings':bindings,'normal_checks':len(checks),'live_closed_body_exact':True,'completed_at':m['completed_at'],'closed_at':rb['closed_at'],'no_accepted_execution_replayed':True}
(OUT/'coordinator-verification.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'coordinator-commands.json').write_text(json.dumps(events,indent=2)+'\n')
(OUT/'audit-completion.json').write_bytes(marker)
print('PASS',len(m['evidence']),'marker hashes;',len(bindings),'new command bindings;',len(checks),'normal checks;',result['accepted_audit_files_unchanged'],'accepted audit files unchanged')
