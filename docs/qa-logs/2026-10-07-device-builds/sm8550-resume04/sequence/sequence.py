"""Fresh watched recovery/build/acceptance controller; root handles issue updates."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,time
owner=Path(__file__).resolve().parent
c=json.loads((owner/'configuration.json').read_text())
tree=Path(c['tree']);primary=Path('/workspace/repos/rocknix')
build=Path(c['build_owner']);accept=Path(c['accept_owner'])
def now():return datetime.now(timezone.utc).isoformat()
def read(p):return json.loads(Path(p).read_text())
def write(p,j):
 with p.open('x') as f:json.dump(j,f,indent=2);f.write('\n')
def state(phase,**kw):
 j={'utc':now(),'pid':os.getpid(),'phase':phase,**kw};p=owner/'state.new';p.write_text(json.dumps(j,indent=2)+'\n');p.replace(owner/'state.json');print(json.dumps(j),flush=True)
def submit(p,cwd):
 subprocess.run(['python3','-I',str(owner/'watch-build-submit.py'),'--owner',str(p),'--','--','python3','-I',str(p/'run.py')],cwd=cwd,check=True)
def exited(p):
 if not (p/'launcher-result.json').exists():return False
 run=Path((p/'run.path').read_text().strip())
 pids=[read(p/'launcher-pid.json')['pid']]+[int((run/n).read_text()) for n in ['build.pid','watcher.pid','command.pid']]
 return not any(Path('/proc',str(pid)).exists() for pid in pids)
def consume(p,phase):
 while not exited(p):state(phase,active_owner=str(p));time.sleep(30)
 if not (p/'owner-verification.json').exists():subprocess.run(['python3','-I',str(owner/'verify-owner.py'),str(p)],check=True)
 j=read(p/'owner-verification.json');assert j['result']=='PASS',(str(p),j['channels'])
def runtime():
 ids=subprocess.check_output(['docker','ps','-q','--no-trunc'],text=True).split()
 rows=json.loads(subprocess.check_output(['docker','inspect',*ids],text=True)) if ids else []
 rows=[r for r in rows if any(m['Source']==str(tree) for m in r['Mounts'])]
 if not rows:return False
 assert len(rows)==1;row=rows[0];j=read(build/'inputs.json');assert row['Image']==j['container_image_id'] and row['State']['Running']
 mounts={m['Source']:(m['Destination'],m['RW']) for m in row['Mounts']}
 for src,dst,rw in [(str(tree),str(tree),True),(str(build),str(build),True),('/workspace/repos/rocknix/.git','/workspace/repos/rocknix/.git',True),(j['source_cache'],str(tree/'sources'),True),(j['nix_private_store'],'/nix',True),(j['nix_snapshot'],j['nix_snapshot'],False)]:assert mounts.get(src)==(dst,rw),(src,mounts.get(src))
 write(build/'runtime-start.json',{'utc':now(),'state':'running','containers':[{'id':row['Id'],'image':row['Image'],'state':row['State']['Status'],'host_pid':row['State']['Pid'],'mounts':[{'source':m['Source'],'destination':m['Destination'],'rw':m['RW']} for m in row['Mounts']]}]})
 return True
result={'result':'FAILED'}
try:
 for p,h in read(owner/'seal.json').items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
 write(owner/'controller-start.json',{'utc':now(),'pid':os.getpid(),'start_ticks':Path('/proc/self/stat').read_text().rsplit(')',1)[1].split()[19]})
 assert not any((p/'launcher-submission.json').exists() for p in [build,accept])
 # Read-only preflight; unchanged source. No reclamation or re-clean.
 state('read-only-host-preflight')
 with (owner/'host-preflight.log').open('x') as out:preflight=subprocess.run([str(primary/'tools/build-preflight')],cwd=primary,stdout=out,stderr=subprocess.STDOUT)
 write(owner/'host-preflight-result.json',{'utc':now(),'returncode':preflight.returncode});assert preflight.returncode==0
 assert read(Path(c['failed_owner'])/'owner-verification.json')['result']=='FAILED'
 ids=subprocess.check_output(['docker','ps','-q'],text=True).split()
 running=json.loads(subprocess.check_output(['docker','inspect',*ids],text=True)) if ids else []
 assert not [r for r in running if any(m['Source']==str(tree) for m in r['Mounts'])],'Existing container still consumes build tree'
 assert subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()==c['old_commit']
 assert not subprocess.check_output(['git','-C',str(tree),'status','--porcelain'],text=True).strip()
 assert subprocess.check_output(['git','-C',str(tree),'diff','--name-only',c['old_commit'],c['new_commit'],'--',*c['product_roots']],text=True).splitlines()==c['product_delta']
 subprocess.run(['python3','-I',str(build/'verify-source.py')],cwd=tree,check=True)
 subprocess.run(['python3','-I',str(owner/'verify-arm.py')],check=True)
 submit(build,tree);state('SM8550-builder-starting',active_owner=str(build))
 for attempt in range(60):
  if runtime():break
  assert not (build/'launcher-result.json').exists(),'Builder exited before verified container startup'
  time.sleep(2)
 else:raise RuntimeError('Build startup was not observed; inspect retained owner before restarting anything')
 submit(accept,primary)
 write(owner/'tracker-handoff-started.json',{'utc':now(),'issues':[506,503,502,492],'milestone':7,'state':'BUILDING','commit':c['new_commit'],'owners':[str(build),str(accept)],'scope':'Root updates ordered tracking; this controller does not send external messages'})
 consume(accept,'SM8550-build-and-artifact-verification')
 assert read(accept/'artifacts/acceptance.json')['result']=='PASS'
 subprocess.run(['python3','-I',str(owner/'verify-arm.py')],check=True)
 result={'result':'PASS','acceptance':str(accept/'artifacts/acceptance.json'),'scope':'Corrected SM8550 artifacts accepted; physical testing/source publication remain separate','retirement_due':['/workspace/tmp/pixelelated-m7-sm8550-build-02/nix','/workspace/tmp/pixelelated-m7-sm8550-recovery-01/preserved']}
except Exception as error:
 result['error']=repr(error);raise
finally:
 result['utc']=now();write(owner/'controller-result.json',result)
 write(owner/'tracker-handoff-terminal.json',{'utc':now(),'issues':[506,503,502,492],'milestone':7,'result':result})
 state('complete' if result['result']=='PASS' else 'needs-review',result=result)
