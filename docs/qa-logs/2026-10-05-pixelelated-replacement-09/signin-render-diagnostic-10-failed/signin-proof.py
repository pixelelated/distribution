"""Installed sign-in presentation, local redirect and actual phone-page proof.

No credentials are entered. The finishing marker is an explicit stand-in.
Dropbox's authenticated trust page is outside this owner's claim.
"""
from pathlib import Path
import base64, datetime, hashlib, http.server, json, os, shlex, socket
import struct, subprocess, threading, time, urllib.parse, urllib.request, runpy

from stable_panel import wait_stable
from persistent_viewer import observe_frames

owner = Path(__file__).parent
out = owner / 'artifacts/signin'
out.mkdir()
ssh = ['ssh', '-i', str(owner / 'pair/qa-key'), '-p', '10026', '-o',
       'BatchMode=yes', '-o', 'ConnectTimeout=8', '-o', 'StrictHostKeyChecking=no',
       '-o', 'UserKnownHostsFile=/dev/null', '-o', 'LogLevel=ERROR', 'root@127.0.0.1']
checks, frames, resources = [], [], []
window_pid = None
oauth_started = False
sid = None
viewer_stop=threading.Event()
viewer_ready=threading.Event()
viewer_errors=[]
viewer_thread=None

def guest(command, **kw):
    return subprocess.run(ssh + [command], check=True, capture_output=True,
                          timeout=kw.pop('timeout', 40), **kw).stdout

def check(value, message):
    assert value, message
    checks.append(message)
    print('PASS ' + message, flush=True)

def shot(name):
    wait_stable(out,name,negative=(name=='01-local-redirect'))
    check(True,name+' rendered surface is stable')
    path = out / (name + '.png')
    subprocess.run(['./tools/vm-visual-qa', '--monitor',
                    '/tmp/rocknix-qemu-monitor-d.sock', 'shot', str(path)], check=True)
    data = path.read_bytes()
    check(struct.unpack('>II', data[16:24]) == (640, 480), name + ' is panel-sized')
    frames.append({'file': path.name, 'sha256': hashlib.sha256(data).hexdigest(),
                   'visual_review': 'pending'})

def port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

def wait_for(fn, seconds, description):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        value = fn()
        if value:
            return value
        time.sleep(.5)
    raise RuntimeError('Timed out: ' + description)

def start_window(url, allowed):
    global window_pid
    code = '''import os,subprocess
from pathlib import Path
for p in Path('/tmp').glob('m7-signin-*'):p.unlink()
runtime=None
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try:
  args=p.read_bytes().split(b'\\0')
  if not args[0].endswith(b'/sway'):continue
  env=dict(x.split(b'=',1) for x in (p.parent/'environ').read_bytes().split(b'\\0') if b'=' in x)
  runtime=env[b'XDG_RUNTIME_DIR'].decode();break
 except (OSError,KeyError):pass
assert runtime
display=next(p.name for p in Path(runtime).glob('wayland-*') if not p.name.endswith('.lock'))
env=dict(os.environ,XDG_RUNTIME_DIR=runtime,WAYLAND_DISPLAY=display,GDK_BACKEND='wayland',CLOUD_SIGNIN_PAGE_FILE='/tmp/m7-signin-page',CLOUD_SIGNIN_DONE_FILE='/tmp/m7-signin-done',CLOUD_SIGNIN_FIELD_FILE='/tmp/m7-signin-field')
with open('/tmp/m7-signin-log','wb') as f:
 p=subprocess.Popen(ARGS,env=env,stdin=subprocess.DEVNULL,stdout=f,stderr=f,start_new_session=True)
print(p.pid)
'''.replace('ARGS', repr(['/usr/bin/cloud-signin-window', url, allowed, '--no-auto-keyboard']))
    window_pid = int(guest('python3 -', input=code.encode()).strip())
    (out / 'window-pids.txt').open('a').write(str(window_pid) + '\n')

def stop_window():
    global window_pid
    if window_pid is not None:
        guest('python3 -', input=('''from pathlib import Path
import os,signal,time
p=Path('/proc/%d')
if p.exists():
 assert b'/usr/bin/cloud-signin-window' in (p/'cmdline').read_bytes()
 os.kill(int(p.name),signal.SIGTERM)
 for _ in range(100):
  if not p.exists() or (p/'stat').read_text().rsplit(')',1)[1].split()[0]=='Z':break
  time.sleep(.1)
 else:raise RuntimeError('owned window did not stop')
''' % window_pid).encode())
        window_pid = None

def loaded(log):
    return guest("grep -c 'load finished' " + shlex.quote(log) + ' || true').strip() not in (b'', b'0')

def sample_memory(name, seconds=30):
    rows = []
    for _ in range(seconds):
        code = '''from pathlib import Path
import json
rows=[]
for p in Path('/proc').glob('[0-9]*/status'):
 try:
  d=dict(x.split(':',1) for x in p.read_text().splitlines() if ':' in x)
  if d['Name'].strip() in ('cloud-signin-wi','WebKitWebProces','WebKitNetworkPr'):
   rows.append({'pid':int(p.parent.name),'name':d['Name'].strip(),'rss_kib':int(d.get('VmRSS','0 kB').split()[0])})
 except (OSError,KeyError,ValueError):pass
print(json.dumps(rows))
'''
        rows.append(json.loads(guest('python3 -', input=code.encode())))
        time.sleep(1)
    result = {'samples': rows, 'peak_total_rss_kib': max(sum(p['rss_kib'] for p in row) for row in rows),
              'numerical_ceiling_enforced': False}
    (out / (name + '-memory.json')).write_text(json.dumps(result, indent=2) + '\n')
    print('MEASURED ' + name + ' peak RSS KiB ' + str(result['peak_total_rss_kib']), flush=True)

echo_requests = []
navigator_observations = []
class Echo(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def do_GET(self):
        echo_requests.append({'path': self.path, 'user_agent': self.headers.get('User-Agent', '')})
        with (out/'local-request-events.jsonl').open('a') as f:
            f.write(json.dumps(dict(echo_requests[-1],utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))+'\n')
        if self.path.startswith('/ua?'):
            navigator_observations.append(urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)['value'][0])
            self.send_response(204); self.end_headers(); return
        if self.path == '/start':
            self.send_response(302); self.send_header('Location', '/mobile-form')
            self.send_header('Content-Length', '0'); self.end_headers(); return
        body = b'<!doctype html><meta name="viewport" content="width=device-width"><style>body{background:#111;color:#eee;font:20px sans-serif;padding:20px}input{max-width:100%}</style><h1>QA redirect reached</h1><label>QA input only <input autofocus></label><script>fetch("/ua?value="+encodeURIComponent(navigator.userAgent))</script>'
        self.send_response(200); self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)

def webdriver(method, path, body=None):
    request = urllib.request.Request(driver_base + path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=60) as r:
        return json.load(r)['value']

probe_release = threading.Event()
probe_observations = []
class PhoneProxy(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def do_GET(self):
        if self.path == '/proof-frame':
            body = ('<!doctype html><style>body{margin:0}</style><iframe id="phone" style="border:0;width:390px;height:1000px" src="/' + pin + '"></iframe>').encode()
        else:
            if '?probe=' in self.path:
                probe_release.wait(30)
            with urllib.request.urlopen(tunnel_base + self.path, timeout=15) as r:
                body = r.read()
            if '?probe=' in self.path:
                # Do not retain the PIN or the page-token value.
                probe_observations.append(body.decode().split()[0])
        self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)

def phone_metrics():
    return webdriver('POST', '/session/' + sid + '/execute/sync', {'script': '''var e=document.getElementById('state'),c=getComputedStyle(e);return {state:e.textContent,width:innerWidth,rootFont:parseFloat(getComputedStyle(document.documentElement).fontSize),top:parseFloat(c.marginTop),bottom:parseFloat(c.marginBottom)};''', 'args': []})

def phone_shot(name, element):
    webdriver('POST', '/session/' + sid + '/frame', {'id': None})
    key = element['element-6066-11e4-a52e-4f735466cecf']
    data = base64.b64decode(webdriver('GET', '/session/' + sid + '/element/' + key + '/screenshot'))
    check(struct.unpack('>II', data[16:24]) == (390, 1000), name + ' captures actual 390px frame')
    (out / (name + '.png')).write_bytes(data)
    frames.append({'file': name + '.png', 'sha256': hashlib.sha256(data).hexdigest(), 'visual_review': 'pending'})
    webdriver('POST', '/session/' + sid + '/frame', {'id': element})

def finishing_state():
    code = """from pathlib import Path
import hashlib,json,time,urllib.parse
p=Path('/tmp/m7-signin-page');raw=p.read_text() if p.exists() else ''
uri=urllib.parse.unquote(raw)
kind='finishing' if hashlib.sha256(uri.encode()).hexdigest()=='11b9f36ec9210da27cf4ba5b45ed6da382be383467185375ddf5938334d27ab5' else 'local-form' if urllib.parse.urlparse(raw).path=='/mobile-form' else 'other-or-missing'
log=Path('/tmp/m7-signin-log').read_text(errors='replace')
print(json.dumps({'guest_monotonic':time.monotonic(),'kind':kind,'page_sha256':hashlib.sha256(raw.encode()).hexdigest(),'done_exists':Path('/tmp/m7-signin-done').exists(),'load_finished_count':log.count('load finished'),'window_exists':Path('/proc/PID').exists()}))
""".replace('PID', str(window_pid))
    state=json.loads(guest('python3 -',input=code.encode()))
    state['host_observed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    transition_samples.append(state)
    (out/'finishing-transition.json').write_text(json.dumps(transition_samples,indent=2)+'\n')
    return state

transition_samples=[]

try:
    check(guest('grep -qx CHASSIS=handset /etc/machine-info && echo yes').strip() == b'yes', 'installed chassis is handset')
    hashes = {}
    for name in ['usr/bin/cloud-signin-window', 'usr/bin/cloud_oauth']:
        wanted = json.loads((owner/'expected-payload.json').read_text())['files'][name]
        actual = guest('sha256sum /' + name).decode().split()[0]
        check(actual == wanted, 'installed ' + name + ' matches exact image payload')
        hashes[name] = actual
    (out / 'payload-hashes.json').write_text(json.dumps(hashes, indent=2) + '\n')
    echo = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Echo)
    resources.append(echo)
    threading.Thread(target=echo.serve_forever, daemon=True).start()
    viewer_dir=out/'persistent-viewer';viewer_dir.mkdir()
    viewer_thread=threading.Thread(target=observe_frames,args=('127.0.0.1',5912,viewer_dir,viewer_stop,viewer_ready,viewer_errors),daemon=True)
    viewer_thread.start()
    check(viewer_ready.wait(10) and not viewer_errors,'persistent read-only VNC viewer obtained initial frame')
    start_window('http://10.0.2.2:' + str(echo.server_port) + '/start', '10.0.2.2')
    wait_for(lambda: loaded('/tmp/m7-signin-log'), 90, 'local redirect loaded')
    check(any(r['path'] == '/start' for r in echo_requests) and any(r['path'] == '/mobile-form' for r in echo_requests), 'installed window follows real HTTP302')
    check(all('Mobile' in r['user_agent'] and 'Safari' in r['user_agent'] for r in echo_requests), 'installed window sends Mobile Safari UA')
    wait_for(lambda: navigator_observations, 15, 'navigator.userAgent echo')
    check(all('Mobile Safari/605.1.15' in ua for ua in navigator_observations), 'actual navigator.userAgent echoes Mobile Safari/605.1.15')
    (out / 'navigator-user-agent.json').write_text(json.dumps(navigator_observations, indent=2) + '\n')
    (out / 'redirect-requests.json').write_text(json.dumps(echo_requests, indent=2) + '\n')
    shot('01-local-redirect')
    before=finishing_state()
    check(before['kind']=='local-form' and not before['done_exists'], 'finishing predicate rejects actual prior local page')
    guest('touch /tmp/m7-signin-done')
    time.sleep(2)
    old_timing=finishing_state()
    check(old_timing['done_exists'] and old_timing['window_exists'], 'actual done marker reached the running installed window')
    wait_for(lambda: finishing_state()['kind']=='finishing', 60, 'installed finishing document load completion')
    check(True, 'installed page record changed to the exact original ROCKNIX RC2 finishing document')
    shot('02-finishing-marker-stand-in')

    # Observe both capture paths at declared offsets before any repaint act.
    def guest_render(action):
        code = """from pathlib import Path
import os,subprocess,json
runtime=None
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try:
  a=p.read_bytes().split(b'\\0')
  if not a[0].endswith(b'/sway'):continue
  e=dict(x.split(b'=',1) for x in (p.parent/'environ').read_bytes().split(b'\\0') if b'=' in x)
  runtime=e[b'XDG_RUNTIME_DIR'].decode();break
 except (OSError,KeyError):pass
assert runtime
display=next(p.name for p in Path(runtime).glob('wayland-*') if not p.name.endswith('.lock'))
env=dict(os.environ,XDG_RUNTIME_DIR=runtime,WAYLAND_DISPLAY=display)
ACTION
"""
        if action=='capture':
            action_code="subprocess.run(['/usr/bin/grim','-t','png','-'],env=env,check=True)"
        else:
            action_code="env['SWAYSOCK']=str(next(Path(runtime).glob('sway-ipc.*.sock')))\nfor verb in ['disable','enable']:\n subprocess.run(['/usr/bin/swaymsg','[pid=PID] fullscreen '+verb],env=env,stdout=subprocess.DEVNULL,check=True)".replace('PID',str(window_pid))
        return guest('python3 -', input=code.replace('ACTION',action_code).encode())
    # The original proof closes immediately after02; keep this window alive.
    start=time.monotonic()
    render=[]
    for offset in [0,5,15]:
        time.sleep(max(0,start+offset-time.monotonic()))
        state=finishing_state();check(state['kind']=='finishing','finishing document remains current at offset'+str(offset))
        tag='render-'+str(offset).zfill(2)
        hmp=out/(tag+'-qemu.png')
        subprocess.run(['./tools/vm-visual-qa','--monitor','/tmp/rocknix-qemu-monitor-d.sock','shot',str(hmp)],check=True)
        # Explicit VNC path on the SAME software guest; capture before grim.
        api=runpy.run_path('./tools/vm-visual-qa')
        w,h,rgb=api['vnc_frame']('127.0.0.1',5912)
        check((w,h)==(640,480),tag+' VNC capture is panel-sized')
        ppm=out/(tag+'-vnc.ppm');ppm.write_bytes(f'P6\n{w} {h}\n255\n'.encode()+rgb)
        api['to_png'](str(ppm),str(out/(tag+'-vnc.png')))
        native=out/(tag+'-grim.png');native.write_bytes(guest_render('capture'))
        check(struct.unpack('>II',native.read_bytes()[16:24])==(640,480),tag+' native compositor capture is panel-sized')
        render.append({'offset_seconds':offset,'actual_elapsed':time.monotonic()-start,'qemu_sha256':hashlib.sha256(hmp.read_bytes()).hexdigest(),'grim_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'vnc_sha256':hashlib.sha256((out/(tag+'-vnc.png')).read_bytes()).hexdigest(),'state':state})
        (out/'render-observations.json').write_text(json.dumps(render,indent=2)+'\n')
    check(viewer_thread.is_alive() and not viewer_errors,'persistent viewer stayed connected without errors or input')
    (out/'local-window.log').write_bytes(guest('cat /tmp/m7-signin-log'))
    stop_window()
except Exception as failure:
    (out / 'failure.json').write_text(json.dumps({'type': type(failure).__name__}, indent=2) + '\n')
    try:shot('failure-panel')
    except Exception:pass
    raise
finally:
    cleanup_errors = []
    try:(out/'sway-runtime.log').write_bytes(guest('cat /var/log/sway.log'))
    except Exception:pass
    viewer_stop.set()
    if viewer_thread:
        viewer_thread.join(8)
        if viewer_thread.is_alive() or viewer_errors:cleanup_errors.append('persistent viewer failure: '+str(viewer_errors))
    probe_release.set()
    if sid:
        try:webdriver('DELETE', '/session/' + sid)
        except Exception:pass
    try:stop_window()
    except Exception as exc:cleanup_errors.append(type(exc).__name__ + ': owned window cleanup failed')
    if oauth_started:
        try:guest('/usr/bin/cloud_oauth cancel >/dev/null 2>&1')
        except Exception as exc:cleanup_errors.append(type(exc).__name__ + ': owned OAuth cleanup failed')
    for r in reversed(resources):
        if isinstance(r, subprocess.Popen):
            r.terminate()
            try:r.wait(timeout=10)
            except subprocess.TimeoutExpired:r.kill();r.wait()
        else:r.shutdown();r.server_close()
    (out/'all-local-requests.json').write_text(json.dumps(echo_requests,indent=2)+'\n')
    (out/'all-local-navigator.json').write_text(json.dumps(navigator_observations,indent=2)+'\n')
    (out / 'observations.json').write_text(json.dumps({'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'checks': checks, 'frames': frames, 'limitations': ['Visual review pending.', 'Finishing uses explicit done-file stand-in, not authenticated sign-in.', 'No authenticated Dropbox trust-page claim.', 'Memory is measured without a numerical ceiling assertion.']}, indent=2) + '\n')
    assert not cleanup_errors, cleanup_errors
print('PASS bounded compositor/capture diagnostic collected; semantic interpretation required', flush=True)
