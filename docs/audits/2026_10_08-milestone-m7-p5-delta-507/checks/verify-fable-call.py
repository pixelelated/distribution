#!/usr/bin/env python3
"""Verify a completed, approved Facilitator call; no network or credential access."""
import datetime, hashlib, json, sys
from pathlib import Path
root=Path.cwd(); owner=Path(sys.argv[1]); run=Path(sys.argv[2]); output=Path(sys.argv[3]); prompt=Path(sys.argv[4])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
channels={str(p):int(p.read_text().strip()) for p in [owner/'inner.rc',owner/'outer.rc',owner/'tool-wrapper.rc',run/'build.rc']}
seal=json.loads((owner/'input-seal.json').read_text())
checks={'four_zero_channels':all(v==0 for v in channels.values()),'input_before':all(json.loads((owner/'input-before.json').read_text()).values()),'input_after':all(json.loads((owner/'input-after.json').read_text()).values()),'sealed_inputs_still_match':all(sha(root/p)==h for p,h in seal.items())}
prov=json.loads(Path(str(output)+'.provenance.json').read_text());final=prov['final'];verification=final['verification'];effort=final['effort_verification']
checks.update(success=final['outcome']=='success',no_retries=final['retries_used']==0,prompt_digest=prov['request']['user_prompt_sha256']==sha(prompt),output_digest=sha(output)==prov['output_file_sha256']==final['file_artifact_sha256'],identity=verification['result']=='PASS' and verification['observed']=='anthropic/claude-fable-5.1' and verification['model_identity_source']=='provider_response',effort=effort['result']=='PASS' and effort['declared']=='xhigh')
pids={json.loads((owner/'launcher-pid.json').read_text())['pid']}
for name in ['build.pid','watcher.pid','command.pid']:
 p=run/name
 if p.exists():
  text=p.read_text().strip()
  try:pids.add(int(text))
  except ValueError: pass
live=owner/'live-readback01.json'
if live.exists():pids.update(int(v) for v in json.loads(live.read_text()).get('host_process_stat',{}))
tree=owner/'process-tree01.json'
if tree.exists():pids.update(int(v['pid']) for v in json.loads(tree.read_text()).get('processes',[]))
processes={}
for pid in sorted(pids):
 p=Path('/proc')/str(pid)/'stat'
 try:
  raw=p.read_text();state=raw.rsplit(')',1)[1].split()[0];processes[str(pid)]={'state':state,'stat':raw,'terminal':state=='Z'}
 except FileNotFoundError:processes[str(pid)]={'terminal':True,'state':'absent'}
checks['recorded_processes_terminal']=all(p['terminal'] for p in processes.values())
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channels':channels,'checks':checks,'passed':all(checks.values()),'input_count':len(seal),'output_bytes':output.stat().st_size,'output_sha256':sha(output),'prompt_sha256':sha(prompt),'processes':processes,'final':final}
(owner/'verified-completion.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));sys.exit(0 if result['passed'] else 1)
