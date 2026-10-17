#!/usr/bin/env python3
"""UNRUN guest guard, adapted from the existing #587 observer; no page/URL logs."""
import hashlib
import json
import os
from pathlib import Path
import signal
import stat
import time

R = Path('/storage/qa616-provider')
EXPECTED = '8c3a9ba06dc78efffee68bb510b5f273f2fafc8d2ecbc8ee17227a3e4c1e3f0a'
started = time.monotonic()
seen = {}
interventions = []
error = None
next_sample = 0

def write(name, obj):
    target = R / name
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(obj) + '\n')
    temporary.replace(target)

def event(obj):
    interventions.append(obj)
    with (R / 'guards.jsonl').open('a') as handle:
        handle.write(json.dumps(obj) + '\n')

def process(pid):
    try:
        p = Path('/proc', str(pid))
        fields = (p / 'stat').read_text().rsplit(')', 1)[1].split()
        if fields[0] == 'Z':
            return None
        return {'pid': pid, 'start': int(fields[19]), 'ppid': int(fields[1])}
    except (OSError, ValueError):
        return None

def table():
    return {int(p.name): row for p in Path('/proc').iterdir()
            if p.name.isdigit() and (row := process(int(p.name)))}

def same(identity):
    row = process(identity['pid'])
    return row if row and row['start'] == identity['start'] else None

def helper(identity):
    if not same(identity):
        return False
    try:
        p = Path('/proc', str(identity['pid']))
        if (p / 'cmdline').read_bytes().split(b'\0', 1)[0] != b'/usr/bin/cloud-signin-window':
            return False
        if any(x.startswith(b'CLOUD_SIGNIN_DEBUG=') for x in (p / 'environ').read_bytes().split(b'\0')):
            raise ValueError('debug environment present')
        with (p / 'exe').open('rb') as handle:
            digest = hashlib.file_digest(handle, 'sha256').hexdigest()
        return digest == EXPECTED and bool(same(identity))
    except (FileNotFoundError, ProcessLookupError):
        return False

def send(identity, sig, require_helper=False):
    try:
        fd = os.pidfd_open(identity['pid'])
    except ProcessLookupError:
        return False
    try:
        if not same(identity) or (require_helper and not helper(identity)):
            return False
        signal.pidfd_send_signal(fd, sig)
        return True
    finally:
        os.close(fd)

def retain_children(case, rows):
    parents = {pid for pid, row in rows.items()
               if (pid, row['start']) in case['owned']}
    previous = set()
    while previous != parents:
        previous = set(parents)
        parents.update(pid for pid, row in rows.items() if row['ppid'] in parents)
    for pid in parents:
        row = rows[pid]
        case['owned'][(pid, row['start'])] = row

def stop_case(case, reason, now):
    if case.get('term_at') is None:
        event({'at': now, 'case': case['case']['id'], 'reason': reason,
               'identity': case['identity'], 'action': 'guard-TERM'})
        # Re-scan ancestry immediately before stopping; retain every exact identity.
        retain_children(case, table())
        root = case['identity']
        send(root, signal.SIGTERM, require_helper=True)
        for identity in case['owned'].values():
            if identity['pid'] != root['pid']:
                send(identity, signal.SIGTERM)
        case['term_at'] = now
    elif now - case['term_at'] >= 5 and not case.get('killed'):
        root = case['identity']
        retain_children(case, table())
        for identity in case['owned'].values():
            if same(identity):
                sent = send(identity, signal.SIGKILL,
                            require_helper=identity['pid'] == root['pid'])
                if sent:
                    event({'at': now, 'case': case['case']['id'],
                           'identity': identity, 'action': 'guard-KILL', 'reason': reason})
        case['killed'] = True

try:
    os.umask(0o077)
    assert os.geteuid() == 0 and os.uname().machine == 'x86_64'
    assert json.loads((R / 'binding.json').read_text())['helper_sha256'] == EXPECTED
    assert not (R / 'guard-result.json').exists() and not (R / 'guard-stop').exists()
    assert hasattr(os, 'pidfd_open') and hasattr(signal, 'pidfd_send_signal')
    while time.monotonic() - started < 1100 and not (R / 'guard-stop').exists():
        now = time.monotonic()
        mem = {line.split(':')[0]: int(line.split()[1])
               for line in Path('/proc/meminfo').read_text().splitlines()}
        pressure = Path('/proc/pressure/memory')
        psi = pressure.read_text() if pressure.exists() else None
        some = float(psi.splitlines()[0].split('avg10=')[1].split()[0]) if psi else None
        rows = table()
        for receipt in sorted((R / 'launches').glob('*.json')):
            if receipt.name in seen:
                continue
            meta = receipt.lstat()
            assert stat.S_ISREG(meta.st_mode) and meta.st_uid == 0 and not meta.st_mode & 0o077 and meta.st_size < 4096
            data = json.loads(receipt.read_text())
            assert data['helper_sha256'] == EXPECTED and data['exec_argv0'] == '/usr/bin/cloud-signin-window'
            assert data['case']['provider'] in ('light', 'drive', 'dropbox')
            identity = {'pid': data['pid'], 'start': data['start']}
            seen[receipt.name] = {'case': data['case'], 'identity': identity,
                                 'noticed': now, 'verified_at': None,
                                 'owned': {(data['pid'], data['start']): identity}}
        for case in seen.values():
            identity = case['identity']
            retain_children(case, rows)
            live = bool(same(identity))
            if case['verified_at'] is None:
                if helper(identity):
                    case['verified_at'] = now
                elif now - case['noticed'] >= 2:
                    raise ValueError('recorded helper never matched exact executable identity')
                else:
                    continue
            owned_live = [x for x in case['owned'].values() if same(x)]
            if not live:
                case.setdefault('exited_at', now)
            window_log = Path('/var/run/cloud_oauth/window.log')
            log_over = window_log.exists() and window_log.stat().st_size > 1024**2
            reason = ('log-size' if log_over else 'memory' if mem['MemAvailable'] < 160*1024 or
                      (mem['MemAvailable'] < 256*1024 and some is not None and some > 5)
                      else 'deadline' if live and now - case['verified_at'] >= 75
                      else 'children-outlived-helper' if owned_live and not live and
                      now - case['exited_at'] >= 5 else None)
            if owned_live and (reason or case.get('term_at') is not None):
                stop_case(case, reason or 'guard-followup', now)
        if now >= next_sample:
            sample = {'at': now, 'mem': mem, 'psi': psi,
                      'cases': [{'id': c['case']['id'], 'identity': c['identity'],
                                 'verified_at': c['verified_at'],
                                 'owned_live': [x for x in c['owned'].values() if same(x)]}
                                for c in seen.values()]}
            with (R / 'guard-samples.jsonl').open('a') as handle:
                handle.write(json.dumps(sample) + '\n')
            assert (R / 'guard-samples.jsonl').stat().st_size <= 4*1024**2
            next_sample = now + 1
        write('guard-heartbeat.json', {'at': now, 'pid': os.getpid(),
                                      'start': process(os.getpid())['start'],
                                      'verified_cases': sum(c['verified_at'] is not None for c in seen.values()),
                                      'interventions': len(interventions)})
        time.sleep(.25)
    if not (R / 'guard-stop').exists():
        raise TimeoutError('guard group lifetime expired')
except BaseException as exc:
    error = type(exc).__name__
finally:
    # Unexpected guard exit also ends the exact tracked browser descendants.
    for case in seen.values():
        if any(same(x) for x in case['owned'].values()):
            stop_case(case, 'guard-exit', time.monotonic())
    if any(any(same(x) for x in c['owned'].values()) for c in seen.values()):
        time.sleep(5)
        for case in seen.values():
            stop_case(case, 'guard-exit', time.monotonic())
    survivors = [x for c in seen.values() for x in c['owned'].values() if same(x)]
    write('guard-result.json', {'rc': int(bool(interventions or error or survivors)),
                               'error_class': error, 'interventions': interventions,
                               'survivors': survivors, 'elapsed': time.monotonic() - started})
raise SystemExit(int(bool(interventions or error or survivors)))
