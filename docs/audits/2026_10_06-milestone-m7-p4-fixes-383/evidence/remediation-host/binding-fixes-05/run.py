from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
owner=Path(__file__).resolve().parent
assert not (owner/'started').exists()
(owner/'started').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat())
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
seal=json.loads((owner/'seal.json').read_text());code=1
try:
 for name,digest in seal.items(): assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
 code=subprocess.run([sys.executable,'-I',str(owner/'tree/tools/rasteratops-cloud-layout-test'),'--case','PL004','--output',str(owner/'proof'),'--rclone','/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement14/build.pixelelated-GENERIC_X64.x86_64/image/system/usr/bin/rclone']).returncode
 for name,digest in seal.items(): assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
finally:
 (owner/'inner.rc').write_text(str(code)+'\n');(owner/'outer.rc').write_text(str(code)+'\n')
sys.exit(code)
