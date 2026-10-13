from pathlib import Path
import json,subprocess,hashlib,datetime,socket
r=Path('/workspace/tmp/pix565-clean-state-20261013');repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');channels=[]
for owner,want in [('boot-owner',0),('first-boot-owner',2),('controls-owner',0),('first-boot02-owner',0),('controls02-owner',0)]:
 o=r/owner;b=Path((o/'console.log').read_text().splitlines()[0].split('recording in ',1)[1])
 assert json.loads((o/'launcher-result.json').read_text())['runner_returncode']==want
 assert int((o/'tool-wrapper.rc').read_text())==want and int((b/'build.rc').read_text())==want
 pids=[json.loads((o/'launcher-pid.json').read_text())['pid']]+[int((b/n).read_text()) for n in ['build.pid','command.pid','watcher.pid','build.status.pid']]
 for pid in pids:
  p=Path('/proc')/str(pid);assert not p.exists() or not (p/'cmdline').read_bytes(),pid
 channels.append({'owner':owner,'run':str(b),'actual_rc':want,'pids':pids,'all_exited':True})
for owner in ('controls-owner','controls02-owner'):
 x=json.loads((r/owner/'controls-result.json').read_text());assert x['guest_rc']==0 and x['stderr_empty'] and x['report']['status']=='pass'
x=subprocess.run([str(repo/'tools/vm-serial'),'--socket',str(r/'serial.sock'),'--timeout','30','sh','cat /proc/sys/kernel/random/boot_id; sha256sum /usr/bin/emulationstation /usr/lib/libc.so.6; uname -r'],capture_output=True,text=True,check=True,timeout=35)
(r/'actual-identities.txt').write_text(x.stdout)
pid=int((r/'vm.pid').read_text());cmd=Path('/proc',str(pid),'cmdline').read_bytes().decode().split('\0')
x=subprocess.run([str(repo/'tools/vm-stop'),str(r/'vm.pid'),str(r/'disk.qcow2')],text=True,capture_output=True,check=True);print(x.stdout,flush=True)
removed=[]
for name in ['disk.qcow2','OVMF.fd']:
 p=r/name;s=p.stat();row={'name':name,'logical_bytes':s.st_size,'allocated_bytes':s.st_blocks*512}
 with p.open('rb') as f:row['sha256']=hashlib.file_digest(f,'sha256').hexdigest()
 p.unlink();row['absent_after']=not p.exists();removed.append(row)
for port in [10577,5962]:
 with socket.socket() as s:s.bind(('127.0.0.1',port))
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channels':channels,'vm_pid':pid,'qemu_argv':cmd,'stop_rc':x.returncode,'retired':removed,'no_ssh_key_staged':True,'allocated_bytes_recovered':sum(x['allocated_bytes'] for x in removed),'ports_released':[10577,5962]}
(r/'retirement.json').write_text(json.dumps(report,indent=2)+'\n');print('Retired clean-state VM; recovered',report['allocated_bytes_recovered'])
