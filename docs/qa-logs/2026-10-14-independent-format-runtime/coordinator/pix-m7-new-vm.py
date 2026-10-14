from pathlib import Path
import argparse, ast, hashlib, json, subprocess

p=argparse.ArgumentParser()
p.add_argument('--owner',type=Path,required=True)
p.add_argument('--inputs',type=Path,required=True)
p.add_argument('--guest-script',type=Path,required=True)
p.add_argument('--issue',type=int,required=True)
p.add_argument('--stage',required=True)
p.add_argument('--guest-seconds',type=int,required=True)
p.add_argument('--vnc',type=int,required=True)
a=p.parse_args()
assert 60 <= a.guest_seconds <= 700 and 100 <= a.vnc <= 199
repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup')
old=Path('/workspace/tmp/pix582-client-vm-20261014-03')
r=a.owner
assert r.parent == Path('/workspace/tmp') and r.name.startswith('pix')
r.mkdir()
for name in ('records','scan','vm','lifecycle-owner'):(r/name).mkdir()
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
facts=json.loads((old/'records/image-size.json').read_text())
write(r/'records/image-size.json',facts)
inputs=json.loads(a.inputs.read_text())
assert inputs['files'] and len({x['destination'] for x in inputs['files']})==len(inputs['files'])
for entry in inputs['files']:
    relative=Path(entry['destination'])
    assert not relative.is_absolute() and '..' not in relative.parts
    source=Path(entry['path'])
    assert source.is_file() and not source.is_symlink() and sha(source)==entry['sha256']
inputs['helper']=json.loads((old/'records/inputs.json').read_text())['helper']
write(r/'records/inputs.json',inputs)
guest=a.guest_script.read_text()
subprocess.run(['sh','-n',str(a.guest_script)],check=True)
(r/'run-guest.sh').write_text(guest)
source=(old/'vm-lifecycle.py').read_text()
source=source.replace('import subprocess,json,gzip,hashlib,time,datetime,socket,tarfile,shutil,shlex,os','import subprocess,json,gzip,hashlib,time,datetime,socket,tarfile,shutil,shlex,os,signal')
source=source.replace("try:\n with socket.socket() as s:s.bind(('127.0.0.1',5998))", "def expired(signum,frame):raise TimeoutError('VM lifecycle deadline or termination')\nsignal.signal(signal.SIGALRM,expired)\nsignal.signal(signal.SIGTERM,expired)\nsignal.alarm(900)\n\ntry:\n with socket.socket() as s:s.bind(('127.0.0.1',"+str(5900+a.vnc)+"))")
source=source.replace("'--vnc','98'", "'--vnc','"+str(a.vnc)+"'")
source=source.replace('PIX582_QA_RC','PIXM7_QA_RC').replace('seconds=180)', 'seconds='+str(a.guest_seconds)+')')
source=source.replace("finally:\n if (v/'vm.pid').exists():", "finally:\n signal.alarm(0)\n if (v/'vm.pid').exists():")
assert 'signal.alarm(900)' in source and '5998' not in source and 'PIX582_QA_RC' not in source
ast.parse(source);(r/'vm-lifecycle.py').write_text(source)
write(r/'records/lifecycle-basis.json',{'source':str(old/'vm-lifecycle.py'),'sha256':sha(old/'vm-lifecycle.py'),'changes':['fresh VNC endpoint','explicit 900-second alarm and SIGTERM finally','guest serial budget','stage-neutral result marker'],'guest_serial_seconds':a.guest_seconds,'vnc_display':a.vnc})
protected=[str(r/'records'),str(repo/'tools/host-maintenance'),facts['image']]
plan={'volume':'/workspace','scan_roots':[str(r/'scan')],'reference_stores':[],'protected':protected,'candidates':[],
 'builds':[{'name':a.stage,'terms_bytes':{'raw_image':facts['raw_bytes_from_backup_lba'],'guest_disk':16*1024**3,'media_records':512*1024**2},
 'basis':'Fresh accepted no-NIC VM20, 8GiB RAM and 4CPU. 16GiB virtual disk, prior equivalent physical allocation about2.3GB. 900s host work alarm plus bounded flush/stop. Exact public input hashes and unchanged image/helper checked before launch. Serialized guest cases bounded by source-owned timers and serial budget. Export compact original records then retire disk/media/UEFI; no owner data/provider.',
 'evidence':[{'path':str(r/name),'sha256':sha(r/name)} for name in ['records/image-size.json','records/inputs.json','records/lifecycle-basis.json','vm-lifecycle.py','run-guest.sh']]}]}
write(r/'retention-plan.json',plan)
write(r/'admission-plan.json',{'checkout':str(repo),'retention_plan':str(r/'retention-plan.json'),'retention_report':str(r/'retention-report.json'),'stage':a.stage,
 'profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],
 'outputs':[{'path':str(r/'vm'),'issue':a.issue,'kind':'qa-scratch','release_when':'Original guest/guard/lifecycle receipts exported and verified; actual owners exited; consume admission then remove disk/media/UEFI. Preserve only immediate-next-test synthetic inputs.'}]})
print(str(r))
