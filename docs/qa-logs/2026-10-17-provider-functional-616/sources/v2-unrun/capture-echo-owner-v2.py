#!/usr/bin/env python3
"""UNRUN: capture an exact fresh local server identity immediately after ready."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import time

ROOT = Path('/storage/qa616-provider')
SERVER_SHA = '640bf444f7a44ed55644519c5749d48df6ed63585c36c65018fc9a91e52bd4af'
PAGE_SHA = '5291483aee24ee0f620bde5e807a09a55735139ef9234ccde609c036573a6c31'

def main(echo):
    os.umask(0o077)
    assert os.geteuid() == 0 and os.uname().machine == 'x86_64'
    assert echo.parent == ROOT and re.fullmatch(r'echo-light[0-9]+', echo.name) and not echo.is_symlink()
    case = json.loads(Path('/run/qa616-provider/current.json').read_text())
    assert case['provider'] == 'light' and case['ua'] == 'default' and case['observer'] == 'off'
    ready_path = echo / 'ready.json'
    metadata = ready_path.lstat()
    assert stat.S_ISREG(metadata.st_mode) and metadata.st_uid == 0 and not metadata.st_mode & 0o022
    assert metadata.st_size < 4096 and 0 <= time.time() - metadata.st_mtime < 5
    raw = ready_path.read_bytes()
    ready = json.loads(raw)
    assert ready['port'] == 18761 and ready['page_sha256'] == PAGE_SHA and ready['max_seconds'] == 240
    process = Path('/proc', str(ready['pid']))
    fields = (process / 'stat').read_text().rsplit(')', 1)[1].split()
    assert fields[0] != 'Z'
    start = int(fields[19])
    assert [x.decode() for x in (process / 'cmdline').read_bytes().split(b'\0') if x] == [
        '/usr/bin/python3', '-I', '-B', str(ROOT / 'calibration-server.py'), '--output', str(echo)]
    assert hashlib.sha256((ROOT / 'calibration-server.py').read_bytes()).hexdigest() == SERVER_SHA
    assert hashlib.sha256((ROOT / 'calibration.html').read_bytes()).hexdigest() == PAGE_SHA
    assert int((process / 'stat').read_text().rsplit(')', 1)[1].split()[19]) == start
    assert ready_path.read_bytes() == raw
    owner = {'case': case, 'pid': ready['pid'], 'start': start,
             'ready_sha256': hashlib.sha256(raw).hexdigest()}
    with (echo / 'owner.json').open('x') as handle:
        json.dump(owner, handle)
        handle.write('\n')
    print(json.dumps({'status': 'IDENTITY_RECORDED', 'pid': ready['pid'], 'start': start}))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--echo', required=True, type=Path)
    try:
        main(parser.parse_args().echo)
    except Exception as error:
        print(json.dumps({'status': 'REFUSED', 'error_class': type(error).__name__}))
        raise SystemExit(1)
