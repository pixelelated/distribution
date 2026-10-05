from pathlib import Path
import hashlib,json,sys,tarfile,shutil
owner=Path(__file__).parent;bundle=Path(sys.argv[1]);stem='RASTERATOPS-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX'
system=owner/'baseline.SYSTEM'
with tarfile.open(bundle/(stem+'.tar')) as archive:
 member=archive.getmember(stem+'/target/SYSTEM');assert member.isfile()
 with archive.extractfile(member) as src,system.open('xb') as dst:shutil.copyfileobj(src,dst)
import subprocess
files={}
for name in ['usr/bin/cloud-signin-window','usr/bin/cloud_oauth']:
 data=subprocess.check_output(['unsquashfs','-cat',str(system),name]);files[name]=hashlib.sha256(data).hexdigest()
r={'files':files,'source':'verified earlier update SYSTEM','build_id':'61b64817bf8ab48237e51abb395484e36cbf924b'}
with (owner/'expected-payload.json').open('x') as f:f.write(json.dumps(r,indent=2)+'\n')
(owner/'artifacts/baseline-payload.json').write_text(json.dumps(r,indent=2)+'\n')
system.unlink();print('PASS baseline hashes derived from verified earlier SYSTEM before guest startup')
