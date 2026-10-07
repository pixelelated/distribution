"""Reconcile three completed protocol runs and their actual backend identities."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

root = Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
q = root / 'docs/qa-logs/2026-10-07-pixelelated-replacement-16'
retained = q / 'cloud-02'
observations = q / 'cloud02-runtime-observation'
dest = q / 'cloud02-acceptance'
assert not dest.exists()
read = lambda p: json.loads(p.read_text())
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
completion = read(retained / 'owner-verification.json')
cleanup = read(retained / 'guest-cleanup-verification.json')
assert completion['result'] == 'PASS'
assert set(completion['channels'].values()) == {'0'} and len(completion['channels']) == 4
assert completion['sealed_inputs'] == 6 and len(completion['pids_absent']) == 4
assert cleanup['passed'] and cleanup['no_live_qemu'] and cleanup['no_live_owner_processes']
assert {9010, 9011, 9012, 9013, 9022, 10022, 10023, 5909, 5910} <= set(cleanup['unbound_tcp_ports'])
assert read(observations / 'cleanup.json')['result'] == 'PASS'
for path, wanted in read(retained / 'sha256.json').items():
    assert digest(retained / path) == wanted, path

reports = list((retained / 'artifacts/rocknix-images').glob('qa-*/report.md'))
assert len(reports) == 3
by_backend = {}
required_assertions = [
    'all 9 files restored byte-identical',
    'the settings backup archive reached the cloud',
    'restore brought back this device\'s newest, not the other device\'s newer archive',
    'all 3 content files reached the cloud',
    'all 3 content files restored byte-identical',
    'a newer local gamelist survived the restore',
]
for report in reports:
    text = report.read_text()
    assert text.startswith('# vm-qa on ee01490913\n')
    backend = re.search(r', cloud (webdav|sftp|s3) \(port ', text).group(1)
    assert backend not in by_backend
    assert re.findall(r'^\| ([a-z-]+) \| (PASS|FAIL|SKIP) \| (\d+)s \| `([^`]+)` \|$', text, re.M) == [
        ('round-trip', 'PASS', re.search(r'^\| round-trip \| PASS \| (\d+)s', text, re.M).group(1), 'round-trip.log')]
    assert '**PASSED** -- every suite that ran passed.' in text
    raw = report.parent / 'round-trip.log'
    lines = raw.read_text().splitlines()
    assertions = [line.strip().removeprefix('PASS  ') for line in lines if line.lstrip().startswith('PASS ')]
    assert len(assertions) == 106
    assert not any(line.lstrip().startswith(('FAIL ', 'SKIP ')) for line in lines)
    assert lines[-1] == 'PASSED'
    for label in required_assertions:
        assert label in assertions, (backend, label)
    live = read(observations / (backend + '-live.json'))
    assert live['backend'] == backend and live['result'] == 'LIVE'
    assert live['port_accepting'] == {'webdav': 9010, 'sftp': 9013, 's3': 9012}[backend]
    assert live['secret_values_recorded'] is False
    if backend == 's3':
        assert live['container']['running'] and live['container']['pid'] == live['process']['pid']
        assert live['container']['image_id'] == live['image']['id']
    else:
        assert live['process']['owned_path_in_arguments']
    by_backend[backend] = dict(assertions=106, failures=0, skips=0,
                              report=str(report.relative_to(root)), raw_log_sha256=digest(raw),
                              backend_observed_utc=live['observed_utc'])
assert set(by_backend) == {'webdav', 'sftp', 's3'}

rclone = (retained / 'artifacts/installed-rclone.txt').read_text()
assert rclone.startswith('rclone v1.75.1\n')
actual = re.search(r'^([a-f0-9]{64})\s+/usr/bin/rclone$', rclone, re.M).group(1)
assert actual == digest(Path('/workspace/tmp/pixelelated-m7-image-16/root/usr/bin/rclone'))
payload = read(retained / 'artifacts/payload-local-cloud.json')
assert payload['passed'] and payload['build_id'] == 'ee014909137e03706e0b3020b8396be589aaa705'
console = (retained / 'console.log').read_text()
assert 'PASS all three local cloud round-trip suites on frozen replacement16' in console
for backend in by_backend:
    assert 'PASS backend suite ' + backend in console
    assert 'BEGIN local cloud backend ' + backend in console
    assert 'END local cloud backend ' + backend in console

result = dict(verified_utc=datetime.now(timezone.utc).isoformat(), result='PASS',
              build_id=payload['build_id'], total_assertions=318, backends=by_backend,
              installed_rclone_version='v1.75.1', installed_rclone_sha256=actual,
              lifecycle=dict(channels=completion['channels'], sealed_inputs=6, actual_cleanup=True),
              backend_observation_directory=str(observations.relative_to(root)),
              scope='Installed scripts and actual local WebDAV, SFTP, and MinIO S3 backends. No hosted provider account or Dropbox OAuth result is claimed.')
dest.mkdir()
(dest / 'acceptance.json').write_text(json.dumps(result, indent=2) + '\n')
(dest / 'verify.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(result, indent=2))
