from pathlib import Path
import gzip,hashlib,json,os,shutil,struct,subprocess,tarfile,zlib
p=Path(__file__).resolve().parent;r=Path.cwd();build=Path('/workspace/tmp/pixelelated-m7-build20b');j=json.loads((build/'inputs.json').read_text())
verify=Path('/workspace/tmp/pixelelated-m7-build20-verify')
assert json.loads((build/'launcher-result.json').read_text())['runner_returncode']==1
assert json.loads((verify/'launcher-result.json').read_text())['runner_returncode']==0
resolution=json.loads((verify/'result.json').read_text());assert resolution['actual_build_container_returncode']==0 and resolution['original_wrapper_returncode']==1
(p/'run.path').write_text(str(r/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
proof=json.loads((verify/'installed-result.json').read_text());assert proof['identity']['BUILD_DIRTY']=='no'
for name,want in proof['artifacts'].items():assert digest(r/name)==want,name
files=[r/name for name in proof['artifacts']]
result=subprocess.check_output(['tools/rasteratops-candidate-store','put','--store','/workspace/artifacts/pixelelated-candidates','--inputs',str(build/'inputs.json'),*map(str,files)],text=True)
(p/'store.log').write_text(result);print(result,flush=True)
bundle=Path(result.strip().split('PASS candidate bundle ')[-1]);assert bundle.is_dir();(p/'bundle.path').write_text(str(bundle)+'\n')
meta=json.loads(next(bundle.glob('*.identity.json')).read_text());name=meta['image_name']
assert meta['build_commit']==j['distribution_commit'] and meta['dirty']=='no'
raw=p/'candidate.img'
with gzip.open(bundle/(name+'.img.gz'),'rb') as a,raw.open('xb') as b:shutil.copyfileobj(a,b,4*1024*1024)
with raw.open('rb') as f:
 def header(lba):
  f.seek(lba*512);h=bytearray(f.read(512));assert h[:8]==b'EFI PART';size=struct.unpack_from('<I',h,12)[0];want=struct.unpack_from('<I',h,16)[0];h[16:20]=b'\0'*4;assert zlib.crc32(h[:size])==want
  entry_lba=struct.unpack_from('<Q',h,72)[0];count,esize,tcrc=struct.unpack_from('<III',h,80);assert esize>=128 and count*esize<1024*1024
  f.seek(entry_lba*512);table=f.read(count*esize);assert zlib.crc32(table)==tcrc
  return h,table,esize
 h,table,esize=header(1);backup=struct.unpack_from('<Q',h,32)[0];bh,bt,besize=header(backup);assert bt==table and besize==esize
 first,last=struct.unpack_from('<QQ',table,32);assert first==8192 and first<=last<backup
mcopy=r/j['build_root']/'toolchain/bin/mcopy';payload={}
with tarfile.open(bundle/(name+'.tar')) as tf:
 for part in ['SYSTEM','KERNEL']:
  target=p/part;subprocess.run([str(mcopy),'-i',str(raw)+'@@'+str(first*512),'::/'+part,str(target)],check=True)
  member=tf.getmember(name+'/target/'+part);h=hashlib.sha256()
  with tf.extractfile(member) as f:
   for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
  actual=digest(target);assert h.hexdigest()==actual,part;payload[part]=actual
subprocess.run(['unsquashfs','-no-xattrs','-no-progress','-processors','2','-d',str(p/'root'),str(p/'SYSTEM')],check=True)
for target,source in proof['mapped_files'].items():assert (p/'root'/target).read_bytes()==(r/source).read_bytes(),target
assert (p/'root/etc/os-release').read_bytes()==(r/j['build_root']/'image/system/etc/os-release').read_bytes()
for name in ['emulationstation','rclone','cloud-signin-window']:assert digest(p/'root/usr/bin'/name)==digest(r/j['build_root']/'image/system/usr/bin'/name)
subprocess.run(['tools/rasteratops-candidate-store','verify',str(bundle)],check=True)
(p/'result.json').write_text(json.dumps({'result':'PASS','bundle':str(bundle),'payload_sha256':payload,'primary_and_backup_GPT_crc_valid':True,'system_first_sector':first,'system_last_sector':last,'installed_mappings':len(proof['mapped_files'])},indent=2)+'\n')
print('PASS immutable bundle, GPT CRCs, raw/update SYSTEM+KERNEL equality and extracted installed bytes',flush=True)

subprocess.run(['python3',str(p/'compare-installed.py')],check=True)
