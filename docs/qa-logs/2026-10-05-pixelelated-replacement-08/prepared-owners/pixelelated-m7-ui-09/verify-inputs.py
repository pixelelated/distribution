"""Refuse qualification of a changed source tree or unrelated candidate bundle."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

owner = Path('/workspace/tmp/pixelelated-m7-replacement-08')
manifest = owner / 'inputs.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest() == '7578b0d91f2f043b492d998c2f8bd4a73467a1524ae692366469153e2eb5c17b'
inputs = json.loads(manifest.read_text())
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == inputs['distribution_commit']
for name, wanted in inputs['source_files'].items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == wanted, name
for name, wanted in inputs['qa_source_files'].items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == wanted, name
for name, wanted in inputs['source_symlinks'].items():
    assert Path(name).is_symlink() and os.readlink(name) == wanted, name
es = os.environ['ES_SRC']
assert subprocess.check_output(['git', '-C', es, 'rev-parse', 'HEAD'], text=True).strip() == inputs['emulationstation_commit']
assert not subprocess.check_output(['git', '-C', es, 'status', '--porcelain'], text=True).strip()
bundle = Path(sys.argv[1])
assert json.loads((bundle / 'manifest.json').read_text())['inputs'] == inputs
for suffix in ['img.gz', 'tar']:
    assert (bundle / ('pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.' + suffix)).is_file()
print('PASS frozen source inputs, ES pin and candidate input custody')
