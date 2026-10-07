from pathlib import Path
import datetime,hashlib,json,shutil,sys
owner=Path(sys.argv[1]).resolve(strict=True)
repo=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
qa=repo/'docs/qa-logs/2026-10-07-pixelelated-replacement-16'
assert owner.name.startswith('pixelelated-m7-')
assert (owner/'owner-verification.json').is_file()
assert json.loads((owner/'guest-cleanup-verification.json').read_text())['passed']
dest=qa/owner.name.removeprefix('pixelelated-m7-');dest.mkdir()
for p in owner.iterdir():
    if p.is_file() and p.suffix not in ['.qcow2','.img','.pcap'] and p.name not in ['qa-key']:
        assert p.stat().st_size<20_000_000, (str(p),p.stat().st_size)
        shutil.copy2(p,dest/p.name)
for name in ['artifacts','proof/artifacts']:
    src=owner/name
    if src.is_dir():
        target=dest/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copytree(src,target,ignore=lambda d,n:[s for s in n if s.endswith(('.pcap','.qcow2','.img')) or s=='qa-key'])
for name in ['proof/cleanup.json']:
    src=owner/name
    if src.is_file():
        (dest/name).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest/name)
run=Path((owner/'run.path').read_text().strip());(dest/'watcher').mkdir()
for p in run.iterdir():
    if p.is_file() and p.name in ['build.rc','build.status','build.log','build.pid','watcher.pid','command.pid','job.json','result.json']:
        shutil.copy2(p,dest/'watcher'/p.name)
for p in dest.rglob('*'):
    if p.is_file():
        b=p.read_bytes()
        assert not any(marker in b for marker in [b'-----BEGIN ' + b'OPENSSH PRIVATE KEY-----',b'-----BEGIN ' + b'RSA PRIVATE KEY-----']),str(p)
(dest/'retention.json').write_text(json.dumps({'retained_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':str(owner),'omissions':'Guest disks/backing chains, pair keys, raw packet captures and cloud payloads remain at original runtime paths. Artifacts exclude private-key duplicates.','scope':'Command outputs and lifecycle evidence; semantic frame review is separate when applicable.'},indent=2)+'\n')
(dest/'sha256.json').write_text(json.dumps({str(p.relative_to(dest)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dest.rglob('*')) if p.is_file()},indent=2)+'\n')
print('Retained',dest)
