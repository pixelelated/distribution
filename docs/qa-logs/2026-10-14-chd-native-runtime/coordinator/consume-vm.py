from pathlib import Path
import json,hashlib,subprocess,shutil,os,datetime,argparse
p=argparse.ArgumentParser();p.add_argument('--owner',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--expected',type=int,choices=[0,1],required=True);a=p.parse_args();repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');packet=a.packet.resolve()
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert os.readlink('/proc/self/ns/pid')=='pid:[4026531836]';v=json.loads((packet/'host-exits.json').read_text());assert all(not Path('/proc',str(pid)).exists() for pid in v['pids_absent'])
evidence=['export-result.json','host-exits.json','guest-manifest.json','original-records.json','analysis.json']
dump(packet/'acceptance.json',{'run':str(a.run),'expected_rc':a.expected,'disposition':'qualified' if a.expected==0 else 'failed-investigated','outputs':json.loads((a.owner/'admission.json').read_text())['state']['outputs'],'evidence':[{'path':str(packet/n),'sha256':sha(packet/n)} for n in evidence]})
subprocess.run(['python3','-I',str(repo/'tools/host-maintenance/build-admission'),'consume','--run',str(a.run),'--evidence',str(packet/'acceptance.json')],check=True)
shutil.copy2(a.run/'admission-consumed.json',packet/'admission-consumed.json');v=a.owner/'vm';assert v.resolve()==v and not v.is_symlink();n=int(subprocess.check_output(['du','-s','-B1',str(v)]).split()[0]);shutil.rmtree(v);dump(packet/'retirement.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'path':str(v),'allocated_bytes_released':n,'exists_after':v.exists(),'original_exit':a.expected});print('retired',n)
