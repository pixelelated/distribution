#!/usr/bin/env python3
"""Export original stopped-owner results; no acceptance, consumption or media deletion."""
import argparse,hashlib,json,re,shutil,subprocess,tarfile
from pathlib import Path
p=argparse.ArgumentParser()
for name in ['owner','run','packet']:p.add_argument('--'+name,type=Path,required=True)
p.add_argument('--retain-failed',action='store_true')
a=p.parse_args();owner=a.owner.resolve(strict=True);run=a.run.resolve(strict=True);out=a.packet.absolute();config=json.loads((owner/'config.json').read_text());tree=Path(config['checkout'])
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024**2),b''):h.update(chunk)
    return h.hexdigest()
def write(path,value):
    with path.open('x') as f:json.dump(value,f,indent=2);f.write('\n')
assert Path('/proc/self/ns/pid').stat().st_ino==4026531836
assert run.parent==tree/'.build-runs' and owner.parent==out.parent==Path('/workspace/tmp') and not out.exists()
assert re.fullmatch('pix[A-Za-z0-9_-]+',out.name), 'unambiguous debugfs output path required'
launcher=json.loads((owner/'lifecycle-owner/launcher-result.json').read_text());runner=json.loads((run/'runner-result.json').read_text());vm=json.loads((owner/'vm-result.json').read_text())
originals={'launcher':launcher['runner_returncode'],'runner':runner['runner_rc'],'command':runner['command_rc'],'monitor':runner['monitor_rc'],'vm':vm['rc'],
 'tool_wrapper':int((owner/'lifecycle-owner/tool-wrapper.rc').read_text()),'build':int((run/'build.rc').read_text())}
originals_pass=all(value==0 for value in originals.values())
assert originals_pass or a.retain_failed,'Original owner failed; explicit preservation mode required'
pids=[launcher['pid']]+[int((run/name).read_text()) for name in ['build.pid','command.pid','watcher.pid']]
if (owner/'qemu.json').exists():pids.append(json.loads((owner/'qemu.json').read_text())['pid'])
assert all(not Path('/proc',str(pid)).exists() for pid in pids)
assert not vm.get('remaining_host_children')
if vm['boots']:assert 'down: owned QEMU exited' in (owner/'vm-stop.log').read_text()
if originals_pass:
    assert len(vm['boots'])==1 and not vm['cleanup_errors'] and not vm.get('forced_host_child_cleanup')
    assert 'PIX_INSTALLED567_UNMOUNT_RC:0' in (owner/'unmount.txt').read_text()
out.mkdir(mode=0o700);write(out/'host-exits.json',{'originals':originals,'pids_absent':pids,'actual_host_namespace':4026531836})
guest=[];readback=None;qualified=False
medium=owner/'vm/output.ext4'
if medium.exists():
    assert medium.stat().st_size==256*1024**2
    destination=out/'guest';destination.mkdir()
    result=subprocess.run(['debugfs','-R','rdump / '+str(destination),str(medium)],capture_output=True,timeout=60)
    (out/'debugfs.stdout').write_bytes(result.stdout);(out/'debugfs.stderr').write_bytes(result.stderr);readback=result.returncode
    write(out/'debugfs-exit.json',{'original_returncode':readback});assert readback==0
    paths=list(destination.rglob('*'));assert len(paths)<=160 and not any(f.is_symlink() for f in paths)
    guest=[f for f in paths if f.is_file()];assert sum(f.stat().st_size for f in guest)<=116*1024**2
    manifest=destination/'guest-export-manifest.json'
    if manifest.exists():
        rows=json.loads(manifest.read_text());assert len(rows)<=128 and sum(r['bytes'] for r in rows)<=112*1024**2
        expected=set()
        for row in rows:
            path=Path(row['path']);assert not path.is_absolute() and '..' not in path.parts and path.parts[0]=='installed567'
            f=destination/path;assert f.stat().st_size==row['bytes'] and sha(f)==row['sha256'];expected.add(f)
        assert expected==set(guest)-{manifest},'missing or unbound original guest evidence'
        root=destination/'installed567';original_rows=root/'fixture-originals.json';archive_path=root/'fixture-originals.tar.gz';objects={}
        if original_rows.exists() and archive_path.exists():
            members=json.loads(original_rows.read_text());assert len(members)<=2048
            with tarfile.open(archive_path,'r:gz') as tar:
                entries=tar.getmembers();assert [m.name for m in entries]==[r['path'] for r in members]
                for m,row in zip(entries,members):
                    name=Path(m.name);assert not name.is_absolute() and '..' not in name.parts and m.name!='key.pem'
                    assert m.mode==row['mode']
                    if row['kind']=='symlink':assert m.issym() and m.linkname==row['target']
                    else:
                        assert m.isfile() and 0<=m.size==row['bytes']<=8*1024**2
                        data=tar.extractfile(m).read();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
                        if m.name in ['result.json','worker-result.json','lock-custody-result.json','backend-after.json']:objects[m.name]=json.loads(data)
        if originals_pass:
            outer=json.loads((root/'outer-guest-result.json').read_text());fixture=objects['result.json'];worker=objects['worker-result.json'];lock=objects['lock-custody-result.json']
            assert outer['status']=='PASS' and not outer['forced_children'] and not outer['cleanup_errors'] and not outer['remaining_children']
            commands=[r for r in outer['commands'] if r['name']=='original-fixture'];assert len(commands)==1 and commands[0]['original_returncode']==0 and not commands[0]['timed_out']
            assert fixture['passed'] and fixture['worker_exit']==0 and not fixture['timeout'] and fixture['interrupted_signal'] is None and fixture['parent_unchanged']
            assert not fixture['stragglers_killed'] and not fixture['namespace_processes_remaining']
            assert worker['passed'] and worker['es_exit']==worker['listener_exit']==0 and not worker['es_forced'] and worker['output_guard_passed']
            assert worker['topup_exits']==[0] and worker['installed_observers']['all_exited'] and objects['backend-after.json']['passed'] and lock['passed'] and not lock['errors']
            assert sha(root/'binding.json')==sha(owner/'records/binding.json')
            restored=json.loads((root/'frontend-restored.json').read_text());binding=json.loads((root/'binding.json').read_text())
            assert restored['boot_id']==binding['boot_id'] and restored['installed_es_sha256']==binding['files']['/usr/bin/emulationstation']['sha256']
            clean=json.loads((owner/'clean/report.json').read_text());assert clean['status']=='pass';qualified=True
    else:assert a.retain_failed,'guest final manifest absent'
assert qualified or a.retain_failed,'Original guest success path did not qualify'
# Archive the original host records after all owners have exited, excluding disposable media.
sources=[]
for base,label in [(owner,'owner'),(run,'run')]:
    for f in sorted(base.rglob('*')):
        if f.is_symlink() or not f.is_file() or (base==owner and f.is_relative_to(owner/'vm')):continue
        assert f.stat().st_size<32*1024**2;sources.append((f,label+'/'+str(f.relative_to(base))))
assert sum(f.stat().st_size for f,_ in sources)<=96*1024**2
with tarfile.open(out/'original-host-records.tar.gz','x:gz') as tar:
    for f,name in sources:tar.add(f,arcname=name,recursive=False)
rows=[{'path':name,'bytes':f.stat().st_size,'sha256':sha(f)} for f,name in sources];write(out/'original-host-records.json',rows)
with tarfile.open(out/'original-host-records.tar.gz') as tar:
    assert {m.name for m in tar.getmembers()}=={r['path'] for r in rows}
    for row in rows:
        raw=tar.extractfile(row['path']).read();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
write(out/'guest-readback.json',[{'path':str(f.relative_to(out/'guest')),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(guest)])
for name in ['vm-result.json','config.json']:shutil.copy2(owner/name,out/name)
write(out/'export-result.json',{'originals':originals,'readback_original_exit':readback,'lossless_export_verified':True,'fixture_pass':qualified,'accepted':False,
 'scope':'One actual installed native ES to ctl/cache/TLS/SQLite/stamp continuation with synthetic loopback provider and accepted interface-availability seam. No product overlays; no repeated four UI/API cases.',
 'next':'Coordinator reviews original results, consumes admission, then retires this exact disk/media/UEFI and synthetic scratch. Export success alone is not runtime acceptance.'})
print(json.dumps({'packet':str(out),'fixture_pass':qualified,'originals':originals}))
