from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, shutil, subprocess
base=Path('/workspace/tmp');old=base/'pixelelated-m7-cloud-01';owner=base/'pixelelated-m7-cloud-02';qa=base/'pixelelated-m7-qa-20'
assert not owner.exists();owner.mkdir(mode=0o700);(owner/'artifacts').mkdir(mode=0o700)
for name in ['qualify.sh','outer.sh']:
 text=(old/name).read_text().replace(old.name,owner.name).replace('m7-pixelelated-replacement14','m7-pixelelated-replacement16').replace('replacement14','replacement16')
 (owner/name).write_text(text);shutil.copymode(old/name,owner/name);subprocess.run(['bash','-n',str(owner/name)],check=True)
for name in ['check-payload.py','proxy-identity.py','verify-inputs.py']:
 text=(qa/name).read_text().replace(qa.name,owner.name)
 (owner/name).write_text(text);ast.parse(text)
manifest=base/'pixelelated-m7-replacement-16/inputs.json';j=json.loads(manifest.read_text())
(owner/'provenance.json').write_text(json.dumps({'prepared_utc':datetime.now(timezone.utc).isoformat(),'parent':str(old),
 'distribution_commit':j['distribution_commit'],'ES_commit':j['emulationstation_commit'],'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),
 'scope':'Renew the existing D-QA-058 WebDAV/SFTP/MinIO-S3 round-trip baseline on candidate16 installed cloud scripts. No hosted account, new RA reset or opt-in suite expansion.',
 'state':'prepared, not submitted'},indent=2)+'\n')
files=sorted(p for p in owner.iterdir() if p.is_file())
(owner/'harness.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p)+'\n' for p in files))
print(owner)
