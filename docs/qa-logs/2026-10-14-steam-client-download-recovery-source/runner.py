#!/usr/bin/env python3
"""UNRUN shared source-sealed process supervision; no command at import."""
import argparse
import ctypes
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import selectors
import shutil
import signal
import stat
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
MARKER = b'\nPIX_INTAKE_CURL_JSON\n'
ACTIVE = None


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def seal():
    require(sys.platform == 'linux' and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, 'Use Linux python3 -I -S -B')
    require(all(not path.is_symlink() for path in HERE.rglob('*')), 'Packet contains a symlink')
    names = set()
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ', 1)
        path = HERE / name
        require(name not in names and not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe/duplicate packet name')
        require(path.resolve(strict=True) == path and path.is_file() and sha(path) == expected, 'Changed/aliased packet file: ' + name)
        names.add(name)
    require(names == {str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and p != HERE / 'SHA256SUMS'}, 'Unsealed packet file')
    return json.loads((HERE / 'source.json').read_bytes())


def process_group(group):
    rows = []
    for path in Path('/proc').iterdir():
        if not path.name.isdecimal():
            continue
        try:
            fields = (path / 'stat').read_text().rsplit(')', 1)[1].split()
            if int(fields[2]) == group:
                rows.append({'pid': int(path.name), 'state': fields[0], 'start_ticks': int(fields[19])})
        except (FileNotFoundError, ProcessLookupError, PermissionError):
            continue
    return rows


def stop_signal(signum, _frame):
    raise InterruptedError('Owner signal ' + str(signum))


def run(argv, output, label, seconds, limits, pass_fds=(), file_cap=None):
    """One child, bounded logs/deadline, parent-death kill and actual original status."""
    global ACTIVE
    parent = os.getpid()
    libc = ctypes.CDLL(None, use_errno=True)
    started = time.monotonic()
    result = {'argv': argv, 'original_exit': None, 'intervention': None}
    selector = selectors.DefaultSelector()
    handles = []
    def child_limits():
        if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0 or os.getppid() != parent:
            os._exit(125)
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        resource.setrlimit(resource.RLIMIT_AS, (limits['worker_address_space_bytes'],) * 2)
        resource.setrlimit(resource.RLIMIT_CPU, (math.ceil(seconds), math.ceil(seconds) + 1))
        resource.setrlimit(resource.RLIMIT_FSIZE, (file_cap or 4 * 1024**2,) * 2)
    process = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               env={'PATH': '/usr/bin:/bin', 'LANG': 'C', 'TMPDIR': str(output)},
                               start_new_session=True, preexec_fn=child_limits, pass_fds=pass_fds)
    ACTIVE = process
    try:
        for stream, name in ((process.stdout, 'stdout'), (process.stderr, 'stderr')):
            os.set_blocking(stream.fileno(), False)
            target = (output / (label + '.' + name)).open('xb')
            handles.append(target)
            selector.register(stream, selectors.EVENT_READ, {'target': target, 'bytes': 0})
        while selector.get_map() or process.poll() is None:
            require(time.monotonic() - started < seconds, label + ' wall deadline reached')
            for key, _ in selector.select(0.05):
                raw = os.read(key.fileobj.fileno(), 65536)
                if not raw:
                    selector.unregister(key.fileobj)
                    continue
                remaining = limits['log_bytes_each'] - key.data['bytes']
                key.data['target'].write(raw[:remaining]); key.data['target'].flush()
                key.data['bytes'] += len(raw)
                require(key.data['bytes'] <= limits['log_bytes_each'], label + ' log exceeds bound')
        result['original_exit'] = process.wait(timeout=0)
    except BaseException as error:
        result['intervention'] = repr(error)
    finally:
        previous_handlers = {sig: signal.signal(sig, signal.SIG_IGN) for sig in (signal.SIGTERM, signal.SIGINT)}
        cleanup_started = time.monotonic()
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
        try:
            result['original_exit'] = process.wait(timeout=limits['cleanup_seconds'])
        except subprocess.TimeoutExpired:
            result['cleanup_timeout'] = True
        # No descendant is intentionally launched. Reap adopted unexpected children;
        # identify before signalling with a pidfd, never a name/pattern or reused PID.
        for row in process_group(process.pid):
            try:
                fd = os.pidfd_open(row['pid'])
                now = next((r for r in process_group(process.pid) if r['pid'] == row['pid']), None)
                if now and now['start_ticks'] == row['start_ticks']:
                    signal.pidfd_send_signal(fd, signal.SIGKILL)
                os.close(fd)
            except ProcessLookupError:
                pass
        while time.monotonic() - cleanup_started < limits['cleanup_seconds']:
            try:
                while True:
                    pid, status = os.waitpid(-1, os.WNOHANG)
                    if not pid:
                        break
                    result.setdefault('adopted_exits', []).append({'pid': pid, 'wait_status': status, 'exit': os.waitstatus_to_exitcode(status)})
            except ChildProcessError:
                pass
            if not process_group(process.pid):
                break
            time.sleep(0.02)
        result['remaining_process_group'] = process_group(process.pid)
        result['cleanup_seconds'] = time.monotonic() - cleanup_started
        result['elapsed_seconds'] = time.monotonic() - started
        ACTIVE = None
        selector.close()
        process.stdout.close(); process.stderr.close()
        for handle in handles:
            handle.close()
        (output / (label + '.result.json')).write_text(json.dumps(result, indent=2) + '\n')
        for sig, handler in previous_handlers.items():
            signal.signal(sig, handler)
    return result


def accepted(row):
    return row['original_exit'] == 0 and row['intervention'] is None and not row['remaining_process_group'] and not row.get('cleanup_timeout')
