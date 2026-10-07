"""Preserve interrupted scopes, then advance the stopped checkout; never launch builds."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,subprocess,sys,tarfile
owner=Path(__file__).resolve().parent
sequence=Path('/workspace/tmp/pixelelated-m7-sm8550-sequence-02')
config=json.loads((sequence/'configuration.json').read_text())
tree=Path(config['tree']);root=tree/'build.pixelelated-SM8550.aarch64'
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def read(p):return json.loads(Path(p).read_text())
try:
 for p,h in read(owner/'seal.json').items():assert sha(p)==h,p
 assert config['old_commit']==subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()
 assert not subprocess.check_output(['git','-C',str(tree),'status','--porcelain'],text=True).strip()
 for name in ['pixelelated-m7-sm8550-build-01','pixelelated-m7-sm8550-acceptance-01']:
  receipt=read(Path('/workspace/tmp')/name/'owner-verification.json');assert receipt['result']=='FAILED'
 assert read('/workspace/tmp/pixelelated-m7-sm8550-acceptance-01/artifacts/acceptance.json')['container_exited'] is True
 for p in config['controls']:
  assert read(Path(p)/'owner-verification.json')['result']=='PASS'
 subprocess.run(['python3','-I','/workspace/tmp/pixelelated-m7-sm8550-build-01/verify-source.py'],cwd=tree,check=True)
 ids=subprocess.check_output(['docker','ps','-q'],text=True).split()
 containers=json.loads(subprocess.check_output(['docker','inspect',*ids],text=True)) if ids else []
 assert not [c for c in containers if any(m['Source']==str(tree) for m in c['Mounts'])], 'Original tree still mounted by running container'
 assert not list((root/'.unpack').iterdir()),'Unexpected incomplete extraction requires classification'
 arm=subprocess.run(['python3','-I',str(sequence/'verify-arm.py')],check=True,capture_output=True,text=True)
 (owner/'artifacts/arm-before.txt').write_text(arm.stdout)
 archive=owner/'artifacts/failure-threads-stamps.tar.gz'
 with tarfile.open(archive,'w:gz') as tf:
  for name in ['.threads','.stamps']:tf.add(root/name,arcname=name)
 with tarfile.open(archive) as tf:
  assert tf.getmember('.threads/status').isfile() and tf.getmember('.stamps').isdir()
 original=read(sequence/'scope-readback.json')
 for row in original['incomplete_scopes']:
  assert sha(row['log'])==row['log_sha256']
  assert not (root/'.stamps'/row['package']/'build_target').exists()
  assert sorted(p.name for p in (root/'.stamps'/row['package']).iterdir())==row['stamp_names']
 paths=[Path(p) for row in original['incomplete_scopes'] for p in row['preserve_then_recreate_paths']]
 if (root/'image').exists():paths.append(root/'image')
 hold=owner/'preserved';hold.mkdir();plan=[]
 for p in sorted(set(paths)):
  st=p.stat();dest=hold/p.relative_to(root)
  assert not dest.exists() and st.st_dev==hold.stat().st_dev
  plan.append({'source':str(p),'destination':str(dest),'device':st.st_dev,'inode':st.st_ino})
 (owner/'artifacts/recovery-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
 for row in plan:
  src=Path(row['source']);dst=Path(row['destination']);dst.parent.mkdir(parents=True,exist_ok=True);src.rename(dst)
  assert not src.exists() and (dst.stat().st_dev,dst.stat().st_ino)==(row['device'],row['inode'])
 # Preserve source identity before the new freeze; old receipts remain historical.
 subprocess.run(['git','-C',str(tree),'merge','--ff-only',config['new_commit']],check=True)
 assert subprocess.check_output(['git','-C',str(tree),'diff','--name-only',config['old_commit'],config['new_commit'],'--',*config['product_roots']],text=True).splitlines()==config['product_delta']
 result={'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS','old_commit':config['old_commit'],'new_commit':config['new_commit'],'interrupted_packages':[r['package'] for r in original['incomplete_scopes']],'preserved_by_rename':plan,'archive':str(archive),'archive_sha256':sha(archive),'deleted_payloads':0,'scope':'Stopped checkout refrozen after exact interrupted-output preservation'}
 (owner/'artifacts/recovery.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
