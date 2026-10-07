from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

q = Path('docs/qa-logs/2026-10-07-pixelelated-replacement-16')
matrix = q / 'p4-build16-installed-matrix-01'
artifact = matrix / 'proof/artifacts'
collision = q / 'p4-build16-collision-01'
dest = q / 'matrix-primary-reconciliation'
assert not dest.exists()
read = lambda p: json.loads(p.read_text())
sha = lambda data: hashlib.sha256(data).hexdigest()
rows = read(artifact / 'results.json')
assert len(rows) == 85 and sum(r['status'] == 'PASS' for r in rows) == 84
assert [r['case'] for r in rows if r['status'] != 'PASS'] == ['T23-content-collision']
assert set(read(matrix / 'owner-verification.json')['channels'].values()) == {'1'}
assert read(matrix / 'guest-cleanup-verification.json')['passed']
assert set(read(collision / 'owner-verification.json')['channels'].values()) == {'0'}
assert read(collision / 'guest-cleanup-verification.json')['passed']
assert read(collision / 'proof/artifacts/results.json') == [{'case': 'T23-content-collision', 'status': 'PASS'}]
for path in [matrix, collision]:
    assert read(path / 'owner-verification.json')['sealed_inputs'] == 212

classifications = {
    'empty': ('empty', ''), 'unrelated': ('empty', ''),
    'fallback': ('found-elsewhere', '/pixelelated/Content'), 'tiered': ('ok', ''),
    'root-tiered': ('ok', ''), 'root-flat': ('ok', ''),
    'root-unrelated': ('empty', ''), 'stranded': ('stranded-at-root', '/'),
    'refused': ('unreadable', None),
}
discovery = {}
for case, (state, found) in classifications.items():
    logs = []
    for p in sorted(artifact.glob('*-PL001-discovery-' + case + '-*.log')):
        facts = dict(line.split('=', 1) for line in p.read_text().splitlines()
                     if line.startswith(('STATE=', 'FOUND=')))
        if facts.get('STATE') == state:
            assert found is None or facts.get('FOUND') == found
            rc = int(p.with_suffix('.rc').read_text())
            assert (rc != 0) == (case == 'refused')
            logs.append(dict(file=p.name, sha256=sha(p.read_bytes()), facts=facts, returncode=rc))
    assert len(logs) == 1, (case, logs)
    discovery[case] = logs[0]

sibling = {}
for label, content in [('root', ''), ('custom', '/Mine/Content'), ('current', '/pixelelated/Content')]:
    final = read(artifact / ('PL003-kept-sibling-' + label + '-final.json'))
    assert final['a']['CONTENT_REMOTE'] == content and final['a']['SAVES_REMOTE'] == '/pixelelated/Saves'
    assert final['b']['SAVES_REMOTE'] == '/ROCKNIX/Saves' and final['b']['LAYOUT_KEEP'] == '/ROCKNIX/Saves'
    assert final['cloud']['ROCKNIX/Saves/gb/kept.srm'] == sha(b'sibling progress\n')
    assert final['cloud']['ROCKNIX/Saves-replaced/stamp/gb/older.srm'] == sha(b'sibling older progress\n')
    sibling[label] = final

binding = {}
for kind in ['comments', 'format', 'token', 'endpoint', 'legacy']:
    final = read(artifact / ('PL004-binding-' + kind + '-final.json'))
    assert final['cloud']['pixelelated/Saves/gb/A.srm'] == sha(b'save witness\n')
    assert final['cloud']['pixelelated/Content/ROMs/gb/A.gb'] == sha(b'content witness\n')
    assert final['a']['SAVES_REMOTE'] == '/pixelelated/Saves'
    assert final['a']['CONTENT_REMOTE'] == '/pixelelated/Content'
    if kind == 'endpoint':
        assert final['cloud']['other-cloud/foreign-witness.txt'] == sha(b'other connection\n')
        reasons = []
        for p in sorted(artifact.glob('*-PL004-binding-endpoint-*.log')):
            if '>>> why THE PREVIOUS CLOUD MOVE NEEDS ITS ORIGINAL CONNECTION' in p.read_text():
                assert int(p.with_suffix('.rc').read_text()) != 0
                reasons.append(p.name)
        assert len(reasons) == 3
        binding[kind] = dict(recovered_original_bytes=True, refusal_logs=reasons, foreign_endpoint_unchanged=True)
    else:
        binding[kind] = dict(recovered_original_bytes=True)

reasons = {}
for kind in ['future', 'malformed', 'config', 'record']:
    expected = "YOUR CLOUD SYNC SETTINGS COULDN'T BE READ" if kind == 'config' else "YOUR CLOUD FOLDER COULDN'T BE READ"
    matches = []
    for p in sorted(artifact.glob('*-PL005-reason-' + kind + '-*.log')):
        lines = p.read_text().splitlines()
        if '>>> why ' + expected in lines:
            assert int(p.with_suffix('.rc').read_text()) != 0
            assert not any("COULDN'T FIND YOUR CLOUD FOLDER" in line for line in lines)
            matches.append(p.name)
    assert len(matches) == 1, (kind, matches)
    reasons[kind] = dict(reason=expected, raw_log=matches[0])

result = dict(verified_utc=datetime.now(timezone.utc).isoformat(),
              original_matrix=dict(passed=84, failed=1, failed_case='T23-content-collision', lifecycle_result=1),
              corrected_collision=dict(case='T23-content-collision', result='PASS', lifecycle_result=0),
              discovery=discovery, active_sibling_shelves=sibling, connection_binding=binding,
              application_reasons=reasons,
              scope='Independent reconciliation of key installed CLI outcomes and retained witness hashes. Full clean/upgrade/protocol gates remain pending; no issue or original failed run is relabeled.')
dest.mkdir()
(dest / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
(dest / 'verify.py').write_bytes(Path(__file__).read_bytes())
print('Verified nine discovery classifications, three active sibling shelves, five connection-binding recoveries and four refusal reasons. Original 84/1 result preserved.')
