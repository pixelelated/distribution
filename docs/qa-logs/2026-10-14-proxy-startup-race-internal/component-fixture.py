#!/usr/bin/env python3
"""UNRUN. No-NIC VM only: exact startup slice/monitor, real signing/SQLite/flusher.

Controlled reachability and in-process synthetic HTTP replies replace transport.
No service, listener, native hashing or provider. Timers retain production values.
Baseline startup-window must return 1 with a precise preserved failed assertion;
candidate all must return 0. A fixture error is never a reproduced baseline.
"""
from __future__ import annotations

import argparse
import ast
import base64
import contextlib
import hashlib
import hmac
import json
import os
from pathlib import Path
import resource
import signal
import sys
import threading
import time
from urllib.parse import parse_qsl, urlsplit
from unittest import mock

PACKET = Path(__file__).resolve().parent
ALL_CASES = ('startup-window', 'already-online', 'persistent-offline',
             'ordinary-reconnect', 'auth-401', 'auth-403', 'network-500',
             'stop-during-initial-probe', 'stop-before-start', 'offline-stop-restart')
USER = 'fixture-a'
TOKEN = '<synthetic-token-a>'
REPORT = {'status': 'FAIL', 'scope': 'controlled source component; actual service proof still owed',
          'cases': [], 'thread_errors': [], 'timers_changed': False}


def need(value, message):
    if not value:
        raise AssertionError(message)


class Denied(BaseException):
    pass


def install_boundary(out, tree):
    roots = tuple(p.resolve() for p in (out, tree, PACKET, Path(sys.base_prefix) / 'lib'))
    public = {str(Path(p).resolve()) for p in ('/etc/os-release', '/proc/self/stat')}

    def audit(event, args):
        if event.startswith('socket.') or event in (
            'subprocess.Popen', 'os.system', 'os.posix_spawn', 'os.fork', 'os.exec'):
            raise Denied(event)
        if event == 'sqlite3.connect':
            need(Path(str(args[0])).resolve().is_relative_to(out), 'non-synthetic database')
        if event == 'open' and not isinstance(args[0], int):
            path = Path(os.fsdecode(args[0])).resolve()
            writing = args[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC)
            if writing and not path.is_relative_to(out):
                raise Denied('write outside result root: ' + str(path))
            if not writing and str(path) not in public and not any(path.is_relative_to(p) for p in roots):
                raise Denied('read outside bound inputs: ' + str(path))
        if event in ('os.remove', 'os.rmdir', 'os.mkdir', 'os.chmod'):
            if not Path(os.fsdecode(args[0])).resolve().is_relative_to(out):
                raise Denied('mutation outside result root')
        if event in ('os.rename', 'os.replace'):
            if not all(Path(os.fsdecode(p)).resolve().is_relative_to(out) for p in args[:2]):
                raise Denied('rename outside result root')

    sys.addaudithook(audit)
    for event, args in [('socket.connect', (None, ('127.0.0.1', 18081))),
                        ('subprocess.Popen', ('false', [], None, None)),
                        ('open', ('/storage/forbidden', 'r', 0))]:
        try:
            sys.audit(event, *args)
        except Denied:
            continue
        raise AssertionError('boundary negative failed: ' + event)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True, help='root containing tree/linux')
    parser.add_argument('--variant', choices=('baseline', 'candidate'), required=True)
    parser.add_argument('--cases', choices=('startup-window', 'all'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    need(sys.flags.optimize == 0, 'assertions required')
    need(os.environ.get('PIX588_ALLOCATED_VM') == 'yes', 'coordinator VM allocation required')
    need({p.name for p in Path('/sys/class/net').iterdir()} == {'lo'}, 'no-NIC guest required')
    need(not any(k.lower().endswith('_proxy') for k in os.environ), 'proxy environment forbidden')
    out = args.output.resolve()
    need(out.is_relative_to('/run') and not out.exists(), 'fresh /run output required')
    binding = json.loads((PACKET / 'bindings.json').read_text())
    tree = (args.source / 'tree').resolve(strict=True)
    need(not list(tree.rglob('*.pyc')), 'unbound bytecode')
    manifest = dict(binding['prepared_python_manifest'])
    manifest[binding['path']] = binding[args.variant + '_sha256']
    need({str(p.relative_to(tree)) for p in tree.rglob('*.py')} == set(manifest), 'source set changed')
    for name, digest in manifest.items():
        path = tree / name
        need(not path.is_symlink() and hashlib.sha256(path.read_bytes()).hexdigest() == digest, name)
    out.mkdir(parents=True, mode=0o700)
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (45, 50))
    resource.setrlimit(resource.RLIMIT_FSIZE, (8 * 1024**2,) * 2)
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('240s wall deadline')))
    signal.alarm(240)
    os.environ['RAOFFLINEPROXY_CONFIG_DIR'] = str(out / 'state')
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(tree / 'linux'))
    install_boundary(out, tree)
    from raofflineproxy import config, cache_keys, flusher, proxy_service, rom_cache, storage

    source_file = tree / binding['path']
    node = next(n for n in ast.parse(source_file.read_bytes()).body
                if getattr(n, 'name', '') == 'run_proxy_service')
    body = next(n for n in node.body if isinstance(n, ast.Try)).body
    first = next(i for i, n in enumerate(body) if isinstance(n, ast.Assign)
                 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'initial_online')
    last = next(i for i, n in enumerate(body) if isinstance(n, ast.Expr)
                and ast.unparse(n.value) == 'connectivity_monitor.start()')
    startup = compile(ast.Module(body=body[first:last + 1], type_ignores=[]), str(source_file), 'exec')
    REPORT.update(variant=args.variant, source_sha256=manifest[binding['path']],
                  source_files=len(manifest), startup_lines=[body[first].lineno, body[last].end_lineno],
                  interpreter=sys.version, substitutions=['controlled reachability',
                  'in-process synthetic GET/POST replies', 'corruption-report observation'])
    started = time.monotonic()

    def thread_error(error):
        REPORT['thread_errors'].append(repr(error.exc_value))

    threading.excepthook = thread_error

    def run_case(name):
        row = {'name': name, 'status': 'FAIL', 'trace': [], 'peer_calls': [], 'applied': []}
        REPORT['cases'].append(row)
        cond = threading.Condition()
        enter = threading.Event()
        release = threading.Event()
        control = {'online': name == 'already-online', 'probes': 0, 'waits': 0, 'flushes': 0}
        case_dir = out / name
        case_dir.mkdir()
        cfg_file = case_dir / 'retroarch.cfg'
        cfg_file.write_text('cheevos_username = "' + USER + '"\ncheevos_token = "' + TOKEN + '"\n')
        cfg_bytes = cfg_file.read_bytes()
        cfg = {'retroarch_cfg': str(cfg_file), 'rocknix_system_cfg': str(case_dir / 'absent-system.cfg'),
               'upstream_host': 'http://fixture.invalid'}
        store = storage.Storage(case_dir / 'proxy.sqlite3')
        need(store.backend == 'sqlite', 'SQLite required')
        server = object.__new__(proxy_service.ProxyRuntimeServer)
        server.config_data = cfg
        server.storage = store
        server.flush_lock = threading.Lock()
        server.pending_award_lock = threading.Lock()
        original_flush = server.flush_pending_awards
        definition = {'Success': True, 'PatchData': {'ID': 10, 'Title': 'Synthetic game',
                      'Achievements': [{'ID': 104, 'Title': 'Synthetic award', 'Flags': 3,
                                        'Points': 5, 'Description': 'Fixture', 'MemAddr': '0xH000000=1'}]}}
        store.upsert_cache(cache_keys.patch(10, USER), json.dumps(definition))
        other_login = json.dumps({'Success': True, 'User': 'fixture-b', 'Token': '<synthetic-token-b>'})
        store.upsert_cache(cache_keys.login('fixture-b'), other_login)
        body = 'r=awardachievement&a=104&g=10&u=' + USER + '&t=' + TOKEN + '&h=0'
        need(server.queue_award('/dorequest.php', body, {}), 'seed award')
        before = store.get_pending_awards()
        need(server.queue_award('/dorequest.php', body, {}), 'dedup queue call')
        need(store.get_pending_awards() == before and len(before) == 1, 'seed dedup')
        secret = config.AWARD_SECRET_FILE.read_bytes()
        row['queue_before'] = before
        row['config_sha256'] = hashlib.sha256(cfg_bytes).hexdigest()
        monitor = proxy_service.ConnectivityMonitor(server)
        need(monitor.interval_seconds == 15, 'production monitor interval')
        if args.variant == 'candidate':
            need(monitor.initial_online is False, 'uninitialized monitor baseline')
        row['interval_seconds'] = monitor.interval_seconds

        def emit(event, **values):
            with cond:
                row['trace'].append({'event': event, 'monotonic': time.monotonic(),
                                     'tid': threading.get_native_id(), **values})
                need(len(row['trace']) <= 80, 'trace bound')
                cond.notify_all()

        def wait_for(predicate, label, seconds=25):
            with cond:
                need(cond.wait_for(lambda: predicate() or REPORT['thread_errors'], seconds), label)
                need(not REPORT['thread_errors'], 'worker exception')

        def probe(force_probe):
            need(force_probe is True, 'forced probe changed')
            control['probes'] += 1
            number = control['probes']
            if number == 2:
                emit('first-monitor-probe-enter')
                enter.set()
                need(release.wait(5), 'controller never released initial probe')
            value = control['online']
            emit('probe-return', number=number, result=value)
            return value

        def flush():
            control['flushes'] += 1
            emit('flush-enter')
            outcome = original_flush()
            emit('flush-return', outcome=outcome)
            return outcome

        def get(url, user_agent, **kwargs):
            need(control['online'], 'GET while offline')
            params = dict(parse_qsl(urlsplit(url).query))
            need(params.get('u') == USER and params.get('t') == TOKEN, 'wrong synthetic account')
            action = params.get('r')
            row['peer_calls'].append({'method': 'GET', 'action': action, 'user': params['u']})
            if action == 'patch':
                return json.dumps(definition)
            if action == 'unlocks':
                return json.dumps({'Success': True, 'UserUnlocks': [104] if row['applied'] else []})
            raise AssertionError('unexpected GET ' + str(action))

        def post(url, payload, **kwargs):
            need(control['online'], 'POST while offline')
            params = dict(parse_qsl(payload))
            need(params.get('u') == USER and params.get('t') == TOKEN, 'wrong synthetic account')
            need(params.get('h') == '0' and params.get('a') == '104', 'wrong award')
            original = before[0]
            for field, key in (('ra_chain_payload_hash', 'payloadHash'),
                               ('ra_chain_prev_hash', 'prevHash'), ('ra_chain_sig', 'signature')):
                need(params[field] == original[key], 'signed queue identity changed')
            signature = base64.b64encode(hmac.new(secret,
                (params['ra_chain_payload_hash'] + ':' + params['ra_chain_prev_hash']).encode(),
                hashlib.sha256).digest()).decode()
            need(hmac.compare_digest(signature, params['ra_chain_sig']), 'independent HMAC check')
            status = {'auth-401': 401, 'auth-403': 403, 'network-500': 500}.get(name, 200)
            row['peer_calls'].append({'method': 'POST', 'action': 'awardachievement',
                                      'user': params['u'], 'status': status, 'signed_identity_verified': True})
            if status == 200:
                need(not row['applied'], 'duplicate application')
                row['applied'].append([USER, 104])
            return status, 'Synthetic', json.dumps({'Success': status == 200})

        def profile(frame, event, arg):
            if event == 'call' and frame.f_code.co_name == 'wait' and frame.f_locals.get('self') is monitor.stop_event:
                need(frame.f_locals.get('timeout') == 15, 'production wait shortened')
                control['waits'] += 1
                emit('monitor-wait', number=control['waits'], timeout=15)

        server.refresh_reachability = probe
        server.flush_pending_awards = flush
        stopped = False
        try:
            with contextlib.ExitStack() as stack:
                stack.enter_context(mock.patch.object(rom_cache, 'http_get', get))
                stack.enter_context(mock.patch.object(flusher, 'http_post', post))
                # Observe the real monitor and startup code; only this unrelated report is replaced.
                stack.enter_context(mock.patch.object(proxy_service, 'retry_storage_corruption_report',
                    lambda *_: emit('startup-corruption-report')))
                threading.setprofile(profile)
                namespace = dict(vars(proxy_service), server=server, config_data=cfg, connectivity_monitor=monitor)
                if name == 'stop-before-start':
                    monitor.stop()
                    emit('stop-before-monitor-start')
                exec(startup, namespace)
                need(enter.wait(5), 'initial worker probe was not reached')
                need(control['probes'] == 2, 'causal startup probe sequence')
                if name in ('startup-window', 'auth-401', 'auth-403', 'network-500',
                            'stop-during-initial-probe', 'stop-before-start'):
                    if name == 'stop-during-initial-probe':
                        monitor.stop()
                        emit('stop-before-probe-return')
                    control['online'] = True
                    emit('controlled-link-online')
                release.set()
                if name in ('stop-during-initial-probe', 'stop-before-start'):
                    monitor.join(5)
                    need(not monitor.is_alive(), 'stopped initial probe failed to join')
                else:
                    wait_for(lambda: control['waits'] >= 1, 'initial monitor processing')
                    if name == 'ordinary-reconnect':
                        control['online'] = True
                        emit('controlled-link-online-after-offline-baseline')
                    if name != 'offline-stop-restart':
                        wait_for(lambda: control['waits'] >= 2, 'natural 15s periodic poll')
                monitor.stop()
                release.set()
                monitor.join(5)
                need(not monitor.is_alive(), 'monitor survived stop')
                stopped = True
                threading.setprofile(None)
                emit('joined-before-storage-close')
                waits = [r['monotonic'] for r in row['trace'] if r['event'] == 'monitor-wait']
                if len(waits) >= 2:
                    need(waits[1] - waits[0] >= 15, 'natural polling interval not observed')
                row['queue_after'] = store.get_pending_awards()
                row['flush_calls'] = control['flushes']
                row['sqlite_integrity'] = store._connection.execute('PRAGMA integrity_check').fetchone()[0]
                need(row['sqlite_integrity'] == 'ok', 'SQLite integrity')
                need(cfg_file.read_bytes() == cfg_bytes, 'credentials changed')
                need(store.get_cache(cache_keys.login('fixture-b'))['responseBody'] == other_login,
                     'unrelated cached account changed')
                if name in ('persistent-offline', 'stop-during-initial-probe', 'stop-before-start', 'offline-stop-restart'):
                    need(control['flushes'] == 0 and row['queue_after'] == before, 'offline/stop queue changed')
                elif name in ('auth-401', 'auth-403', 'network-500'):
                    need(control['flushes'] == 1 and not row['applied'], 'refusal retried or applied')
                    need(len(row['queue_after']) == 1, 'refusal lost queue')
                    after = row['queue_after'][0]
                    allowed = {'lastError', 'retryCount'}
                    need(all(after[k] == v for k, v in before[0].items() if k not in allowed), 'signed identity/account changed')
                    need(after['status'] == 'pending', 'refusal not pending')
                    need(after['retryCount'] == (1 if name == 'network-500' else 0), 'retry semantics changed')
                    need(after['lastError'] == ('HTTP 500' if name == 'network-500' else
                         'Token rejected by server (HTTP ' + name[-3:] + ')'), 'refusal reason changed')
                else:
                    if name == 'startup-window' and control['flushes'] == 0 and row['queue_after'] == before:
                        row['baseline_failure_signature'] = 'startup false; initial/periodic monitor true; zero flush; exact signed row retained'
                    need(control['flushes'] == 1 and row['applied'] == [[USER, 104]] and not row['queue_after'],
                         'queued signed award not applied exactly once')
                if name == 'offline-stop-restart':
                    store.close()
                    store = storage.Storage(case_dir / 'proxy.sqlite3')
                    server.storage = store
                    need(store.get_pending_awards() == before, 'restart changed pending row')
                    # A fresh online startup reuses the exact unchanged startup slice and real queue.
                    control.update(online=True, probes=0, waits=0, flushes=0)
                    enter.clear()
                    release.set()
                    monitor = proxy_service.ConnectivityMonitor(server)
                    stopped = False
                    threading.setprofile(profile)
                    namespace = dict(vars(proxy_service), server=server, config_data=cfg, connectivity_monitor=monitor)
                    exec(startup, namespace)
                    wait_for(lambda: control['waits'] >= 1, 'online restart startup')
                    monitor.stop()
                    monitor.join(5)
                    need(not monitor.is_alive(), 'restart monitor survived')
                    stopped = True
                    threading.setprofile(None)
                    need(control['flushes'] == 1 and row['applied'] == [[USER, 104]] and not store.get_pending_awards(),
                         'restart did not flush once')
                    row['restart_queue_after'] = store.get_pending_awards()
                    row['restart_sqlite_integrity'] = store._connection.execute('PRAGMA integrity_check').fetchone()[0]
                    need(row['restart_sqlite_integrity'] == 'ok', 'restart integrity')
            row['status'] = 'PASS'
        finally:
            monitor.stop()
            release.set()
            if monitor.ident is not None:
                monitor.join(5)
            threading.setprofile(None)
            row['worker_alive_at_storage_close'] = monitor.is_alive()
            need(not monitor.is_alive(), 'refuse closing storage under live worker')
            store.close()
            row['storage_closed'] = True

    try:
        for case in ALL_CASES if args.cases == 'all' else ('startup-window',):
            run_case(case)
        need(not REPORT['thread_errors'], 'thread errors')
        REPORT['status'] = 'PASS'
        return 0
    except BaseException as error:
        REPORT['error'] = type(error).__name__ + ': ' + str(error)
        return 1
    finally:
        signal.alarm(0)
        REPORT['elapsed_seconds'] = time.monotonic() - started
        REPORT['live_threads'] = [t.name for t in threading.enumerate() if t is not threading.main_thread()]
        (out / 'result.json').write_text(json.dumps(REPORT, indent=2) + '\n')
        print(json.dumps({'status': REPORT['status'], 'variant': args.variant, 'result': str(out / 'result.json')}))


if __name__ == '__main__':
    sys.exit(main())
