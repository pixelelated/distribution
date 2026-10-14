#!/usr/bin/env python3
"""UNRUN compact stopped-owner exporter; no admission consumption or media deletion."""
import argparse,hashlib,json,shutil,tarfile
from pathlib import Path
p=argparse.ArgumentParser()
for key in ['owner','run','packet']:p.add_argument('--'+key,type=Path,required=True)
a=p.parse_args();owner=a.owner.resolve(strict=True);run=a.run.resolve(strict=True);out=a.packet.absolute();config=json.loads((owner/'config.json').read_text());tree=Path(config['checkout'])
def sha(f):
    with f.open('rb') as s:return hashlib.file_digest(s,'sha256').hexdigest()
def write(p,obj):
    with p.open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
assert Path('/proc/self/ns/pid').stat().st_ino==4026531836
assert run.parent==tree/'.build-runs' and owner.parent==out.parent==Path('/workspace/tmp') and not out.exists()
launcher=json.loads((owner/'lifecycle-owner/launcher-result.json').read_text());rc=launcher['runner_returncode'];assert rc in (0,1)
assert (owner/'lifecycle-owner/tool-wrapper.rc').read_text().strip()==(run/'build.rc').read_text().strip()==str(rc)
runner=json.loads((run/'runner-result.json').read_text());assert runner['runner_rc']==runner['command_rc']==rc and runner['monitor_rc']==0
vm=json.loads((owner/'vm-result.json').read_text());assert vm['rc']==rc
pids=[launcher['pid']]+[int((run/name).read_text()) for name in ['build.pid','command.pid','watcher.pid']]
if (owner/'qemu.json').exists():
    pids.append(json.loads((owner/'qemu.json').read_text())['pid'])
    if rc==0:assert 'down: owned QEMU exited' in (owner/'vm-stop.log').read_text()
assert all(not Path('/proc',str(pid)).exists() for pid in pids)
assert not vm.get('remaining_host_children'), 'host descendants must be absent before export'
if rc==0:
    assert not vm['cleanup_errors'] and not vm.get('forced_host_child_cleanup')
    assert [row['phase'] for row in vm['phases']]==['seed','before','after','backup']
    for row in vm['phases']:assert sha(owner/'phases'/row['phase']/(row['phase']+'.result.json'))==row['result_sha256']
    assert len(vm['boots'])==2 and vm['boots'][0]['boot_id']!=vm['boots'][1]['boot_id']
    for name in ['seed','before','after','backup']:
        assert (owner/'phases'/name/(name+'.transport.rc')).read_text().strip()=='0'
        assert json.loads((owner/'phases'/name/(name+'.result.json')).read_text())['result']=='PASS'
    assert json.loads((owner/'guest/backup-child.json').read_text())=={'returncode':0,'timed_out':False}
    assert {p.name for p in (owner/'guest').iterdir()}=={name+'.json' for name in ['seed-started','seed','before','before-policy','after','after-policy','backup-child','backup']}
    for row in json.loads((owner/'guest-manifest.json').read_text()):assert sha(owner/'guest'/row['path'])==row['sha256']
out.mkdir(mode=0o700);write(out/'host-exits.json',{'original_exit':rc,'pids_absent':pids,'actual_host_namespace':4026531836})
sources=[]
for base,label in [(owner,'owner'),(run,'run')]:
    for f in sorted(base.rglob('*')):
        if f.is_symlink() or not f.is_file() or (base==owner and f.is_relative_to(owner/'vm')):continue
        assert f.stat().st_size<32*1024**2;sources.append((f,label+'/'+str(f.relative_to(base))))
with tarfile.open(out/'original-records.tar.gz','x:gz') as tar:
    for f,name in sources:tar.add(f,arcname=name,recursive=False)
rows=[{'path':name,'bytes':f.stat().st_size,'sha256':sha(f)} for f,name in sources];write(out/'original-records.json',rows)
with tarfile.open(out/'original-records.tar.gz') as tar:
    assert {m.name for m in tar.getmembers()}=={row['path'] for row in rows}
    for row in rows:
        raw=tar.extractfile(row['path']).read();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
shutil.copytree(owner/'guest',out/'guest')
for name in ['config.json','vm-result.json','guest-manifest.json']:
    if (owner/name).exists():shutil.copy2(owner/name,out/name)
write(out/'export-result.json',{'original_exit':rc,'host_files':len(rows),'lossless_export_verified':True,'accepted':False,
 'scope':'Original serial phase outputs/receipts and value-free guest records only. Backup logs/archive and synthetic settings remain private in the stopped owned disk until explicit retirement.',
 'next':'Coordinator reviews originals, explicitly consumes admission, then retires owned VM disk/media/UEFI.'})
print(json.dumps({'packet':str(out),'original_exit':rc,'owners_absent':pids}))
