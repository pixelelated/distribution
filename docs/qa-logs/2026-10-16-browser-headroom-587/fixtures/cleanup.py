import subprocess,time,json,hashlib,os
from pathlib import Path
R=Path('/storage/qa587');commands=[]
def call(a):
 p=subprocess.run(a,capture_output=True,text=True,timeout=25);row={'argv':a,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr};commands.append(row);assert p.returncode==0,row;return p.stdout
observer=json.loads((R/'observer-result.json').read_text());assert observer['rc']==0 and not observer['guards'] and observer['error'] is None
call(['systemctl','show','qa587-observer','-p','Result','-p','ExecMainCode','-p','ExecMainStatus','-p','ActiveState'])
call(['systemctl','stop','raofflineproxy.service']);state=call(['systemctl','show','raofflineproxy.service','-p','Result','-p','ExecMainCode','-p','ExecMainStatus','-p','ActiveState','-p','MainPID']);assert 'Result=success' in state and 'MainPID=0' in state
call(['systemctl','stop','qa587-peer']);call(['ip','link','delete','qa587dummy']);call(['ip','route','del','192.0.2.1/32','dev','lo']);call(['ip','addr','del','192.0.2.2/32','dev','lo'])
call(['umount','/usr/bin/rclone']);call(['systemctl','unset-environment','CLOUD_SIGNIN_DEBUG']);assert not call(['/usr/bin/rclone','listremotes']).strip()
assert hashlib.sha256(Path('/usr/bin/rclone').read_bytes()).digest()==hashlib.sha256((R/'rclone-original').read_bytes()).digest()
protected=json.loads((R/'protected.json').read_text());preserved={p:dict(expected=x,actual={'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest(),'mode':Path(p).stat().st_mode&0o777}) for p,x in protected.items()}
installed=json.loads((R/'installed.json').read_text());changed=[p for p,h in installed.items() if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h];assert not changed
j=call(['journalctl','-k','-b','--no-pager']);(R/'kernel.log').write_text(j)
errors=[x for x in j.splitlines() if any(s in x.lower() for s in ['out of memory','oom-kill','segfault','general protection fault','kernel panic'])];assert not errors
(R/'proxy-journal.log').write_text(call(['journalctl','-b','-u','raofflineproxy.service','--no-pager']))
assert sorted(x.name for x in Path('/sys/class/net').iterdir())==['lo']
processes=[]
for p in Path('/proc').iterdir():
 if not p.name.isdigit():continue
 try:
  argv=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace');exe=os.path.basename(os.readlink(p/'exe'))
  if exe=='cloud-signin-window' or 'WebKit' in exe or 'qa587/peer.py' in argv or 'qa587/observer.py' in argv or '-m raofflineproxy.main run-service' in argv:processes.append({'pid':int(p.name),'exe':exe,'argv':argv})
 except OSError:pass
assert not processes,processes
result={'rc':0,'observer':observer,'commands':commands,'protected':preserved,'installed_changed':changed,'rclone_restored':True,'kernel_failures':errors,'remaining_test_processes':processes,'interfaces':['lo']}
(R/'cleanup-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
