from pathlib import Path
import hashlib,json,subprocess,sys
owner=Path(sys.argv[1]);name=sys.argv[2];expected=int(sys.argv[3])
repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup')
assert Path('/proc/self/ns/pid').stat().st_ino==4026531836
stage=owner/'stages'/name
console=(stage/'submit/console.log').read_text()
run=Path(console.split('watch-build: recording in ',1)[1].splitlines()[0])
result=json.loads((stage/'result.json').read_text())
assert (run/'build.rc').read_text().strip()==str(expected)
assert json.loads((stage/'submit/launcher-result.json').read_text())['runner_returncode']==expected
assert result['cleanup']['status']=='PASS' and result['watchdog_original_exit']==0
assert result['status']==('PASS' if expected==0 else 'FAIL')
assert not result['cleanup']['forced_stop'] and result['cleanup']['exact_id_absent']
assert not result['cleanup']['survivors'] and not result['cleanup']['remaining_cgroup_pids']
assert result['original_attach_exit']==result['original_container_exit']==expected
ids=[int((run/n).read_text()) for n in ['build.pid','command.pid','watcher.pid']]
for n in ['submit/launcher-start.json','watchdog-client.json','docker-client.json']:
 ids.append(json.loads((stage/n).read_text())['pid'])
assert all(not Path('/proc',str(pid)).exists() for pid in ids),ids
def write(p,data):
 with p.open('x') as f:json.dump(data,f,indent=2);f.write('\n')
write(stage/'host-completion.json',{'status':'PASS','actual_host_pids_absent':ids,'pid_namespace':Path('/proc/self/ns/pid').stat().st_ino,'original_expected_exit':expected,'run':str(run)})
admission=json.loads((run/'admission.json').read_text())
files=['result.json','container-result.json','host-completion.json','watchdog-result.json','submit/launcher-result.json']
accept={'run':str(run),'expected_rc':expected,'disposition':'qualified' if expected==0 else 'failed-investigated','outputs':admission['outputs'],'evidence':[{'path':str(stage/n),'sha256':hashlib.sha256((stage/n).read_bytes()).hexdigest()} for n in files]}
write(stage/'acceptance.json',accept)
subprocess.run(['python3','-I',str(repo/'tools/host-maintenance/build-admission'),'consume','--run',str(run),'--evidence',str(stage/'acceptance.json')],check=True)
print(json.dumps({'stage':name,'status':result['status'],'original_rc':expected,'run':str(run),'host_pids_absent':ids}))
