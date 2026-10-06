from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat,subprocess,sys
owner=Path(__file__).resolve().parent
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
 for p,h in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
 source=Path('/workspace/tmp/pixelelated-m7-p4-no-join-negative-01');v=json.loads((source/'owner-verification.json').read_text());assert set(v['channels'].values())=={'1'} and json.loads((source/'guest-cleanup-verification.json').read_text())['passed']
 for p in Path('/proc').glob('[0-9]*/cmdline'):
  try:args=[a.decode(errors='replace') for a in p.read_bytes().split(b'\0') if a]
  except OSError:continue
  assert not (args and Path(args[0]).name.startswith('qemu-system-')),str(p)
 targets=[]
 for name in ['vm-a.qcow2','vm-b.qcow2']:
  p=source/'pair'/name;s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_uid==os.getuid() and s.st_nlink==1
  with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
  targets.append(dict(path=str(p),sha256=h,device=s.st_dev,inode=s.st_ino,size=s.st_size,allocated_bytes=s.st_blocks*512,mtime_ns=s.st_mtime_ns))
 subprocess.run([sys.executable,'-I',str(owner/'inspect.py')],check=True)
 space=os.statvfs('/workspace');available=space.f_bavail*space.f_frsize;reclaim=sum(x['allocated_bytes'] for x in targets)
 plan=dict(utc=datetime.now(timezone.utc).isoformat(),targets=targets,reclaim_bytes=reclaim,available_bytes=available,required_bytes=347886931968,projected_bytes=available+reclaim,permission='NOT APPROVED: proposal only',retained='All failed01 logs/frames/source records, successful02 pair, retained RC2/1ac source images, every candidate/build/source cache; only the two failed01 standalone QA disk files are proposed.',scope='Four established storage roots; QCOW2 suffix; no followed directory symlinks. All backing chains checked; no live QEMU. No deletion performed.')
 (owner/'proposal.json').write_text(json.dumps(plan,indent=2)+'\n');print(json.dumps(plan),flush=True);rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
