"""Seven immutable inputs and new exact owning-tracker reads; no old replay."""
import base64,datetime,hashlib,json,pathlib,re,subprocess
C=pathlib.Path(__file__).resolve().parent;R=C.parents[3];A=C.parent;expected=json.loads((C/'expected-current.json').read_text());ctx=json.loads((C/'context.json').read_text());out=C/'collection';out.mkdir(exist_ok=False);commands=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists();p.write_text(json.dumps(x,indent=2,ensure_ascii=True)+'\n')
def call(argv):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(argv,capture_output=True,cwd=R);end=datetime.datetime.now(datetime.timezone.utc).isoformat();commands.append({'argv':argv,'cwd':str(R),'start':start,'end':end,'rc':r.returncode,'stdout_base64':base64.b64encode(r.stdout).decode(),'stderr_base64':base64.b64encode(r.stderr).decode(),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)});(out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');assert r.returncode==0,(argv,r.returncode);return r.stdout
prefix='docs/qa-logs/2026-11-03-m6-records-final/';rows=[]
for name in ['acceptance.md','criteria.md','root-live-publication.json','root-record-checks-network.json','integration/retention.json','p1-support/retention.json','publication/retention.json']:
 path=prefix+name;b=call(['git','show',ctx['coordinator']+':'+path]);meta=call(['git','ls-tree',ctx['coordinator'],'--',path]).decode().strip();dst=C/'coordinator'/name;dst.parent.mkdir(parents=True,exist_ok=True);assert not dst.exists();dst.write_bytes(b);assert dst.read_bytes()==b;rows.append({'source_commit':ctx['coordinator'],'source_path':path,'ls_tree':meta,'retained_path':str(dst.relative_to(R)),'bytes':len(b),'sha256':sha(b)})
write(C/'coordinator-inputs.json',rows)
frozen={}
for row in call(['git','ls-tree','-rlz',ctx['accepted_final'],'--',str(A.relative_to(R))]).split(b'\0'):
 if row:
  meta,path=row.split(b'\t',1);mode,kind,oid,size=meta.decode().split();frozen[path.decode()]={'mode':mode,'type':kind,'oid':oid,'bytes':int(size)}
assert len(frozen)==976 and all(x['mode']=='100644' and x['type']=='blob' for x in frozen.values());write(C/'accepted-audit-identities.json',frozen)
issues={}
for n in [1417,693,1416,1415]:
 b=call(['gh','api','repos/pixelelated/distribution/issues/'+str(n)]);x=json.loads(b);(C/('tracker-'+str(n)+'.json')).write_bytes(b);issues[n]=x
 if str(n) in expected['issues']:
  prior=expected['issues'][str(n)];assert x['body']==prior['body'] and x['state']==prior['state'] and x['state_reason']==prior['state_reason']
 ticks=re.findall(r'^\s*- \[([ xX])\]',x['body'],re.M)
 if n==1417:assert x['state']=='closed' and x['state_reason']=='completed' and x['closed_at']=='2026-11-03T14:07:02Z' and ticks==['x']
 elif n==693:assert x['state']=='open' and ticks.count('x')==17 and ticks.count(' ')==1 and 'fixed-at: '+ctx['accepted_final'] in x['body']
 elif n==1416:assert x['state']=='open' and ticks==['x','x']
 else:assert x['state']=='open'
for n,name in [(6605921275,'acceptance'),(6605965227,'dispatch')]:
 b=call(['gh','api','repos/pixelelated/distribution/issues/comments/'+str(n)]);x=json.loads(b);assert x['body']==expected['comments'][str(n)]['body'];(C/(name+'-readback.json')).write_bytes(b);(C/(name+'-body.md')).write_text(x['body'])
verified=datetime.datetime.now(datetime.timezone.utc).isoformat();receipt={'result':'PASS','exact_bodies_and_states':True,'closed_completed':[1417],'verified_utc':verified,'closed_at':issues[1417]['closed_at'],'timestamp_meaning':'Current verification time is distinct from tracker closure time.','issues':{str(n):{'state':x['state'],'state_reason':x['state_reason'],'closed_at':x['closed_at'],'body_sha256':sha(x['body'].encode())} for n,x in issues.items()},'accepted_final':ctx['accepted_final'],'coordinator':ctx['coordinator'],'no_tracker_writes':True};write(C/'tracker-completion.json',receipt)
evidence=[A/'04-analysis.md',A/'05-punch-list.md',C/'tracker-1417.json',C/'tracker-completion.json',C/'acceptance-readback.json',C/'dispatch-readback.json',C/'coordinator-inputs.json']+[R/x['retained_path'] for x in rows]
marker={'schema':1,'issue':1417,'completed_at':verified,'tracker_readback':str((C/'tracker-1417.json').relative_to(R)),'tracker_completion':str((C/'tracker-completion.json').relative_to(R)),'evidence':{str(p.relative_to(R)):sha(p.read_bytes()) for p in evidence},'accepted_final':ctx['accepted_final'],'reviewed_at':'d707c82ab8c48b674acc1f95a9571f0cb24d226a','execution_seed':'8710a6210a40de0110244d03a886161ee06faf29','source_fix':'45d455adccb0b2fc418f6442c4ca16a983430617','actual_primary':ctx['identity'],'acceptance_url':expected['comments']['6605921275']['url']};write(A/'audit-completion.json',marker)
print(json.dumps({'result':'PASS','coordinator_inputs':len(rows),'frozen_audit_files':len(frozen),'closed_completed':1417,'closed_at':issues[1417]['closed_at'],'verified_utc':verified,'693':'open;17 checked/1 unchecked; accepted source/seed/final headers unchanged','1416':'open;2 checked','1415':'open','tracker_writes':False}))
