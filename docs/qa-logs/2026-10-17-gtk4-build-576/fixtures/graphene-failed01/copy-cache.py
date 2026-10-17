import hashlib,json,os,subprocess,time
from pathlib import Path
root=Path.cwd()/'build.pixelelated-GENERIC_X64.x86_64'
assert not root.exists()
root.mkdir()
began=time.monotonic()
records=[]
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
for name in ['toolchain','.stamps','.build.conf']:
 src=Path('/baseline')/name; dst=root/name
 subprocess.run(['cp','-a','--reflink=never','--',str(src),str(dst)],check=True)
 files=list(src.rglob('*')) if src.is_dir() else [src]
 regular=links=total=0
 digest=hashlib.sha256()
 for p in files:
  q=dst/p.relative_to(src) if src.is_dir() else dst
  a=p.lstat();b=q.lstat()
  assert (a.st_dev,a.st_ino)!=(b.st_dev,b.st_ino)
  assert a.st_mode==b.st_mode
  if p.is_symlink():
   assert os.readlink(p)==os.readlink(q);links+=1
  elif p.is_file():
   assert a.st_size==b.st_size
   h=sha(p);assert h==sha(q)
   digest.update((str(p.relative_to(src))+' '+h+'\n').encode())
   regular+=1;total+=a.st_size
 records.append(dict(name=name,regular_files=regular,symlinks=links,logical_bytes=total,content_manifest_sha256=digest.hexdigest()))
Path('/build-owner/cache-copy.json').write_text(json.dumps(dict(status='PASS',records=records,seconds=time.monotonic()-began,independent_inodes=True),indent=2)+'\n')
