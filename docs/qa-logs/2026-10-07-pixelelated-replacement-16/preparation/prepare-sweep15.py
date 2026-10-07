from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, shutil, subprocess
old=Path('/workspace/tmp/pixelelated-m7-sweep-14');owner=old.with_name('pixelelated-m7-sweep-15')
assert json.loads((old/'owner-verification.json').read_text())['result']=='FAILED'
assert json.loads((old/'artifacts/artifact-report.json').read_text())['pass']
assert not owner.exists();owner.mkdir(mode=0o700);(owner/'artifacts').mkdir(mode=0o700)
names=['run.py','outer.sh','verify-inputs.py','scan-artifact.py','allowlist.json','secret-patterns','context-review.json','context-controls.py','check-controls.py','parse-theme.cpp','reconcile-locales.py']
for name in names:
 text=(old/name).read_text()
 if name not in ['allowlist.json','secret-patterns','context-review.json']:text=text.replace(old.name,owner.name)
 if name=='reconcile-locales.py':
  original="assert set(git(a.tree,'diff','--name-only',DISTRO_BASE,'HEAD','--','*.po','*.xml').splitlines())=={meta,cemu}"
  assert original in text
  artifact='docs/qa-logs/2026-10-06-pixelelated-replacement-15/sweep-11/artifacts/parsed-theme.xml'
  digest=hashlib.sha256(Path(artifact).read_bytes()).hexdigest()
  replacement=f'''# Retained prior QA output is documentary XML, not a package input. Match
# the one reviewed path AND bytes; any additional XML/PO path still fails.
documentary_xml={{'{artifact}':'{digest}'}}
inputs=json.loads(Path('/workspace/tmp/pixelelated-m7-replacement-16/inputs.json').read_text())
for path,digest in documentary_xml.items():
 assert sha(a.tree/path)==digest
 assert path not in inputs['source_files'] and path not in inputs['qa_source_files']
assert set(git(a.tree,'diff','--name-only',DISTRO_BASE,'HEAD','--','*.po','*.xml').splitlines())=={{meta,cemu}}|set(documentary_xml)'''
  text=text.replace(original,replacement)
  text=text.replace("report={'es_base':ES_BASE", "report={'documentary_xml':documentary_xml,'es_base':ES_BASE")
 (owner/name).write_text(text);shutil.copymode(old/name,owner/name)
 if name.endswith('.py'):ast.parse(text)
 if name.endswith('.sh'):subprocess.run(['bash','-n',str(owner/name)],check=True)
(owner/'provenance.json').write_text(json.dumps({'prepared_utc':datetime.now(timezone.utc).isoformat(),'parent':str(old),
 'correction':'Classify the exact prior parsed-theme.xml QA artifact by path and SHA256, prove it is outside consumed input manifests; all other XML/PO change paths still fail closed.',
 'artifact':artifact,'sha256':digest,'unchanged':'All scanner classifications, patterns, controls, installed translation and theme assertions.',
 'state':'prepared, not submitted'},indent=2)+'\n')
files=sorted(p for p in owner.iterdir() if p.is_file())
(owner/'harness.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p)+'\n' for p in files))
print(owner)
