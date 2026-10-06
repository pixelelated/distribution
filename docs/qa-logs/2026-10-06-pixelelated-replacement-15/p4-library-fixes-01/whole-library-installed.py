"""Actual installed helper/native hashing/storage/network, synthetic loopback provider.

No module functions, request timers or batching constants are replaced. The
indexed path and interrupted/retried unindexed path each prepare125 distinct
valid iNES fixtures. Persisted-pause/429 controls use only the local provider;
no hosted service or real account is involved.
"""
from pathlib import Path
import collections,hashlib,json,os,subprocess,sys,threading,time
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import parse_qs,urlsplit

root=Path('/storage/.cache/m7-whole-library-15');root.mkdir(exist_ok=False)
os.environ['RAOFFLINEPROXY_CONFIG_DIR']=str(root/'observer-config')
from raofflineproxy import cache_budget,cache_keys,cache_queue,config,network,rate_limit,rom_browser,rom_cache,storage
checks=[];requests=[];roms=[];hash_ids={};case='init';mode='normal';blocked=threading.Event();release=threading.Event()
def check(ok,name):
 checks.append(dict(case=case,assertion=name,passed=bool(ok)));(root/'assertions.json').write_text(json.dumps(checks,indent=2)+'\n');print(('PASS ' if ok else 'FAIL ')+case+': '+name,flush=True);assert ok,name
check(all(Path(m.__file__).is_relative_to('/usr/lib/python3.14/site-packages/raofflineproxy') for m in [cache_budget,cache_keys,cache_queue,config,network,rate_limit,rom_browser,rom_cache,storage]),'only packaged modules loaded')
check(network.RA_MIN_REQUEST_INTERVAL_SECONDS==.3 and network.SCAN_BATCH_SIZE==50 and network.SCAN_BATCH_COOLDOWN_SECONDS==30,'production request pacing and batch timers unchanged')
for i in range(1,126):
 p=root/'roms'/f'{i}.nes';p.parent.mkdir(exist_ok=True)
 prg=bytes([i])*16384;p.write_bytes(b'NES\x1a'+bytes([1,0])+bytes(10)+prg)
 hashes=rom_browser.hash_candidates_for_manual_cache(p)
 check(bool(hashes) and all(h not in hash_ids for h in hashes),'native distinct ROM hash '+str(i))
 for h in hashes:hash_ids[h]=i
 roms.append((i,hashes[0],p))

class Provider(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  params=parse_qs(urlsplit(self.path).query);action=params.get('r',[''])[0];h=params.get('m',[''])[0];game=int(params.get('g',['0'])[0]) or hash_ids.get(h,0)
  row=dict(case=case,action=action,game=game,at=time.monotonic(),status=200);requests.append(row)
  if len(requests)%25==0:print('HTTP progress',case,len(requests),'requests',flush=True)
  if mode=='interrupt' and action=='patch' and game==61:
   row['deliberately_blocked']=True;blocked.set();release.wait(timeout=120)
  if mode=='429' and action=='patch':row['status']=429;payload={'Success':False,'Error':'QA server pause'}
  elif action=='gameid':payload={'Success':True,'GameID':game}
  elif action=='patch':payload={'Success':True,'PatchData':{'ID':game,'Title':'QA game '+str(game),'Achievements':[]}}
  elif action=='unlocks':payload={'Success':True,'UserUnlocks':[]}
  elif action=='achievementsets':payload={'Success':True,'GameId':game,'Sets':[{'GameId':game,'Achievements':[]}]}
  else:row['status']=400;payload={'Success':False,'Error':'unexpected synthetic request'}
  body=json.dumps(payload).encode();self.send_response(row['status']);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)))
  if row['status']==429:self.send_header('Retry-After','1200')
  self.end_headers()
  try:self.wfile.write(body)
  except (BrokenPipeError,ConnectionResetError):pass

server=ThreadingHTTPServer(('127.0.0.1',0),Provider);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
def prepare(name,kind,count=125):
 p=root/name;p.mkdir();(p/'config.json').write_text(json.dumps(dict(upstream_host='http://127.0.0.1:'+str(server.server_port),cache_images=False,upload_logs=False,upload_usage_stats=False)))
 st=storage.Storage(database_path=p/'proxy.sqlite3');st.upsert_cache(cache_keys.login('QA'),json.dumps({'User':'QA','Token':'synthetic-local-only'}));st.close()
 jobs=p/'jobs.tsv';jobs.write_text(''.join(f'I\t{i}\t{h}\t{rom}\n' if kind=='I' else f'H\t\t\t{rom}\n' for i,h,rom in roms[:count]))
 return p
def launch(p,label):
 f=(p/(label+'.log')).open('wb');env=dict(os.environ,RAOFFLINEPROXY_CONFIG_DIR=str(p),RAOFFLINEPROXY_IMAGE_WAIT='0')
 child=subprocess.Popen(['/usr/bin/python3','/usr/bin/raofflineproxy-cache-indexed',str(p/'jobs.tsv')],env=env,stdout=f,stderr=subprocess.STDOUT)
 (p/(label+'.pid')).write_text(str(child.pid)+'\n');return child,f
def wait(child,output,bound=900):
 try:rc=child.wait(timeout=bound)
 except BaseException:
  child.terminate()
  try:child.wait(timeout=10)
  except subprocess.TimeoutExpired:child.kill();child.wait()
  raise
 finally:output.close()
 return rc
def rows(p):
 st=storage.Storage(database_path=p/'proxy.sqlite3')
 try:return {r['cacheKey']:r['responseBody'] for r in st.iter_cache_by_prefix(cache_keys.PREFIX_PATCH)}
 finally:st.close()
def ready(p,label,count=125):
 output=(p/(label+'.log')).read_text();check(sum(l.startswith('OK ') for l in output.splitlines())==count,'helper reports only actual completed games')
 st=storage.Storage(database_path=p/'proxy.sqlite3')
 try:
  check(len(st.cache_keys_by_prefix(cache_keys.PREFIX_PATCH))==count and cache_queue.count(st)==0,'all games stored and zero queued')
  for i,h,rom in roms[:count]:
   patch=st.get_cache(cache_keys.patch(i,'QA'));alias=st.get_cache(cache_keys.game_id(h));check(bool(patch and alias) and json.loads(alias['responseBody'])['GameID']==i and patch['sourceRomPath']==rom_browser.normalize_cached_rom_path(rom),'game '+str(i)+' patch/alias/source path exact')
 finally:st.close()
def pacing(records,batches):
 gaps=[b['at']-a['at'] for a,b in zip(records,records[1:])]
 check(bool(gaps) and min(gaps)>=.26,'actual local HTTP request spacing preserves production .3s throttle within scheduler tolerance')
 check(sum(x>=29 for x in gaps)>=batches,'actual provider observations include required thirty-second batch cooldowns')
 return dict(requests=len(records),min_interval=min(gaps),cooldowns=sum(x>=29 for x in gaps))

results=[]
try:
 case='indexed125';p=prepare(case,'I');start=len(requests);child,f=launch(p,'complete');check(wait(child,f)==0,'installed indexed helper exited0');ready(p,'complete');records=requests[start:];check(len(records)==375 and not any(r['action']=='gameid' for r in records),'indexed preparation makes three actual cache requests per game and no ROM lookup');results.append(dict(case=case,pacing=pacing(records,2)))
 case='unindexed125-interrupt';p=prepare(case,'H');mode='interrupt';start=len(requests);child,f=launch(p,'interrupted')
 try:
  check(blocked.wait(timeout=400),'actual game61 HTTP request reached mid-run interrupt boundary')
  child.terminate();check(wait(child,f,10)==-15,'real helper process stopped at the blocked provider call')
 finally:
  if child.poll() is None:child.terminate();wait(child,f,10)
  release.set();mode='normal'
 before=rows(p);check(len(before)==60,'sixty completed games preserved after actual process interruption')
 case='unindexed125-retry';child,f=launch(p,'retry');check(wait(child,f)==0,'fresh installed helper process retries successfully');ready(p,'retry');after=rows(p);check(all(after[k]==v for k,v in before.items()),'all previously completed game bytes remain unchanged')
 counts=collections.Counter(r['game'] for r in requests[start:] if r['action']=='patch');check(all(counts[i]==1 for i in range(1,61)),'retry does not fetch the sixty completed games again');results.append(dict(case=case,pacing=pacing(requests[start:],2)))
 case='persisted-pause';p=prepare(case,'H',3);st=storage.Storage(database_path=p/'proxy.sqlite3');cache_budget.pause_until(st,storage.current_millis()+600000);st.close();start=len(requests);child,f=launch(p,'paused');check(wait(child,f)==0,'paused helper completes with truthful per-game failures');text=(p/'paused.log').read_text();st=storage.Storage(database_path=p/'proxy.sqlite3');check('DONE cached=0 failed=3' in text and not any(l.startswith('OK ') for l in text.splitlines()) and cache_queue.count(st)==3 and not rows(p),'queued work is never reported ready');st.close();check(len(requests)==start,'persisted pause sends no HTTP requests')
 for kind in ['I','H']:
  case='actual429-'+kind;p=prepare(case,kind,3);mode='429';start=len(requests);child,f=launch(p,'refused');check(wait(child,f)==0,'429 produces completed helper with failed games');text=(p/'refused.log').read_text();check('DONE cached=0 failed=3' in text and not rows(p),'server429 produces no false readiness');events=requests[start:];check(sum(r['status']==429 for r in events)==1 and events[-1]['status']==429,'one429 stops subsequent actual provider requests');st=storage.Storage(database_path=p/'proxy.sqlite3');check(cache_budget.load(st).paused_until>storage.current_millis()+1190000,'real Retry-After pause persisted');st.close();n=len(requests);child,f=launch(p,'restart');check(wait(child,f)==0 and len(requests)==n and not rows(p),'new helper process respects persisted429 pause without sending');mode='normal'
 case='upstream-budget-control';p=prepare(case,'H',1);st=storage.Storage(database_path=p/'proxy.sqlite3');cache_budget.save(st,cache_budget.BudgetWindow(window_start=cache_budget.current_millis(),used=100));start=len(requests)
 try:
  result=rom_browser.add_rom_to_cache(roms[0][2],st,json.loads((p/'config.json').read_text()));check(result.success and result.queued and cache_queue.count(st)==1 and not rows(p) and len(requests)==start,'upstream default budget still queues at100 without claiming ready')
 finally:st.close()
finally:
 release.set();server.shutdown();server.server_close();thread.join(timeout=5)
 (root/'provider-requests.json').write_text(json.dumps(requests,indent=2)+'\n');(root/'pacing.json').write_text(json.dumps(results,indent=2)+'\n')
check(not thread.is_alive(),'local provider stopped')
print('PASS installed whole-library actual HTTP/native hashing, pacing, interruption/retry and persisted429 controls',flush=True)
