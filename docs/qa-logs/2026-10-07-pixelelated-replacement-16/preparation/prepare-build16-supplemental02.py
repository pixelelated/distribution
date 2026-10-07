from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json
old=Path('/workspace/tmp/pixelelated-m7-p4-build16-supplemental-01')
owner=Path('/workspace/tmp/pixelelated-m7-p4-build16-supplemental-02')
assert not owner.exists(); owner.mkdir(mode=0o700)
(owner/'proof').mkdir(mode=0o700)
for name in ['run.py','extra-boundaries.py','verify-inputs.py']:
 data=(old/name).read_bytes(); ast.parse(data); (owner/name).write_bytes(data)
provenance=json.loads((old/'provenance.json').read_text())
provenance.update(prepared_utc=datetime.now(timezone.utc).isoformat(),parent=str(old),correction='Create the fresh empty proof directory required by both watch-build --activity-dir and Proof.__init__. No case function or product change; first launch stopped before a watcher run or guest existed.')
(owner/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
inputs={n:h for n,h in json.loads((old/'seal.json').read_text()).items() if not n.startswith(str(old)+'/')}
for p in owner.iterdir():
 if p.is_file():inputs[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
assert len(inputs)==212
for name,digest in inputs.items():assert hashlib.sha256((Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16')/name).read_bytes()).hexdigest()==digest,name
assert (owner/'proof').is_dir() and not any((owner/'proof').iterdir())
(owner/'seal.json').write_text(json.dumps(inputs,indent=2)+'\n')
print(owner,'212 verified seals; activity/output directory exists and is empty')
