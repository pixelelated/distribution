from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, sys
owner=Path(sys.argv[1]).resolve(strict=True)
assert owner.name.startswith('pixelelated-m7-')
receipt=json.loads((owner/'owner-verification.json').read_text())
dest=Path.cwd()/'docs/qa-logs/2026-10-07-pixelelated-replacement-16'/owner.name.removeprefix('pixelelated-m7-')
dest.mkdir()
for p in owner.iterdir():
 if p.is_file() and (p.suffix in ['.py','.sh','.json','.jsonl','.sha256','.log','.rc','.path','.cpp'] or p.name=='secret-patterns'):
  assert p.name!='inputs.json' and p.stat().st_size<30_000_000
  shutil.copy2(p,dest/p.name)
if (owner/'artifacts').is_dir():shutil.copytree(owner/'artifacts',dest/'artifacts')
run=Path((owner/'run.path').read_text().strip());(dest/'watcher').mkdir()
for name in ['build.rc','build.status','build.log','build.pid','watcher.pid','command.pid','job.json','result.json']:
 if (run/name).is_file():shutil.copy2(run/name,dest/'watcher'/name)
for p in dest.rglob('*'):
 if p.is_file():
  assert p.suffix not in ['.qcow2','.img','.pcap']
  assert b'-----BEGIN ' + b'OPENSSH PRIVATE KEY-----' not in p.read_bytes()
(dest/'retention.json').write_text(json.dumps({'retained_utc':datetime.now(timezone.utc).isoformat(),'owner':str(owner),'result':receipt['result'],'scope':'Host artifact checks only. No guest, raw image, compiled helper or input-manifest duplicate copied.'},indent=2)+'\n')
(dest/'sha256.json').write_text(json.dumps({str(p.relative_to(dest)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dest.rglob('*')) if p.is_file()},indent=2)+'\n')
print(dest)
