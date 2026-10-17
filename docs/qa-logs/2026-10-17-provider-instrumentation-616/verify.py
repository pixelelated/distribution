#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
"""Verify stored and losslessly decoded publication artifacts, without runtime."""
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def local(name):
    path = ROOT / name
    if path.is_symlink() or not path.resolve(strict=True).is_relative_to(ROOT):
        raise ValueError('nonlocal or symlinked artifact')
    return path


def main():
    count = 0
    for line in (ROOT / 'SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ', 1)
        if digest(local(name).read_bytes()) != expected:
            raise ValueError('stored artifact digest mismatch')
        count += 1
    decoded = excluded = 0
    for row in json.loads((ROOT / 'provenance.json').read_text())['entries']:
        if not row['included']:
            excluded += 1
            continue
        data = local(row['stored']).read_bytes()
        if digest(data) != row['stored_sha256']:
            raise ValueError('provenance stored digest mismatch')
        raw = gzip.decompress(data) if row['encoding'] == 'gzip' else data
        if len(raw) != row['original_bytes'] or digest(raw) != row['original_sha256']:
            raise ValueError('lossless original digest mismatch')
        if raw.startswith(b'\x7fELF'):
            raise ValueError('ELF payload must remain outside publication packet')
        decoded += 1
    if excluded != 2:
        raise ValueError('expected exactly two excluded ELF artifacts')
    print(json.dumps({'status': 'PASS', 'stored_files': count,
        'originals_verified': decoded, 'excluded_elf_artifacts': excluded,
        'scope': 'file hashes and lossless decoding only; no new runtime'}))


if __name__ == '__main__':
    main()
