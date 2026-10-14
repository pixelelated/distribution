#!/usr/bin/env python3
"""UNRUN full-file SHA256 only, under the download owner's remaining deadline."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', required=True, type=Path)
    args = parser.parse_args()
    result = {'status': 'FAIL', 'evidence': 'Size/SHA256 only; no archive parsing, decoding or execution'}
    try:
        selected = json.loads((HERE / 'bound/selected.json').read_bytes())
        expected = 110373661
        if selected['size'] != expected:
            raise ValueError('Advertised size changed')
        fd = os.open(args.archive, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd, 'rb') as stream:
            before = os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size != expected:
                raise ValueError('Archive must be a single-link regular file of exact advertised size')
            checksum, count = hashlib.sha256(), 0
            while count <= expected:
                raw = stream.read(min(1024**2, expected + 1 - count))
                if not raw:
                    break
                checksum.update(raw); count += len(raw)
            after = os.fstat(stream.fileno())
            result.update(bytes=count, sha256=checksum.hexdigest())
            if count != expected or checksum.hexdigest() != selected['sha256_from_manifest']:
                raise ValueError('Exact advertised archive length/SHA256 mismatch')
            if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                raise ValueError('Archive changed while hashing')
            result['status'] = 'PASS'
    except BaseException as error:
        result['error'] = repr(error)
    print(json.dumps(result))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
