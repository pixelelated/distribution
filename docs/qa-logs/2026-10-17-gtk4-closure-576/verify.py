#!/usr/bin/env python3
"""Verify this evidence packet only; never execute its captured tools."""
import argparse
import hashlib
import gzip
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--originals', action='store_true', help='also require unchanged original absolute source files')
args = parser.parse_args()
root = Path(__file__).resolve().parent
entries = {}
for line in (root / 'SHA256SUMS').read_text().splitlines():
    digest, name = line.split('  ', 1)
    path = Path(name)
    if path.is_absolute() or '..' in path.parts or name in entries:
        raise SystemExit('invalid manifest path: ' + name)
    entries[name] = digest
actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p != root / 'SHA256SUMS'}
expected = set(entries)
if actual != expected:
    raise SystemExit('manifest file-set mismatch')
for name, digest in entries.items():
    path = root / name
    if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise SystemExit('hash mismatch: ' + name)
originals = json.loads((root / 'original-files.json').read_text())['lossless_originals']
for item in originals:
    data = (root / item['packet_path']).read_bytes()
    if item.get('encoding') == 'gzip':
        data = gzip.decompress(data)
    if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
        raise SystemExit('original copy mismatch: ' + item['packet_path'])
    if args.originals:
        source = Path(item['source'])
        if source.is_symlink() or source.read_bytes() != data:
            raise SystemExit('source changed: ' + str(source))
print(json.dumps({'status': 'PASS', 'manifest_entries': len(entries), 'lossless_originals': len(originals), 'source_paths_compared': args.originals, 'target_execution': False}))
