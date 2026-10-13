from pathlib import Path
import json,tarfile,statistics,urllib.parse,hashlib
r=Path(__file__).parent
rows=[json.loads(l) for l in (r/'events.jsonl').read_text().splitlines()]
results=[]
def percentile(a,p):return sorted(a)[round((len(a)-1)*p)]
for name in ['none1','idle1','active1','active2','idle2','none2']:
 d=r/name;result=json.loads((d/'result.json').read_text());assert result['rc']==0
 with tarfile.open(d/'guest.tgz') as t:
  samples=[json.loads(l) for l in t.extractfile('./samples.jsonl').read().splitlines()]
  sr=json.load(t.extractfile('./sampler-result.json'));assert sr['rc']==0
  assert './guard.json' not in t.getnames()
 ev=[x for x in rows if x['run']==name]
 gaps=[g for x in ev if x['kind']=='heartbeat' for g in x['gaps']]
 browser=lambda p:p['exe'].startswith('WebKit') or p['exe']=='cloud-signin-window'
 groups=lambda tag,x:sum(p['pss'] for p in x['processes'] if (browser(p) if tag=='browser' else p['exe']==tag))/1024
 assert all(x['boot']==result['before']['boot'] for x in samples)
 assert any(p['tag']=='cloud_oauth wait' for x in samples for p in x['processes'])
 assert not any(browser(p) for p in samples[-1]['processes'])
 stats={'name':name,'load_seconds':result['loaded_seconds'],'samples':len(samples),'heartbeat_ms':{'p50':percentile(gaps,.5),'p95':percentile(gaps,.95),'maximum':max(gaps)},'available_mib':{'baseline_median':statistics.median(x['mem']['MemAvailable']/1024 for x in samples[:5]),'minimum':min(x['mem']['MemAvailable']/1024 for x in samples),'recovery_median':statistics.median(x['mem']['MemAvailable']/1024 for x in samples[-5:])},'browser_pss_peak_mib':max(groups('browser',x) for x in samples),'es_pss_mib':{'baseline':statistics.median(groups('emulationstation',x) for x in samples[:5]),'minimum':min(groups('emulationstation',x) for x in samples),'recovery':statistics.median(groups('emulationstation',x) for x in samples[-5:])},'sampler_seconds_max':max(x['sampling_seconds'] for x in samples),'vmstat_delta':{k:samples[-1]['vmstat'][k]-samples[0]['vmstat'][k] for k in samples[0]['vmstat']},'normal_es_wait_observed':True,'same_boot_and_frontend':True,'browser_children_gone':True}
 p=d/'phone-requests.json'
 if p.exists():
  req=json.loads(p.read_text());stats['phone']={'requests':len(req),'failed':sum(x.get('status') not in [200,204] for x in req),'typing':[]}
  for x in req:
   b=dict(urllib.parse.parse_qsl(x.get('body') or ''))
   if 'type' not in b:continue
   applied=next(v for v in ev if v['kind']=='input' and v['length']==len(b['type']) and v['received_wall_ms']>=x['issued'])
   movement=next((v for v in req if 'move=' in (v.get('body') or '') and v['issued']>=x['issued']),None)
   stats['phone']['typing'].append({'characters':len(b['type']),'post_to_ack_ms':x['ack']-x['issued'],'post_to_applied_event_received_ms':applied['received_wall_ms']-x['issued'],'page':applied['n'],'next_movement_post_after_typing_ack_ms':movement['issued']-x['ack'] if movement else None})
 results.append(stats)
(r/'analysis.json').write_text(json.dumps(results,indent=2)+'\n')
for s in results:print(s['name'],'load',round(s['load_seconds'],2),'heartbeat p95/max',s['heartbeat_ms']['p95'],s['heartbeat_ms']['maximum'],'browser MiB',round(s['browser_pss_peak_mib'],1),'available min',round(s['available_mib']['minimum'],1),'typed',[(x['page'],x['post_to_ack_ms']) for x in s.get('phone',{}).get('typing',[])])
