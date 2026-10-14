from pathlib import Path
import json,hashlib,re,subprocess,datetime,shutil,stat,os
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup')
assert json.loads((r/'vm-result.json').read_text())['rc']==0
expected_failures={'capability-probe-owner':1,'capability-small02-owner':1,'capability-system-finish-owner':1,'rvz-owner':2,'setup-owner':2,'steam-owner':1,'steam-installed-owner':1,'steam-applets-owner':1,'dolphin-v2-gc-state-fr1280-owner':1,'dolphin-v3-gc-state-fr1280-owner':1}
rows=[]
for owner in sorted(r.iterdir()):
 if not owner.is_dir() or not (owner/'launcher-submission.json').exists():continue
 launcher=json.loads((owner/'launcher-result.json').read_text());rc=expected_failures.get(owner.name,0)
 assert launcher['runner_returncode']==rc and int((owner/'tool-wrapper.rc').read_text())==rc,(owner,launcher,rc)
 m=re.search(r'watch-build: recording in (\S+)',(owner/'console.log').read_text());pids=[launcher['pid']];row={'owner':owner.name,'original_rc':rc,'launcher':launcher}
 if m:
  run=Path(m.group(1));rr=json.loads((run/'runner-result.json').read_text());assert rr['command_rc']==rr['runner_rc']==rc and rr['monitor_rc']==0,(owner,rr)
  row.update(run=str(run),runner=rr)
  pids += [int((run/n).read_text()) for n in ['build.pid','command.pid','watcher.pid','build.status.pid'] if (run/n).exists()]
 else:assert rc==2,('Missing watched run',owner)
 states=[]
 for pid in sorted(set(pids)):
  p=Path('/proc')/str(pid);absent=not p.exists();cmd=(p/'cmdline').read_bytes() if not absent else b''
  assert absent or not cmd,('Still alive',owner,pid)
  states.append({'pid':pid,'absent':absent,'exited_zombie':not absent and not cmd})
 row['actual_host_processes']=states;rows.append(row)
boots=json.loads((r/'vm-result.json').read_text())['boots']
for boot in boots:
 p=Path('/proc')/str(boot['pid'])/'cmdline';assert not p.exists() or not p.read_bytes()
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owners':rows,'vm_pids_exited':[b['pid'] for b in boots],'scope':'Lifecycle complete; component and UI partial qualification only. Original failed fixtures remain failures. No native engine, full image, or RC acceptance.'}
(r/'consumption.json').write_text(json.dumps(receipt,indent=2)+'\n')
main=next(x for x in rows if x['owner']=='vm-owner');evidence=['vm-result.json','consumption.json','steam-applets-results/result.json','capability-system-fr1280/readback-result.json']
assert all((r/n).is_file() for n in evidence)
a={'run':main['run'],'expected_rc':0,'disposition':'qualified','outputs':json.loads((r/'admission.json').read_text())['state']['outputs'],'evidence':[{'path':str(r/n),'sha256':hashlib.sha256((r/n).read_bytes()).hexdigest()} for n in evidence]}
(r/'acceptance.json').write_text(json.dumps(a,indent=2)+'\n');p=subprocess.run([str(repo/'tools/host-maintenance/build-admission'),'consume','--run',a['run'],'--evidence',str(r/'acceptance.json')],capture_output=True,text=True);(r/'admission-consumed.txt').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr
v=r/'vm';ret=[]
for p in sorted(v.iterdir()):
 s=p.lstat()
 if stat.S_ISREG(s.st_mode):
  assert p.name in ['disk.qcow2','OVMF.fd','qa-key','qa-key.pub','known_hosts'],p
  ident=(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns);q=p.lstat();assert ident==(q.st_dev,q.st_ino,q.st_size,q.st_mtime_ns)
  p.unlink();ret.append({'path':str(p),'allocated_bytes':s.st_blocks*512,'absent':not p.exists()})
 else:assert stat.S_ISSOCK(s.st_mode),p
(r/'retirement.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'retired':ret,'released_allocated_bytes':sum(x['allocated_bytes'] for x in ret),'automatic_cleanup':False,'immediate_test_disk_retired':True},indent=2)+'\n')
print('Original owners consumed; lifecycle admission released; disk and temporary keys retired')
