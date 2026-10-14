#!/usr/bin/env python3
"""UNRUN, read-only cgroup enforcement admission for the disposable service proof."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

ROOT = Path('/sys/fs/cgroup')
SERVICE = 'pix583-service-proof.service'
OWNER = 'pix583-service-proof-owner.service'
BOOT_ARGUMENT = 'systemd.unified_cgroup_hierarchy=1'


def need(value, reason):
    if not value:
        raise AssertionError(reason)


def read(path, cap=65536):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        need(stat.S_ISREG(os.fstat(fd).st_mode), 'nonregular kernel observation: ' + str(path))
        raw = bytearray()
        while True:
            chunk = os.read(fd, min(8192, cap + 1 - len(raw)))
            if not chunk:
                return raw.decode('ascii')
            raw.extend(chunk)
            need(len(raw) <= cap, 'kernel observation exceeds cap: ' + str(path))
    finally:
        os.close(fd)


def platform_contract(binding_path):
    binding = json.loads(binding_path.read_text())
    kernel = binding['kernel_config_module']
    need(os.uname().release == kernel['release'], 'kernel release differs from retained config evidence')
    files = dict(binding['retained_image_elfs'])
    files[kernel['guest_path']] = kernel
    measured = {}
    for name, expected in files.items():
        path = Path(name)
        need(path.is_file() and path.stat().st_size == expected['bytes'], 'platform file size changed: ' + name)
        with path.open('rb') as f:
            digest = hashlib.file_digest(f, 'sha256').hexdigest()
        need(digest == expected['sha256'], 'platform file differs from retained image: ' + name)
        measured[name] = {'sha256': digest, 'bytes': expected['bytes']}
    return {'files': measured, 'kernel_release': os.uname().release,
            'scope': 'retained image platform only; no current product/native source qualification'}


def layout():
    need(os.geteuid() == 0 and 'QEMU' in read('/sys/class/dmi/id/sys_vendor'), 'disposable root QEMU only')
    need(read('/proc/1/comm').strip() == 'systemd', 'actual systemd PID1 required')
    need({p.name for p in Path('/sys/class/net').iterdir()} == {'lo'}, 'no-NIC guest required')
    args = read('/proc/cmdline').split()
    need([a for a in args if a.startswith('systemd.unified_cgroup_hierarchy=')] == [BOOT_ARGUMENT],
         'fresh explicit unified-hierarchy boot required')
    mounts = []
    for line in read('/proc/self/mountinfo', 262144).splitlines():
        fields = line.split(); split = fields.index('-')
        if fields[split + 1] in ('cgroup', 'cgroup2'):
            mounts.append({'id': fields[0], 'device': fields[2], 'root': fields[3],
                           'path': fields[4], 'type': fields[split + 1], 'line': line})
    need(len(mounts) == 1 and mounts[0]['path'] == str(ROOT) and mounts[0]['root'] == '/'
         and mounts[0]['type'] == 'cgroup2', 'full v2 mount required; hybrid/v1/aliased roots refused')
    need(ROOT.resolve(strict=True) == ROOT, 'cgroup root alias')
    pid1 = read('/proc/1/cgroup').splitlines()
    need(len(pid1) == 1 and pid1[0].startswith('0::/'), 'PID1 not solely in unified hierarchy')
    controllers = read(ROOT / 'cgroup.controllers').split()
    need({'memory', 'pids'} <= set(controllers), 'required v2 memory/pids controllers unavailable')
    return {'mounts': mounts, 'controllers': controllers, 'pid1_cgroup': pid1,
            'cmdline': ' '.join(args), 'boot_id': read('/proc/sys/kernel/random/boot_id').strip()}


def identity(pid):
    text = read('/proc/' + str(pid) + '/stat')
    fields = text.rsplit(')', 1)[1].split()
    need(text.split(' ', 1)[0] == str(pid) and fields[0] != 'Z', 'PID absent/zombie/changed')
    return {'pid': pid, 'ppid': int(fields[1]), 'start_ticks': int(fields[19])}


def counters(path):
    pairs = [line.split() for line in read(path).splitlines()]
    need(all(len(p) == 2 and p[1].isdigit() for p in pairs), 'malformed cgroup counters')
    need(len({p[0] for p in pairs}) == len(pairs), 'duplicate cgroup counter')
    return {key: int(value) for key, value in pairs}


def observe(pid, unit, memory_bytes, tasks):
    need((unit, memory_bytes, tasks) in ((OWNER, 1073741824, 128), (SERVICE, 536870912, 64)),
         'unbound resource contract')
    facts = layout(); before = identity(pid)
    group = '/system.slice/' + unit
    membership = read('/proc/' + str(pid) + '/cgroup').splitlines()
    need(membership == ['0::' + group], 'PID is not in the exact owned unit cgroup')
    path = ROOT / group.lstrip('/')
    need(path.resolve(strict=True) == path, 'unit cgroup alias')
    info = path.stat()
    limits = {name: read(path / name).strip() for name in ('memory.max', 'pids.max')}
    need(limits == {'memory.max': str(memory_bytes), 'pids.max': str(tasks)},
         'kernel resource limits differ or are unenforced: ' + repr(limits))
    members = read(path / 'cgroup.procs').splitlines()
    need(all(p.isdigit() for p in members) and pid in set(map(int, members)), 'PID missing from kernel cgroup census')
    memory = counters(path / 'memory.events'); processes = counters(path / 'pids.events')
    need(memory.get('oom') == memory.get('oom_kill') == 0 and processes.get('max') == 0,
         'kernel memory/process guard fired')
    need(identity(pid) == before and read('/proc/' + str(pid) + '/cgroup').splitlines() == membership,
         'PID identity/cgroup changed during admission')
    after = path.stat()
    need((info.st_dev, info.st_ino) == (after.st_dev, after.st_ino), 'cgroup identity changed')
    return {'identity': before, 'control_group': group, 'cgroup_identity': [info.st_dev, info.st_ino],
            'limits': limits, 'memory_events': memory, 'pids_events': processes,
            'members': sorted(set(map(int, members))), 'layout': facts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--service-receipts', type=Path, required=True)
    args = parser.parse_args()
    out = args.service_receipts
    need(out.is_absolute() and out.resolve(strict=True) == out
         and out.name == 'payload' and out.parent.parent == Path('/run/pix583-service-owner'),
         'receipt directory outside allocated payload')
    result = {'status': 'FAIL', 'role': 'ExecStartPre; main has not started', 'pid': os.getpid()}
    try:
        result['kernel'] = observe(os.getpid(), SERVICE, 536870912, 64)
        result['status'] = 'PASS'
    except BaseException as error:
        result['error'] = type(error).__name__ + ': ' + str(error)
    finally:
        with (out / ('cgroup-start-' + str(os.getpid()) + '.json')).open('x') as f:
            json.dump(result, f, indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
