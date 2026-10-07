from pathlib import Path
import gzip,hashlib,json,os,shlex,shutil,subprocess,time
O=Path('/workspace/tmp/pixelelated-m7-migration-copy-vm04');A=O/'artifacts';R=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
IMAGE=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/target/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz')
DISK=O/'vm.qcow2';PID=O/'vm.pid';SER='/tmp/pix-copy04-ser.sock';MON='/tmp/pix-copy04-mon.sock'
SSH=['ssh','-i',str(O/'qa-key'),'-p','10142','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','LogLevel=ERROR','-o','ConnectTimeout=8','root@127.0.0.1']
def mark(s):print(time.strftime('%FT%TZ',time.gmtime()),s,flush=True);(O/'stage').write_text(s+'\n')
def run(args,**kw):return subprocess.run([str(a) for a in args],check=True,**kw)
def remote(cmd):return run(SSH+[cmd],capture_output=True,text=True,timeout=100).stdout
def sha(p):return hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()
def ready():
 run([R/'tools/vm-serial','--socket',SER,'wait','--up-to','300'])
 pub=(O/'qa-key.pub').read_text().strip()
 run([R/'tools/vm-serial','--socket',SER,'sh',"mkdir -p /storage/.ssh && chmod 700 /storage/.ssh && printf '%s\\n' "+shlex.quote(pub)+" > /storage/.ssh/authorized_keys && chmod 600 /storage/.ssh/authorized_keys"],stdout=subprocess.DEVNULL)
 deadline=time.monotonic()+180
 while time.monotonic()<deadline:
  try:
   if 'PIX_COPY_READY' in remote('printf PIX_COPY_READY'):return
  except (subprocess.SubprocessError,OSError):pass
  time.sleep(2)
 raise RuntimeError('SSH readiness timeout')
def scp(src,dst):run(['scp','-q','-i',O/'qa-key','-P','10142','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','LogLevel=ERROR',src,'root@127.0.0.1:'+dst])
def stop():run([R/'tools/vm-stop',PID,DISK])
def wait_prompt():
 deadline=time.monotonic()+120
 while time.monotonic()<deadline:
  s=remote("test -f /tmp/emulationstation.ready && curl -fsS --max-time 2 http://127.0.0.1:1234/isIdle && grep 'cloud folder: /ROCKNIX.*offering the move' /var/log/es_log.txt || true")
  if 'true' in s and 'offering the move' in s:return s
  time.sleep(2)
 raise RuntimeError('migration prompt did not arrive')
try:
 mark('verify image and create one disposable guest')
 assert sha(IMAGE)=='74e57ad8957b1c719c18db098d5713577a952af8802524658d0ada7dee1b6b12'
 with gzip.open(IMAGE,'rb') as src,open(O/'image.img','wb') as dst:shutil.copyfileobj(src,dst,8*1024*1024)
 run(['qemu-img','convert','-f','raw','-O','qcow2',O/'image.img',DISK]);run(['qemu-img','resize',DISK,'16G']);(O/'image.img').unlink()
 run(['ssh-keygen','-q','-t','ed25519','-N','','-f',O/'qa-key','-C','migration-copy-qa'])
 for res in ['640x480','1280x800']:
  mark('boot '+res)
  with open(A/('qemu-'+res+'.log'),'w') as f:run([R/'projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm','run','--headless','--daemonize','--monitor',MON,'--serial',SER,'--pidfile',PID,'--vnc','45','--ssh-port','10142','--mac','52:54:00:50:50:42','--res',res,DISK],stdout=f,stderr=subprocess.STDOUT)
  pid=int(PID.read_text());(A/('qemu-'+res+'.argv')).write_bytes(Path('/proc',str(pid),'cmdline').read_bytes())
  ready()
  remote('systemctl stop essway; mkdir -p /storage/qa-copy /storage/.config/rclone')
  scp(O/'emulationstation','/storage/qa-copy/emulationstation');scp(O/'fr.mo','/storage/qa-copy/fr.mo')
  remote('chmod 755 /storage/qa-copy/emulationstation; mount --bind /storage/qa-copy/emulationstation /usr/bin/emulationstation; mount --bind /storage/qa-copy/fr.mo /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo')
  scp(O/'setup.sh','/storage/qa-copy/setup.sh')
  out=remote('sh /storage/qa-copy/setup.sh');(A/('fixture-'+res+'.log')).write_text(out)
  for lang in ['en_US','fr_FR']:
   tag=res+'-'+lang;mark('render '+tag)
   remote("systemctl stop essway; . /etc/profile >/dev/null 2>&1; set_setting system.language "+lang+"; rm -f /tmp/emulationstation.ready; : > /var/log/es_log.txt; systemctl start essway")
   (A/(tag+'-prompt.log')).write_text(wait_prompt())
   # A real settled frame, followed by a second one to detect scrolling.
   steps=O/(tag+'.steps');steps.write_text('settle 25 1.2\nshot prompt\nwait 5\nshot steady\n')
   run([R/'tools/vm-visual-qa','--monitor',MON,'run',steps,'--outdir',A/tag])
   proof=remote("sha256sum /usr/bin/emulationstation /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo /storage/qa-copy/cloud/ROCKNIX/Saves/gb/QA.srm; grep '^BUILD_ID=' /etc/os-release; grep -E '^(STATE|SAVES|SOURCE|CURRENT)=' /storage/.cache/cloud_sync/scan/state; test ! -e /storage/qa-copy/cloud/pixelelated && echo QA_DESTINATION_ABSENT; pgrep emulationstation | while read p; do readlink /proc/$p/exe; done")
   assert sha(O/'emulationstation') in proof and 'STATE=superseded-with-files' in proof and 'QA_DESTINATION_ABSENT' in proof
   (A/(tag+'-installed.log')).write_text(proof)
   steps2=O/(tag+'-dismiss.steps');steps2.write_text('key z\nwait-for-change 12 0\nsettle\nshot dismissed\n')
   run([R/'tools/vm-visual-qa','--monitor',MON,'run',steps2,'--outdir',A/(tag+'-dismiss')])
   assert 'QA_SOURCE_UNCHANGED' in remote('test -f /storage/qa-copy/cloud/ROCKNIX/Saves/gb/QA.srm && test ! -e /storage/qa-copy/cloud/pixelelated && echo QA_SOURCE_UNCHANGED')
  stop()
 mark('PASS capture matrix; direct frame inspection pending')
 (O/'result.json').write_text(json.dumps({'capture':'PASS','resolutions':['640x480','1280x800'],'languages':['en_US','fr_FR'],'guest_stopped':True,'visual_acceptance':'PENDING'},indent=2)+'\n')
except BaseException:
 mark('FAILED; preserving compact failure evidence')
 raise
finally:
 if PID.exists():stop()
