from pathlib import Path
import sys,json,socket,hashlib,subprocess,datetime
owner=Path(sys.argv[1]); run=Path((owner/'run.path').read_text().strip())
status=(run/'build.status').read_text()
assert 'state:       finished' in status,status
rc={str(p):int(p.read_text().strip()) for p in [owner/'inner.rc',owner/'outer.rc',owner/'tool-wrapper.rc',run/'build.rc']}
assert set(rc.values())=={0},rc
pids=[json.loads((owner/'launcher-pid.json').read_text())['pid']]
for line in status.splitlines():
 if line.startswith(('job_pid:','watcher_pid:')):pids.append(int(line.split()[1]))
pids.extend(map(int,(owner/'guest-pids.txt').read_text().split()))
assert all(not Path('/proc',str(p)).exists() for p in pids),pids
for entry in Path('/proc').glob('[0-9]*/cmdline'):
 try:name=Path(entry.read_bytes().split(b'\0',1)[0].decode()).name
 except (OSError,UnicodeError):continue
 assert not name.startswith('qemu-system-'),str(entry)
for port in [10026,5912]:
 with socket.socket() as s:s.bind(('127.0.0.1',port))
subprocess.run(['sha256sum','-c',str(owner/'harness.sha256')],check=True,stdout=subprocess.DEVNULL)
results=[]
for p in sorted((owner/'artifacts').glob('*/result.json')):
 data=json.loads(p.read_text());assert data['failures']==0
 results.append({'path':str(p.relative_to(owner)),**data})
assert len(results)==4
record={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':str(owner),'run':str(run),'result_channels':rc,'actual_absent_pids':pids,'no_qemu':True,'unbound_ports':[10026,5912],'harness_seal_verified':True,'results':results,'assertions':sum(r['assertions'] for r in results),'frames':len(list((owner/'artifacts').glob('*/*.png'))),'qualification':'final runtime matrix; visual review separate' if owner.name.endswith('03') else ('superseded: pending refusal crossed the next language profile; French baseline already shows a card' if owner.name.endswith('02') else 'superseded: original census omitted compiled proxy modules; functional observations retained')}
(owner/'completion.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
