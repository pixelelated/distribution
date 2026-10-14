#!/usr/bin/env python3
"""Static only: never execute/import prepared fixtures or product code."""
import ast,difflib,gzip,hashlib,json,sys
from pathlib import Path
root=Path(__file__).resolve().parent
base=root.parent/'2026-10-14-proxy-rvz-source'
sha=lambda b:hashlib.sha256(b).hexdigest()
for line in (base/'SHA256SUMS').read_text().splitlines():
 expected,name=line.split('  ',1);assert sha((base/name).read_bytes())==expected,name
inputs=(root/'fixture-inputs.json').read_bytes()
for name,expected in json.loads(inputs).items(): assert sha((root/name).read_bytes())==expected,name
p=root/'fixtures/probe.py';tree=ast.parse(p.read_bytes())
seal=next(n.value.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='INPUTS_SHA256' for t in n.targets))
assert seal==sha(inputs)
parsed=[]
for p in sorted(root.rglob('*.py')): ast.parse(p.read_bytes());parsed.append(str(p.relative_to(root)))
bind=json.loads((root/'bindings.json').read_text())
for name,item in bind['candidates'].items():
 old=(base/'source'/name).read_bytes();new=(root/'candidates'/name).read_bytes()
 assert sha(old)==item['baseline_sha256'] and sha(new)==item['candidate_sha256']
 patch=gzip.decompress((root/'candidates'/(name+'.patch.gz')).read_bytes())
 assert sha(patch)==item['uncompressed_patch_sha256']
 expected=''.join(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile='a/'+item['target'],tofile='b/'+item['target'])).encode()
 assert patch==expected
reviewed=(base/'candidates/rvz_datasource.py').read_text()
assert (root/'candidates/rvz_datasource.py').read_text()==reviewed.replace('bytes(output[leading_bytes:])','bytes(memoryview(output)[leading_bytes:])')
ctl=(root/'candidates/raofflineproxy-ctl').read_text()
assert 'if indexed_root and not any(path.is_relative_to(root) for path in failed_rvz_paths):' in ctl
extracted=ctl.split('list_jobs() {',1)[1].split("<<'PY'\n",1)[1].split('\nPY\n}',1)[0]+'\n'
assert extracted==(root/'candidates/list_jobs.py').read_text()
probe=(root/'fixtures/probe.py').read_text()
assert "'unrelated'" in probe and 'str(unrelated) not in walked_roots' in probe
for p in root.rglob('*'):
 if p.is_file() and p.suffix!='.gz': assert all(not l.endswith((b' ',b'\t')) for l in p.read_bytes().splitlines()),str(p)
print(json.dumps({'status':'PASS','evidence':'static AST/hash/diff/whitespace only','python':sys.version,'parsed':parsed,'base_manifest_sha256':sha((base/'SHA256SUMS').read_bytes()),'runtime':'UNRUN','cases_prepared':44},indent=2))
