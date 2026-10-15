#!/usr/bin/env python3
"""Bounded, host-only #591 continuation over retained synthetic/VM frames."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

packet = Path('/tmp/pix-m7-frame-diff-review-20261015')
tree = Path('/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-02')
owner = packet / 'execution01'
owner.mkdir(exist_ok=False)
inputs = [packet / n for n in ('claim-controls.py', 'frame-diff.candidate', 'claims.composed.txt')]
inputs += [tree / 'tools/frame-diff', tree / 'tools/vm-walks/masks.txt']
hashes = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
(owner / 'inputs.json').write_text(json.dumps(hashes, indent=2) + '\n')
commands = [
    ('old-control', [sys.executable, str(packet / 'claim-controls.py'), '--source', str(tree / 'tools/frame-diff'), '--out', str(packet / 'old-control01'), '--only', 'adjacent', '--expect-old-failure'], 40),
    ('candidate-controls', [sys.executable, str(packet / 'claim-controls.py'), '--source', str(packet / 'frame-diff.candidate'), '--out', str(packet / 'controls01')], 60),
    ('retained-comparison', [sys.executable, str(packet / 'frame-diff.candidate'), 'compare', '/workspace/artifacts/rocknix-images/walk-baseline', '/workspace/tmp/pix-m7-final-baseline-20261014-02/artifacts/webdav/rocknix-images/qa-fac608ff89-webdav-a-20261014-2320/walks', '--masks', str(tree / 'tools/vm-walks/masks.txt'), '--claims', str(packet / 'claims.composed.txt'), '--report', str(packet / 'continuation01.md')], 240),
]
rows = []
for name, argv, limit in commands:
    started = time.monotonic()
    with (owner / (name + '.stdout')).open('xb') as out, (owner / (name + '.stderr')).open('xb') as err:
        process = subprocess.Popen(argv, stdout=out, stderr=err, start_new_session=True)
        timed_out = False
        try:
            rc = process.wait(timeout=limit)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                rc = process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                rc = process.wait(timeout=5)
    row = dict(name=name, argv=argv, original_returncode=rc, timed_out=timed_out,
               elapsed_seconds=time.monotonic()-started, pid=process.pid, timeout_seconds=limit)
    rows.append(row)
    (owner / (name + '.json')).write_text(json.dumps(row, indent=2)+'\n')
    print(json.dumps(row), flush=True)
    if timed_out or rc:
        break
unchanged = hashes == {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
passed = len(rows) == len(commands) and all(r['original_returncode'] == 0 and not r['timed_out'] for r in rows) and unchanged
(owner / 'result.json').write_text(json.dumps(dict(passed=passed, inputs_unchanged=unchanged, stages=rows), indent=2)+'\n')
sys.exit(0 if passed else 1)
