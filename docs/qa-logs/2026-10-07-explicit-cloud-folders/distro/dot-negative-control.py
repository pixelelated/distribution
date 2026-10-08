from pathlib import Path
import runpy,types,hashlib,json,shutil
root=Path('/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders')
m=runpy.run_path(str(root/'tools/pixelelated-cloud-folder-test'))
old=Path('/tmp/pixelelated-508-dot-control/cloud_setup')
assert hashlib.sha256(old.read_bytes()).hexdigest()=='7b3e080a5bbf233c512ee061f1c0ffc1a41cc8bd65a2e23fd69432b436be8e8d'
out=Path('/tmp/pixelelated-508-dot-control/artifacts');out.mkdir()
args=types.SimpleNamespace(ref=None,rclone='/workspace/repos/rocknix.worktrees/generic-x64/build.ROCKNIX-GENERIC_X64.x86_64/image/system/usr/bin/rclone')
results=[]
for tier in ['saves','backups']:
 f=m['legacy'].Fixture(out/tier,args);shutil.copyfile(old,f.path/'repo/cloud_setup')
 values={'saves':'/Mine/Saves','backups':'/Mine/Backups','content':'/Mine/Content'};values[tier]='./';f.conf(**values)
 f.file('/owner.txt','root sentinel\n');before=m['snapshot'](f)
 r=f.run('cloud_setup','--seed-folders');after=m['snapshot'](f)
 required='pixelelated/'+('Saves' if tier=='saves' else 'Backups')+'/README.txt'
 assert r.returncode==0 and required in after[1] and before[0]==after[0],(tier,r.returncode,r.stdout)
 result={'tier':tier,'old_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'expected_old_behavior_observed':'wrong fresh-default namespace seeded while selected dot-root remained unchanged','rc':r.returncode,'before_cloud':before[1],'after_cloud':after[1]}
 (f.path/'result.json').write_text(json.dumps(result,indent=2)+'\n');results.append(result)
 for name in ['repo','shim','storage','cloud','ctl','log','run']:shutil.rmtree(f.path/name)
 print('VERIFIED expected predecessor failure:',tier,flush=True)
(out/'result.json').write_text(json.dumps(results,indent=2)+'\n')
