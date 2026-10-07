from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,shutil
base=Path('/workspace/tmp');build=base/'pixelelated-m7-replacement-16';old=base/'pixelelated-m7-p4-inherited-shelf-01';owner=base/'pixelelated-m7-p4-build16-inherited-shelf-01'
assert json.loads((build/'completion.json').read_text())['result']=='PASS'
manifest=build/'inputs.json';j=json.loads(manifest.read_text());mh=hashlib.sha256(manifest.read_bytes()).hexdigest()
assert not owner.exists();owner.mkdir(mode=0o700);(owner/'proof').mkdir(mode=0o700)
mapping={old.name:owner.name,'m7-pixelelated-replacement15':'m7-pixelelated-replacement16','pixelelated-m7-replacement-15':'pixelelated-m7-replacement-16','ed5a6a51f5974deec8748fbf0dbd2f4984b690f5':j['distribution_commit'],'0bc7c44d06fc0180eaa170d8ec68bad2247c34af90319a9491beafeb538580d6':mh}
for name in ['run.py','extra-boundaries.py','verify-inputs.py']:
 s=(old/name).read_text()
 for a,b in mapping.items():s=s.replace(a,b)
 ast.parse(s);(owner/name).write_text(s);shutil.copymode(old/name,owner/name)
(owner/'provenance.json').write_text(json.dumps({'prepared_utc':datetime.now(timezone.utc).isoformat(),'parent':str(old),'state':'prepared, not submitted','distribution_commit':j['distribution_commit'],'ES_commit':j['emulationstation_commit'],'manifest_sha256':mh,'scope':'Installed candidate16 recovers historical RC2/GAMES-replaced and actual historical record-copy/record-delete states; original bytes and repeated-apply idempotence required.'},indent=2)+'\n')
files=[owner/name for name in ['run.py','extra-boundaries.py','verify-inputs.py','provenance.json']]
files.extend(Path(j['host_worktree'])/name for name in j['qa_source_files'])
(owner/'seal.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n');print(owner)
