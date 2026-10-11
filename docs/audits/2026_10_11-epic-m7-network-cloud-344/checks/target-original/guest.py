
from pathlib import Path
import subprocess,json,hashlib,time,os
P=Path('/storage/qa537/audit18');P.mkdir(exist_ok=True)
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
 a=run('cloud_scan','--context');scan=run('cloud_scan','--run-id','audit18-alpha')
 valid_before=run('cloud_scan','--stamp-valid','done','audit18-alpha')
 switched=run('cloud_remote','select','beta');b=run('cloud_scan','--context');valid_after=run('cloud_scan','--stamp-valid','done','audit18-alpha')
 save('scan.json',dict(alpha=a,beta=b,scan=scan,valid_before=valid_before,switch=switched,valid_after=valid_after))
 print('SCAN',a['rc'],b['rc'],'identity_equal',a['stdout']==b['stdout'],'scan_rc',scan['rc'],'stamp_before_after',valid_before['rc'],valid_after['rc'],flush=True)
 # A blocked synthetic mkdir exposes the actual exclusion window without network I/O.
 run('cloud_remote','select','alpha')
 shim=Path('/usr/bin/rclone');shim.write_text('#!/bin/sh\nif [ "$1" = mkdir ] && [ ! -e /storage/qa537/audit18/mkdir-entered ]; then\n touch /storage/qa537/audit18/mkdir-entered\n while [ ! -e /storage/qa537/audit18/release ]; do sleep 0.1; done\nfi\nexec /storage/qa537/rclone-real "$@"\n');shim.chmod(0o755)
 with (P/'seed.log').open('w') as log:
  child=subprocess.Popen(['cloud_setup','--seed-folders','settings'],stdout=log,stderr=subprocess.STDOUT)
  try:
   for _ in range(100):
    if (P/'mkdir-entered').exists():break
    if child.poll() is not None:raise RuntimeError('seed finished before controlled mkdir')
    time.sleep(.1)
   else:raise RuntimeError('no blocked mkdir')
   change=run('cloud_remote','select','beta')
   save('seed.json',{'while_seed_alive':child.poll() is None,'select_during_seed':change})
   print('SEED live',child.poll() is None,'selection_rc',change['rc'],flush=True)
  finally:
   (P/'release').touch();child.wait(timeout=30)
 subprocess.run(['cp','/storage/qa537/rclone-real','/usr/bin/rclone'],check=True)
 run('cloud_remote','select','alpha')
 local=Path('/storage/roms/qa537audit');local.mkdir(exist_ok=True)
 (local/'local.rom').write_text('local content\n');(local/'save.srm').write_text('preserve progress\n')
 preview=run('cloud_content_restore','--match');plan=Path('/storage/.cache/cloud_sync/content-match-plan').read_text()
 change=run('cloud_remote','select','beta');apply=run('cloud_content_restore','--match','--apply')
 files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in local.iterdir() if p.is_file()}
 save('match.json',dict(preview=preview,plan=plan,switch=change,apply=apply,local_after=files))
 print('MATCH preview',preview['rc'],'apply',apply['rc'],'files',list(files),flush=True)
finally:
 subprocess.run(['cp','/storage/qa537/rclone-real','/usr/bin/rclone'],check=True)
 for name,data in backups.items():
  p=Path(name)
  if data is None:p.unlink(missing_ok=True)
  else:p.write_bytes(data)
 print('RESTORED synthetic configuration',flush=True)
