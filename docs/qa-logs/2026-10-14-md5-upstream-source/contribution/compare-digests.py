#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check retained before/after command results; never execute a compiler or target."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    out = args.output
    for label in ('before-build', 'after-build', 'before', 'after'):
        for suffix in ('stdout', 'stderr', 'rc'):
            if (out / (label + '.' + suffix)).stat().st_size > 65536:
                raise RuntimeError('oversized output: ' + label)
    rc = {label:int((out / (label + '.rc')).read_text())
          for label in ('before-build', 'after-build', 'before', 'after')}
    before_error = (out / 'before.stderr').read_text()
    if rc != {'before-build':0, 'after-build':0, 'before':1, 'after':0}:
        raise RuntimeError('unexpected original/timeout-wrapper exit: ' + repr(rc))
    if (before_error.count('runtime error: load of misaligned address') != 1
            or str(out / 'before.c') + ':' not in before_error
            or 'AddressSanitizer' in before_error):
        raise RuntimeError('before did not reproduce the expected MD5 alignment diagnostic')
    if (out / 'after.stderr').read_bytes():
        raise RuntimeError('patched target emitted sanitizer stderr')
    data = bytes((i * 13 + 7) & 255 for i in range(1024))
    lengths = (0, 1, 55, 56, 63, 64, 65, 127, 128, 129, 1024)
    expected = ''.join(f'{offset} {length} {split} '
                       + hashlib.md5(data[:length], usedforsecurity=False).hexdigest() + '\n'
                       for offset in range(8) for length in lengths for split in range(3))
    if (out / 'after.stdout').read_text() != expected:
        raise RuntimeError('missing, extra, reordered, or incorrect digest row')
    result = {'status':'PASS', 'independent_digest_rows':264,
              'before':'expected alignment UB, original exit1 retained',
              'after':'exit0 and empty sanitizer stderr', 'command_exits':rc}
    with (out / 'comparison.json').open('x') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
