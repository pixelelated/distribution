from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
owner=Path(__file__).parent;tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement17');build=Path('/workspace/tmp/pixelelated-m7-replacement-17');run=Path((build/'run.path').read_text().strip())
assert Path.cwd()==tree
assert json.loads((build/'completion.json').read_text())['result']=='PASS'
assert not (owner/'qa.start').exists()
(owner/'qa.start').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')
(owner/'run.path').write_text(str(tree/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
result=1
try:
 for n,h in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
 subprocess.run(['python3','-I',str(build/'verify-source.py')],check=True)
 artifacts=sorted((tree/'target').iterdir())
 assert len(artifacts)==4 and all(p.is_file() for p in artifacts)
 artifacts += [run/'build.log',run/'build.status']+[build/n for n in ['completion.json','copy-verification.json','cache-ready.json','cache-compare.txt','copy-input-proof.json','freeze-receipt.json','host-preflight.txt','capacity.json']]
 proc=subprocess.run([str(tree/'tools/rasteratops-candidate-store'),'put','--store','/workspace/artifacts/pixelelated-candidates','--inputs',str(build/'inputs.json'),*map(str,artifacts)],text=True,capture_output=True)
 print(proc.stdout,flush=True);print(proc.stderr,file=sys.stderr,flush=True);proc.check_returncode()
 (owner/'store.log').write_text(proc.stdout+proc.stderr)
 bundle=Path(proc.stdout.splitlines()[-1].removeprefix('PASS candidate bundle '));assert bundle.is_dir() and json.loads((bundle/'manifest.json').read_text())['inputs']==json.loads((build/'inputs.json').read_text())
 subprocess.run([str(tree/'tools/rasteratops-candidate-store'),'verify',str(bundle)],check=True)
 (owner/'bundle.path').write_text(str(bundle)+'\n')
 for n,h in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
 result=0
finally:
 (owner/'inner.rc').write_text(str(result)+'\n');(owner/'outer.rc').write_text(str(result)+'\n')
sys.exit(result)
