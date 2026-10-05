from pathlib import Path
import hashlib,json,subprocess,sys,datetime
owner=Path('/workspace/tmp/pixelelated-m7-qa-17')
old=Path('/workspace/tmp/pixelelated-m7-qa-15/pair/vm-a.qcow2')
new=owner/'pair/vm-a.qcow2'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
receipt=owner/'artifacts/upgraded-disk-custody.json'
if '--verify-original' in sys.argv:
 assert sha(old)==json.loads(receipt.read_text())['original_sha256']
 print('PASS original QA15 upgraded disk unchanged');sys.exit(0)
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try:a=p.read_bytes().split(b'\0')
 except (OSError,UnicodeError):continue
 if a and Path(a[0].decode(errors='replace')).name.startswith('qemu-system-'):raise RuntimeError('existing QEMU')
assert not new.exists()
before=sha(old)
subprocess.run(['qemu-img','convert','-f','qcow2','-O','qcow2',str(old),str(new)],check=True)
subprocess.run(['qemu-img','compare','-f','qcow2','-F','qcow2',str(old),str(new)],check=True)
assert sha(old)==before and old.stat().st_ino!=new.stat().st_ino
info=json.loads(subprocess.check_output(['qemu-img','info','--output=json',str(new)],text=True))
assert 'backing-filename' not in info
receipt.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original':str(old),'original_sha256':before,'copy':str(new),'copy_initial_sha256':sha(new),'guest_bytes_equal':True,'independent_inode':True,'info':info},indent=2)+'\n')
print('PASS independent byte-equivalent copy of actual QA15 upgraded disk')
