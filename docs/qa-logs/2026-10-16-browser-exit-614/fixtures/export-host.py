#!/usr/bin/env python3
"""After the original owner exits, export compact originals. Never consume or delete."""
import argparse,hashlib,json,shutil,tarfile
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
for n in ['owner','run','output']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();owner=a.owner.resolve(strict=True);run=a.run.resolve(strict=True);out=a.output.absolute();cfg=json.loads((owner/'config.json').read_text())
assert not out.exists() and out.parent==Path('/workspace/tmp')
assert Path('/proc/self/ns/pid').stat().st_ino==cfg['host_pid_namespace']
assert run.parent==Path(cfg['checkout'])/'.build-runs'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,obj):
    with p.open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
def gone(pid,start=None):
    try:
        f=Path('/proc',str(pid),'stat').read_text().rsplit(')',1)[1].split()
        return f[0]=='Z' or start is not None and int(f[19])!=int(start)
    except FileNotFoundError:return True
launch=json.loads((owner/'lifecycle-owner/launcher-result.json').read_text());rr=json.loads((run/'runner-result.json').read_text());vm=json.loads((owner/'vm-result.json').read_text());rc=rr['runner_rc']
channels={'launcher':launch['runner_returncode'],'tool_wrapper':int((owner/'lifecycle-owner/tool-wrapper.rc').read_text()),'build':int((run/'build.rc').read_text()),'command':rr['command_rc'],'monitor':rr['monitor_rc'],'runner':rc,'vm':vm['rc']}
coherent=channels['launcher']==channels['tool_wrapper']==rc and channels['build']==channels['command']==channels['vm']
pids=[launch['pid']]+[int((run/n).read_text()) for n in ['build.pid','command.pid','watcher.pid','build.status.pid'] if (run/n).exists()]
assert all(gone(pid) for pid in pids)
assert all(gone(row['pid'],row['start_ticks']) for row in vm['boots'])
identities=json.loads((owner/'records/host-process-identities.json').read_text())
assert all(gone(row['pid'],row['start_ticks']) for row in identities)
assert not vm['surviving_host_processes'] and not vm['qemu_still_live']
qualified=rc==0 and coherent and all(v==0 for v in channels.values())
if qualified:
    assert len(vm['boots'])==1 and not vm['cleanup_errors'] and not vm['forced_host_cleanup']
    clean=json.loads((owner/'clean/report.json').read_text());assert clean['status']=='pass' and clean['blocked_count']==clean['error_count']==0
    repeat=json.loads((owner/'extra/repeat-result.json').read_text());assert repeat['status']=='PASS' and len(repeat['cases'])==4
    cleanup=json.loads((owner/'extra/guest-evidence/qa614/cleanup-result.json').read_text());assert cleanup['rc']==0 and cleanup['observer']['rc']==0 and not cleanup['observer']['guards'] and cleanup['observer']['stopped']
    assert vm['qualification']['status']=='PASS'
out.mkdir(mode=0o700);rows=[];sources=[];private_rows=[]
for base,label in [(owner,'owner'),(run,'run')]:
    for f in sorted(base.rglob('*')):
        if f.is_symlink() or not f.is_file():continue
        if base==owner and any(f.is_relative_to(owner/n) for n in ['vm','host-tmp']):continue
        if base==owner and (f.is_relative_to(owner/'private') or f.parent==owner/'records' and '-zerotier-' in f.name and f.suffix in ['.stdout','.stderr']):
            private_rows.append({'path':str(f),'bytes':f.stat().st_size,'sha256':sha(f)});continue
        assert f.stat().st_size<=16*1024**2
        name=label+'/'+str(f.relative_to(base));row={'path':name,'bytes':f.stat().st_size,'sha256':sha(f)};rows.append(row);sources.append((f,name))
assert len(rows)<=4096 and sum(r['bytes'] for r in rows)<=256*1024**2
with tarfile.open(out/'original-records.tar.gz','x:gz') as t:
    for f,name in sources:t.add(f,arcname=name,recursive=False)
with tarfile.open(out/'original-records.tar.gz','r:gz') as t:
    assert {m.name for m in t.getmembers()}=={r['path'] for r in rows}
    for row in rows:
        data=t.extractfile(row['path']).read();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
write(out/'original-records.json',rows)
write(out/'private-originals-held.json',{'files':private_rows,'policy':'Raw local CLI/serial outputs remain private owner-held; identity/token/configuration bytes never leave guest.'})
for name in ['vm-result.json','config.json']:shutil.copyfile(owner/name,out/name)
write(out/'host-exits.json',{'status':'OWNERS_GONE','original_rc':rc,'original_channels':channels,'channels_coherent':coherent,'pids_exited':pids,'qemu_identities':vm['boots'],'command_identities':identities,'host_pid_namespace':cfg['host_pid_namespace']})
write(out/'export-result.json',{'status':'EXPORTED','original_rc':rc,'original_channels':channels,'files':len(rows),'bytes':sum(r['bytes'] for r in rows),'lossless_exported_originals_verified':True,'private_originals_held':len(private_rows),'private_settings_or_account_values_exported':False,'acceptance_claimed':False})
evidence=[{'path':str(f),'sha256':sha(f)} for f in sorted(out.iterdir()) if f.is_file()]
# This is a concrete draft. Root reviews originals before invoking the existing consume tool.
write(out/'consumption-draft.json',{'run':str(run),'expected_rc':rc,'disposition':'qualified' if qualified else 'failed-investigated','outputs':json.loads((run/'admission.json').read_text())['outputs'],'evidence':evidence,'requires_coordinator_review':True,'channels_coherent':coherent,'monitor_succeeded':rr['monitor_rc']==0})
print(json.dumps({'status':'EXPORTED_NOT_CONSUMED','output':str(out),'original_rc':rc,'retirement':'After coordinator review and consume, retire only this owner disk/OVMF/TMPDIR through existing guarded tooling.'}))
