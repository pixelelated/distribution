#!/usr/bin/env python3
"""UNRUN source derivative of accepted pix-m7-close-vm.py; export, never consume/delete."""
import argparse,hashlib,json,shutil,subprocess,tarfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--owner',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);a=p.parse_args()
owner=a.owner.resolve(strict=True);run=a.run.resolve(strict=True);out=a.packet.absolute();config=json.loads((owner/'config.json').read_text());tree=Path(config['checkout'])
def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(path,value):
    with path.open('x') as f:json.dump(value,f,indent=2);f.write('\n')
assert Path('/proc/self/ns/pid').stat().st_ino==4026531836
assert run.parent==tree/'.build-runs' and owner.parent==out.parent==Path('/workspace/tmp') and not out.exists()
launcher=json.loads((owner/'lifecycle-owner/launcher-result.json').read_text());rc=launcher['runner_returncode'];assert rc in (0,1)
assert (owner/'lifecycle-owner/tool-wrapper.rc').read_text().strip()==str(rc) and (run/'build.rc').read_text().strip()==str(rc)
rr=json.loads((run/'runner-result.json').read_text());assert rr['runner_rc']==rr['command_rc']==rc and rr['monitor_rc']==0
vm=json.loads((owner/'vm-result.json').read_text());assert vm['rc']==rc
pids=[b['pid'] for b in vm['boots']]+[launcher['pid']]+[int((run/n).read_text()) for n in ['build.pid','command.pid','watcher.pid']]
assert all(not Path('/proc',str(pid)).exists() for pid in pids)
if vm['boots']:assert 'down: owned QEMU exited' in (owner/'vm-stop.log').read_text()
if rc==0:
    assert len(vm['boots'])==1 and not vm['cleanup_errors']
    assert 'PIX_UNMOUNT_RC:0' in (owner/'unmount-640x480.txt').read_text()
out.mkdir();write(out/'host-exits.json',{'original_exit':rc,'pids_absent':pids,'actual_host_namespace':4026531836})
guest_files=[];readback_rc=None
if (owner/'vm/output.ext4').exists():
    (out/'guest').mkdir()
    r=subprocess.run(['debugfs','-R','rdump / '+str(out/'guest'),str(owner/'vm/output.ext4')],capture_output=True,text=True,timeout=30)
    (out/'debugfs.stdout').write_text(r.stdout);(out/'debugfs.stderr').write_text(r.stderr);readback_rc=r.returncode
    assert r.returncode==0 and not any(f.is_symlink() for f in (out/'guest').rglob('*'))
    guest_files=[f for f in (out/'guest').rglob('*') if f.is_file()]
    assert len(guest_files)<=1024 and sum(f.stat().st_size for f in guest_files)<=32*1024**2
    write(out/'guest-manifest.json',[{'path':str(f.relative_to(out/'guest')),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(guest_files)])
if rc==0:
    root=out/'guest/installed588';guest=json.loads((root/'outer-guest-result.json').read_text());own=json.loads((root/'original-owner/owner-result.json').read_text());payload=json.loads((root/'original-owner/payload/result.json').read_text())
    assert guest['status']==own['status']==payload['status']=='PASS'
    assert own['original_child_exit']==0 and not own['timed_out'] and not own['signals'] and own['remaining_children']==[]
    assert not guest['forced_cleanup'] and not guest['cleanup_errors'] and not own['cleanup_errors'] and not payload['cleanup_errors']
    original=[r for r in guest['commands'] if r['name']=='original-systemd-run'];assert len(original)==1 and original[0]['original_returncode']==0 and not original[0]['timed_out']
    assert sha(root/'binding.json')==sha(owner/'records/binding.json')
    for row in json.loads((root/'original-owner-manifest.json').read_text()):assert sha(root/'original-owner'/row['path'])==row['sha256']
# Preserve original failures too. Failure export does not grant acceptance or consumption.
sources=[]
for base,label in [(owner,'owner'),(run,'run')]:
    for f in sorted(base.rglob('*')):
        if f.is_symlink() or not f.is_file() or (base==owner and f.is_relative_to(owner/'vm')):continue
        assert f.stat().st_size<32*1024**2;sources.append((f,label+'/'+str(f.relative_to(base))))
with tarfile.open(out/'original-records.tar.gz','x:gz') as tar:
    for f,name in sources:tar.add(f,arcname=name,recursive=False)
rows=[{'path':name,'bytes':f.stat().st_size,'sha256':sha(f)} for f,name in sources];write(out/'original-records.json',rows)
with tarfile.open(out/'original-records.tar.gz') as tar:
    assert {m.name for m in tar.getmembers()}=={r['path'] for r in rows}
    for row in rows:
        raw=tar.extractfile(row['path']).read();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
for name in ['vm-result.json','config.json']:shutil.copy2(owner/name,out/name)
write(out/'export-result.json',{'original_exit':rc,'guest_files':len(guest_files),'host_files':len(rows),'lossless_export_verified':True,'readback_rc':readback_rc,'accepted':False,'next':'Coordinator reviews original receipts, then explicitly consumes admission and retires scratch. No publication or RC claim.'})
print(json.dumps({'packet':str(out),'original_exit':rc,'owners_absent':pids,'exported_guest_files':len(guest_files)}))
