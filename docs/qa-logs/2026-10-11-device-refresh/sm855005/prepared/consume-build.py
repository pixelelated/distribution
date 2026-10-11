from pathlib import Path
import datetime,hashlib,json,subprocess
O=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
result=load(O/'launcher-result.json');assert result['runner_returncode']==0
run=Path((O/'run.path').read_text().strip())
channels={str(p):int(p.read_text().strip()) for p in [O/'inner.rc',O/'outer.rc',O/'tool-wrapper.rc',run/'build.rc']}
assert all(v==0 for v in channels.values()),channels
pids={result['pid']}
for p in [*[run/n for n in ['build.pid','command.pid','watcher.pid','build.status.pid']],O/'observer.pid']:
 if p.exists():pids.add(int(p.read_text().strip()))
assert all(not Path('/proc',str(pid)).exists() for pid in pids),pids
cid=(O/'build.cid').read_text().strip();q=subprocess.run(['docker','inspect',cid],capture_output=True,text=True);assert q.returncode==1 and ('no such object' in q.stderr.lower() or 'no such container' in q.stderr.lower())
for n,h in load(O/'build-seal.json').items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
assert load(O/'artifacts/installed-inclusion.json')['result']=='PASS'
assert load(O/'artifacts/output-manifest.json')['result']=='BUILT_REQUIRES_ARTIFACT_ACCEPTANCE'
subprocess.run(['python3','-I',str(O/'verify-source.py')],check=True)
record={'result':'PASS','verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channels':channels,'launcher_returncode':result['runner_returncode'],'actual_owner_pids_absent':sorted(pids),'actual_container_removed':cid,'run':str(run),'source_and_seals_unchanged':True,'scope':'build/installed inclusion; raw/update acceptance still required'}
(O/'build-consumption.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
