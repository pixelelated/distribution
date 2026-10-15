"""UNRUN fixture logging only. Never changes transfer resources or original exits."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import time

PROCESS_BYTES = 4096
TOTAL_BYTES = 2 * 1024**2
MAX_PROCESSES = 512
_writer = None


def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def event(row):
    global _writer
    pid = os.getpid()
    row.update(pid=pid, monotonic_ns=time.monotonic_ns())
    raw = (json.dumps(row, sort_keys=True) + '\n').encode()
    need(len(raw) <= PROCESS_BYTES, 'Boundary event exceeds per-process cap')
    directory = os.open('/qa/boundary-events', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    fd = None
    try:
        if _writer is None:
            # A fresh, exclusive regular file per interpreter. No inherited shared
            # offset can collide with the actual transfer RLIMIT_FSIZE.
            need(len(os.listdir(directory)) < MAX_PROCESSES, 'Too many boundary event processes')
            name = str(pid) + '-' + str(row['monotonic_ns']) + '.ndjson'
            fd = os.open(name, os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                         0o600, dir_fd=directory)
            info = os.fstat(fd)
            _writer = (pid, name, info.st_dev, info.st_ino)
        else:
            need(_writer[0] == pid, 'Boundary writer inherited across fork')
            fd = os.open(_writer[1], os.O_WRONLY | os.O_APPEND | os.O_NOFOLLOW, dir_fd=directory)
        info = os.fstat(fd)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1
             and (info.st_dev, info.st_ino) == _writer[2:], 'Boundary event file identity changed')
        need(info.st_size + len(raw) <= PROCESS_BYTES, 'Boundary process log exceeds cap')
        need(os.write(fd, raw) == len(raw), 'Short boundary event write')
        os.fsync(fd)
    finally:
        if fd is not None:
            os.close(fd)
        os.close(directory)


def read_bounded(path, cap):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and before.st_size <= cap, 'Unexpected event file type/size: ' + str(path))
        chunks = []; size = 0
        while True:
            block = os.read(fd, min(65536, cap + 1 - size))
            if not block:
                break
            chunks.append(block); size += len(block)
            need(size <= cap, 'Event read exceeds cap')
        after = os.fstat(fd)
        identity = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        need(identity(before) == identity(after) and size == before.st_size,
             'Event file changed after trace/quiescence: ' + str(path))
        return b''.join(chunks)
    finally:
        os.close(fd)


def collect(qa, output):
    # Original trace results and outer quiescence are checked by the caller first.
    # Keep both streams intact; publish a separate, byte-preserving ordered copy.
    directory = qa / 'boundary-events'
    need(directory.is_dir() and not directory.is_symlink(), 'Aliased boundary event directory')
    files = []
    with os.scandir(directory) as entries:
        for entry in entries:
            need(len(files) < MAX_PROCESSES and re.fullmatch(r'[1-9][0-9]*-[1-9][0-9]*\.ndjson', entry.name),
                 'Unexpected/excess boundary event file')
            need(entry.is_file(follow_symlinks=False), 'Nonregular boundary event file')
            files.append(Path(entry.path))
    rows = []; inputs = []; total = 0
    for path in [qa / 'events.ndjson', *sorted(files)]:
        boundary = path.parent == directory
        raw = read_bounded(path, PROCESS_BYTES if boundary else TOTAL_BYTES)
        total += len(raw)
        need(total <= TOTAL_BYTES and (not raw or raw.endswith(b'\n')), 'Incomplete/oversized event stream')
        need(not boundary or raw, 'Empty boundary event stream')
        inputs.append({'path': str(path.relative_to(qa)), 'bytes': len(raw),
                       'sha256': hashlib.sha256(raw).hexdigest()})
        for number, line in enumerate(raw.splitlines(keepends=True), 1):
            need(len(line) <= PROCESS_BYTES, 'Oversized event row')
            row = json.loads(line)
            need(isinstance(row, dict) and type(row.get('pid')) is int and row['pid'] > 0
                 and type(row.get('monotonic_ns')) is int and row['monotonic_ns'] > 0, 'Invalid event identity/time')
            if boundary:
                need(row['pid'] == int(path.name.split('-')[0]), 'Boundary event PID differs from its stream')
            rows.append((row['monotonic_ns'], row['pid'], str(path.relative_to(qa)), number, line, row))
    rows.sort(key=lambda r: r[:4])
    raw = b''.join(r[4] for r in rows)
    with output.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    receipt = {'status': 'COLLECTED', 'ordering': 'original monotonic_ns, pid, path, line; no new timestamps',
               'originals_unchanged': True, 'inputs': inputs, 'events': len(rows), 'bytes': len(raw),
               'sha256': hashlib.sha256(raw).hexdigest(), 'per_boundary_process_cap': PROCESS_BYTES,
               'aggregate_cap': TOTAL_BYTES, 'scope': 'fixture events; original caller/trace receipts are separate'}
    with output.with_suffix('.json').open('x') as f:
        json.dump(receipt, f, indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
    return [r[5] for r in rows]
