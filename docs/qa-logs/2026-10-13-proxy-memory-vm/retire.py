from pathlib import Path
import json,subprocess,hashlib,datetime,socket
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup'); channels=[]
for owner,run in [('boot-owner','20261013T054703Z-ca2e0553'),('experiment-owner','20261013T054939Z-ce4d5dee')]:
 o=r/owner;b=repo/'.build-runs'/run
 assert json.loads((o/'launcher-result.json').read_text())['runner_returncode']==0
 assert (o/'tool-wrapper.rc').read_text().strip()=='0' and (b/'build.rc').read_text().strip()=='0'
 pids=[json.loads((o/'launcher-pid.json').read_text())['pid']]+[int((b/x).read_text()) for x in ('build.pid','command.pid','watcher.pid')]
 for pid in pids:
  p=Path('/proc')/str(pid)
  assert not p.exists() or not (p/'cmdline').read_bytes(),pid
 channels.append({'owner':owner,'run':run,'launcher_rc':0,'wrapper_rc':0,'build_rc':0,'pids':pids,'all_exited':True})
assert json.loads((r/'result.json').read_text())['rc']==0
pid=int((r/'vm.pid').read_text());cmd=Path('/proc',str(pid),'cmdline').read_bytes().decode().split('\0')
x=subprocess.run([str(repo/'tools/vm-stop'),str(r/'vm.pid'),str(r/'disk.qcow2')],text=True,capture_output=True,check=True);print(x.stdout,flush=True)
removed=[]
for name in ('disk.qcow2','OVMF.fd','qa-key','qa-key.pub','known_hosts','stage.tar.gz'):
 p=r/name
 if not p.exists():continue
 s=p.stat();entry={'name':name,'logical_bytes':s.st_size,'allocated_bytes':s.st_blocks*512}
 if name not in ('qa-key','qa-key.pub','known_hosts'):
  with p.open('rb') as f:entry['sha256']=hashlib.file_digest(f,'sha256').hexdigest()
 p.unlink();entry['absent_after']=not p.exists();removed.append(entry)
for port in (10575,5960):
 with socket.socket() as s:s.bind(('127.0.0.1',port))
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channels':channels,'vm_pid':pid,'qemu_argv':cmd,'stop_stdout':x.stdout.strip(),'stop_rc':x.returncode,'retired':removed,'allocated_bytes_recovered':sum(x['allocated_bytes'] for x in removed),'host_ports_released':[10575,5960],'fixture_scope':'No owner device/account/config used. All state synthetic; no product changes.'}
(r/'retirement.json').write_text(json.dumps(report,indent=2)+'\n');print('Retired; recovered '+str(report['allocated_bytes_recovered'])+' allocated bytes',flush=True)
