from pathlib import Path
import hashlib,json,os,shutil,subprocess,tarfile,datetime
owner=Path('/workspace/tmp/pix566-es-component-20261014-01');stage=owner/'stages/es-component';tree=Path('/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01');repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup')
packet=repo/'docs/qa-logs/2026-10-14-screenscraper-rejection-runtime/attempt01';packet.mkdir(parents=True,exist_ok=True)
run=Path((stage/'submit/console.log').read_text().split('watch-build: recording in ',1)[1].splitlines()[0])
def dump(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert Path('/proc/self/ns/pid').stat().st_ino==4026531836
cid=(stage/'container.cid').read_text().strip();m=json.loads((stage/'container-owner.json').read_text());v=json.loads((stage/'coordinator-container-readback.json').read_text())
assert v['id']==cid and v['name']=='/'+m['name'] and v['labels']['pix574.owner']==m['nonce']
assert v['state']['Status']=='exited' and not v['state']['Running'] and v['state']['Pid']==0 and v['state']['ExitCode']==1
assert v['memory']==8*1024**3
r=subprocess.run(['docker','inspect',cid],capture_output=True,text=True,timeout=20)
assert r.returncode==1 and r.stdout=='[]\n' and r.stderr.lower()=='error: no such object: '+cid+'\n'
shutil.copy2('/tmp/pix566-close-failed-component-original.py',packet/'initial-closeout.py')
dump(packet/'initial-closeout-failure.json',{'exit':1,'cause':'Exact stopped container rm passed its zero/CID assertions; follow-up absence assertion incorrectly required capitalized No. Actual Docker prints lowercase error: no such object and [] stdout. No compiler/product run was replayed; current exact absent readback is verified.'})
pids={int((run/n).read_text()) for n in ['build.pid','command.pid','watcher.pid'] if (run/n).exists()}
for f in ['submit/launcher-start.json','watchdog-client.json','docker-client.json']:
 pids.add(json.loads((stage/f).read_text())['pid'])
assert all(not Path('/proc',str(pid)).exists() for pid in pids),pids
assert int((run/'build.rc').read_text())==1 and int((stage/'submit/tool-wrapper.rc').read_text())==1
assert json.loads((run/'runner-result.json').read_text())==dict(command_rc=1,monitor_rc=0,runner_rc=1,utc=json.loads((run/'runner-result.json').read_text())['utc'])
assert json.loads((stage/'container-result.json').read_text())['children']==[]
dump(stage/'coordinator-cleanup.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_id':cid,'original_container_exit':1,'already_stopped':True,'removal':'Original rm passed zero/CID assertions before initial absence-case assertion failed; current absence reverified','exact_id_absent':True,'host_pids_absent':sorted(pids),'pid_namespace':4026531836,'original_failure_preserved':True})
records=[]
with tarfile.open(packet/'original-records.tar.gz','w:gz') as archive:
 for prefix,root in [('owner',owner),('run',run)]:
  for p in sorted(root.rglob('*')):
   if not p.is_file():continue
   name=prefix+'/'+str(p.relative_to(root));archive.add(p,arcname=name,recursive=False);records.append({'path':name,'sha256':sha(p),'bytes':p.stat().st_size})
dump(packet/'original-records.json',{'archive_sha256':sha(packet/'original-records.tar.gz'),'files':records})
for n in ['result.json','container-result.json','watchdog-result.json','coordinator-cleanup.json','coordinator-container-readback.json']:shutil.copy2(stage/n,packet/n)
dump(packet/'analysis.json',{'status':'FAIL','original_runner_exit':1,'original_container_exit':1,'original_attach_exit':0,'original_watchdog_exit':1,'no_compiler_or_product_test_executed':True,'cause':'Reused DockerOwner expected4GiB while declared creator/inner bounds8GiB. Both initial observer and generic cleanup refused; stopping attach client forwarded termination to container. Coordinator subsequently verified exact nonce/CID, original exited1 and removed only that stopped container.','next':'Fresh owner with consistently bound8GiB checker; original result remains1.'})
dump(packet/'acceptance.json',{'run':str(run),'expected_rc':1,'disposition':'failed-investigated','outputs':json.loads((run/'admission.json').read_text())['outputs'],'evidence':[{'path':str(packet/n),'sha256':sha(packet/n)} for n in ['original-records.json','analysis.json','coordinator-cleanup.json','coordinator-container-readback.json']]})
subprocess.run(['python3','-I',str(tree/'tools/host-maintenance/build-admission'),'consume','--run',str(run),'--evidence',str(packet/'acceptance.json')],check=True)
shutil.copy2(run/'admission-consumed.json',packet/'admission-consumed.json');shutil.copy2(Path(__file__),packet/'close-failed-component.py')
print('Failure1 preserved; exact stopped container removed; original owners absent and admission consumed. No product test or pass claimed.')
