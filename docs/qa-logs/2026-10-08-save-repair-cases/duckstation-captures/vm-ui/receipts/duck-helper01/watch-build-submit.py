#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present pixelelated
"""Submit a durable watch-build process. Submission success is NOT job success.

Run from the frozen worktree. --owner must be a fresh QA/build owner. The
standard runner retains build.rc/status; this launcher retains tool-wrapper.rc.
Actively read both until completion. Disconnected notification is separate.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def write_json(path, data):
    with path.open('x') as stream:
        json.dump(data, stream, indent=2)
        stream.write('\n')


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def worker(owner, command):
    owner = Path(owner)
    write_json(owner / 'launcher-start.json', {
        'utc': now(), 'pid': os.getpid(), 'cwd': str(Path.cwd()),
        'start_ticks': Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()[19],
    })
    try:
        result = subprocess.run(command).returncode
        result = result if result >= 0 else 128 - result
    except OSError:
        result = 125
    # Never manufacture the runner's build.rc, or the job's own inner/outer rc.
    with (owner / 'tool-wrapper.rc').open('x') as stream:
        stream.write(str(result) + '\n')
    write_json(owner / 'launcher-result.json', {
        'utc': now(), 'pid': os.getpid(), 'runner_returncode': result,
        'submission_is_not_completion': True,
    })
    return result


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--worker':
        return worker(sys.argv[2], sys.argv[3:])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--owner', required=True, type=Path)
    parser.add_argument('runner_args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    runner_args = args.runner_args
    if runner_args and runner_args[0] == '--':
        runner_args = runner_args[1:]
    owner = args.owner.resolve(strict=True)
    runner = Path.cwd() / 'tools/watch-build'
    if not owner.is_dir() or not runner.is_file() or not os.access(runner, os.X_OK):
        parser.error('existing owner and executable cwd/tools/watch-build required')
    if not runner_args or os.environ.get('RASTERATOPS_BUILD_RUN'):
        parser.error('runner arguments required; inherited active runs cannot be submitted')
    for name in ['qa.start', 'start', 'inner.rc', 'outer.rc', 'tool-wrapper.rc', 'console.log']:
        if (owner / name).exists():
            parser.error('owner has already started: ' + name)
    os.umask(0o077)
    # Exclusive reservation is permanent even if launch fails. Use a fresh owner.
    write_json(owner / 'launcher-submission.json', {
        'utc': now(), 'cwd': str(Path.cwd()), 'runner': str(runner),
        'runner_sha256': hashlib.sha256(runner.read_bytes()).hexdigest(),
        'submission_is_not_completion': True,
    })
    copy = owner / 'watch-build-submit.py'
    with copy.open('xb') as output:
        output.write(Path(__file__).read_bytes())
    copy.chmod(0o500)
    with (owner / 'console.log').open('xb', buffering=0) as log:
        child = subprocess.Popen(
            [sys.executable, '-I', str(copy), '--worker', str(owner),
             str(runner), *runner_args], stdin=subprocess.DEVNULL,
            stdout=log, stderr=subprocess.STDOUT,
            start_new_session=True, close_fds=True)
    write_json(owner / 'launcher-pid.json', {'pid': child.pid, 'utc': now()})
    print(json.dumps({'state': 'submitted', 'pid': child.pid, 'owner': str(owner),
                      'completion': str(owner / 'launcher-result.json'),
                      'submission_is_not_completion': True}))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print('watch-build-submit: ' + str(error), file=sys.stderr)
        sys.exit(2)
