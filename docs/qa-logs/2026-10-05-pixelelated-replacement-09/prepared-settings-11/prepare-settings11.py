from pathlib import Path
import ast,hashlib,json,shutil,subprocess
old=Path('/workspace/tmp/pixelelated-m7-settings-10');new=Path('/workspace/tmp/pixelelated-m7-settings-11');assert not new.exists();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((old/'completion.json').read_text());assert receipt['actual_tool_rc']==1 and receipt['qemu_absent'];paths=[]
for line in (old/'harness.sha256').read_text().splitlines():
 h,n=line.split(None,1);p=Path(n);assert sha(p)==h;paths.append(p)
root=Path('/workspace/tmp/pixelelated-m7-image-11/root');prior=json.loads((old/'expected.json').read_text());current={p:sha(root/p.lstrip('/')) for p in prior};assert prior['/usr/bin/emulationstation']!=current['/usr/bin/emulationstation'];assert all(prior[k]==current[k] for k in prior if k!='/usr/bin/emulationstation')
new.mkdir();(new/'artifacts').mkdir()
for p in paths:
 out=new/p.name;shutil.copyfile(p,out)
 if out.suffix in {'.py','.sh','.json'}:out.write_text(out.read_text().replace(str(old),str(new)))
(new/'expected.json').write_text(json.dumps(current,indent=2)+'\n')
p=new/'guest-proof.py';s=p.read_text().replace("check('installed bytes ' + path, sha(Path(path).read_bytes()) == digest, sha256=digest)","actual = sha(Path(path).read_bytes())\n        check('installed bytes ' + path, actual == digest, actual_sha256=actual, expected_sha256=digest)")
s=s.replace("check('unchanged installed bytes ' + path, sha(Path(path).read_bytes()) == digest)","actual = sha(Path(path).read_bytes())\n            check('unchanged installed bytes ' + path, actual == digest, actual_sha256=actual, expected_sha256=digest)");p.write_text(s)
proof={'issue':443,'original_completion':receipt,'extracted_root':str(root),'payload_equality':json.loads(Path('/workspace/tmp/pixelelated-m7-image-11/artifacts/payload-equality.json').read_text()),'prior_expected':prior,'current_expected':current,'obsolete_digest_rejected':current['/usr/bin/emulationstation']!=prior['/usr/bin/emulationstation'],'source_assertions_unchanged':True};(new/'correction-provenance.json').write_text(json.dumps(proof,indent=2)+'\n')
# Fail before any VM if the extracted-image-derived expectations are stale again.
p=new/'run.sh';s=p.read_text();needle='python3 "$TASK_OWNER/verify-inputs.py" "$TASK_BUNDLE"';at=s.index(needle)+len(needle);s=s[:at]+'''
python3 - <<'EXPECTED'
from pathlib import Path
import hashlib,json
root=Path('/workspace/tmp/pixelelated-m7-image-11/root');owner=Path('/workspace/tmp/pixelelated-m7-settings-11')
for name,wanted in json.loads((owner/'expected.json').read_text()).items():assert hashlib.sha256((root/name.lstrip('/')).read_bytes()).hexdigest()==wanted,name
print('PASS expectations match independently extracted immutable candidate')
EXPECTED
'''+s[at:];p.write_text(s)
for p in sorted(new.iterdir()):
 if not p.is_file():continue
 if p.suffix=='.py':ast.parse(p.read_text())
 if p.suffix=='.sh':subprocess.run(['bash','-n',str(p)],check=True)
paths=sorted(p for p in new.iterdir() if p.is_file());(new/'harness.sha256').write_text(''.join(f'{sha(p)}  {p}\n' for p in paths))
for p in paths+[new/'harness.sha256']:p.chmod(0o500 if p.suffix=='.sh' else 0o400)
print('PASS settings11 fresh sealed owner; three expected hashes bound to actual image, original rejection preserved; 13 source members')
