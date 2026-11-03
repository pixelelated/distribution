"""Compare named immutable D records; never invoke their producers."""
import hashlib
import json
from pathlib import Path
import subprocess
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
D = 'a0d4c4fda7a0c16c04d57edf921ffeb741eff19b'
SEED = '8710a6210a40de0110244d03a886161ee06faf29'
A = 'docs/audits/2026_11_03-epic-m6-records/'
commands = []

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    argv = ['git', '-C', str(REPO), *args]
    started = datetime.now(timezone.utc).isoformat()
    p = subprocess.run(argv, capture_output=True)
    commands.append({'argv': argv, 'start': started,
                     'end': datetime.now(timezone.utc).isoformat(),
                     'rc': p.returncode, 'stdout_sha256': sha(p.stdout),
                     'stderr_sha256': sha(p.stderr)})
    if p.returncode:
        raise RuntimeError('immutable Git read failed')
    return p.stdout

retention = json.loads((HERE / 'publication/retention.json').read_text())
entry = next(r for r in retention['files']
             if r['original_relative_path'] == 'final-manifest.json')
raw = json.loads((HERE / 'publication' / entry['stored']).read_text()).encode()
assert sha(raw) == entry['original_sha256'] == '46ecf1d456f71be015600ed5aec2bdceea51bb1b1946dc6ebda3126ad8870b8f'
manifest = json.loads(raw)
assert manifest['tip'] == D and manifest['seed'] == SEED
assert git('show', '-s', '--format=%P', D).decode().strip() == SEED
paths = [p.decode() for p in git('diff', '--name-only', '-z', SEED, D).split(b'\0') if p]
assert paths == [r['path'] for r in manifest['files']]
contents = {}
framing = hashlib.sha256()
for row in manifest['files']:
    b = git('show', D + ':' + row['path'])
    assert len(b) == row['bytes'] and sha(b) == row['sha256']
    contents[row['path']] = b
    framing.update((row['path'] + '\n').encode() + b + b'\n')
assert len(paths) == 314
assert sum(len(b) for b in contents.values()) == 22391067
assert framing.hexdigest() == manifest['stdin_sha256']
assert sha(json.dumps(manifest['files'], sort_keys=True, separators=(',', ':')).encode()) == manifest['file_manifest_sha256']

lint = json.loads(contents[A + 'stage-d/pre-issue-lint/receipt.json'])
seal = json.loads(contents[A + 'stage-d/sealed-manifest.json'])
prefixes = []
for name in ['04-analysis.md', '05-punch-list.md']:
    old = next(v for p, v in lint['inputs'].items() if p.endswith('/' + name))
    b = contents[A + name]
    assert sha(b[:old['bytes']]) == old['sha256'] and len(b) > old['bytes']
    prefixes.append({'path': A + name, 'earlier_bytes': old['bytes'],
                     'final_bytes': len(b), 'prefix_exact': True,
                     'earlier_equals_final': False})
for name in ['00-running-log.md', '06-audit-summary.md']:
    old = next(r for r in seal['files'] if r['path'] == A + name)
    b = contents[A + name]
    assert sha(b[:old['bytes']]) == old['sha256'] and len(b) > old['bytes']
    prefixes.append({'path': A + name, 'earlier_bytes': old['bytes'],
                     'final_bytes': len(b), 'prefix_exact': True,
                     'earlier_equals_final': False})

result = {'observed_at': datetime.now(timezone.utc).isoformat(),
          'program_sha256': sha(Path(__file__).read_bytes()),
          'scope': 'Named D final-file custody and four preserved earlier prefixes only; no producer or scanner replay',
          'tip': D, 'seed': SEED, 'files': len(paths),
          'logical_bytes': sum(len(b) for b in contents.values()),
          'stdin_sha256': framing.hexdigest(),
          'file_manifest_sha256': manifest['file_manifest_sha256'],
          'earlier_input_qualifications': prefixes, 'commands': commands}
(HERE / 'root-final-custody.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS D custody: 314 immutable files; four earlier prefixes exact, not final-input lints')
