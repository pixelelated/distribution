from pathlib import Path
import hashlib,json,subprocess,time,datetime
owner=Path(__file__).parent;out=owner/'artifacts';backing=Path('/workspace/tmp/pixelelated-m7-qa-09/pair/vm-a.qcow2');vm='./projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm';mon='/tmp/rocknix-qemu-monitor-d.sock';serial='/tmp/rocknix-qemu-serial-d.sock';pid=None;disk=None;pids=[]
ssh=['ssh','-i','/workspace/tmp/pixelelated-m7-qa-09/pair/qa-key','-p','10026','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1']
def run(a,**kw):return subprocess.run(a,check=True,**kw)
def guest(c):return subprocess.check_output(ssh+[c],text=True,timeout=40)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def stop():
 global pid
 if pid is not None:run(['python3',str(owner/'stop-guest.py'),str(pid),str(disk)]);pid=None
original=sha(backing);(out/'backing-before.json').write_text(json.dumps({'path':str(backing),'sha256':original}))
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try:n=Path(p.read_bytes().split(b'\0',1)[0].decode()).name
 except (OSError,UnicodeError):continue
 assert not n.startswith('qemu-system-'),p
try:
 for phase in ['back-transitions','close-reopen']:
  disk=owner/(phase+'.qcow2');run(['qemu-img','create','-f','qcow2','-F','qcow2','-b',str(backing),str(disk)])
  run([vm,'run','--headless','--daemonize','--res','1280x800','--monitor',mon,'--serial',serial,'--pidfile','/tmp/rocknix-qemu-d.pid','--vnc','12','--ssh-port','10026','--mac','52:54:00:52:4E:5B',str(disk)])
  pid=int(Path('/tmp/rocknix-qemu-d.pid').read_text());pids.append(pid);(owner/'guest.pid').write_text(str(pid)+'\n');(out/'owned-pids.json').write_text(json.dumps(pids))
  run(['./tools/vm-serial','--socket',serial,'wait','--up-to','300'])
  for _ in range(60):
   try:
    if json.loads(guest('curl -sS -m 3 http://127.0.0.1:1234/isIdle'))==[True]:break
   except (subprocess.CalledProcessError,ValueError):pass
   time.sleep(1)
  else:raise RuntimeError('ES idle readiness failed')
  bid=guest('sed -n "s/^BUILD_ID=//p" /etc/os-release').strip().strip('"');assert bid=='a2586374b7b565965fe0c644656e22ff3c0ec317'
  facts=". /etc/profile >/dev/null 2>&1; get_setting system.language; sed -n '/inputConfig type=.keyboard/,/<.inputConfig>/p' /storage/.config/emulationstation/es_input.cfg"
  (out/(phase+'-before.txt')).write_text(guest(facts))
  run(['./tools/vm-visual-qa','--monitor',mon,'dismiss'])
  run(['./tools/vm-visual-qa','--monitor',mon,'run',str(owner/(phase+'.steps')),'--outdir',str(out/phase)])
  (out/(phase+'-after.txt')).write_text(guest(facts));guest('sync');stop()
 print('COMPLETE bounded menu captures; semantic review still required',flush=True)
finally:
 stop();after=sha(backing);(out/'backing-after.json').write_text(json.dumps({'sha256':after,'unchanged':after==original}));assert after==original
