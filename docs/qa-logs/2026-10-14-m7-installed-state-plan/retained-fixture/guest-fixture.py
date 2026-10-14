#!/usr/bin/env python3
"""Synthetic disposable GENERIC_X64 fixture; CONFIG/PHASE supplied by prepare.py.

No provider request, game launch, update or reboot. Public output is value-free.
The complete unchanged selected-state gate supplies parsing and boot readiness.
"""
import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import resource
import signal
import stat
import subprocess
import tarfile
import time
import types
import urllib.request

STAGE = 'initial'
REPORT = {'schema': 1, 'phase': PHASE, 'result': 'FAIL', 'checks': {}}
SYSTEM = Path('/storage/.config/system/configs/system.cfg')
ES = Path('/storage/.config/emulationstation/es_settings.cfg')
ROM = Path('/storage/roms/gb/pixelelated-installed-state.gb')
GAMELIST = ROM.with_name('gamelist.xml')
TOKEN = Path('/storage/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat')
STAMP = Path('/storage/.cache/cloud_sync')
STATE = Path('/storage/.cache/pixelelated-installed-state-' + CONFIG['id'])
BACKUPS = Path('/storage/roms/backup')
RA = {'global.retroachievements.username': 'synthetic-ra-user',
      'global.retroachievements.password': 'synthetic-ra-pass',
      'global.retroachievements.token': 'synthetic-ra-token',
      'global.retroachievements.key': 'synthetic-ra-key'}
SS = {'ScreenScraperUser': 'synthetic-ss-user', 'ScreenScraperPass': 'synthetic-ss-pass',
      'ScreenScraperDevId': 'synthetic-developer', 'ScreenScraperDevPass': 'synthetic-dev-pass'}
KNOBS = {'global.retroachievements': '0', 'global.retroachievements.offlineproxy': '0',
         'cloudsaves.startup': '0', 'cloudsaves.gameexit': '0',
         'rehearsal.installed-state': 'synthetic-preserved'}
ES_EXTRA = {'CollectionSystemsAuto': 'favorites,recent'}
ROM_BYTES = b'PIXELELATED SYNTHETIC METADATA FIXTURE\n'
TOKEN_BYTES = b'synthetic-standalone-token\n'
STAMPS = {'last-backup': b'1600000000 0\n', 'last-restore': b'1600000060 0\n'}
SECRET_BYTES = [v.encode() for k, v in {**RA, **SS}.items()
                if not k.endswith(('username', 'User', 'DevId'))] + [TOKEN_BYTES.strip()]

def require(ok, code):
    if not ok:
        raise RuntimeError(code)


def stable(s):
    return (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)


def data(path, maximum=1024 * 1024):
    path = Path(path)
    require(not path.is_symlink(), 'input-symlink')
    with path.open('rb') as f:
        before = os.fstat(f.fileno())
        require(stat.S_ISREG(before.st_mode) and before.st_size <= maximum, 'input-shape')
        result = f.read(maximum + 1)
        after = os.fstat(f.fileno())
    require(stable(before) == stable(after) and len(result) == before.st_size, 'input-changed')
    return result


def file_sha(path):
    with Path(path).open('rb') as f:
        before = os.fstat(f.fileno())
        require(stat.S_ISREG(before.st_mode) and before.st_size <= 256 * 1024**2, 'elf-shape')
        h = hashlib.sha256()
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
        require(stable(os.fstat(f.fileno())) == stable(before), 'elf-changed')
    return h.hexdigest()


def put(path, value, create=False):
    path = Path(path)
    require(not path.is_symlink(), 'output-symlink')
    if create:
        require(not path.exists(), 'output-exists')
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o600
    temporary = path.with_name(path.name + '.pix565-new')
    with temporary.open('xb') as f:
        os.fchmod(f.fileno(), mode)
        f.write(value)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temporary, path)


def receipt(name, value):
    target = STATE / (name + '.json')
    put(target, (json.dumps(value, sort_keys=True, indent=2) + '\n').encode(), create=True)


def read_receipt(name):
    return json.loads(data(STATE / (name + '.json')))


def pairs(raw):
    return {key: value for section, key, value in GATE.pairs(raw) if not section}


def settings(raw):
    tree = GATE.xml(raw, 'config')
    out = {}
    for child in tree:
        name = child.attrib.get('name')
        require(name is not None and name not in out and 'value' in child.attrib, 'xml-shape')
        out[name] = child.attrib['value']
    return tree, out


def identity(candidate):
    release = pairs(data('/etc/os-release'))
    with Path('/sys/class/dmi/id/sys_vendor').open() as f:
        vendor = f.read(4096).lower()
    require('qemu' in vendor or 'kvm' in vendor, 'disposable-qemu-required')
    require(release.get('hw_device') == 'GENERIC_X64' and release.get('hw_arch') == 'x86_64', 'qa-device-required')
    want = CONFIG['candidate_commit'] if candidate else CONFIG['previous_commit']
    require(release.get('build_id') == want, 'build-mismatch')
    require(file_sha('/usr/bin/emulationstation') == CONFIG['candidate_es_sha256' if candidate else 'previous_es_sha256'], 'es-file-mismatch')
    return release['build_id']


def frontend_pids():
    found = []
    for p in Path('/proc').iterdir():
        if p.name.isdigit():
            try:
                if os.readlink(p / 'exe') == '/usr/bin/emulationstation':
                    found.append(int(p.name))
            except FileNotFoundError:
                pass
    return found


def ready():
    deadline = time.monotonic() + 70
    while True:
        try:
            boot = GATE.first_boot_ready()
            pids = frontend_pids()
            require(len(pids) == 1, 'frontend-count')
            require(file_sha('/proc/' + str(pids[0]) + '/exe') == file_sha('/usr/bin/emulationstation'), 'executing-es-mismatch')
            return boot
        except Exception:
            if time.monotonic() >= deadline:
                raise RuntimeError('boot-not-ready') from None
            time.sleep(1)


def command(*args, timeout=30):
    r = subprocess.run(args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=timeout)
    require(r.returncode == 0 and len(r.stdout) <= 16384 and len(r.stderr) <= 16384, 'service-command')
    return r.stdout.decode()


def stop_frontend():
    active = []
    for unit in ['essway.service', 'emustation.service']:
        r = subprocess.run(['systemctl', 'is-active', unit], capture_output=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip() == b'active':
            active.append(unit)
    require(len(active) == 1, 'frontend-unit-count')
    command('systemctl', 'stop', active[0])
    deadline = time.monotonic() + 10
    while frontend_pids() and time.monotonic() < deadline:
        time.sleep(.2)
    require(not frontend_pids(), 'frontend-stop')
    return active[0]


def request(path):
    # Guest loopback ES API only; no game launch or provider endpoint.
    with urllib.request.urlopen('http://127.0.0.1:1234' + path, timeout=3) as f:
        require(f.status == 200, 'es-api-status')
        raw = f.read(8 * 1024**2 + 1)
    require(len(raw) <= 8 * 1024**2, 'es-api-size')
    return json.loads(raw)


def loaded_history():
    deadline = time.monotonic() + 30
    while True:
        try:
            if request('/isIdle') == [True]:
                break
        except (OSError, ValueError):
            pass
        require(time.monotonic() < deadline, 'es-idle-timeout')
        time.sleep(.5)
    rows = [row for row in request('/systems/gb/games') if row.get('path') == str(ROM)]
    recent = [row for row in request('/systems/recent/games') if row.get('path') == str(ROM)]
    REPORT['checks']['api_game_match_count'] = len(rows)
    REPORT['checks']['api_recent_match_count'] = len(recent)
    require(len(rows) == 1 and len(recent) == 1, 'loaded-history-membership')
    require(int(rows[0].get('playcount', 0)) == 5 and rows[0].get('lastplayed') == '20260908T031024', 'loaded-history-fields')


def selected():
    conf = pairs(data(SYSTEM))
    _, es = settings(data(ES))
    require(all(conf.get(k) == v for k, v in {**RA, **KNOBS}.items()), 'retained-system-fields')
    require(all(es.get(k) == v for k, v in {**SS, **ES_EXTRA}.items()), 'retained-es-fields')
    require(data(ROM) == ROM_BYTES and data(TOKEN) == TOKEN_BYTES, 'retained-fixture-bytes')
    for name, value in STAMPS.items():
        require(data(STAMP / name) == value, 'retained-activity-stamp')
    root = GATE.xml(data(GAMELIST), 'gameList')
    rows = [g for g in root.findall('game') if g.findtext('path') == './' + ROM.name]
    require(len(rows) == 1, 'retained-gamelist-entry')
    require(rows[0].findtext('playcount') == '5' and rows[0].findtext('lastplayed') == '20260908T031024', 'retained-gamelist-fields')
    return {'ra_fields_equal': True, 'screenscraper_fields_equal': True,
            'automatic_operations_disabled': True, 'history_fields_equal': True,
            'activity_stamp_bytes_equal': True, 'standalone_token_equal': True}


def seed():
    global STAGE
    STAGE = 'clean-before-seed'
    identity(False)
    boot = ready()
    clean = GATE.Check(GATE.Local(Path('/')), 'first-boot').run()
    require(clean['status'] == 'pass', 'baseline-not-clean')
    require(not STATE.exists() and not STATE.is_symlink(), 'state-owner-exists')
    require(not Path('/storage/.config/backuptool.conf').exists(), 'custom-backup-config')
    for p in [ROM, GAMELIST, TOKEN, *(STAMP / x for x in STAMPS)]:
        require(not p.exists() and not p.is_symlink(), 'fixture-input-exists')
    STATE.mkdir(mode=0o700)
    receipt('seed-started', {'id': CONFIG['id'], 'boot': boot, 'build': CONFIG['previous_commit']})
    unit = stop_frontend()
    try:
        STAGE = 'seed-selected-files'
        current = pairs(data(SYSTEM))
        _, es = settings(data(ES))
        require(all(not current.get(k, '') for k in RA) and all(not es.get(k, '') for k in SS), 'nonempty-account-before-seed')
        changes = {**RA, **KNOBS}
        lines = [line for line in data(SYSTEM).decode().splitlines()
                 if line.lstrip().split('=', 1)[0].strip().lower() not in changes]
        put(SYSTEM, ('\n'.join(lines) + '\n' + ''.join(k + '=' + v + '\n' for k, v in changes.items())).encode())
        tree, _ = settings(data(ES))
        for key, value in {**SS, **ES_EXTRA}.items():
            matches = [n for n in tree if n.attrib.get('name') == key]
            require(len(matches) <= 1, 'duplicate-selected-es-field')
            node = matches[0] if matches else GATE.ET.SubElement(tree, 'string', name=key)
            node.set('value', value)
        # Match the actual writer's line-per-setting contract: backup strips lines.
        GATE.ET.indent(tree, space='    ')
        put(ES, GATE.ET.tostring(tree, encoding='utf-8', xml_declaration=True) + b'\n')
        for directory in [ROM.parent, TOKEN.parent, STAMP]:
            directory.mkdir(parents=True, exist_ok=True)
            require(directory.is_dir() and not directory.is_symlink(), 'fixture-parent-shape')
        put(ROM, ROM_BYTES, create=True)
        put(TOKEN, TOKEN_BYTES, create=True)
        put(GAMELIST, ('<?xml version="1.0"?><gameList><game><path>./' + ROM.name + '</path><name>Synthetic retained metadata</name><playcount>5</playcount><lastplayed>20260908T031024</lastplayed></game></gameList>\n').encode(), create=True)
        for name, value in STAMPS.items():
            put(STAMP / name, value, create=True)
        selected()
        os.sync()
    finally:
        command('systemctl', 'start', unit)
    STAGE = 'seed-loaded-verification'
    require(ready() == boot, 'boot-changed-during-seed')
    REPORT['checks'].update(selected())
    loaded_history()
    REPORT['checks']['loaded_recent_history'] = True
    receipt('seed', {'id': CONFIG['id'], 'boot': boot, 'result': 'PASS',
            'candidate_commit': CONFIG['candidate_commit'], 'candidate_es_sha256': CONFIG['candidate_es_sha256']})


def before_after(candidate):
    global STAGE
    STAGE = 'retained-before' if not candidate else 'retained-after'
    identity(candidate)
    boot = ready()
    seed_record = read_receipt('seed')
    require(seed_record['id'] == CONFIG['id'] and seed_record['result'] == 'PASS' and
            seed_record['candidate_commit'] == CONFIG['candidate_commit'] and
            seed_record['candidate_es_sha256'] == CONFIG['candidate_es_sha256'], 'seed-receipt')
    if candidate:
        before = read_receipt('before')
        require(before['result'] == 'PASS' and before['boot'] != boot, 'new-boot-required')
        require(not any(Path('/storage/.update').iterdir()), 'update-queue-not-empty')
    else:
        require(boot == seed_record['boot'], 'baseline-boot-changed')
    REPORT['checks'].update(selected())
    loaded_history()
    REPORT['checks']['loaded_recent_history'] = True
    policy = GATE.Check(GATE.Local(Path('/')), 'retained-upgrade').run()
    require(policy['status'] == 'pass', 'retained-policy')
    REPORT['checks']['retained_policy_pass'] = True
    REPORT['checks']['expected_build_and_executing_es'] = True
    receipt('after' if candidate else 'before', {'id': CONFIG['id'], 'result': 'PASS', 'boot': boot,
            'distribution_commit': CONFIG['candidate_commit'] if candidate else CONFIG['previous_commit'],
            'es_commit': CONFIG['candidate_es_commit'] if candidate else CONFIG['previous_es_commit']})
    receipt('after-policy' if candidate else 'before-policy', policy)


def backup_process():
    def limits():
        resource.setrlimit(resource.RLIMIT_FSIZE, (256 * 1024**2, 256 * 1024**2))
    with (STATE / 'backup.stdout').open('xb') as out, (STATE / 'backup.stderr').open('xb') as err:
        child = subprocess.Popen(['/usr/bin/backuptool', 'backup'], stdin=subprocess.DEVNULL,
                                 stdout=out, stderr=err, start_new_session=True, preexec_fn=limits)
        try:
            rc = child.wait(timeout=180)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGTERM)
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait(timeout=5)
            rc = 124
    receipt('backup-child', {'returncode': rc})
    require(rc == 0, 'backup-original-exit')


def archive_check(path):
    require(not path.is_symlink() and path.is_file() and path.stat().st_size <= 256 * 1024**2, 'archive-size')
    contents, seen, total = {}, set(), 0
    wanted = {'storage/.config/system/configs/system.cfg', 'storage/.config/emulationstation/es_settings.cfg'}
    with tarfile.open(path, 'r:gz') as archive:
        for member in archive:
            name = PurePosixPath(member.name)
            require(not name.is_absolute() and '..' not in name.parts and name.parts and name.parts[0] == 'storage', 'archive-path')
            key = str(name)
            require(key not in seen and len(seen) < 4096, 'archive-duplicate-or-count')
            seen.add(key)
            require(member.isdir() or member.isfile(), 'archive-member-type')
            require(member.size <= 16 * 1024**2, 'archive-member-size')
            if member.isfile():
                total += member.size
                require(total <= 256 * 1024**2, 'archive-expanded-size')
                stream = archive.extractfile(member)
                require(stream is not None, 'archive-read')
                raw = stream.read(16 * 1024**2 + 1)
                require(len(raw) == member.size, 'archive-short-read')
                require(not any(secret in raw for secret in SECRET_BYTES), 'archive-synthetic-secret-present')
                if key in wanted:
                    contents[key] = raw
    require(set(contents) == wanted, 'archive-selected-members-missing')
    require(str(TOKEN).lstrip('/') not in seen, 'archive-standalone-token-present')
    syscfg = pairs(contents['storage/.config/system/configs/system.cfg'])
    _, escfg = settings(contents['storage/.config/emulationstation/es_settings.cfg'])
    require(syscfg.get('global.retroachievements.username') == RA['global.retroachievements.username'], 'archive-ra-user-missing')
    require(not any(k in syscfg for k in RA if not k.endswith('username')), 'archive-ra-secrets-present')
    require(syscfg.get('rehearsal.installed-state') == KNOBS['rehearsal.installed-state'], 'archive-setting-missing')
    require(escfg.get('ScreenScraperUser') == SS['ScreenScraperUser'] and escfg.get('ScreenScraperDevId') == SS['ScreenScraperDevId'], 'archive-identifiers-missing')
    require('ScreenScraperPass' not in escfg and 'ScreenScraperDevPass' not in escfg, 'archive-password-fields-present')
    require(escfg.get('CollectionSystemsAuto') == ES_EXTRA['CollectionSystemsAuto'], 'archive-harmless-setting-missing')
    return {'archive_credentials_absent': True, 'archive_user_identifiers_preserved': True,
            'archive_harmless_settings_preserved': True, 'archive_token_file_absent': True,
            'archive_member_count': len(seen)}


def backup():
    global STAGE
    STAGE = 'backup-prerequisites'
    identity(True)
    boot = ready()
    after = read_receipt('after')
    require(after['result'] == 'PASS' and after['boot'] == boot, 'after-receipt')
    require(file_sha('/usr/bin/backuptool') == CONFIG['backuptool_sha256'], 'installed-backuptool-mismatch')
    require(not Path('/storage/.config/backuptool.conf').exists(), 'custom-backup-config')
    cloud = pairs(data('/storage/.config/cloud_sync.conf'))
    require(cloud.get('settings_backups', '/storage/roms/backup').rstrip('/') == str(BACKUPS), 'backup-folder-override')
    require(not BACKUPS.is_symlink(), 'backup-folder-symlink')
    prior = set(BACKUPS.glob('*.tar.gz')) if BACKUPS.exists() else set()
    require(not prior, 'fresh-backup-folder-required')
    unit = stop_frontend()
    try:
        STAGE = 'installed-backup'
        selected()
        paths = [SYSTEM, ES, ROM, GAMELIST, TOKEN, *(STAMP / x for x in STAMPS)]
        before = {p: data(p) for p in paths}
        backup_process()
        require(all(data(p) == raw for p, raw in before.items()), 'backup-mutated-source')
        current = set(BACKUPS.glob('*.tar.gz'))
        require(len(current - prior) == 1, 'new-archive-count')
        archive = next(iter(current - prior))
        require(re.fullmatch(r'\d{4}_\d{2}_\d{2}-\d{6}-(?:[A-Za-z0-9_-]+-)?ROCKNIX_SETTINGS\.tar\.gz', archive.name) is not None, 'archive-name-contract')
        STAGE = 'installed-backup-comparison'
        REPORT['checks'].update(archive_check(archive))
        REPORT['checks']['selected_runtime_bytes_unchanged'] = True
    finally:
        command('systemctl', 'start', unit)
    require(ready() == boot, 'boot-changed-during-backup')
    selected()
    loaded_history()
    REPORT['checks']['frontend_restored'] = True
    receipt('backup', {'id': CONFIG['id'], 'result': 'PASS', 'boot': boot})


def main():
    global GATE, STAGE
    raw = base64.b64decode(CONFIG['gate_base64'], validate=True)
    require(hashlib.sha256(raw).hexdigest() == CONFIG['gate_sha256'], 'gate-source-mismatch')
    GATE = types.ModuleType('bound_state_gate')
    exec(compile(raw, '<bound-state-check>', 'exec'), GATE.__dict__)
    require(re.fullmatch('[a-z0-9][a-z0-9-]{0,47}', CONFIG['id']) is not None, 'owner-id')
    require(PHASE in {'seed', 'before', 'after', 'backup'}, 'phase')
    {'seed': seed, 'before': lambda: before_after(False), 'after': lambda: before_after(True), 'backup': backup}[PHASE]()
    REPORT['result'] = 'PASS'
    REPORT['stage'] = 'complete'


if __name__ == '__main__':
    try:
        main()
    except BaseException as error:
        REPORT['stage'] = STAGE
        # Only our literal error codes are public; no parser/child/input values.
        REPORT['error'] = str(error) if type(error) is RuntimeError and re.fullmatch('[a-z-]+', str(error)) else 'fixture-refused'
    print(json.dumps(REPORT, sort_keys=True))
    raise SystemExit(0 if REPORT['result'] == 'PASS' else 1)
