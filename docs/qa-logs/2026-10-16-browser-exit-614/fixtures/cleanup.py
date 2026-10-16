import subprocess,time,json,hashlib
from pathlib import Path
R=Path('/storage/qa614');(R/'stop').touch();deadline=time.monotonic()+8
while not (R/'observer-result.json').exists() and time.monotonic()<deadline:time.sleep(.1)
observer=json.loads((R/'observer-result.json').read_text());assert observer['rc']==0 and observer['stopped'] and not observer['guards']
commands=[]
for argv in [['systemctl','show','qa614-observer','-p','Result','-p','ExecMainCode','-p','ExecMainStatus','-p','ActiveState'],['umount','/usr/bin/rclone'],['systemctl','unset-environment','CLOUD_SIGNIN_DEBUG'],['/usr/bin/rclone','listremotes']]:
 p=subprocess.run(argv,capture_output=True,text=True,timeout=10);commands.append({'argv':argv,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0
assert commands[-1]['stdout'].strip()==''
assert hashlib.sha256(Path('/usr/bin/rclone').read_bytes()).digest()==hashlib.sha256((R/'rclone-original').read_bytes()).digest()
j=subprocess.run(['journalctl','-k','-b','--no-pager'],capture_output=True,text=True,timeout=10);assert j.returncode==0
(R/'kernel.log').write_text(j.stdout)
failures=[x for x in j.stdout.splitlines() if any(s in x.lower() for s in ['out of memory','oom-kill','segfault','general protection fault','kernel panic'])];assert not failures
result={'rc':0,'observer':observer,'commands':commands,'rclone_restored':True,'kernel_failures':failures};(R/'cleanup-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
