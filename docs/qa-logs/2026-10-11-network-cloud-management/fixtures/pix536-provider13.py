import importlib.machinery, importlib.util, sys, threading, http.server, signal, json
from pathlib import Path
sys.path.insert(0,'/usr/bin')
l=importlib.machinery.SourceFileLoader('qa_oauth','/usr/bin/cloud_oauth'); spec=importlib.util.spec_from_loader(l.name,l); c=importlib.util.module_from_spec(spec);l.exec_module(c)
ROOT=Path('/storage/qa537/browser13');ROOT.mkdir(exist_ok=True)
class Provider(http.server.BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  with (ROOT/'events.jsonl').open('a') as f:f.write(json.dumps({'host':self.headers.get('Host'),'path':self.path})+'\n')
  if self.path.startswith('/event'):
   self.send_response(204);self.end_headers();return
  if self.path.startswith('/popup'):
   body='<h1>Identity popup</h1><button onclick="opener.postMessage(\'fixture-done\',\'*\');window.close()">Finish sign-in</button>'
  elif self.path.startswith('/next'):
   body='<h1>Navigation arrived</h1><a href="http://dropbox.com:9977/">Back to provider</a>'
  else:
   body='''<style>body{margin:0;background:#fff;font:20px sans-serif}a,button,input{box-sizing:border-box;display:block;position:absolute;left:20px;width:570px;height:44px;font:20px sans-serif}a{padding:8px}button{top:70px}input{top:130px}</style>
<button id=button onclick="fetch('/event?button=clicked')">Click witness</button>
<input id=text oninput="fetch('/event?input='+encodeURIComponent(this.value))">
<a style="top:190px" href="http://login.microsoftonline.com:9977/next">Continue with Microsoft</a>
<a style="top:250px" href="http://accounts.google.com:9977/popup" target="auth">Continue with Google (popup)</a>
<a style="top:310px" href="http://unrelated.example:9977/next">Unrelated site (must be blocked)</a>
<script>addEventListener('message',()=>fetch('/event?popup=returned'))</script>'''
  body += '''<style>body{min-height:1800px}</style><script>
function witness(kind,value){fetch('/event?'+kind+'='+encodeURIComponent(value));}
for(const kind of ['mouseover','mousedown','mouseup','click'])addEventListener(kind,e=>{if(e.target.id)witness(kind,e.target.id)});
addEventListener('scroll',()=>witness('scroll',Math.round(scrollY)));
addEventListener('pageshow',()=>witness('ready',location.pathname));
</script>'''
  raw=('<!doctype html><meta charset=utf-8>'+body).encode();self.send_response(200);self.send_header('Content-Type','text/html');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
provider=http.server.ThreadingHTTPServer(('127.0.0.1',9977),Provider);threading.Thread(target=provider.serve_forever,daemon=True).start()
holder=c.SessionHolder('dropbox','qa-signin','Fixture',120);holder.pin='1234';holder.session=c.Session('dropbox','qa-signin',120);holder.session.provider='http://dropbox.com:9977/'
Path(c.STATE_DIR).mkdir(exist_ok=True);Path(c.state_path('phone-keyboard')).touch()
assert holder.start_browser()
(ROOT/'window.pid').write_text(str(holder.browser.proc.pid))
server=c.make_server('127.0.0.1',9978,holder,lambda:None)
(ROOT/'ready').write_text('ready\n')
signal.signal(signal.SIGTERM,lambda *_:sys.exit(0))
try:server.serve_forever()
finally:holder.end();server.server_close();provider.server_close()
