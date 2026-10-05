from pathlib import Path
import hashlib,json,sys,tarfile,shutil
owner=Path(__file__).parent;bundle=Path(sys.argv[1]);stem='ROCKNIX-GENERIC_X64.x86_64-20260929'
system=owner/'baseline.SYSTEM'
with tarfile.open(bundle/(stem+'.tar')) as archive:
 member=archive.getmember(stem+'/target/SYSTEM');assert member.isfile()
 with archive.extractfile(member) as src,system.open('xb') as dst:shutil.copyfileobj(src,dst)
import subprocess
files={}
for name in ['usr/bin/cloud-signin-window','usr/bin/cloud_oauth']:
 data=subprocess.check_output(['unsquashfs','-cat',str(system),name]);files[name]=hashlib.sha256(data).hexdigest()
os_release=subprocess.check_output(['unsquashfs','-cat',str(system),'etc/os-release']).decode()
identity=dict(line.split('=',1) for line in os_release.splitlines() if '=' in line)
assert identity['BUILD_ID'].strip(chr(34))=='69e6039f8fdbf971d3e6b694537f250036fdcd98'
assert identity['OS_NAME'].strip(chr(34))=='ROCKNIX'
r={'identity':{k:identity[k] for k in ['BUILD_ID','OS_NAME']},'files':files,'source':'verified earlier update SYSTEM','build_id':'69e6039f8fdbf971d3e6b694537f250036fdcd98'}
with (owner/'expected-payload.json').open('x') as f:f.write(json.dumps(r,indent=2)+'\n')
(owner/'artifacts/baseline-payload.json').write_text(json.dumps(r,indent=2)+'\n')
system.unlink();print('PASS baseline hashes derived from verified earlier SYSTEM before guest startup')
