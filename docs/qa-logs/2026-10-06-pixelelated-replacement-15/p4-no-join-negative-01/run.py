"""Genuine retained pre-join image, updated and fresh guests on one local cloud."""
from pathlib import Path
import datetime, hashlib, json, os, shlex, socket, subprocess, time

owner = Path(__file__).resolve().parent
tree = Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15')
out = owner / 'artifacts'
vp = str(tree / 'tools/vm-pair')
be = str(tree / 'tools/cloud-test-backend')
old = Path('/workspace/artifacts/rocknix-images/x64-all-20260929-69e6039f8f/ROCKNIX-GENERIC_X64.x86_64-20260929.img.gz')
new = Path('/workspace/artifacts/rocknix-images/x64-all-20261001-1acdaf2cce/ROCKNIX-GENERIC_X64.x86_64-20261001.img.gz')
tar = new.with_name('ROCKNIX-GENERIC_X64.x86_64-20261001.tar')
expected = json.loads((owner / 'expected-scripts.json').read_text())
rows = []
pair_started = backend_started = False


def check(ok, text):
    rows.append({'assertion': text, 'passed': bool(ok)})
    (out / 'assertions.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(('PASS ' if ok else 'FAIL ') + text, flush=True)
    assert ok, text


def run(args, label, timeout=600, allowed=(0,)):
    r = subprocess.run(args, text=True, capture_output=True, timeout=timeout)
    (out / (label + '.log')).write_text(r.stdout + r.stderr)
    if allowed is not None:
        check(r.returncode in allowed, label + ' exit ' + str(r.returncode))
    return r


def guest(g, command, allowed=(0,), timeout=120, data=None):
    r = subprocess.run([vp, 'ssh', g, '. /etc/profile >/dev/null 2>&1; ' + command],
                       text=True, input=data, capture_output=True, timeout=timeout)
    if allowed is not None:
        assert r.returncode in allowed, (g, command, r.returncode, r.stdout, r.stderr)
    return r


def state(g):
    return guest(g, "grep -E '^(SAVES|SETTINGS|CONTENT)_REMOTE=' /storage/.config/cloud_sync.conf").stdout


def files():
    data = owner / 'cloud/data'
    return {str(p.relative_to(data)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(data.rglob('*')) if p.is_file()}


def identity(g, label, commit):
    bid = guest(g, "sed -n 's/^BUILD_ID=//p' /etc/os-release").stdout.strip().strip('"')
    check(bid == commit, label + ' exact installed BUILD_ID')
    actual = {}
    for name, digest in expected[commit].items():
        actual[name] = guest(g, 'sha256sum ' + shlex.quote(name)).stdout.split()[0]
        check(actual[name] == digest, label + ' exact installed ' + Path(name).name)
    (out / (label + '-identity.json')).write_text(json.dumps({'build_id': bid, 'files': actual}, indent=2) + '\n')


for entry in Path('/proc').glob('[0-9]*/cmdline'):
    try:
        first = Path(entry.read_bytes().split(b'\0', 1)[0].decode()).name
    except (OSError, UnicodeError):
        continue
    assert not first.startswith('qemu-system-'), 'another VM owns QA'
for port in [10022, 10023, 5909, 5910, 9040]:
    with socket.socket() as s:
        s.bind(('127.0.0.1', port))
check(not (owner / 'pair').exists(), 'fresh independent pair directory')
for row in json.loads((out / 'retained-image-verification.json').read_text())['files']:
    with Path(row['path']).open('rb') as f:
        check(hashlib.file_digest(f, 'sha256').hexdigest() == row['sha256'], 'retained image hash ' + Path(row['path']).name)

old_commit, new_commit = expected['commits']
try:
    backend_started = True
    run([be, 'up'], 'backend-up')
    pair_started = True
    run([vp, 'up', str(old)], 'pair-up')
    run([vp, 'reimage', 'b', str(new)], 'fresh-b')
    identity('a', 'previous-a', old_commit)
    identity('b', 'fresh-b', new_commit)
    check('layout_join()' not in guest('b', 'cat /usr/bin/cloud_migrate_layout').stdout, 'historical installed migration has no join implementation')
    config = subprocess.check_output([be, 'rclone-conf'], text=True)
    for g in ['a', 'b']:
        guest(g, 'systemctl stop essway; mkdir -p /storage/.config/rclone /storage/roms/nes; cat > /storage/.config/rclone/rclone.conf; chmod 600 /storage/.config/rclone/rclone.conf', data=config)
        guest(g, '/usr/bin/cloud_sync_helper >/dev/null 2>&1; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0')
    a_before, b_before = state('a'), state('b')
    check('SAVES_REMOTE="/ROCKNIX/Saves"' in a_before, 'actual RC2 starts on ROCKNIX')
    check('SAVES_REMOTE="/Rasteratops/Saves"' in b_before, 'historical fresh peer starts on its own shipped default')
    check('/ROCKNIX/Saves' in guest('b', '/usr/bin/cloud_migrate_layout --superseded').stdout.splitlines(), 'historical build recognizes the earlier source; negative premise valid')
    witness = b'pixelelated QA historical no-join save\n' * 120
    guest('a', 'cat > /storage/roms/nes/NoJoinFromA.srm', data=witness.decode())
    backup = guest('a', '/usr/bin/cloud_backup --yes --method=copy --update --saves-only', timeout=180)
    (out / 'previous-a-backup.log').write_text(backup.stdout + backup.stderr)
    saved = owner / 'cloud/data/ROCKNIX/Saves/nes/NoJoinFromA.srm'
    check(saved.read_bytes() == witness, 'actual RC2 backup reached the cloud byte for byte')
    guest('a', '/usr/bin/backuptool backup >/dev/null 2>&1', timeout=180)
    settings = guest('a', '/usr/bin/cloud_backup --yes --system-only', timeout=180)
    (out / 'previous-a-settings-backup.log').write_text(settings.stdout + settings.stderr)
    check(any(k.endswith('_SETTINGS.tar.gz') for k in files()), 'actual RC2 settings archive also reached cloud')
    cloud_before = files()
    boot0 = guest('a', 'cat /proc/sys/kernel/random/boot_id').stdout.strip()
    run([vp, 'scp', 'a', str(tar), '/storage/.update/'], 'a-update-copy')
    guest('a', 'sync; reboot', allowed=None)
    deadline = time.monotonic() + 420
    boot1 = ''
    while time.monotonic() < deadline:
        try:
            r = guest('a', 'cat /proc/sys/kernel/random/boot_id', allowed=None, timeout=12)
        except subprocess.TimeoutExpired:
            time.sleep(5)
            continue
        boot1 = r.stdout.strip()
        if r.returncode == 0 and boot1 and boot1 != boot0:
            r = guest('a', "sed -n 's/^BUILD_ID=//p' /etc/os-release", allowed=None)
            if r.stdout.strip().strip('"') == new_commit:
                break
        time.sleep(5)
    check(boot1 and boot1 != boot0, 'a rebooted for actual in-place update')
    identity('a', 'updated-a', new_commit)
    guest('a', 'systemctl stop essway')
    check(state('a') == a_before, 'in-place update retains the populated ROCKNIX pointers')
    check(files() == cloud_before, 'in-place update preserves original cloud bytes')
    scan = guest('b', '/usr/bin/cloud_scan --folder', allowed=None, timeout=180)
    (out / 'fresh-b-scan.log').write_text(scan.stdout + scan.stderr)
    scan_state = guest('b', 'cat /storage/.cache/cloud_sync/scan/state', allowed=None).stdout
    (out / 'fresh-b-scan.state').write_text(scan_state)
    check(scan.returncode == 0, 'historical scan runs successfully before join assertion')
    check('STATE=superseded-with-files' in scan_state and 'SOURCE=/ROCKNIX/Saves' in scan_state, 'scan sees populated earlier folder; not a missing-provider false control')
    seed = guest('b', '/usr/bin/cloud_setup --seed-folders', allowed=None, timeout=180)
    (out / 'fresh-b-seed.log').write_text(seed.stdout + seed.stderr)
    check(seed.returncode == 0, 'historical wizard seeding completed')
    b_after = state('b')
    joined = b_after == a_before
    check(not joined and b_after == b_before, 'EXPECTED NEGATIVE: genuine old fresh build did not join any of the three earlier pointers')
    restore = guest('b', '/usr/bin/cloud_restore --yes --method=copy --update --saves-only', allowed=None, timeout=180)
    (out / 'fresh-b-restore.log').write_text(restore.stdout + restore.stderr)
    missing = guest('b', 'test ! -e /storage/roms/nes/NoJoinFromA.srm', allowed=None).returncode == 0
    check(missing, 'EXPECTED NEGATIVE: fresh peer cannot restore the existing earlier save through its unchanged defaults')
    after = files()
    check(all(after.get(k) == v for k, v in cloud_before.items()), 'all original cloud bytes remain intact during negative control')
    check(saved.read_bytes() == witness, 'source witness survives byte for byte')
    (out / 'no-join-negative.json').write_text(json.dumps({
        'verified_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'previous_commit': old_commit, 'negative_commit': new_commit,
        'a_before': a_before, 'a_after': state('a'), 'b_before': b_before, 'b_after': b_after,
        'cloud_before': cloud_before, 'cloud_after': after, 'scan_state': scan_state,
        'join_assertion': 'EXPECTED FAIL', 'restore_witness_assertion': 'EXPECTED FAIL',
        'restore_returncode': restore.returncode, 'original_bytes_preserved': True,
        'scope': 'Actual retained pre-join image on updated RC2 guest a and fresh guest b. Historical default is intentionally not the current product default. No personal provider or fielded Rasteratops migration claim.'
    }, indent=2) + '\n')
finally:
    cleanup_errors = []
    for started, command, label in [(pair_started, vp, 'pair-down'),
                                     (backend_started, be, 'backend-down')]:
        if started:
            try:
                run([command, 'down'], label)
            except Exception as error:
                cleanup_errors.append(str(error))
    assert not cleanup_errors, cleanup_errors

print('PASS genuine installed mixed-pair no-join expected negative', flush=True)
