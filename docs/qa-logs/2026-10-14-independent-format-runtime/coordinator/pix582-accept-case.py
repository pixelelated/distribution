from pathlib import Path
import argparse,datetime,hashlib,json,shutil,subprocess,tarfile
p=argparse.ArgumentParser()
p.add_argument('--owner',type=Path,required=True)
p.add_argument('--run',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
p.add_argument('--case',required=True)
p.add_argument('--expected-caller',required=True)
a=p.parse_args();repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup')
owner=a.owner;run=a.run;out=a.packet
r=json.loads((out/'result.json').read_text())
assert r['status']=='PASS' and r['case']==a.case
assert r['supervision']['quiescent'] and not r['supervision']['intervention'] and not r['remaining_descendants']
assert r['caller']['original_installer_exits']==[int(x) for x in a.expected_caller.split(',')]
assert r['caller']['protected'] and all(r['caller']['protected'].values())
refused=a.case in ('proc-census-error','transport-timeout')
assert r['caller']['complete_caller']==(not refused)
assert r['caller']['native_client_execution']==('NOT_REACHED' if refused else 'DENIED; not qualification')
for c in r['supervision_controls']:assert c['status']=='PASS' and not c['remaining_descendants']
ids=json.loads((out/'host-exits.json').read_text())['pids_absent']
assert Path('/proc/self/ns/pid').stat().st_ino==4026531836 and all(not Path('/proc',str(x)).exists() for x in ids)
assert json.loads((out/'export-result.json').read_text())['original_exit']==0
adm=json.loads((run/'admission.json').read_text())
names=['result.json','namespace-result.json','host-exits.json','vm-result.json','guest-manifest.json','original-records.json','unmount-640x480.txt']
acceptance={'run':str(run),'expected_rc':0,'disposition':'qualified','outputs':adm['outputs'],'evidence':[{'path':str(out/n),'sha256':hashlib.sha256((out/n).read_bytes()).hexdigest()} for n in names]}
with (owner/'acceptance.json').open('x') as f:json.dump(acceptance,f,indent=2);f.write('\n')
subprocess.run(['python3','-I',str(repo/'tools/host-maintenance/build-admission'),'consume','--run',str(run),'--evidence',str(owner/'acceptance.json')],check=True)
shutil.copy2(owner/'acceptance.json',out/'acceptance.json');shutil.copy2(run/'admission-consumed.json',out/'admission-consumed.json')
size=int(subprocess.check_output(['du','-s','-B1',str(owner/'vm')],text=True).split()[0])
assert not (owner/'vm/vm.pid').exists();shutil.rmtree(owner/'vm')
(out/'retirement.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'path':str(owner/'vm'),'allocated_bytes_released':size,'exists_after':False,'original_exit':0},indent=2)+'\n')
print(json.dumps({'case':a.case,'status':'PASS','caller_exits':r['caller']['original_installer_exits'],'retired_bytes':size,'consumed':True}))
