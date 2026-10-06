from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent;root=Path('/workspace/repos/rocknix');repo=Path('/workspace/repos/rocknix.worktrees/conflict-resolution');assert Path.cwd()==root
(owner/'run.path').write_text(str(root/os.environ['RASTERATOPS_BUILD_RUN'])+'\n');rc=1
try:
 for n,h in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h
 feature='e98339387135678f7ec82a8f90bde9643d2e4cd0';nex='ec2283f20f10e692f15bdb417917adb0e320155f'
 def git(where,*args):return subprocess.check_output(['git','-C',str(where),*args]).decode().strip()
 assert git(repo,'rev-parse','HEAD')==feature and git(root,'rev-parse','HEAD')==nex
 assert not git(root,'status','--porcelain')
 env=dict(os.environ,TMPDIR=str(owner/'tmp'))
 for where,branch,sha,label in [(repo,'feature/conflict-resolution',feature,'feature'),(root,'next',nex,'next')]:
  with (owner/(label+'-push.log')).open('x') as log:r=subprocess.run(['git','-C',str(where),'push','origin',sha+':refs/heads/'+branch],env=env,stdout=log,stderr=subprocess.STDOUT)
  assert r.returncode==0,label+' push failed; retained log'
  actual=git(where,'ls-remote','origin','refs/heads/'+branch).split()[0];assert actual==sha,(branch,actual)
  print('PASS normal guarded push and remote readback '+branch,flush=True)
 changed=git(repo,'diff','--name-only',feature+'^',feature).splitlines()
 def tree(sha):
  data=subprocess.check_output(['git','-C',str(repo),'ls-tree','-r','-z',sha]);return {n.split(b'\t',1)[1]:n.split(b'\t',1)[0] for n in data.split(b'\0') if n}
 a,b=tree(feature),tree(nex)
 for name in changed:assert a.get(os.fsencode(name))==b.get(os.fsencode(name)),name
 assert not list((owner/'tmp').iterdir()),'hook left temporary files'
 result=dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),feature=feature,next=nex,changed_paths=len(changed),changed_paths_equal=True,remote_refs_verified=True,normal_hooks=True,temporary_directory=str(owner/'tmp'),scope='Source repairs/evidence published; candidate15 remains unchanged; rebuilt installed acceptance pending')
 (owner/'publication.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
