#!/usr/bin/env python3
"""One exact metadata helper in the existing offline guest; preserve original exits."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import platform
import runpy
import signal
import socket
import stat
import subprocess
import sys
import tarfile
import time

INPUT = Path('/tmp/pix-input')
OUTPUT = Path('/tmp/pix-output')
STAGE = OUTPUT / 'metadata'
MAX_RECORDS = 16 * 1024**2


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2); stream.write('\n')


def expired(signum, frame):
    raise TimeoutError('Metadata stage deadline or termination')


def tools_state(binding):
    rows = {}
    for name, expected in binding['installed_dependencies'].items():
        path = Path(name); resolved = path.resolve(strict=True); info = resolved.stat()
        rows[name] = {'resolved': str(resolved), 'sha256': sha(resolved),
                      'bytes': info.st_size, 'mode': stat.S_IMODE(info.st_mode),
                      'symlink': str(path.readlink()) if path.is_symlink() else None}
        assert rows[name] == expected, 'Installed dependency changed: ' + name
    return rows


def archive_control(source):
    """Retain helper records and synthetic link identities without dereferencing."""
    rows = []; total = 0
    for path in sorted(source.rglob('*')):
        info = path.lstat(); name = str(path.relative_to(source))
        if stat.S_ISDIR(info.st_mode):
            continue
        assert stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode)
        row = {'path': name, 'mode': stat.S_IMODE(info.st_mode)}
        if stat.S_ISLNK(info.st_mode):
            target = os.readlink(path)
            assert not Path(target).is_absolute() and '..' not in Path(target).parts
            row.update(kind='symlink', target=target)
        else:
            total += info.st_size
            assert info.st_size <= 2 * 1024**2 and total <= MAX_RECORDS // 2
            row.update(kind='file', bytes=info.st_size, sha256=sha(path))
        rows.append(row)
    save(STAGE / 'control-members.json', rows)
    archive_path = STAGE / 'control-records.tar.gz'
    with tarfile.open(archive_path, 'x:gz', dereference=False) as archive:
        for row in rows:
            archive.add(source / row['path'], arcname=row['path'], recursive=False)
    with tarfile.open(archive_path, 'r:gz') as archive:
        members = archive.getmembers()
        assert [member.name for member in members] == [row['path'] for row in rows]
        for member, row in zip(members, rows):
            assert member.mode == row['mode']
            if row['kind'] == 'symlink':
                assert member.issym() and member.linkname == row['target']
            else:
                assert member.isfile()
                data = archive.extractfile(member).read()
                assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
                assert sha(source / row['path']) == row['sha256']
    return {'members': len(rows), 'original_regular_bytes': total,
            'archive_sha256': sha(archive_path)}


def main():
    STAGE.mkdir()
    started = time.monotonic()
    result = {'status': 'FAIL', 'restored': False, 'original_helper_exit': None,
              'scope': 'Installed guest curl/Bash; exact source function only; no installed/native Steam claim'}
    proc = None; utilities = None; before = None; dependency_before = None
    signal.signal(signal.SIGALRM, expired)
    signal.signal(signal.SIGTERM, expired)
    signal.signal(signal.SIGINT, expired)
    signal.alarm(135)  # Includes the unchanged helper's110s work+10s cleanup.
    try:
        assert sys.flags.optimize == 0 and os.geteuid() == 0 and platform.machine() == 'x86_64'
        assert Path('/sys/class/dmi/id/sys_vendor').read_text().strip() == 'QEMU'
        family = json.loads((INPUT / 'family.json').read_text()); binding = family['metadata']
        fields = dict(line.split('=', 1) for line in Path('/etc/os-release').read_text().splitlines() if '=' in line)
        assert fields['BUILD_ID'].strip('"') == family['source_commit']
        assert fields['HW_DEVICE'].strip('"') == 'GENERIC_X64'
        assert sorted(name for _, name in socket.if_nameindex()) == ['lo']
        assert sorted(path.name for path in Path('/sys/class/net').iterdir()) == ['lo']
        save(STAGE / 'guest-identity.json', {'build_id': fields['BUILD_ID'], 'device': fields['HW_DEVICE'],
             'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip(), 'interfaces': ['lo']})
        assert sha(INPUT / 'guest-stage.py') == binding['original_guest_stage_sha256']
        assert sha(INPUT / binding['helper']) == binding['helper_sha256']
        assert sha(INPUT / binding['candidate_source']) == binding['candidate_source_sha256']
        assert sha(INPUT / family['installer_path']) == family['installer_sha256'] == binding['frozen_installer_sha256']
        # Only the unchanged wrapper's utility definitions load; main/fixture never run here.
        utilities = runpy.run_path(str(INPUT / 'guest-stage.py'), run_name='pix582_existing_stage_utilities')
        assert family['cases'] == list(utilities['CASES'])
        assert not utilities['children']()
        assert not (OUTPUT / 'steam').exists(), 'Metadata must precede the unchanged14'
        assert ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) == 0
        before = utilities['parent_state'](); save(STAGE / 'parent-before.json', before)
        dependency_before = tools_state(binding); save(STAGE / 'tools-before.json', dependency_before)
        assert os.statvfs(OUTPUT).f_bavail * os.statvfs(OUTPUT).f_frsize >= MAX_RECORDS
        version = subprocess.run(['/usr/bin/bash', '--version'], capture_output=True, timeout=3)
        (STAGE / 'bash-version.stdout').write_bytes(version.stdout)
        (STAGE / 'bash-version.stderr').write_bytes(version.stderr)
        save(STAGE / 'bash-version-result.json', {'original_exit': version.returncode})
        assert version.returncode == 0
        argv = ['python3', '-I', '-S', '-B', str(INPUT / binding['helper']),
                '--source', str(INPUT / binding['candidate_source']),
                '--baseline-source', str(INPUT / family['installer_path']),
                '--curl', '/usr/bin/curl', '--bash', '/usr/bin/bash',
                '--scope', 'installed-vm-curl', '--out', str(STAGE / 'control')]
        env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'LC_ALL': 'C', 'LANG': 'C'}
        save(STAGE / 'command.json', {'argv': argv, 'environment': env})
        with (STAGE / 'stdout').open('xb') as stdout, (STAGE / 'stderr').open('xb') as stderr:
            proc = subprocess.Popen(argv, env=env, stdin=subprocess.DEVNULL,
                                    stdout=stdout, stderr=stderr, start_new_session=True)
            save(STAGE / 'helper-process.json', {'pid': proc.pid,
                 'stat': Path('/proc', str(proc.pid), 'stat').read_text()})
            deadline = time.monotonic() + 125
            while proc.poll() is None:
                assert time.monotonic() < deadline, 'Original helper did not finish within its envelope'
                assert stdout.tell() <= 2 * 1024**2 and stderr.tell() <= 2 * 1024**2
                time.sleep(0.1)
            result['original_helper_exit'] = proc.returncode
        save(STAGE / 'original-result.json', {'helper_exit': proc.returncode})
        observed = json.loads((STAGE / 'control/result.json').read_text())
        result['helper_status'] = observed['status']
        assert proc.returncode == 0 and observed['status'] == 'PASS' and observed['passed'] is True
        assert observed['source_sha256'] == binding['candidate_source_sha256']
        assert observed['baseline']['source_sha256'] == family['installer_sha256']
        assert observed['baseline']['executed'] is False and observed['scope'] == 'installed-vm-curl'
        assert observed['curl_sha256'] == dependency_before['/usr/bin/curl']['sha256']
        assert observed['bash'] == dependency_before['/usr/bin/bash']['resolved']
        assert [row['path'] for row in observed['requests']] == ['/normal-cachyos', '/normal-ge', '/oversize', '/stall']
        assert not observed['cleanup'] and not observed['signals'] and observed['old_families_equal']
        assert observed['handler_threads_stopped'] and observed['server_thread_stopped']
        assert not utilities['children']()
        assert tools_state(binding) == dependency_before and utilities['parent_state']() == before
        save(STAGE / 'tools-after.json', tools_state(binding))
        save(STAGE / 'parent-after.json', utilities['parent_state']())
        result.update(status='PASS', restored=True)
    except BaseException as error:
        result['error'] = repr(error)
    finally:
        signal.alarm(10)  # At most145s including failure cleanup; host serial ceiling150s.
        try:
            if proc is not None and proc.poll() is None:
                result.update(status='FAIL', restored=False, failure_intervention=True)
                os.killpg(proc.pid, signal.SIGTERM)
                try:
                    proc.wait(timeout=6)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL); proc.wait(timeout=1)
                result['original_helper_exit'] = proc.returncode
            if utilities is not None:
                result['remaining_descendants'] = utilities['children']()
                if result['remaining_descendants']:
                    result.update(status='FAIL', restored=False)
            control = STAGE / 'control'
            if control.is_dir() and not result.get('remaining_descendants'):
                result['archive'] = archive_control(control)
        except BaseException as error:
            result.update(status='FAIL', restored=False, preservation_error=repr(error))
        result['elapsed_seconds'] = time.monotonic() - started
        save(STAGE / 'stage-result.json', result)
        # Archive includes helper output links. Never flatten them or follow a fixture link.
        rows = [{'path': 'metadata/' + path.name, 'bytes': path.stat().st_size, 'sha256': sha(path)}
                for path in sorted(STAGE.iterdir()) if path.is_file() and not path.is_symlink()]
        assert sum(row['bytes'] for row in rows) <= MAX_RECORDS
        save(OUTPUT / 'metadata-export-manifest.json', rows)
        subprocess.run(['sync'], check=True, timeout=2)
        signal.alarm(0)
        print('PIX_METADATA_STAGE_RESULT:' + json.dumps({key: result[key] for key in
              ('status', 'restored', 'original_helper_exit')}), flush=True)
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
