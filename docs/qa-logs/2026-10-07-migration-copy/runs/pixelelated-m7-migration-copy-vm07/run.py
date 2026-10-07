from pathlib import Path
import hashlib,json,subprocess,time
R=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
O=Path('/workspace/tmp/pixelelated-m7-migration-copy-vm07');A=O/'artifacts'
P=Path('/workspace/tmp/pixelelated-m7-migration-copy-vm04'); C=Path('/workspace/tmp/pixelelated-m7-migration-copy-vm06')
KEY=P/'qa-key';DISK=P/'vm.qcow2';PID=P/'vm.pid';MON='/tmp/pix-copy04-mon.sock';SER='/tmp/pix-copy04-ser.sock'
OPTIONS=['-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','LogLevel=ERROR','-o','ConnectTimeout=8']
def run(a,**kw):return subprocess.run([str(v) for v in a],check=True,**kw)
def ssh(s):return run(['ssh','-i',KEY,'-p','10142',*OPTIONS,'root@127.0.0.1',s],capture_output=True,text=True,timeout=100).stdout
def scp(f,dst):run(['scp','-q','-i',KEY,'-P','10142',*OPTIONS,f,'root@127.0.0.1:'+dst])
def sha(p):return hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()
def mark(s):print(time.strftime('%FT%TZ',time.gmtime()),s,flush=True);(O/'stage').write_text(s+'\n')
def stop():
 if PID.exists():
  try:ssh('sync')
  finally:run([R/'tools/vm-stop',PID,DISK])
try:
 assert KEY.is_file() and DISK.is_file() and (C/'baseline-fr.mo').is_file() and (P/'emulationstation').is_file()
 for res,kind in [('640x480','baseline-source-fr'),('1280x800','changed-fr')]:
  mark('boot '+res+' '+kind)
  with open(A/(kind+'-qemu.log'),'w') as f:run([R/'projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm','run','--headless','--daemonize','--monitor',MON,'--serial',SER,'--pidfile',PID,'--vnc','45','--ssh-port','10142','--mac','52:54:00:50:50:42','--res',res,DISK],stdout=f,stderr=subprocess.STDOUT)
  run([R/'tools/vm-serial','--socket',SER,'wait','--up-to','300'])
  ssh('systemctl stop essway')
  if kind=='changed-fr':
   scp(P/'emulationstation','/storage/qa-copy/emulationstation')
   ssh('chmod 755 /storage/qa-copy/emulationstation; sync; mount --bind /storage/qa-copy/emulationstation /usr/bin/emulationstation')
  catalog=C/('baseline-fr.mo' if kind=='baseline-source-fr' else 'fr.mo')
  scp(catalog,'/storage/qa-copy/fr.mo')
  ssh('sync; mount --bind /storage/qa-copy/fr.mo /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo; . /etc/profile >/dev/null 2>&1; set_setting system.language fr_FR; rm -f /tmp/emulationstation.ready; : > /var/log/es_log.txt; sync; systemctl start essway')
  deadline=time.monotonic()+120
  while time.monotonic()<deadline:
   state=ssh("test -f /tmp/emulationstation.ready && curl -fsS --max-time 2 http://127.0.0.1:1234/isIdle && grep 'cloud folder: /ROCKNIX.*offering the move' /var/log/es_log.txt || true")
   if 'true' in state and 'offering the move' in state:break
   time.sleep(2)
  else:raise RuntimeError('prompt timeout')
  (A/(kind+'-prompt.log')).write_text(state)
  proof=ssh('sha256sum /usr/bin/emulationstation /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo /storage/qa-copy/cloud/ROCKNIX/Saves/gb/QA.srm; grep "^BUILD_ID=" /etc/os-release; grep -E "^(STATE|SOURCE|CURRENT)=" /storage/.cache/cloud_sync/scan/state; test ! -e /storage/qa-copy/cloud/pixelelated && echo QA_DESTINATION_ABSENT; . /etc/profile >/dev/null 2>&1; get_setting system.language')
  expected=sha(P/'emulationstation') if kind=='changed-fr' else 'f6bf7e0b71ce1491b59901a88af3cc49c2bb22117df6dca8bcbe651066263c94'
  assert expected in proof and sha(catalog) in proof and 'fr_FR' in proof and 'STATE=superseded-with-files' in proof and 'QA_DESTINATION_ABSENT' in proof
  (A/(kind+'-installed.log')).write_text(proof)
  steps=O/(kind+'.steps');steps.write_text('wake\nsettle 25 1.2\nshot prompt\nwait 5\nshot steady\n')
  run([R/'tools/vm-visual-qa','--monitor',MON,'run',steps,'--outdir',A/kind])
  ssh('systemctl stop essway; sync');stop()
 mark('PASS captures complete; direct inspection pending')
 (O/'result.json').write_text(json.dumps({'capture':'PASS','guest_stopped':True,'visual_acceptance':'PENDING'},indent=2)+'\n')
finally:stop()
