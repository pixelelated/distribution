#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""Materialize only the small, accepted #567 source inputs. Never run them."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    inputs = json.loads(Path(__file__).with_name('source.json').read_text())['accepted_inputs']
    # Read and verify everything before creating an output directory. Each object
    # is an explicit immutable git path; no archive expansion or source execution.
    staged = {}
    for row in inputs:
        data = subprocess.run(
            ['git', '-C', str(args.repo.resolve(strict=True)), 'show',
             row['commit'] + ':' + row['path']],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10,
        ).stdout
        if len(data) > 131072 or hashlib.sha256(data).hexdigest() != row['sha256']:
            raise RuntimeError('source identity or size differs: ' + row['name'])
        name = Path(row['name'])
        if name.is_absolute() or '..' in name.parts or name.as_posix() in staged:
            raise RuntimeError('invalid source member')
        staged[name.as_posix()] = data
    if sum(map(len, staged.values())) > 262144:
        raise RuntimeError('source packet exceeds 256 KiB')
    output = args.output.absolute()
    output.mkdir(mode=0o700)  # Refuse any existing path, including a symlink.
    for name, data in staged.items():
        destination = output / name
        destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        with destination.open('xb') as stream:
            stream.write(data)
        destination.chmod(0o600)
    receipt = {'source_materialized_only': True, 'runtime_run': False,
               'installed_topup_adapter_present': False,
               'files': {name: hashlib.sha256(data).hexdigest()
                         for name, data in staged.items()}}
    (output / 'SOURCE-ONLY.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'source_materialized_only': True, 'runtime_run': False,
                      'files': len(staged), 'bytes': sum(map(len, staged.values()))}))


if __name__ == '__main__':
    main()
