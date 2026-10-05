from pathlib import Path
import ast,hashlib,json,shutil,subprocess,datetime
prefix='/workspace/tmp/pixelelated-m7-'
names=[('proxy-10','proxy-11'),('optins-10','optins-11'),('memory-10','memory-11'),('ui-12','ui-13'),('predecessor-08','predecessor-09'),('subset-07','subset-08'),('cloud-ui-06','cloud-ui-07'),('signin-ui-06','signin-ui-07'),('signin-1g-06','signin-1g-07')]
receipt=json.loads(Path(prefix+'proxy-10/completion.json').read_text());assert receipt['job_rc']==1 and receipt['qemu_absent'];assert not Path(prefix+'proxy-10/guest.pid').exists()
controls=json.loads(Path('/tmp/pixelelated-445-directory-controls.json').read_text());assert controls['passed']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for old,new in names:
 assert not Path(prefix+new).exists()
 if old!='proxy-10':assert not Path(prefix+old+'/qa.start').exists()
out=[]
for old,new in names:
 src=Path(prefix+old);dst=Path(prefix+new);dst.mkdir(mode=0o700);(dst/'artifacts').mkdir(mode=0o700)
 for line in (src/'harness.sha256').read_text().splitlines():
  h,n=line.split(None,1);p=Path(n);assert sha(p)==h;q=dst/p.name;shutil.copyfile(p,q)
  if p.suffix in {'.sh','.py','.json'}:
   s=q.read_text()
   for a,b in names:s=s.replace(prefix+a,prefix+b)
   q.write_text(s)
 shutil.copyfile('/tmp/pixelelated-prepare-owned-dirs.py',dst/'prepare-dirs.py')
 (dst/'required-directories.json').write_text(json.dumps({'issue':445,'required':['pair','artifacts'],'mode':'0700','creator':'prepare-dirs.py','assertions_unchanged':True},indent=2)+'\n')
 p=dst/'run.sh';s=p.read_text();needle='sha256sum -c "$TASK_OWNER/harness.sha256"';assert s.count(needle)==1;s=s.replace(needle,needle+'\npython3 -I "$TASK_OWNER/prepare-dirs.py"');p.write_text(s)
 subprocess.run(['python3','-I',str(dst/'prepare-dirs.py')],check=True)
 for p in dst.iterdir():
  if p.suffix=='.py':ast.parse(p.read_text())
  if p.suffix=='.sh':subprocess.run(['bash','-n',str(p)],check=True)
 files=sorted(p for p in dst.iterdir() if p.is_file());(dst/'harness.sha256').write_text(''.join(f'{sha(p)}  {p}\n' for p in files))
 for p in files+[dst/'harness.sha256']:p.chmod(0o500 if p.suffix=='.sh' else 0o400)
 out.append({'prior':str(src),'owner':str(dst),'sealed_members':len(files),'seal_sha256':sha(dst/'harness.sha256')})
Path('/tmp/pixelelated-proxy11-chain.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'issue':445,'owners':out,'directory_controls':controls,'product_and_assertions_unchanged':True},indent=2)+'\n')
print('PASS fresh9-owner chain with explicit private directory setup, sealed sources and unchanged assertions')
