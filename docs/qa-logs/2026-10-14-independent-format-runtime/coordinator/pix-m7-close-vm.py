from pathlib import Path
import argparse, datetime, hashlib, json, shutil, subprocess, tarfile

p=argparse.ArgumentParser()
p.add_argument('--owner',type=Path,required=True)
p.add_argument('--run',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
a=p.parse_args()
repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup')
owner=a.owner; run=a.run; out=a.packet
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):
    with path.open('x') as f:json.dump(value,f,indent=2);f.write('\n')
assert Path('/proc/self/ns/pid').stat().st_ino==4026531836
assert run.parent==repo/'.build-runs' and owner.parent==Path('/workspace/tmp')
launcher=json.loads((owner/'lifecycle-owner/launcher-result.json').read_text())
rc=launcher['runner_returncode'];assert rc in (0,1)
assert (owner/'lifecycle-owner/tool-wrapper.rc').read_text().strip()==str(rc)
assert (run/'build.rc').read_text().strip()==str(rc)
rr=json.loads((run/'runner-result.json').read_text())
assert rr['runner_rc']==rr['command_rc']==rc and rr['monitor_rc']==0
vm=json.loads((owner/'vm-result.json').read_text());assert vm['rc']==rc and len(vm['boots'])==1
pids=[vm['boots'][0]['pid'],launcher['pid']]+[int((run/n).read_text()) for n in ['build.pid','command.pid','watcher.pid']]
assert all(not Path('/proc',str(pid)).exists() for pid in pids)
assert 'down: owned QEMU exited' in (owner/'vm-stop.log').read_text()
flush=owner/('unmount-640x480.txt' if rc==0 else 'finally-flush.txt')
assert ('PIX_UNMOUNT_RC:0' if rc==0 else 'PIX_FINALLY_FLUSH_RC:0') in flush.read_text()
out.mkdir(parents=True);(out/'guest').mkdir()
write(out/'host-exits.json',{'pids_absent':pids,'actual_host_namespace':4026531836})
readback=subprocess.run(['debugfs','-R','rdump / '+str(out/'guest'),str(owner/'vm/output.ext4')],capture_output=True,text=True,timeout=30)
(out/'debugfs.stdout').write_text(readback.stdout);(out/'debugfs.stderr').write_text(readback.stderr)
assert readback.returncode==0
guest_files=[f for f in (out/'guest').rglob('*') if f.is_file()]
assert guest_files, 'No exported guest evidence'
assert not any(f.is_symlink() for f in (out/'guest').rglob('*'))
write(out/'guest-manifest.json',[{'path':str(f.relative_to(out/'guest')),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(guest_files)])
sources=[]
for root,label in [(owner,'owner'),(run,'run')]:
    for f in sorted(root.rglob('*')):
        if f.is_symlink() or not f.is_file() or (root==owner and f.is_relative_to(owner/'vm')):continue
        assert f.stat().st_size<32*1024**2, str(f)
        sources.append((f,label+'/'+str(f.relative_to(root))))
with tarfile.open(out/'original-records.tar.gz','x:gz') as archive:
    for f,name in sources:archive.add(f,arcname=name,recursive=False)
rows=[{'path':name,'bytes':f.stat().st_size,'sha256':sha(f)} for f,name in sources]
write(out/'original-records.json',rows)
with tarfile.open(out/'original-records.tar.gz') as archive:
    assert {f.name for f in archive.getmembers() if f.isfile()}=={row['path'] for row in rows}
    for row in rows:
        data=archive.extractfile(row['path']).read()
        assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
for name in ['vm-result.json','vm-stop.log','records/inputs.json']:
    shutil.copy2(owner/name,out/Path(name).name)
shutil.copy2(flush,out/flush.name)
write(out/'export-result.json',{'original_exit':rc,'guest_files':len(guest_files),'host_files':len(rows),'lossless_export_verified':True,'readback_rc':readback.returncode})
print(json.dumps({'packet':str(out),'original_exit':rc,'owners_absent':pids,'exported_files':len(guest_files),'next':'Inspect original guest outcomes, then explicitly consume and retire.'}))
