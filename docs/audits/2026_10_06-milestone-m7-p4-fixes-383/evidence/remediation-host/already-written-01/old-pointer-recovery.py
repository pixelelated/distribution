"""Already-written control: real old writer, preserved config, explicit folder repair."""
from pathlib import Path
import hashlib,importlib.machinery,importlib.util,json,subprocess,types
root=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15')
loader=importlib.machinery.SourceFileLoader('layout_cases',str(root/'tools/rasteratops-cloud-layout-test'))
spec=importlib.util.spec_from_loader(loader.name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m)
owner=Path(__file__).resolve().parent
args=types.SimpleNamespace(ref=None,rclone='/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement14/build.pixelelated-GENERIC_X64.x86_64/image/system/usr/bin/rclone')
oldref='7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2'
old=subprocess.check_output(['git','-C',str(root),'show',oldref+':projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout'])
results=[]
for mode in ['--join','--follow','--settle']:
 f=m.Fixture(owner/mode[2:],args)
 (f.path/'repo/predecessor').write_bytes(old);(f.path/'repo/predecessor').chmod(0o755)
 if mode=='--join':
  f.conf('/GAMES','/GAMES/backup','/GAMES/Content');f.file('/ROCKNIX/Saves/gb/A.srm','save\n');target='/ROCKNIX'
 else:
  f.conf('/ROCKNIX/Saves','/ROCKNIX/Backups','/ROCKNIX/Content');target='/pixelelated'
  if mode=='--follow':f.file('/pixelelated/Saves/gb/A.srm','save\n')
 before=m.cloud_hashes(f)
 m.put(f.path/'shim/sed','#!/bin/bash\nif [[ "$*" == *"^SETTINGS_REMOTE="* ]]; then echo fired > /ctl/pointer-fired; exit 1; fi\nexec /usr/bin/sed "$@"\n',True)
 first=f.run('predecessor',mode)
 assert first.returncode!=0 and (f.path/'ctl/pointer-fired').exists()
 (f.path/'shim/sed').unlink()
 partial=f.pointers();assert partial['SAVES_REMOTE']==target+'/Saves'
 assert partial['SETTINGS_REMOTE']!=target+'/Backups'
 assert before==m.cloud_hashes(f)
 state=f.run('cloud_migrate_layout','--state');assert state.returncode==0
 # The retained mixed choices are readable, never inferred to be a new cloud.
 # Only the player's existing CHANGE CLOUD FOLDER action selects siblings.
 repaired=f.run('cloud_setup','--set-saves-remote',target+'/Saves')
 assert repaired.returncode==0,repaired.stdout
 assert all(f.pointers()[k]==target+'/'+tier for k,tier in [('SAVES_REMOTE','Saves'),('SETTINGS_REMOTE','Backups'),('CONTENT_REMOTE','Content')])
 assert before==m.cloud_hashes(f)
 result={'mode':mode,'old_writer':oldref,'old_sha256':hashlib.sha256(old).hexdigest(),'old_rc':first.returncode,'partial':partial,'state_after_upgrade':state.stdout,'explicit_repair':'cloud_setup --set-saves-remote '+target+'/Saves','repaired':f.pointers(),'cloud_unchanged':True}
 results.append(result);(owner/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 print('PASS already-written '+mode+' explicit folder-selection repair',flush=True)
