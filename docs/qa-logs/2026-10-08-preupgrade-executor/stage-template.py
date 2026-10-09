import base64,hashlib,json,os,pathlib,sys,zlib
payload=json.loads(zlib.decompress(base64.b64decode(PAYLOAD)))
assert set(payload)=={'operation.py','inspect.py','plan.json'}
root=pathlib.Path('/storage/.cache')/STAGE_NAME
assert root.parent.is_dir() and not root.parent.is_symlink()
assert not root.exists() and not root.is_symlink()
os.umask(0o077);root.mkdir(mode=0o700)
for name,entry in payload.items():
 data=base64.b64decode(entry['bytes']);assert hashlib.sha256(data).hexdigest()==entry['sha256']
 with (root/name).open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 assert (root/name).stat().st_mode&0o777==0o600
 assert hashlib.sha256((root/name).read_bytes()).hexdigest()==entry['sha256']
fd=os.open(root,os.O_RDONLY|os.O_DIRECTORY);os.fsync(fd);os.close(fd);os.sync()
print('PASS private operation packet staged and hash verified',flush=True)
