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

PRIOR=O
O=Path('/workspace/tmp/pixelelated-m7-migration-copy-vm06');A=O/'artifacts'
try:
 for res,kind in [('640x480','baseline-source-fr'),('1280x800','changed-fr')]:
  mark('boot '+res+' '+kind)
  with open(A/(kind+'-qemu.log'),'w') as f:run([R/'projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm','run','--headless','--daemonize','--monitor',MON,'--serial',SER,'--pidfile',PID,'--vnc','45','--ssh-port','10142','--mac','52:54:00:50:50:42','--res',res,DISK],stdout=f,stderr=subprocess.STDOUT)
  run([R/'tools/vm-serial','--socket',SER,'wait','--up-to','300'])
  remote('systemctl stop essway')
  (A/(kind+'-prior-overlay.log')).write_text(remote('sha256sum /storage/qa-copy/emulationstation /storage/qa-copy/fr.mo; od -An -tx1 -N16 /storage/qa-copy/emulationstation'))
  if kind=='changed-fr':
   scp(PRIOR/'emulationstation','/storage/qa-copy/emulationstation')
   remote('chmod 755 /storage/qa-copy/emulationstation; sync; mount --bind /storage/qa-copy/emulationstation /usr/bin/emulationstation')
  scp(O/('baseline-fr.mo' if kind=='baseline-source-fr' else 'fr.mo'),'/storage/qa-copy/fr.mo')
  remote('sync; mount --bind /storage/qa-copy/fr.mo /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo; . /etc/profile >/dev/null 2>&1; set_setting system.language fr_FR; rm -f /tmp/emulationstation.ready; : > /var/log/es_log.txt; sync; systemctl start essway')
  (A/(kind+'-prompt.log')).write_text(wait_prompt())
  proof=remote('sha256sum /usr/bin/emulationstation /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo /storage/qa-copy/cloud/ROCKNIX/Saves/gb/QA.srm; grep "^BUILD_ID=" /etc/os-release; grep -E "^(STATE|SOURCE|CURRENT)=" /storage/.cache/cloud_sync/scan/state; test ! -e /storage/qa-copy/cloud/pixelelated && echo QA_DESTINATION_ABSENT; . /etc/profile >/dev/null 2>&1; get_setting system.language')
  expected=sha(PRIOR/'emulationstation') if kind=='changed-fr' else 'f6bf7e0b71ce1491b59901a88af3cc49c2bb22117df6dca8bcbe651066263c94'
  assert expected in proof and 'fr_FR' in proof and 'STATE=superseded-with-files' in proof and 'QA_DESTINATION_ABSENT' in proof
  (A/(kind+'-installed.log')).write_text(proof)
  steps=O/(kind+'.steps');steps.write_text('wake\nsettle 25 1.2\nshot prompt\nwait 5\nshot steady\n')
  run([R/'tools/vm-visual-qa','--monitor',MON,'run',steps,'--outdir',A/kind])
  remote('systemctl stop essway; sync')
  stop()
 mark('PASS narrow recapture complete; direct visual acceptance pending')
 (O/'result.json').write_text(json.dumps({'capture':'PASS','guest_stopped':True,'visual_acceptance':'PENDING'},indent=2)+'\n')
finally:
 if PID.exists():stop()
