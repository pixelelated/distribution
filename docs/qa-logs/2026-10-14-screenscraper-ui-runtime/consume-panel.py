from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess
p=argparse.ArgumentParser();p.add_argument('--owner',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);a=p.parse_args()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
assert os.readlink('/proc/self/ns/pid')=='pid:[4026531836]'
assert a.owner.parent==Path('/workspace/tmp') and a.owner.name.startswith('pix566-ui')
runtime=json.loads((a.owner/'records/runtime.json').read_text());tree=Path(runtime['checkout'])
assert a.run.parent==tree/'.build-runs'
assert json.loads((a.packet/'analysis.json').read_text())['status']=='PASS'
assert json.loads((a.packet/'export-result.json').read_text())['original_exit']==0
for pid in json.loads((a.packet/'host-exits.json').read_text())['pids_absent']:assert not Path('/proc',str(pid)).exists()
runner=json.loads((a.run/'runner-result.json').read_text())
assert runner['runner_rc']==runner['command_rc']==runner['monitor_rc']==0
assert json.loads((a.owner/'vm-result.json').read_text())['rc']==0
assert json.loads((a.owner/'lifecycle-owner/launcher-result.json').read_text())['runner_returncode']==0
assert (a.owner/'lifecycle-owner/tool-wrapper.rc').read_text().strip()=='0'
evidence=['export-result.json','host-exits.json','guest-export-manifest.json','original-records.json','analysis.json']
save(a.packet/'acceptance.json',{'run':str(a.run),'expected_rc':0,'disposition':'qualified','outputs':json.loads((a.owner/'admission.json').read_text())['state']['outputs'],'evidence':[{'path':str(a.packet/n),'sha256':sha(a.packet/n)} for n in evidence]})
subprocess.run(['python3','-I',str(tree/'tools/host-maintenance/build-admission'),'consume','--run',str(a.run),'--evidence',str(a.packet/'acceptance.json')],check=True)
shutil.copy2(a.run/'admission-consumed.json',a.packet/'admission-consumed.json')
vm=a.owner/'vm';assert vm.resolve()==vm and not vm.is_symlink()
allocated=int(subprocess.check_output(['du','-s','-B1',str(vm)]).split()[0]);shutil.rmtree(vm)
save(a.packet/'retirement.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'removed':str(vm),'allocated_bytes_released':allocated,'exists_after':vm.exists(),'original_exit':0})
print(json.dumps({'consumed':str(a.run),'retired_bytes':allocated}))
