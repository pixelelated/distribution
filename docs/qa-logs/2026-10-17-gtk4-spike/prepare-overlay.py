#!/usr/bin/env python3
"""Materialize an exact source-only overlay into a new empty staging directory."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    packet = Path(__file__).resolve().parent
    inputs = json.loads((packet / 'inputs.json').read_text())
    output = args.output.absolute()
    if output.exists() or not output.parent.is_dir():
        raise SystemExit('output must be a new directory under an existing allocated parent')
    patches = {}
    for name, expected in inputs['source_sha256'].items():
        if '/patches/' not in name:
            continue
        plain = gzip.decompress((packet / 'source-patches' / (Path(name).name + '.gz')).read_bytes())
        if hashlib.sha256(plain).hexdigest() != expected:
            raise SystemExit('patch bytes differ from bound product source')
        patches[Path(name).name] = plain
    output.mkdir(mode=0o700)
    shutil.copytree(packet / 'overlay/projects', output / 'projects')
    target = output / 'projects/ROCKNIX/packages/web/webkitgtk/patches'
    target.mkdir()
    for name, data in patches.items():
        (target / name).write_bytes(data)
    (output / 'packages').mkdir()
    print(json.dumps({'files': sum(1 for p in output.rglob('*') if p.is_file()),
                      'bytes': sum(p.stat().st_size for p in output.rglob('*') if p.is_file()),
                      'patches': len(patches), 'build_invoked': False}))


if __name__ == '__main__':
    main()
