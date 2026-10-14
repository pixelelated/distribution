from pathlib import Path
import json,hashlib,subprocess,time,shutil,os
r=Path('/tmp/pix-output');s=Path('/tmp/pix-input');result={'rc':1,'started':time.time()}
def run(a):return subprocess.run(a,capture_output=True,text=True,check=True,timeout=20).stdout
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
try:
 run(['systemctl','stop','essway.service']);run(['umount','/usr/bin/emulationstation'])
 target=r/'emulationstation';shutil.copyfile(s/'emulationstation',target);target.chmod(0o755)
 expected='8752b5391ea8728c1a088d0a80e3776469692dda665e8f07f062fed3206263d2';assert sha(target)==expected and os.access(target,os.X_OK)
 run(['mount','--bind',str(target),'/usr/bin/emulationstation']);run(['mount','--make-private','/usr/bin/emulationstation'])
 catalog=Path('/usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo');assert catalog.is_file()
 run(['mount','--bind',str(s/'artifacts/fr.mo'),str(catalog)]);run(['mount','--make-private',str(catalog)])
 run(['systemctl','reset-failed','essway.service']);run(['systemctl','start','essway.service'])
 for i in range(35):
  p=subprocess.run(['curl','-fsS','--max-time','2','http://127.0.0.1:1234/isIdle'],capture_output=True,text=True,timeout=3)
  if p.returncode==0 and json.loads(p.stdout)==[True]:break
  time.sleep(1)
 else:raise RuntimeError('frontend not idle')
 pid=int(run(['pidof','emulationstation']).strip());assert sha(Path('/proc')/str(pid)/'exe')==expected
 result.update(rc=0,es_pid=pid,es_sha256=expected,catalog_sha256=sha(catalog),mode=oct(target.stat().st_mode&0o777),boot=Path('/proc/sys/kernel/random/boot_id').read_text().strip(),sockets=[str(p) for p in Path('/run/0-runtime-dir').glob('wayland-*') if p.is_socket()])
finally:
 result['ended']=time.time();(r/'provision02-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
raise SystemExit(result['rc'])
