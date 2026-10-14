#!/usr/bin/env python3
"""Export the original watched standard/cloud results after actual owners exit; never consume."""
import argparse,hashlib,json,shutil,tarfile
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
for n in ['owner','run','output']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();owner=a.owner.resolve(strict=True);run=a.run.resolve(strict=True);out=a.output.absolute();cfg=json.loads((owner/'config.json').read_text())
assert not out.exists() and out.parent==Path('/workspace/tmp') and run.parent==Path(cfg['checkout'])/'.build-runs'
assert Path('/proc/self/ns/pid').stat().st_ino==cfg['host_pid_namespace']
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
def gone(pid,start=None):
 try:
  f=Path('/proc',str(pid),'stat').read_bytes().rpartition(b')')[2].split()
  return f[0]==b'Z' or start is not None and int(f[19])!=int(start)
 except FileNotFoundError:return True
launch=json.loads((owner/'lifecycle-owner/launcher-result.json').read_text());rr=json.loads((run/'runner-result.json').read_text());original=json.loads((owner/'result.json').read_text());rc=rr['runner_rc']
channels={'launcher':launch['runner_returncode'],'tool_wrapper':int((owner/'lifecycle-owner/tool-wrapper.rc').read_text()),'build':int((run/'build.rc').read_text()),'command':rr['command_rc'],'monitor':rr['monitor_rc'],'runner':rc,'owner':original['rc']}
coherent=channels['launcher']==channels['tool_wrapper']==rc and channels['build']==channels['command']==channels['owner']
pids=[launch['pid']]+[int((run/n).read_text()) for n in ['build.pid','command.pid','watcher.pid','build.status.pid'] if (run/n).exists()]
assert all(gone(pid) for pid in pids)
identities=json.loads((owner/'records/process-identities.json').read_text());assert all(gone(r['pid'],r['start_ticks']) for r in identities+original['qemu'])
assert not original['surviving_owned_processes'] and not original['qemu_still_live'] and original.get('backend_name_absent'),'cleanup incomplete; keep owner private for investigation'
qualified=coherent and all(v==0 for v in channels.values())
if qualified:
 assert len(original['qemu'])==2 and not original['cleanup_errors'] and not original.get('forced_child_cleanup') and not original['remaining_children']
 assert [r['backend'] for r in original['reports']]==['webdav','sftp','s3']
 assert [len(r['rows']) for r in original['reports']]==[15,1,1]
 for r in original['reports']:assert sha(Path(r['path']))==r['sha256'] and all(x['result']=='PASS' for x in r['rows'])
out.mkdir(mode=0o700);rows=[];sources=[]
for base,label in [(owner,'owner'),(run,'run')]:
 for f in sorted(base.rglob('*')):
  if f.is_symlink() or not f.is_file():continue
  if base==owner and any(f.is_relative_to(owner/n) for n in ['pair','runtime','tmp','cloud','scan']):continue
  assert f.stat().st_size<=32*1024**2
  name=label+'/'+str(f.relative_to(base));rows.append({'path':name,'bytes':f.stat().st_size,'sha256':sha(f)});sources.append((f,name))
assert len(rows)<=4096 and sum(r['bytes'] for r in rows)<=cfg['record_limit_bytes']
with tarfile.open(out/'original-records.tar.gz','x:gz') as t:
 for f,name in sources:t.add(f,arcname=name,recursive=False)
with tarfile.open(out/'original-records.tar.gz','r:gz') as t:
 assert {m.name for m in t.getmembers()}=={r['path'] for r in rows}
 for r in rows:
  data=t.extractfile(r['path']).read();assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
write(out/'original-records.json',rows)
for n in ['result.json','config.json']:shutil.copyfile(owner/n,out/n)
write(out/'host-exits.json',{'status':'OWNERS_GONE','original_rc':rc,'original_channels':channels,'channels_coherent':coherent,'pids_exited':pids,'qemu_identities':original['qemu'],'command_identities':identities,'backend_owners':original['backend_owners'],'host_pid_namespace':cfg['host_pid_namespace']})
write(out/'export-result.json',{'status':'EXPORTED','original_rc':rc,'original_channels':channels,'files':len(rows),'bytes':sum(r['bytes'] for r in rows),'lossless_originals_verified':True,'private_keys_backend_state_and_guest_disks_exported':False,'acceptance_claimed':False})
evidence=[{'path':str(f),'sha256':sha(f)} for f in sorted(out.iterdir()) if f.is_file()]
write(out/'consumption-draft.json',{'run':str(run),'expected_rc':rc,'disposition':'qualified' if qualified else 'failed-investigated','outputs':json.loads((run/'admission.json').read_text())['outputs'],'evidence':evidence,'requires_coordinator_review':True,'channels_coherent':coherent,'monitor_succeeded':rr['monitor_rc']==0})
print(json.dumps({'status':'EXPORTED_NOT_CONSUMED','output':str(out),'original_rc':rc}))
