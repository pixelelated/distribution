"""Preserve completed original CHD family receipts; never delete build inputs."""
from pathlib import Path
import argparse, hashlib, io, json, tarfile
p=argparse.ArgumentParser()
p.add_argument('--owner',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
a=p.parse_args();owner=a.owner;out=a.packet
assert owner.parent==Path('/workspace/tmp') and owner.resolve()==owner
assert Path('/proc/self/ns/pid').stat().st_ino==4026531836
files={};summary={}
def collect(root,prefix):
    for f in sorted(root.rglob('*')):
        assert not f.is_symlink()
        if f.is_file():
            assert f.stat().st_size<32*1024**2
            files[prefix+'/'+str(f.relative_to(root))]=f
for stage in sorted((owner/'stages').iterdir()):
    completion=json.loads((stage/'host-completion.json').read_text())
    assert not any(Path('/proc',str(pid)).exists() for pid in completion['actual_host_pids_absent'])
    run=Path(completion['run']);assert (run/'admission-consumed.json').is_file()
    result=json.loads((stage/'result.json').read_text())
    assert result['cleanup']['status']=='PASS' and not result['cleanup']['forced_stop']
    assert result['cleanup']['exact_id_absent'] and not result['cleanup']['survivors']
    summary[stage.name]={'status':result['status'],'original_container_exit':result['original_container_exit'],'run':str(run)}
    collect(stage,'owner/stages/'+stage.name);collect(run,'run/'+run.name)
for f in owner.iterdir():
    if f.is_file():files['owner/'+f.name]=f
out.mkdir(parents=True)
manifest={}
with tarfile.open(out/'original-records.tar.gz','x:gz') as tar:
    for name,f in sorted(files.items()):
        data=f.read_bytes();info=tarfile.TarInfo(name);info.size=len(data);info.mode=0o644;info.mtime=0
        tar.addfile(info,io.BytesIO(data));manifest[name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
with tarfile.open(out/'original-records.tar.gz') as tar:
    assert set(tar.getnames())==set(manifest)
    for name,row in manifest.items():
        data=tar.extractfile(name).read();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
(out/'original-records.json').write_text(json.dumps(manifest,indent=2)+'\n')
(out/'export-result.json').write_text(json.dumps({'lossless_export_verified':True,'files':len(manifest),'stages':summary,'work_retired':False},indent=2)+'\n')
print(json.dumps({'packet':str(out),'files':len(manifest),'archive_bytes':(out/'original-records.tar.gz').stat().st_size,'work_retired':False}))
