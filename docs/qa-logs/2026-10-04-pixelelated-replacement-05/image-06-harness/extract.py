from pathlib import Path
import gzip,hashlib,json,shutil,struct,subprocess,sys,tarfile
owner=Path(__file__).parent;bundle=Path(sys.argv[1]);name='pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX'
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
raw=owner/'candidate.img'
print('START raw image decompression',flush=True)
with gzip.open(bundle/(name+'.img.gz'),'rb') as src,raw.open('xb') as dst:shutil.copyfileobj(src,dst,4*1024*1024)
with raw.open('rb') as f:
 f.seek(512);header=f.read(92);assert header[:8]==b'EFI PART'
 entries=struct.unpack_from('<Q',header,72)[0];size=struct.unpack_from('<I',header,84)[0];assert size>=128
 f.seek(entries*512);entry=f.read(size);first,last=struct.unpack_from('<QQ',entry,32)
 assert first==8192 and last>=first
print('PASS raw GPT system partition starts at sector8192',flush=True)
mcopy='/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement05/build.pixelelated-GENERIC_X64.x86_64/toolchain/bin/mcopy'
subprocess.run([mcopy,'-i',str(raw)+'@@'+str(first*512),'::/SYSTEM',str(owner/'SYSTEM')],check=True)
with tarfile.open(bundle/(name+'.tar')) as tf:
 member=tf.getmember(name+'/target/SYSTEM');h=hashlib.sha256()
 with tf.extractfile(member) as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 tar_hash=h.hexdigest()
image_hash=digest(owner/'SYSTEM');assert image_hash==tar_hash
(owner/'artifacts/payload-equality.json').write_text(json.dumps({'candidate_bundle':bundle.name,'image_SYSTEM_sha256':image_hash,'update_SYSTEM_sha256':tar_hash,'system_partition_start_sector':first,'system_partition_end_sector':last,'same_bytes':True},indent=2)+'\n')
print('PASS raw image SYSTEM equals update tar SYSTEM',image_hash,flush=True)
subprocess.run(['unsquashfs','-no-xattrs','-no-progress','-processors','2','-d',str(owner/'root'),str(owner/'SYSTEM')],check=True)
print('PASS immutable candidate filesystem extracted without executing it',flush=True)
