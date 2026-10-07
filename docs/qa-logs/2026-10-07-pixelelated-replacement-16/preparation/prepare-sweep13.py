from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, shutil, subprocess
old = Path('/workspace/tmp/pixelelated-m7-sweep-12')
owner = old.with_name('pixelelated-m7-sweep-13')
assert json.loads((old / 'owner-verification.json').read_text())['result'] == 'FAILED'
assert not owner.exists()
owner.mkdir(mode=0o700)
(owner / 'artifacts').mkdir(mode=0o700)
names = ['run.py','outer.sh','verify-inputs.py','scan-artifact.py','allowlist.json',
         'secret-patterns','context-controls.py','check-controls.py','parse-theme.cpp','reconcile-locales.py']
for name in names:
    text = (old/name).read_text()
    if name not in ['allowlist.json','secret-patterns']:
        text = text.replace(old.name, owner.name)
    (owner/name).write_text(text)
    shutil.copymode(old/name, owner/name)
    if name.endswith('.py'): ast.parse(text)
    if name.endswith('.sh'): subprocess.run(['bash','-n',str(owner/name)],check=True)
source = Path('/workspace/tmp/pixelelated-m7-sweep-11/context-review.json')
shutil.copy2(source, owner/'context-review.json')
assert (owner/'context-review.json').read_bytes() == source.read_bytes()
rows = json.loads(source.read_text())['contexts']
allow = json.loads((owner/'allowlist.json').read_text())
for row in rows:
    assert any((r['path'],r['context_sha256']) == (row['path'],row['context_sha256']) for r in allow['branding'])
(owner/'provenance.json').write_text(json.dumps({
    'prepared_utc':datetime.now(timezone.utc).isoformat(), 'parent':str(old),
    'correction':'Include the required byte-identical prior context-review fixture, omitted by the candidate16 preparer. No allowlist, scanner or product changes.',
    'context_fixture_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'contexts':len(rows),'state':'prepared, not submitted'},indent=2)+'\n')
files = sorted(p for p in owner.iterdir() if p.is_file())
(owner/'harness.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p)+'\n' for p in files))
print(owner)
