from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat,subprocess,sys
owner=Path(__file__).resolve().parent
preflight=owner.with_name('pixelelated-m7-qa-disk-retirement-preflight-02')
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
 for p,h in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
 plan=json.loads((preflight/'proposal.json').read_text())
 excluded={Path(x['path']) for x in plan['targets']}
 failed=Path('/workspace/tmp/pixelelated-m7-p4-no-join-negative-01')
 def retained_files():
  rows={}
  for p in sorted(failed.rglob('*')):
   if p in excluded or not p.is_file() or p.is_symlink():continue
   with p.open('rb') as f:rows[str(p)]=hashlib.file_digest(f,'sha256').hexdigest()
  return rows
 def protected_metadata():
  roots=[Path('/workspace/tmp/pixelelated-m7-p4-no-join-negative-02/pair'),Path('/workspace/artifacts/rocknix-images/x64-all-20260929-69e6039f8f'),Path('/workspace/artifacts/rocknix-images/x64-all-20261001-1acdaf2cce')]
  rows={}
  for root in roots:
   assert root.is_dir(),root
   for p in sorted(root.rglob('*')):
    s=p.lstat()
    if stat.S_ISREG(s.st_mode):rows[str(p)]=[s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_blocks]
  return rows
 before=retained_files();protected=protected_metadata()
 assert before and protected
 (owner/'artifacts/retained-before.json').write_text(json.dumps({'failed01_sha256':before,'protected_metadata':protected},indent=2)+'\n')
 digest=hashlib.sha256((preflight/'proposal.json').read_bytes()).hexdigest()
 subprocess.run([sys.executable,'-I',str(owner/'execute.py'),'--approved-plan-sha',digest],check=True)
 assert before==retained_files(),'Failed01 retained evidence changed'
 assert protected==protected_metadata(),'Protected pair/source metadata changed'
 receipt=json.loads((preflight/'execution.json').read_text())
 assert receipt['all_targets_absent'] and len(receipt['removed'])==2
 (owner/'artifacts/retention-verification.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'passed':True,'failed01_files_hash_unchanged':len(before),'protected_files_metadata_unchanged':len(protected),'execution':receipt},indent=2)+'\n')
 print('PASS exact two approved disks removed; retained evidence hashes and protected file identities unchanged',flush=True)
 rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
