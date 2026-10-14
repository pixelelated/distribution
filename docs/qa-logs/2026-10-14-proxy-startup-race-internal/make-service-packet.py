#!/usr/bin/env python3
"""UNRUN runtime adapter; materialize a fresh derivative, never launch it.

Input must be the losslessly restored accepted execution packet. Output preserves
its owner, cgroup limits, systemd unit, original result handling and cleanup.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def replace_once(text, before, after):
    assert text.count(before) == 1, repr(before[:80])
    return text.replace(before, after)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execution-packet', required=True, type=Path)
    parser.add_argument('--destination', required=True, type=Path)
    parser.add_argument('--variant', required=True, choices=('baseline', 'candidate'))
    args = parser.parse_args()
    source = args.execution_packet.resolve(strict=True)
    dest = args.destination.absolute()
    binding = json.loads((HERE / 'bindings.json').read_text())
    expected = json.loads((HERE / 'service-inputs.json').read_text())
    manifest_raw = (source / 'SHA256SUMS').read_bytes()
    assert sha(manifest_raw) == expected['execution_manifest_sha256']
    files = {}
    for line in manifest_raw.decode().splitlines():
        digest, name = line.split('  ', 1)
        assert not Path(name).is_absolute() and '..' not in Path(name).parts
        raw = (source / name).read_bytes()
        assert sha(raw) == digest, name
        files[name] = raw
    assert {str(p.relative_to(source)) for p in source.rglob('*') if p.is_file()} == set(files) | {'SHA256SUMS'}
    for name, digest in expected['modified_inputs'].items():
        assert sha(files[name]) == digest, name

    observer = files['bootstrap/sitecustomize.py'].decode()
    observer = replace_once(observer, '    def profile(frame, event, arg):\n',
        '    from startup_gate import StartupGate\n'
        '    startup_gate = StartupGate(state, emit)\n\n'
        '    def profile(frame, event, arg):\n')
    observer = replace_once(observer, "        obj = frame.f_locals.get('self')\n",
        "        startup_gate.observe(frame, event, arg)\n"
        "        obj = frame.f_locals.get('self')\n")
    files['bootstrap/sitecustomize.py'] = observer.encode()
    files['bootstrap/startup_gate.py'] = (HERE / 'startup_gate.py').read_bytes()

    runner = files['run.py'].decode()
    begin = runner.index("        action('start')\n        second = until(lambda: active(first)")
    end = runner.index("        REF.stop(peer)\n        peer = None\n", begin)
    causal = '''        # #588: only this fresh startup is armed; first run created a real signed row.
        dump(STATE / 'startup-window-armed.json',
             {'schema': 1, 'nonce': 'fresh-synthetic-startup-window'})
        action('start')
        fourth = until(lambda: active(first), 5, 'startup-window actual service not active')
        def held():
            marker = STATE / 'startup-window-blocked.json'
            if not marker.exists():
                return None
            value = json.loads(marker.read_text())
            need(value == {'pid': fourth, 'nonce': 'fresh-synthetic-startup-window'}, 'wrong held service')
            return value
        release_identity = until(held, 5, 'initial monitor probe never held')
        need(rows() == queued, 'startup false probe changed signed queue')
        need(any(r.get('kind') == 'startup-main-probe-return' and r.get('result') == 'False'
                 for r in events(fourth)), 'actual main false return not observed')
        # No request to the proxy between its main false result and the held worker probe.
        state = REF.ProtocolState('e5880000000000000000000000000001')
        state.secret = (STATE / 'award_secret.key').read_bytes()
        state.queued = {104: copy.deepcopy(queued[0])}
        peer = REF.upstream(state)
        # Listener creation has returned before release; actual probe/HTTP remain untouched.
        dump(OUT / 'peer-open-before-release.json',
             {'pid': os.getpid(), 'monotonic': time.monotonic(), 'endpoint': ['127.0.0.1', 18081]})
        temporary = STATE / 'startup-window-release.tmp'
        dump(temporary, release_identity)
        os.replace(temporary, STATE / 'startup-window-release.json')
        worker_start(fourth)
        def online_probes():
            return [r for r in events(fourth) if r.get('function') == 'refresh_reachability'
                    and r.get('event') == 'return' and r.get('thread') != 'MainThread'
                    and r.get('result') == 'True']
        # Initial and next natural 15s monitor probe; no cadence override or extra reconnect.
        until(lambda: len(online_probes()) >= 2, 25, 'two natural online monitor observations absent')
        observed = events(fourth)
        flush_calls = [r for r in observed if r.get('class') == 'ProxyRuntimeServer'
                       and r.get('function') == 'flush_pending_awards' and r.get('event') == 'call']
        remaining = rows()
        REPORT['startup_window'] = {'initial_main_online': False,
            'online_monitor_probes': online_probes(), 'flush_calls': flush_calls,
            'queue_before': queued, 'queue_after': remaining,
            'applied': state.applied, 'peer_errors': state.thread_errors,
            'baseline_failure_signature': bool(not flush_calls and remaining == queued and not state.applied)}
        startup_pass = len(flush_calls) == 1 and not remaining and state.applied == [(REF.USER_A, 104)]
        need(not state.thread_errors, 'synthetic peer errors')
        need(int(properties()['NRestarts']) == 0, 'unexpected automatic restart')
        REPORT['steps'].append('controlled actual main false to first monitor true; observed natural next 15s probe')
'''
    runner = runner[:begin] + causal + runner[end:]
    runner = replace_once(runner, "        REPORT['status'] = 'PASS'\n",
        "        need(startup_pass, 'startup-window queued signed award was not applied exactly once')\n"
        "        REPORT['status'] = 'PASS'\n")
    files['run.py'] = runner.encode()
    service_binding = json.loads(files['bindings.json'])
    service_binding['prepared_python_manifest'][binding['path']] = binding[args.variant + '_sha256']
    # source.json remains the immutable preparation provenance; manifest separately
    # binds the one post-preparation repair. Do not manufacture a new provenance flag.
    service_binding['startup_repair'] = {'variant': args.variant,
        'baseline_sha256': binding['baseline_sha256'], 'candidate_sha256': binding['candidate_sha256'],
        'scope': 'controlled startup only; installed/native/final-image acceptance separate'}
    files['bindings.json'] = (json.dumps(service_binding, indent=2) + '\n').encode()
    seal = json.loads(files['runner-seal.json'])
    for name in seal:
        if name in files:
            seal[name] = sha(files[name])
    files['runner-seal.json'] = (json.dumps(seal, indent=2) + '\n').encode()
    for name, raw in files.items():
        if name.endswith('.py'):
            ast.parse(raw, filename=name)
    assert not dest.exists() and not dest.is_symlink()
    assert any(dest.is_relative_to(p) for p in (Path('/tmp'), Path('/workspace/tmp')))
    dest.mkdir(parents=True, mode=0o700)
    for name, raw in files.items():
        path = dest / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    # The earlier execution materializer preserves bytes, not executable mode.
    (dest / 'raofflineproxy-ctl').chmod(0o755)
    manifest = ''.join(sha(raw) + '  ' + name + '\n' for name, raw in sorted(files.items()))
    (dest / 'SHA256SUMS').write_text(manifest)
    print(json.dumps({'status': 'PREPARED_ONLY_UNRUN', 'variant': args.variant,
                      'execution_manifest_sha256': sha(manifest.encode()), 'files': len(files),
                      'destination': str(dest), 'runtime': False}, indent=2))


if __name__ == '__main__':
    main()
