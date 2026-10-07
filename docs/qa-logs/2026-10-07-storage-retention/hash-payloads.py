from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime,hashlib,json,os,stat,sys,time
owner=Path(__file__).resolve().parent
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
def identity(p):
 s=p.lstat();return dict(device=s.st_dev,inode=s.st_ino,size=s.st_size,allocated_bytes=s.st_blocks*512,mtime_ns=s.st_mtime_ns,uid=s.st_uid,mode=s.st_mode,links=s.st_nlink)
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while block:=f.read(8*1024**2):h.update(block)
 return h.hexdigest()
rc=1
try:
 for n,h in json.loads((owner/'seal.json').read_text()).items():assert digest(Path(n))==h,n
 plan=json.loads((owner/'selection.json').read_text());results=[];errors=[];total=0;tick=time.monotonic();started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 def check(r):
  p=Path(r['path']);assert identity(p)==r['identity'],str(p)
  assert stat.S_ISREG(p.lstat().st_mode) and not p.is_symlink(),str(p)
  h=digest(p);assert identity(p)==r['identity'],str(p)
  side=p.with_name(p.name+'.sha256');side_result=None
  if r['kind']=='superseded-firmware' and side.is_file():
   expected=side.read_text().split()[0];assert len(expected)==64 and h==expected,(str(p),'checksum mismatch')
   side_result={'path':str(side),'sha256':digest(side),'matches':True}
  return {**r,'sha256':h,'sidecar':side_result}
 with (owner/'artifacts/verified.ndjson').open('x') as stream, ThreadPoolExecutor(max_workers=4) as pool:
  futures={pool.submit(check,r):r['path'] for r in plan['candidates']}
  for future in as_completed(futures):
   try:
    r=future.result();results.append(r);total+=r['identity']['allocated_bytes'];stream.write(json.dumps(r)+'\n');stream.flush()
   except Exception as error:errors.append({'path':futures[future],'error':str(error)})
   if time.monotonic()-tick>10:print(f'Hashed {len(results)}/{len(futures)} payloads, {total/2**30:.2f} GiB, {len(errors)} errors',flush=True);tick=time.monotonic()
 # These independent records remain at their original paths; payload-only retirement never removes their owner directories.
 records=[];roots=sorted({r['group'] for r in results});payloads={r['path'] for r in results}
 for root in roots:
  for base,dirs,files in os.walk(root,followlinks=False):
   dirs[:]=[n for n in dirs if n not in ['root','sources','build','toolchain','qa-overlay'] and not Path(base,n).is_symlink()]
   for n in files:
    p=Path(base,n)
    if str(p) in payloads or p.is_symlink():continue
    s=p.lstat()
    if not stat.S_ISREG(s.st_mode) or s.st_size>16*1024**2:continue
    before=identity(p);h=digest(p);assert identity(p)==before,str(p)
    records.append({'path':str(p),'identity':before,'sha256':h})
 report={'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'payloads':sorted(results,key=lambda r:r['path']),'errors':errors,'retained_records':records,'allocated_review_bytes':total,'deletion_performed':False,'scope':'Payload identity and digest inventory, with original independent compact records retained in place. Dependencies and active-use checks still required before retirement.'}
 p=owner/'artifacts/result.json';p.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'verified':len(results),'errors':len(errors),'retained_records':len(records),'allocated_review_bytes':total,'report_sha256':digest(p)}),flush=True)
 assert not errors,errors[:5]
 rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
