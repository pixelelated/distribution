#!/usr/bin/env python3
"""Read-only binding collector for the one-time #519 owner operation.

Never prints configuration values or payload bytes. Its complete JSON still
contains personal paths and must be retained privately, not committed.
"""
import hashlib,json,os,pathlib,stat,subprocess,time
P=pathlib.Path
FILES=[
 '/etc/os-release','/usr/bin/emulationstation','/usr/bin/cloud_migrate_layout',
 '/usr/bin/cloud_scan','/usr/bin/cloud_sync_helper','/usr/bin/chksysconfig',
 '/usr/bin/start_es.sh','/etc/profile.d/001-functions',
 '/usr/lib/systemd/system/emustation.service','/usr/lib/systemd/system/essway.service',
 '/usr/lib/autostart/common/001-setup','/usr/lib/autostart/common/111-sway-init',
 '/storage/.config/cloud_sync.conf','/storage/.config/cloud_sync.conf.bak',
 '/storage/.config/cloud_sync.conf.defaults','/storage/.config/cloud_sync.conf.pre-contentpath-fix',
 '/storage/.config/cloud_sync-rules.txt','/storage/.config/rclone/rclone.conf',
 '/storage/.config/system/configs/system.cfg','/storage/.config/system/configs/system.cfg.backup',
 '/storage/.config/cloud-layout-migration.json']
MARKERS=['/storage/.config/.restore-in-progress','/storage/.config/.restore-reverted',
 '/storage/.config/.restore-finish-pending','/storage/.config/.cloud-journey-pending',
 '/storage/.cache/cloud_sync/journey-tiers','/tmp/.system.cfg.lock']
HOOKS=['/storage/.config/autostart','/storage/.config/emulationstation/scripts',
 '/usr/bin/scripts','/var/run/emulationstation/scripts']

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def metadata(p):
 if p.is_symlink():return {'kind':'symlink','target':os.readlink(p)}
 if not p.exists():return {'kind':'absent'}
 s=p.stat();r={'mode':stat.S_IMODE(s.st_mode),'uid':s.st_uid,'gid':s.st_gid}
 if p.is_file():r.update(kind='file',bytes=s.st_size,sha256=digest(p))
 elif p.is_dir():r.update(kind='directory')
 else:r.update(kind='other')
 return r
def tree(p,limit=128*1024*1024,allow_symlinks=False):
 if not p.exists():return {'root':metadata(p),'entries':{}}
 assert p.is_dir() and not p.is_symlink(),str(p)
 entries={};size=0
 for f in sorted(p.rglob('*')):
  assert len(entries)<20000,'enumeration bound'
  assert allow_symlinks or not f.is_symlink(),'unclassified symlink '+str(f)
  if f.is_file() and not f.is_symlink():size+=f.stat().st_size
  assert size<=limit,'byte bound'
  entries[str(f.relative_to(p))]=metadata(f)
 return {'root':metadata(p),'entries':entries}
def run(a):return subprocess.check_output(a,text=True,stderr=subprocess.PIPE,timeout=25)
def settings():
 text=P('/storage/.config/system/configs/system.cfg').read_text();assert text.endswith('\n')
 pairs=[l.split('=',1) for l in text.splitlines() if '=' in l and not l.lstrip().startswith('#')]
 auto={k:[v for a,v in pairs if a==k] for k in ['cloudsaves.startup','cloudsaves.gameexit']}
 bootgame=any(bool(v) for k,v in pairs if k in ['global.bootgame.path','global.bootgame.cmd'])
 return {'automatic_sync':auto,'startup_game_configured':bootgame}
def collect(frontend=True):
 assert os.geteuid()==0
 start=time.monotonic();before=P('/proc/sys/kernel/random/boot_id').read_text().strip()
 files={f:metadata(P(f)) for f in FILES}
 assert all(files[f]['kind']=='file' for f in FILES[:12]),'missing installed source'
 # Force local-only enumeration, independent of personal remote credentials.
 entries=json.loads(run(['/usr/bin/rclone','lsjson','/storage/roms','--recursive','--files-only','--filter-from','/storage/.config/cloud_sync-rules.txt','--config','/dev/null']))
 assert len(entries)<=20000 and sum(x['Size'] for x in entries)<=128*1024*1024
 payload={}
 for e in sorted(entries,key=lambda e:e['Path']):
  rel=P(e['Path']);assert not rel.is_absolute() and '..' not in rel.parts
  p=P('/storage/roms')/rel;assert p.is_file() and not p.is_symlink()
  payload[e['Path']]=metadata(p)
 hooks={p:tree(P(p),8*1024*1024) for p in HOOKS}
 units={}
 for u in ['emustation.service','essway.service']:
  text=run(['systemctl','show',u,'-p','ActiveState','-p','SubState','-p','MainPID','-p','UnitFileState','-p','KillMode','-p','Restart','-p','FragmentPath','-p','DropInPaths'])
  units[u]=dict(l.split('=',1) for l in text.splitlines() if '=' in l)
 busy=[]
 for p in P('/proc').glob('[0-9]*'):
  try:
   comm=(p/'comm').read_text().strip();cmd=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
   if int(p.name)==os.getpid():continue
   if comm=='rclone' or any(t in cmd for t in ['/usr/bin/cloud_backup','/usr/bin/cloud_restore','/usr/bin/cloud_capture','/usr/bin/cloud_scan','/usr/bin/cloud_migrate_layout','/usr/bin/cloud_content_']):
    busy.append({'pid':int(p.name),'comm':comm,'argv_sha256':hashlib.sha256(cmd.encode()).hexdigest()})
  except (FileNotFoundError,ProcessLookupError):continue
 markers={p:metadata(P(p)) for p in MARKERS}
 temporaries={}
 for parent,prefixes in [('/storage/.config',['cloud_sync.conf.','cloud-layout-migration.']),('/storage/.config/system/configs',['system.cfg.'])]:
  for p in P(parent).iterdir():
   if any(p.name.startswith(n) for n in prefixes):temporaries[str(p)]=metadata(p)
 assert before==P('/proc/sys/kernel/random/boot_id').read_text().strip(),'boot changed'
 assert files=={f:metadata(P(f)) for f in FILES},'configuration/source changed during collection'
 idle=json.loads(run(['curl','-fsS','--max-time','2','http://127.0.0.1:1234/isIdle'])) if frontend else None
 return {'schema':1,'read_only':True,'boot_id':before,'files':files,'settings':settings(),'safe_payload':payload,'local_recovery':tree(P('/storage/.cache/cloud_sync/replaced')),'hooks':hooks,'unit_overrides':tree(P('/storage/.config/system.d'),8*1024*1024,True),'units':units,'busy_cloud_processes':busy,'frontend_idle':idle,'markers':markers,'temporaries':temporaries,'scan':tree(P('/storage/.cache/cloud_sync/scan'),1024*1024),'elapsed_seconds':round(time.monotonic()-start,3)}
if __name__=='__main__':print(json.dumps(collect(),indent=2))
