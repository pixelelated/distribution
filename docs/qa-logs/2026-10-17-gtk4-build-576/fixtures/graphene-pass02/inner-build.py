#!/usr/bin/env python3
"""Run inside one canonical builder; retain original make rc and final cgroup facts."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import time


def counters(path):
    return {k: int(v) for k, v in (line.split() for line in path.read_text().splitlines())}


def observe():
    root = Path('/sys/fs/cgroup')
    return {'monotonic': time.monotonic(), 'memory_current': int((root / 'memory.current').read_text()),
            'memory_peak': int((root / 'memory.peak').read_text()),
            'memory_max': (root / 'memory.max').read_text().strip(),
            'memory_swap_max': (root / 'memory.swap.max').read_text().strip(),
            'memory_events': counters(root / 'memory.events'),
            'memory_pressure': (root / 'memory.pressure').read_text(),
            'io_pressure': (root / 'io.pressure').read_text(),
            'io_stat': (root / 'io.stat').read_text()}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stage', required=True)
    p.add_argument('--cpus', type=int, required=True)
    p.add_argument('--memory-bytes', type=int, required=True)
    p.add_argument('command', nargs=argparse.REMAINDER)
    a = p.parse_args()
    command = a.command[1:] if a.command[:1] == ['--'] else a.command
    assert command
    output = Path('/build-owner/stages') / a.stage
    result = {'stage': a.stage, 'original_command_rc': None, 'wrapper_rc': 125}
    child = None
    signalled = []
    def interrupt(number, _frame):
        signalled.append(number)
        if child is not None and child.poll() is None:
            os.killpg(child.pid, number)
    for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGHUP]:
        signal.signal(sig, interrupt)
    try:
        assert os.getuid() != 0
        assert os.environ['TMPDIR'] == '/tmp'
        assert os.environ['RASTERATOPS_BUILD_RUN'].startswith('.build-runs/')
        assert len(os.sched_getaffinity(0)) == a.cpus
        nproc = int(subprocess.check_output(['nproc'], text=True))
        assert nproc == a.cpus
        fd, path = tempfile.mkstemp(dir=os.environ['TMPDIR'])
        os.close(fd)
        Path(path).unlink()
        before = observe()
        result.update(uid=os.getuid(), gid=os.getgid(), visible_cpus=a.cpus, nproc=nproc,
                      effective_tmpdir='/tmp', actual_mktemp=True, before=before)
        assert before['memory_max'] == str(a.memory_bytes)
        assert before['memory_swap_max'] == '0'
        nonce = os.urandom(16).hex()
        ready = output / 'inner-ready.json'
        temporary = output / 'inner-ready.tmp'
        temporary.write_text(json.dumps({'stage': a.stage, 'nonce': nonce, 'pid': os.getpid()}) + '\n')
        temporary.replace(ready)
        deadline = time.monotonic() + 30
        acknowledgment = output / 'host-observed.json'
        while not acknowledgment.exists():
            assert not signalled, 'interrupted before host observation'
            assert time.monotonic() < deadline, 'host observation handshake expired'
            time.sleep(.1)
        ack = json.loads(acknowledgment.read_text())
        assert ack['stage'] == a.stage and ack['nonce'] == nonce
        assert len(ack['container_id']) == 64
        assert ack['container_id'].startswith(Path('/etc/hostname').read_text().strip())
        result['host_observation_handshake'] = ack
        with (output / 'cgroup.jsonl').open('x') as samples:
            samples.write(json.dumps(before) + '\n'); samples.flush()
            child = subprocess.Popen(command, start_new_session=True)
            result['child_pid'] = child.pid
            result['started_monotonic'] = time.monotonic()
            while child.poll() is None:
                time.sleep(1)
                if int(time.monotonic() - result['started_monotonic']) % 5 == 0:
                    samples.write(json.dumps(observe()) + '\n'); samples.flush()
            result['original_command_rc'] = child.wait()
            after = observe()
            samples.write(json.dumps(after) + '\n'); samples.flush()
        result['after'] = after
        result['elapsed_seconds'] = time.monotonic() - result['started_monotonic']
        result['signals'] = signalled
        assert not signalled
        assert all(after['memory_events'].get(k, 0) == before['memory_events'].get(k, 0)
                   for k in ['oom', 'oom_kill', 'oom_group_kill'])
        result['wrapper_rc'] = result['original_command_rc'] if result['original_command_rc'] >= 0 else 128 - result['original_command_rc']
    except BaseException as error:
        result['error'] = type(error).__name__ + ': ' + str(error)
        if child is not None:
            if child.poll() is None:
                os.killpg(child.pid, signal.SIGTERM)
                try:
                    child.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait(timeout=10)
            result['original_command_rc'] = child.returncode
    finally:
        with (output / 'inner-result.json').open('x') as stream:
            json.dump(result, stream, indent=2); stream.write('\n')
    print(json.dumps({'stage': a.stage, 'original_command_rc': result['original_command_rc'],
                      'wrapper_rc': result['wrapper_rc']}), flush=True)
    return result['wrapper_rc']


if __name__ == '__main__':
    raise SystemExit(main())
