"""Run only packaged proxy modules, with predecessor-written synthetic state."""
import os,json,sys,time,hashlib,subprocess,urllib.request,urllib.error
from pathlib import Path
root=Path('/storage/.cache/pixelelated-m7-subset-01');os.environ['RAOFFLINEPROXY_CONFIG_DIR']=str(root)
from raofflineproxy import config,storage,cache_keys,rom_cache,image_cache,auth
checks=[]
def check(ok,name):
 checks.append({'assertion':name,'passed':bool(ok)});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 (root/'assertions.json').write_text(json.dumps(checks,indent=2)+'\n');assert ok,name
check(config.__file__.startswith('/usr/lib/python3.14/site-packages/'),'actual packaged modules, no source override')
check(config.running_on_rocknix(),'packaged detector recognizes pixelelated')
check(config.detect_rocknix_system_cfg({})=='/storage/.config/system/configs/system.cfg','canonical account path is discovered without override')
before=json.loads((root/'before.json').read_text())
for i in range(2):
 st=storage.Storage()
 check(st.get_all_cache_by_prefix('')==before['cache'],f'reopen {i+1} retains all predecessor cache rows')
 check(st.get_pending_awards()==before['awards'],f'reopen {i+1} retains all predecessor pending rows')
 check(rom_cache.build_achievement_game_ids(st.get_all_cache_by_prefix(cache_keys.PREFIX_PATCH),st.get_all_cache_by_prefix(cache_keys.PREFIX_ACHIEVEMENTSETS))=={1:100,2:200},f'reopen {i+1} retains base/subset award mapping')
 check(st.load_login_credentials()=={'user':'QA','token':'<synthetic>'},f'reopen {i+1} retains synthetic cached sign-in')
 st.close()
check(image_cache.resolve_cached_static_asset('/Badge/old.png').read_bytes()==(root/'image_cache/static/Badge/old.png').read_bytes(),'legacy unsharded image path remains readable')
st=storage.Storage();cred=auth.resolve_credentials(st,{});st.close()
check(bool(cred and cred.get('user')=='QA' and cred.get('token')=='<synthetic>'),'packaged resolver reads canonical synthetic account automatically')
(root/'config.json').write_text(json.dumps({'proxy_host':'127.0.0.1','proxy_port':18080,'upstream_host':'http://127.0.0.1:9','cache_images':True,'upload_logs':False,'upload_usage_stats':False}))
# No default route exists in this disposable guest; upstream is also loopback.
log=(root/'service-private.log').open('wb')
p=subprocess.Popen(['/usr/bin/python3','-m','raofflineproxy.main','run-service'],env=dict(os.environ),stdout=log,stderr=subprocess.STDOUT)
(root/'owned-service.pid').write_text(str(p.pid)+'\n')
def get(path,as_json=True):
 req=urllib.request.Request('http://127.0.0.1:18080'+path,headers={'X-RA-Store-Only':'1'})
 with urllib.request.urlopen(req,timeout=5) as response:
  data=response.read();return json.loads(data) if as_json else data
try:
 for i in range(60):
  if p.poll() is not None:raise RuntimeError('packaged service exited before readiness')
  try:patch=get('/dorequest.php?r=patch&g=100&u=QA');break
  except (OSError,ValueError):time.sleep(.5)
 else:raise RuntimeError('packaged service did not become ready')
 check(patch.get('PatchData',{}).get('Title')=='old cached game','real packaged service serves inherited game cache')
 sets=get('/dorequest.php?r=achievementsets&m=abc&u=QA')
 check([x['GameId'] for x in sets['Sets']]==[100,200],'real service serves inherited base and subset sets')
 for game,achievement in [(100,1),(200,2)]:
  response=get(f'/dorequest.php?r=unlocks&g={game}&u=QA')
  check(achievement in response.get('UserUnlocks',[]),f'queued award remains visible in game {game}')
 check(get('/Badge/old.png',False)==(root/'image_cache/static/Badge/old.png').read_bytes(),'real service serves original legacy image bytes')
 st=storage.Storage();awards=st.get_pending_awards();st.close()
 check(len(awards)==2 and {x['achievementId'] for x in awards}=={1,2},'offline service retains both queued awards without flushing')
finally:
 p.terminate()
 try:p.wait(timeout=15)
 except subprocess.TimeoutExpired:p.kill();p.wait();raise
 log.close()
check(p.poll() is not None,'owned packaged service stops cleanly')
print('PASS packaged account discovery, predecessor cache/sign-in/queue reopen and offline HTTP service',flush=True)

# Real installed flusher, real loopback HTTP provider; never patch package functions.
from raofflineproxy import flusher
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import parse_qs,urlsplit
import threading,dataclasses
requests=[];accepted=set();permit_subset=False
class Provider(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):self.handle_api('GET')
 def do_POST(self):self.handle_api('POST')
 def handle_api(self,method):
  params=parse_qs(urlsplit(self.path).query)
  if method=='POST':params.update(parse_qs(self.rfile.read(int(self.headers.get('Content-Length','0'))).decode()))
  action=params.get('r',[''])[0];game=int(params.get('g',['0'])[0]);aid=int(params.get('a',['0'])[0])
  requests.append({'method':method,'action':action,'game':game,'achievement':aid})
  status=200
  if action=='patch' and game in (100,200):payload={'Success':True,'PatchData':{'ID':game,'Achievements':[{'ID':1 if game==100 else 2}]}}
  elif action=='unlocks' and game in (100,200):payload={'Success':True,'UserUnlocks':[a for a in accepted if a==(1 if game==100 else 2)]}
  elif action=='awardachievement' and aid in (1,2):
   if aid==2 and not permit_subset:status=503;payload={'Success':False,'Error':'synthetic temporary refusal'}
   else:accepted.add(aid);payload={'Success':True}
  else:status=400;payload={'Success':False,'Error':'unexpected synthetic request'}
  requests[-1]['status']=status
  data=json.dumps(payload).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
server=ThreadingHTTPServer(('127.0.0.1',0),Provider);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
local={'upstream_host':f'http://127.0.0.1:{server.server_port}','cache_images':False,'upload_logs':False,'upload_usage_stats':False}
check(Path(flusher.__file__).is_relative_to('/usr/lib/python3.14/site-packages/'),'flush uses installed module without source replacement')
st=storage.Storage()
try:
 first=flusher.flush_pending_awards(st,local)
 (root/'flush-first.json').write_text(json.dumps(dataclasses.asdict(first),indent=2)+'\n')
 check(first.flushed==1 and first.skipped_stale==0 and first.pending_remaining==1,'base accepted and temporarily refused subset stays pending, not stale')
 rows=st.get_pending_awards();subset=next(a for a in rows if a['achievementId']==2)
 check(subset['status']=='pending' and subset['retryCount']==1,'subset failure retains queued row with retry count')
 check({r['game'] for r in requests if r['action']=='patch'}=={100,200},'actual HTTP patch refresh includes the subset own game200')
 check(accepted=={1},'provider accepted only base before retry')
 permit_subset=True
 second=flusher.flush_pending_awards(st,local)
 (root/'flush-second.json').write_text(json.dumps(dataclasses.asdict(second),indent=2)+'\n')
 check(second.flushed==1 and second.skipped_stale==0 and second.pending_remaining==0,'installed retry flushes subset without stale deletion')
 check(accepted=={1,2} and sum(r['action']=='awardachievement' and r['achievement']==1 for r in requests)==1,'provider receives both awards without resending successful base')
 check(sum(r['action']=='awardachievement' and r['achievement']==2 for r in requests)==2,'subset has exactly refused and successful HTTP attempts')
 check(st.get_pending_awards()==[],'processed queue clears only after every award accepted')
 check(2 in json.loads(st.get_cache(cache_keys.unlocks(200,'QA'))['responseBody'])['UserUnlocks'],'subset unlock cache records actual accepted subset result')
 check(flusher.FLUSH_STAMP_FILE.read_text().split()[1]=='1','completed retry writes actual one-award flush stamp')
 count=len(requests);third=flusher.flush_pending_awards(st,local)
 check(third.total==0 and len(requests)==count,'empty repeat makes no provider request')
finally:
 st.close();server.shutdown();server.server_close();thread.join(timeout=5)
 (root/'provider-requests.json').write_text(json.dumps(requests,indent=2)+'\n')
check(not thread.is_alive(),'loopback provider stopped')
print('PASS installed subset refresh, temporary refusal, retention and HTTP retry',flush=True)
