#!/usr/bin/env python3
"""Run-owned host sampler imported by build-owner.py; no background daemon."""
import json
import os
from pathlib import Path
import subprocess
import threading
import time


class Resources:
    def __init__(self, owner, config, roots):
        self.owner, self.config, self.roots = owner, config, roots
        self.stop = threading.Event()
        self.ready = threading.Event()
        self.failed = threading.Event()
        self.errors = []
        self.disk_process = None
        self.threads = []
        self.initial_allocated_total = None

    def fail(self, error):
        self.errors.append(type(error).__name__ + ': ' + str(error))
        self.failed.set()
        self.ready.set()

    def memory_loop(self):
        try:
            initial_oom = None
            with (self.owner / 'host-resources.jsonl').open('x') as stream:
                while not self.stop.is_set():
                    memory = {line.split(':')[0]: int(line.split()[1]) * 1024
                              for line in Path('/proc/meminfo').read_text().splitlines()
                              if line.split(':')[0] in ['MemTotal', 'MemAvailable', 'SwapTotal', 'SwapFree']}
                    vm = {k: int(v) for k, v in (line.split() for line in Path('/proc/vmstat').read_text().splitlines())
                          if k in ['pswpin', 'pswpout', 'pgmajfault', 'oom_kill']}
                    disk = os.statvfs('/workspace')
                    row = {'utc_epoch': time.time(), 'monotonic': time.monotonic(), 'memory_bytes': memory,
                           'vmstat_pages': vm, 'page_size': os.sysconf('SC_PAGE_SIZE'),
                           'pressure': {name: Path('/proc/pressure', name).read_text() for name in ['memory', 'io']},
                           'workspace_available_bytes': disk.f_bavail * disk.f_frsize}
                    stream.write(json.dumps(row) + '\n'); stream.flush()
                    if initial_oom is None:
                        initial_oom = vm['oom_kill']
                    assert vm['oom_kill'] == initial_oom, 'host OOM counter increased'
                    assert memory['MemAvailable'] >= self.config['minimum_host_available_bytes'], 'host RAM floor crossed'
                    assert memory['SwapTotal'] > 0 and memory['SwapFree'] >= memory['SwapTotal'] // 5, 'host swap floor crossed'
                    assert row['workspace_available_bytes'] >= self.config['minimum_volume_available_bytes'], 'disk floor crossed'
                    if self.stop.wait(5):
                        break
        except BaseException as error:
            self.fail(error)

    def disk_loop(self):
        try:
            with (self.owner / 'allocated-roots.jsonl').open('x') as stream:
                while True:
                    began = time.time()
                    rows = []
                    incomplete = False
                    for path in self.roots:
                        if not path.exists():
                            rows.append({'path': str(path), 'allocated_bytes': 0, 'exists': False})
                            continue
                        started = time.monotonic()
                        self.disk_process = subprocess.Popen(['du', '-s', '-x', '--block-size=1', '--', str(path)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=dict(os.environ, LC_ALL='C'))
                        while True:
                            try:
                                stdout, stderr = self.disk_process.communicate(timeout=1)
                                break
                            except subprocess.TimeoutExpired:
                                if self.stop.is_set():
                                    self.disk_process.terminate()
                                    try:
                                        stdout, stderr = self.disk_process.communicate(timeout=10)
                                    except subprocess.TimeoutExpired:
                                        self.disk_process.kill()
                                        stdout, stderr = self.disk_process.communicate(timeout=10)
                                    rows.append({'path': str(path), 'original_rc': self.disk_process.returncode,
                                                 'stderr': stderr, 'partial_stdout': stdout,
                                                 'elapsed_seconds': time.monotonic() - started})
                                    self.disk_process = None
                                    stream.write(json.dumps({'started_epoch': began, 'rows': rows,
                                         'interrupted_by_owner_completion': True, 'incomplete': True}) + '\n'); stream.flush()
                                    return
                                if time.monotonic() - started > self.config['disk_scan_timeout_seconds']:
                                    raise RuntimeError('allocation scan exceeded declared timeout')
                        rc = self.disk_process.returncode
                        self.disk_process = None
                        row = {'path': str(path), 'original_rc': rc, 'stderr': stderr,
                               'elapsed_seconds': time.monotonic() - started}
                        if rc == 0:
                            row['allocated_bytes'] = int(stdout.split()[0])
                        rows.append(row)
                        if rc:
                            missing_only = bool(stderr.strip()) and all(
                                line.startswith('du: ') and line.endswith(': No such file or directory')
                                for line in stderr.splitlines() if line.strip())
                            if missing_only and self.initial_allocated_total is not None:
                                row['expected_live_scan_enoent_race'] = True
                                row['partial_stdout'] = stdout
                                incomplete = True
                                continue
                            stream.write(json.dumps({'started_epoch': began, 'rows': rows, 'incomplete': True}) + '\n'); stream.flush()
                            raise RuntimeError('allocation measurement failed; original stderr retained')
                    stream.write(json.dumps({'started_epoch': began, 'finished_epoch': time.time(), 'rows': rows,
                                             'incomplete': incomplete,
                                             'peak_semantics': 'maximum observed allocated bytes, not continuous peak'}) + '\n'); stream.flush()
                    if not incomplete:
                        total = sum(row['allocated_bytes'] for row in rows)
                        if self.initial_allocated_total is None:
                            self.initial_allocated_total = total
                        assert total - self.initial_allocated_total <= self.config['maximum_incremental_allocated_bytes'], 'admitted incremental disk allowance crossed'
                    self.ready.set()
                    if self.stop.wait(self.config['disk_sample_interval_seconds']):
                        break
        except BaseException as error:
            process = self.disk_process
            if process is not None and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill(); process.wait(timeout=10)
            self.disk_process = None
            self.fail(error)

    def start(self):
        self.threads = [threading.Thread(target=f, name=name) for name, f in
                        [('host-metrics', self.memory_loop), ('allocated-roots', self.disk_loop)]]
        for thread in self.threads:
            thread.start()

    def finish(self):
        self.stop.set()
        for thread in self.threads:
            thread.join(timeout=30)
            if thread.is_alive():
                self.fail(RuntimeError('resource sampler did not exit'))
        # A final stable measurement is distinct from in-flight sampled peaks.
        # Skip extra filesystem work after a limit/observer failure.
        if not self.errors:
            final = {'started_epoch': time.time(), 'final_after_producer': True, 'rows': []}
            try:
                for path in self.roots:
                    if not path.exists():
                        final['rows'].append({'path': str(path), 'allocated_bytes': 0, 'exists': False})
                        continue
                    result = subprocess.run(['du', '-s', '-x', '--block-size=1', '--', str(path)],
                        capture_output=True, text=True, timeout=self.config['disk_scan_timeout_seconds'], env=dict(os.environ, LC_ALL='C'))
                    row = {'path': str(path), 'original_rc': result.returncode, 'stderr': result.stderr}
                    final['rows'].append(row)
                    if result.returncode:
                        raise RuntimeError('final allocation measurement failed')
                    row['allocated_bytes'] = int(result.stdout.split()[0])
                assert sum(row['allocated_bytes'] for row in final['rows']) - self.initial_allocated_total <= self.config['maximum_incremental_allocated_bytes'], 'final admitted disk allowance exceeded'
            except BaseException as error:
                final['incomplete'] = True
                self.fail(error)
            final['finished_epoch'] = time.time()
            with (self.owner / 'allocated-roots.jsonl').open('a') as stream:
                stream.write(json.dumps(final) + '\n')
        samples = [json.loads(line) for line in (self.owner / 'host-resources.jsonl').read_text().splitlines()] if (self.owner / 'host-resources.jsonl').exists() else []
        allocation = [json.loads(line) for line in (self.owner / 'allocated-roots.jsonl').read_text().splitlines()] if (self.owner / 'allocated-roots.jsonl').exists() else []
        if not samples or not any(not row.get('incomplete') for row in allocation):
            self.fail(RuntimeError('complete initial telemetry missing'))
        peaks = {}
        for sample in allocation:
            for row in sample['rows']:
                if 'allocated_bytes' in row:
                    peaks[row['path']] = max(peaks.get(row['path'], 0), row['allocated_bytes'])
        result = {'errors': self.errors, 'all_threads_exited': all(not t.is_alive() for t in self.threads),
                  'status': 'PASS' if not self.errors else 'FAIL', 'host_sample_count': len(samples),
                  'allocation_sample_count': len(allocation), 'maximum_observed_allocated_bytes_by_root': peaks,
                  'incomplete_disk_sample_count': sum(bool(s.get('incomplete')) for s in allocation),
                  'disk_peak_limit': 'sampled maxima with scan durations; not continuous or atomic peaks; maxima during incomplete samples are unknown'}
        if samples:
            result.update(minimum_host_mem_available_bytes=min(s['memory_bytes']['MemAvailable'] for s in samples),
                maximum_total_minus_available_bytes=max(s['memory_bytes']['MemTotal'] - s['memory_bytes']['MemAvailable'] for s in samples),
                minimum_swap_free_bytes=min(s['memory_bytes']['SwapFree'] for s in samples),
                swap_page_deltas={k: samples[-1]['vmstat_pages'][k] - samples[0]['vmstat_pages'][k] for k in ['pswpin', 'pswpout']})
        with (self.owner / 'resource-result.json').open('x') as stream:
            json.dump(result, stream, indent=2); stream.write('\n')
        return not self.errors
