import subprocess,os,sys,json,time,http.server,threading,socket,hashlib,urllib.parse
from pathlib import Path
r=Path(__file__).parent
ssh=['ssh','-i',str(r/'qa-key'),'-p','10570','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(r/'known_hosts'),'root@127.0.0.1']
events=[]
class Handler(http.server.BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  u=urllib.parse.urlsplit(self.path);q=urllib.parse.parse_qs(u.query)
  if u.path=='/event':
   events.append(dict(t=time.monotonic(),query=q));self.send_response(204);self.end_headers();return
  n=int(q.get('n',['0'])[0]);run=q.get('run',['none'])[0]
  js='''window.keep=new Uint8Array(80*1024*1024);window.keep.fill(19);
let tick=0;setInterval(()=>fetch('/event?run=RUN&n=N&tick='+(++tick)),1000);
document.querySelector('input').focus();document.addEventListener('keydown',e=>fetch('/event?run=RUN&n=N&key='+e.key));
if(N<3)setTimeout(()=>location.href='/page?run=RUN&n='+(N+1),16000);
'''.replace('RUN',run).replace('N',str(n))
  data=('<!doctype html><meta charset=utf-8><title>Memory fixture '+str(n)+'</title><body style="font:28px sans-serif;background:white;color:#123"><h1>Memory fixture '+str(n)+'</h1><input aria-label="QA input"><p>80 MiB touched array; three forward navigations.</p><script>'+js+'</script>').encode()
  self.send_response(200);self.send_header('Content-Type','text/html');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
port=server.server_address[1]
with (r/'measure.py').open('rb') as f:subprocess.run(ssh+['cat > /tmp/pressure-measure.py'],stdin=f,check=True)
cases=[('public-installed','/usr/bin/cloud-signin-window','https://www.dropbox.com/login',150,{}),('public-old-code','/tmp/qa-historical','https://www.dropbox.com/login',150,{}),('public-desktop','/tmp/qa-current','https://www.dropbox.com/login',120,{'QA_DESKTOP_UA':'1'}),('public-cache','/tmp/qa-current','https://www.dropbox.com/login',120,{'QA_DOCUMENT_VIEWER':'1'}),('synthetic-default','/tmp/qa-current','synthetic',75,{}),('synthetic-cache','/tmp/qa-current','synthetic',75,{'QA_DOCUMENT_VIEWER':'1'}),('synthetic-no-probe','/tmp/qa-current','synthetic',75,{'QA_NO_PROBE':'1'})]
(r/'cases.json').write_text(json.dumps(cases,indent=2))
results=[]
try:
 for case,binary,url,duration,env in cases:
  if url=='synthetic':url=f'http://10.0.2.2:{port}/page?run={case}&n=0'
  spec=json.dumps([case,binary,url,duration,env]);import shlex
  print('START '+case,flush=True)
  with (r/(case+'.json')).open('wb') as out,(r/(case+'.stderr')).open('wb') as err:
   p=subprocess.Popen(ssh+['python3 /tmp/pressure-measure.py '+shlex.quote(spec)],stdout=out,stderr=err)
   try:rc=p.wait(timeout=duration+70)
   except subprocess.TimeoutExpired:p.kill();p.wait();rc=124
  results.append(dict(case=case,rc=rc));(r/'progress.json').write_text(json.dumps(results,indent=2))
  if rc:raise RuntimeError(case+' rc='+str(rc))
  x=json.loads((r/(case+'.json')).read_text());assert x['samples'],case
  for frame in x['frames']:
   dst=r/(case+'-'+Path(frame['file']).name)
   with dst.open('wb') as f:subprocess.run(ssh+['cat '+shlex.quote(frame['file'])],stdout=f,check=True)
  peak=max(sum(p['pss_kib'] for p in row['processes'] if p['exe']!='emulationstation') for row in x['samples']);low=min(row['mem']['MemAvailable'] for row in x['samples'])
  print(f'DONE {case} peak_browser_PSS={peak}KiB minimum_available={low}KiB loaded={"load finished" in x["log"]}',flush=True)
  time.sleep(5)
finally:
 (r/'events.json').write_text(json.dumps(events,indent=2));server.shutdown();server.server_close()
print('MATRIX COMPLETE',flush=True)
