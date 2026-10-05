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
def boot(name,res):
 global pid
 args=['--headless','--gl','auto','--res',res,'--monitor',monpath,'--serial',serial,'--pidfile','/tmp/rocknix-qemu-d.pid','--vnc','12','--ssh-port','10026','--mac','52:54:00:52:4E:5B',str(disk)]
 with (out/(name+'-qemu.json')).open('w') as f:run([vm,'qemu-args',*args],stdout=f)
 run([vm,'run','--daemonize',*args]);pid=int(Path('/tmp/rocknix-qemu-d.pid').read_text());observed.append(pid);(owner/'guest.pid').write_text(str(pid)+'\n');save('owned-pids.json',observed)
 run(['python3',str(owner/'capture-boot.py'),'--monitor',monpath,'--output',str(out/name),'--seconds','40'])
 run(['./tools/vm-serial','--socket',serial,'wait','--up-to','180'])
 for _ in range(30):
  try:
   bid=guest('sed -n "s/^BUILD_ID=//p" /etc/os-release').strip().strip('"');assert bid=='57cbc9b981205328444d41f6c4237dc9f5736d7f';break
  except subprocess.CalledProcessError:time.sleep(1)
 else:raise RuntimeError('guest failed SSH readiness')
 cmdline=guest('cat /proc/cmdline');(out/(name+'-cmdline.txt')).write_text(cmdline)
 (out/(name+'-console.txt')).write_text(guest('cat /proc/sys/kernel/printk; cat /sys/class/tty/tty0/active; cat /sys/class/graphics/fb0/name; cat /sys/class/graphics/fb0/virtual_size; cat /sys/class/graphics/fb0/bits_per_pixel'))
 (out/(name+'-kernel.log')).write_text(guest('journalctl -k -b --no-pager | grep -v -i -E "key|pass|token|user|psk"'))
 results[name]=match(out/name,res.split('x')[0]);save('results-in-progress.json',results);return cmdline
def shot(name):
 folder=out/name;folder.mkdir();p=folder/'000.png';run(['./tools/vm-visual-qa','--monitor',monpath,'shot',str(p)])
 (folder/'captures.json').write_text(json.dumps({'scope':'controlled framebuffer/console diagnostic, not boot qualification','frames':[{'file':p.name,'elapsed_seconds':0,'sha256':sha(p)}]},indent=2)+'\n');results[name]=match(folder,'640');save('results-in-progress.json',results)
try:
 cmdline=boot('original-640','640x480');assert 'quiet' not in cmdline.split(),cmdline
 cfgs=guest('find /flash -name grub.cfg').splitlines();assert len(cfgs)==1,cfgs;cfg=cfgs[0];assert cfg.startswith('/flash/')
 oldcfg=guest('cat '+shlex.quote(cfg));(out/'grub-original.cfg').write_text(oldcfg)
 oldprintk=guest('cat /proc/sys/kernel/printk').strip()
 guest('systemctl stop essway; chvt 1; dmesg -n 1')
 payload=(owner/'consumed-init-splash').read_bytes();subprocess.run(ssh+['cat > /tmp/qa-splash && chmod 700 /tmp/qa-splash'],input=payload,check=True,timeout=30)
 assert guest('sha256sum /tmp/qa-splash').split()[0]==sha(owner/'consumed-init-splash')
 def mode(n):guest("python3 -c 'import os,fcntl; fd=os.open(\"/dev/tty1\",os.O_RDWR); fcntl.ioctl(fd,0x4b3a,"+str(n)+"); os.close(fd)'")
 mode(0);guest("printf '\033[2J\033[H\033[?25l' >/dev/tty1; /tmp/qa-splash");shot('text-mode-drawn')
 guest("printf '\033[19;1H\033[2K' >/dev/tty1");shot('text-mode-erased-line')
 mode(1);guest('/tmp/qa-splash');shot('graphics-mode-drawn')
 guest("printf '\033[19;1H\033[2K' >/dev/tty1");shot('graphics-mode-console-write')
 mode(0);guest('printf %s '+shlex.quote(oldprintk)+' > /proc/sys/kernel/printk')
 # Change the disposable COW boot config only; retain exact before/after.
 lines=oldcfg.splitlines(keepends=True);count=0
 for i,line in enumerate(lines):
  if line.lstrip().startswith('linux '):
   assert 'quiet' not in line.split();lines[i]=line.rstrip('\n')+' quiet\n';count+=1
 assert count==1;newcfg=''.join(lines);guest('mount -o remount,rw /flash; cat > '+shlex.quote(cfg)+'; sync',newcfg)
 assert guest('cat '+shlex.quote(cfg))==newcfg;(out/'grub-quiet.cfg').write_text(newcfg)
 guest('sync');stop()
 for name,res in [('quiet-640','640x480'),('quiet-1280','1280x960')]:
  cmdline=boot(name,res);assert 'quiet' in cmdline.split();guest('sync');stop()
 save('diagnostic-summary.json',{'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'three predeclared boot observations plus text/graphics-mode controls; COW config modification only','results':results,'not_candidate_acceptance':True})
 print('COMPLETE bounded boot/console observations; inspect evidence before selecting a fix',flush=True)
finally:
 stop();after=sha(backing);save('backing-after.json',{'path':str(backing),'sha256':after,'unchanged':after==original});assert after==original
