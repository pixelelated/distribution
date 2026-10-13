from pathlib import Path
import json,subprocess,hashlib,datetime,os
r=Path(__file__).parent;old=Path('/workspace/tmp/pix570-handoff-20261013');repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');ssh=json.loads((r/'ssh-command.json').read_text());receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':[],'removed':[]}
for root,count in [(old,6),(Path('/workspace/tmp/pix570-ua-20261013'),8),(r,8)]:
 p=root/'matrix-result.json';x=json.loads(p.read_text());assert x['rc']==0 and len(x['cases'])==count,(str(root),x)
 assert json.loads((root/'matrix-owner/launcher-result.json').read_text())['runner_returncode']==0
 receipt['results'].append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'cases':count})
c="""python3 - <<'P'
from pathlib import Path
import subprocess,json,hashlib
subprocess.run(['/usr/bin/cloud_oauth','cancel'],check=True,capture_output=True)
subprocess.run(['umount','/usr/bin/cloud-signin-window'],check=True,capture_output=True)
es=[];browsers=[]
for p in Path('/proc').glob('[0-9]*'):
 try:
  exe=(p/'exe').resolve().name
  if exe=='emulationstation':es.append(int(p.name))
  if exe in ['cloud-signin-window','WebKitWebProcess','WebKitNetworkProcess']:browsers.append(int(p.name))
 except OSError:pass
x={'boot':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'es':es,'browser_processes':browsers,'rclone_sha256':hashlib.sha256(Path('/usr/bin/rclone').read_bytes()).hexdigest(),'browser_sha256':hashlib.sha256(Path('/usr/bin/cloud-signin-window').read_bytes()).hexdigest(),'meminfo':{l.split(':')[0]:int(l.split()[1]) for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith(('MemTotal:','MemAvailable:','SwapTotal:','SwapFree:'))}}
assert x['boot']=='5f507670-bab1-4cd9-9803-f0a1fbbdcf1e' and es==[1630] and not browsers,x
assert x['rclone_sha256']=='ed887da83d3e2c07ff8acc60cb5b56dbe7bb4d73cc445b6ff71988f164c0558a'
assert x['browser_sha256']=='6cbc445686d3d484ff20450342776e9eb92b47f6112a0352be1a50b334eef81b'
print(json.dumps(x,indent=2))
P"""
p=subprocess.run(ssh+[c],capture_output=True,text=True,timeout=35);(r/'final-readback.txt').write_text(p.stdout+p.stderr);p.check_returncode();receipt['guest']=json.loads(p.stdout)
pid=int((old/'vm.pid').read_text());subprocess.run([str(repo/'tools/vm-stop'),str(old/'vm.pid'),str(old/'disk.qcow2')],check=True,timeout=30)
proc=Path('/proc')/str(pid);assert not (proc/'stat').exists() or (proc/'stat').read_text().rsplit(')',1)[1].split()[0]=='Z'
for name in ['disk.qcow2','OVMF.fd','qa-key','qa-key.pub','known_hosts','monitor.sock','serial.sock']:
 p=old/name
 if not p.exists():continue
 st=p.lstat();receipt['removed'].append({'path':str(p),'size':st.st_size,'allocated':st.st_blocks*512});p.unlink()
receipt['rc']=0;(r/'retirement.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'rc':0,'removed':len(receipt['removed']),'allocated_bytes':sum(x['allocated'] for x in receipt['removed'])}))
