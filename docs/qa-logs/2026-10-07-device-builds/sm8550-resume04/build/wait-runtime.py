"""Block all proof/build work until the controller observes this exact container."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,socket,time
owner=Path(__file__).resolve().parent
j=json.loads((owner/'inputs.json').read_text())
receipt=owner/'runtime-start.json';deadline=time.monotonic()+120
while True:
    try:
        data=receipt.read_bytes();runtime=json.loads(data);break
    except (OSError,json.JSONDecodeError):
        assert time.monotonic()<deadline,'Controller did not publish verified container startup within120seconds; no proof/build work ran'
        print('Waiting for controller-verified container identity before proof/build work',flush=True)
        time.sleep(1)
assert runtime['state']=='running' and len(runtime['containers'])==1
row=runtime['containers'][0]
assert row['image']==j['container_image_id'] and row['state']=='running'
assert row['id'].startswith(socket.gethostname()),'Startup receipt belongs to another container'
mounts={r['source']:(r['destination'],r['rw']) for r in row['mounts']}
assert mounts[str(owner)]==(str(owner),True)
assert mounts[j['host_worktree']]==(j['host_worktree'],True)
assert mounts[j['nix_private_store']]==('/nix',True)
assert mounts[j['nix_snapshot']]==(j['nix_snapshot'],False)
assert os.getuid()!=0
root=Path(j['host_worktree'])
for p in [Path('/nix'),owner,root,root/j['build_root'],root/'sources']:
    assert p.is_dir() and os.access(p,os.W_OK),str(p)+' must be writable for canonical build entrypoints'
for name,value in [('PROJECT','ROCKNIX'),('DEVICE','SM8550'),('ARCH','aarch64'),('CUSTOM_VERSION','0.0.1')]:assert os.environ.get(name)==value,name
with (owner/'artifacts/container-gate.json').open('x') as out:
    json.dump({'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS','container':row['id'],'image':row['image'],'runtime_receipt_sha256':hashlib.sha256(data).hexdigest(),'nix_writable':True,'uid':os.getuid(),'scope':'Controller observed exact container and mounts before any proof/build work'},out,indent=2);out.write('\n')
print('PASS observed container gate, writable active Nix cache and build paths',flush=True)
