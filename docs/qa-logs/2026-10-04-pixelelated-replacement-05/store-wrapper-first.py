from pathlib import Path
import hashlib,json,datetime,subprocess
owner=Path('/workspace/tmp/pixelelated-m7-replacement-05');tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement05');r=Path((owner/'run.path').read_text().strip())
for name in ['build.pid','watcher.pid']:
 pid=int((r/name).read_text());assert not Path('/proc',str(pid)).exists(),pid
checks={str(p):p.read_text().strip() for p in [owner/'inner.rc',owner/'outer.rc',owner/'tool-wrapper.rc',r/'build.rc']};assert set(checks.values())=={'0'}
container=json.loads((owner/'container-actual.json').read_text());ids=subprocess.check_output(['docker','ps','-q','--no-trunc'],text=True).split();assert container['id'] not in ids
j={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_tool':62521,'actual_exit_code':0,'result_channels':checks,'runner_and_watcher_exited':True,'owned_container_exited':True,'build_log_sha256':hashlib.sha256((r/'build.log').read_bytes()).hexdigest()};(owner/'completion.json').write_text(json.dumps(j,indent=2)+'\n')
stem='pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX';artifacts=[]
for ext in ['img.gz','tar']:
 p=tree/'target'/(stem+'.'+ext);sumfile=p.with_name(p.name+'.sha256');digest=hashlib.sha256(p.read_bytes()).hexdigest();assert sumfile.read_text().split()[0]==digest
 print(ext,p.stat().st_size,digest,flush=True);artifacts += [str(p),str(sumfile)]
files=artifacts+[str(r/'build.log'),str(r/'build.status')]+[str(owner/n) for n in ['completion.json','container-actual.json','host-preflight.txt','package-freshness.log','cache-ready.json','prelaunch-host.txt']]
out=subprocess.check_output([str(tree/'tools/rasteratops-candidate-store'),'put','--store','/workspace/artifacts/pixelelated-candidates','--inputs',str(owner/'inputs.json'),*files],text=True);print(out,flush=True)
# Tool emits the verified path on its final line.
last=out.strip().splitlines()[-1];path=Path(last);assert path.is_dir(),last
(owner/'bundle.path').write_text(str(path)+'\n')
