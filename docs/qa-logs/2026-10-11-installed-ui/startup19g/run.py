from pathlib import Path
import subprocess,os,json,time,hashlib,socket
P=Path(__file__).resolve().parent;R=Path('/workspace/repos/rocknix')
for d in ['runtime','pair','tmp','artifacts']:(P/d).mkdir()
env={**os.environ,'TMPDIR':str(P/'tmp'),'VM_PAIR_DIR':str(P/'pair'),'VM_QEMU_RUNTIME_DIR':str(P/'runtime')}
image=next(Path('/workspace/artifacts/pixelelated-candidates/sha256/ee8e263c2e63b7fc79a458e9e89b0f4a3c393487377a6a820c7f7166dada1662').glob('*.img.gz'))
for port in [10022,5909]:
 s=socket.socket();s.bind(('127.0.0.1',port));s.close()
rows=[]
def run(name,args):
 print('START',name,flush=True)
 with (P/(name+'.log')).open('w') as f:r=subprocess.run(args,env=env,stdout=f,stderr=subprocess.STDOUT)
 rows.append({'step':name,'returncode':r.returncode});(P/'result.json').write_text(json.dumps(rows,indent=2)+'\n');print('END',name,r.returncode,flush=True);return r.returncode
def guest(cmd):return subprocess.check_output([str(R/'tools/vm-pair'),'ssh','a',cmd],env=env,text=True,timeout=60).strip()
try:
 assert run('clean-boot',[str(R/'tools/vm-pair'),'reimage','a',str(image)])==0
 for _ in range(90):
  if guest('test -f /tmp/emulationstation.ready && systemctl is-active rocknix-autostart')=='active':break
  time.sleep(.2)
 else:raise RuntimeError('frontend/storage not ready')
 identity=guest('cat /etc/os-release');assert 'a0f60255abfefaddce772d0bba29977bafb7adab' in identity
 unit=guest('systemctl show essway -p NRestarts -p ExecMainStatus -p ActiveState -p SubState -p ExecMainStartTimestampMonotonic')
 assert 'NRestarts=0' in unit and 'ActiveState=active' in unit and 'SubState=running' in unit
 journal=guest("journalctl -b -u essway -u sway --no-pager -o short-monotonic | grep -v -i -E 'key|pass|token|user|psk'")
 assert 'Started essway.service' in journal and 'Starting essway.service' in journal
 assert 'Scheduled restart job' not in journal and 'wayland not available' not in journal.lower() and 'Failed to start' not in journal
 files={}
 for path in ['/usr/bin/emulationstation','/usr/bin/sway-ready','/usr/lib/systemd/system/essway.service']:
  expected=hashlib.sha256((Path('/workspace/tmp/pixelelated-m7-image19/root')/path.lstrip('/')).read_bytes()).hexdigest()
  actual=guest('sha256sum '+path).split()[0];assert actual==expected;files[path]=actual
 for name,value in [('identity.txt',identity),('unit.txt',unit),('journal.txt',journal)]: (P/'artifacts'/name).write_text(value+'\n')
 (P/'artifacts/source-bindings.json').write_text(json.dumps(files,indent=2)+'\n')
 (P/'startup.steps').write_text('wake\ndismiss-dialogs\nsettle\nshot clean-startup\n')
 assert run('frame',[str(R/'tools/vm-visual-qa'),'--monitor',str(P/'runtime/rocknix-qemu-monitor.sock'),'run',str(P/'startup.steps'),'--outdir',str(P/'artifacts/frame')])==0
 print('PASS fresh installed startup with positive journal, zero restarts, exact helper/unit/ES; frame review pending',flush=True)
finally:
 run('pair-down',[str(R/'tools/vm-pair'),'down'])
