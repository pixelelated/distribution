#!/usr/bin/env python3
"""Static inspection only: parse and hash files, never import/execute fixtures."""
import ast
import difflib
import gzip
import hashlib
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
sha = lambda value: hashlib.sha256(value).hexdigest()
inputs_bytes = (root/'fixture-inputs.json').read_bytes()
inputs = json.loads(inputs_bytes)
for name, expected in inputs.items():
    assert sha((root/name).read_bytes()) == expected, name
fixture_ast = ast.parse((root/'fixtures/probe.py').read_bytes())
constant = next(n.value.value for n in fixture_ast.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'INPUTS_SHA256' for t in n.targets))
assert constant == sha(inputs_bytes)
parsed = []
for path in sorted(root.rglob('*.py')):
    ast.parse(path.read_bytes(), filename=str(path))
    parsed.append(str(path.relative_to(root)))
bindings = json.loads((root/'bindings.json').read_text())
patches = []
for name, entry in bindings['candidates'].items():
    before = (root/'source'/name).read_bytes()
    after = (root/'candidates'/name).read_bytes()
    patch = gzip.decompress((root/'candidates'/entry['patch']).read_bytes())
    assert sha(before) == entry['baseline_sha256']
    assert sha(after) == entry['candidate_sha256']
    assert sha(patch) == entry['uncompressed_patch_sha256']
    expected = ''.join(difflib.unified_diff(before.decode().splitlines(True),
                      after.decode().splitlines(True), fromfile='a/'+entry['target'],
                      tofile='b/'+entry['target'])).encode()
    assert patch == expected, name
    patches.append({'name': name, 'uncompressed_patch_sha256': sha(patch),
                    'candidate_sha256': sha(after)})

def nodes(path):
    return {node.name: ast.dump(node, include_attributes=False)
            for node in ast.parse(path.read_bytes()).body
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
old, new = [nodes(root/variant/'rvz_datasource.py') for variant in ('source','candidates')]
assert old.keys() == new.keys()
assert [name for name in old if old[name] != new[name]] == ['_generate_rvz_bytes']
assert (root/'source/rvz_datasource.py').read_bytes() == (root/'research/current-rvz_datasource.py').read_bytes()
for variant in ('source','candidates'):
    ctl = (root/variant/'raofflineproxy-ctl').read_text()
    extracted = ctl.split('list_jobs() {',1)[1].split("<<'PY'\n",1)[1].split('\nPY\n}',1)[0]+'\n'
    assert extracted.encode() == (root/variant/'list_jobs.py').read_bytes()
for path in (root/'source').glob('*.sha256'):
    expected, name = path.read_text().split()
    assert sha(gzip.decompress((path.parent/(name+'.gz')).read_bytes())) == expected
for path in root.rglob('*'):
    if path.is_file() and path.suffix != '.gz':
        assert not any(line.endswith((b' ',b'\t')) for line in path.read_bytes().splitlines()), str(path)
print(json.dumps({'status':'PASS', 'evidence':'AST/source/hash/whitespace inspection ONLY',
                  'python':sys.version, 'parsed_files':parsed, 'sealed_input_files':len(inputs),
                  'patches':patches, 'runtime':'UNRUN; no fixture import or execution'}, indent=2))
