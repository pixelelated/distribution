from pathlib import Path
import datetime,hashlib,json,subprocess,sys
owner=Path(sys.argv[1]).resolve();run=Path((owner/'run.path').read_text().strip())
channels={n:(owner/n).read_text().strip() for n in ['inner.rc','outer.rc','tool-wrapper.rc']};channels['build.rc']=(run/'build.rc').read_text().strip();assert len(set(channels.values()))==1,channels
pids=[json.loads((owner/'launcher-pid.json').read_text())['pid']]+[int((run/n).read_text()) for n in ['build.pid','watcher.pid','command.pid']]
for pid in pids:assert not Path('/proc',str(pid)).exists(),pid
inputs={}
if (owner/'seal.json').exists():inputs.update(json.loads((owner/'seal.json').read_text()))
if (owner/'harness.sha256').exists():
 for line in (owner/'harness.sha256').read_text().splitlines():
  h,n=line.split('  ',1);inputs[n]=h
for n,h in inputs.items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
receipt=dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),result='PASS' if channels['build.rc']=='0' else 'FAILED',channels=channels,pids_absent=pids,sealed_inputs=len(inputs),scope='owner processes and input seals only; separately verify guest/backend cleanup where applicable',launcher_result=json.loads((owner/'launcher-result.json').read_text()))
with (owner/'owner-verification.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt))
