from pathlib import Path
import datetime,hashlib,json,os,signal,subprocess,sys
owner=Path(__file__).resolve().parent
tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16')
bundle=Path(sys.argv[1]).resolve(strict=True)
assert Path.cwd()==tree
assert not (owner/'qa.start').exists()
(owner/'qa.start').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')
(owner/'run.path').write_text(str(tree/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
code=1
try:
 for name,digest in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
 os.environ['ES_SRC']='/home/max/Development/emulationstation-next.worktrees/qa-integration'
 subprocess.run([sys.executable,'-I',str(owner/'verify-inputs.py'),str(bundle)],check=True)
 subprocess.run([str(tree/'tools/rasteratops-candidate-store'),'verify',str(bundle)],check=True)
 signal.signal(signal.SIGINT,signal.SIG_DFL)
 code=subprocess.run([sys.executable,'-I',str(owner/'extra-boundaries.py'),'--tree',str(tree),'--image',str(bundle/'pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz'),'--build-id','ee014909137e03706e0b3020b8396be589aaa705','--output',str(owner/'proof')]).returncode
 subprocess.run([sys.executable,'-I',str(owner/'verify-inputs.py'),str(bundle)],check=True)
 for name,digest in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
except BaseException:
 code=1;raise
finally:
 (owner/'inner.rc').write_text(str(code)+'\n');(owner/'outer.rc').write_text(str(code)+'\n')
sys.exit(code)
