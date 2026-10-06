"""Prepare candidate16 clean/upgrade and raw/update payload proofs after its build is verified."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,shutil,subprocess
base=Path('/workspace/tmp');parent=base/'pixelelated-m7-qa-19';owner=base/'pixelelated-m7-qa-20'
image_parent=base/'pixelelated-m7-image-15';image=base/'pixelelated-m7-image-16'
build=base/'pixelelated-m7-replacement-16';manifest=build/'inputs.json';j=json.loads(manifest.read_text());mh=hashlib.sha256(manifest.read_bytes()).hexdigest()
assert json.loads((build/'completion.json').read_text())['result']=='PASS'
assert j['emulationstation_commit']==json.loads((base/'pixelelated-m7-p4-es-interruption-copy-publication-01/publication.json').read_text())['commit']
assert not owner.exists() and not image.exists()
replace={'pixelelated-m7-qa-19':'pixelelated-m7-qa-20','pixelelated-m7-image-15':'pixelelated-m7-image-16','m7-pixelelated-replacement15':'m7-pixelelated-replacement16','pixelelated-m7-replacement-15':'pixelelated-m7-replacement-16','ed5a6a51f5974deec8748fbf0dbd2f4984b690f5':j['distribution_commit'],'ed5a6a51f5':j['distribution_commit'][:10],'0bc7c44d06fc0180eaa170d8ec68bad2247c34af90319a9491beafeb538580d6':mh}
for old,new,names in [(parent,owner,['verify-inputs.py','check-payload.py','identity-frames.py','proxy-identity.py','qualify.sh','outer.sh','verify-renderer.py','es_lifecycle.py','identity.steps']),(image_parent,image,['verify-inputs.py','run.sh','extract.py','outer.sh'])]:
 new.mkdir(mode=0o700);(new/'artifacts').mkdir(mode=0o700)
 for name in names:
  s=(old/name).read_text()
  for a,b in replace.items():s=s.replace(a,b)
  (new/name).write_text(s);shutil.copymode(old/name,new/name)
  if name.endswith('.py'):ast.parse(s)
  if name.endswith('.sh'):subprocess.run(['bash','-n',str(new/name)],check=True)
 proof={'prepared_utc':datetime.now(timezone.utc).isoformat(),'state':'prepared, not submitted','parent_owner':str(old),'distribution_commit':j['distribution_commit'],'ES_commit':j['emulationstation_commit'],'manifest_sha256':mh,'boundary':'Fresh candidate16 installed bytes; actual ROCKNIX RC2 upgrade and clean install; no new account reset or personal provider. Supplemental corrected-source retry and EN/FR640/1280 proofs remain separately required.'}
 (new/'provenance.json').write_text(json.dumps(proof,indent=2)+'\n');files=sorted(p for p in new.iterdir() if p.is_file());(new/'harness.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p)+'\n' for p in files));print(json.dumps(proof))
