#!/usr/bin/python3
"""Execute two sealed source packets in one disposable no-NIC VM; preserve failures."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tarfile
import time

BASE = Path('/tmp/pix-input/controls')
OUT = Path('/tmp/pix-output')


def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def write(p, data):
    with p.open('x') as f:
        json.dump(data, f, indent=2)
        f.write('\n')


def archive(root, destination):
    rows = []
    for path in sorted(root.rglob('*')):
        relative = str(path.relative_to(root))
        if path.is_symlink():
            rows.append({'path': relative, 'link': os.readlink(path)})
        elif path.is_file():
            rows.append({'path': relative, 'bytes': path.stat().st_size, 'sha256': sha(path)})
    assert len(rows) < 4096
    assert sum(r.get('bytes', 0) for r in rows) < 64 * 1024**2
    with tarfile.open(destination, 'x:gz') as tar:
        for row in rows:
            tar.add(root / row['path'], arcname=row['path'], recursive=False)
    with tarfile.open(destination) as tar:
        assert len(tar.getmembers()) == len(rows)
        for row in rows:
            member = tar.getmember(row['path'])
            if 'link' in row:
                assert member.issym() and member.linkname == row['link']
            else:
                data = tar.extractfile(member).read()
                assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
    return rows


def main():
    assert sorted(p.name for p in Path('/sys/class/net').iterdir()) == ['lo']
    assert (OUT / 'lost+found').is_dir()
    result = {'rc': 1, 'commands': [], 'started': time.time(), 'no_network': True}
    write(OUT / 'boot.json', {'os_release': Path('/etc/os-release').read_text(),
                              'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip()})
    try:
        for name, script, arg, scratch, seconds in [
            ('dolphin', BASE / 'dolphin/fixtures/probe.py', '--output', Path('/run/pix594-session-01'), 75),
            ('steam', BASE / 'steam/probe.py', '--out', Path('/run/pix595-isolation-01'), 75),
        ]:
            row = {'name': name, 'argv': ['/usr/bin/python3', '-I', '-S', '-B', str(script), arg, str(scratch)],
                   'timeout_seconds': seconds, 'original_returncode': None, 'timed_out': False}
            result['commands'].append(row)
            case = OUT / name
            case.mkdir()
            try:
                with (case / 'stdout').open('xb') as out, (case / 'stderr').open('xb') as err:
                    child = subprocess.Popen(row['argv'], stdout=out, stderr=err, start_new_session=True)
                    row['pid'] = child.pid
                    try:
                        row['original_returncode'] = child.wait(timeout=seconds)
                    except subprocess.TimeoutExpired:
                        row['timed_out'] = True
                        os.killpg(child.pid, signal.SIGKILL)
                        row['original_returncode'] = child.wait(timeout=3)
            finally:
                write(case / 'command.json', row)
                if scratch.exists():
                    write(case / 'archive-members.json', archive(scratch, case / 'originals.tar.gz'))
                    for file in ['result.json', 'bindings.json']:
                        if (scratch / file).is_file():
                            shutil.copy2(scratch / file, case / file)
            assert row['original_returncode'] == 0 and not row['timed_out'], name
        result['rc'] = 0
    except BaseException as error:
        result['error'] = type(error).__name__ + ': ' + str(error)
    finally:
        result['ended'] = time.time()
        write(OUT / 'result.json', result)
        rows = [{'path': str(p.relative_to(OUT)), 'bytes': p.stat().st_size, 'sha256': sha(p)}
                for p in sorted(OUT.rglob('*')) if p.is_file()]
        assert not any(p.is_symlink() for p in OUT.rglob('*'))
        assert len(rows) <= 4096 and sum(x['bytes'] for x in rows) <= 128 * 1024**2
        write(OUT / 'guest-export-manifest.json', rows)
        os.sync()
    return result['rc']


if __name__ == '__main__':
    raise SystemExit(main())
