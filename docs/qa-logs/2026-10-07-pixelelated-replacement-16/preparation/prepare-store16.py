from pathlib import Path
import ast,hashlib,json
base=Path('/workspace/tmp');build=base/'pixelelated-m7-replacement-16';owner=base/'pixelelated-m7-store-16';tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16')
assert json.loads((build/'completion.json').read_text())['result']=='PASS'
assert not owner.exists();owner.mkdir(mode=0o700);(owner/'artifacts').mkdir(mode=0o700)
s=Path('docs/qa-logs/2026-10-06-pixelelated-replacement-15/store-15/run.py').read_text().replace('replacement15','replacement16').replace('replacement-15','replacement-16');ast.parse(s);(owner/'run.py').write_text(s)
paths=[owner/'run.py',tree/'tools/rasteratops-candidate-store',build/'inputs.json']
(owner/'seal.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2)+'\n');print(owner)
