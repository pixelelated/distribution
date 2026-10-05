#!/usr/bin/env python3
"""Actual watcher plus deterministic counter controls; no build/VM mutation."""
from pathlib import Path
import datetime, hashlib, importlib.util, json, os, signal, subprocess, sys, tempfile, time
root = Path.cwd()
out = Path(sys.argv[1]).resolve()
out.mkdir()
source = Path(__file__).with_name('observe-checksum.py')
spec = importlib.util.spec_from_file_location('checksum_observer', source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
activity = out / 'copy-artifacts'
activity.mkdir()
log = out / 'job.log'
log.write_text('controlled job: main log intentionally old\n')
os.utime(log, (time.time() - 180, time.time() - 180))
status = out / 'status.txt'
(activity / 'checksum-progress.json').write_text('{"fixture":"fresh JSON is deliberately not a watched log"}\n')
job = subprocess.Popen(['sleep', '60'], start_new_session=True)
(out / 'job.pid').write_text(str(job.pid) + '\n')
watch = None
checks = []

def wait_for(state):
    for unused in range(60):
        text = status.read_text() if status.exists() else ''
        if text.startswith('state:       ' + state + '\n'):
            return text
        time.sleep(.1)
    raise AssertionError((state, text))

def sample(count, start=10):
    return [{'pid': 123, 'start_ticks': start, 'io': {'rchar': count}}]

try:
    with (out / 'watcher-console.log').open('w') as console:
        watch = subprocess.Popen(['bash', str(root / 'tools/watch-job'), '--log', str(log),
            '--rc', str(out / 'job.rc'), '--pid', str(job.pid), '--status', str(status),
            '--activity-dir', str(activity), '--interval', '1', '--stall-min', '1'],
            stdout=console, stderr=subprocess.STDOUT, start_new_session=True)
        (out / 'watcher.pid').write_text(str(watch.pid) + '\n')
        (out / 'json-only-status.txt').write_text(wait_for('stalled'))
        checks.append('JSON-only receipt reproduces stalled despite alive job')
        assert module.record_snapshot(out, sample(100))['total_delta'] == 0
        progress_log = activity / 'checksum-progress.log'
        assert not progress_log.exists()
        checks.append('first observation creates no activity log')
        result = module.record_snapshot(out, sample(120))
        assert result['total_delta'] == 20
        text = wait_for('running')
        assert 'activity:    ' + str(progress_log) in text
        (out / 'corrected-status.txt').write_text(text)
        checks.append('actual watcher identifies corrected .log and reports running')
        before = (progress_log.stat().st_mtime_ns, progress_log.read_bytes())
        assert module.record_snapshot(out, sample(120))['total_delta'] == 0
        assert (progress_log.stat().st_mtime_ns, progress_log.read_bytes()) == before
        checks.append('unchanged counters do not refresh log or content')
        assert module.record_snapshot(out, sample(900, start=20))['total_delta'] == 0
        assert (progress_log.stat().st_mtime_ns, progress_log.read_bytes()) == before
        checks.append('reused PID with new start identity creates no activity')
        assert module.record_snapshot(out, sample(800, start=20))['total_delta'] == 0
        assert (progress_log.stat().st_mtime_ns, progress_log.read_bytes()) == before
        checks.append('counter regression creates no activity')
finally:
    for process in [watch, job]:
        if process is not None and process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=5)
    cleanup = [{'pid': p.pid, 'returncode': p.returncode,
                'absent': not (Path('/proc') / str(p.pid)).exists()} for p in [watch, job] if p]
    assert all(row['absent'] for row in cleanup)
    (out / 'cleanup.json').write_text(json.dumps(cleanup, indent=2) + '\n')
report = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'passed': True,
          'scope': 'Host-only isolated controls, synthetic counters; not a new real-copy acceptance',
          'adapter_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
          'watcher_sha256': hashlib.sha256((root / 'tools/watch-job').read_bytes()).hexdigest(),
          'checks': checks, 'cleanup': cleanup}
(out / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
