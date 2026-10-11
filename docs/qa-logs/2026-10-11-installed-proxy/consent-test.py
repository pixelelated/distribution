#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present pixelelated
"""Prove installed reporting consent in an isolated QA guest with no default route.

Uses real packaged reporting functions, SQLite and loopback HTTP. Only the log
upload destination constant is redirected; no reporting/consent function is
replaced. Does not prove scheduler timing, UI consent or a real provider.
"""
import argparse
import hashlib
import http.server
import importlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
import zipfile


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def child(root, name, endpoint, replay, require_early_uptime):
    state = root / name
    state.mkdir(mode=0o700, exist_ok=replay)
    os.environ['RAOFFLINEPROXY_CONFIG_DIR'] = str(state)
    os.environ['RAOFFLINEPROXY_USAGE_URL'] = endpoint + '/usage'
    modules = {n: importlib.import_module('raofflineproxy.' + n) for n in
               ['config', 'cache_keys', 'storage', 'usage_stats', 'usage_report',
                'storage_corruption', 'log_uploader', 'proxy_service']}
    loaded = {}
    for name_, module in modules.items():
        path = Path(module.__file__).resolve()
        if not path.is_relative_to('/usr/lib') or path.suffix != '.pyc':
            raise RuntimeError('Refusing non-installed bytecode: ' + str(path))
        loaded[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    cfg, stats = modules['config'], modules['usage_stats']
    report, corruption = modules['usage_report'], modules['storage_corruption']
    uploader, service = modules['log_uploader'], modules['proxy_service']
    assert cfg.CONFIG_DIR.resolve() == state.resolve()
    uploader.REQUEST_UPLOAD_URL = endpoint + '/request-upload'
    # Deliberately synthetic cached sign-in: enough to make reporting eligible.
    synthetic_name, synthetic_session = 'QAConsentOnly', 'qa-' + 'only'
    store = modules['storage'].Storage()
    try:
        if not replay:
            store.upsert_cache(modules['cache_keys'].login(synthetic_name),
                               json.dumps({'User': synthetic_name, 'Token': synthetic_session}))
            assert store.load_login_credentials() is not None
            value, version, logs, expected_usage, expected_logs = CASES[name]
            data = {'usage_stats_consent_version': version}
            if name != 'unanswered':
                data['usage_stats_consent'] = value
                data['upload_logs'] = logs
            cfg.save_config(data)
            stats.USAGE_STATS_FILE.write_text(json.dumps({'requests_emulator': 7}))
            if name == 'explicit-decline':
                stats.save_consent(False)
                assert not stats.USAGE_STATS_FILE.exists(), 'decline did not clear counters'
                # Old on-disk counters must not bypass the consent guard either.
                stats.USAGE_STATS_FILE.write_text(json.dumps({'requests_emulator': 7}))
            uptime = time.monotonic()
            stats.record_request(stats.SOURCE_EMULATOR, 200)
            stats.flush()
            actual = stats.snapshot().get('requests_emulator')
            expected = 8 if expected_usage else 7
            save(root / (name + '-counter-observation.json'),
                 {'uptime_seconds': uptime, 'actual': actual, 'expected': expected,
                  'installed_modules': loaded})
            if require_early_uptime and name == 'usage-only':
                assert uptime < stats.CONSENT_CACHE_SECONDS, ('early boot window missed', uptime)
            assert actual == expected, (name, 'counter', actual, expected, 'uptime', uptime)
            corrupt_file = state / 'synthetic.json.corrupt-test'
            corrupt_file.write_text('{ invalid synthetic state')
            cfg.LOG_FILE.write_text('Synthetic QA incident only\n')
            corruption.record_incident(corrupt_file, 'synthetic QA incident',
                                       corrupt_file.stat().st_size, 1)
            assert corruption.load_incident()['reported'] is False
        else:
            expected_usage = expected_logs = False
            assert store.load_login_credentials() is not None
        before = corruption.load_incident()
        usage_sent = report.report_if_due(store)
        assert usage_sent is expected_usage, (name, 'usage result', usage_sent)
        service.retry_storage_corruption_report(cfg.load_config())
        after = corruption.load_incident()
        if expected_logs:
            assert after['reported'] is True and after['upload_id'] == 'qa-upload'
        else:
            assert after == before, 'refused/replayed incident changed'
        if expected_usage:
            assert stats.last_reported_at() > 0
            assert not stats.reportable(stats.snapshot()), 'sent counters not cleared'
        save(root / (name + ('-replay' if replay else '') + '-result.json'),
             {'case': name, 'replay': replay, 'usage_sent': usage_sent,
              'incident_reported': after['reported'], 'installed_modules': loaded})
    finally:
        store.close()


# usage consent, consent version, independent log consent, expected usage/log sends
CASES = {
    # Exercise the granted path first so a fast boot can prove #457 directly.
    'usage-only': (True, 1, False, True, False),
    'unanswered': (None, 1, None, False, False),
    'declined': (False, 1, False, False, False),
    'null': (None, 1, None, False, False),
    'zero': (0, 1, 0, False, False),
    'one': (1, 1, 1, False, False),
    'string-false': ('false', 1, 'false', False, False),
    'string-true': ('true', 1, 'true', False, False),
    'list': ([], 1, [], False, False),
    'object': ({}, 1, {}, False, False),
    'old-grant': (True, 0, False, False, False),
    'old-decline': (False, 0, False, False, False),
    'explicit-decline': (True, 1, False, False, False),
    'logs-only': (False, 1, True, False, True),
    'both-enabled': (True, 1, True, True, True),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--expected-build')
    parser.add_argument('--case', choices=CASES)
    parser.add_argument('--endpoint')
    parser.add_argument('--replay', action='store_true')
    parser.add_argument('--require-early-uptime', action='store_true',
                        help='require the first granted counter before the 30-second cache interval')
    args = parser.parse_args()
    if args.case:
        if not args.endpoint or not args.endpoint.startswith('http://127.0.0.1:'):
            parser.error('child requires loopback endpoint')
        child(args.output, args.case, args.endpoint, args.replay, args.require_early_uptime)
        return 0
    identity = dict(line.split('=', 1) for line in Path('/etc/os-release').read_text().splitlines()
                    if '=' in line)
    if not args.expected_build or identity.get('BUILD_ID', '').strip('"') != args.expected_build:
        parser.error('exact expected BUILD_ID required')
    for family in ['-4', '-6']:
        routes = subprocess.check_output(['ip', family, 'route', 'show', 'default'], text=True)
        if routes.strip():
            parser.error('remove guest default routes before isolated proof')
    root = args.output.resolve()
    if not root.is_relative_to('/storage/.cache'):
        parser.error('output must be a fresh directory under /storage/.cache')
    root.mkdir(mode=0o700, exist_ok=False)
    events = []

    class Collector(http.server.BaseHTTPRequestHandler):
        def log_message(self, *unused):
            pass

        def do_POST(self):
            self.receive()

        def do_PUT(self):
            self.receive()

        def receive(self):
            body = self.rfile.read(int(self.headers.get('Content-Length', '0')))
            event = {'method': self.command, 'path': self.path, 'bytes': len(body),
                     'sha256': hashlib.sha256(body).hexdigest()}
            response, code = b'{}', 200
            if self.path == '/usage' and self.command == 'POST':
                payload = json.loads(body)
                assert payload['counters']['requests_emulator'] == 8
                assert b'QAConsentOnly' not in body and b'qa-only' not in body
                event['payload_fields'] = sorted(payload)
            elif self.path == '/request-upload' and self.command == 'POST':
                response = json.dumps({'id': 'qa-upload', 'uploadUrl': endpoint + '/upload'}).encode()
            elif self.path == '/upload' and self.command == 'PUT':
                with zipfile.ZipFile(io.BytesIO(body)) as archive:
                    event['archive_members'] = sorted(archive.namelist())
                    assert 'storage_corruption.txt' in archive.namelist()
                    assert b'synthetic QA incident' in archive.read('storage_corruption.txt')
            else:
                code = 404
            events.append(event)
            self.send_response(code)
            self.send_header('Content-Length', str(len(response)))
            self.end_headers()
            self.wfile.write(response)

    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Collector)
    endpoint = 'http://127.0.0.1:' + str(server.server_port)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    results = []
    try:
        for name, (_, _, _, usage, logs) in CASES.items():
            for replay in [False, True]:
                before = len(events)
                command = [sys.executable, '-I', str(Path(__file__).resolve()), '--output',
                           str(root), '--case', name, '--endpoint', endpoint]
                if replay:
                    command.append('--replay')
                if args.require_early_uptime:
                    command.append('--require-early-uptime')
                run = subprocess.run(command, text=True, capture_output=True, timeout=45)
                (root / (name + ('-replay' if replay else '') + '.log')).write_text(run.stdout + run.stderr)
                assert run.returncode == 0, (name, replay, run.returncode)
                observed = [(e['method'], e['path']) for e in events[before:]]
                expected = [] if replay else ([('POST', '/usage')] if usage else []) + (
                    [('POST', '/request-upload'), ('PUT', '/upload')] if logs else [])
                assert observed == expected, (name, replay, observed, expected)
                results.append({'case': name, 'replay': replay, 'requests': len(observed)})
                save(root / 'collector-events.json', events)
                print('PASS', name, 'restart' if replay else 'first call', len(observed), 'HTTP requests', flush=True)
        save(root / 'summary.json', {'build_id': args.expected_build, 'checks': len(results),
                                    'results': results, 'external_provider_contact': False,
                                    'required_early_uptime': args.require_early_uptime,
                                    'scope': 'Installed reporting functions and actual loopback HTTP; no scheduler/UI proof'})
    finally:
        save(root / 'collector-events.json', events)
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    return 0


if __name__ == '__main__':
    sys.exit(main())
