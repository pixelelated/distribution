from pathlib import Path
import datetime,hashlib,json,subprocess
O=Path(__file__).resolve().parent;launch=O/'cache-launch'
load=lambda p:json.loads(p.read_text())
result=load(launch/'launcher-result.json');assert result['runner_returncode']==0
run=Path((O/'copy.run').read_text().strip())
channels={str(p):int(p.read_text().strip()) for p in [O/'copy.rc',O/'copy.outer.rc',launch/'tool-wrapper.rc',run/'build.rc']}
assert all(v==0 for v in channels.values()),channels
pids={result['pid']}
for n in ['build.pid','command.pid','watcher.pid','build.status.pid']:
 p=run/n
 if p.exists():pids.add(int(p.read_text().strip()))
assert all(not Path('/proc',str(pid)).exists() for pid in pids),pids
ready=load(O/'cache-ready.json');assert ready['result']=='PASS' and len(ready['roots'])==2
assert all(r['checksum_equal'] and r['independent_regular_files']>1000000 for r in ready['roots'])
for n,h in load(O/'copy-seal.json').items():assert hashlib.sha256((O/n).read_bytes()).hexdigest()==h,n
subprocess.run(['python3','-I',str(O/'verify-source.py')],check=True)
record={'result':'PASS','verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channels':channels,'launcher_returncode':result['runner_returncode'],'actual_owner_pids_absent':sorted(pids),'run':str(run),'cache_ready':ready,'copy_seal_unchanged':True}
(O/'cache-consumption.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
