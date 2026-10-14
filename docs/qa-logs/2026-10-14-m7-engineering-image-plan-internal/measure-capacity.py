#!/usr/bin/env python3
"""Future coordinator command: bounded roots, read-only full allocation measurement.

This performs directory scans. It was AST-checked but NOT run in the source lane.
Run under watch-build --record-only, with no active producer of these roots.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess

PARENT = Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20')
ROOT = 'build.pixelelated-GENERIC_X64.x86_64'
HEAD = '1a026648442321609b2288c2c9c06803817f9df2'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--perform-full-measurement', action='store_true', required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists()
    assert subprocess.check_output(['git', '-C', str(PARENT), 'rev-parse', 'HEAD'], text=True).strip() == HEAD
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    rows = []
    for path in [PARENT / ROOT, PARENT / 'target', Path('/workspace/cache/rocknix-sources')]:
        assert path.is_dir() and not path.is_symlink()
        print('Measuring allocated bytes: ' + str(path), flush=True)
        r = subprocess.run(['du', '-s', '-x', '--block-size=1', '--', str(path)],
                           capture_output=True, text=True, timeout=1800, check=True)
        rows.append({'path': str(path), 'allocated_bytes': int(r.stdout.split()[0])})
    s = os.statvfs('/workspace')
    result = {'schema': 1, 'utc_start': start,
              'utc_finish': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'parent_head': HEAD, 'measurements': rows,
              'available_bytes': s.f_bavail * s.f_frsize,
              'existing_allocations_already_excluded_from_available': True}
    with a.output.open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
