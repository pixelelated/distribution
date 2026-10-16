import json,time,threading
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
R=Path('/storage/qa587');lock=threading.Lock()
def log(v):
 with lock:
  with (R/'peer-events.jsonl').open('a') as f:f.write(json.dumps(dict(at=time.monotonic(),**v))+'\n')
class H(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_HEAD(self):self.send_response(200);self.end_headers();log({'method':'HEAD'})
 def do_GET(self):self.answer(parse_qs(urlparse(self.path).query),'GET')
 def do_POST(self):self.answer(parse_qs(self.rfile.read(int(self.headers.get('Content-Length','0'))).decode()),'POST')
 def answer(self,q,method):
  action=q.get('r',[''])[0];mode=(R/'peer-mode').read_text().strip();row={'method':method,'action':action,'mode':mode,'user':q.get('u',[''])[0],'achievement':q.get('a',[''])[0]};log(row)
  if action=='patch':
   g=int(q.get('g',['10'])[0]);v={'Success':True,'PatchData':{'ID':g,'Title':'Synthetic','Achievements':[{'ID':101 if g==10 else 201}]}}
  elif action=='unlocks':v={'Success':True,'UserUnlocks':[]}
  elif action=='startsession':v={'Success':True,'Unlocks':[],'HardcoreUnlocks':[]}
  elif action=='login2':v={'Success':True,'User':q.get('u',['fixture'])[0],'Token':'fixture-only'}
  else:v={'Success':True}
  raw=json.dumps(v).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers()
  try:
   if action=='awardachievement' and mode=='slow':
    (R/'peer-award-entered.json').write_text(json.dumps(row)+'\n')
    for b in raw:
     self.wfile.write(bytes([b]));self.wfile.flush();time.sleep(1.3)
   else:self.wfile.write(raw)
   log({'action':action,'response':'sent','mode':mode})
  except (BrokenPipeError,ConnectionResetError):log({'action':action,'response':'client-closed','mode':mode})
ThreadingHTTPServer(('127.0.0.1',19081),H).serve_forever()
