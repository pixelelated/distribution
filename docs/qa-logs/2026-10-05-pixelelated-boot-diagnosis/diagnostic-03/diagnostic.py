from pathlib import Path
import array,datetime,hashlib,importlib.machinery,json,os,shlex,subprocess,time
owner=Path(__file__).parent;out=owner/'artifacts';backing=Path('/workspace/tmp/pixelelated-m7-ui-07/guest-d.qcow2');disk=owner/'guest-d.qcow2'
vm='./projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm';monpath='/tmp/rocknix-qemu-monitor-d.sock';serial='/tmp/rocknix-qemu-serial-d.sock'
ssh=['ssh','-i','/workspace/tmp/pixelelated-m7-ui-07/pair/qa-key','-p','10026','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1']
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
 return h.hexdigest()
def save(name,value):(out/name).write_text(json.dumps(value,indent=2)+'\n')
def run(args,**kw):return subprocess.run(args,check=True,**kw)
def guest(cmd,stdin=None):return subprocess.check_output(ssh+[cmd],input=stdin,text=True,timeout=45)
pid=None;observed=[];results={};original=sha(backing)
save('backing-before.json',{'path':str(backing),'sha256':original})
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try:name=Path(p.read_bytes().split(b'\0',1)[0].decode()).name
 except (OSError,UnicodeError):continue
 assert not name.startswith('qemu-system-'),'Existing guest refuses diagnostic'
run(['qemu-img','create','-f','qcow2','-F','qcow2','-b',str(backing),str(disk)])
def stop():
 global pid
 if pid is not None:run(['python3',str(owner/'stop-guest.py'),str(pid),str(disk)]);pid=None
def match(folder,size):
 dest=out/(folder.name+'-match')
 r=subprocess.run(['python3',str(owner/'match-splash.py'),'--frames',str(folder),'--reference',str(owner/f'reference-{size}.png'),'--old-logo',str(owner/'old-logo.png'),'--output',str(dest)])
 assert r.returncode in (0,1)
 d=json.loads((dest/'result.json').read_text());assert d['threshold']==.995 and all(x['rejected']for x in d['controls'])
 return {'matcher_rc':r.returncode,'best':d['best'],'pass':d['pass']}
def boot(name,res,capture=True):
 global pid
 args=['--headless','--gl','auto','--res',res,'--monitor',monpath,'--serial',serial,'--pidfile','/tmp/rocknix-qemu-d.pid','--vnc','12','--ssh-port','10026','--mac','52:54:00:52:4E:5B',str(disk)]
 with (out/(name+'-qemu.json')).open('w') as f:run([vm,'qemu-args',*args],stdout=f)
 run([vm,'run','--daemonize',*args]);pid=int(Path('/tmp/rocknix-qemu-d.pid').read_text());observed.append(pid);(owner/'guest.pid').write_text(str(pid)+'\n');save('owned-pids.json',observed)
 if capture:run(['python3',str(owner/'capture-boot.py'),'--monitor',monpath,'--output',str(out/name),'--seconds','40'])
 run(['./tools/vm-serial','--socket',serial,'wait','--up-to','180'])
 for _ in range(30):
  try:
   bid=guest('sed -n "s/^BUILD_ID=//p" /etc/os-release').strip().strip('"');assert bid=='57cbc9b981205328444d41f6c4237dc9f5736d7f';break
  except subprocess.CalledProcessError:time.sleep(1)
 else:raise RuntimeError('guest failed SSH readiness')
 cmdline=guest('cat /proc/cmdline');(out/(name+'-cmdline.txt')).write_text(cmdline)
 (out/(name+'-console.txt')).write_text(guest('cat /proc/sys/kernel/printk; cat /sys/class/tty/tty0/active; cat /sys/class/graphics/fb0/name; cat /sys/class/graphics/fb0/virtual_size; cat /sys/class/graphics/fb0/bits_per_pixel'))
 (out/(name+'-kernel.log')).write_text(guest('journalctl -k -b --no-pager | grep -v -i -E "key|pass|token|user|psk"'))
 if capture:results[name]=match(out/name,res.split('x')[0]);save('results-in-progress.json',results)
 return cmdline
try:
 cmdline=boot('setup-640','640x480',False)
 assert 'portable' in cmdline.split() and 'quiet' not in cmdline.split(),cmdline
 cfgs=guest('find /flash -name grub.cfg').splitlines();assert len(cfgs)==1,cfgs
 assert cfgs[0].startswith('/flash/')
 save('boot-config-paths.json',{'syslinux':'/flash/syslinux.cfg','grub':cfgs[0]})
 for cfg,prefix in [('/flash/syslinux.cfg','APPEND '),(cfgs[0],'linux ')]:
  original_cfg=guest('cat '+shlex.quote(cfg));(out/(Path(cfg).stem+'-original.cfg')).write_text(original_cfg)
  lines=original_cfg.splitlines(keepends=True);count=0
  for i,line in enumerate(lines):
   if line.lstrip().startswith(prefix):
    assert 'quiet' not in line.split();lines[i]=line.rstrip('\n')+' quiet\n';count+=1
  assert count==1,(cfg,count)
  modified_cfg=''.join(lines);guest('mount -o remount,rw /flash; cat > '+shlex.quote(cfg)+'; sync',modified_cfg)
  assert guest('cat '+shlex.quote(cfg))==modified_cfg
  (out/(Path(cfg).stem+'-quiet.cfg')).write_text(modified_cfg)
 guest('sync');stop()
 for name,res in [('quiet-640','640x480'),('quiet-1280','1280x960')]:
  cmdline=boot(name,res)
  assert all(x in cmdline.split() for x in ['quiet','portable','console=ttyS0,115200','console=tty0']),cmdline
  guest('sync');stop()
 save('diagnostic-summary.json',{'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'two predeclared quiet boot observations after asserting actual BIOS/Syslinux boot; COW config only','results':results,'not_candidate_acceptance':True})
 print('COMPLETE bounded quiet-boot observations; inspect evidence before selecting a fix',flush=True)
finally:
 stop();after=sha(backing);save('backing-after.json',{'path':str(backing),'sha256':after,'unchanged':after==original});assert after==original
