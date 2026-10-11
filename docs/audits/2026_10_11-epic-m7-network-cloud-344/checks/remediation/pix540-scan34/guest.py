
from pathlib import Path
import subprocess,json,hashlib,time,os
P=Path('/storage/qa537/scan34');P.mkdir(exist_ok=True)
def run(*args):
 p=subprocess.run(args,capture_output=True,text=True,timeout=90)
 return {'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def save(name,x): (P/name).write_text(json.dumps(x,indent=2)+'\n')
cfg=Path('/storage/.config/rclone/rclone.conf');active=cfg.with_name('active-connection')
sync=Path('/storage/.config/cloud_sync.conf');selected=Path('/storage/.cache/cloud_sync/content-systems')
backups={str(p):p.read_bytes() if p.exists() else None for p in [cfg,active,sync,selected]}
try:
 for remote in ['alpha','beta']:
  p=P/remote/'Content/ROMs/qa537audit';p.mkdir(parents=True,exist_ok=True)
  (p/(remote+'.rom')).write_text(remote+' content\n')
  (P/remote/'Backups').mkdir(exist_ok=True)
  (P/remote/'Saves').mkdir(exist_ok=True)
  (P/remote/'.layout').write_text('layout=2\n')
 cfg.write_text('[alpha]\ntype = alias\nremote = '+str(P/'alpha')+'\n\n[beta]\ntype = alias\nremote = '+str(P/'beta')+'\n');cfg.chmod(0o600)
 active.write_text('alpha\n');active.chmod(0o600)
 sync.write_text('SAVES_REMOTE="/Saves"\nSETTINGS_REMOTE="/Backups"\nCONTENT_REMOTE="/Content"\nRCLONE_NET_OPTS="--contimeout 2s --timeout 3s --low-level-retries 1 --retries 1"\n')
 selected.parent.mkdir(exist_ok=True);selected.write_text('qa537audit\n')
 a=run('cloud_scan','--context');scan=run('cloud_scan','--run-id','audit34-alpha')
 valid_before=run('cloud_scan','--stamp-valid','done','audit34-alpha')
 switched=run('cloud_remote','select','beta');b=run('cloud_scan','--context');valid_after=run('cloud_scan','--stamp-valid','done','audit34-alpha')
 save('scan.json',dict(alpha=a,beta=b,scan=scan,valid_before=valid_before,switch=switched,valid_after=valid_after))
 print('SCAN',a['rc'],b['rc'],'identity_equal',a['stdout']==b['stdout'],'scan_rc',scan['rc'],'stamp_before_after',valid_before['rc'],valid_after['rc'],flush=True)
 # Same context succeeds; missing versus explicit-empty is a distinct identity.
 assert a['stdout']!=b['stdout'] and scan['rc']==0 and valid_before['rc']==0 and valid_after['rc']!=0
 active.unlink();missing=run('cloud_scan','--context');active.write_text('\n');empty=run('cloud_scan','--context')
 assert missing['stdout']!=empty['stdout']
 run('cloud_remote','select','alpha')
 barrier=P/'scan-entered';release=P/'release'
 shim=Path('/usr/bin/rclone');shim.write_text('#!/bin/sh\ncase "$1" in lsf|lsd) if [ ! -e '+str(barrier)+' ]; then touch '+str(barrier)+'; while [ ! -e '+str(release)+' ]; do sleep 0.1; done; fi;; esac\nexec /storage/qa537/rclone-real "$@"\n');shim.chmod(0o755)
 with (P/'inflight.log').open('w') as log:
  child=subprocess.Popen(['cloud_scan','--run-id','audit34-inflight'],stdout=log,stderr=subprocess.STDOUT)
  try:
   for _ in range(100):
    if barrier.exists():break
    assert child.poll() is None,'scan ended before controlled listing'
    time.sleep(.1)
   else:raise RuntimeError('no controlled listing')
   change=run('cloud_remote','select','beta');assert change['rc']==0 and child.poll() is None
  finally:release.touch();child.wait(timeout=30)
  valid=run('cloud_scan','--stamp-valid','done','audit34-inflight')
  assert child.returncode!=0 and valid['rc']!=0
 save('result.json',{'completed_switch_invalidated':True,'missing_empty_distinct':True,'inflight_refused':child.returncode,'inflight_stamp_rc':valid['rc']})
 print('PASS completed, missing/empty and in-flight selection identity controls',flush=True)

finally:
 subprocess.run(['cp','/storage/qa537/rclone-real','/usr/bin/rclone'],check=True)
 for name,data in backups.items():
  p=Path(name)
  if data is None:p.unlink(missing_ok=True)
  else:p.write_bytes(data)
 print('RESTORED synthetic configuration',flush=True)
