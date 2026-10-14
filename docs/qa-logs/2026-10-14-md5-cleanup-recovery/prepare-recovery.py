#!/usr/bin/env python3
"""UNRUN. Read one sealed failed owner; create a NEW bounded public runtime export."""
import argparse
import json
from pathlib import Path
import runpy
import shutil

HERE = Path(__file__).resolve().parent
R = runpy.run_path(str(HERE / 'recovery.py'))
require, verify = R['require'], R['verify']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--owner', type=Path, required=True)
    parser.add_argument('--packet', type=Path, required=True, help='immutable0962 original packet')
    parser.add_argument('--output', type=Path, required=True, help='NEW export, never original owner')
    args = parser.parse_args()
    known = R['packet']()
    require(str(args.owner) == known['owner'] and args.owner.resolve() == args.owner,
            'only the exact failed owner is eligible')
    verify(args.packet, known['original_packet'])
    binding = json.loads((args.packet / 'input-bindings.json').read_text())
    sources = {'candidate':dict(binding['candidate']['files']),
               'baseline-repaired':dict(binding['pristine_baseline']['files']),
               'fixture':binding['sealed_fixture']['files']}
    sources['candidate'][binding['md5_driver']['path']] = binding['md5_driver']['sha256']
    sources['baseline-repaired'][binding['baseline_repair']['path']] = binding['baseline_repair']['after']
    for mode, hashes in sources.items():
        root = args.owner / 'sources' / mode
        verify(root, hashes)
        require({str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()} == set(hashes),
                'source snapshot closure changed')
        require(len(hashes) == known['source_snapshot_counts'][mode], 'source count differs')
    output = args.output
    require(output.is_absolute() and output.resolve() == output and not output.exists()
            and output.parent.is_dir() and output.is_relative_to(Path('/workspace/tmp'))
            and not output.is_relative_to(args.owner), 'new export outside original owner required')
    members = {name:args.owner / name for name in known['evidence']}
    members['evidence/watcher-build.rc'] = Path(known['watcher_build_rc'])
    members.update({name:args.owner / name for name in known['artifacts']})
    members.update({'packet/' + name:args.packet / name for name in known['original_packet']})
    recovery_members = [line.split('  ',1)[1] for line in (HERE/'SHA256SUMS').read_text().splitlines()] + ['SHA256SUMS']
    members.update({'recovery/' + name:HERE/name for name in recovery_members})
    expected = dict(known['evidence'], **known['artifacts'])
    for name, digest in expected.items():
        require(R['sha'](members[name]) == digest, 'original evidence/artifact changed: ' + name)
    require(sum(p.stat().st_size for p in members.values()) <= 40 * 1024**2,
            'export exceeds40MiB; no build/cache copy allowed')
    output.mkdir(mode=0o700)
    for name, source in members.items():
        dest = output / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        with source.open('rb') as src, dest.open('xb') as target:
            shutil.copyfileobj(src, target)
        if name.startswith('artifacts/') and '/lib/' not in name:
            dest.chmod(0o755)
    receipt = R['validate'](output)
    with (output / 'recovery-acceptance.json').open('x') as stream:
        stream.write(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status':'ACCEPTED_FOR_RUNTIME_ONLY','output':str(output),
                      'original_outer_exit':1,'runtime':'UNRUN'}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
