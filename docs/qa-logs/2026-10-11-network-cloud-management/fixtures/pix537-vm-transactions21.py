import importlib.util, pathlib, subprocess,tarfile,json,hashlib
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
D=pathlib.Path('/workspace/repos/rocknix.worktrees/m7-cloud-connections');O=pathlib.Path('/tmp/pix537-vm-transactions21');O.mkdir(exist_ok=True)
files=['tools/cloud-connections-test']+['projects/ROCKNIX/packages/network/rclone/sources/'+x for x in ['cloud_connections.py','cloud_remote','cloud_oauth']]
import pexpect,ptyprocess
with tarfile.open(O/'fixture.tar','w') as tar:
 for f in files:tar.add(D/f,arcname=f)
 for module in (pexpect,ptyprocess):tar.add(pathlib.Path(module.__file__).parent,arcname='dependencies/'+module.__name__,filter=lambda x:None if '__pycache__' in x.name else x)
v.scp(O/'fixture.tar','/storage/qa537/transaction-fixture.tar')
v.remote('mkdir -p /storage/qa537/transaction21; tar -xf /storage/qa537/transaction-fixture.tar -C /storage/qa537/transaction21')
command='PYTHONPATH=/storage/qa537/transaction21/dependencies python3 /storage/qa537/transaction21/tools/cloud-connections-test'
p=subprocess.run(['ssh',*v.opts,'-p',str(v.G['ssh_port']),'root@127.0.0.1',command],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(O/'result.log').write_text(p.stdout)
(O/'receipt.json').write_text(json.dumps({'returncode':p.returncode,'command':command,'inputs':[{'path':f,'sha256':hashlib.sha256((D/f).read_bytes()).hexdigest()} for f in files]},indent=2)+'\n')
print(p.stdout);p.check_returncode()
