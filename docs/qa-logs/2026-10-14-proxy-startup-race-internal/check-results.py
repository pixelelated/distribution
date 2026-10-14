#!/usr/bin/env python3
"""Check separately retained original fixture exits; do not rewrite their results."""
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--kind', choices=('component', 'service'), required=True)
p.add_argument('--baseline-result', type=Path, required=True)
p.add_argument('--baseline-rc', type=Path, required=True)
p.add_argument('--candidate-result', type=Path, required=True)
p.add_argument('--candidate-rc', type=Path, required=True)
a = p.parse_args()
b = json.loads(a.baseline_result.read_text())
c = json.loads(a.candidate_result.read_text())
assert int(a.baseline_rc.read_text()) == 1, 'original baseline must fail its behavior assertion'
assert int(a.candidate_rc.read_text()) == 0, 'original candidate must pass'
assert b['status'] == 'FAIL' and c['status'] == 'PASS'
if a.kind == 'component':
    assert b['variant'] == 'baseline' and c['variant'] == 'candidate'
    assert not b['live_threads'] and not c['live_threads']
    assert not b['thread_errors'] and not c['thread_errors']
    assert len(b['cases']) == 1 and b['cases'][0]['name'] == 'startup-window'
    row = b['cases'][0]
    assert row['baseline_failure_signature'] == 'startup false; initial/periodic monitor true; zero flush; exact signed row retained'
    assert row['queue_before'] == row['queue_after'] and row['flush_calls'] == 0 and not row['applied']
    assert [r['result'] for r in row['trace'] if r['event'] == 'probe-return'] == [False, True, True]
    assert b['error'] == 'AssertionError: queued signed award not applied exactly once'
    assert {r['name'] for r in c['cases']} == {
        'startup-window', 'already-online', 'persistent-offline', 'ordinary-reconnect',
        'auth-401', 'auth-403', 'network-500', 'stop-during-initial-probe',
        'stop-before-start', 'offline-stop-restart'}
    assert all(r['status'] == 'PASS' and r['sqlite_integrity'] == 'ok' for r in c['cases'])
    assert all(r['storage_closed'] and not r['worker_alive_at_storage_close']
               for result in (b, c) for r in result['cases'])
else:
    assert not b['cleanup_errors'] and not c['cleanup_errors']
    assert b['startup_window']['baseline_failure_signature'] is True
    assert b['startup_window']['queue_before'] == b['startup_window']['queue_after']
    assert not b['startup_window']['flush_calls'] and not b['startup_window']['applied']
    assert b['error'] == 'AssertionError: startup-window queued signed award was not applied exactly once'
    assert len(c['startup_window']['flush_calls']) == 1
    assert c['startup_window']['applied'] == [['fixture-a', 104]] and not c['startup_window']['queue_after']
    for result in (b, c):
        assert len(result['startup_window']['online_monitor_probes']) >= 2
        assert not result['startup_window']['peer_errors']
        stopped = result['last_stopped_properties']
        assert stopped['ExecMainCode'] == '1' and stopped['ExecMainStatus'] == '0' and stopped['Result'] == 'success'
print(json.dumps({'status': 'PASS', 'kind': a.kind, 'baseline_original_exit': 1,
                  'candidate_original_exit': 0, 'source_component_is_service_acceptance': False,
                  'remaining': 'coordinator original-owner/host-exit/installed composed-image evidence'}))
