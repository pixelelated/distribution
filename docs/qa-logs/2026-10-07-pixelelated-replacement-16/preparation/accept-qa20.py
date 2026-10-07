"""Reconcile completed QA20 artifacts; never accepts a live or partial run."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import statistics

root = Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
q = root / 'docs/qa-logs/2026-10-07-pixelelated-replacement-16'
retained = q / 'qa-20'
owner = Path('/workspace/tmp/pixelelated-m7-qa-20')
build = 'ee014909137e03706e0b3020b8396be589aaa705'
bundle = '7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a'
frozen = Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16')
dest = q / 'qa20-acceptance'
assert not dest.exists()

def read(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

completion = read(retained / 'owner-verification.json')
cleanup = read(retained / 'guest-cleanup-verification.json')
assert completion['result'] == 'PASS'
assert completion['channels'] == dict.fromkeys(
    ['inner.rc', 'outer.rc', 'tool-wrapper.rc', 'build.rc'], '0')
assert completion['sealed_inputs'] == 10 and len(completion['pids_absent']) == 4
assert cleanup['passed'] and cleanup['no_live_qemu'] and cleanup['no_live_owner_processes']
assert {9010, 9011, 10022, 10023, 5909, 5910} <= set(cleanup['unbound_tcp_ports'])
for name, wanted in read(retained / 'sha256.json').items():
    assert digest(retained / name) == wanted, name

reports = list((retained / 'artifacts/rocknix-images').glob('qa-*/report.md'))
assert len(reports) == 1
report = reports[0]
run = report.parent
text = report.read_text()
assert text.startswith('# vm-qa on ' + build[:10] + '\n') and bundle in text
suites = re.findall(r'^\| ([a-z-]+) \| (PASS|FAIL|SKIP) \| (\d+)s \| `([^`]+)` \|$', text, re.M)
expected = ['scripts', 'lifetime', 'wrapper', 'vocabulary', 'french', 'quoting',
            'menumap', 'register', 'pair-identity', 'fresh', 'round-trip', 'exit',
            'time-to-play', 'walks', 'frame-diff']
assert [s[0] for s in suites] == expected, suites
assert all(s[1] == 'PASS' and (run / s[3]).stat().st_size for s in suites)
assert '**PASSED** -- every suite that ran passed.' in text
for name in ['scripts', 'round-trip', 'exit']:
    assert (run / (name + '.log')).read_text().strip().endswith('PASSED'), name

walks = list((run / 'walks').rglob('*.png'))
assert len(walks) == 78
diff = (run / 'frame-diff.md').read_text()
assert '78 screens' in diff and '0 stale against another baseline' in diff
assert re.search(r'\*\*PASS\*\* -- \d+ box\(es\) claimed, 0 unclaimed, 0 screen\(s\) missing\.', diff)
walk_review = read(root / '.build-runs/qa20-walk-frame-review.json')
assert {'back-up-page/02-back-up-page.png', 'restore-page/02-restore-page.png',
        'to-change-cloud-folder/03-folder-editor.png'} <= {row['file'] for row in walk_review}
for row in walk_review:
    assert row['result'] == 'PASS' and row['primary_direct_review']
    assert digest(run / 'walks' / row['file']) == row['sha256']
timing = read(run / 'time-to-play/time-to-play.json')
assert timing['build'] == build[:10] and timing['backend'] == 'webdav'
assert timing['rom_seeded'] and timing['interface_rebooted']
cells = timing['cells']
assert set(cells) == {'launch', 'exit', 'g2g'}, set(cells)
for key, field in [('launch', 't_first_game_frame'), ('exit', 't_sync_stamp'), ('g2g', 't_second_game_frame')]:
    assert cells[key] and all(isinstance(row[field], (float, int)) and row[field] > 0 for row in cells[key]), (key, field)
assert all(row['stamp']['rc'] == '0' and row['stamp']['token'] == 'completed' for row in cells['exit'])
assert statistics.median(row['t_sync_stamp'] for row in cells['exit']) <= 3
timing_review = read(root / '.build-runs/qa20-timing-frame-review.json')
assert timing_review['result'] == 'PASS' and len(timing_review['frames']) == 6
for row in timing_review['frames']:
    assert row['primary_direct_review'] and row['dimensions'] == [1280, 800]
    assert digest(run / 'time-to-play' / row['file']) == row['sha256']

payloads = {}
proxy = {}
artifact = retained / 'artifacts'
expected_scripts = {
    'cloud_migrate_layout': '0e4ccebde159006acb6313027e33b363b177eff2b62db2bacc93fea05396b2c1',
    'cloud_content_restore': '3b28fd1403657d713f92f216840a52ff7e692bf09746a7ccb8c2519c6940d2f8',
    'cloud_setup': '44f0c93b5eb1380fd237fe9a3fbbd604bb8b60181923a6f3e78c0dffa501fc3f',
    'cloud_scan': 'a4830b23e7d3df7d86cba7867ccaaca583ea8881e90a4c5d3988671d79b20aa1',
}
for phase in ['initial-clean', 'clean', 'upgrade', 'upgrade-software']:
    data = read(artifact / ('payload-' + phase + '.json'))
    assert data['phase'] == phase and data['build_id'] == build
    assert data['passed'] and data['os_name'] == 'pixelelated'
    files = data['files']
    assert files['running_emulationstation']['exe'] == '/usr/bin/emulationstation'
    assert files['running_emulationstation']['OS_NAME'] == 'pixelelated'
    for name, wanted in expected_scripts.items():
        assert files['/usr/bin/' + name] == {'sha256': wanted, 'mode': '755'}
        assert digest(frozen / 'projects/ROCKNIX/packages/network/rclone/sources' / name) == wanted
    payloads[phase] = {name: value for name, value in files.items() if name != 'running_emulationstation'}
    identity = read(artifact / ('proxy-identity-' + phase + '.json'))
    assert identity['passed'] and identity['actual_os_recognized']
    assert [case['recognized'] for case in identity['cases']] == [True, True, False, False, False]
    proxy[phase] = identity
assert all(value == payloads['initial-clean'] for value in payloads.values())

renderers = {}
for phase, mode in [('initial-clean', 'virgl'), ('upgrade-virgl', 'virgl'), ('upgrade-software', 'software')]:
    data = read(artifact / ('renderer-' + phase + '.json'))
    assert data['passed'] and data['mode'] == mode
    env = data['process']['graphics_env']
    if mode == 'software':
        assert data['negotiated_features'][0] == '0' and env['WLR_RENDERER'] == 'pixman'
        assert 'Creating pixman renderer' in data['sway_log']
    else:
        assert data['negotiated_features'][0] == '1' and 'WLR_RENDERER' not in env
        assert 'Creating GLES2 renderer' in data['sway_log'] and 'virgl' in data['sway_log']
    renderers[phase] = data['files']
assert all(files == renderers['initial-clean'] for files in renderers.values())

frames = read(root / '.build-runs/qa20-identity-frame-review.json')
assert len(frames) == 15 and len({row['file'] for row in frames}) == 15
for row in frames:
    assert row['result'] == 'PASS' and row['primary_direct_review']
    assert digest(artifact / row['file']) == row['sha256']
    assert row['dimensions'] == ([640, 480] if row['phase'] == 'upgrade-software' else [1280, 800])
assert {phase: sum(row['phase'] == phase for row in frames) for phase in ['initial-clean', 'upgrade', 'upgrade-software']} == dict.fromkeys(['initial-clean', 'upgrade', 'upgrade-software'], 5)

# Bind the rehearsal to the exact path emitted by this run, not a wildcard's newest match.
console = (retained / 'console.log').read_text()
paths = re.findall(r'^(/workspace/artifacts/rocknix-images/qa-ee01490913-upgrade-from-69e6039f8f-\d{8}-\d{4})$', console, re.M)
assert len(paths) == 1, paths
upgrade = Path(paths[0])
assert (upgrade / 'rc').read_text().strip() == '0'
log = (upgrade / 'rehearsal.log').read_text()
assert 'old build id: 69e6039f8fdbf971d3e6b694537f250036fdcd98' in log
assert re.search(r'^=== \d\d:\d\d:\d\d RESULT PASS$', log, re.M)
assert not re.search(r'^FAIL ', log, re.M)
checks = re.findall(r'^PASS (.+)$', log, re.M)
assert len(checks) == 26 and len(set(checks)) == 26
for required in ['four seeded files exist', 'new build id is ee01490913',
                 'saves and save states byte-identical', 'marker file kept', 'setting kept',
                 'rclone remote kept', 'rclone (new) lists the remote', 'saves remote kept',
                 'cloud conf gained the new defaults, kept the old values', 'backup archive kept',
                 'update queue empty']:
    assert required in checks, required
state = (upgrade / 'state-after.txt').read_text()
assert build in state and 'OS_NAME="pixelelated"' in state
assert (upgrade / 'journal-err-after.txt').is_file()

dest.mkdir()
shutil.copytree(upgrade, dest / 'actual-rc2-upgrade')
shutil.copy2(root / '.build-runs/qa20-identity-frame-review.json', dest / 'identity-frame-review.json')
shutil.copy2(root / '.build-runs/qa20-timing-frame-review.json', dest / 'timing-frame-review.json')
shutil.copy2(root / '.build-runs/qa20-walk-frame-review.json', dest / 'walk-frame-review.json')
result = dict(verified_utc=datetime.now(timezone.utc).isoformat(), result='PASS',
              owner=str(owner), build_id=build, bundle=bundle,
              report=str(report.relative_to(root)), suites=suites, walk_frames=len(walks),
              visual_differences='0 unclaimed; 0 missing; 0 stale claims',
              identity_direct_frames=len(frames), payload_profiles=list(payloads),
              renderer_profiles={p: 'software' if p.endswith('software') else 'virgl' for p in renderers},
              installed_payload_unchanged=True, installed_proxy_identity_profiles=list(proxy),
              actual_upgrade_source=str(upgrade), upgrade_assertions=checks,
              timings_seconds={key: statistics.median(row[field] for row in cells[key]) for key, field in [('launch','t_first_game_frame'), ('exit','t_sync_stamp'), ('g2g','t_second_game_frame')]},
              lifecycle=dict(channels=completion['channels'], sealed_inputs=10, actual_cleanup=cleanup['passed']),
              scope='Full default clean-install qualification and actual RC2 upgrade; local three-protocol renewal is separate.')
(dest / 'acceptance.json').write_text(json.dumps(result, indent=2) + '\n')
(dest / 'sha256.json').write_text(json.dumps({str(p.relative_to(dest)): digest(p) for p in sorted(dest.rglob('*')) if p.is_file()}, indent=2) + '\n')
print(json.dumps(result, indent=2))
