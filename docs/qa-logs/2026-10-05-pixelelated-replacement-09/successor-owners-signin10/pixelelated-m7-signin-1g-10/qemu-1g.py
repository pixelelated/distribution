from pathlib import Path
import argparse,hashlib,importlib.machinery,json,os
p=Path('projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm')
m=importlib.machinery.SourceFileLoader('qa_canonical_vm',str(p)).load_module()
a=argparse.ArgumentParser();m.add_qemu_options(a);args=a.parse_args()
profile=m.load_profile();before=profile['memory_mib'];assert before==8192;profile['memory_mib']=1024
command=m.qemu_command(profile,args)
assert command[command.index('-m')+1]=='1024'
owner=Path(__file__).parent
(owner/'artifacts/qemu-1g.json').write_text(json.dumps({'canonical_helper_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'canonical_memory_mib':before,'test_memory_mib':1024,'command':command},indent=2)+'\n')
m.prepare_run(profile,args);os.execv(command[0],command)
