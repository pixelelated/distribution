from pathlib import Path
import hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent;root=Path('/workspace/repos/rocknix')
assert Path.cwd()==root
(owner/'run.path').write_text(str(root/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
 for n,h in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
 rc=subprocess.run([sys.executable,'-I',str(owner/'publish.py')]).returncode
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
