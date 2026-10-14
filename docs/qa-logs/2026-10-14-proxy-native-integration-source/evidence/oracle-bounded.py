# SPDX-License-Identifier: MIT
"""UNRUN runner primitive; preserve command rc/logs and kill its group on timeout."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def run(owner, label, argv, seconds=30, env=None, cwd=None):
    prefix = Path(owner) / label
    started = time.monotonic()
    with prefix.with_suffix('.stdout').open('xb') as stdout, prefix.with_suffix('.stderr').open('xb') as stderr:
        child = subprocess.Popen([str(a) for a in argv], stdout=stdout, stderr=stderr,
                                 start_new_session=True, env=env, cwd=cwd)
        timeout = False
        try:
            child.wait(timeout=seconds)
        except subprocess.TimeoutExpired:
            timeout = True
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            child.wait()
    receipt = dict(argv=[str(a) for a in argv], pid=child.pid, process_group=child.pid,
                   returncode=child.returncode, timed_out=timeout, elapsed=time.monotonic()-started,
                   executable_sha256=sha(argv[0]))
    prefix.with_suffix('.json').write_text(json.dumps(receipt, indent=2)+'\n')
    if timeout:
        raise RuntimeError(label + ': timeout; original result retained')
    return receipt, prefix.with_suffix('.stdout').read_text(), prefix.with_suffix('.stderr').read_text()


def require(value, message):
    if not value:
        raise RuntimeError(message)


def verify_sources(root, binding):
    for name, digest in binding.items():
        require(sha(Path(root)/name) == digest, 'source binding changed: '+name)


def synthetic_manifest(directory):
    directory = Path(directory).resolve(strict=True)
    manifest = directory / 'manifest.json'
    require(manifest.stat().st_size <= 65536, 'unexpected fixture manifest size')
    rows = json.loads(manifest.read_text())
    require(isinstance(rows, list) and 1 <= len(rows) <= 64, 'unexpected fixture count')
    names = set()
    total = 0
    for row in rows:
        name = row['name']
        require(isinstance(name, str) and name not in names, 'duplicate/invalid fixture name')
        names.add(name)
        path = (directory / name).resolve(strict=True)
        require(path.parent == directory and path.is_file(), 'fixture outside supplied owner')
        require(row['console'] in ('gamecube', 'nes'), 'unexpected fixture console')
        size = path.stat().st_size
        total += size
        require(size == row['bytes'] and total <= 32 * 1024 * 1024, 'fixture byte budget changed')
        require(sha(path) == row['sha256'], 'fixture bytes changed: ' + name)
    raw = next(row for row in rows if row['name'] == 'synthetic.iso')
    data = (directory / raw['name']).read_bytes()
    require(len(data) == 0x60000 and data[:6] == b'PX5740', 'not the prepared self-created raw input')
    return directory, rows
