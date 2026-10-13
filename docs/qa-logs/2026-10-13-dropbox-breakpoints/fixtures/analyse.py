from pathlib import Path
import json,tarfile,statistics,collections
r=Path(__file__).parent;results=[]
def p95(xs):return sorted(xs)[int(.95*(len(xs)-1))]
for name in ['desktop360','handset768','desktop480','handset640','desktop640','handset480','desktop768','handset360']:
 d=r/name
 if not (d/'result.json').exists():continue
 record=json.loads((d/'result.json').read_text());xs=[json.loads(l[8:]) for l in (d/'window.log').read_text().splitlines() if l.startswith('QA_JSON ')];assert xs,name
 with tarfile.open(d/'guest.tgz') as t:samples=[json.loads(l) for l in t.extractfile('./samples.jsonl').read().splitlines()]
 browser=lambda x:sum(p['pss'] for p in x['processes'] if p['exe'] in ['cloud-signin-window','WebKitNetworkProcess','WebKitWebProcess'])/1024
 last=xs[-1];page=last['page'];resources=page['resources'];nav=page['navigation'];data={'name':name,'viewport':record['viewport'],'requested_width':record['requested_width'],'rc':record['rc'],'guarded':record['guarded'],'effective_ua':page['ua'],'page_path':page['path'],'geometry_email_field':page['emailVisible'],'max_heartbeat_ms':max(x['page']['heartbeatMax'] for x in xs),'eval_p95_ms':p95([x['eval_ms'] for x in xs]),'eval_max_ms':max(x['eval_ms'] for x in xs),'dom_loaded_ms':nav['dom'],'load_ms':nav['load'],'requested':last['requested'],'finished':last['finished'],'failed':last['failed'],'response_lengths_bytes':last['response_lengths'],'timed_resources':len(resources),'timing_types':dict(collections.Counter(x['kind'] for x in resources)),'timing_visible_encoded_bytes':sum(x['encoded'] for x in resources),'peak_browser_pss_mib':max(map(browser,samples)),'min_available_mib':min(x['mem']['MemAvailable']/1024 for x in samples),'available_recovery_mib':samples[-1]['mem']['MemAvailable']/1024,'normal_es_wait_observed':any(any(p['tag']=='cloud_oauth wait' for p in x['processes']) for x in samples),'same_frontend':record['before']==record['after'],'browser_last_sample_mib':browser(samples[-1]),'vmstat_delta':{k:samples[-1]['vmstat'][k]-samples[0]['vmstat'][k] for k in samples[0]['vmstat']}}
 results.append(data)
 print(name,'load',round(nav['load']),'heartbeat',round(data['max_heartbeat_ms']),'evalmax',round(data['eval_max_ms']),'PSS',round(data['peak_browser_pss_mib']),'avail',round(data['min_available_mib']),'requests',last['requested'],'lengths',last['response_lengths'])
(r/'analysis.json').write_text(json.dumps(results,indent=2)+'\n')
