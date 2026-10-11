from pathlib import Path
import hashlib,json,stat,subprocess,tarfile,shutil
p=Path(__file__).resolve().parent
previous=Path('/workspace/tmp/pixelelated-m7-image19');current=Path('/workspace/tmp/pixelelated-m7-image20')
assert json.loads((current/'launcher-result.json').read_text())['runner_returncode']==1
assert json.loads((current/'result.json').read_text())['result']=='PASS'
old=previous/'root';new=current/'root';oldsystem=p/'previous-SYSTEM'
oldbundle=Path((previous/'bundle.path').read_text().strip());newbundle=Path((current/'bundle.path').read_text().strip())
for b in [oldbundle,newbundle]:subprocess.run(['tools/rasteratops-candidate-store','verify',str(b)],check=True)
with tarfile.open(next(oldbundle.glob('*.tar'))) as tf:
 members=[x for x in tf.getmembers() if x.name.endswith('/target/SYSTEM')];assert len(members)==1
 with tf.extractfile(members[0]) as source,oldsystem.open('xb') as target:shutil.copyfileobj(source,target,4*1024*1024)
assert hashlib.sha256(oldsystem.read_bytes()).hexdigest()=='806f6f1728228f57ef4a028fe939effa2c1b853f6fd6d22eea0e7db414fe8e9c'
archive_reads=[]
def digest(f,root,system):
 h=hashlib.sha256()
 try:stream=f.open('rb')
 except PermissionError:
  proc=subprocess.run(['unsquashfs','-cat',str(system),f.relative_to(root).as_posix()],capture_output=True,check=True)
  assert len(proc.stdout)==f.stat().st_size
  archive_reads.append({'root':str(root),'path':f.relative_to(root).as_posix(),'bytes':len(proc.stdout)})
  return hashlib.sha256(proc.stdout).hexdigest()
 with stream:
  for block in iter(lambda:stream.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest()
def inventory(root,system):
 data={}
 for f in root.rglob('*'):
  mode=f.lstat().st_mode;row={'mode':oct(stat.S_IMODE(mode)),'type':stat.S_IFMT(mode)}
  if stat.S_ISREG(mode):row.update(size=f.stat().st_size,sha256=digest(f,root,system))
  elif stat.S_ISLNK(mode):row['target']=f.readlink().as_posix()
  data[f.relative_to(root).as_posix()]=row
 return data
try:
 a=inventory(old,oldsystem);print('Indexed predecessor',len(a),flush=True)
 b=inventory(new,current/'SYSTEM');print('Indexed corrected image',len(b),flush=True)
 changes={n:{'before':a.get(n),'after':b.get(n)} for n in sorted(a.keys()|b.keys()) if a.get(n)!=b.get(n)}
 (p/'installed-delta.json').write_text(json.dumps({'before':'replacement19','after':'replacement20','entries_before':len(a),'entries_after':len(b),'changes':changes,'archive_reads':archive_reads,'requires_review':True},indent=2)+'\n')
 print('Installed differences require review:',list(changes),flush=True)
finally:oldsystem.unlink()
print('PASS full file comparison completed without permission changes; transient SYSTEM removed',flush=True)
