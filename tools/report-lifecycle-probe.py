#!/usr/bin/env python3
"""Opt-in build-preflight seam: private harmless child + exact real report writer.
No service, build, namespace setup, admission, arbitrary argv, or cleanup tree.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import time

WRITER_SHA256 = '71c0939c05ba53700a35fd804b30476aceee315f4c46fd27ea9bb9311eb260a4'


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def save(path, data, mode=0o400):
    # Fixture/control/original custody only. The report ALWAYS uses report_writer CLI.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    first = None
    try:
        view = memoryview(data)
        while view:
            n = os.write(fd, view[:65536])
            if n <= 0:
                raise OSError('short custody write')
            view = view[n:]
        os.fsync(fd)
    except BaseException as error:
        first = error
    try:
        os.close(fd)
    except BaseException as error:
        if first is None:
            first = error
    if first is not None:
        raise first
    return dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                identity=identity(path.lstat()))


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':')) + '\n').encode('ascii')


def run(root, scenario):
    anchor = time.monotonic()
    cut = anchor + 30
    wall_cut = time.time_ns() // 1000000 + 30000
    if not root.is_absolute() or root.parent.resolve(strict=True) != root.parent:
        raise ValueError('literal existing ordinary writable parent required')
    root.mkdir(mode=0o700, exist_ok=False)
    writer = Path(__file__).with_name('report_writer.py')
    b = writer.read_bytes()
    if len(b) > 32768 or hashlib.sha256(b).hexdigest() != WRITER_SHA256:
        raise ValueError('writer source binding')
    # This fixed child cannot spawn descendants; unreaped Popen owns its PID.
    program = {'success': 'print("synthetic lifecycle child")',
               'nonzero': 'import sys; print("synthetic refusal"); sys.exit(7)',
               'timeout': 'import time; time.sleep(5)'}[scenario]
    argv = [sys.executable, '-I', '-B', '-c', program]
    request = dict(argv=argv, timeout_seconds=0.3, term_seconds=1, kill_seconds=1,
                   deadline_monotonic=cut, deadline_wall_ms=wall_cut)
    save(root/'child-request.json', encoded(request))
    child = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, close_fds=True)
    timed_out = False
    retired = False
    first = None
    secondary = []
    out = err = b''
    try:
        out, err = child.communicate(timeout=0.3)
    except subprocess.TimeoutExpired:
        timed_out = True
        first = 'TimeoutExpired'
    except BaseException as error:
        first = type(error).__name__ + ':' + str(error)[:160]
    finally:
        # Only this known no-descendant fixture child; no name/cgroup/PID search.
        if child.returncode is None:
            try:
                child.terminate()
            except ProcessLookupError:
                pass
            except BaseException as error:
                secondary.append(type(error).__name__)
            try:
                out, err = child.communicate(timeout=1)
            except subprocess.TimeoutExpired:
                try:
                    child.kill()
                except ProcessLookupError:
                    pass
                except BaseException as error:
                    secondary.append(type(error).__name__)
                try:
                    out, err = child.communicate(timeout=1)
                except BaseException as error:
                    secondary.append(type(error).__name__)
            except BaseException as error:
                secondary.append(type(error).__name__)
        retired = type(child.returncode) is int
    if len(out) + len(err) > 65536:
        raise ValueError('fixture child output cap')
    stdout_ref = save(root/'child.stdout', out)
    stderr_ref = save(root/'child.stderr', err)
    native = dict(argv=argv, pid=child.pid, original_rc=child.returncode,
                  timed_out=timed_out, retired=retired, first_error=first,
                  secondary=secondary, stdout=stdout_ref, stderr=stderr_ref)
    native_ref = save(root/'child-original.json', encoded(native))
    # Compact reference to accessible full originals; no copied transcript waterfall.
    payload = encoded(dict(schema='m7-lifecycle-probe-report-v1', original=native_ref,
                           child_retired=retired, child_rc=child.returncode,
                           namespace='UNEXERCISED_SEPARATE_CHECK_REQUIRED',
                           build_or_service=False, whole_runtime_qualified=False,
                           synthetic_padding='x' * 621000))
    source = dict(path=str(root/'report-source.json'), bytes=len(payload),
                  sha256=hashlib.sha256(payload).hexdigest())
    parent = root.stat()
    write_request = dict(schema='m7-exclusive-report-stdin-v1', bytes=len(payload),
                         sha256=source['sha256'], spool=source['path'],
                         destination=str(root/'report.json'), parent_identity=[parent.st_dev, parent.st_ino],
                         deadline_monotonic=cut, deadline_wall_ms=wall_cut)
    writer_argv = [sys.executable, '-I', '-B', str(writer), '--receive', json.dumps(write_request, separators=(',', ':'))]
    save(root/'writer-request.json', encoded(dict(argv=writer_argv, request=write_request)))
    if time.monotonic() >= cut - 7:
        raise ValueError('no writer/custody reserve')
    # Same Python CLI/writer proposed for the real report; bounded external caller.
    try:
        result = subprocess.run(writer_argv, input=payload + b'\x04', capture_output=True,
                                timeout=min(5, cut-time.monotonic()-2), check=False)
    except subprocess.TimeoutExpired as error:
        # subprocess.run kills/waits its direct no-descendant child on timeout;
        # its API supplies no exact exit status. Keep that status UNKNOWN.
        partial_out = save(root/'writer.stdout', error.stdout or b'')
        partial_err = save(root/'writer.stderr', error.stderr or b'')
        save(root/'writer-original.json', encoded(dict(argv=writer_argv, original_rc=None,
            exception='TimeoutExpired', stdout=partial_out, stderr=partial_err,
            channels_complete=False, terminal_status='UNKNOWN_NO_RETRY')))
        raise
    # Originals before interpretation, including failures.
    wrout = save(root/'writer.stdout', result.stdout)
    wrerr = save(root/'writer.stderr', result.stderr)
    original = save(root/'writer-original.json', encoded(dict(argv=writer_argv,
                    original_rc=result.returncode, stdout=wrout, stderr=wrerr)))
    if result.returncode != 0:
        raise ValueError('report writer refused; complete originals retained')
    lines = result.stdout.splitlines()
    if len(lines) != 2 or json.loads(lines[0])['status'] != 'REPORT_STDIN_READY':
        raise ValueError('writer READY/terminal framing')
    receipt = json.loads(lines[1])
    if receipt['output'] != {k: source[k] if k != 'path' else str(root/'report.json')
                             for k in ('path', 'bytes', 'sha256')}:
        raise ValueError('writer receipt mismatch')
    if (root/'report.json').read_bytes() != payload:
        raise ValueError('external report readback')
    observed = dict(status='ISOLATED_LIFECYCLE_SEAM_OBSERVED', child=native,
                    report=receipt, writer_original=original, deadline_monotonic=cut,
                    elapsed_seconds=time.monotonic()-anchor, namespace_verified=False,
                    runtime_or_assembly_qualified=False,
                    successful_child=not timed_out and child.returncode == 0 and not secondary)
    save(root/'RESULT.json', encoded(observed))
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    if time.monotonic() >= cut or time.time_ns() // 1000000 >= wall_cut:
        raise ValueError('whole probe custody late')
    print(json.dumps(dict(status=observed['status'], successful_child=observed['successful_child'],
                         result=str(root/'RESULT.json'), child_retired=retired,
                         report=receipt['output'], elapsed_seconds=time.monotonic()-anchor)), flush=True)
    return 0 if observed['successful_child'] and retired else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--scenario', choices=('success', 'nonzero', 'timeout'), default='success')
    args = parser.parse_args()
    try:
        return run(args.root, args.scenario)
    except BaseException as error:
        try:
            print(json.dumps(dict(status='REFUSED_OR_PARTIAL', primary=type(error).__name__,
                                  detail=str(error)[:256], root=str(args.root), no_retry=True)), file=sys.stderr, flush=True)
        except BaseException:
            pass
        return 1


if __name__ == '__main__':
    sys.exit(main())
