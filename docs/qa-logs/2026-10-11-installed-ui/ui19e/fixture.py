from pathlib import Path
import json,subprocess,os,time,hashlib
p=Path(__file__).resolve().parent
previous=Path('/workspace/tmp/pixelelated-m7-upgrade19c')
for name,digest in json.loads((p/'prepared-manifest.json').read_text())['files'].items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest
assert Path('/workspace/tmp/pixelelated-m7-installed19d/launcher-result.json').exists()
subprocess.run(['python3','/workspace/tmp/pixelelated-m7-build19/verify-source.py'],check=True)
env={**os.environ,'TMPDIR':str(p/'tmp'),'VM_PAIR_DIR':str(previous/'pair'),'VM_QEMU_RUNTIME_DIR':str(p/'runtime'),'CLOUD_QA_STATE':str(p/'cloud'),'CLOUD_QA_BACKEND':'webdav'}
pair='/workspace/repos/rocknix/tools/vm-pair';backend='/workspace/repos/rocknix/tools/cloud-test-backend'
rows=[]
def step(name,cmd):
 print('START',name,flush=True)
 with (p/(name+'.log')).open('w') as f:rc=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 rows.append({'step':name,'returncode':rc});(p/'result.json').write_text(json.dumps(rows,indent=2)+'\n');print('END',name,rc,flush=True);return rc
try:
 assert step('backend',[backend,'up'])==0
 assert step('boot-ui',['projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm','run','--headless','--daemonize','--monitor',str(p/'runtime/rocknix-qemu-monitor-b.sock'),'--serial',str(p/'runtime/rocknix-qemu-serial-b.sock'),'--pidfile',str(p/'runtime/rocknix-qemu-b.pid'),'--vnc','10','--ssh-port','10023','--mac','52:54:00:52:4E:59',str(previous/'pair/vm-b.qcow2')])==0
 for _ in range(90):
  ready=subprocess.run([pair,'ssh','b','systemctl is-active rocknix-autostart.service'],env=env,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,timeout=15)
  if ready.returncode==0 and ready.stdout.strip()=='active':break
  time.sleep(2)
 else:raise RuntimeError('guest storage not ready')
 (p/'ready.json').write_text(json.dumps({'state':'ready for actively supervised UI commands','port':10023,'source':'a0f60255abfefaddce772d0bba29977bafb7adab','disk':str(previous/'pair/vm-b.qcow2')},indent=2)+'\n')
 print('READY supervised UI fixture; no proof result inferred',flush=True)
 deadline=time.monotonic()+1800
 while not (p/'finish.json').exists():
  if time.monotonic()>deadline:raise RuntimeError('supervised UI fixture deadline reached')
  time.sleep(2)
 final=json.loads((p/'finish.json').read_text());assert final['commands_complete'] and final['result'] in ['PASS','FAIL']
 if final['result']!='PASS':raise RuntimeError('UI proof needs follow-through; preserving failure')
finally:
 step('pair-down',[pair,'down']);step('backend-down',[backend,'down'])
print('PASS fixture lifecycle and explicitly recorded UI command results',flush=True)
