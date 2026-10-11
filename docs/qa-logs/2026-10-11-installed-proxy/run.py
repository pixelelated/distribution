from pathlib import Path
import os,subprocess,json,hashlib,time
p=Path(__file__).resolve().parent
previous=Path('/workspace/tmp/pixelelated-m7-upgrade19c')
for name,digest in json.loads((p/'prepared-manifest.json').read_text())['files'].items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest,name
assert json.loads((previous/'launcher-result.json').read_text())['runner_returncode']==1
subprocess.run(['python3','/workspace/tmp/pixelelated-m7-build19/verify-source.py'],check=True)
env={**os.environ,'TMPDIR':str(p/'tmp'),'VM_PAIR_DIR':str(previous/'pair'),'VM_QEMU_RUNTIME_DIR':str(p/'runtime'),'PYTHONDONTWRITEBYTECODE':'1'}
subprocess.run(['python3',str(p/'preflight.py')],env=env,check=True)
rows=[]
def step(name,cmd):
 print('START',name,flush=True)
 with (p/(name+'.log')).open('w') as f:rc=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 rows.append({'step':name,'returncode':rc});(p/'result.json').write_text(json.dumps(rows,indent=2)+'\n');print('END',name,rc,flush=True);return rc
pair='/workspace/repos/rocknix/tools/vm-pair'
try:
 assert step('boot-retained',['projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm','run','--headless','--daemonize','--monitor',str(p/'runtime/rocknix-qemu-monitor.sock'),'--serial',str(p/'runtime/rocknix-qemu-serial.sock'),'--pidfile',str(p/'runtime/rocknix-qemu.pid'),'--vnc','9','--ssh-port','10022','--mac','52:54:00:52:4E:58',str(previous/'pair/vm-a.qcow2')])==0
 for _ in range(90):
  ready=subprocess.run([pair,'ssh','a','systemctl is-active rocknix-autostart.service'],env=env,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,timeout=15)
  if ready.returncode==0 and ready.stdout.strip()=='active':break
  time.sleep(2)
 else:raise RuntimeError('retained guest startup not ready')
 assert step('payload',['python3',str(p/'check-payload.py'),'retained-followthrough'])==0
 assert step('installed',['python3',str(p/'installed.py')])==0
finally:step('pair-down',[pair,'down'])
raise SystemExit(0 if all(x['returncode']==0 for x in rows) else 1)
