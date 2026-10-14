#!/usr/bin/env python3
"""UNRUN text adapter only: emits a proposed syslinux file, never changes a disk/boot."""
import argparse
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    binding = json.loads((HERE / 'compatibility.json').read_text())['boot_config']
    before = (HERE / 'boot/syslinux.before.cfg').read_bytes()
    after = (HERE / 'boot/syslinux.after.cfg').read_bytes()
    sha = lambda raw: hashlib.sha256(raw).hexdigest()
    assert sha(before) == binding['before_sha256'] and sha(after) == binding['after_sha256']
    assert after == before.rstrip(b'\n') + b' systemd.unified_cgroup_hierarchy=1\n'
    assert args.input.resolve(strict=True) == args.input.absolute() and args.input.is_file()
    assert args.input.stat().st_size == len(before) and args.input.read_bytes() == before
    assert args.output.parent.resolve(strict=True) == args.output.absolute().parent
    assert not args.output.exists() and not args.output.is_symlink()
    assert not args.output.with_suffix('.receipt.json').exists()
    with args.output.open('xb') as f:
        f.write(after); f.flush(); os.fsync(f.fileno())
    receipt = {'status': 'TEXT_PREPARED_ONLY', 'input': str(args.input), 'output': str(args.output),
               'before_sha256': sha(before), 'after_sha256': sha(after),
               'parameter': binding['parameter'], 'boot_or_disk_changed': False}
    with args.output.with_suffix('.receipt.json').open('x') as f:
        json.dump(receipt, f, indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())


if __name__ == '__main__':
    main()
