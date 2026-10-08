from pathlib import Path
import datetime,hashlib,json,os,socket,time
O=Path(__file__).resolve().parent;j=json.loads((O/'inputs.json').read_text());deadline=time.monotonic()+120
while True:
 try:data=(O/'container-observed.json').read_bytes();r=json.loads(data);break
 except (OSError,json.JSONDecodeError):
  assert time.monotonic()<deadline,'No verified container startup within120seconds; compilation did not run'
  time.sleep(1)
assert r['state']['Running'] and r['id'].startswith(socket.gethostname())
assert r['image']==j['container_image_id'] and r['reference']==j['container'] and r['user']=='1000:1000'
assert r['workdir']==j['container_worktree'] and Path.cwd()==Path(j['container_worktree'])
for source,dest,rw in [(j['host_worktree'],j['container_worktree'],True),(str(O),str(O),True),(j['nix_private_store'],'/nix',True),(j['nix_snapshot'],j['nix_snapshot'],False)]:
 assert any(m['Source']==source and m['Destination']==dest and m['RW']==rw for m in r['mounts']),(source,dest,rw)
assert os.getuid()==1000
for p in [Path('/nix'),O,Path.cwd(),Path.cwd()/j['build_root'],Path.cwd()/'sources']:assert p.is_dir() and os.access(p,os.W_OK),p
for k,h in j['nix_toolchain_hashes'].items():assert hashlib.sha256(Path(k).read_bytes()).hexdigest()==h,k
with (O/'artifacts/container-gate.json').open('x') as f:json.dump({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','container':r['id'],'image':r['image'],'runtime_receipt_sha256':hashlib.sha256(data).hexdigest(),'nix_writable':True,'scope':'Actual pinned container and exact writable private Nix/read-only snapshot mounts verified before any proof/build work'},f,indent=2)
print('PASS actual container and Nix gate before build',flush=True)
