#!/usr/bin/env python3
"""UNRUN: exact-identity local calibration input, independent of product page marker."""
import argparse
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
import stat
import time
import urllib.parse
import urllib.request

ROOT = Path('/storage/qa616-provider')
STATE = Path('/var/run/cloud_oauth')
CONFIG = Path('/run/qa616-provider/current.json')
HELPER_SHA = '8c3a9ba06dc78efffee68bb510b5f273f2fafc8d2ecbc8ee17227a3e4c1e3f0a'
SERVER_SHA = '640bf444f7a44ed55644519c5749d48df6ed63585c36c65018fc9a91e52bd4af'
PAGE_SHA = '5291483aee24ee0f620bde5e807a09a55735139ef9234ccde609c036573a6c31'

def private(path, maximum, allow_readable=False):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        meta = os.fstat(fd)
        if (not stat.S_ISREG(meta.st_mode) or meta.st_uid != 0
                or meta.st_mode & (0o022 if allow_readable else 0o077) or meta.st_size > maximum):
            raise ValueError('private input binding')
        with os.fdopen(fd, 'rb', closefd=False) as handle:
            return handle.read(maximum + 1)
    finally:
        os.close(fd)

def read_json(path, maximum=8192, allow_readable=False):
    return json.loads(private(path, maximum, allow_readable))

def digest(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()

def process(pid, start):
    if type(pid) is not int or type(start) is not int or pid <= 1 or start <= 0:
        raise ValueError('invalid process identity')
    root = Path('/proc', str(pid))
    fields = (root / 'stat').read_text().rsplit(')', 1)[1].split()
    if fields[0] == 'Z' or int(fields[19]) != start:
        raise ValueError('process identity changed')
    return root

def args(root):
    return [part.decode() for part in (root / 'cmdline').read_bytes().split(b'\0') if part]

def verify(echo, action):
    if os.geteuid() != 0 or os.uname().machine != 'x86_64':
        raise ValueError('disposable x86_64 guest only')
    root_meta = ROOT.lstat()
    if not stat.S_ISDIR(root_meta.st_mode) or root_meta.st_uid != 0 or root_meta.st_mode & 0o077:
        raise ValueError('private fixture root required')
    if echo.parent != ROOT or not re.fullmatch(r'echo-light[0-9]+', echo.name) or echo.is_symlink():
        raise ValueError('fresh local echo directory required')
    case = read_json(CONFIG, 2048)
    if (set(case) != {'id', 'provider', 'ua', 'observer'}
            or not isinstance(case['id'], str)
            or not re.fullmatch('[a-z0-9-]{1,64}', case['id'])
            or case['provider'] != 'light' or case['ua'] != 'default' or case['observer'] != 'off'):
        raise ValueError('not the fixed local light case')
    binding = read_json(ROOT / 'binding.json', 16384)
    if binding['helper_sha256'] != HELPER_SHA or binding['calibration_port'] != 18761:
        raise ValueError('candidate binding changed')
    launch = read_json(ROOT / 'launches' / (case['id'] + '.json'))
    if (launch['case'] != case or launch['helper_sha256'] != HELPER_SHA
            or launch['exec_argv0'] != '/usr/bin/cloud-signin-window'
            or launch['page_replaced_for_light_control'] is not True
            or launch['private_oauth_url_recorded'] is not False):
        raise ValueError('local launch receipt mismatch')
    browser = process(launch['pid'], launch['start'])
    argv = args(browser)
    expected = ['/usr/bin/cloud-signin-window',
                'http://127.0.0.1:18761/fixture?case=clean&case_id=' + case['id'],
                '127.0.0.1']
    if argv[:3] != expected or '--no-auto-keyboard' not in argv[3:] or digest(browser / 'exe') != HELPER_SHA:
        raise ValueError('helper is not the fixed loopback launch')
    tail = argv[3:]
    if not (tail == ['--no-auto-keyboard'] or
            len(tail) == 3 and tail[0] == '--exit-hint' and len(tail[1]) <= 128 and tail[2] == '--no-auto-keyboard'):
        raise ValueError('unexpected local helper options')
    if any(v.startswith(b'CLOUD_SIGNIN_DEBUG=') for v in (browser / 'environ').read_bytes().split(b'\0')):
        raise ValueError('debug environment forbidden')

    heartbeat = read_json(ROOT / 'guard-heartbeat.json')
    now = time.monotonic()
    if not 0 <= now - heartbeat['at'] < 2 or heartbeat['interventions'] != 0:
        raise ValueError('guard is not healthy')
    if (ROOT / 'guard-result.json').exists() or (ROOT / 'guard-stop').exists():
        raise ValueError('guard already ended')
    guard = process(heartbeat['pid'], heartbeat['start'])
    if (args(guard) != ['/usr/bin/python3', '-I', '-B', str(ROOT / 'guard.py')]
            or digest(ROOT / 'guard.py') != binding['files']['guard.py']):
        raise ValueError('guard process binding changed')
    # The sample binds a verified executable to THIS case, not merely any old launch.
    samples = private(ROOT / 'guard-samples.jsonl', 4 * 1024**2)
    lines = samples.split(b'\n')[:-1]  # Ignore a concurrently appended partial line.
    sample = json.loads(lines[-1])
    if not 0 <= now - sample['at'] < 2:
        raise ValueError('stale guard sample')
    row = next(row for row in sample['cases'] if row['id'] == case['id'])
    identity = {'pid': launch['pid'], 'start': launch['start']}
    if row['identity'] != identity or row['verified_at'] is None or not any(
            p['pid'] == launch['pid'] and p['start'] == launch['start'] for p in row['owned_live']):
        raise ValueError('guard has not verified this live helper')

    ready = read_json(echo / 'ready.json', allow_readable=True)
    owner = read_json(echo / 'owner.json')
    if (set(owner) != {'case', 'pid', 'start', 'ready_sha256'} or owner['case'] != case
            or owner['pid'] != ready['pid'] or owner['ready_sha256'] != digest(echo / 'ready.json')
            or ready['port'] != 18761 or ready['page_sha256'] != PAGE_SHA or ready['max_seconds'] != 240):
        raise ValueError('listener ready identity mismatch')
    server = process(owner['pid'], owner['start'])
    if (args(server) != ['/usr/bin/python3', '-I', '-B', str(ROOT / 'calibration-server.py'), '--output', str(echo)]
            or digest(ROOT / 'calibration-server.py') != SERVER_SHA or digest(ROOT / 'calibration.html') != PAGE_SHA):
        raise ValueError('listener source identity mismatch')
    # Confirm this exact server still owns the loopback-only TCP listener.
    inodes = set()
    for line in (server / 'net/tcp').read_text().splitlines()[1:]:
        columns = line.split()
        if columns[1] == '0100007F:4949' and columns[3] == '0A':
            inodes.add(columns[9])  # 18761 == 0x4949
    owned = {os.readlink(fd) for fd in (server / 'fd').iterdir()}
    if len(inodes) != 1 or not any('socket:[' + inode + ']' in owned for inode in inodes):
        raise ValueError('exact loopback listener ownership missing')
    events = read_json(echo / 'requests.json', 65536, allow_readable=True)
    if not isinstance(events, list) or not 2 <= len(events) <= 64:
        raise ValueError('local echo missing')
    if [event['route'] for event in events if event['route'] in ('original', 'final')] != ['original', 'final']:
        raise ValueError('local original-to-final navigation not observed')
    if any(event['route'] not in ('original', 'final', 'unknown') for event in events):
        raise ValueError('unexpected local fixture route')

    state = read_json(STATE / 'session.json', 65536, allow_readable=True)
    if state.get('backend') != 'dropbox' or state.get('status') != 'waiting' or (STATE / 'signed-in').exists():
        raise ValueError('authorization not waiting')
    if any(Path('/storage/.config/rclone').rglob('*')):
        raise ValueError('account configuration is not empty')
    if action == 'type-q' and not (STATE / 'field').exists():
        raise ValueError('native field focus marker absent')
    # The product deliberately omits every loopback URL from its page marker.
    # Fixed launch argv + bounded immutable local server/HTML prove this fixture.
    address = urllib.parse.urlsplit(state['address'])
    if address.scheme != 'http' or address.port != 8080 or address.username or address.password or address.path:
        raise ValueError('unexpected broker address')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
        probe.connect(('192.0.2.1', 9))  # Route lookup; no packet is sent.
        local = probe.getsockname()[0]
    if address.hostname != local or not ipaddress.ip_address(local).is_private:
        raise ValueError('broker must be this disposable guest')
    # Final identity/current-case checks immediately before the one local POST.
    process(launch['pid'], launch['start'])
    process(owner['pid'], owner['start'])
    process(heartbeat['pid'], heartbeat['start'])
    if read_json(CONFIG, 2048) != case:
        raise ValueError('case changed')
    return state, case

def main(action, echo):
    state, case = verify(echo, action)
    fields = {'pin': state['pin']}
    if action == 'type-q':
        fields['type'] = 'q'
    else:
        fields['key'] = {'backspace': 'backspace', 'tab': 'tab',
                         'activate-negative': 'enter', 'escape': 'escape'}[action]
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            return None
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    request = urllib.request.Request(state['address'] + '/',
        data=urllib.parse.urlencode(fields).encode(), method='POST',
        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    with opener.open(request, timeout=3) as response:
        if response.status != 204 or response.read(1):
            raise ValueError('unexpected broker response')
    print(json.dumps({'case': case['id'], 'action': action, 'broker_http_status': 204,
                      'local_identity_checks': 'passed', 'dom_delivery_proven_by_this_command': False}))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['type-q', 'backspace', 'tab', 'activate-negative', 'escape'])
    parser.add_argument('--echo', type=Path, required=True)
    options = parser.parse_args()
    try:
        main(options.action, options.echo)
    except Exception as error:
        print(json.dumps({'status': 'REFUSED', 'error_class': type(error).__name__}))
        raise SystemExit(1)
