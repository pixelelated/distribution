# SPDX-License-Identifier: GPL-2.0-or-later
"""Private SYSTEM reconstruction for an admitted, non-exporting QA reader."""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import runpy
import signal
import stat
import tarfile
import time


POLICY = 'private-update-system-readback-v1'
RECEIPT = 'private-readback.json'
STAGE = 'private-readback'
LEAF = 'SYSTEM'
MAX_ARCHIVE = 5 * 1024**3
MAX_SYSTEM = 4 * 1024**3
MAX_RECORD = 16 * 1024
MAX_HEADERS = 4096
CHUNK = 1024**2
OPEN = os.O_CLOEXEC | os.O_NOFOLLOW | os.O_NONBLOCK


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def canonical(value):
    path = Path(value)
    require(path.is_absolute() and str(path) == str(value) and path.resolve(strict=True) == path,
            'noncanonical readback path')
    return path


def identity(s):
    return [s.st_dev, s.st_ino, s.st_uid, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns, s.st_blocks * 512]


def dir_identity(s):
    return [s.st_dev, s.st_ino, s.st_uid, s.st_mode]


def hex_digest(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def tick(deadline):
    require(time.monotonic() < deadline, 'private readback time bound reached')


@contextmanager
def descriptor(fd):
    try:
        yield fd
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass  # Preserve the operation error and never retry a close.
        raise
    else:
        os.close(fd)


@contextmanager
def lease_notifications():
    def broken(_signum, _frame):
        raise RuntimeError('private readback kernel lease was contended')

    previous = signal.signal(signal.SIGIO, broken)
    try:
        yield
    finally:
        signal.signal(signal.SIGIO, previous)


def file_lease(fd, mode):
    try:
        fcntl.fcntl(fd, fcntl.F_SETLEASE, mode)
    except BlockingIOError as error:
        raise ValueError('private readback file is busy (kernel lease refused)') from error


def verify_file(fd, location, expected, parent=None):
    require(identity(os.fstat(fd)) ==
            identity(os.stat(location, dir_fd=parent, follow_symlinks=False)) == expected,
            'private readback descriptor or name changed')


@contextmanager
def keeper_file(path, expected=None):
    canonical(path)
    with descriptor(os.open(path, os.O_RDONLY | OPEN)) as fd:
        s = os.fstat(fd)
        require(stat.S_ISREG(s.st_mode) and s.st_uid == os.geteuid() and s.st_nlink == 1
                and not s.st_mode & 0o022 and 0 < s.st_size <= MAX_ARCHIVE,
                'independent archive is not a bounded owned regular file')
        current = identity(s)
        require(expected is None or expected == current, 'independent archive custody changed')
        file_lease(fd, fcntl.F_RDLCK)
        verify_file(fd, canonical(path), current)
        yield fd, current


def read_exact(fd, offset, size):
    data = os.pread(fd, size, offset)
    require(len(data) == size, 'private readback short read')
    return data


def write_all(fd, data):
    view = memoryview(data)
    while view:
        count = os.write(fd, view)
        require(count > 0, 'private readback short write')
        view = view[count:]


def reconstruction(archive, size, expected_sha, deadline, destination=None):
    """Read one bounded plain release tar. No extraction of archive-selected paths."""
    whole, member_sha = hashlib.sha256(), hashlib.sha256()
    offset = 0

    def take(count):
        nonlocal offset
        tick(deadline)
        require(0 < count <= CHUNK and offset + count <= size, 'release tar extent exceeds file')
        data = read_exact(archive, offset, count)
        whole.update(data)
        offset += count
        return data

    selected, long_name, names, roots = None, None, set(), set()
    for _ in range(MAX_HEADERS):
        header = take(512)
        if not any(header):
            require(long_name is None and not any(take(512)), 'invalid release tar end marker')
            while offset < size:
                require(not any(take(min(CHUNK, size - offset))), 'release tar has nonzero tail')
            break
        require(header[257:265] in (tarfile.POSIX_MAGIC, tarfile.GNU_MAGIC),
                'private readback needs a plain GNU or POSIX release tar')
        try:
            entry = tarfile.TarInfo.frombuf(header, 'ascii', 'strict')
        except (tarfile.HeaderError, UnicodeError) as error:
            raise ValueError('invalid release tar header') from error
        if entry.type == tarfile.GNUTYPE_LONGNAME:
            require(long_name is None and 1 < entry.size <= 4096, 'invalid GNU long name')
            raw = take(entry.size)
            require(raw.endswith(b'\0') and b'\0' not in raw[:-1], 'invalid GNU long name bytes')
            long_name = raw[:-1].decode('ascii')
        else:
            name = long_name if long_name is not None else entry.name
            long_name = None
            if entry.isdir():
                name = name.rstrip('/')
            parts = PurePosixPath(name)
            require(entry.type in (tarfile.REGTYPE, tarfile.AREGTYPE, tarfile.DIRTYPE)
                    and parts.parts and not parts.is_absolute() and str(parts) == name
                    and '..' not in parts.parts and name not in names
                    and not {'storage', 'usr', '.config'}.intersection(parts.parts)
                    and all(32 < ord(c) < 127 for c in name)
                    and (entry.size == 0 if entry.isdir() else entry.size >= 0),
                    'unsafe, duplicate or unsupported release tar member')
            names.add(name)
            roots.add(parts.parts[0])
            wanted = len(parts.parts) == 3 and parts.parts[1:] == ('target', LEAF)
            if wanted:
                require(selected is None and entry.isfile() and 0 < entry.size <= MAX_SYSTEM,
                        'release tar does not uniquely bind a bounded SYSTEM')
                selected = {'name': name, 'size': entry.size}
            remaining = entry.size
            while remaining:
                data = take(min(CHUNK, remaining))
                remaining -= len(data)
                if wanted:
                    member_sha.update(data)
                    if destination is not None:
                        write_all(destination, data)
        padding = (-entry.size) % 512
        if padding:
            require(not any(take(padding)), 'release tar has nonzero member padding')
    else:
        raise ValueError('release tar header bound exceeded')
    require(selected is not None and len(roots) == 1 and whole.hexdigest() == expected_sha,
            'independent archive digest or SYSTEM membership differs')
    return dict(selected, sha256=member_sha.hexdigest())


def leaf_digest(fd, size, deadline):
    sha = hashlib.sha256()
    for offset in range(0, size, CHUNK):
        tick(deadline)
        sha.update(read_exact(fd, offset, min(CHUNK, size - offset)))
    return sha.hexdigest()


def publish(directory, name, body):
    raw = (json.dumps(body, sort_keys=True, separators=(',', ':')) + '\n').encode('ascii')
    require(len(raw) <= MAX_RECORD, 'private readback record exceeds its bound')
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | OPEN
    with descriptor(os.open(name, flags, 0o400, dir_fd=directory)) as fd:
        write_all(fd, raw)
        os.fsync(fd)
    os.fsync(directory)
    require(record(directory, name)[0] == body, 'private readback record readback differs')


def record(directory, name):
    with descriptor(os.open(name, os.O_RDONLY | OPEN, dir_fd=directory)) as fd:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_uid == os.geteuid()
                and before.st_nlink == 1 and stat.S_IMODE(before.st_mode) == 0o400
                and 0 < before.st_size <= MAX_RECORD, 'invalid private readback record')
        raw = read_exact(fd, 0, before.st_size)
        verify_file(fd, name, identity(before), directory)
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def absent(directory, name):
    try:
        os.stat(name, dir_fd=directory, follow_symlinks=False)
    except FileNotFoundError:
        return True
    return False


def optional_record(directory, name):
    try:
        return record(directory, name)[0]
    except FileNotFoundError:
        if absent(directory, name):
            return None
        raise


def verify_stage(run, directory, expected):
    stage = canonical(run / STAGE)
    actual = dir_identity(os.fstat(directory))
    require(actual == dir_identity(stage.lstat()) == expected and actual[2] == os.geteuid()
            and actual[3] == (stat.S_IFDIR | 0o700), 'private readback stage identity or mode changed')


def admitted_readback(row, archive, archive_sha):
    scope = row['retention_scope']
    require(row.get('private_readback') == {'archive': str(archive), 'sha256': archive_sha}
            and not row.get('retire_on_consume'), 'private readback was not declared in the producer admission')
    require(str(archive) in scope['protected']
            and not any(archive.is_relative_to(path) for path in scope['outputs'])
            and not archive.is_relative_to(Path(row['run'])),
            'independent archive is not a protected input outside generated outputs')


@contextmanager
def produce(archive, archive_sha):
    """Entered by the fixed host QA reader; the pathname stays inside this reader."""
    require(os.getuid() == os.geteuid() != 0 and hex_digest(archive_sha),
            'ordinary-account readback with an exact archive digest is required')
    checkout = Path.cwd()
    inherited = os.environ.get('RASTERATOPS_BUILD_RUN', '')
    relative = Path(inherited)
    require(len(relative.parts) == 2 and relative.parts[0] == '.build-runs'
            and relative.parts[1] != '..', 'private readback must be inside an admitted watcher')
    run = canonical(checkout / relative)
    archive = canonical(archive)
    admission = runpy.run_path(str(Path(__file__).with_name('build-admission')))
    deadline = time.monotonic() + 180
    with admission['retirement_parent'](run / RECEIPT, checkout, checkout.stat().st_dev) as run_fd:
        row = read_admission(run_fd)
        require(row['state'] == 'running' and row['run'] == str(run) and row['checkout'] == str(checkout)
                and row['runner_pid'] == os.getppid(), 'private readback must be the direct admitted child')
        admitted_readback(row, archive, archive_sha)
        with lease_notifications(), keeper_file(archive) as (keeper, custody):
            os.mkdir(STAGE, 0o700, dir_fd=run_fd)
            flags = os.O_RDONLY | os.O_DIRECTORY | OPEN
            with descriptor(os.open(STAGE, flags, dir_fd=run_fd)) as stage:
                fcntl.flock(stage, fcntl.LOCK_EX | fcntl.LOCK_NB)
                stage_identity = dir_identity(os.fstat(stage))
                require(stage_identity[0] == row['volume_device'], 'private readback volume changed')
                verify_stage(run, stage, stage_identity)
                os.fsync(run_fd)
                flags = os.O_RDWR | os.O_EXCL | os.O_CREAT | OPEN
                with descriptor(os.open(LEAF, flags, 0o600, dir_fd=stage)) as target:
                    member = reconstruction(keeper, custody[5], archive_sha, deadline, target)
                    os.fchmod(target, 0o400)
                    os.fsync(target)
                    leaf = identity(os.fstat(target))
                    verify_file(target, LEAF, leaf, stage)
                    require(leaf[5] == member['size'] and leaf_digest(target, leaf[5], deadline) == member['sha256'],
                            'private reconstruction readback differs')
                verify_file(keeper, canonical(archive), custody)
                require(fcntl.fcntl(keeper, fcntl.F_GETLEASE) == fcntl.F_RDLCK, 'archive lease lost')
                os.fsync(stage)
                publish(run_fd, RECEIPT, dict(schema=1, policy=POLICY, run=str(run), admission_id=row['id'],
                        stage=stage_identity, leaf=leaf, archive=str(archive), archive_identity=custody,
                        archive_sha256=archive_sha, member=member))
                with descriptor(os.open(LEAF, os.O_RDONLY | OPEN, dir_fd=stage)) as fd:
                    verify_file(fd, LEAF, leaf, stage)
                    yield fd
                    verify_file(fd, LEAF, leaf, stage)
                    require(fcntl.fcntl(keeper, fcntl.F_GETLEASE) == fcntl.F_RDLCK, 'archive lease lost')


def read_admission(directory, name='admission.json', *, sync=False):
    with descriptor(os.open(name, os.O_RDONLY | OPEN, dir_fd=directory)) as fd:
        s = os.fstat(fd)
        require(stat.S_ISREG(s.st_mode) and s.st_uid == os.geteuid() and s.st_nlink == 1
                and not s.st_mode & 0o022 and 0 < s.st_size <= 1024**2, 'invalid original admission')
        raw = read_exact(fd, 0, s.st_size)
        if sync:
            os.fsync(fd)
            os.fsync(directory)
        verify_file(fd, name, identity(s), directory)
        return json.loads(raw)


def retire(run, row, original, deadline, before_unlink, admission):
    """Called under the ordinary cycle's ordered registry locks."""
    target = run / STAGE / LEAF
    with admission['retirement_parent'](run / RECEIPT, Path(row['checkout']), row['volume_device']) as run_fd:
        receipt, receipt_sha = record(run_fd, RECEIPT)
        require(set(receipt) == {'schema', 'policy', 'run', 'admission_id', 'stage', 'leaf', 'archive',
                                'archive_identity', 'archive_sha256', 'member'}
                and type(receipt['schema']) is int and receipt['schema'] == 1 and receipt['policy'] == POLICY
                and receipt['run'] == str(run) and receipt['admission_id'] == row['id']
                and hex_digest(receipt['archive_sha256'])
                and isinstance(receipt['stage'], list) and len(receipt['stage']) == 4
                and receipt['stage'][0] == row['volume_device'], 'producer readback receipt differs')
        receipt_refs = [item for item in original['evidence'] if item['path'] == str(run / RECEIPT)]
        require(receipt_refs == [{'path': str(run / RECEIPT), 'sha256': receipt_sha}],
                'original acceptance did not bind the producer receipt')
        require(str(run / RECEIPT) in row['retained_evidence'], 'producer receipt is outside retained custody')
        admission['protect_paths']([target], row['retention_scope']['protected'] +
                                   [item['path'] for item in original['evidence']],
                                   'original inputs or accepted evidence hold the private readback')
        archive = canonical(receipt['archive'])
        admitted_readback(row, archive, receipt['archive_sha256'])
        require(isinstance(receipt['leaf'], list) and len(receipt['leaf']) == 9
                and all(type(value) is int and value >= 0 for value in receipt['leaf'])
                and receipt['leaf'][2:5] == [os.geteuid(), stat.S_IFREG | 0o400, 1]
                and 0 < receipt['leaf'][5] <= MAX_SYSTEM, 'ineligible private readback leaf')
        flags = os.O_RDONLY | os.O_DIRECTORY | OPEN
        with descriptor(os.open(STAGE, flags, dir_fd=run_fd)) as stage:
            fcntl.flock(stage, fcntl.LOCK_EX | fcntl.LOCK_NB)
            verify_stage(run, stage, receipt['stage'])
            intent_name, result_name = 'private-readback-intent.json', 'private-readback-result.json'
            bound = dict(schema=1, receipt_sha256=receipt_sha, acceptance_sha256=row['evidence_sha256'],
                         path=str(target), identity=receipt['leaf'])
            intent = optional_record(run_fd, intent_name)
            result = optional_record(run_fd, result_name)
            require(intent is None or intent == bound, 'private readback intent differs')
            if result is not None:
                require(isinstance(result, dict) and intent == bound and result == dict(bound, status=result.get('status'))
                        and result.get('status') in ('retired', 'absent_unconfirmed')
                        and absent(stage, LEAF), 'private readback result differs')
                return result['status'], 0
            require(read_admission(run_fd, 'admission-consumed.json', sync=True) == row,
                    'durable consumption changed before private readback retirement')
            with lease_notifications():
                return retire_leaf(run, run_fd, stage, receipt, archive, bound, intent,
                                   intent_name, result_name, before_unlink, deadline)


def retire_leaf(run, run_fd, stage, receipt, archive, bound, intent,
                intent_name, result_name, before_unlink, deadline):
    try:
        fd = os.open(LEAF, os.O_RDONLY | OPEN, dir_fd=stage)
    except FileNotFoundError:
        require(intent == bound, 'private readback disappeared without a durable intent')
        publish(run_fd, result_name, dict(bound, status='absent_unconfirmed'))
        return 'absent_unconfirmed', 0
    with descriptor(fd) as leaf, keeper_file(archive, receipt['archive_identity']) as (keeper, custody):
        file_lease(leaf, fcntl.F_WRLCK)
        verify_file(leaf, LEAF, receipt['leaf'], stage)
        observed = reconstruction(keeper, custody[5], receipt['archive_sha256'], deadline)
        require(observed == receipt['member'] and receipt['leaf'][5] == observed['size']
                and leaf_digest(leaf, observed['size'], deadline) == observed['sha256'],
                'private reconstruction or independent archive readback differs')
        if intent is None:
            publish(run_fd, intent_name, bound)
        before_unlink()
        tick(deadline)
        verify_stage(run, stage, receipt['stage'])
        verify_file(keeper, canonical(archive), custody)
        verify_file(leaf, LEAF, receipt['leaf'], stage)
        require(fcntl.fcntl(leaf, fcntl.F_GETLEASE) == fcntl.F_WRLCK
                and fcntl.fcntl(keeper, fcntl.F_GETLEASE) == fcntl.F_RDLCK, 'kernel readback lease lost')
        os.unlink(LEAF, dir_fd=stage)
        require(os.fstat(leaf).st_nlink == 0 and absent(stage, LEAF),
                'intended private readback inode still linked')
        os.fsync(stage)
    publish(run_fd, result_name, dict(bound, status='retired'))
    return 'retired', receipt['leaf'][-1]
