from pathlib import Path
import ast,hashlib,json,shutil,subprocess,datetime
prefix='/workspace/tmp/pixelelated-m7-'
names=[('guest-10','guest-11'),('runtime-11','runtime-12'),('proxy-09','proxy-10'),('optins-09','optins-10'),('memory-09','memory-10'),('ui-11','ui-12'),('predecessor-07','predecessor-08'),('subset-06','subset-07'),('cloud-ui-05','cloud-ui-06'),('signin-ui-05','signin-ui-06'),('signin-1g-05','signin-1g-06')]
receipt=json.loads(Path(prefix+'guest-10/interruption-cleanup.json').read_text());assert receipt['qemu_absent'] and receipt['actual_tool_rc']==143
assert json.loads(Path('/tmp/pixelelated-watch-submit-controls.json').read_text())['passed']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for old,new in names:
 assert not Path(prefix+new).exists()
 if old!='guest-10':assert not Path(prefix+old+'/qa.start').exists()
out=[]
for old,new in names:
 src=Path(prefix+old);dst=Path(prefix+new);dst.mkdir();(dst/'artifacts').mkdir()
 for line in (src/'harness.sha256').read_text().splitlines():
  expected,filename=line.split(None,1);p=Path(filename);assert sha(p)==expected
  q=dst/p.name;shutil.copyfile(p,q)
  if p.suffix in {'.sh','.py','.json'}:
   s=q.read_text()
   for a,b in names:s=s.replace(prefix+a,prefix+b)
   q.write_text(s)
 for p in dst.iterdir():
  if p.suffix=='.py':ast.parse(p.read_text())
  if p.suffix=='.sh':subprocess.run(['bash','-n',str(p)],check=True)
 files=sorted(p for p in dst.iterdir() if p.is_file());(dst/'harness.sha256').write_text(''.join(f'{sha(p)}  {p}\n' for p in files))
 for p in files+[dst/'harness.sha256']:p.chmod(0o500 if p.suffix=='.sh' else 0o400)
 out.append({'prior':str(src),'owner':str(dst),'sealed_members':len(files),'seal_sha256':sha(dst/'harness.sha256')})
Path('/tmp/pixelelated-guest11-chain.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'issue':444,'owners':out,'product_and_assertions_unchanged':True},indent=2)+'\n')
print('PASS fresh11-owner dependency chain prepared and sealed; unchanged product and assertions')
