#!/usr/bin/env python3
"""Positive/negative controls for the image sweep; no secret literals at rest."""
import importlib.util
import json
from pathlib import Path
import re
import shlex
import tempfile

here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('sweep', here / 'scan-artifact.py')
sweep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sweep)
repo = here.parents[2]
line, = [s for s in (repo / '.githooks/secret-patterns').read_text().splitlines()
         if s.startswith('SECRET_PATTERNS=')]
patterns = re.compile(shlex.split(line)[0].split('=', 1)[1].encode())
results = []


def check(name, condition):
    assert condition, name
    results.append({'case': name, 'pass': True})


with tempfile.TemporaryDirectory(prefix='pixelelated-sweep-control-') as tmp:
    root = Path(tmp)
    file = root / 'sample'
    allow = {'branding': [], 'public_patterns': []}
    file.write_bytes(b'pixelelated\n')
    check('clean input passes', sweep.scan(root, allow, patterns)['pass'])
    file.write_bytes(b'Welcome to ROCKNIX\n')
    check('unclassified old product text fails', not sweep.scan(root, allow, patterns)['pass'])
    sha, = sweep.contexts(file.read_bytes())
    allow['branding'] = [{'path': 'sample', 'context_sha256': sha, 'disposition': 'KEEP'}]
    check('reviewed exact context passes', sweep.scan(root, allow, patterns)['pass'])
    file.write_bytes(b'Welcome to ROCKNIX changed\n')
    check('changed text is not covered by prior approval', not sweep.scan(root, allow, patterns)['pass'])
    file.write_bytes(b'Welcome to ROCKNIX\n')
    allow['branding'][0]['disposition'] = 'FIX'
    check('known unresolved defect still fails', not sweep.scan(root, allow, patterns)['pass'])
    allow['branding'] = []
    # Build the intentionally fake credential only in the temporary fixture.
    file.write_bytes(b'dev' + b'password=' + b'fixture' * 4)
    check('credential injection fails', not sweep.scan(root, allow, patterns)['pass'])
    allow['public_patterns'] = [{'path': 'sample', 'file_sha256': sweep.digest(file.read_bytes()), 'matches': 1}]
    check('exact reviewed public-pattern file passes', sweep.scan(root, allow, patterns)['pass'])
    file.write_bytes(file.read_bytes() + b'changed')
    check('changed public-pattern file fails', not sweep.scan(root, allow, patterns)['pass'])
    file.write_bytes(b'pixelelated\n')
    (root / 'legacy-link').symlink_to('/nonexistent/ROCKNIX')
    report = sweep.scan(root, allow, patterns)
    check('absolute guest link is recorded, never followed', report['pass'] and report['counts']['legacy_symlink_paths'] == 1)
    file.chmod(0)
    try:
        sweep.scan(root, allow, patterns)
    except (PermissionError, RuntimeError):
        check('unreadable input refuses a verdict', True)
    else:
        raise AssertionError('unreadable input did not fail')
    finally:
        file.chmod(0o600)

print(json.dumps({'passed': len(results), 'failed': 0, 'results': results}, indent=2))
