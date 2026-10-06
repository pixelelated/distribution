from pathlib import Path
import hashlib, importlib.machinery, importlib.util, json, re, subprocess, types
owner=Path(__file__).resolve().parent
tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15')
loader=importlib.machinery.SourceFileLoader('layout_fixture',str(tree/'tools/rasteratops-cloud-layout-test'))
spec=importlib.util.spec_from_loader(loader.name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m)
rclone=tree/'build.pixelelated-GENERIC_X64.x86_64/image/system/usr/bin/rclone'
version=subprocess.check_output([str(rclone),'version'],text=True).splitlines()[0]
assert 'v1.75.1' in version
results=[]
for name,deny_copy in [('parent-only-fallback',False),('parent-and-copy-failure',True)]:
 f=m.Fixture(owner/'artifacts'/name,types.SimpleNamespace(ref=None,rclone=str(rclone)))
 f.conf('/ROCKNIX/Saves','/ROCKNIX/Backups','/ROCKNIX/Content')
 f.file('/ROCKNIX/Saves/gb/CloudOnly.srm','cloud-only witness\n')
 m.put(f.path/'storage/roms/gb/Local.srm','local unsent witness\n')
 m.put(f.path/'ctl/bucket','1')
 f.fault(r'^lsf --dirs-only qa:/ROCKNIX/?( |$)',5)
 if deny_copy:
  with (f.path/'ctl/faults').open('a') as s:s.write(r'^copy .* /storage/roms/? qa:/ROCKNIX/Saves/?( |$)'+'\t5\n')
 cloud=f.path/'cloud/ROCKNIX/Saves/gb/CloudOnly.srm';local=f.path/'storage/roms/gb/Local.srm'
 original={'cloud':hashlib.sha256(cloud.read_bytes()).hexdigest(),'local':hashlib.sha256(local.read_bytes()).hexdigest(),'pointers':f.pointers()}
 first=f.run('cloud_backup','--yes','--saves-only')
 fired=(f.path/'ctl/fault-fired').read_text().splitlines()
 assert any(re.search(r'^lsf --dirs-only qa:/ROCKNIX/?( |$)',x) for x in fired),'parent guard not reached'
 assert '>>> offer create-saves-folder' not in first.stdout,'unknown listing became absence'
 assert hashlib.sha256(cloud.read_bytes()).hexdigest()==original['cloud']
 assert hashlib.sha256(local.read_bytes()).hexdigest()==original['local']
 assert f.pointers()==original['pointers']
 sent=f.path/'cloud/ROCKNIX/Saves/gb/Local.srm'
 if deny_copy:
  assert any(re.search(r'^copy .* /storage/roms/? qa:/ROCKNIX/Saves/?( |$)',x) for x in fired),'intended real copy fault did not fire'
  assert first.returncode!=0 and "Couldn't finish" in first.stdout,'denied copy did not report failure'
  assert any(x.startswith('copy ') for x in fired),'copy fault did not fire'
  assert not sent.exists(),'denied copy uploaded local witness'
 else:
  assert first.returncode==0 and 'Completed.' in first.stdout,'permitted fallback did not complete'
  assert sent.read_bytes()==local.read_bytes(),'fallback did not upload actual bytes'
 (f.path/'ctl/faults').unlink()
 m.put(f.path/'storage/roms/gb/After.srm','new retry witness\n')
 second=f.run('cloud_backup','--yes','--saves-only')
 assert second.returncode==0 and 'Completed.' in second.stdout,'retry did not complete truthfully'
 assert sent.read_bytes()==local.read_bytes()
 assert (f.path/'cloud/ROCKNIX/Saves/gb/After.srm').read_bytes()==b'new retry witness\n'
 assert hashlib.sha256(cloud.read_bytes()).hexdigest()==original['cloud']
 assert f.pointers()==original['pointers']
 result={'case':name,'status':'PASS','first_rc':first.returncode,'retry_rc':second.returncode,'fault_calls':fired,'before':original,'after_cloud':m.cloud_hashes(f),'interpretation':'Failed parent listing is unknown. Production deliberately permits backup fallback. Nonzero failure requires the separately injected copy refusal.'}
 results.append(result)
 (owner/'artifacts/results.json').write_text(json.dumps({'rclone_version':version,'rclone_sha256':hashlib.sha256(rclone.read_bytes()).hexdigest(),'results':results},indent=2)+'\n')
 print('PASS '+name,flush=True)
