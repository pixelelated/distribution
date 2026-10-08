#!/usr/bin/env python3
"""Recheck retained primary review custody; this does not perform visual review."""
import argparse
import hashlib
import json
from pathlib import Path
import struct

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('evidence_root', type=Path, help='Scratch or compact published PL-003 root containing matrix02/04/05')
parser.add_argument('--complete', action='store_true', help='Require all 44 distinct reviewed outcomes')
args = parser.parse_args()
reviews = Path(__file__).resolve().parent
source_hash = 'e80b09fdee07043468154a4c9f9ec0a4fb7bdc9ba82f7c9d806b048d5cd3b010'
catalog_hash = 'f056223d0fa947a7c9790c914b7696586b168e33135c627ebbc4d1d6d530dfb4'
helper_hash = '1aa57c4d6162afb8f45f7464b79213ffb808b5b99d4869e4630d11ca889ede86'

def sha(data):
    return hashlib.sha256(data).hexdigest()

seen = set()
verified = []
for receipt in sorted(reviews.glob('frame-review-matrix*-batch*.json')):
    owner = receipt.stem.split('-')[2]
    assert owner in ('matrix02', 'matrix04', 'matrix05'), owner
    for row in json.loads(receipt.read_text()):
        key = row['locale'], row['resolution'], row['case']
        assert key not in seen, ('duplicate review', key)
        seen.add(key)
        assert row['primary_viewed_utc'] and row['visual_result'].startswith('PASS:'), key
        frame = args.evidence_root / owner / row['frame']
        data = frame.read_bytes()
        assert sha(data) == row['frame_sha256'], frame
        assert struct.unpack('>II', data[16:24]) == tuple(map(int, row['resolution'].split('x'))), frame
        case = frame.parent.parent
        before = (case / 'before.txt').read_bytes()
        assert before == (case / 'after.txt').read_bytes(), key
        assert sha(before) == row['map_sha256'], key
        if owner != 'matrix02':
            guards = sorted(case.glob('phase*-*.identity.txt'))
            assert len(guards) == 6, key
            identity = guards[0].read_bytes()
            assert all(p.read_bytes() == identity for p in guards), key
            assert sha(identity) == row['identity_sha256'], key
            lines = identity.decode().splitlines()
            assert lines[0] == (args.evidence_root / owner / 'boot-id.txt').read_text().strip(), key
            assert lines[1].startswith('ES_PID='), key
            assert lines[2].split()[0] == source_hash, key
            expected_helper = sha((args.evidence_root / owner / 'refusal-fixture.sh').read_bytes()) if row['injection'] else helper_hash
            assert lines[3].split()[0] == expected_helper, key
            assert lines[4].split()[0] == catalog_hash, key
            if row['injection']:
                assert row['proof_kind'] == 'injected status rendering only', key
            if row['case'] == 'bucket':
                assert 'InvalidBucketName' in (case / 'provider-probe.log').read_text(), key
        else:
            assert row['locale'] == 'en_US' and row['resolution'] == '640x480', key
            assert json.loads((reviews / 'reuse-provenance-primary.json').read_text())['result'].startswith('PASS reuse provenance'), key
        verified.append({'owner': owner, 'locale': key[0], 'resolution': key[1], 'case': key[2], 'frame_sha256': row['frame_sha256']})
if args.complete:
    cases = {'invalid-components', 'blank', 'root', 'invalid-name', 'invalid-characters', 'bucket', 'unreachable', 'busy', 'timeout', 'settings-write', 'unknown'}
    expected = {(locale, resolution, case) for locale in ['en_US', 'fr_FR'] for resolution in ['640x480', '1280x800'] for case in cases}
    assert seen == expected, {'missing': sorted(expected - seen), 'extra': sorted(seen - expected)}
print(json.dumps({'result': 'PASS', 'complete_matrix_required': args.complete, 'verified_reviews': len(verified), 'scope': 'Recomputes bytes, dimensions, state preservation and identity against already-recorded primary visual reviews; no new visual or runtime verdict.', 'reviews': verified}, indent=2))
