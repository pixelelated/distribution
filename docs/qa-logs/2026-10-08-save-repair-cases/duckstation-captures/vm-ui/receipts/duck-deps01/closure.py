import pathlib,subprocess,os,json,hashlib,time
root=pathlib.Path('/storage/qa521/extract/squashfs-root');env=dict(os.environ);env['LD_LIBRARY_PATH']=str(root/'usr/lib');rows=[];start=time.monotonic();seen=set()
for p in sorted(root.rglob('*')):
 if not p.is_file() or p.is_symlink():continue
 with p.open('rb') as f:
  if f.read(4)!=b'\x7fELF':continue
 q=subprocess.run(['ldd',str(p)],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=10);out=q.stdout.decode(errors='replace');missing=[x.strip() for x in out.splitlines() if 'not found' in x or 'version ' in x or 'not a dynamic' in x];rows.append({'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exit':q.returncode,'issues':missing,'ldd':out})
print(json.dumps({'scope':'Every regular bundled ELF with exact extracted usr/lib resolution on actual guest; no application main executed','elapsed_seconds':time.monotonic()-start,'entries':rows},indent=2))
