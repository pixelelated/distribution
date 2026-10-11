from pathlib import Path
import subprocess,json,hashlib,time,shutil,os,fcntl,signal
P=Path('/storage/qa537/seed37');P.mkdir(exist_ok=True)
cfg=Path('/storage/.config/rclone/rclone.conf');active=cfg.with_name('active-connection');sync=Path('/storage/.config/cloud_sync.conf');system=Path('/storage/.config/system/configs/system.cfg')
backups={str(p):(p.read_bytes(),p.stat().st_mode&0o777) if p.exists() else None for p in [cfg,active,sync,system]}
results=[];children=[]
def run(*args):
 p=subprocess.run(args,capture_output=True,text=True,timeout=20);return {'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def barrier(tag):
 entered=P/(tag+'-entered');release=P/(tag+'-release')
 shim=Path('/usr/bin/rclone');shim.write_text('#!/bin/sh\nif [ "$1" = mkdir ] && [ ! -e '+str(entered)+' ]; then echo $$ > '+str(entered)+'; while [ ! -e '+str(release)+' ]; do sleep 0.1; done; fi\nexec /storage/qa537/rclone-real "$@"\n');shim.chmod(0o755)
 log=(P/(tag+'.log')).open('w');child=subprocess.Popen(['cloud_setup','--seed-folders','settings'],stdout=log,stderr=subprocess.STDOUT,start_new_session=True);children.append((child,log,release))
 for _ in range(100):
  if entered.exists():return child,release,int(entered.read_text())
  assert child.poll() is None
  time.sleep(.1)
 raise RuntimeError('no seed writer witness')
try:
 for n in ['alpha','beta']:(P/n).mkdir(exist_ok=True)
 cfg.write_text('[alpha]\ntype = alias\nremote = '+str(P/'alpha')+'\n\n[beta]\ntype = alias\nremote = '+str(P/'beta')+'\n');active.write_text('alpha\n')
 sync.write_text('SAVES_REMOTE="/Saves"\nSETTINGS_REMOTE="/Backups"\nCONTENT_REMOTE="/Content"\n');system.write_text('cloudsaves.startup=0\ncloudsaves.gameexit=0\n')
 child,release,pid=barrier('ordinary');before=cfg.read_bytes();before_active=active.read_bytes()
 inherited=[]
 for f in Path('/proc',str(pid),'fd').iterdir():
  try:
   if os.readlink(f)=='/run/cloud_sync.lock' or os.readlink(f)=='/var/run/cloud_sync.lock':inherited.append(f.name)
  except FileNotFoundError:pass
 assert not inherited
 for args in [('select','beta'),('update','alpha','alias','remote='+str(P/'beta')),('remove','alpha')]:
  x=run('cloud_remote',*args);assert x['rc']==2 and 'A cloud operation is running.' in x['stderr'],x;results.append({'case':args[0],'rc':x['rc'],'seed_alive':child.poll() is None})
 assert cfg.read_bytes()==before and active.read_bytes()==before_active
 release.touch();assert child.wait(timeout=20)==0
 assert (P/'alpha/Backups/README.txt').exists() and not (P/'beta/Backups').exists()
 results.append({'case':'unchanged-seed','rc':0,'correct_note':True,'child_inherited_lock':False})
 shutil.copy2('/storage/qa537/rclone-real','/usr/bin/rclone')
 with open('/var/run/cloud_sync.lock','a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  x=run('cloud_setup','--seed-folders','bios');assert x['rc']==75,x
  assert not (P/'alpha/Content/BIOS').exists()
  results.append({'case':'busy-seed','rc':75,'no_write':True})
 child,release,pid=barrier('orphan');child.send_signal(signal.SIGTERM);child.wait(timeout=5)
 assert Path('/proc',str(pid)).exists()
 x=run('cloud_remote','select','beta');assert x['rc']==0,x
 results.append({'case':'parent-ended','child_alive':True,'selection_rc':0,'no_inherited_lock':True})
 os.killpg(child.pid,signal.SIGTERM)
 (P/'result.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2),flush=True)
 print('PASS6 seeding exclusion/ownership controls',flush=True)
finally:
 for child,log,release in children:
  try:os.killpg(child.pid,signal.SIGTERM)
  except ProcessLookupError:pass
  release.touch();log.close()
 shutil.copy2('/storage/qa537/rclone-real','/usr/bin/rclone')
 for name,data in backups.items():
  p=Path(name)
  if data is None:p.unlink(missing_ok=True)
  else:p.write_bytes(data[0]);p.chmod(data[1])
 print('RESTORED synthetic configuration',flush=True)
