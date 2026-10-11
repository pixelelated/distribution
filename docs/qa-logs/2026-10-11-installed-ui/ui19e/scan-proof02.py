from ui import *
import http.server,http.client,threading,shutil
art=P/'artifacts'; requests=[]; delay_next=True; delay_lock=threading.Lock()
class Proxy(http.server.BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def serve(self):
  if self.command not in ('PROPFIND','GET','HEAD','OPTIONS'):self.send_error(405);return
  body=self.rfile.read(int(self.headers.get('Content-Length','0')))
  global delay_next
  with delay_lock:
   delay=2 if delay_next else 0.05; delay_next=False
  time.sleep(delay)
  c=http.client.HTTPConnection('127.0.0.1',9010,timeout=30)
  headers={k:v for k,v in self.headers.items() if k.lower() not in ('host','connection','transfer-encoding')}
  try:
   c.request(self.command,self.path,body,headers);r=c.getresponse();data=r.read()
   self.send_response(r.status)
   for k,v in r.getheaders():
    if k.lower() not in ('connection','transfer-encoding','content-length'):self.send_header(k,v)
   self.send_header('Content-Length',str(len(data)));self.end_headers()
   if self.command!='HEAD':self.wfile.write(data)
   requests.append({'method':self.command,'path':self.path,'status':r.status})
  finally:c.close()
 do_PROPFIND=serve;do_GET=serve;do_HEAD=serve;do_OPTIONS=serve
class Server(http.server.ThreadingHTTPServer):allow_reuse_address=True
server=None
original=guest('cat /storage/.config/rclone/rclone.conf')+'\n'
assert ':9010' in original
python("from pathlib import Path\np=Path('/storage/.config/rclone/rclone.conf');p.write_text("+repr(original.replace(':9010',':9014'))+");p.chmod(0o600)")
# Only the owned synthetic transport is changed; selected pointers stay fixed.
cmd='sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/active-connection'
def manifest():return {str(x.relative_to(P/'cloud/data')):hashlib.sha256(x.read_bytes()).hexdigest() for x in (P/'cloud/data').rglob('*') if x.is_file()}
def scan_wait(name):
 for _ in range(90):
  if guest('test -f /storage/.cache/cloud_sync/scan/'+name+' && echo yes || true')=='yes':return
  time.sleep(1)
 raise RuntimeError('scan did not finish: '+name)
try:
 server=Server(('0.0.0.0',9014),Proxy);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 # Positive EN content, followed by truly empty FR content.
 rom=P/'cloud/data/pixelelated/Content/ROMs/nes/Cloud-UI.nes';rom.parent.mkdir(parents=True,exist_ok=True);rom.write_bytes(b'SYNTHETIC UI FIXTURE NOT A GAME')
 for locale,tag,positive in [('en_US','en2',True),('fr_FR','fr2',False)]:
  if not positive:rom.unlink();rom.parent.rmdir()
  restart(locale);before=guest(cmd);cloud_before=manifest();delay_next=True
  walk(tag+'-opening',HUB+'key down\nwait-for-change\nkey x\nwait-for-change 20 0\nshot running\n')
  scan_wait('done');walk(tag+'-options','settle\nshot options\n')
  delay_next=True
  walk(tag+'-content-selection','key down\nwait-for-change\nkey x\nwait-for-change 12 0\nkey down\nwait-for-change\nkey down\nwait-for-change\nkey down\nwait-for-change\nkey right\nwait-for-change\nshot continue\nkey x\nwait-for-change 20 0\nshot second-running\n')
  scan_wait('content-done');walk(tag+'-systems','settle\nshot '+('systems' if positive else 'empty')+'\n')
  (art/(tag+'-scan-facts.txt')).write_text(guest('cat /storage/.cache/cloud_sync/scan/settings /storage/.cache/cloud_sync/scan/scan /storage/.cache/cloud_sync/scan/done /storage/.cache/cloud_sync/scan/content-done')+'\n')
  assert guest(cmd)==before and manifest()==cloud_before
  print('PASS',tag,'scan sequence and preservation; frames require review',flush=True)
 (art/'scan-preservation02.json').write_text(json.dumps({'selected_paths_and_active_connection':True,'cloud_payloads_unchanged':True,'requests':requests},indent=2)+'\n')
 (art/'scan-workers02.json').write_text(python("import os,json\nrows=[]\nfor n in os.listdir('/proc'):\n if n.isdigit() and int(n)!=os.getpid():\n  try:\n   a=open('/proc/'+n+'/cmdline','rb').read().split(b'\\0'); a=[x.decode(errors='replace') for x in a if x]\n   if a and (a[0].endswith('/rclone') or (len(a)>1 and a[1]=='/usr/bin/cloud_scan')):rows.append({'pid':int(n),'argv':a})\n  except OSError:pass\nprint(json.dumps(rows,indent=2))\nassert not rows\n")+'\n')
finally:
 if server:server.shutdown();server.server_close()
 (art/'delay-proxy-requests02.json').write_text(json.dumps(requests,indent=2)+'\n')
 python("from pathlib import Path\np=Path('/storage/.config/rclone/rclone.conf');p.write_text("+repr(original)+");p.chmod(0o600)")
print('PASS actual scan command sequences and workers; semantic frame review pending',flush=True)
