#!/usr/bin/env python3
"""UNRUN: one bounded actual-main/systemd lifecycle proof; no component suite replay."""
import argparse
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import socket
import sqlite3
import subprocess
import sys
import threading
import time

PACKET = Path('/run/pix583-service-packet')
PREPARED = Path('/run/pix583-service-inputs/prepared')
ROOT = Path('/run/pix583-service-owner')
UNIT = 'pix583-service-proof.service'
OWNER = 'pix583-service-proof-owner.service'
UNIT_FILE = Path('/run/systemd/system') / UNIT
DROP_DIR = UNIT_FILE.with_name(UNIT + '.d')
DROP_FILE = DROP_DIR / 'fixture.conf'
WORKERS = {'ConnectivityMonitor', 'PeriodicRefresh', 'CacheQueueWorker', 'FolderWatcher', 'UsageReporter'}
REPORT = {'status': 'FAIL', 'commands': [], 'steps': [], 'cleanup_errors': [], 'source_pins_verified': False}


def need(value, message):
    if not value:
        raise AssertionError(message)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + '\n')


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def until(predicate, seconds, message):
    deadline = time.monotonic() + seconds
    while True:
        value = predicate()
        if value:
            return value
        need(time.monotonic() < deadline, message)
        time.sleep(0.1)


def command(argv, timeout=12, allowed=(0,)):
    index = len(REPORT['commands'])
    row = {'argv': argv, 'original_exit': None, 'timeout': False}
    REPORT['commands'].append(row)
    started = time.monotonic()
    row['monotonic_start'] = started
    with (OUT / f'command-{index}.stdout').open('xb') as stdout, (OUT / f'command-{index}.stderr').open('xb') as stderr:
        proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                                start_new_session=True, env={'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'LANG': 'C', 'LC_ALL': 'C'})
        row['identity'] = CENSUS.proc_identity(proc.pid)
        try:
            row['original_exit'] = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            row['timeout'] = True
            row['cleanup'] = CENSUS.signal_child(row['identity'], os.getpid())
            row['original_exit'] = proc.wait(timeout=2)
        finally:
            row['elapsed_seconds'] = time.monotonic() - started
            dump(OUT / 'commands.json', REPORT['commands'])
    text = (OUT / f'command-{index}.stdout').read_text()
    need(len(text) <= 2 * 1024**2 and (OUT / f'command-{index}.stderr').stat().st_size <= 2 * 1024**2,
         'command log exceeds bound')
    need(not row['timeout'] and row['original_exit'] in allowed, 'original command failed: ' + repr(row))
    return text


def properties(unit=UNIT):
    keys = ('LoadState', 'ActiveState', 'SubState', 'MainPID', 'FragmentPath', 'DropInPaths',
            'ControlGroup', 'Result', 'ExecMainCode', 'ExecMainStatus', 'ExecStartPost', 'NRestarts',
            'Restart', 'RestartUSec', 'TimeoutStopUSec', 'StartLimitIntervalUSec', 'StartLimitBurst',
            'ConditionResult', 'InvocationID', 'BindsTo', 'Environment', 'ExecStart')
    keys += ('RuntimeMaxUSec', 'KillMode', 'MemoryMax')
    text = command(['systemctl', 'show', unit, '--no-pager', '--property=' + ','.join(keys)], allowed=(0, 1))
    result = dict(line.split('=', 1) for line in text.splitlines() if '=' in line)
    need(REPORT['commands'][-1]['original_exit'] == 0 or result.get('LoadState') == 'not-found', 'systemd property read failed')
    return result


def owned_unit():
    need(sha(UNIT_FILE) == UNIT_SHA and sha(DROP_FILE) == DROP_SHA, 'owned unit files changed')
    p = properties()
    need(p['FragmentPath'] == str(UNIT_FILE) and p['DropInPaths'].split() == [str(DROP_FILE)], 'unit definition changed')
    need(OWNER in p['BindsTo'].split(), 'service not bound to fresh owner')
    return p


def action(verb):
    owned_unit()
    command(['systemctl', verb, UNIT], timeout=35 if verb in ('start', 'restart') else 22)


def events(pid):
    path = STATE / f'observer-{pid}.jsonl'
    if not path.exists():
        return []
    raw = path.read_bytes()
    need(len(raw) <= 1024 * 1024, 'observer log bound')
    # A trailing write still in progress is not an event. Final reads require newline below.
    return [json.loads(line) for line in raw.splitlines(keepends=True) if line.endswith(b'\n')]


def rows():
    with sqlite3.connect('file:' + str(STATE / 'proxy.sqlite3') + '?mode=ro', uri=True, timeout=1) as db:
        db.row_factory = sqlite3.Row
        return [dict(row) for row in db.execute('SELECT * FROM pending_awards ORDER BY id')]


def cache_queue_count():
    with sqlite3.connect('file:' + str(STATE / 'proxy.sqlite3') + '?mode=ro', uri=True, timeout=1) as db:
        return db.execute("SELECT count(*) FROM api_cache WHERE cacheKey LIKE 'cachequeue:%'").fetchone()[0]


def active(old=None):
    p = properties()
    pid = int(p['MainPID'])
    if p['ActiveState'] != 'active' or pid <= 0 or pid == old:
        return None
    identity = CENSUS.proc_identity(pid)
    need(identity is not None, 'active service identity unreadable')
    cmd = Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')
    need(cmd[:4] == [b'/usr/bin/python3', b'-m', b'raofflineproxy.main', b'run-service'], 'wrong actual service entrypoint')
    group = p['ControlGroup']
    need(group.startswith('/system.slice/') and group.endswith('/' + UNIT), 'unexpected service cgroup')
    members = cgroup_members(group)
    need(members == [pid], 'unexpected service descendants')
    need(p['Result'] == 'success' and 'status=0' in p['ExecStartPost'] and 'code=exited' in p['ExecStartPost'],
         'packaged readiness command did not exit 0')
    need(p['Restart'] == 'on-failure' and p['RestartUSec'] == '5s' and p['TimeoutStopUSec'] == '15s'
         and p['StartLimitIntervalUSec'] == '5min' and p['StartLimitBurst'] == '5', 'packaged lifecycle limits changed')
    found = [r for r in REF.tcp_listeners() if r[1] == '0100007F:1F90']
    need(len(found) == 1, 'missing/ambiguous IPv4 service listener')
    inode = found[0][9]
    links = []
    for f in Path(f'/proc/{pid}/fd').iterdir():
        try:
            links.append(os.readlink(f))
        except FileNotFoundError:
            continue  # A request/DNS FD may close; only a positive listener match counts.
    need(CENSUS.proc_identity(pid) == identity, 'MainPID identity changed during listener observation')
    need(f'socket:[{inode}]' in links, 'listener does not belong to systemd MainPID')
    need(os.readlink(f'/proc/{pid}/ns/net') == os.readlink('/proc/self/ns/net'), 'wrong service network namespace')
    entry = {'identity': identity, 'properties': p, 'listener_inode': inode}
    entry['kernel_limits'] = CGROUP.observe(pid, UNIT, 536870912, 64)
    need(int((STATE / 'service.pid').read_text()) == pid, 'tracked service PID differs')
    saved = json.loads((STATE / 'service_status.json').read_text())
    need(saved.get('running') is True and saved.get('pid') == pid, 'service status does not identify MainPID')
    entry['observed_monotonic'] = time.monotonic()
    entry['saved_status'] = saved
    REPORT.setdefault('incarnations', {})[str(pid)] = entry
    return pid


def cgroup_members(group):
    CGROUP.layout()  # A vanished/replaced hierarchy is not an empty owned group.
    need(group.startswith('/system.slice/') and group.endswith('/' + UNIT), 'invalid owned cgroup')
    root = Path('/sys/fs/cgroup') / group.lstrip('/')
    try:
        root.stat()
    except FileNotFoundError:
        return []
    found = set()
    def observation_error(error):
        raise error
    count = 0
    for base, dirs, files in os.walk(root, onerror=observation_error):
        count += 1
        need(count <= 128 and 'cgroup.procs' in files, 'unreadable/unbounded owned cgroup')
        found.update(int(line) for line in (Path(base) / 'cgroup.procs').read_text().splitlines())
    need(count > 0, 'owned cgroup observation unexpectedly empty')
    return sorted(found)


def worker_start(pid):
    def observed():
        e = events(pid)
        return {r['class'] for r in e if r.get('function') == 'run' and r.get('event') == 'call'} == WORKERS
    until(observed, 12, 'actual main did not start all five workers')
    e = events(pid)
    need(any(r['kind'] == 'guard-ready' for r in e), 'boundary absent')
    for name in ('main', 'run_service_foreground', 'run_proxy_service'):
        need(any(r.get('function') == name and r.get('event') == 'call' for r in e), 'actual entrypoint not observed: ' + name)
    timings = {r['class']: r['timings'] for r in e if r.get('function') == 'run' and r.get('event') == 'call'}
    need(timings == {'ConnectivityMonitor': {'interval_seconds': 15}, 'PeriodicRefresh': {'interval_seconds': 3600},
                    'CacheQueueWorker': {'poll_seconds': 60}, 'FolderWatcher': {'poll_seconds': 60},
                    'UsageReporter': {'interval_seconds': 900, 'initial_delay_seconds': 60}}, 'worker timers changed')


def gone(pid, graceful):
    until(lambda: CENSUS.proc_identity(pid) is None, 3, 'old service PID remains')
    group = REPORT['incarnations'][str(pid)]['properties']['ControlGroup']
    # A restart may reuse this cgroup for the new PID; only the old identity must be absent.
    need(pid not in cgroup_members(group), 'old cgroup member remains')
    if graceful:
        e = events(pid)
        stopped = [i for i, r in enumerate(e) if r.get('function') == 'stop_workers' and r.get('event') == 'return']
        closed = [i for i, r in enumerate(e) if r.get('function') == 'close' and r.get('class') == 'Storage' and r.get('event') == 'call']
        need(len(stopped) == 1 and e[stopped[0]]['alive'] == dict.fromkeys(WORKERS, False), 'worker survived graceful join')
        need(closed and min(closed) > stopped[0], 'storage closed before workers stopped')
        need(any(r['kind'] == 'python-exit' and r['threads'] == [] for r in e), 'Python exited with live threads')
    need(not any(r['kind'] == 'thread-error' for r in events(pid)), 'background thread failed')


def login_only():
    status, head, body = REF.request({'r': 'login2', 'u': REF.USER_A, 't': REF.TOKENS[REF.USER_A]})
    need(status == 200 and head.get('x-ra-proxy') == head.get('x-ra-offline') == '1'
         and body.get('Success') is True and body.get('User') == REF.USER_A
         and body.get('Token') == REF.TOKENS[REF.USER_A], 'not identified cached sign-in')


def main():
    global OUT, STATE, CENSUS, REF, UNIT_SHA, DROP_SHA, CGROUP
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    OUT = args.output.absolute()
    need(OUT.parent.parent == ROOT and OUT.parent.resolve(strict=True).parent == ROOT and not OUT.exists(), 'fresh owner payload required')
    OUT.mkdir(mode=0o700)
    resource.setrlimit(resource.RLIMIT_AS, (768 * 1024**2,) * 2)
    resource.setrlimit(resource.RLIMIT_FSIZE, (4 * 1024**2,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    started = time.monotonic()
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('240s work deadline')))
    signal.alarm(240)
    created = False
    peer = None
    bulk = None
    try:
        need(os.geteuid() == 0 and 'QEMU' in Path('/sys/class/dmi/id/sys_vendor').read_text(), 'allocated root QEMU guest only')
        need(Path('/proc/1/comm').read_text().strip() == 'systemd', 'actual systemd PID1 required')
        need(set(p.name for p in Path('/sys/class/net').iterdir()) == {'lo'}, 'no-NIC guest required')
        routes = Path('/proc/net/route').read_text().splitlines()
        need(not routes or len(routes) == 1 and routes[0].startswith('Iface'), 'unexpected IPv4 route')
        need(not any(k.lower().endswith('_proxy') or k.startswith(('LD_', 'LISTEN_', 'RAOFFLINEPROXY_')) for k in os.environ), 'external loader/network environment')
        need(PACKET.resolve(strict=True) == PACKET and PREPARED.resolve(strict=True) == PREPARED, 'staging redirects')
        need(not UNIT_FILE.exists() and not UNIT_FILE.is_symlink() and not DROP_DIR.exists() and not DROP_DIR.is_symlink(), 'fixture unit already exists')
        need(Path('/sys/fs/cgroup/cgroup.controllers').is_file(), 'cgroup v2 required for this bounded packet')
        CGROUP = module('service_cgroup_guard', PACKET / 'cgroup_guard.py')
        REPORT['platform_contract'] = CGROUP.platform_contract(PACKET / 'compatibility.json')
        REPORT['cgroup_layout'] = CGROUP.layout()
        dump(OUT / 'cgroup-layout.json', REPORT['cgroup_layout'])
        sealed = set()
        for line in (PACKET / 'SHA256SUMS').read_text().splitlines():
            digest, name = line.split('  ', 1)
            need(not Path(name).is_absolute() and '..' not in Path(name).parts, 'invalid sealed filename')
            need(sha(PACKET / name) == digest, 'packet changed: ' + name)
            sealed.add(name)
        actual = {str(p.relative_to(PACKET)) for p in PACKET.rglob('*') if p.is_file()}
        need(actual == sealed | {'SHA256SUMS'}, 'unsealed packet file')
        staged = list(PACKET.rglob('*')) + list(PREPARED.rglob('*'))
        need(len(staged) < 2048 and not any(p.is_symlink() for p in staged), 'unbounded/redirected staging')
        need(sum(p.stat().st_size for p in staged if p.is_file()) <= 8 * 1024**2, '8MiB staging bound exceeded')
        binding = json.loads((PACKET / 'bindings.json').read_text())
        need(sha(PREPARED / 'source.json') == binding['prepared_source_sha256'], 'prepared source changed')
        manifest = {str(p.relative_to(PREPARED / 'tree')): sha(p) for p in (PREPARED / 'tree').rglob('*.py')}
        need(manifest == binding['prepared_python_manifest'] and not list(PREPARED.rglob('*.pyc')), 'prepared Python manifest differs')
        CENSUS = module('service_census', PACKET / 'census.py')
        REF = module('service_native_reference', PACKET / 'reference_native.py')
        def local_network(event, args):
            if event == 'socket.__new__' and args[1:3] != (socket.AF_INET, socket.SOCK_STREAM):
                raise RuntimeError('driver socket family/type refused')
            if event in ('socket.bind', 'socket.connect') and args[1] not in (('127.0.0.1', 8080), ('127.0.0.1', 18081)):
                raise RuntimeError('driver external endpoint refused')
            if event == 'socket.getaddrinfo' and args[0] != '127.0.0.1':
                raise RuntimeError('driver external resolution refused')
        sys.addaudithook(local_network)
        need(not [r for r in REF.tcp_listeners() if int(r[1].split(':')[1], 16) in (8080, 18081)], 'allocated endpoint occupied; stop nothing')
        fs = os.statvfs(ROOT)
        mount = [r.split() for r in Path('/proc/self/mountinfo').read_text().splitlines()]
        need(any(r[4] == str(ROOT) and r[r.index('-') + 1] == 'tmpfs' for r in mount), 'dedicated scratch tmpfs required')
        need(fs.f_blocks * fs.f_frsize <= 64 * 1024**2 and fs.f_bavail * fs.f_frsize >= 48 * 1024**2, '64MiB scratch / 48MiB free required')
        need(properties()['LoadState'] == 'not-found', 'fixture unit already loaded')
        production = properties('raofflineproxy.service')
        need(production.get('MainPID', '0') == '0' and production.get('ActiveState') in ('inactive', 'failed'),
             'installed proxy is active; this fixture stops no existing service')
        need(os.access('/usr/bin/raofflineproxy-ctl', os.X_OK), 'installed controller bind target missing')
        owner = properties(OWNER)
        need(owner['ActiveState'] == 'active' and str(os.getppid()) == owner['MainPID'], 'fresh systemd owner identity missing')
        need(owner['RuntimeMaxUSec'] in ('4min 40s', '280s') and owner['TimeoutStopUSec'] == '20s'
             and owner['KillMode'] == 'control-group' and owner['MemoryMax'] == '1073741824', 'owner bounds differ from allocated command')
        REPORT['owner_cgroup_limits'] = CGROUP.observe(int(owner['MainPID']), OWNER, 1073741824, 128)
        REPORT['admission'] = {'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
                               'owner': owner, 'installed_proxy_properties': production,
                               'installed_unit_sha256': sha(production['FragmentPath']),
                               'source_pins_verified': False, 'libraries': binding['libraries'], 'tools': {}}
        for name in ('python3', 'systemctl', 'journalctl', 'bash'):
            p = Path(shutil.which(name)).absolute()
            REPORT['admission']['tools'][name] = {'invoked': str(p), 'resolved': str(p.resolve()), 'sha256': sha(p)}
        for row in binding['libraries'].values():
            need(str(Path(row['path']).resolve()) == row['resolved_path'] and sha(row['path']) == row['sha256'], 'installed ELF identity changed')
        dump(OUT / 'admission.json', REPORT['admission'])
        storage = OUT / 'storage'
        STATE = storage / '.config/raofflineproxy'
        STATE.mkdir(parents=True)
        shutil.copyfile(PACKET / 'seed/proxy.sqlite3', STATE / 'proxy.sqlite3')
        shutil.copyfile(PACKET / 'seed/award_secret.key', STATE / 'award_secret.key')
        logical = '/storage/.config/raofflineproxy'
        config = {'proxy_host': '127.0.0.1', 'proxy_port': 8080, 'upstream_host': 'http://127.0.0.1:18081',
                  'retroarch_cfg': logical + '/retroarch.cfg', 'rocknix_system_cfg': logical + '/system.cfg',
                  'ppsspp_ini': logical + '/empty-ppsspp.ini', 'dolphin_config_dir': logical + '/empty-dolphin',
                  'cache_images': False, 'upload_logs': False, 'usage_stats_consent': False, 'usage_stats_consent_version': 1}
        dump(STATE / 'config.json', config)
        (STATE / 'retroarch.cfg').write_text('cheevos_username = "fixture-a"\ncheevos_token = "<synthetic-token-a>"\ncontent_history_path = "' + logical + '/content_history.lpl"\n')
        (STATE / 'system.cfg').write_text('global.retroachievements.offlineproxy=1\nglobal.retroachievements.hardcore=0\n')
        (STATE / 'content_history.lpl').write_text('{"items":[]}\n')
        (STATE / 'empty-ppsspp.ini').write_text('[Recent]\n')
        (STATE / 'empty-dolphin').mkdir()
        protected = {p.name: sha(p) for p in STATE.iterdir() if p.is_file() and p.name != 'proxy.sqlite3'}
        need(rows() == [] and cache_queue_count() == 0, 'accepted synthetic seed is not empty of pending work')
        UNIT_SHA = sha(PACKET / 'raofflineproxy.service')
        st = storage.stat()
        drop = f'''[Unit]
ConditionPathExists=
ConditionPathExists={OUT}/enabled
BindsTo={OWNER}
After={OWNER}
[Service]
Environment=PYTHONPATH={PACKET}/bootstrap:{PREPARED}/tree/linux
Environment=PYTHONDONTWRITEBYTECODE=1
Environment=PYTHONNOUSERSITE=1
Environment=DEVICE_HAS_DUAL_SCREEN=false
Environment=PIX583_STORAGE_ID={st.st_dev}:{st.st_ino}
Environment=RAOFFLINEPROXY_RCHASH_LIB=/usr/lib/libraproxy_rchash.so
UnsetEnvironment=http_proxy https_proxy all_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY no_proxy NO_PROXY PYTHONOPTIMIZE PYTHONHOME LD_PRELOAD LD_LIBRARY_PATH
BindPaths={storage}:/storage
BindReadOnlyPaths={PACKET}/profile:/etc/profile
BindReadOnlyPaths={PACKET}/raofflineproxy-ctl:/usr/bin/raofflineproxy-ctl
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths={OUT} /storage
NoNewPrivileges=yes
ExecStartPre=/usr/bin/python3 -I -S -B {PACKET}/cgroup_guard.py --service-receipts {OUT}
MemoryMax=512M
TasksMax=64
LimitAS=512M
LimitCPU=120
LimitFSIZE=4M
LimitCORE=0
StandardOutput=append:{OUT}/service.stdout
StandardError=append:{OUT}/service.stderr
'''
        DROP_SHA = hashlib.sha256(drop.encode()).hexdigest()
        # Keep failed creation visible and owned; never silently abandon a partial unit.
        created = True
        with UNIT_FILE.open('xb') as stream:
            stream.write((PACKET / 'raofflineproxy.service').read_bytes())
        DROP_DIR.mkdir()
        with DROP_FILE.open('x') as stream:
            stream.write(drop)
        REPORT['unit'] = {'base_sha256': UNIT_SHA, 'dropin_sha256': DROP_SHA, 'dropin': drop}
        command(['systemctl', 'daemon-reload'])
        action('start')
        p = properties()
        need(p['MainPID'] == '0' and p['ConditionResult'] == 'no', 'missing-marker condition did not skip startup')
        (OUT / 'enabled').write_text('synthetic-only\n')
        action('start')
        first = until(active, 5, 'first actual service not active')
        worker_start(first)
        REF.ready()
        status, _, body = REF.request({'r': 'awardachievement', 'a': '104', 'g': '10', 'u': REF.USER_A, 't': REF.TOKENS[REF.USER_A], 'h': '0'})
        need(status == 200 and body.get('Error') == 'queued_offline', 'new synthetic award not queued')
        queued = rows()
        need(len(queued) == 1 and queued[0]['achievementId'] == 104, 'wrong pending row')
        dump(OUT / 'pending-before-stop.json', queued)
        action('stop')
        stopped = properties()
        need(stopped['ExecMainCode'] == '1' and stopped['ExecMainStatus'] == '0' and stopped['Result'] == 'success', 'graceful stop was forced/failed')
        gone(first, True)
        need(rows() == queued and not (STATE / 'service.pid').exists(), 'stop changed queue or left tracked pid')
        need(json.loads((STATE / 'service_status.json').read_text())['running'] is False, 'stopped state missing')
        REPORT['steps'].append('graceful stop preserved exact signed row; workers joined before SQLite close')
        action('start')
        second = until(lambda: active(first), 5, 'start after stop failed')
        worker_start(second)
        login_only()
        need(rows() == queued, 'start changed offline queue')
        action('restart')
        third = until(lambda: active(second), 5, 'explicit systemd restart failed')
        gone(second, True)
        worker_start(third)
        login_only()
        need(rows() == queued, 'explicit restart changed offline queue')
        owned_unit()
        command(['systemctl', 'kill', '--kill-whom=main', '--signal=SIGKILL', UNIT])
        failed = until(lambda: (p if (p := properties())['ExecMainCode'] == '2' and p['ExecMainStatus'] == '9' else None), 3, 'original SIGKILL exit not retained')
        REPORT['expected_idle_crash'] = failed
        fourth = until(lambda: active(third), 18, 'packaged Restart=on-failure did not recover')
        gone(third, False)
        worker_start(fourth)
        login_only()
        need(int(properties()['NRestarts']) == 1 and rows() == queued, 'automatic restart changed queue or repeated')
        REPORT['steps'].append('manual and one automatic restart preserved exact signed row and new owned listener')
        # Synthetic queued-job input only. No hashing/parity/scan suite is replayed.
        digest = 'e5830000000000000000000000000001'
        bulk = (STATE / 'cache_queue.bulk.lock').open('a+')
        fcntl.flock(bulk, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with sqlite3.connect(STATE / 'proxy.sqlite3', timeout=1) as db:
            need(db.execute('SELECT count(*) FROM api_cache WHERE cacheKey LIKE ?', ('%' + digest + '%',)).fetchone()[0] == 0,
                 'synthetic worker hash already cached')
            db.execute('INSERT INTO api_cache(cacheKey,responseBody,sourceRomPath,cachedAt,firstCachedAt) VALUES(?,?,?,?,?)',
                       ('cachequeue:' + digest, json.dumps({'hashes': [digest], 'sourceRomPath': None,
                        'label': 'Service worker synthetic mapping; not a ROM hash', 'queuedAt': int(time.time()*1000), 'attempts': 0}),
                        None, int(time.time()*1000), int(time.time()*1000)))
        state = REF.ProtocolState(digest)
        state.secret = (STATE / 'award_secret.key').read_bytes()
        state.queued = {104: copy.deepcopy(queued[0])}
        peer = REF.upstream(state)
        until(lambda: rows() == [], 25, 'natural ConnectivityMonitor did not flush after reconnect')
        need(state.applied == [(REF.USER_A, 104)], 'reconnect applied wrong/duplicate award')
        need(any(r.get('function') == 'flush_pending_awards' and r.get('event') == 'call' and
                 r.get('thread') != 'MainThread' for r in events(fourth)), 'flush did not run on background worker')
        def rounds():
            return [r for r in events(fourth) if r.get('class') == 'CacheQueueWorker' and
                    r.get('function') == 'process_once' and r.get('event') == 'return']
        until(lambda: len(rounds()) >= 1, 70, 'natural first 60s queue poll absent')
        need(cache_queue_count() == 1 and not any(r['action'] == 'gameid' for r in state.calls), 'bulk lock did not hold queued work')
        fcntl.flock(bulk, fcntl.LOCK_UN)
        bulk.close()
        bulk = None
        until(lambda: len(rounds()) >= 2 and cache_queue_count() == 0, 70, 'next natural queue poll did not drain')
        need(any(r['action'] == 'gameid' for r in state.calls), 'queue worker did not use local peer')
        e = events(fourth)
        need(any(r.get('class') == 'FolderWatcher' and r.get('function') == 'process_once' and r.get('event') == 'return' for r in e), 'folder polling not observed')
        need(any(r.get('function') == 'report_if_due' and r.get('event') == 'return' and r.get('result') == 'False' for r in e), 'consent-disabled usage pass absent')
        need(not any(r.get('function') == 'run_pass' for r in e), 'unexpected hourly pass in bounded proof')
        need(state.applied == [(REF.USER_A, 104)] and not state.thread_errors, 'peer saw duplicate/error')
        REPORT['steps'].append('natural 15s reconnect and two 60s queue polls; real bulk lock; empty folder and no-consent usage rounds')
        REF.stop(peer)
        peer = None
        REF.ready()
        action('stop')
        final = properties()
        need(final['Result'] == 'success' and final['ExecMainCode'] == '1' and final['ExecMainStatus'] == '0', 'final stop forced/failed')
        gone(fourth, True)
        need(cgroup_members(REPORT['incarnations'][str(fourth)]['properties']['ControlGroup']) == [], 'service descendants remain')
        with sqlite3.connect('file:' + str(STATE / 'proxy.sqlite3') + '?mode=ro', uri=True) as db:
            need(db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok', 'final SQLite integrity failure')
        need(all(sha(STATE / name) == digest for name, digest in protected.items()), 'synthetic preferences/account files changed')
        REPORT['peer'] = {'calls': state.calls, 'applied': state.applied, 'errors': state.thread_errors}
        REPORT['requests'] = REF.REPORT['requests']
        REPORT['status'] = 'PASS'
    except BaseException as error:
        REPORT['error'] = type(error).__name__ + ': ' + str(error)
    finally:
        signal.alarm(30)
        if bulk is not None:
            bulk.close()
        if peer is not None:
            try:
                REF.stop(peer)
            except BaseException as error:
                REPORT['cleanup_errors'].append(str(error))
        if created:
            try:
                action('stop')
                p = properties()
                REPORT['final_unit'] = p
                need(p['ActiveState'] in ('inactive', 'failed') and p['MainPID'] == '0', 'fixture unit not stopped')
                for incarnation in REPORT.get('incarnations', {}).values():
                    need(not cgroup_members(incarnation['properties']['ControlGroup']), 'owned cgroup not empty')
                command(['journalctl', '--no-pager', '-u', UNIT, '-n', '200', '-o', 'json'])
                owned_unit()
                UNIT_FILE.unlink()
                DROP_FILE.unlink()
                DROP_DIR.rmdir()
                command(['systemctl', 'daemon-reload'])
                command(['systemctl', 'reset-failed', UNIT], allowed=(0, 1))
            except BaseException as error:
                REPORT['cleanup_errors'].append(str(error))
        if REPORT['cleanup_errors']:
            REPORT['status'] = 'FAIL'
        if 'REF' in globals():
            try:
                need(not REF.SERVERS, 'local peer remains registered')
                need(not [r for r in REF.tcp_listeners() if int(r[1].split(':')[1], 16) in (8080, 18081)],
                     'fixture listener remains')
                until(lambda: not [t for t in threading.enumerate() if t is not threading.main_thread()],
                      2, 'driver peer thread remains')
            except BaseException as error:
                REPORT['status'] = 'FAIL'
                REPORT['cleanup_errors'].append(str(error))
        REPORT['elapsed_seconds'] = time.monotonic() - started
        REPORT['retained_bytes'] = sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())
        if REPORT['retained_bytes'] > 16 * 1024**2:
            REPORT['status'] = 'FAIL'
            REPORT['cleanup_errors'].append('16MiB retained-data bound exceeded')
        dump(OUT / 'result.json', REPORT)
        signal.alarm(0)
        print(json.dumps({'status': REPORT['status'], 'result': str(OUT / 'result.json')}), flush=True)
    return 0 if REPORT['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
