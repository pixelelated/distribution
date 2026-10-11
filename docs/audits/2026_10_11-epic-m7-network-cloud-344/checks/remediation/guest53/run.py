from pathlib import Path
import importlib.util,subprocess,tarfile,json,hashlib
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
D=Path('/workspace/repos/rocknix.worktrees/m7-cloud-connections');O=Path('/workspace/tmp/pix540-final-target53')
files=['tools/cloud-connections-test']+['projects/ROCKNIX/packages/network/rclone/sources/'+n for n in ('cloud_connections.py','cloud_remote','cloud_oauth')]
with tarfile.open('/tmp/pix540-vm-transactions39/fixture.tar') as old,tarfile.open(O/'fixture.tar','w') as new:
 for m in old.getmembers():
  if m.name.startswith('dependencies/'):
   new.addfile(m,old.extractfile(m) if m.isfile() else None)
 for f in files:new.add(D/f,arcname=f)
v.scp(O/'fixture.tar','/storage/qa537/transaction53.tar')
v.remote('systemctl stop essway; mkdir -p /storage/qa537/transaction53; tar -xf /storage/qa537/transaction53.tar -C /storage/qa537/transaction53')
cmd='PYTHONPATH=/storage/qa537/transaction53/dependencies python3 /storage/qa537/transaction53/tools/cloud-connections-test'
with (O/'transactions.log').open('w') as log:r=subprocess.run(['ssh',*v.opts,'-p',str(v.G['ssh_port']),'root@127.0.0.1',cmd],stdout=log,stderr=subprocess.STDOUT)
r.check_returncode();print('PASS 26 actual-guest connection transactions',flush=True)
v.scp(O/'guest.py','/storage/qa537/selection-refusal53.py')
out=v.remote('python3 /storage/qa537/selection-refusal53.py');result=json.loads(out);assert result['result']=='PASS' and result['restored'];(O/'refusals.json').write_text(out)
(O/'result.json').write_text(json.dumps({'result':'PASS','transactions':26,'refusal_controls':len(result['controls']),'inputs':[{'path':f,'sha256':hashlib.sha256((D/f).read_bytes()).hexdigest()} for f in files]},indent=2)+'\n')
print('PASS 15 actual script refusal controls and state restoration',flush=True)
