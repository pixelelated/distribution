"""Four predeclared clean/actual-RC2-upgrade boots; no product or boot edits."""
from pathlib import Path
import datetime,gzip,hashlib,json,os,shutil,subprocess,sys,tarfile
owner=Path(__file__).parent;out=owner/'artifacts';bundle=Path(sys.argv[1]);frozen=Path('/workspace/tmp/pixelelated-m7-replacement-09');inputs=json.loads((frozen/'inputs.json').read_text());commit=inputs['distribution_commit'];qa=Path('/workspace/tmp/pixelelated-m7-qa-11');backing=qa/'pair/vm-a.qcow2'
assert (qa/'outer.rc').read_text().strip()=='0'
assert json.loads((qa/'completion.json').read_text())['actual_tool_rc']==0
vm='./projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm';mon='/tmp/rocknix-qemu-monitor-d.sock';serial='/tmp/rocknix-qemu-serial-d.sock'
def run(args,**kw):return subprocess.run(args,check=True,**kw)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def save(name,value):(out/name).write_text(json.dumps(value,indent=2)+'\n')
def guest(cmd):return subprocess.check_output(['./tools/vm-serial','--socket',serial,'sh',cmd],text=True,timeout=75).strip()
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try:n=Path(p.read_bytes().split(b'\0',1)[0].decode()).name
 except (OSError,UnicodeError):continue
 assert not n.startswith('qemu-system-'),'existing guest '+p.parent.name
original=sha(backing);save('backing-before.json',{'path':str(backing),'sha256':original})
with tarfile.open(bundle/'pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.tar') as archive:
 members=[m for m in archive if m.isfile() and m.name.endswith('/target/KERNEL')];assert len(members)==1,[m.name for m in members]
 h=hashlib.sha256();f=archive.extractfile(members[0])
 for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 kernel_sha=h.hexdigest();save('expected-kernel.json',{'member':members[0].name,'sha256':kernel_sha})
raw=owner/'clean-image.img';base=owner/'clean-base.qcow2'
assert not raw.exists() and not base.exists()
with gzip.open(bundle/'pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz','rb') as src,raw.open('xb') as dst:shutil.copyfileobj(src,dst,8*1024*1024)
run(['qemu-img','convert','-f','raw','-O','qcow2',str(raw),str(base)]);run(['qemu-img','resize',str(base),'16G']);raw.unlink()
base_hash=sha(base);pid=None;disk=None;pids=[];results={}
def stop():
 global pid
 if pid is not None:run(['python3',str(owner/'stop-guest.py'),str(pid),str(disk)]);pid=None
try:
 for phase in ['clean','upgrade']:
  for res in ['640x480','1280x960']:
   name=phase+'-'+res.split('x')[0];disk=owner/(name+'.qcow2');run(['qemu-img','create','-f','qcow2','-F','qcow2','-b',str(base if phase=='clean' else backing),str(disk)])
   args=['--headless','--gl','auto','--res',res,'--monitor',mon,'--serial',serial,'--pidfile','/tmp/rocknix-qemu-d.pid','--vnc','12','--ssh-port','10026','--mac','52:54:00:52:4E:5B',str(disk)]
   with (out/(name+'-qemu.json')).open('w') as f:run([vm,'qemu-args',*args],stdout=f)
   run([vm,'run','--daemonize',*args]);pid=int(Path('/tmp/rocknix-qemu-d.pid').read_text());pids.append(pid);(owner/'guest.pid').write_text(str(pid)+'\n');save('owned-pids.json',pids)
   run(['python3',str(owner/'capture-boot.py'),'--monitor',mon,'--output',str(out/name),'--seconds','60' if phase=='clean' else '40'])
   run(['./tools/vm-serial','--socket',serial,'wait','--up-to','300'])
   bid=guest("sed -n 's/^BUILD_ID=//p' /etc/os-release").strip('"');assert bid==commit,(name,bid)
   cmdline=guest('cat /proc/cmdline');(out/(name+'-cmdline.txt')).write_text(cmdline+'\n');words=cmdline.split()
   assert 'console=ttyS0,115200' in words and 'console=tty0' in words,(name,cmdline)
   assert ('quiet' in words)==(phase=='clean'),(name,cmdline)
   actual_kernel=guest('sha256sum /flash/KERNEL').split()[0];assert actual_kernel==kernel_sha,(name,actual_kernel)
   (out/(name+'-console.txt')).write_text(guest('cat /proc/sys/kernel/printk; cat /sys/class/tty/tty0/active; cat /sys/class/graphics/fb0/name; cat /sys/class/graphics/fb0/virtual_size; cat /sys/class/graphics/fb0/bits_per_pixel')+'\n')
   (out/(name+'-kernel.log')).write_text(guest('journalctl -k -b --no-pager | grep -v -i -E "key|pass|token|user|psk"')+'\n')
   guest('sync');stop()
   dest=out/(name+'-match');r=subprocess.run(['python3',str(owner/'match-splash.py'),'--frames',str(out/name),'--reference',str(owner/('reference-'+res.split('x')[0]+'.png')),'--old-logo',str(owner/'old-logo.png'),'--output',str(dest)])
   assert r.returncode in (0,1),r.returncode
   d=json.loads((dest/'result.json').read_text());assert d['threshold']==.995 and len(d['controls'])==3 and all(c['rejected'] for c in d['controls'])
   results[name]={'passed':d['pass'],'matcher_rc':r.returncode,'best':d['best'],'build_id':bid,'kernel_sha256':actual_kernel,'quiet':('quiet' in words)};save('results-in-progress.json',results)
 save('qualification.json',{'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'first boot of two clean16GiB disks and two COW boots of actualRC2-upgraded disk; no boot config/product edits','results':results,'passed':all(r['passed'] for r in results.values())})
 assert len(results)==4 and all(r['passed'] for r in results.values()),results
 print('PASS four actual candidate clean/upgrade boots with unchanged splash threshold and controls',flush=True)
finally:
 stop();after=sha(backing);save('backing-after.json',{'path':str(backing),'sha256':after,'unchanged':after==original,'clean_base_unchanged':sha(base)==base_hash});assert after==original and sha(base)==base_hash
