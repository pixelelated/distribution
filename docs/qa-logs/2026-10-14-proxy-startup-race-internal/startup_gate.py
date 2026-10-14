"""UNRUN fixture-only scheduling barrier for the accepted actual-service observer.

Only an armed fresh synthetic-storage process pauses. No product timer, probe,
queue, HTTP response, worker body or signal handler is replaced.
"""
import json
import os
from pathlib import Path
import threading
import time


class StartupGate:
    def __init__(self, state, emit):
        self.state = Path(state)
        self.emit = emit
        armed = self.state / 'startup-window-armed.json'
        self.control = json.loads(armed.read_text()) if armed.exists() else None
        if self.control is not None:
            assert self.control == {'schema': 1, 'nonce': 'fresh-synthetic-startup-window'}
        self.main_online = None
        self.used = False

    def observe(self, frame, event, result):
        if self.control is None or frame.f_code.co_name != 'refresh_reachability':
            return
        if threading.current_thread() is threading.main_thread() and event == 'return':
            assert self.main_online is None, 'unexpected second main startup probe'
            self.main_online = result
            self.emit('startup-main-probe-return', result=repr(result))
            return
        worker = threading.current_thread()
        if type(worker).__name__ != 'ConnectivityMonitor' or event != 'call' or self.used:
            return
        self.used = True
        assert self.main_online is False, 'startup probe was not observed offline'
        assert frame.f_locals['force_probe'] is True
        identity = {'pid': os.getpid(), 'nonce': self.control['nonce']}
        marker = self.state / 'startup-window-blocked.json'
        assert not marker.exists(), 'stale scheduling marker'
        temporary = marker.with_suffix('.tmp')
        temporary.write_text(json.dumps(identity) + '\n')
        os.replace(temporary, marker)
        self.emit('startup-monitor-held', **identity, bound_seconds=10)
        release = self.state / 'startup-window-release.json'
        deadline = time.monotonic() + 10
        while not release.exists():
            assert time.monotonic() < deadline, 'controller did not release startup scheduling barrier'
            if worker.stop_event.wait(0.05):
                self.emit('startup-monitor-released-on-stop', **identity)
                return
        assert json.loads(release.read_text()) == identity, 'release names wrong service process'
        self.emit('startup-monitor-released', **identity)
