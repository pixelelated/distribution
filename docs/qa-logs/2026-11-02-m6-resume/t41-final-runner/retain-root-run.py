#!/usr/bin/env python3
"""Retain completed, masked command receipts; never execute an acceptance gate."""
import collections
import hashlib
import json
import pathlib
import re

SOURCE = pathlib.Path('/workspace/tmp/m6-coordinator/kit/selftest/accept-t41-candidate-01a19d12/root-final-e481-20261102T2023')
DEST = pathlib.Path(__file__).resolve().parent / 'root-final-run'
sha = lambda b: hashlib.sha256(b).hexdigest()

def main():
    result = json.loads((SOURCE / 'driver-result.json').read_text())
    assert result['status'] == 'complete' and result['rc'] == 1
    gate_dirs = list((SOURCE / 'evidence').glob('final-gates-*'))
    assert len(gate_dirs) == 1
    gates = gate_dirs[0]
    receipts = sorted(gates.glob('[0-9]*.json'))
    labels = collections.Counter()
    records = []
    for f in receipts:
        raw = f.read_bytes()
        d = json.loads(raw)
        assert not d['fixture'] and not d['timed_out'] and d['problem'] is None
        assert d['lane_tip'] == result['argv'][2] and d['coordinator_tip'] == result['argv'][3]
        assert d['executor'] == result['executor']
        row = {'file': f.name, 'sha256': sha(raw), 'text': raw.decode('utf-8'), 'outputs': {}}
        for stream in ('stdout', 'stderr'):
            filename = d[stream]
            assert pathlib.Path(filename).name == filename
            data = (gates / filename).read_bytes()
            assert sha(data) == d[stream + '_masked_sha256']
            row['outputs'][stream] = {'file': filename, 'sha256': sha(data), 'text': data.decode('utf-8')}
        labels[(re.sub(r'-\d+$', '-N', d['label']), d['rc'])] += 1
        records.append(row)
    DEST.mkdir(exist_ok=True)
    pack = DEST / 'command-receipts.jsonl'
    with pack.open('w') as out:
        for row in records:
            out.write(json.dumps(row, ensure_ascii=True, separators=(',', ':')) + '\n')
    for name in ('driver-start.json', 'driver-result.json', 'driver.stdout', 'driver.stderr', 'accept.out'):
        (DEST / name).write_bytes((SOURCE / name).read_bytes())
    (DEST / 'verdicts.tsv').write_bytes((SOURCE / 'evidence/verdicts.tsv').read_bytes())
    for name in ('append-merge.json', 'whitespace-cached.json', 'whitespace-tips.json'):
        (DEST / name).write_bytes((gates / name).read_bytes())
    verdicts = [line.split('\t') for line in (DEST / 'verdicts.tsv').read_text().splitlines()]
    assert len(verdicts) == 54
    assert [(r[0], r[1]) for r in verdicts if r[0] != 'PASS'] == [('FAIL', 'issue-body')]
    assert sha((DEST / 'driver.stdout').read_bytes()) == result['stdout_sha256']
    assert sha((DEST / 'driver.stderr').read_bytes()) == result['stderr_sha256']
    manifest = {
        'schema': 1, 'source': str(SOURCE), 'executor': result['executor'],
        'lane_tip': result['argv'][2], 'coordinator_tip': result['argv'][3],
        'original_result': {'rc': 1, 'pass': 53, 'fail': ['issue-body']},
        'storage': 'Each JSONL row holds the exact original command JSON and exact masked stdout/stderr as UTF-8 strings. Decode text and re-encode UTF-8 to recover bytes. Raw pre-mask hashes remain in each command receipt; no claim that masked and original bytes are identical.',
        'commands': len(records),
        'command_groups': [{'label': k, 'rc': rc, 'count': n} for (k, rc), n in sorted(labels.items())],
        'files': {f.name: {'bytes': f.stat().st_size, 'sha256': sha(f.read_bytes())} for f in sorted(DEST.iterdir()) if f.is_file() and f.name != 'manifest.json'},
    }
    (DEST / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'commands': len(records), 'pack_bytes': pack.stat().st_size, 'pack_sha256': sha(pack.read_bytes()), 'original_pass': 53, 'original_fail': 1}))

if __name__ == '__main__':
    main()
