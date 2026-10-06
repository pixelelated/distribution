from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent;tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15');bundle=Path(sys.argv[1]).resolve(strict=True)
assert Path.cwd()==tree and not (owner/'qa.start').exists()
(owner/'qa.start').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n');(owner/'run.path').write_text(str(tree/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
code=1
try:
 for n,h in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
 os.environ['ES_SRC']='/home/max/Development/emulationstation-next.worktrees/qa-integration'
 subprocess.run([sys.executable,'-I',str(owner/'verify-inputs.py'),str(bundle)],check=True)
 code=subprocess.run([sys.executable,'-I',str(owner/'proof.py')]).returncode
 for n,h in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
except BaseException:code=1;raise
finally:
 (owner/'inner.rc').write_text(str(code)+'\n');(owner/'outer.rc').write_text(str(code)+'\n')
sys.exit(code)
