#!/usr/bin/env python3
"""Observe owned rsync reads; publish real deltas as watched logs (#437)."""
from pathlib import Path
import datetime
import json
import sys


def record_snapshot(owner, workers):
    owner = Path(owner)
    history = owner / 'copy-io-snapshots.jsonl'
    prior = json.loads(history.read_text().splitlines()[-1]) if history.exists() else {'workers': []}
    old = {row['pid']: row for row in prior['workers']}
    deltas = {}
    for row in workers:
        previous = old.get(row['pid'])
        if previous and previous.get('start_ticks') == row['start_ticks']:
            delta = row['io']['rchar'] - previous['io']['rchar']
            if delta > 0:
                deltas[str(row['pid'])] = delta
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    snapshot = {'utc': now, 'workers': workers}
    with history.open('a') as stream:
        stream.write(json.dumps(snapshot) + '\n')
    progress = {'observed_utc': now, 'scope': 'Actual same-process rsync read deltas; not checksum acceptance',
                'rchar_deltas': deltas, 'total_delta': sum(deltas.values())}
    if progress['total_delta']:
        directory = owner / 'copy-artifacts'
        directory.mkdir(exist_ok=True)
        (directory / 'checksum-progress.json').write_text(json.dumps(progress, indent=2) + '\n')
        # watch-job deliberately scans *.log, not JSON receipt files.
        with (directory / 'checksum-progress.log').open('a') as stream:
            stream.write(json.dumps(progress) + '\n')
    return progress


def observe(owner):
    owner = Path(owner).resolve()
    run = Path((owner / 'copy.run').read_text().strip())
    root = int((run / 'build.pid').read_text())
    assert str(owner).encode() in (Path('/proc') / str(root) / 'cmdline').read_bytes()
    nodes = {}
    for process in Path('/proc').glob('[0-9]*'):
        try:
            fields = (process / 'stat').read_text().rsplit(')', 1)[1].split()
            nodes[int(process.name)] = {
                'ppid': int(fields[1]), 'state': fields[0], 'start_ticks': int(fields[19]),
                'exe': Path((process / 'cmdline').read_bytes().split(b'\0', 1)[0].decode()).name}
        except (OSError, ValueError, UnicodeError):
            continue
    owned = {root}
    while True:
        expanded = owned | {pid for pid, row in nodes.items() if row['ppid'] in owned}
        if expanded == owned:
            break
        owned = expanded
    workers = []
    for pid in sorted(owned):
        row = nodes.get(pid)
        if not row or row['exe'] != 'rsync':
            continue
        try:
            io = dict(line.split(':', 1) for line in (Path('/proc') / str(pid) / 'io').read_text().splitlines())
            workers.append(dict(row, pid=pid, io={key: int(value) for key, value in io.items()}))
        except (OSError, ValueError):
            continue
    return record_snapshot(owner, workers)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: observe-checksum.py COPY_OWNER')
    print(json.dumps(observe(sys.argv[1])))
