from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime,hashlib,json,os,subprocess,time
REPO=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
OUT=Path('/tmp/pixelelated-approved-cleanup-20261006')
CUSTODY=REPO/'docs/qa-logs/2026-10-05-build-storage/custody-followup-20261006'
PRESERVE=REPO/'docs/qa-logs/2026-10-05-build-storage/preservation-20261006'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def git(p,*a):return subprocess.check_output(['git','-C',str(p),*a],text=True)
todo={};git_inputs={};manifests=[]
def add(p,digest):
 p=Path(p);assert p.is_file(),p
 if p in todo:assert todo[p]==digest,p
 todo[p]=digest
rows=json.loads((CUSTODY/'tree-custody.json').read_text())
assert [Path(r['tree']).name[-2:] for r in rows]==['03','05','06','07','08']
for r in rows:
 tree=Path(r['tree']);assert tree.is_dir() and not tree.is_symlink()
 assert git(tree,'rev-parse','HEAD').strip()==r['head']
 assert git(tree,'branch','--show-current').strip()==r['branch']
 assert git(tree,'status','--porcelain')==r['tracked_status']
 assert hashlib.sha256(subprocess.check_output(['git','-C',str(tree),'diff','--binary'])).hexdigest()==r['tracked_diff_sha256']
 for b in r['retained_bundles']:
  root=Path(b['path']);assert sha(root/'manifest.json')==b['manifest_sha256']
  for name,info in b['files'].items():add(root/name,info['sha256'])
 print('Verified exact branch/source/tracked diff',tree.name,flush=True)
for kind in ['preserve-01','runtime-02']:
 summary=json.loads((PRESERVE/kind/'summary.json').read_text())
 for row in summary['trees']:
  p=Path(row['manifest']);assert sha(p)==row['manifest_sha256'];manifests.append({'path':str(p),'sha256':row['manifest_sha256']})
  m=json.loads(p.read_text())
  if kind=='preserve-01':
   for e in m['entries']:
    if e['kind']=='file':add(p.parent/'objects'/e['sha256'],e['sha256'])
  else:
   for e in m['runtime_elf']:add(e['object'],e['sha256'])
source=json.loads((PRESERVE/'runtime-02/source-custody.json').read_text())
add(source['rclone_archive'],source['rclone_archive_sha256'])
for r in source['trees']:
 p=Path(r['manifest']);assert sha(p)==r['sha256'];manifests.append({'path':str(p),'sha256':r['sha256']});m=json.loads(p.read_text());assert not m['errors']
 for rec in m['records']:
  for c in rec.get('cache',[]):
   q=Path(source['source_cache'])/rec['package']/c['name']
   if 'sha256' in c:add(q,c['sha256'])
   else:git_inputs[q]=c
for p,c in git_inputs.items():
 assert git(p,'rev-parse','HEAD').strip()==c['git_head'],p
 have=[x.strip() for x in git(p,'submodule','status','--recursive').splitlines()]
 assert have==[x.strip() for x in c['submodules']],p
print('Verified source inventory manifests and',len(git_inputs),'git source inputs; hashing',len(todo),'retained files',flush=True)
total=0;count=0;last=time.monotonic();verified=[]
def check(item):
 p,want=item;s=p.stat();got=sha(p);after=p.stat()
 assert (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns),p
 assert got==want,(p,got,want)
 return {'path':str(p),'sha256':got,'bytes':s.st_size,'dev':s.st_dev,'inode':s.st_ino,'mtime_ns':s.st_mtime_ns,'ctime_ns':s.st_ctime_ns}
with ThreadPoolExecutor(max_workers=4) as pool:
 for future in as_completed([pool.submit(check,item) for item in todo.items()]):
  row=future.result();verified.append(row);count+=1;total+=row['bytes']
  if time.monotonic()-last>5:
   print('Hashed',count,'/',len(todo),'retained files;',total,'bytes',flush=True);last=time.monotonic()
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Five exact source/diffs, retained bundle payloads, independent ES/runtime objects, source archives/git pins; no deletion','files_verified':len(verified),'bytes_hashed':total,'git_inputs':len(git_inputs),'manifests':manifests,'files':verified,'all_pass':True}
(OUT/'preservation-reverified.json').write_text(json.dumps(r,indent=2)+'\n')
print('PASS preservation reverified',count,'files',total,'bytes',flush=True)
