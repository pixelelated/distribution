from pathlib import Path
import json,hashlib,re,subprocess,shutil,datetime
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');rows=[]
for o in ['report-owner','compile-owner']:
 owner=r/o;l=json.loads((owner/'launcher-result.json').read_text());assert l['runner_returncode']==0 and int((owner/'tool-wrapper.rc').read_text())==0
 run=Path(re.search(r'watch-build: recording in (\S+)',(owner/'console.log').read_text()).group(1));rr=json.loads((run/'runner-result.json').read_text());assert all(rr[k]==0 for k in ['command_rc','monitor_rc','runner_rc']);pids=[l['pid']]+[int((run/n).read_text()) for n in ['build.pid','command.pid','watcher.pid']]
 assert all(not Path(f'/proc/{p}').exists() for p in pids)
 rows.append({'owner':o,'run':str(run),'pids_exited':pids,'original_rc':0,'runner':rr})
assert json.loads((r/'result.json').read_text())['rc']==0
assert json.loads((r/'compile-result.json').read_text())['rc']==0
assert 'PASS 64/64' in (r/'capability/run/stdout').read_text()
assert not (r/'capability/run/stderr').read_text()
cid=(r/'container.cid').read_text().strip();p=subprocess.run(['docker','inspect',cid],capture_output=True);assert p.returncode!=0
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stages':rows,'container_removed':True,'container_id':cid,'qualification':'Compiled composition and64extracted host capability controls only. Target RVZ/runtime and new installed UI still due.'};(r/'consumption.json').write_text(json.dumps(receipt,indent=2)+'\n')
a={'run':rows[-1]['run'],'expected_rc':0,'disposition':'qualified','outputs':json.loads((r/'admission.json').read_text())['state']['outputs'],'evidence':[{'path':str(r/n),'sha256':hashlib.sha256((r/n).read_bytes()).hexdigest()} for n in ['result.json','compile-result.json','capability/run/result.json','consumption.json']]};(r/'acceptance.json').write_text(json.dumps(a,indent=2)+'\n')
p=subprocess.run([str(repo/'tools/host-maintenance/build-admission'),'consume','--run',a['run'],'--evidence',str(r/'acceptance.json')],capture_output=True,text=True);(r/'admission-consumed.txt').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr
# Keep target executables at original paths for the immediately queued guest.
ret=[]
for target in [r/'scratch/es',r/'tmp',r/'capability/run/capability']:
 files=[p for p in target.rglob('*') if p.is_file() and not p.is_symlink()] if target.is_dir() else [target]
 ret.append({'path':str(target),'allocated_file_bytes':sum(p.stat().st_blocks*512 for p in files)})
 if target.is_dir():shutil.rmtree(target)
 else:target.unlink()
for directory,name in [(r/'controls/candidate','pix574-hash-control'),(r/'controls/baseline','pix574-hash-control'),(r/'controls/retry','pix574-retry-control')]:
 for target in directory.iterdir():
  if target.name==name:continue
  files=[p for p in target.rglob('*') if p.is_file() and not p.is_symlink()] if target.is_dir() else [target]
  ret.append({'path':str(target),'allocated_file_bytes':sum(p.stat().st_blocks*512 for p in files if not p.is_symlink())})
  if target.is_dir():shutil.rmtree(target)
  else:target.unlink()
(r/'retirement.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'retired':ret,'retired_allocated_file_bytes':sum(x['allocated_file_bytes'] for x in ret),'retained':['scratch/emulationstation','scratch/fr.mo','scratch/en_GB.mo','controls/candidate/pix574-hash-control','controls/baseline/pix574-hash-control','controls/retry/pix574-retry-control'],'hold':'Immediately queued synthetic target/runtime and installed VM qualification','automatic_cleanup':False},indent=2)+'\n')
print('Compile channels consumed; cache/objects retired; target executables held for next guest')
