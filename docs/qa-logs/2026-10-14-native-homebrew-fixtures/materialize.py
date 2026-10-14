#!/usr/bin/env python3
"""Hash-check author fixtures and prepare a fresh staging directory; never execute them."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--cache', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
p.add_argument('--download', action='store_true', help='permit bounded official URL downloads')
a = p.parse_args()
manifest = Path(__file__).with_name('fixtures.json')
entries = json.loads(manifest.read_text())['artifacts']
staged = []
for e in entries:
    cache_name = e['url'].rsplit('/', 1)[1]
    source = a.cache / cache_name
    if source.exists():
        with source.open('rb') as f:
            data = f.read(e['download_bytes'] + 1)
    elif a.download:
        with urllib.request.urlopen(e['url'], timeout=30) as response:
            data = response.read(e['download_bytes'] + 1)
    else:
        p.error(f'missing cached artifact: {source}; --download permits its official URL')
    expected = e.get('archive_sha256', e['sha256'])
    if len(data) != e['download_bytes'] or hashlib.sha256(data).hexdigest() != expected:
        p.error(f'archive/download changed: {cache_name}')
    if 'member' in e:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            info = archive.getinfo(e['member'])
            if info.file_size != e['bytes']:
                p.error(f'member length changed: {cache_name}')
            data = archive.read(info)
    if len(data) != e['bytes'] or hashlib.sha256(data).hexdigest() != e['sha256']:
        p.error(f'fixture changed: {e["filename"]}')
    staged.append((e, data))
# Validate every input before any output. Never replace an existing staging tree.
a.out.mkdir(parents=False, exist_ok=False)
for e, data in staged:
    (a.out / e['filename']).write_bytes(data)
(a.out / 'SHA256SUMS').write_text(''.join(
    f'{e["sha256"]}  {e["filename"]}\n' for e, _ in staged))
(a.out / 'provenance.json').write_text(json.dumps({
    'fixture_manifest_sha256': hashlib.sha256(manifest.read_bytes()).hexdigest(),
    'runtime': 'UNRUN', 'artifacts': entries}, indent=2) + '\n')
print(f'Prepared {len(staged)} verified data files in {a.out}; no content executed')
