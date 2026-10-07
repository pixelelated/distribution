from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,shutil,subprocess
base=Path('/workspace/tmp');build=base/'pixelelated-m7-replacement-16';bundle=Path((base/'pixelelated-m7-store-16/bundle.path').read_text().strip());manifest=build/'inputs.json';j=json.loads(manifest.read_text());mh=hashlib.sha256(manifest.read_bytes()).hexdigest()
assert json.loads((build/'completion.json').read_text())['result']=='PASS'
assert json.loads((base/'pixelelated-m7-store-16/owner-verification.json').read_text())['result']=='PASS'
common={'m7-pixelelated-replacement15':'m7-pixelelated-replacement16','pixelelated-m7-replacement-15':'pixelelated-m7-replacement-16','pixelelated-m7-image-15':'pixelelated-m7-image-16','ed5a6a51f5974deec8748fbf0dbd2f4984b690f5':j['distribution_commit'],'bab4df649f48847cc43d21c77c058107ad902754':j['emulationstation_commit'],'0bc7c44d06fc0180eaa170d8ec68bad2247c34af90319a9491beafeb538580d6':mh,'43a698bcd7d570c63ebdd5db015e5302463f7ee4a15438fd9ef2359437be19da':bundle.name,'candidate15':'candidate16','replacement15':'replacement16'}
for kind,names in [('sweep',['run.py','outer.sh','verify-inputs.py','scan-artifact.py','allowlist.json','secret-patterns','context-controls.py','check-controls.py','parse-theme.cpp','reconcile-locales.py']),('inventory',['run.sh','outer.sh','verify-inputs.py','source-inventory.py','qualify-inventory.py','component-map.py'])]:
 old=base/('pixelelated-m7-'+kind+'-11');owner=base/('pixelelated-m7-'+kind+'-12');assert not owner.exists();owner.mkdir(mode=0o700);(owner/'artifacts').mkdir(mode=0o700)
 mapping=dict(common);mapping[old.name]=owner.name
 for name in names:
  raw=(old/name).read_text()
  # Classification is carried byte-identical; new contexts must fail for review.
  if name not in ['allowlist.json','secret-patterns']:
   for a,b in mapping.items():raw=raw.replace(a,b)
  (owner/name).write_text(raw);shutil.copymode(old/name,owner/name)
  if name.endswith('.py'):ast.parse(raw)
  if name.endswith('.sh'):subprocess.run(['bash','-n',str(owner/name)],check=True)
 (owner/'provenance.json').write_text(json.dumps({'prepared_utc':datetime.now(timezone.utc).isoformat(),'state':'prepared, not submitted','parent':str(old),'distribution_commit':j['distribution_commit'],'ES_commit':j['emulationstation_commit'],'manifest_sha256':mh,'bundle':str(bundle),'scope':'Exact candidate16 artifact and consumed source checks. Existing image-context allowlist unchanged; new contexts require explicit review. Known P5 license gaps remain tracked.'},indent=2)+'\n')
 files=sorted(p for p in owner.iterdir() if p.is_file());(owner/'harness.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p)+'\n' for p in files));print(owner)
