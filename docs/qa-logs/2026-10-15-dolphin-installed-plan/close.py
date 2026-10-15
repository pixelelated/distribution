#!/usr/bin/env python3
"""UNRUN stopped-owner exporter; preserves failures, never consumes or deletes media."""
import argparse,hashlib,json,shutil,subprocess,tarfile
from pathlib import Path
p=argparse.ArgumentParser()
for name in ['owner','run','packet']:p.add_argument('--'+name,type=Path,required=True)
a=p.parse_args();owner=a.owner.resolve(strict=True);run=a.run.resolve(strict=True);out=a.packet.absolute();config=json.loads((owner/'config.json').read_text());tree=Path(config['checkout'])
def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def write(path,value):
    with path.open('x') as stream:json.dump(value,stream,indent=2);stream.write('\n')
assert Path('/proc/self/ns/pid').stat().st_ino==4026531836
assert run.parent==tree/'.build-runs' and owner.parent==out.parent==Path('/workspace/tmp') and not out.exists()
launcher=json.loads((owner/'lifecycle-owner/launcher-result.json').read_text());rc=launcher['runner_returncode'];assert rc in (0,1)
assert (owner/'lifecycle-owner/tool-wrapper.rc').read_text().strip()==(run/'build.rc').read_text().strip()==str(rc)
runner=json.loads((run/'runner-result.json').read_text());assert runner['runner_rc']==runner['command_rc']==rc and runner['monitor_rc']==0
vm=json.loads((owner/'vm-result.json').read_text());assert vm['rc']==rc
pids=[launcher['pid']]+[int((run/name).read_text()) for name in ['build.pid','command.pid','watcher.pid']]+[b['pid'] for b in vm['boots']]
assert all(not Path('/proc',str(pid)).exists() for pid in pids)
assert vm.get('remaining_host_children')==[], 'host children must be observed absent'
if vm['boots']:assert 'down: owned QEMU exited' in (owner/'vm-stop.log').read_text()
if rc==0:
    assert len(vm['boots'])==1 and not vm['cleanup_errors'] and not vm.get('forced_host_child_cleanup')
    assert (owner/'unmount-640x480.txt').read_text()=='PIX_UNMOUNT_RC:0\n'
out.mkdir(mode=0o700);write(out/'host-exits.json',{'original_exit':rc,'pids_absent':pids,'actual_host_namespace':4026531836})
guest_rows=[];readback_rc=None;manifest_verified=False;readback_error=None
if (owner/'vm/output.ext4').exists():
    (out/'guest').mkdir()
    try:
        command=['debugfs','-R','rdump / '+str(out/'guest'),str(owner/'vm/output.ext4')]
        child=subprocess.run(command,capture_output=True,timeout=60)
        (out/'debugfs.stdout').write_bytes(child.stdout);(out/'debugfs.stderr').write_bytes(child.stderr);readback_rc=child.returncode
        assert readback_rc==0 and not any(f.is_symlink() for f in (out/'guest').rglob('*'))
        files=sorted(f for f in (out/'guest').rglob('*') if f.is_file())
        assert len(files)<=257 and sum(f.stat().st_size for f in files)<=210*1024**2
        guest_rows=[{'path':str(f.relative_to(out/'guest')),'bytes':f.stat().st_size,'sha256':sha(f)} for f in files]
        manifest=out/'guest/guest-export-manifest.json'
        if manifest.exists():
            originals=json.loads(manifest.read_text())
            assert originals==[r for r in guest_rows if r['path']!='guest-export-manifest.json']
            manifest_verified=True
    except BaseException as exc:readback_error=type(exc).__name__+': '+str(exc)
write(out/'guest-manifest.json',guest_rows)
write(out/'readback-result.json',{'original_returncode':readback_rc,'manifest_verified':manifest_verified,'error':readback_error})
# Always retain host originals, even when a failed guest cannot yield a complete manifest.
originals=[]
for base,label in [(owner,'owner'),(run,'run')]:
    for f in sorted(base.rglob('*')):
        if f.is_symlink() or not f.is_file() or (base==owner and f.is_relative_to(owner/'vm')):continue
        assert f.stat().st_size<32*1024**2;originals.append((f,label+'/'+str(f.relative_to(base))))
with tarfile.open(out/'original-records.tar.gz','x:gz') as tar:
    for f,name in originals:tar.add(f,arcname=name,recursive=False)
rows=[{'path':name,'bytes':f.stat().st_size,'sha256':sha(f)} for f,name in originals];write(out/'original-records.json',rows)
with tarfile.open(out/'original-records.tar.gz') as tar:
    assert {m.name for m in tar.getmembers()}=={r['path'] for r in rows}
    for row in rows:
        raw=tar.extractfile(row['path']).read();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
for name in ['config.json','vm-result.json']:shutil.copy2(owner/name,out/name)
validation_error=None
try:
    if rc==0:
        assert readback_rc==0 and manifest_verified and readback_error is None
        root=out/'guest/native-owner';own=json.loads((root/'owner-result.json').read_text())
        assert (out/'guest/guest-owner.rc').read_text().strip()=='0'
        assert own['status']=='PASS' and own['original_child_exit']==0 and not own['timed_out']
        assert own['remaining_children']==[] and not own['signals'] and not own['reaped'] and not own['cleanup_errors']
        assert own['case_seal']==config['case_seal'] and own['verification_sha256']==config['verification_sha256']
        for row in own['copied_case_files']:assert sha(root/row['path'])==row['sha256']
        case=root/'case';proof=json.loads((case/'result.json').read_text())
        assert proof['status']=='PASS' and len(proof['rows'])==3
        assert [row['case'] for row in proof['rows']]==['installed-enabled','installed-disabled','installed-failed-boot']
        assert all(row['status']=='PASS' and row['remaining_dolphin']==[] and not row.get('endpoint_errors') for row in proof['rows'])
        assert [row['original_exit'] for row in proof['rows']]==[0,0,1]
        assert len(proof['rows'][0]['requests'])==1 and proof['rows'][0]['initialized']==proof['rows'][0]['shutdown']==1
        assert not proof['rows'][1]['requests'] and not proof['rows'][1]['initialized'] and not proof['rows'][1]['shutdown']
        assert proof['rows'][2]['boot_error'] and proof['rows'][2]['initialized']==proof['rows'][2]['shutdown']==1 and len(proof['rows'][2]['requests'])<=1
        assert all(proof['installed_before'][key]==proof['installed_after'][key] for key in ['executable','resources']) and proof['source_commit']==config['commit']
        installed=proof['installed_before'];assert len(installed['resources'])==6
        assert installed['executable']['path']=='/usr/bin/dolphin-emu-nogui'
        expected=json.loads((owner/'records/final-image-result.json').read_text())['products']['usr/bin/dolphin-emu-nogui']
        assert installed['executable']['sha256']==expected['sha256'] and installed['executable']['bytes']==expected['bytes']
        resources=json.loads((owner/'source/case/resources.json').read_text())['resources']
        for found,expected_resource in zip(installed['resources'],resources,strict=True):
            assert found['path']=='/'+expected_resource['installed'] and found['resolved']==expected_resource['resolved']
            assert found['bytes']==expected_resource['bytes'] and found['sha256']==expected_resource['sha256']
            assert found['link_target']=='../../config/dolphin-emu'
        for row in proof['rows']:
            stderr=(case/row['case']/'stderr').read_text(errors='replace')
            assert row['badge_load_failures']=={message:stderr.count(message) for message in row['badge_load_failures']}
            assert row['argv'][0]=='/usr/bin/dolphin-emu-nogui' and row['binary_sha256']==expected['sha256']
            assert len(row['badge_load_failures'])==4 and not any(row['badge_load_failures'].values())
            if not row['badboot']:
                assert row['running_before']['exe']==row['running_after']['exe']=='/usr/bin/dolphin-emu-nogui'
                assert row['running_before']['exe_sha256']==row['running_after']['exe_sha256']==expected['sha256']

except BaseException as exc:validation_error=type(exc).__name__+': '+str(exc)
write(out/'analysis.json',{'original_exit':rc,'original_success_channels_verified':rc==0 and validation_error is None,'validation_error':validation_error,'runtime_acceptance':'coordinator review pending'})
write(out/'export-result.json',{'original_exit':rc,'guest_files':len(guest_rows),'host_files':len(rows),'readback_rc':readback_rc,
 'host_archive_verified':True,'guest_manifest_verified':manifest_verified,'lossless_export_verified':readback_error is None and manifest_verified,
 'validation_error':validation_error,'accepted':False,'next':'Coordinator reviews original receipts, consumes exact admission, then retires owned vm/ disk/media/UEFI.'})
print(json.dumps({'packet':str(out),'original_exit':rc,'owners_absent':pids,'readback_error':readback_error,'validation_error':validation_error}))
raise SystemExit(0 if readback_error is None and validation_error is None else 1)
