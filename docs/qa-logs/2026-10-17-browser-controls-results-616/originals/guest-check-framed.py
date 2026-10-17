#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
"""Fresh no-NIC QA guest only: bounded diagnostic-helper functional checks."""
import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import resource
import signal
import socket
import stat
import subprocess
import sys
import threading
import time
from urllib.parse import parse_qs, urlsplit

PORT = 18761
HTML_SHA256 = 'f33796db2c501d8c76226d90e8b1eeff5b8476db1a62cc89de983b6c517a45d1'
CASES = [('default-off-clean', 'default', 'off', 'clean'),
         ('default-on-clean', 'default', 'on', 'clean'),
         ('desktop-off-clean', 'desktop', 'off', 'clean'),
         ('desktop-on-clean', 'desktop', 'on', 'clean'),
         ('desktop-on-blocked', 'desktop', 'on', 'blocked'),
         ('desktop-on-hidden', 'desktop', 'on', 'hidden')]


def write_json(path, value):
    temporary = path.with_name(path.name + '.new')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def process(pid):
    try:
        values = Path('/proc', str(pid), 'stat').read_text().rsplit(')', 1)[1].split()
        return {'pid': int(pid), 'state': values[0], 'ppid': int(values[1]),
                'pgrp': int(values[2]), 'session': int(values[3]), 'start': int(values[19])}
    except (OSError, ValueError, IndexError):
        return None


def signal_identity(identity, number):
    try:
        descriptor = os.pidfd_open(identity['pid'])
    except ProcessLookupError:
        return False
    try:
        current = process(identity['pid'])
        if current and current['start'] == identity['start']:
            signal.pidfd_send_signal(descriptor, number)
            return True
    finally:
        os.close(descriptor)
    return False


def group_members(leader):
    members = []
    for entry in Path('/proc').iterdir():
        if entry.name.isdigit():
            row = process(int(entry.name))
            if row and row['session'] == leader and row['pgrp'] == leader:
                members.append(row)
    return members


def terminate_group(leader):
    events = []
    for number, duration in [(signal.SIGTERM, 1.0), (signal.SIGKILL, 1.0)]:
        until = time.monotonic() + duration
        while time.monotonic() < until:
            members = [row for row in group_members(leader) if row['state'] != 'Z']
            if not members:
                return events
            for row in members:
                if signal_identity(row, number):
                    events.append({'pid': row['pid'], 'start': row['start'], 'signal': int(number)})
            time.sleep(.1)
    return events


def memory_available():
    for line in Path('/proc/meminfo').read_text().splitlines():
        if line.startswith('MemAvailable:'):
            return int(line.split()[1])
    raise RuntimeError('MemAvailable missing')


def guard(owner):
    config = json.loads((owner / 'guard-config.json').read_text())
    result = {'pass': False, 'triggers': [], 'minimum_available_kib': None, 'error': None}
    started = time.monotonic()
    try:
        while not (owner / 'guard-stop').exists():
            now = time.monotonic()
            available = memory_available()
            previous = result['minimum_available_kib']
            result['minimum_available_kib'] = available if previous is None else min(previous, available)
            active = json.loads((owner / 'active.json').read_text()) if (owner / 'active.json').exists() else None
            parent = process(config['driver']['pid'])
            reason = None
            if not parent or parent['start'] != config['driver']['start']:
                reason = 'driver-exited-without-stop'
            elif available < 160 * 1024:
                reason = 'available-memory-below-160-MiB'
            elif now >= config['deadline']:
                reason = 'whole-deadline'
            elif active and now >= active['deadline']:
                reason = 'browser-case-deadline'
            if reason:
                trigger = {'reason': reason, 'at': now, 'available_kib': available}
                if active:
                    trigger['cleanup'] = terminate_group(active['pid'])
                result['triggers'].append(trigger)
                write_json(owner / 'abort.json', trigger)
                if reason == 'whole-deadline' and parent:
                    signal_identity(config['driver'], signal.SIGTERM)
                break
            write_json(owner / 'guard-heartbeat.json', {'at': now, 'pid': os.getpid(),
                                                       'available_kib': available})
            time.sleep(.1)
        result['pass'] = not result['triggers']
    except BaseException as error:
        result['error'] = str(error)
        write_json(owner / 'abort.json', {'reason': 'guard-error', 'error': str(error)})
        try:
            active = json.loads((owner / 'active.json').read_text())
            result['cleanup'] = terminate_group(active['pid'])
        except (OSError, ValueError):
            pass
    finally:
        result['seconds'] = time.monotonic() - started
        write_json(owner / 'guard-result.json', result)
    return 0 if result['pass'] else 1


def command(arguments, environment=None, timeout=5, check=True):
    result = subprocess.run(arguments, env=environment, capture_output=True,
                            text=True, timeout=timeout)
    if check and result.returncode:
        raise RuntimeError('command refused: ' + arguments[0] + ' exit ' + str(result.returncode))
    return result


def sway_environment():
    candidates = []
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit():
            continue
        try:
            if Path(os.readlink(entry / 'exe')).name != 'sway':
                continue
            identity = process(int(entry.name))
            raw = dict(item.split(b'=', 1) for item in (entry / 'environ').read_bytes().split(b'\0') if b'=' in item)
            runtime = Path(raw.get(b'XDG_RUNTIME_DIR', b'').decode())
            if not runtime.is_absolute() or not runtime.is_dir():
                continue
            displays = [p for p in runtime.glob('wayland-*') if p.is_socket()]
            ipc = [p for p in runtime.glob('sway-ipc.*.sock') if p.is_socket()]
            if len(displays) != 1 or len(ipc) != 1:
                raise RuntimeError('ambiguous Wayland or Sway sockets')
            env = dict(os.environ, XDG_RUNTIME_DIR=str(runtime),
                       WAYLAND_DISPLAY=displays[0].name, SWAYSOCK=str(ipc[0]),
                       GDK_BACKEND='wayland')
            # Retain explicit rendering selection from the actual compositor.
            for key in ['LIBGL_ALWAYS_SOFTWARE', 'GALLIUM_DRIVER', 'MESA_LOADER_DRIVER_OVERRIDE']:
                if key.encode() in raw:
                    env[key] = raw[key.encode()].decode()
            version = json.loads(command(['swaymsg', '-r', '-t', 'get_version'], env).stdout)
            if process(identity['pid'])['start'] != identity['start']:
                raise RuntimeError('Sway identity changed during discovery')
            candidates.append((identity, env, version))
        except (FileNotFoundError, ProcessLookupError):
            continue
    if len(candidates) != 1:
        raise RuntimeError('expected exactly one verified existing Sway session')
    return candidates[0]


def unit_state():
    return command(['systemctl', 'is-active', 'essway.service'], check=False).stdout.strip()


def wait_unit(expected, seconds=12):
    until = time.monotonic() + seconds
    while time.monotonic() < until:
        if unit_state() == expected:
            return True
        time.sleep(.2)
    return False


def samples(path):
    result = []
    for line in path.read_text(errors='replace').splitlines():
        if line.startswith('QA616_SAMPLE '):
            result.append(json.loads(line[len('QA616_SAMPLE '):]))
    return result


def run(args):
    os.umask(0o077)
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    # A 1 MiB inherited file-size limit killed the first control with SIGXFSZ.
    # Browser memfd/shared-memory backing files also use this ceiling.
    # Explicit diagnostic-log bounds remain below.
    resource.setrlimit(resource.RLIMIT_FSIZE, (128 * 1024 * 1024, 128 * 1024 * 1024))
    if sorted(p.name for p in Path('/sys/class/net').iterdir()) != ['lo']:
        raise RuntimeError('this driver requires the fresh no-NIC VM profile')
    if os.uname().machine != 'x86_64' or os.geteuid() != 0:
        raise RuntimeError('expected root inside the allocated x86_64 QA guest')
    helper = args.helper.resolve(strict=True)
    html = args.html.resolve(strict=True)
    if digest(helper.read_bytes()) != args.helper_sha256 or digest(html.read_bytes()) != HTML_SHA256:
        raise RuntimeError('staged helper or HTML hash mismatch')
    if not stat.S_ISREG(helper.stat().st_mode) or not os.access(helper, os.X_OK):
        raise RuntimeError('helper is not an executable regular file')
    owner = args.output
    if not owner.is_absolute() or not str(owner).startswith('/storage/'):
        raise RuntimeError('output must be a new absolute path below /storage')
    owner.mkdir(mode=0o700)
    (owner / 'frames').mkdir()
    result = {'schema': 1, 'scope': 'direct diagnostic launch; not ES handoff or performance proof',
              'pass': False, 'error': None, 'cases': [], 'restored_essway': None,
              'helper_sha256': args.helper_sha256, 'html_sha256': HTML_SHA256,
              'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip()}
    started = time.monotonic()
    write_json(owner / 'guard-config.json', {'driver': process(os.getpid()), 'deadline': started + 160})
    guard_log = (owner / 'guard.log').open('w')
    watcher = subprocess.Popen([sys.executable, '-I', str(Path(__file__).resolve()), '--guard', str(owner)],
                               stdout=guard_log, stderr=subprocess.STDOUT, start_new_session=True)
    server = None
    server_thread = None
    current = None
    initial_state = None
    guard_finished = False
    events = {}
    server_diagnostics = []
    events_lock = threading.Lock()
    base_html = html.read_text()
    # The companion's only HTML adaptation allows one same-origin proof POST.
    if base_html.count("connect-src 'none'") != 1 or base_html.count('</script>') != 1:
        raise RuntimeError('fixture transformation anchor mismatch')
    adapted = base_html.replace("connect-src 'none'", "connect-src 'self'")
    # Cover the complete viewport in the negative control regardless of font
    # wrapping; retain the original fixture otherwise.
    adapted = adapted.replace('</style>', '.blocked #mask { position:fixed; inset:0; width:auto; height:auto }\n</style>')
    injected = """
const qa616Case = new URLSearchParams(location.search).get('case_id');
const qa616Status = document.createElement('p');
qa616Status.style.fontSize = '16px';
document.body.appendChild(qa616Status);
const qa616SetStatus = value => { qa616Status.textContent = 'DOM proof: ' + value; };
qa616SetStatus('waiting');
document.addEventListener('securitypolicyviolation', () => qa616SetStatus('CSP blocked'));
let qa616Attempts = 0;
const qa616Report = () => {
  if (!(innerWidth > 0 && innerHeight > 0 && devicePixelRatio > 0)) {
    qa616SetStatus('waiting for viewport');
    if (++qa616Attempts < 100) setTimeout(qa616Report, 50);
    else qa616SetStatus('viewport unavailable');
    return;
  }
  qa616SetStatus('requested');
  try {
    fetch('/__qa616_dom', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({case_id:qa616Case, ua:navigator.userAgent,
                            width:innerWidth, height:innerHeight, scale:devicePixelRatio})
    }).then(response => qa616SetStatus('HTTP ' + response.status))
      .catch(() => qa616SetStatus('fetch rejected'));
  } catch (_) { qa616SetStatus('synchronous exception'); }
};
const qa616Schedule = () => requestAnimationFrame(qa616Report);
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded',qa616Schedule,{once:true});
else qa616Schedule();
"""
    adapted = adapted.replace('</script>', injected + '</script>')
    result['served_fixture_sha256'] = digest(adapted.encode())
    (owner / 'served-fixture.html').write_text(adapted)
    known = {case[0]: case for case in CASES}

    class Handler(BaseHTTPRequestHandler):
        protocol_version = 'HTTP/1.0'

        def log_message(self, *_arguments):
            pass

        def diagnostic(self, event, category):
            # Fixed categories only; never request paths, header values or bodies.
            with events_lock:
                if len(server_diagnostics) < 64:
                    server_diagnostics.append({'at': time.monotonic(), 'event': event, 'category': category})
                    write_json(owner / 'server-diagnostics.json', server_diagnostics)

        def respond(self, status, body=b'', kind='text/plain'):
            self.send_response(status)
            self.send_header('Content-Type', kind)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            self.diagnostic('GET', 'entered')
            location = urlsplit(self.path)
            query = parse_qs(location.query)
            case_id = query.get('case_id', [''])[0]
            mode = query.get('case', [''])[0]
            if location.path != '/fixture' or case_id not in known or mode != known[case_id][3]:
                self.diagnostic('GET', 'route-refused')
                self.respond(404)
                return
            ua = self.headers.get('User-Agent', '')
            if len(ua) > 512:
                self.diagnostic('GET', 'UA-size-refused')
                self.respond(400)
                return
            with events_lock:
                events.setdefault(case_id, {})['http'] = {
                    'ua_sha256': digest(ua.encode()), 'mobile': 'Mobile ' in ua,
                    'desktop_x11': '(X11; Linux ' in ua,
                    'webkit_tokens': 'AppleWebKit/605.1.15' in ua and 'Safari/605.1.15' in ua}
            self.respond(200, adapted.encode(), 'text/html; charset=utf-8')
            self.diagnostic('GET', 'fixture-served')

        def do_POST(self):
            origin = self.headers.get('Origin')
            self.diagnostic('POST', 'origin-missing' if origin is None else
                            'origin-matched' if origin == 'http://127.0.0.1:' + str(PORT) else 'origin-other')
            if self.path != '/__qa616_dom' or self.headers.get('Origin') != 'http://127.0.0.1:' + str(PORT):
                self.diagnostic('POST', 'route-or-origin-refused')
                self.respond(403)
                return
            value = None
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if length <= 0 or length > 1024:
                    raise ValueError('bounded request required')
                value = json.loads(self.rfile.read(length))
                if set(value) != {'case_id', 'ua', 'width', 'height', 'scale'} or value['case_id'] not in known:
                    raise ValueError('unexpected proof schema')
                if not isinstance(value['ua'], str) or len(value['ua']) > 512:
                    raise ValueError('unexpected UA')
                for name in ['width', 'height', 'scale']:
                    if not isinstance(value[name], (int, float)) or not 0 < value[name] <= 32768:
                        raise ValueError('invalid geometry')
                proof = {name: value[name] for name in ['width', 'height', 'scale']}
                proof['ua_sha256'] = digest(value['ua'].encode())
                with events_lock:
                    events.setdefault(value['case_id'], {})['dom'] = proof
                self.respond(204)
                self.diagnostic('POST', 'proof-accepted')
            except (ValueError, TypeError, KeyError):
                # Record only bounded structural facts and numeric geometry.
                details = {'object': isinstance(value, dict)}
                if isinstance(value, dict):
                    details.update(keys_match=set(value) == {'case_id', 'ua', 'width', 'height', 'scale'},
                                   known_case=isinstance(value.get('case_id'), str) and value.get('case_id') in known,
                                   ua_is_string=isinstance(value.get('ua'), str),
                                   ua_length=len(value['ua']) if isinstance(value.get('ua'), str) else None)
                    for field in ['width', 'height', 'scale']:
                        number = value.get(field)
                        details[field] = number if isinstance(number, (int, float)) and -32768 <= number <= 32768 else None
                write_json(owner / 'rejected-proof-shape.json', details)
                self.diagnostic('POST', 'proof-schema-refused')
                self.respond(400)

    def interrupted(_number, _frame):
        raise RuntimeError('driver interrupted; cleaning owned browser and restoring frontend')

    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)

    def guard_ok():
        if watcher.poll() is not None or (owner / 'abort.json').exists():
            raise RuntimeError('independent guard exited or triggered')
        heartbeat = json.loads((owner / 'guard-heartbeat.json').read_text())
        if time.monotonic() - heartbeat['at'] > 2:
            raise RuntimeError('independent guard heartbeat stale')

    try:
        until = time.monotonic() + 3
        while not (owner / 'guard-heartbeat.json').exists() and time.monotonic() < until:
            if watcher.poll() is not None:
                break
            time.sleep(.05)
        guard_ok()
        identity, environment, version = sway_environment()
        result['sway'] = {'identity': identity, 'version': version,
                          'environment': {key: environment[key] for key in ['XDG_RUNTIME_DIR', 'WAYLAND_DISPLAY', 'SWAYSOCK', 'GDK_BACKEND']}}
        initial_state = unit_state()
        if initial_state not in ['active', 'inactive']:
            raise RuntimeError('frontend unit in non-quiescent initial state')
        result['initial_essway'] = initial_state
        if initial_state == 'active':
            command(['systemctl', 'stop', '--no-block', 'essway.service'])
            if not wait_unit('inactive'):
                raise RuntimeError('frontend did not stop while preserving Sway')
        if process(identity['pid'])['start'] != identity['start']:
            raise RuntimeError('Sway changed after frontend stop')
        # Binding is the allocation check: no port substitution or reuse.
        server = HTTPServer(('127.0.0.1', PORT), Handler, bind_and_activate=True)
        server.timeout = .25
        server_thread = threading.Thread(target=server.serve_forever, kwargs={'poll_interval': .1}, daemon=True)
        server_thread.start()
        result['loopback_port'] = PORT
        for case_id, mode, observer, control in CASES:
            guard_ok()
            log_path = owner / (case_id + '.log')
            environment = {key: value for key, value in environment.items() if not key.startswith('QA616_') and not key.startswith('CLOUD_SIGNIN_')}
            environment.update(QA616_UA=mode, QA616_OBSERVER=observer, HOME='/storage')
            url = 'http://127.0.0.1:%d/fixture?case=%s&case_id=%s' % (PORT, control, case_id)
            case_started = time.monotonic()
            log = log_path.open('w')
            current = subprocess.Popen([str(helper), url, '127.0.0.1', '--no-auto-keyboard'],
                                       env=environment, stdout=log, stderr=subprocess.STDOUT,
                                       start_new_session=True)
            write_json(owner / 'active.json', {'pid': current.pid, 'identity': process(current.pid),
                                               'case': case_id, 'deadline': case_started + 15})
            row = {'id': case_id, 'ua_mode': mode, 'observer': observer, 'control': control,
                   'pid': current.pid, 'start': case_started}
            result['cases'].append(row)
            while time.monotonic() - case_started < 10:
                guard_ok()
                if current.poll() is not None:
                    raise RuntimeError('browser exited before functional observation')
                if log_path.stat().st_size > 512 * 1024:
                    raise RuntimeError('browser diagnostic log bound exceeded')
                with events_lock:
                    proof = dict(events.get(case_id, {}))
                observed = samples(log_path)
                if 'dom' in proof and 'http' in proof and (observed or observer == 'off'):
                    if time.monotonic() - case_started >= 5:
                        break
                time.sleep(.1)
            guard_ok()
            frame = owner / 'frames' / (case_id + '.png')
            capture = command(['grim', str(frame)], environment, timeout=3, check=False)
            row['frame'] = {'path': str(frame), 'capture_returncode': capture.returncode,
                            'sha256': digest(frame.read_bytes()) if frame.is_file() else None,
                            'visual_review': 'pending external review'}
            with events_lock:
                row['proof'] = dict(events.get(case_id, {}))
            row['samples'] = samples(log_path)
            row['cleanup_signals'] = terminate_group(current.pid)
            row['browser_returncode'] = current.wait(timeout=2)
            row['seconds'] = time.monotonic() - case_started
            current = None
            log.close()
            (owner / 'active.json').unlink(missing_ok=True)
            if any(entry['state'] != 'Z' for entry in group_members(row['pid'])):
                raise RuntimeError('owned browser group still has live members')
            proof = row['proof']
            checks = {'http_and_dom_ua_match': 'http' in proof and 'dom' in proof and proof['http']['ua_sha256'] == proof['dom']['ua_sha256'],
                      'webkit_identity': proof.get('http', {}).get('webkit_tokens', False),
                      'controlled_sigterm_exit': row['browser_returncode'] == -signal.SIGTERM,
                      'frame_captured_not_yet_reviewed': capture.returncode == 0 and frame.is_file(),
                      'samples_as_selected': bool(row['samples']) if observer == 'on' else not row['samples']}
            if mode == 'desktop':
                checks['desktop_applied'] = proof.get('http', {}).get('desktop_x11', False) and not proof.get('http', {}).get('mobile', True)
            if observer == 'on':
                final = row['samples'][-1] if row['samples'] else {}
                checks['ready_complete'] = final.get('ready') == 2
                checks['geometry_matches_dom'] = all(final.get(key) == proof.get('dom', {}).get(key) for key in ['width', 'height', 'scale'])
                checks['expected_input_hint'] = (final.get('hittable_text_inputs', -1) >= 1 if control == 'clean' else final.get('hittable_text_inputs') == 0)
            row['checks'] = checks
            row['pass'] = all(checks.values())
            write_json(owner / (case_id + '.json'), row)
            if not row['pass']:
                raise RuntimeError('functional assertion failed: ' + case_id)
        baseline = result['cases'][0]['proof']['dom']
        result['fixed_viewport'] = all(all(row['proof']['dom'][key] == baseline[key] for key in ['width', 'height', 'scale']) for row in result['cases'])
        result['default_desktop_identity_differs'] = result['cases'][0]['proof']['dom']['ua_sha256'] != result['cases'][2]['proof']['dom']['ua_sha256']
        result['visual_review_pending'] = True
        result['pass'] = result['fixed_viewport'] and all(row['pass'] for row in result['cases'])
    except BaseException as error:
        result['error'] = str(error)
    finally:
        if current:
            result['final_browser_cleanup'] = terminate_group(current.pid)
            try:
                result['final_browser_returncode'] = current.wait(timeout=2)
            except subprocess.TimeoutExpired:
                result['final_browser_returncode'] = None
                result['pass'] = False
        (owner / 'active.json').unlink(missing_ok=True)
        if server:
            server.shutdown()
            server.server_close()
        if server_thread:
            server_thread.join(timeout=1)
        try:
            if initial_state == 'active':
                command(['systemctl', 'start', '--no-block', 'essway.service'])
                result['restored_essway'] = wait_unit('active')
            else:
                result['restored_essway'] = initial_state == 'inactive' and unit_state() == 'inactive'
        except BaseException as error:
            result['restore_error'] = str(error)
            result['restored_essway'] = False
        (owner / 'guard-stop').touch()
        try:
            result['guard_returncode'] = watcher.wait(timeout=4)
            guard_finished = True
        except subprocess.TimeoutExpired:
            result['guard_cleanup'] = terminate_group(watcher.pid)
            result['guard_returncode'] = watcher.wait(timeout=2)
        guard_log.close()
        if (owner / 'guard-result.json').exists():
            result['guard'] = json.loads((owner / 'guard-result.json').read_text())
        result['pass'] = result['pass'] and result['restored_essway'] and guard_finished and result['guard_returncode'] == 0
        result['seconds'] = time.monotonic() - started
        write_json(owner / 'result.json', result)
    print(json.dumps({'pass': result['pass'], 'seconds': result['seconds'], 'error': result['error'],
                      'result': str(owner / 'result.json'), 'visual_review_pending': True}))
    return 0 if result['pass'] else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--guard', type=Path)
    parser.add_argument('--helper', type=Path)
    parser.add_argument('--helper-sha256')
    parser.add_argument('--html', type=Path)
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    if arguments.guard:
        raise SystemExit(guard(arguments.guard))
    if not all([arguments.helper, arguments.helper_sha256, arguments.html, arguments.output]):
        parser.error('--helper, --helper-sha256, --html and --output are required')
    raise SystemExit(run(arguments))
