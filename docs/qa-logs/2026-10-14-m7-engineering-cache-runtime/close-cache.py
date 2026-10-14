from pathlib import Path
import datetime,gzip,hashlib,json,os,shutil,subprocess
owner=Path('/workspace/tmp/pix-m7-engineering-cache-20261014-01')
tree=Path('/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01')
repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup')
packet=repo/'docs/qa-logs/2026-10-14-m7-engineering-cache-runtime'
run=Path((owner/'run.path').read_text().strip())
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def write(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
assert Path('/proc/self/ns/pid').stat().st_ino==4026531836
assert int((owner/'inner.rc').read_text())==0
assert int((owner/'tool-wrapper.rc').read_text())==0
runner=json.loads((run/'runner-result.json').read_text())
assert runner['runner_rc']==runner['command_rc']==runner['monitor_rc']==0
assert int((run/'build.rc').read_text())==0
assert (run/'build.status').read_text().startswith('state:       finished\n')
assert (owner/'cache-compare.txt').read_bytes()==b''
ready=json.loads((owner/'cache-ready.json').read_text())
assert ready['checksum_equal'] and ready['independent_regular_files']>2000000
assert ready['new']==str(tree/'build.pixelelated-GENERIC_X64.x86_64')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=tree,text=True).strip()=='e483a7f0925e7ebb56335133a5de423269390945'
assert not subprocess.check_output(['git','status','--porcelain'],cwd=tree)
pids={int((run/n).read_text()) for n in ['build.pid','command.pid','watcher.pid'] if (run/n).exists()}
pids.add(json.loads((owner/'launcher-start.json').read_text())['pid'])
assert all(not Path('/proc',str(pid)).exists() for pid in pids),pids
packet.mkdir()
records=[]
for prefix,root,names in [('owner',owner,['admission-plan.json','admission.json','planning-inputs.json','retention-plan.json','retention-report.json','cache-ready.json','cache-compare.txt','inner.rc','tool-wrapper.rc','launcher-submission.json','launcher-start.json','launcher-result.json','console.log']),('run',run,['admission.json','admission-plan.json','runner-result.json','build.rc','build.status','build.pid','command.pid','watcher.pid','build.log'])]:
 (packet/prefix).mkdir()
 for name in names:
  p=root/name
  if not p.exists():continue
  dst=packet/prefix/(name+'.gz' if name.endswith('.log') else name)
  if name.endswith('.log'):
   with p.open('rb') as src,dst.open('xb') as target,gzip.GzipFile(filename='',fileobj=target,mode='wb',mtime=0) as zipped:shutil.copyfileobj(src,zipped,1024*1024)
  else:shutil.copy2(p,dst)
  records.append({'source':str(p),'original_bytes':p.stat().st_size,'original_sha256':sha(p),'stored':str(dst.relative_to(packet)),'stored_sha256':sha(dst)})
write(packet/'original-records.json',records)
write(packet/'host-exits.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid_namespace':4026531836,'pids_absent':sorted(pids),'run':str(run)})
write(packet/'analysis.json',{'status':'PASS','source_commit':'e483a7f0925e7ebb56335133a5de423269390945','cache':ready,'original_command_exit':0,'original_runner_exit':0,'original_monitor_exit':0,'original_launcher_exit':0,'scope':'Independent accepted-parent cache copy only; no new package/image acceptance. Final published source can advance only after owner closure.','cache_retained_for':'Immediately queued final frontend proof and assembled engineering image.'})
write(packet/'acceptance.json',{'run':str(run),'expected_rc':0,'disposition':'qualified','outputs':json.loads((run/'admission.json').read_text())['outputs'],'evidence':[{'path':str(packet/n),'sha256':sha(packet/n)} for n in ['analysis.json','host-exits.json','original-records.json','owner/cache-ready.json','owner/cache-compare.txt']]})
subprocess.run(['python3','-I',str(tree/'tools/host-maintenance/build-admission'),'consume','--run',str(run),'--evidence',str(packet/'acceptance.json')],check=True)
shutil.copy2(run/'admission-consumed.json',packet/'admission-consumed.json')
shutil.copy2(Path(__file__),packet/'close-cache.py')
(packet/'README.md').write_text('Independent engineering-cache copy completed with full checksum equality and '+str(ready['independent_regular_files'])+' independent regular files. Original command, runner, watcher and launcher exits are0; actual host owners exited and admission is consumed. Source was frozen at e483a7f0925e7ebb56335133a5de423269390945. Accepted predecessor remained unchanged. This is cache-copy evidence, not new firmware acceptance. Original progress logs are compressed byte-preserving with original and stored identities in original-records.json. The cache remains held for the immediate new engineering image.\n')
files=sorted(p for p in packet.rglob('*') if p.is_file())
(packet/'SHA256SUMS').write_text(''.join(sha(p)+'  '+str(p.relative_to(packet))+'\n' for p in files))
print(json.dumps({'status':'PASS','files':ready['independent_regular_files'],'packet':str(packet),'run':str(run)}))
