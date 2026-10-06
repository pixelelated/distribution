"""Exercise installed presentation with a local provider stand-in, no OAuth exchange.

The production SessionHolder, BrowserSession, handler, keyboard and done callback
are loaded from the immutable installed file. Only the provider Session object
is a fixture. No installed file or function is replaced. State stays in the
disposable guest and is never a real account sign-in.
"""
from pathlib import Path
import hashlib, importlib.machinery, importlib.util, json, os, signal, sys, threading, time, types, urllib.parse
root=Path('/tmp/m7-signin-presentation');root.mkdir(mode=0o700,exist_ok=False)
path='/usr/bin/cloud_oauth'
loader=importlib.machinery.SourceFileLoader('installed_cloud_oauth',path)
spec=importlib.util.spec_from_loader(loader.name,loader)
m=importlib.util.module_from_spec(spec);loader.exec_module(m)
assert not Path(m.STATE_DIR).exists(),'a sign-in already owns the guest'
Path(m.STATE_DIR).mkdir(mode=0o700)
Path(m.state_path('phone-keyboard')).touch()
holder=m.SessionHolder('dropbox','qa-local-presentation','QA local page',600)
holder.session=types.SimpleNamespace(provider=sys.argv[1],proc=None,collector=None,superseded=False)
server=m.make_server('0.0.0.0',8080,holder,lambda:None)
thread=threading.Thread(target=server.serve_forever,daemon=True)
stop=threading.Event()
signal.signal(signal.SIGTERM,lambda *_:stop.set())
signal.signal(signal.SIGINT,lambda *_:stop.set())
records=[]
def record(label):
 raw=Path(m.state_path('page')).read_text() if Path(m.state_path('page')).exists() else ''
 page=urllib.parse.unquote(raw)
 browser=holder.browser
 facts={'action':label,'monotonic':time.monotonic(),'language':m.signin_language(),
        'window_pid':browser.proc.pid if browser and browser.proc else None,
        'window_alive':bool(browser and browser.is_running()),
        'done_exists':Path(m.state_path('signed-in')).exists(),
        'page_sha256':hashlib.sha256(raw.encode()).hexdigest(),
        'is_finishing_fr':'Connect&eacute;' in page and 'Finalisation sur votre console' in page,
        'is_finishing_en':'<h1>Connected</h1>' in page and 'Finishing up on your handheld' in page}
 records.append(facts)
 (root/'observations.json').write_text(json.dumps(records,indent=2)+'\n')
 (root/'state.json').write_text(json.dumps(facts)+'\n')
thread.start()
try:
 assert m.browser_stack_available(),'installed display stack unavailable'
 assert holder.start_browser(),'installed BrowserSession refused the local page'
 (root/'private-connection.json').write_text(json.dumps({'pin':holder.pin,'port':server.server_port}))
 (root/'source.json').write_text(json.dumps({'installed_oauth_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'fixture':'provider Session only; actual installed presentation and done callback'}))
 deadline=time.monotonic()+600
 while not stop.is_set() and time.monotonic()<deadline:
  for label in ['signed-in','start-browser','stop-browser','quit']:
   action=root/('action-'+label)
   if not action.exists():continue
   action.unlink()
   if label=='signed-in':holder.signed_in()
   elif label=='start-browser':
    assert not Path(m.state_path('signed-in')).exists()
    assert holder.start_browser()
   elif label=='stop-browser':holder.stop_browser()
   else:stop.set()
   record(label)
  record('sample')
  stop.wait(.25)
finally:
 holder.stop_browser()
 server.shutdown();server.server_close();thread.join(timeout=10)
 assert not thread.is_alive()
 record('cleanup')
 (root/'fixture.rc').write_text('0\n')
