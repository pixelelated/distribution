#!/usr/bin/env python3
"""Bounded immutable-reference -> exclusive report publication. No job control.

This function block is embedded byte-for-byte in the proposed terminal source.
The CLI is also the writer exercised by the preflight lifecycle probe.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import time

# BEGIN SHARED WRITER
def rw_identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def rw_require(value, reason):
    if not value:
        raise ValueError(reason)


def rw_close(fd, primary, secondary, stage):
    # Ownership is spent by the caller before this one attempt; never retry close.
    try:
        os.close(fd)
    except BaseException as error:
        if primary is None:
            primary = error
        elif len(secondary) < 16:
            secondary.append({'stage': stage, 'type': type(error).__name__,
                              'error': str(error)[:160]})
    return primary


def rw_parent(path, held, gate):
    # Walk components using pinned descriptors. A symlink in any component refuses.
    p = Path(path)
    rw_require(type(path) is str and len(path) <= 4096 and len(p.parts) <= 24 and
               p.is_absolute() and str(p) == path and
               '..' not in p.parts and p.name not in ('', '.', '..'), 'literal absolute path')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    held.append((fd, 'root-directory'))
    for component in p.parts[1:-1]:
        gate()
        fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW |
                     os.O_CLOEXEC, dir_fd=fd)
        held.append((fd, 'parent-directory'))
    s = os.fstat(fd)
    rw_require(stat.S_ISDIR(s.st_mode), 'parent is directory')
    return fd, p.name, s


def rw_publish(request, gate, secondary):
    """Read once, O_EXCL write, fsync, independently open/read back; compact receipt.

    Gate is the caller's ORIGINAL absolute deadline, including reserved time.
    All opened descriptors close once. Failed/partial output remains held.
    No exception including a close/diagnostic failure can replace an earlier error.
    """
    rw_require(type(request) is dict and set(request) == {
        'schema', 'source', 'destination', 'parent_identity', 'deadline_monotonic',
        'deadline_wall_ms'}, 'writer request fields')
    rw_require(request['schema'] == 'm7-exclusive-report-reference-v1', 'writer schema')
    src = request['source']
    rw_require(type(src) is dict and set(src) == {'path', 'bytes', 'sha256', 'identity'},
               'source reference fields')
    rw_require(type(src['bytes']) is int and 0 < src['bytes'] <= 16 * 1024**2,
               'source byte cap')
    rw_require(type(src['sha256']) is str and len(src['sha256']) == 64 and
               all(c in '0123456789abcdef' for c in src['sha256']), 'source digest')
    rw_require(type(src['identity']) is list and len(src['identity']) == 6 and
               all(type(x) is int for x in src['identity']), 'native source identity')
    rw_require(type(request['parent_identity']) is list and len(request['parent_identity']) == 2
               and all(type(x) is int for x in request['parent_identity']), 'parent identity')
    rw_require(type(request['deadline_monotonic']) in (int, float) and
               type(request['deadline_wall_ms']) is int, 'deadline types')
    rw_require(src['path'] != request['destination'], 'source cannot be destination')
    held = []
    primary = None
    receipt = None
    actual_read = 0

    def check():
        gate()
        rw_require(time.monotonic() < request['deadline_monotonic'] and
                   time.time_ns() // 1000000 < request['deadline_wall_ms'], 'writer expired')

    def read_exact(fd, expected):
        nonlocal actual_read
        parts = []
        remaining = expected
        while remaining:
            check()
            block = os.read(fd, min(65536, remaining))
            actual_read += len(block)
            rw_require(bool(block), 'short source/readback')
            parts.append(block)
            remaining -= len(block)
        check()
        extra = os.read(fd, 1)
        actual_read += len(extra)
        rw_require(not extra, 'source/readback grew')
        return b''.join(parts)

    try:
        check()
        sp, sn, _ = rw_parent(src['path'], held, check)
        source_fd = os.open(sn, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=sp)
        held.append((source_fd, 'source'))
        before = os.fstat(source_fd)
        rw_require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                   before.st_uid == os.geteuid() and stat.S_IMODE(before.st_mode) == 0o400,
                   'source must be owned single-link regular0400')
        rw_require(rw_identity(before) == src['identity'] ==
                   rw_identity(os.stat(sn, dir_fd=sp, follow_symlinks=False)) and
                   before.st_size == src['bytes'], 'source identity/size')
        data = read_exact(source_fd, src['bytes'])
        rw_require(hashlib.sha256(data).hexdigest() == src['sha256'], 'source digest mismatch')
        rw_require(rw_identity(before) == rw_identity(os.fstat(source_fd)) ==
                   rw_identity(os.stat(sn, dir_fd=sp, follow_symlinks=False)), 'source changed')
        dp, dn, ds = rw_parent(request['destination'], held, check)
        rw_require([ds.st_dev, ds.st_ino] == request['parent_identity'] and
                   ds.st_uid == os.geteuid() and stat.S_IMODE(ds.st_mode) == 0o700,
                   'destination parent identity/owner/mode')
        check()  # final no-write cutoff immediately before O_EXCL
        out = os.open(dn, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW |
                      os.O_CLOEXEC, 0o600, dir_fd=dp)
        held.append((out, 'output'))
        view = memoryview(data)
        while view:
            check()
            count = os.write(out, view[:65536])
            rw_require(count > 0, 'write made no progress')
            view = view[count:]
        os.fsync(out)
        check()
        written = os.fstat(out)
        rw_require(stat.S_ISREG(written.st_mode) and written.st_nlink == 1 and
                   written.st_uid == os.geteuid() and stat.S_IMODE(written.st_mode) == 0o600 and
                   written.st_size == src['bytes'], 'published file shape')
        # A separate nofollow open proves the path, not only the writing descriptor.
        back = os.open(dn, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=dp)
        held.append((back, 'readback'))
        rw_require(rw_identity(os.fstat(back)) == rw_identity(written), 'readback identity')
        observed = read_exact(back, src['bytes'])
        rw_require(observed == data and hashlib.sha256(observed).hexdigest() == src['sha256'],
                   'readback bytes/hash')
        rw_require(rw_identity(written) == rw_identity(os.fstat(back)) ==
                   rw_identity(os.stat(dn, dir_fd=dp, follow_symlinks=False)), 'readback drift')
        os.fsync(dp)
        check()
        # Rewalk after publication to detect detached/replaced ancestors.
        again, _, current_parent = rw_parent(request['destination'], held, check)
        rw_require([current_parent.st_dev, current_parent.st_ino] == request['parent_identity']
                   and rw_identity(os.stat(dn, dir_fd=again, follow_symlinks=False)) ==
                   rw_identity(written), 'destination detached')
        rw_require(rw_identity(os.fstat(source_fd)) == src['identity'] ==
                   rw_identity(os.stat(sn, dir_fd=sp, follow_symlinks=False)), 'source final drift')
        source_again, _, _ = rw_parent(src['path'], held, check)
        rw_require(rw_identity(os.stat(sn, dir_fd=source_again, follow_symlinks=False)) ==
                   src['identity'], 'source ancestors detached')
        receipt = dict(status='EXCLUSIVE_REPORT_READBACK', source=src,
                       output=dict(path=request['destination'], bytes=len(data), sha256=src['sha256']),
                       identity=rw_identity(written), read_bytes=actual_read, fsynced=True,
                       whole_lifecycle=False, namespace_verified=False)
    except BaseException as error:
        primary = error
    finally:
        while held:
            fd, label = held.pop()
            primary = rw_close(fd, primary, secondary, label)
    if primary is not None:
        raise primary
    check()  # includes successful descriptor teardown; no success after deadline
    return receipt
def rw_receive(request, gate, secondary):
    """One bounded raw-PTY/stdin submission, then the SAME exclusive writer.

    Request/READY are small argv/output. Full ASCII bytes plus one EOT travel only
    through write_stdin, once. Raw mode affects this newly allocated PTY only.
    Blocking I/O is bounded by the enclosing selected timeout, never by a reset.
    """
    rw_require(type(request) is dict and set(request) == {'schema', 'bytes', 'sha256',
        'spool', 'destination', 'parent_identity', 'deadline_monotonic',
        'deadline_wall_ms'}, 'receiver request fields')
    rw_require(request['schema'] == 'm7-exclusive-report-stdin-v1', 'receiver schema')
    n = request['bytes']
    rw_require(type(n) is int and 0 < n <= 16 * 1024**2, 'receiver byte cap')
    rw_require(type(request['sha256']) is str and len(request['sha256']) == 64 and
               all(c in '0123456789abcdef' for c in request['sha256']), 'receiver digest')
    rw_require(type(request['deadline_monotonic']) in (float, int) and
               type(request['deadline_wall_ms']) is int, 'receiver deadline types')
    held = []
    primary = None
    result = None
    attrs = None

    def check():
        gate()
        rw_require(time.monotonic() < request['deadline_monotonic'] and
                   time.time_ns() // 1000000 < request['deadline_wall_ms'], 'receiver expired')

    try:
        check()
        sp, name, st = rw_parent(request['spool'], held, check)
        rw_require(st.st_uid == os.geteuid() and stat.S_IMODE(st.st_mode) == 0o700,
                   'spool private owned parent')
        # Validate target parent before admitting data, but never create it.
        _, _, dp = rw_parent(request['destination'], held, check)
        rw_require([dp.st_dev, dp.st_ino] == request['parent_identity'] and
                   dp.st_uid == os.geteuid() and stat.S_IMODE(dp.st_mode) == 0o700,
                   'receiver destination parent')
        if os.isatty(0):
            import termios
            import tty
            attrs = termios.tcgetattr(0)
            tty.setraw(0, termios.TCSANOW)
        ready = dict(status='REPORT_STDIN_READY', bytes=n, sha256=request['sha256'],
                     deadline_monotonic=request['deadline_monotonic'])
        print(json.dumps(ready, separators=(',', ':')), flush=True)
        blocks = []
        remaining = n
        while remaining:
            check()
            b = os.read(0, min(65536, remaining))
            rw_require(bool(b), 'receiver short input')
            blocks.append(b)
            remaining -= len(b)
        check()
        rw_require(os.read(0, 1) == b'\x04', 'receiver missing EOT')
        data = b''.join(blocks)
        rw_require(data.isascii() and hashlib.sha256(data).hexdigest() == request['sha256'],
                   'receiver ASCII/hash mismatch')
        check()
        fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW |
                     os.O_CLOEXEC, 0o400, dir_fd=sp)
        held.append((fd, 'spool'))
        view = memoryview(data)
        while view:
            check()
            count = os.write(fd, view[:65536])
            rw_require(count > 0, 'spool write no progress')
            view = view[count:]
        os.fsync(fd)
        check()
        s = os.fstat(fd)
        rw_require(rw_identity(s) == rw_identity(os.stat(name, dir_fd=sp, follow_symlinks=False)),
                   'spool path drift')
        os.fsync(sp)
        source = dict(path=request['spool'], bytes=n, sha256=request['sha256'], identity=rw_identity(s))
        # Close spool descriptors before using it as an immutable input.
        while held:
            opened, label = held.pop()
            primary = rw_close(opened, primary, secondary, label)
        if primary is not None:
            raise primary
        result = rw_publish(dict(schema='m7-exclusive-report-reference-v1', source=source,
            destination=request['destination'], parent_identity=request['parent_identity'],
            deadline_monotonic=request['deadline_monotonic'],
            deadline_wall_ms=request['deadline_wall_ms']), check, secondary)
        result['stdin_bytes'] = n + 1
        result['transport_read_bytes'] = result['read_bytes'] + n + 1
    except BaseException as error:
        primary = error
    finally:
        while held:
            opened, label = held.pop()
            primary = rw_close(opened, primary, secondary, label)
        if attrs is not None:
            try:
                termios.tcsetattr(0, termios.TCSANOW, attrs)
            except BaseException as error:
                if primary is None:
                    primary = error
                elif len(secondary) < 16:
                    secondary.append(dict(stage='pty-restore', type=type(error).__name__))
    if primary is not None:
        raise primary
    check()
    return result
# END SHARED WRITER


def main():
    secondary = []
    try:
        receiving = len(sys.argv) == 3 and sys.argv[1] == '--receive'
        if (len(sys.argv) != 2 and not receiving) or len(sys.argv[-1].encode()) > 8192:
            raise ValueError('one bounded JSON request required')
        request = json.loads(sys.argv[-1])
        result = (rw_receive if receiving else rw_publish)(request, lambda: None, secondary)
        print(json.dumps(result, separators=(',', ':')), flush=True)
        if time.monotonic() >= request['deadline_monotonic']:
            raise ValueError('writer response publication late')
        return 0
    except BaseException as error:
        # Output failure never changes the operation's first error/status.
        record = dict(status='FAILED_OR_UNKNOWN', primary_type=type(error).__name__,
                      primary=str(error)[:256], secondary=secondary,
                      partial_outputs='HOLD_NO_RETRY_NO_ROLLBACK')
        try:
            print(json.dumps(record, separators=(',', ':')), file=sys.stderr, flush=True)
        except BaseException:
            pass
        return 1


if __name__ == '__main__':
    sys.exit(main())
