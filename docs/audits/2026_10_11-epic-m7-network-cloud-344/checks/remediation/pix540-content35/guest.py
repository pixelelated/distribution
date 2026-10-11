from pathlib import Path
import subprocess,json,hashlib,time,shutil,os
P=Path('/storage/qa537/content35');P.mkdir(exist_ok=True)
cfg=Path('/storage/.config/rclone/rclone.conf');active=cfg.with_name('active-connection');sync=Path('/storage/.config/cloud_sync.conf');selected=Path('/storage/.cache/cloud_sync/content-systems');system=Path('/storage/.config/system/configs/system.cfg')
local=Path('/storage/roms/qa540match');local.mkdir(exist_ok=True)
plan=Path('/storage/.cache/cloud_sync/content-match-plan');scan=Path('/usr/bin/cloud_scan');real_scan=P/'cloud_scan-real';shutil.copy2(scan,real_scan)
backups={str(p):(p.read_bytes(),p.stat().st_mode&0o777) if p.exists() else None for p in [cfg,active,sync,selected,system,plan]}
results=[]
def run(*args):
 p=subprocess.run(args,capture_output=True,text=True,timeout=45)
 return {'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def record(name,**data):
 results.append({'case':name,**data});(P/'result.json').write_text(json.dumps(results,indent=2)+'\n');print(name,json.dumps(data),flush=True)
def hashes():
 return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for root in [local,P/'alpha',P/'beta'] for p in root.rglob('*') if p.is_file()}
def reset():
 shutil.copy2(real_scan,scan)
 for p in local.iterdir():
  if p.is_file():p.unlink()
 (local/'local.rom').write_text('local content\n');(local/'save.srm').write_text('preserve progress\n')
 for n in ['alpha','beta']:
  root=P/n
  if root.exists():shutil.rmtree(root)
  (root/'Content/ROMs/qa540match').mkdir(parents=True)
  (root/'Content/ROMs/qa540match'/f'{n}.rom').write_text(n+' content\n')
 cfg.write_text('[alpha]\ntype = alias\nremote = '+str(P/'alpha')+'\n\n[beta]\ntype = alias\nremote = '+str(P/'beta')+'\n');cfg.chmod(0o600)
 active.write_text('alpha\n');active.chmod(0o600)
 sync.write_text('SAVES_REMOTE="/Saves"\nSETTINGS_REMOTE="/Backups"\nCONTENT_REMOTE="/Content"\nRCLONE_NET_OPTS="--contimeout 2s --timeout 3s --low-level-retries 1 --retries 1"\n')
 selected.write_text('qa540match\n');system.write_text('cloudsaves.startup=0\ncloudsaves.gameexit=0\n')
 plan.unlink(missing_ok=True)
def replace():
 p=run('cloud_remote','update','alpha','alias','remote='+str(P/'beta'));assert p['rc']==0,p
try:
 for kind in ['selection','same-name','folder','old-plan','mode','unchanged']:
  reset();preview=run('cloud_content_restore','--match');assert preview['rc']==0,preview
  assert plan.read_text().startswith('plan2 ')
  before=hashes();extra=[]
  if kind=='selection':assert run('cloud_remote','select','beta')['rc']==0
  elif kind=='same-name':replace()
  elif kind=='folder':sync.write_text(sync.read_text().replace('/Content','/Other'))
  elif kind=='old-plan':plan.write_text('plan 1\n'+'\n'.join(plan.read_text().splitlines()[1:])+'\n')
  elif kind=='mode':extra=['--with-media']
  apply=run('cloud_content_restore','--match','--apply',*extra)
  assert not plan.exists(),kind
  if kind=='unchanged':
   assert apply['rc']==0,apply
   assert not (local/'local.rom').exists() and (local/'alpha.rom').exists()
   assert (local/'save.srm').read_text()=='preserve progress\n'
  else:assert apply['rc']!=0 and hashes()==before,(kind,apply)
  record(kind,preview_rc=preview['rc'],apply_rc=apply['rc'],plan_spent=True,payload_preserved=kind!='unchanged',save_preserved=True)
 # Stop after the initial genuine context has been read, before config/preflight.
 # Same-name update is a real cooperative writer; no transfer lock is held yet.
 for command in ['cloud_content_backup','cloud_content_restore']:
  reset();entered=P/'entered';release=P/'release';entered.unlink(missing_ok=True);release.unlink(missing_ok=True)
  scan.write_text('#!/bin/sh\nif [ "$1" = --context ] && [ ! -e '+str(entered)+' ]; then\n '+str(real_scan)+' --context || exit $?\n touch '+str(entered)+'\n while [ ! -e '+str(release)+' ]; do sleep 0.1; done\n exit 0\nfi\nexec '+str(real_scan)+' "$@"\n');scan.chmod(0o755)
  before=hashes()
  with (P/(command+'.log')).open('w') as log:
   child=subprocess.Popen([command,'qa540match'],stdout=log,stderr=subprocess.STDOUT)
   try:
    for _ in range(100):
     if entered.exists():break
     assert child.poll() is None,'transfer ended before controlled preflight'
     time.sleep(.1)
    else:raise RuntimeError('missing preflight witness')
    replace();assert child.poll() is None
   finally:release.touch();child.wait(timeout=45)
   assert child.returncode!=0 and hashes()==before,command
   record(command+'-preflight',rc=child.returncode,payload_preserved=True)
 # A configuration change during preview cannot publish a bound plan.
 reset();entered=P/'preview-entered';release=P/'preview-release';entered.unlink(missing_ok=True);release.unlink(missing_ok=True)
 shim=Path('/usr/bin/rclone');shim.write_text('#!/bin/sh\ncase "$1" in lsf|lsd) if [ ! -e '+str(entered)+' ]; then touch '+str(entered)+'; while [ ! -e '+str(release)+' ]; do sleep 0.1; done; fi;; esac\nexec /storage/qa537/rclone-real "$@"\n');shim.chmod(0o755)
 with (P/'preview.log').open('w') as log:
  child=subprocess.Popen(['cloud_content_restore','--match'],stdout=log,stderr=subprocess.STDOUT)
  try:
   for _ in range(100):
    if entered.exists():break
    assert child.poll() is None
    time.sleep(.1)
   else:raise RuntimeError('missing preview witness')
   assert run('cloud_remote','select','beta')['rc']==0
  finally:release.touch();child.wait(timeout=45)
  assert child.returncode!=0 and not plan.exists()
  record('inflight-preview',rc=child.returncode,no_plan=True)
 print('PASS all9 configuration-bound content controls',flush=True)
finally:
 shutil.copy2(real_scan,scan);shutil.copy2('/storage/qa537/rclone-real','/usr/bin/rclone')
 for name,data in backups.items():
  p=Path(name)
  if data is None:p.unlink(missing_ok=True)
  else:p.write_bytes(data[0]);p.chmod(data[1])
 print('RESTORED synthetic configuration',flush=True)
