from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, shutil, subprocess
old = Path('/workspace/tmp/pixelelated-m7-sweep-13')
owner = old.with_name('pixelelated-m7-sweep-14')
assert json.loads((old/'owner-verification.json').read_text())['result']=='FAILED'
report=json.loads((old/'artifacts/artifact-report.json').read_text())
expected={
 '84b5540b90c4553448bf12307e8ffc2854cee70e8bb8e2a5699878be8504d9ce':'    # RC2 moved /GAMES to /ROCKNIX but left /GAMES-replaced behind. Check',
 '63e752a50618b8a29703ae2e736aca10d9b4ca39c11f0e040060899abf4bcae5':'    # device still selects ROCKNIX. A live earlier sibling remains excluded.',
}
assert len(report['findings'])==2
assert {r['context_sha256'] for r in report['findings']}==set(expected)
assert all(r['type']=='branding' and r['path']=='usr/bin/cloud_migrate_layout' for r in report['findings'])
source=Path('projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout').read_text()
assert not owner.exists();owner.mkdir(mode=0o700);(owner/'artifacts').mkdir(mode=0o700)
names=['run.py','outer.sh','verify-inputs.py','scan-artifact.py','allowlist.json','secret-patterns','context-review.json','context-controls.py','check-controls.py','parse-theme.cpp','reconcile-locales.py']
for name in names:
 text=(old/name).read_text()
 if name not in ['allowlist.json','secret-patterns','context-review.json']:text=text.replace(old.name,owner.name)
 (owner/name).write_text(text);shutil.copymode(old/name,owner/name)
 if name.endswith('.py'):ast.parse(text)
 if name.endswith('.sh'):subprocess.run(['bash','-n',str(owner/name)],check=True)
allow=json.loads((owner/'allowlist.json').read_text())
review=json.loads((owner/'context-review.json').read_text())
added=[]
for digest,text in expected.items():
 assert text in source and hashlib.sha256(text.encode()).hexdigest()==digest
 row={'path':'usr/bin/cloud_migrate_layout','context_sha256':digest,'disposition':'KEEP','issue':478,
      'reason':'Source comment documents actual ROCKNIX RC2 /GAMES-replaced recovery and preservation of an earlier-layout sibling. Historical compatibility evidence, not active OS branding.'}
 allow['branding'].append(row);review['contexts'].append(dict(row,text=text));added.append(row)
(owner/'allowlist.json').write_text(json.dumps(allow,indent=2)+'\n')
(owner/'context-review.json').write_text(json.dumps(review,indent=2)+'\n')
(owner/'provenance.json').write_text(json.dumps({'prepared_utc':datetime.now(timezone.utc).isoformat(),'parent':str(old),
 'classification_review':added,'unchanged':'Scanner, secret patterns and all prior classifications; only two exact source-comment contexts added.',
 'state':'prepared, not submitted'},indent=2)+'\n')
files=sorted(p for p in owner.iterdir() if p.is_file())
(owner/'harness.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p)+'\n' for p in files))
print(owner)
