#!/usr/bin/env python3
"""UNRUN synthetic detached FD holder; executed only inside admitted fixture jail."""
import json
import os
from pathlib import Path
import signal
import sys
import time

fd, case, attempt = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
assert case in ('detached-transfer-child', 'proc-census-error', 'transport-timeout') and attempt == 1
os.setsid()
signal.signal(signal.SIGTERM, signal.SIG_IGN)
raw = Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()
held = os.fstat(fd)
qa = Path('/qa')
(qa / 'detached-child-ready-1.json').write_text(json.dumps({
    'pid': os.getpid(), 'ppid': os.getppid(), 'start_ticks': int(raw[19]),
    'fd_device': held.st_dev, 'fd_inode': held.st_ino,
    'case': case, 'meaning': 'Synthetic live holder of the transaction archive FD'}) + '\n')
if case == 'proc-census-error':
    # Observe the refusal before ending naturally. This is fixture-owned release,
    # not product cleanup success. The owner preserves the unmatched journal.
    deadline = time.monotonic() + 25
    stage = Path('/storage/.local/share/Steam/.steam-client-update')
    while time.monotonic() < deadline:
        events = [json.loads(s) for s in (qa / 'events.ndjson').read_text().splitlines()]
        if any(e.get('kind') == 'helper-exit' and e.get('helper') == 'client'
               and e.get('mode') == 'install' and e.get('original_exit') == 1 for e in events):
            break
        time.sleep(0.01)
    else:
        raise RuntimeError('Expected census refusal did not finish within 25 seconds')
    rows = [json.loads(s) for s in (stage / 'owner.jsonl').read_text().splitlines()]
    starts = [r['serial'] for r in rows if r['op'] == 'transfer-start']
    stops = [r['serial'] for r in rows if r['op'] == 'transfer-stopped']
    archive = (stage / 'archive').stat()
    assert starts == [1, 2] and stops == [1] and os.fstat(fd).st_nlink == 1
    assert (archive.st_dev, archive.st_ino) == (held.st_dev, held.st_ino)
    (qa / 'held-state-observation.json').write_text(json.dumps({
        'status': 'OBSERVED_HELD_WHILE_CHILD_LIVE', 'pid': os.getpid(),
        'archive_identity_unchanged': True, 'unmatched_transfer': 2,
        'original_child_exit': 77, 'release': 'independent fixture actor; not product quiescence'}) + '\n')
    os.close(fd)
    sys.exit(77)
time.sleep(600)  # Product's bounded cleanup must kill/reap this known child.
raise RuntimeError('Product failed to retire the synthetic child')
