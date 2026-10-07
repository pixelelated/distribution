from pathlib import Path
import hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
 for path,sha in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha
 subprocess.run(['python3','-I','/workspace/repos/rocknix.worktrees/conflict-resolution/docs/qa-logs/2026-10-07-pixelelated-replacement-16/h700-retirement-proposal/execute.py','--owner',str(owner)],check=True)
 assert not (owner/'execution.json').exists()
 rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
