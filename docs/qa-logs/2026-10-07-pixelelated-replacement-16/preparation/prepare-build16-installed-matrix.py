from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,shutil
base=Path('/workspace/tmp');build=base/'pixelelated-m7-replacement-16';old=base/'pixelelated-m7-p4-reader-values-04';owner=base/'pixelelated-m7-p4-build16-installed-matrix-01'
assert json.loads((build/'completion.json').read_text())['result']=='PASS'
manifest=build/'inputs.json';j=json.loads(manifest.read_text());mh=hashlib.sha256(manifest.read_bytes()).hexdigest();tree=Path(j['host_worktree'])
assert (old/'boundaries.py').read_bytes()==(tree/'tools/pixelelated-vm-cloud-boundaries').read_bytes(),'The corrected reader harness must match frozen QA source'
assert not owner.exists();owner.mkdir(mode=0o700);(owner/'proof').mkdir(mode=0o700)
mapping={old.name:owner.name,'m7-pixelelated-replacement15':'m7-pixelelated-replacement16','pixelelated-m7-replacement-15':'pixelelated-m7-replacement-16','ed5a6a51f5974deec8748fbf0dbd2f4984b690f5':j['distribution_commit'],'0bc7c44d06fc0180eaa170d8ec68bad2247c34af90319a9491beafeb538580d6':mh}
for name in ['run.py','reader-value-control.py','boundaries.py','verify-inputs.py']:
 s=(old/name).read_text()
 for a,b in mapping.items():s=s.replace(a,b)
 if name=='run.py':
  assert s.count(",'--case','PL008'")==1;s=s.replace(",'--case','PL008'",'')
 ast.parse(s);(owner/name).write_text(s);shutil.copymode(old/name,owner/name)
(owner/'provenance.json').write_text(json.dumps({'prepared_utc':datetime.now(timezone.utc).isoformat(),'parent':str(old),'state':'prepared, not submitted','distribution_commit':j['distribution_commit'],'ES_commit':j['emulationstation_commit'],'manifest_sha256':mh,'expected_cases':85,'scope':'Full installed migration/discovery/pointer/binding/reason/chooser/reader matrix. Uses the previously corrected reader observer, exact-value distractor, and actual old-scanner negative control. Full QA20, historical-shelf and direct UI proofs remain separate.'},indent=2)+'\n')
files=sorted(p for p in owner.iterdir() if p.is_file())+[tree/name for name in j['qa_source_files']]
(owner/'seal.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n');print(owner)
