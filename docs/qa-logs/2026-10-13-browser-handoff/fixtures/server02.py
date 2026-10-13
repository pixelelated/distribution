from pathlib import Path
import http.server,urllib.parse,json,time,threading,signal,os
r=Path(__file__).parent
class Handler(http.server.BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def respond(self,body,status=200,ctype='text/html'):
  data=body.encode();self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
 def do_POST(self):
  data=json.loads(self.rfile.read(int(self.headers['Content-Length'])));data['received_wall_ms']=time.time()*1000;data['received_mono']=time.monotonic()
  with (r/'events.jsonl').open('a') as f:f.write(json.dumps(data)+'\n')
  self.respond('',204)
 def do_GET(self):
  u=urllib.parse.urlsplit(self.path);q=urllib.parse.parse_qs(u.query)
  if u.path=='/start':
   spec=json.loads((r/'case.json').read_text());self.send_response(302);self.send_header('Location','/page?run='+spec['name']+'&n=0');self.end_headers();return
  if u.path!='/page':self.respond('',404);return
  run=q['run'][0];n=int(q.get('n',['0'])[0]);assert run.replace('-','').isalnum() and 0<=n<=3
  js='''const run=RUN,n=N,start=performance.now();
const box=document.querySelector('input');let last=start,gaps=[],ticks=0;
function emit(x){fetch('/events',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({run,n,t:performance.now(),...x})}).catch(()=>{});}
window.keep=new Uint8Array(80*1024*1024);window.keep.fill(19);
box.focus();emit({kind:'loaded',allocation:window.keep.byteLength});
setInterval(()=>{const now=performance.now();gaps.push(now-last);last=now;ticks++;document.querySelector('#heartbeat').textContent='Heartbeat '+ticks;},100);
setInterval(()=>{emit({kind:'heartbeat',gaps:gaps.splice(0),length:box.value.length});},1000);
box.addEventListener('input',()=>emit({kind:'input',length:box.value.length,valid:/^a*$/.test(box.value)}));
document.addEventListener('mousemove',e=>emit({kind:'pointer',x:e.clientX,y:e.clientY}));
document.addEventListener('click',e=>emit({kind:'click',x:e.clientX,y:e.clientY}));
if(n<3)setTimeout(()=>location.href='/page?run='+run+'&n='+(n+1),20000);
'''.replace('RUN',json.dumps(run)).replace('n=N','n='+str(n))
  self.respond('<!doctype html><meta name="viewport" content="width=device-width"><title>QA handoff</title><style>body{background:#eef;color:#123;font:22px sans-serif;margin:24px}input{width:90%;font:24px monospace}#heartbeat{font-variant-numeric:tabular-nums}</style><h1>Browser control '+str(n)+'</h1><p>Local synthetic page. No account.</p><input id="qa" aria-label="QA input" autocomplete="off"><p id="heartbeat">Starting</p><p>80 MiB touched; navigation every 20 s.</p><script>'+js+'</script>')
server=http.server.ThreadingHTTPServer(('127.0.0.1',33375),Handler)
(r/'server02.pid').write_text(str(os.getpid()))
def stop(*a):threading.Thread(target=server.shutdown,daemon=True).start()
signal.signal(signal.SIGTERM,stop);timer=threading.Timer(2400,stop);timer.daemon=True;timer.start()
print('Local fixture listening on33375',flush=True)
try:server.serve_forever()
finally:server.server_close();(r/'server02-result.json').write_text(json.dumps({'rc':0,'ended':time.time()})+'\n')
