#!/usr/bin/env python3
"""Source-only prepared runner support; import only during an admitted execution."""
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time

HERE = Path(__file__).resolve().parent
SEQUENCES = {'es':['es-syntax']}
LIMITS = {'es':600}
DISK_LIMIT = 1024**3


def require(ok, message):
    if not ok: raise RuntimeError(message)


def read(path): return json.loads(Path(path).read_text())


def write(path, value):
    path = Path(path)
    with path.open('x') as stream:
        json.dump(value, stream, indent=2); stream.write('\n')


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def verify_packet(root):
    root = Path(root)
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ',1)
        require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'unsafe manifest path')
        require(sha(root/name) == digest, 'packet member changed: '+name)


def identity(pid):
    try:
        stat = Path('/proc')/str(pid)/'stat'
        words = stat.read_text().rsplit(')',1)[1].split()
        return {'pid':pid, 'start_ticks':int(words[19]), 'state':words[0],
                'pgrp':int(words[2]), 'session':int(words[3]),
                'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip()}
    except FileNotFoundError: return None


def same_process(before):
    now = identity(before['pid'])
    return bool(now and all(now[k] == before[k] for k in ('pid','start_ticks','boot_id')))


def absent(code, stdout, stderr, cid):
    return (re.fullmatch(r'[0-9a-f]{64}',cid) is not None and code == 1
            and stdout in ('','\n') and re.fullmatch(
            r'(?i:(?:error: |error response from daemon: )?no such (?:object|container): )'
            +re.escape(cid)+r'\n?',stderr) is not None)


def command(record, argv, seconds=30, env=None, stdin_path=None, stdout_path=None,
            stdout_limit=32*1024**2, capture_stdout=True):
    """Retain original child exit, start identity and bounded diagnostics."""
    record = Path(record); argv = list(map(str,argv))
    started = time.time(); p = None; receipt = {'argv':argv,'started':started}
    output = Path(stdout_path) if stdout_path is not None else record.with_suffix('.stdout')
    input_stream = None
    try:
        if stdin_path is not None:
            receipt['stdin'] = {'path':str(stdin_path),'sha256':sha(stdin_path)}
            input_stream = Path(stdin_path).open('rb')
        receipt['stdout_path'] = str(output)
        with output.open('xb') as out, record.with_suffix('.stderr').open('xb') as err:
            p = subprocess.Popen(argv, stdin=input_stream, stdout=out, stderr=err, env=env, start_new_session=True)
            receipt['pid'] = p.pid; receipt['identity'] = identity(p.pid)
            write(record.with_suffix('.start.json'),receipt)
            try: receipt['original_exit'] = p.wait(timeout=seconds)
            except subprocess.TimeoutExpired:
                receipt['timed_out'] = True
                os.killpg(p.pid,signal.SIGKILL)
                receipt['original_exit'] = p.wait(timeout=5)
        require(not receipt.get('timed_out'), 'command deadline: '+str(record))
        receipt['stdout_bytes'] = output.stat().st_size
        require(receipt['stdout_bytes'] <= stdout_limit
                and record.with_suffix('.stderr').stat().st_size <= 1024**2, 'oversized command diagnostics')
        if not capture_stdout:receipt['stdout_sha256'] = sha(output)
        return receipt['original_exit'], output.read_bytes() if capture_stdout else b'', record.with_suffix('.stderr').read_bytes()
    finally:
        if p is not None and p.poll() is None:
            os.killpg(p.pid,signal.SIGKILL); receipt['original_exit'] = p.wait(timeout=5)
        if input_stream is not None:input_stream.close()
        receipt['ended'] = time.time()
        if p is not None: receipt['reaped'] = p.poll() is not None
        write(record.with_suffix('.json'),receipt)


def safe_member(name):
    path = Path(name)
    require(not path.is_absolute() and path.parts and all(x not in ('.','..','.git') for x in path.parts)
            and str(path) == name.rstrip('/') and '\x00' not in name, 'unsafe source member: '+name)
    return path


def verify_source(work, family, binding):
    from native import inspect_source
    return inspect_source(work, family, binding)


def host_cgroup(pid, cid):
    lines=(Path('/proc')/str(pid)/'cgroup').read_text().splitlines()
    unified=[x[3:] for x in lines if x.startswith('0::')]
    require(len(unified)==1,'unified host cgroup required')
    path=Path('/sys/fs/cgroup')/unified[0].lstrip('/')
    require(path.resolve()==path and path.is_relative_to('/sys/fs/cgroup')
            and path.name in (cid,'docker-'+cid+'.scope'),'unexpected owned host cgroup path')
    return path
