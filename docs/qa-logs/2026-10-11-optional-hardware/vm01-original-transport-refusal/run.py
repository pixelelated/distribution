from pathlib import Path
import subprocess,os,time,json,hashlib
P=Path(__file__).resolve().parent;R=Path('/workspace/repos/rocknix');PRE=Path('/workspace/tmp/pixelelated-m7-startup19g')
for d in ['runtime','tmp','artifacts']:(P/d).mkdir()
env={**os.environ,'TMPDIR':str(P/'tmp'),'VM_PAIR_DIR':str(PRE/'pair'),'VM_QEMU_RUNTIME_DIR':str(P/'runtime')};mon=P/'runtime/rocknix-qemu-monitor.sock'
rows=[]
def step(name,args):
 print('START',name,flush=True)
 with (P/(name+'.log')).open('w') as f:r=subprocess.run(args,env=env,stdout=f,stderr=subprocess.STDOUT)
 rows.append({'step':name,'returncode':r.returncode});(P/'result.json').write_text(json.dumps(rows,indent=2)+'\n');print('END',name,r.returncode,flush=True);return r.returncode
def guest(cmd):return subprocess.check_output([str(R/'tools/vm-pair'),'ssh','a',cmd],env=env,text=True,timeout=90).strip()
def sample(tag):
 r=subprocess.run([str(R/'tools/vm-pair'),'ssh','a','/usr/bin/rocknix-info'],env=env,text=True,capture_output=True,timeout=60)
 (P/'artifacts'/(tag+'-script.json')).write_text(json.dumps({'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr},indent=2)+'\n');return r
steps=(R/'docs/qa-logs/2026-10-09-build-identity/ui01-failed-harness/information.steps').read_text()+'key down x14\nwait-for-change 30 0\nsettle\nshot cpu-information\n'
(P/'information.steps').write_text(steps)
def frames(tag):
 guest("systemctl stop essway; . /etc/profile >/dev/null 2>&1; set_setting system.language en_US; rm -f /tmp/emulationstation.ready; systemctl start essway")
 for _ in range(60):
  if guest('test -f /tmp/emulationstation.ready && echo yes || true')=='yes':break
  time.sleep(.3)
 else:raise RuntimeError('frontend not ready')
 assert step(tag+'-frames',[str(R/'tools/vm-visual-qa'),'--monitor',str(mon),'run',str(P/'information.steps'),'--outdir',str(P/'artifacts'/tag)])==0
mounted=False
try:
 assert step('boot',[str(R/'projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm'),'run','--headless','--daemonize','--monitor',str(mon),'--serial',str(P/'runtime/rocknix-qemu-serial.sock'),'--pidfile',str(P/'runtime/rocknix-qemu.pid'),'--vnc','9','--ssh-port','10022',str(PRE/'pair/vm-a.qcow2')])==0
 assert step('serial-ready',[str(R/'tools/vm-pair'),'serial','a','true'])==0
 for _ in range(60):
  try:
   if guest('systemctl is-active rocknix-autostart')=='active':break
  except subprocess.CalledProcessError:pass
  time.sleep(1)
 else:raise RuntimeError('storage/SSH unavailable')
 guest("swaymsg -s /run/0-runtime-dir/sway-ipc.0.sock 'output Virtual-1 mode --custom 640x480@60Hz'")
 old=sample('original');assert old.returncode!=0 and 'arithmetic syntax error' in old.stderr
 original_hash=guest('sha256sum /usr/bin/rocknix-info').split()[0]
 frames('original')
 assert step('copy-script',[str(R/'tools/vm-pair'),'scp','a',str(P/'rocknix-info'),'/storage/qa548-rocknix-info'])==0
 guest('chmod 755 /storage/qa548-rocknix-info; mount --bind /storage/qa548-rocknix-info /usr/bin/rocknix-info');mounted=True
 new_hash=guest('sha256sum /usr/bin/rocknix-info').split()[0];assert new_hash==hashlib.sha256((P/'rocknix-info').read_bytes()).hexdigest()
 fixed=sample('fixed');assert fixed.returncode==0 and not fixed.stderr and 'CPU CURRENT FREQUENCY: Not Available' in fixed.stdout and 'CPU MAXIMUM FREQUENCY: Not Available' in fixed.stdout
 frames('fixed')
 (P/'artifacts/bindings.json').write_text(json.dumps({'distribution':'a0f60255abfefaddce772d0bba29977bafb7adab','es':'c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78','overlay':'rocknix-info only','original_sha256':original_hash,'corrected_sha256':new_hash,'width':640,'height':480,'locale':'en_US'},indent=2)+'\n')
 print('PASS actual original failure and corrected quiet success; frames require review',flush=True)
finally:
 if mounted:
  guest('umount /usr/bin/rocknix-info; rm /storage/qa548-rocknix-info')
  assert guest('sha256sum /usr/bin/rocknix-info').split()[0]==original_hash
 step('pair-down',[str(R/'tools/vm-pair'),'down'])
