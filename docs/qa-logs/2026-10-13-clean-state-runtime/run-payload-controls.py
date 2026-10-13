#!/usr/bin/env python3
import argparse,datetime,hashlib,json,os,signal,subprocess,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('owner',type=Path);a=p.parse_args();o=a.owner
scratch=o/'scratch';scratch.mkdir();bindir=o/'bin';bindir.mkdir()
mcopy=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64/toolchain/bin/mcopy')
(bindir/'mcopy').symlink_to(mcopy)
env={**os.environ,'PATH':str(bindir)+':/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin','TMPDIR':str(scratch)}
def processes():
 rows={}
 for p in Path('/proc').glob('[0-9]*/stat'):
  try:
   s=p.read_text().rsplit(')',1)[1].split();rows[int(p.parent.name)]=(int(s[1]),s[19],s[0])
  except (OSError,ValueError,IndexError):pass
 return rows
seen={};peak=0;start=time.monotonic();reason=None
with (o/'stdout.json').open('xb') as out,(o/'stderr.log').open('xb') as err:
 child=subprocess.Popen(['/usr/bin/python3','-B',str(o/'source/tools/pixelelated-state-check-test'),'--payload-tests'],stdout=out,stderr=err,stdin=subprocess.DEVNULL,env=env,start_new_session=True)
 while True:
  rows=processes();known={child.pid}
  for _ in range(10):
   added={pid for pid,(ppid,_,_) in rows.items() if ppid in known};new=known|added
   if new==known:break
   known=new
  seen.update({pid:rows[pid][1] for pid in known if pid in rows})
  used=0
  for path in scratch.rglob('*'):
   try:
    if path.is_file():used+=path.stat().st_blocks*512
   except FileNotFoundError:pass
  peak=max(peak,used)
  if used>1024**3:reason='scratch-bound';break
  if time.monotonic()-start>180:reason='time-bound';break
  if child.poll() is not None:break
  time.sleep(.2)
 rows=processes();left=[pid for pid,tick in seen.items() if pid!=child.pid and pid in rows and rows[pid][1]==tick and rows[pid][2]!='Z']
 if reason or left:
  reason=reason or 'surviving-child'
  for pid,tick in reversed(list(seen.items())):
   rows=processes()
   if pid in rows and rows[pid][1]==tick and rows[pid][2]!='Z':os.kill(pid,signal.SIGKILL)
 child.wait(timeout=5)
try:report=json.loads((o/'stdout.json').read_text())
except Exception:report={'status':'invalid-json'}
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rc':child.returncode,'guard':reason,'seconds':time.monotonic()-start,'peak_scratch_allocated_bytes':peak,'scratch_empty':not any(scratch.iterdir()),'observed_children':seen,'stderr_empty':(o/'stderr.log').stat().st_size==0,'report':report,'mcopy_path':str(mcopy),'mcopy_sha256':hashlib.sha256(mcopy.read_bytes()).hexdigest()}
(o/'result.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k not in ('report','observed_children')}),flush=True)
raise SystemExit(0 if child.returncode==0 and not reason and receipt['stderr_empty'] and receipt['scratch_empty'] and report.get('status')=='pass' else 2)
