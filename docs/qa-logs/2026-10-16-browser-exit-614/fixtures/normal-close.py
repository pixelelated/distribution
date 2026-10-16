import subprocess,json,time
from pathlib import Path
pids=subprocess.check_output(['pidof','cloud-signin-window'],text=True).split();assert len(pids)==1
p=Path('/proc',pids[0]);before={'pid':int(pids[0]),'start':int((p/'stat').read_text().rsplit(')',1)[1].split()[19])}
start=time.monotonic();r=subprocess.run(['/usr/bin/cloud_oauth','close'],capture_output=True,text=True,timeout=20);elapsed=time.monotonic()-start
print(json.dumps({'before':before,'started':start,'elapsed':elapsed,'original_rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'browser_pid_gone':not p.exists(),'guard':Path('/storage/qa614/guard.jsonl').exists()}))
assert r.returncode==0 and elapsed<20 and not p.exists() and not Path('/storage/qa614/guard.jsonl').exists()
